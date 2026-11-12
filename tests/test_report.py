import json
from pathlib import Path

from src.self_inspection_report import (
    compliance_rate,
    main,
    parse_checklist,
    render_markdown,
    summarize,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "sample_completed.md"


def _summary():
    return summarize(parse_checklist(FIXTURE.read_text()), report_date="2026-11-11")


def test_compliance_rate_excludes_na_and_unanswered():
    assert compliance_rate(3, 2) == 60.0
    assert compliance_rate(0, 0) is None
    assert compliance_rate(2, 1) == 66.7


def test_overall_counts():
    o = _summary()["overall"]
    assert (o["total"], o["yes"], o["no"], o["na"], o["not_answered"]) == (7, 3, 2, 1, 1)
    assert o["compliance_rate"] == 60.0
    assert o["complete"] is False


def test_section_rows():
    rows = {r["section"]: r for r in _summary()["sections"]}
    assert rows["117.7"]["compliance_rate"] == 66.7
    assert rows["117.15"]["compliance_rate"] is None


def test_findings_list_items_marked_no_with_notes():
    findings = _summary()["findings"]
    assert [f["item_id"] for f in findings] == ["PROC-05", "TRN-02"]
    assert "overdue" in findings[1]["notes"]


def test_markdown_contains_key_parts():
    md = render_markdown(_summary())
    assert "# Self-Inspection Summary: Larkspur Systems, Inc. (fictional)" in md
    assert "Personal study output" in md
    assert "| PROC-05 | 117.7(d) |" in md
    assert "TRN-03 (117.12(g))" in md
    assert "60.0%" in md


def test_cli_json_output_to_file(tmp_path, capsys):
    out = tmp_path / "report.json"
    code = main([str(FIXTURE), "--format", "json", "--output", str(out), "--date", "2026-11-11"])
    assert code == 0
    data = json.loads(out.read_text())
    assert data["report_date"] == "2026-11-11"
    assert data["overall"]["no"] == 2


def test_cli_fail_on_findings_returns_1(capsys):
    assert main([str(FIXTURE), "--fail-on-findings"]) == 1


def test_cli_missing_file_returns_2(tmp_path, capsys):
    assert main([str(tmp_path / "missing.md")]) == 2
    assert "error:" in capsys.readouterr().err


def test_cli_custom_company(capsys):
    main([str(FIXTURE), "--company", "Example Co (fictional)"])
    assert "Example Co (fictional)" in capsys.readouterr().out
