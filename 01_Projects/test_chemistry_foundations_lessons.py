from __future__ import annotations

import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHEMISTRY = ROOT / "02_Areas" / "Chemistry"
APP_ROOT = ROOT / "macOS" / "ColiDev"


def _sections(name: str) -> tuple[str, str]:
    markdown = (CHEMISTRY / "lessons" / f"{name}.md").read_text(encoding="utf-8")
    russian = markdown.split("## Русский", 1)[1].split("## English", 1)[0]
    english = markdown.split("## English", 1)[1].split("## Sources", 1)[0]
    return russian, english


def _answer(section: str, heading: str) -> str:
    return section.split(f"### {heading}", 1)[1].split("###", 1)[0].strip()


def test_chemistry_roadmap_links_both_foundations_lessons_in_order() -> None:
    roadmap = (CHEMISTRY / "curriculum.md").read_text(encoding="utf-8")
    foundations = roadmap.split("## База / Foundations", 1)[1].split("## Углубление", 1)[0]
    assert foundations.index("lesson:atoms_electrons_and_chemical_bonds") < foundations.index("lesson:water_hydrogen_bonds_and_ph")


def test_intro_element_shares_add_up_to_the_quoted_total() -> None:
    russian, english = _sections("intro")
    shares = {"oxygen": 65, "carbon": 18, "hydrogen": 10, "nitrogen": 3}
    assert sum(shares.values()) == 96
    assert "около 96 %" in russian and "65 %" in russian and "18 %" in russian
    assert "about 96%" in english and "65% oxygen" in english
    assert _answer(russian, "Ответ") == "1" and _answer(english, "Answer") == "1"


def test_carbon_bond_count_follows_from_its_electron_shells() -> None:
    electrons = 6
    inner, outer = 2, electrons - 2
    assert (inner, outer) == (2, 4) and 8 - outer == 4
    russian, english = _sections("atoms_electrons_and_chemical_bonds")
    assert "2 на внутренней оболочке и 4 на внешней" in russian and "четыре ковалентные связи" in russian
    assert "2 in the inner shell and 4 in the outer one" in english and "four covalent bonds" in english
    assert _answer(russian, "Ответ") == "1" and _answer(english, "Answer") == "1"


def test_ph_question_uses_the_logarithmic_scale() -> None:
    ratio = 10 ** (6 - 4)
    assert ratio == 100 and math.isclose(-math.log10(1e-4) - -math.log10(1e-6), -2)
    russian, english = _sections("water_hydrogen_bonds_and_ph")
    assert "10² = 100 раз" in russian and "10² = 100 times" in english
    # The neutral value is tied to 25 °C, because water's ionization depends on temperature.
    assert "25 °C" in russian and "меняется с температурой" in russian
    assert "25 °C" in english and "changes with temperature" in english
    assert _answer(russian, "Ответ") == "1" and _answer(english, "Answer") == "1"


def test_every_chemistry_lesson_cites_openstax_pages() -> None:
    for lesson in sorted((CHEMISTRY / "lessons").glob("*.md")):
        sources = lesson.read_text(encoding="utf-8").split("## Sources", 1)[1]
        assert re.search(r"\(https://openstax\.org/books/(?:chemistry|biology)-2e/pages/[0-9a-z-]+\)", sources), lesson.name


def test_chemistry_is_registered_in_the_app_and_backend() -> None:
    routes = json.loads((ROOT / "02_Areas" / "intro_lesson_routes.json").read_text(encoding="utf-8"))["routes"]
    assert {"subject_id": "chemistry", "resource": "intro", "progress_lesson_id": "intro.chemistry"} in routes
    models = (APP_ROOT / "App" / "AppModels.swift").read_text(encoding="utf-8")
    strings = (APP_ROOT / "App" / "L10n.swift").read_text(encoding="utf-8")
    assert "    case chemistry\n" in models and 'case .chemistry: return "flask.fill"' in models
    assert '"subject.chemistry": ("Химия", "Chemistry")' in strings and '"subject.chemistry.subtitle"' in strings
