#!/usr/bin/env python3
"""Reproducible retrieval check for ColiDev's local course RAG.

The question set lives in ``rag_eval_questions.json``. Each run indexes the
course corpus into a throwaway SQLite file, so the per-user index in
Application Support is never touched.

Examples::

    .venv/bin/python 01_Projects/rag_eval.py                        # keywords only
    .venv/bin/python 01_Projects/rag_eval.py --embedding-model bge-m3:latest
    .venv/bin/python 01_Projects/rag_eval.py --embedding-model bge-m3:latest --json out.json

Embeddings are requested only from a loopback Ollama endpoint.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

sys.path.insert(0, str(Path(__file__).resolve().parent))

import knowledge_index  # noqa: E402
from knowledge_index import KnowledgeIndex, OllamaEmbeddingProvider  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_PATH = Path(__file__).resolve().parent / "rag_eval_questions.json"
TOP_K = 4  # The tutor asks the course index for four excerpts.


def load_questions(path: Path = QUESTIONS_PATH) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload["questions"])


def _ranked_documents(results: list[dict[str, Any]]) -> list[str]:
    ranked: list[str] = []
    for result in results:
        if result["path"] not in ranked:
            ranked.append(result["path"])
    return ranked


def score_question(question: dict[str, Any], ranked_paths: list[str]) -> dict[str, Any]:
    relevant = set(question["relevant"])
    first_hit = next(
        (rank for rank, path in enumerate(ranked_paths, start=1) if path in relevant), None
    )
    return {
        "id": question["id"],
        "lang": question["lang"],
        "subject": question["subject"],
        "ranked": ranked_paths,
        "hit_at_1": first_hit == 1,
        "hit_at_k": first_hit is not None,
        "reciprocal_rank": 1 / first_hit if first_hit else 0.0,
        "main_lesson_found": question["relevant"][0] in ranked_paths,
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, float]:
    count = max(1, len(rows))
    return {
        "questions": len(rows),
        "hit_at_1": sum(row["hit_at_1"] for row in rows) / count,
        f"hit_at_{TOP_K}": sum(row["hit_at_k"] for row in rows) / count,
        "mrr": sum(row["reciprocal_rank"] for row in rows) / count,
        "main_lesson_found": sum(row["main_lesson_found"] for row in rows) / count,
    }


def _require_embeddings(index: KnowledgeIndex) -> None:
    """Stop instead of reporting keyword results as semantic ones."""
    if index.embedding_provider is not None and index._embedding_retry_after > time.monotonic():
        raise RuntimeError(
            "Ollama embeddings failed during the run, so search fell back to keywords; "
            "check that the embedding model is still installed"
        )


@contextmanager
def _fusion(**overrides: Any) -> Iterator[None]:
    """Temporarily change knowledge_index fusion constants (e.g. _LEXICAL_WEIGHT)."""
    previous = {name: getattr(knowledge_index, name) for name in overrides}
    for name, value in overrides.items():
        setattr(knowledge_index, name, value)
    try:
        yield
    finally:
        for name, value in previous.items():
            setattr(knowledge_index, name, value)


def run(
    *,
    embedding_model: str | None,
    ollama_url: str = "http://127.0.0.1:11434",
    questions: list[dict[str, Any]] | None = None,
    project_root: Path = PROJECT_ROOT,
    database_path: Path | None = None,
    fusion: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Score retrieval; reuse ``database_path`` to skip re-embedding the corpus.

    Every mode goes through the production ``refresh_and_search`` path, so the
    per-lesson excerpt limit and top-k are the ones the tutor sees.
    """
    questions = questions if questions is not None else load_questions()
    fusion = fusion or {}
    with tempfile.TemporaryDirectory(prefix="colidev-rag-eval-") as scratch:
        database_path = database_path or Path(scratch) / "knowledge.sqlite3"
        provider = (
            OllamaEmbeddingProvider(ollama_url, embedding_model, timeout_seconds=120)
            if embedding_model
            else None
        )
        lexical_index = KnowledgeIndex(project_root, database_path)
        status = lexical_index.refresh_sources()
        searches: dict[str, tuple[KnowledgeIndex, dict[str, Any]]] = {"lexical": (lexical_index, {})}

        warmup_seconds = None
        if provider is not None:
            index = KnowledgeIndex(project_root, database_path, embedding_provider=provider)
            started = time.perf_counter()
            embedded = index.warm_embeddings()
            warmup_seconds = time.perf_counter() - started
            if not embedded:
                raise RuntimeError(f"Ollama could not embed the corpus with {embedding_model}")
            searches["semantic"] = (index, {"_LEXICAL_WEIGHT": 0.0})
            searches["hybrid"] = (index, fusion)

        modes: dict[str, list[dict[str, Any]]] = {name: [] for name in searches}
        latencies: dict[str, list[float]] = {name: [] for name in searches}
        for question in questions:
            for name, (index, overrides) in searches.items():
                with _fusion(**overrides):
                    started = time.perf_counter()
                    results = index.refresh_and_search(question["question"], limit=TOP_K)
                    latencies[name].append(time.perf_counter() - started)
                _require_embeddings(index)
                modes[name].append(score_question(question, _ranked_documents(results)))

    return {
        "embedding_model": embedding_model,
        "fusion": {
            name: fusion.get(name, getattr(knowledge_index, name))
            for name in ("_RRF_K", "_LEXICAL_WEIGHT", "_SEMANTIC_WEIGHT", "_FUSION_CANDIDATES")
        },
        "document_count": status["document_count"],
        "top_k": TOP_K,
        "warmup_seconds": warmup_seconds,
        "median_query_seconds": {name: statistics.median(values) for name, values in latencies.items()},
        "summary": {name: summarize(rows) for name, rows in modes.items()},
        "by_language": {
            name: {
                lang: summarize([row for row in rows if row["lang"] == lang])
                for lang in sorted({row["lang"] for row in rows})
            }
            for name, rows in modes.items()
        },
        "questions": modes,
    }


def _print_report(report: dict[str, Any]) -> None:
    model = report["embedding_model"] or "keywords only"
    print(f"Model: {model}; documents: {report['document_count']}; top-k: {report['top_k']}")
    if report["embedding_model"]:
        print(f"Fusion: {report['fusion']}")
    if report["warmup_seconds"] is not None:
        print(f"Corpus embedding time: {report['warmup_seconds']:.1f} s")
    for name, summary in report["summary"].items():
        print(
            f"{name:>8}: hit@1 {summary['hit_at_1']:.0%}  hit@{TOP_K} {summary[f'hit_at_{TOP_K}']:.0%}"
            f"  MRR {summary['mrr']:.3f}  main lesson {summary['main_lesson_found']:.0%}"
            f"  median {report['median_query_seconds'][name]:.3f} s"
        )
    for name, rows in report["questions"].items():
        misses = [row["id"] for row in rows if not row["hit_at_k"]]
        if misses:
            print(f"{name:>8} misses: {', '.join(misses)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--embedding-model", help="Installed local Ollama embedding model, e.g. bge-m3:latest")
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    parser.add_argument("--json", type=Path, help="Write the full report to this JSON file")
    parser.add_argument(
        "--database", type=Path,
        help="Keep the throwaway index here to reuse vectors between runs (never the app's own index)",
    )
    parser.add_argument(
        "--questions", type=Path, default=QUESTIONS_PATH,
        help="Question set (default: rag_eval_questions.json; rag_eval_holdout_questions.json confirms tuning)",
    )
    parser.add_argument("--rrf-k", type=int, help="Override the fusion rank constant")
    parser.add_argument("--semantic-weight", type=float, help="Override the vector ranking weight")
    parser.add_argument("--candidates", type=int, help="Fuse only the top N chunks of each ranking")
    args = parser.parse_args(argv)

    fusion = {
        name: value
        for name, value in (
            ("_RRF_K", args.rrf_k),
            ("_SEMANTIC_WEIGHT", args.semantic_weight),
            ("_FUSION_CANDIDATES", args.candidates),
        )
        if value is not None
    }
    report = run(
        embedding_model=args.embedding_model,
        ollama_url=args.ollama_url,
        database_path=args.database,
        fusion=fusion,
        questions=load_questions(args.questions),
    )
    _print_report(report)
    if args.json:
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
