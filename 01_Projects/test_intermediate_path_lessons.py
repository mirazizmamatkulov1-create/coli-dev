from __future__ import annotations

import itertools
import math
from pathlib import Path


AREAS = Path(__file__).resolve().parents[1] / "02_Areas"


def _sections(subject: str, name: str) -> tuple[str, str]:
    markdown = (AREAS / subject / "lessons" / f"{name}.md").read_text(encoding="utf-8")
    russian = markdown.split("## Русский", 1)[1].split("## English", 1)[0]
    english = markdown.split("## English", 1)[1].split("## Sources", 1)[0]
    return russian, english


def _answer(section: str, heading: str) -> str:
    return section.split(f"### {heading}", 1)[1].split("###", 1)[0].strip()


def _linked(subject: str, resource: str) -> bool:
    roadmap = (AREAS / subject / "curriculum.md").read_text(encoding="utf-8")
    intermediate = roadmap.split("## Углубление / Intermediate", 1)[1].split("\n## ", 1)[0]
    return f"lesson:{resource}" in intermediate


def test_equilibrium_quotient_matches_the_source_example() -> None:
    quotient = (0.0040 * 0.0040) / (0.020 * 0.020)
    assert math.isclose(quotient, 0.040) and quotient < 0.64
    russian, english = _sections("Chemistry", "reaction_rate_and_equilibrium")
    assert "0,000016 / 0,0004 = 0,040" in russian and "0.000016 / 0.0004 = 0.040" in english
    # The catalyst point is stated as in Chemistry 2e 13.3: K is unchanged.
    assert "константа K не меняется" in russian and "the constant K does not change" in english
    assert _answer(russian, "Ответ") == "1" and _answer(english, "Answer") == "1"
    assert _linked("Chemistry", "reaction_rate_and_equilibrium")


def test_coin_microstates_match_the_entropy_lesson() -> None:
    five = list(itertools.product("HT", repeat=5))
    mixed = sum(1 for toss in five if toss.count("H") in (2, 3))
    assert (len(five), mixed) == (32, 20)
    four = list(itertools.product("HT", repeat=4))
    counts = {heads: sum(1 for toss in four if toss.count("H") == heads) for heads in range(5)}
    assert counts == {0: 1, 1: 4, 2: 6, 3: 4, 4: 1} and max(counts, key=counts.get) == 2
    russian, english = _sections("Physics", "entropy_and_the_second_law")
    assert "20 из 32" in russian and "6/16 = 37,5 %" in russian
    assert "20 of the 32" in english and "6/16 = 37.5%" in english
    assert "открытые системы" in russian and "open systems" in english
    assert _answer(russian, "Ответ") == "1" and _answer(english, "Answer") == "1"
    assert _linked("Physics", "entropy_and_the_second_law")


def test_hardy_weinberg_carrier_share() -> None:
    q = math.sqrt(0.16)
    p = 1 - q
    assert math.isclose(q, 0.4) and math.isclose(2 * p * q, 0.48) and math.isclose(p * p, 0.36)
    # Practice population: 49 YY, 42 Yy, 9 yy out of 100 gives p = 0.7 exactly in equilibrium.
    p_practice = (2 * 49 + 42) / 200
    assert math.isclose(p_practice, 0.7)
    assert [round(x * 100) for x in (p_practice ** 2, 2 * p_practice * (1 - p_practice), (1 - p_practice) ** 2)] == [49, 42, 9]
    russian, english = _sections("Biology", "population_genetics_hardy_weinberg")
    assert "2pq = 2 · 0,6 · 0,4 = 0,48" in russian and "2pq = 2 · 0.6 · 0.4 = 0.48" in english
    assert _answer(russian, "Ответ") == "1" and _answer(english, "Answer") == "1"
    assert _linked("Biology", "population_genetics_hardy_weinberg")


def test_matrix_vector_product_matches_the_lesson() -> None:
    weights = [[1, 2], [0, -1]]
    inputs = [3, 4]
    assert [sum(w * x for w, x in zip(row, inputs)) for row in weights] == [11, -4]
    assert sum(a * b for a, b in zip((1, 2, 3), (4, -5, 6))) == 12
    assert sum(a * b for a, b in zip((2, 1), (-1, 2))) == 0
    russian, english = _sections("Mathematics", "vectors_and_matrices")
    assert "h = g(Wx + b)" in russian and "h = g(Wx + b)" in english
    assert _answer(russian, "Ответ") == "1" and _answer(english, "Answer") == "1"
    assert _linked("Mathematics", "vectors_and_matrices")


def test_parallel_circuit_current() -> None:
    parallel = 1 / (1 / 2 + 1 / 6)
    assert math.isclose(parallel, 1.5) and math.isclose(12 / parallel, 8)
    assert math.isclose(12 / 2 + 12 / 6, 8) and math.isclose(12 / (2 + 6), 1.5)
    russian, english = _sections("Physics", "circuits_and_ohms_law")
    assert "I = 12 / 1,5 = 8 А" in russian and "I = 12 / 1.5 = 8 A" in english
    assert _answer(russian, "Ответ") == "1" and _answer(english, "Answer") == "1"
    assert _linked("Physics", "circuits_and_ohms_law")


def test_bacterial_doubling() -> None:
    assert 2 ** (180 // 30) == 64 and 24 * 60 // 30 == 48 and 2 ** (120 // 20) == 64
    russian, english = _sections("Biology", "microbial_growth_and_prokaryotes")
    assert "2⁶ = 64" in russian and "2⁶ = 64" in english
    assert "стационарной фазе" in russian and "stationary phase" in english
    assert _answer(russian, "Ответ") == "1" and _answer(english, "Answer") == "1"
    assert _linked("Biology", "microbial_growth_and_prokaryotes")


def test_counter_instances_keep_separate_state() -> None:
    russian, english = _sections("Programming", "python_classes_and_composition")
    code = russian.split("```python", 1)[1].split("```", 1)[0]
    question = russian.split("### Вопрос", 1)[1].split("```python", 1)[1].split("```", 1)[0]
    namespace: dict = {}
    exec(code + "\n" + question.replace("print(a.count)", "result = (a.count, b.count)"), namespace)
    assert namespace["result"] == (2, 1)
    assert "не проверяет" in russian and "does not check them at run time" in english
    assert _answer(russian, "Ответ") == "1" and _answer(english, "Answer") == "1"
    assert _linked("Programming", "python_classes_and_composition")


def test_http_status_classes() -> None:
    russian, english = _sections("Programming", "http_and_apis")
    for code in ("200 OK", "404 Not Found", "500 Internal Server Error"):
        assert code in russian and code in english
    # The lesson's example of ColiDev's own API must exist in the app source.
    models = (AREAS.parent / "macOS" / "ColiDev" / "App" / "AppModels.swift").read_text(encoding="utf-8")
    assert '"api/status"' in models and "GET /api/status" in russian and "GET /api/status" in english
    assert _answer(russian, "Ответ") == "1" and _answer(english, "Answer") == "1"
    assert _linked("Programming", "http_and_apis")
