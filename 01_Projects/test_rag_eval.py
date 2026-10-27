"""Checks for the reproducible RAG and tutor-model evaluation sets."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

import pytest

import rag_eval
import tutor_model_eval
from subject_rubrics import SUBJECT_RUBRICS

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_retrieval_questions_cover_both_languages_and_existing_lessons() -> None:
    questions = rag_eval.load_questions()

    assert 15 <= len(questions) <= 20
    assert len({question["id"] for question in questions}) == len(questions)
    assert {question["lang"] for question in questions} == {"ru", "en"}
    assert min(
        sum(question["lang"] == lang for question in questions) for lang in ("ru", "en")
    ) >= 7
    assert len({question["subject"] for question in questions}) >= 5
    for question in questions:
        assert question["question"].strip()
        assert question["relevant"]
        for path in question["relevant"]:
            assert path.startswith("02_Areas/") and path.endswith(".md")
            assert (PROJECT_ROOT / path).is_file(), f"{question['id']}: {path} is missing"


def test_scoring_uses_the_first_relevant_lesson_rank() -> None:
    question = {
        "id": "q", "lang": "en", "subject": "physics",
        "relevant": ["main.md", "also.md"],
    }

    row = rag_eval.score_question(question, ["other.md", "also.md", "main.md"])

    assert row["hit_at_1"] is False
    assert row["hit_at_k"] is True
    assert row["reciprocal_rank"] == 0.5
    assert row["main_lesson_found"] is True
    summary = rag_eval.summarize([row, rag_eval.score_question(question, [])])
    assert summary["hit_at_4"] == 0.5
    assert summary["mrr"] == 0.25


def test_keyword_only_retrieval_baseline_runs_offline() -> None:
    report = rag_eval.run(embedding_model=None)

    summary = report["summary"]["lexical"]
    assert set(report["summary"]) == {"lexical"}
    assert summary["questions"] == len(rag_eval.load_questions())
    # Keyword search found 15 of 20 lessons in the 2026-10-26 run; a large drop
    # means tokenisation or ranking regressed.
    # По словам находилось 15 из 20 уроков (прогон 2026-10-26); сильное падение
    # значит, что сломались токенизация или ранжирование.
    assert summary["hit_at_4"] >= 0.5


def test_eval_stops_instead_of_scoring_a_keyword_fallback_as_semantic(monkeypatch, tmp_path) -> None:
    project = tmp_path / "project"
    lesson = project / "02_Areas" / "Physics" / "lessons" / "heat.md"
    lesson.parent.mkdir(parents=True)
    lesson.write_text("# Heat\n\nQ = mcΔT gives the heat needed to warm water.\n", encoding="utf-8")

    class ModelRemovedMidRun:
        """Embeds the corpus, then fails like Ollama after its model is deleted."""

        def __init__(self, base_url: str, model: str, timeout_seconds: float = 12) -> None:
            self.model = f"fake:{model}"

        def embed(self, texts: list[str]) -> list[list[float]]:
            return [[1.0, 0.0] for _ in texts]

        def embed_query(self, text: str) -> list[list[float]]:
            raise ConnectionError("model 'bge-m3:latest' not found")

    monkeypatch.setattr(rag_eval, "OllamaEmbeddingProvider", ModelRemovedMidRun)
    question = {
        "id": "heat", "lang": "en", "subject": "physics",
        "question": "How much heat warms water?",
        "relevant": ["02_Areas/Physics/lessons/heat.md"],
    }

    with pytest.raises(RuntimeError, match="fell back to keywords"):
        rag_eval.run(embedding_model="bge-m3:latest", questions=[question], project_root=project)


@pytest.mark.skipif(
    os.environ.get("COLIDEV_RAG_EVAL_OLLAMA") != "1",
    reason="Set COLIDEV_RAG_EVAL_OLLAMA=1 to embed the course with local Ollama bge-m3 (about 2 minutes)",
)
def test_hybrid_retrieval_beats_keywords_with_local_bge_m3() -> None:
    report = rag_eval.run(embedding_model="bge-m3:latest")

    assert report["summary"]["hybrid"]["hit_at_4"] > report["summary"]["lexical"]["hit_at_4"]
    assert report["summary"]["hybrid"]["mrr"] > report["summary"]["lexical"]["mrr"]


def test_tutor_questions_are_russian_with_grading_notes() -> None:
    questions = tutor_model_eval.load_questions()

    assert 8 <= len(questions) <= 10
    assert len({question["id"] for question in questions}) == len(questions)
    for question in questions:
        assert question["subject"] in SUBJECT_RUBRICS
        assert question["expected"].strip()
        assert any("а" <= character <= "я" for character in question["question"].casefold())


def test_tutor_eval_uses_the_production_output_budget() -> None:
    import orchestrator

    assert tutor_model_eval.NUM_PREDICT == orchestrator.OLLAMA_NUM_PREDICT


def test_tutor_variant_parsing_keeps_production_payload_by_default() -> None:
    assert tutor_model_eval.parse_variant("qwen2.5-coder:7b") == {
        "label": "qwen2.5-coder:7b", "model": "qwen2.5-coder:7b",
    }
    assert tutor_model_eval.parse_variant("qwen3.5:latest,think=false")["think"] is False
    with pytest.raises(argparse.ArgumentTypeError):
        tutor_model_eval.parse_variant("qwen3.5:latest,temperature=0")
