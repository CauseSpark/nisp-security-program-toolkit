from pathlib import Path

import pytest

from src.self_inspection_report import ChecklistError, parse_checklist

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "sample_completed.md"
BLANK = ROOT / "checklists" / "self_inspection.md"


def test_parses_sections_and_items_from_fixture():
    sections = parse_checklist(FIXTURE.read_text())
    assert [s.number for s in sections] == ["117.7", "117.12", "117.15"]
    assert sum(len(s.items) for s in sections) == 7


def test_status_is_normalized_case_insensitively():
    sections = parse_checklist(FIXTURE.read_text())
    proc02 = next(i for i in sections[0].items if i.item_id == "PROC-02")
    assert proc02.status == "Yes"


def test_blank_status_means_not_answered():
    sections = parse_checklist(FIXTURE.read_text())
    trn03 = next(i for s in sections for i in s.items if i.item_id == "TRN-03")
    assert trn03.status == ""


def test_shipped_checklist_parses_and_is_blank():
    sections = parse_checklist(BLANK.read_text())
    items = [i for s in sections for i in s.items]
    assert len(items) > 20
    assert all(i.status == "" for i in items)


def test_shipped_checklist_covers_core_dcsa_sections():
    numbers = {s.number for s in parse_checklist(BLANK.read_text())}
    # Eight checklist areas DCSA's public NAESOC guidance lists as common to all companies.
    for core in ["117.7", "117.8", "117.9", "117.10", "117.11", "117.12", "117.13", "117.16"]:
        assert core in numbers


def test_invalid_status_raises_with_line_number():
    text = "## 117.7 Procedures\n| ID | Item | Ref | Status | Notes |\n|---|---|---|---|---|\n| PROC-01 | Q | 117.7 | Maybe | |\n"
    with pytest.raises(ChecklistError, match=r"line 4: PROC-01 has invalid status 'Maybe'"):
        parse_checklist(text)


def test_duplicate_ids_raise():
    text = "## 117.7 Procedures\n| PROC-01 | Q | 117.7 | Yes | |\n| PROC-01 | Q2 | 117.7 | No | |\n"
    with pytest.raises(ChecklistError, match="duplicate"):
        parse_checklist(text)


def test_item_before_section_raises():
    with pytest.raises(ChecklistError, match="before any"):
        parse_checklist("| PROC-01 | Q | 117.7 | Yes | |\n")


def test_empty_input_raises():
    with pytest.raises(ChecklistError, match="no checklist items"):
        parse_checklist("# Nothing here\n")


def test_missing_notes_column_is_tolerated():
    sections = parse_checklist("## 117.8 Reporting\n| REP-01 | Q | 117.8 | No |\n")
    assert sections[0].items[0].notes == ""
    assert sections[0].items[0].status == "No"
