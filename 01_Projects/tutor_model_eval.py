#!/usr/bin/env python3
"""Compare local Ollama tutor models on Russian questions with course RAG context.

Only the loopback Ollama endpoint is called; cloud routes are never used. The
prompt is built the way the local tutor route builds it: retrieved course
excerpts go into the learner message as JSON, and the system prompt is the
tutor's Russian language system prompt.

Example::

    .venv/bin/python 01_Projects/tutor_model_eval.py \\
        --embedding-model bge-m3:latest --json tutor-answers.json \\
        --variant qwen2.5-coder:7b --variant qwen3.5:latest --variant qwen3.5:latest,think=false

A variant is ``model`` or ``model,think=false``. Without ``think`` the request
matches what the tutor sends today.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import httpx  # noqa: E402

from knowledge_index import KnowledgeIndex, OllamaEmbeddingProvider  # noqa: E402
from subject_rubrics import add_subject_rubric  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_PATH = Path(__file__).resolve().parent / "tutor_eval_questions.json"
OLLAMA_URL = "http://127.0.0.1:11434"
NUM_PREDICT = 1024  # Same output budget as the tutor's Ollama requests.


def load_questions(path: Path = QUESTIONS_PATH) -> list[dict[str, Any]]:
    return list(json.loads(path.read_text(encoding="utf-8"))["questions"])


def parse_variant(value: str) -> dict[str, Any]:
    model, *options = [part.strip() for part in value.split(",")]
    variant: dict[str, Any] = {"label": value, "model": model}
    for option in options:
        key, _, raw = option.partition("=")
        if key != "think" or raw not in {"true", "false"}:
            raise argparse.ArgumentTypeError(f"Unsupported variant option: {option}")
        variant["think"] = raw == "true"
    return variant


def _orchestrator():
    # Keep the app's own per-user files untouched when the backend module loads.
    os.environ.setdefault("COLIDEV_DATA_DIR", tempfile.mkdtemp(prefix="colidev-tutor-eval-"))
    import orchestrator

    return orchestrator


def build_prompts(
    question: dict[str, Any], index: KnowledgeIndex
) -> tuple[str, str, list[dict[str, Any]]]:
    """Return (system, user) messages and the sources, as the local tutor route does."""
    orchestrator = _orchestrator()
    retrieval_query = f"{question['subject_name']} {question['question']}"
    course_sources = index.refresh_and_search(retrieval_query, 4)
    sources = orchestrator._combine_retrieval_sources(course_sources, [], official_sources=[])
    learner_message = orchestrator._augment_message_with_sources(question["question"], sources, "ru")
    tutor_guidance = add_subject_rubric(
        f"Ты — внимательный учебный тьютор. Предмет: {question['subject_name']}. "
        "Отвечай по-русски. Объясняй ясно и по шагам, подбирай глубину к вопросу. "
        "Не выдумывай источники и текущие факты.",
        question["subject"],
        "ru",
    )
    engine = orchestrator.ConsiliumEngine(None, "ru", None)
    # Mirrors ConsiliumEngine.stream_local.
    user_message = (
        "You are the local learning assistant powered by Ollama. "
        f"Answer in {engine.output_language}; explain carefully with useful examples. "
        "Be accurate and concise.\n\n"
        f"Tutor guidance: {tutor_guidance}\n\n"
        f"Learner question: {learner_message}"
    )
    return engine.language_system, user_message, sources


def _chat(client: httpx.Client, variant: dict[str, Any], system: str, user: str) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": variant["model"],
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "stream": True,
        "options": {"num_predict": NUM_PREDICT},
    }
    if "think" in variant:
        payload["think"] = variant["think"]
    started = time.perf_counter()
    first_content: float | None = None
    content: list[str] = []
    thinking: list[str] = []
    final: dict[str, Any] = {}
    with client.stream("POST", f"{OLLAMA_URL}/api/chat", json=payload) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line.strip():
                continue
            event = json.loads(line)
            message = event.get("message") or {}
            if message.get("thinking"):
                thinking.append(message["thinking"])
            if message.get("content"):
                if first_content is None:
                    first_content = time.perf_counter() - started
                content.append(message["content"])
            if event.get("done"):
                final = event
                break
    total = time.perf_counter() - started
    eval_count = final.get("eval_count")
    eval_seconds = (final.get("eval_duration") or 0) / 1e9
    return {
        "answer": "".join(content),
        "thinking_chars": len("".join(thinking)),
        "seconds_to_first_answer_token": first_content,
        "total_seconds": total,
        "prompt_tokens": final.get("prompt_eval_count"),
        "output_tokens": eval_count,
        "tokens_per_second": eval_count / eval_seconds if eval_count and eval_seconds else None,
        "done_reason": final.get("done_reason"),
    }


def _unload(client: httpx.Client, model: str) -> None:
    client.post(f"{OLLAMA_URL}/api/generate", json={"model": model, "keep_alive": 0}).raise_for_status()


def run(
    variants: list[dict[str, Any]],
    *,
    embedding_model: str | None,
    database_path: Path | None,
    questions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    questions = questions if questions is not None else load_questions()
    with tempfile.TemporaryDirectory(prefix="colidev-tutor-eval-") as scratch:
        provider = (
            OllamaEmbeddingProvider(OLLAMA_URL, embedding_model, timeout_seconds=120)
            if embedding_model
            else None
        )
        index = KnowledgeIndex(
            PROJECT_ROOT, database_path or Path(scratch) / "knowledge.sqlite3", provider
        )
        index.refresh_sources()
        if provider is not None and not index.warm_embeddings():
            raise RuntimeError(f"Could not embed the course with {embedding_model}")
        prompts = [build_prompts(question, index) for question in questions]

    results: dict[str, Any] = {"embedding_model": embedding_model, "variants": []}
    with httpx.Client(trust_env=False, timeout=httpx.Timeout(600, connect=5)) as client:
        if embedding_model:
            _unload(client, embedding_model)  # Leave unified memory to the chat model.
        for variant in variants:
            started = time.perf_counter()
            # An empty generate request only loads the model, so answer timings exclude it.
            client.post(f"{OLLAMA_URL}/api/generate", json={"model": variant["model"]}).raise_for_status()
            load_seconds = time.perf_counter() - started
            answers = []
            for question, (system, user, sources) in zip(questions, prompts, strict=True):
                print(f"{variant['label']}: {question['id']}", file=sys.stderr, flush=True)
                answer = _chat(client, variant, system, user)
                answer.update({
                    "id": question["id"],
                    "question": question["question"],
                    "expected": question["expected"],
                    "sources": [source["path"] for source in sources],
                })
                answers.append(answer)
            _unload(client, variant["model"])
            results["variants"].append({**variant, "load_seconds": load_seconds, "answers": answers})
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--variant", action="append", type=parse_variant, required=True)
    parser.add_argument("--embedding-model", help="Local embedding model for hybrid retrieval")
    parser.add_argument("--database", type=Path, help="Reuse a throwaway index built by rag_eval.py")
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args(argv)

    report = run(args.variant, embedding_model=args.embedding_model, database_path=args.database)
    args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for variant in report["variants"]:
        answers = variant["answers"]
        empty = sum(not answer["answer"].strip() for answer in answers)
        median = sorted(answer["total_seconds"] for answer in answers)[len(answers) // 2]
        print(f"{variant['label']}: median {median:.1f} s, empty answers {empty}/{len(answers)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
