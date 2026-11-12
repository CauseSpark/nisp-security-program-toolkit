"""Guardrail tests: keep the repo public-safe and self-consistent."""

import csv
import re
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = sorted((ROOT / "templates").glob("*.md"))
TRACKER = ROOT / "trackers" / "training_tracker.csv"
ALL_TEXT_FILES = [
    p for p in ROOT.rglob("*")
    if p.is_file() and p.suffix in {".md", ".csv", ".py", ".yml"} and ".git" not in p.parts
    and p.name != "test_repo_content.py"
]

EXPECTED_TEMPLATES = {
    "security_program_plan.md",
    "sop_visitor_control.md",
    "sop_incident_reporting.md",
    "insider_threat_program_outline.md",
    "training_plan.md",
}
TRACKER_COLUMNS = [
    "employee_id", "employee_name", "role", "course_id", "course_name", "rule_ref",
    "assigned_date", "due_date", "completed_date", "status",
]
TRACKER_STATUSES = {"Assigned", "Complete", "Overdue"}

# Classification or CUI banner markings must never appear in this public repo.
BANNER_RE = re.compile(r"\b(TOP SECRET|SECRET|CONFIDENTIAL|CUI)//|\(\s*(TS|S|C|CUI)\s*\)")


def test_all_expected_templates_exist():
    assert EXPECTED_TEMPLATES <= {p.name for p in TEMPLATES}


@pytest.mark.parametrize("path", TEMPLATES, ids=lambda p: p.name)
def test_templates_are_marked_study_material_and_fictional(path):
    text = path.read_text()
    assert "Personal study material" in text
    assert "fictional" in text.lower()


def test_readme_has_required_sections_and_disclaimer():
    readme = (ROOT / "README.md").read_text()
    for heading in ["## Purpose", "## Quick start", "## What this demonstrates", "## Disclaimer"]:
        assert heading in readme
    assert "personal study material" in readme.lower()
    assert "32 CFR Part 117" in readme


def test_no_classification_or_cui_banner_markings():
    offenders = [str(p.relative_to(ROOT)) for p in ALL_TEXT_FILES if BANNER_RE.search(p.read_text())]
    assert offenders == []


def test_links_to_official_sources_use_https():
    overview = (ROOT / "docs" / "overview.md").read_text()
    links = re.findall(r"\]\((https?://[^)\s]+)", overview)
    assert links, "overview should link to sources"
    assert all(link.startswith("https://") for link in links)
    assert any("ecfr.gov" in link for link in links)
    assert any("dcsa.mil" in link for link in links)


def test_training_tracker_schema_and_values():
    with TRACKER.open(newline="") as fh:
        reader = csv.DictReader(fh)
        assert reader.fieldnames == TRACKER_COLUMNS
        rows = list(reader)
    assert rows
    for row in rows:
        assert row["status"] in TRACKER_STATUSES
        assert "(fictional)" in row["employee_name"]
        assert row["rule_ref"].startswith("117.")
        date.fromisoformat(row["due_date"])
        if row["status"] == "Complete":
            date.fromisoformat(row["completed_date"])
        else:
            assert row["completed_date"] == ""


def test_relative_links_in_templates_resolve():
    broken = []
    for path in TEMPLATES:
        for target in re.findall(r"\]\(((?!https?://)[^)#\s]+)", path.read_text()):
            if not (path.parent / target).resolve().exists():
                broken.append(f"{path.name} -> {target}")
    assert broken == []
