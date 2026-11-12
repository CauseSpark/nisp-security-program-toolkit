"""Turn a completed self-inspection checklist into a summary report.

Personal study tool. It reads the Markdown checklist format used in
checklists/self_inspection.md and produces a Markdown or JSON summary:
per-section counts, a compliance rate, open findings, and unanswered items.

Usage:
    python src/self_inspection_report.py CHECKLIST.md [--company NAME]
        [--format md|json] [--output FILE] [--fail-on-findings]

Exit codes: 0 = ok, 1 = findings present and --fail-on-findings set,
2 = input error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

VALID_STATUSES = {"yes": "Yes", "no": "No", "n/a": "N/A", "na": "N/A", "": ""}
SECTION_RE = re.compile(r"^##\s+(117\.\d+)\s+(.*?)\s*$")
ITEM_ID_RE = re.compile(r"^[A-Z]{2,6}-\d{2,3}$")

DISCLAIMER = (
    "Personal study output. Not an official DCSA product and not a substitute for the "
    "DCSA Self-Inspection Handbook or the current text of 32 CFR Part 117."
)


class ChecklistError(ValueError):
    """Raised when the checklist cannot be parsed."""


@dataclass
class Item:
    item_id: str
    question: str
    ref: str
    status: str  # "Yes", "No", "N/A", or "" (not answered)
    notes: str
    section: str


@dataclass
class Section:
    number: str
    title: str
    items: list[Item] = field(default_factory=list)

    def count(self, status: str) -> int:
        return sum(1 for i in self.items if i.status == status)


def _split_row(line: str) -> list[str]:
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def parse_checklist(text: str) -> list[Section]:
    """Parse checklist Markdown into sections and items."""
    sections: list[Section] = []
    current: Section | None = None
    seen_ids: set[str] = set()

    for lineno, raw in enumerate(text.splitlines(), start=1):
        heading = SECTION_RE.match(raw)
        if heading:
            current = Section(number=heading.group(1), title=heading.group(2))
            sections.append(current)
            continue
        if not raw.lstrip().startswith("|"):
            continue
        cells = _split_row(raw)
        if not cells or not ITEM_ID_RE.match(cells[0]):
            continue  # header or separator row
        if current is None:
            raise ChecklistError(f"line {lineno}: item {cells[0]} appears before any '## 117.x' section")
        if len(cells) < 4:
            raise ChecklistError(f"line {lineno}: expected ID | Item | Ref | Status | Notes")
        while len(cells) < 5:
            cells.append("")
        item_id, question, ref, status_raw, notes = cells[:5]
        key = status_raw.lower()
        if key not in VALID_STATUSES:
            raise ChecklistError(
                f"line {lineno}: {item_id} has invalid status '{status_raw}' (use Yes, No, N/A, or blank)"
            )
        if item_id in seen_ids:
            raise ChecklistError(f"line {lineno}: duplicate item ID {item_id}")
        seen_ids.add(item_id)
        current.items.append(
            Item(item_id, question, ref, VALID_STATUSES[key], notes, current.number)
        )

    sections = [s for s in sections if s.items]
    if not sections:
        raise ChecklistError("no checklist items found")
    return sections


def compliance_rate(yes: int, no: int) -> float | None:
    """Percent of applicable, answered items marked Yes. None if nothing applicable."""
    answered = yes + no
    return None if answered == 0 else round(100.0 * yes / answered, 1)


def summarize(sections: list[Section], company: str = "Larkspur Systems, Inc. (fictional)",
              report_date: str | None = None) -> dict:
    rows = []
    totals = {"Yes": 0, "No": 0, "N/A": 0, "": 0}
    for s in sections:
        counts = {k: s.count(k) for k in totals}
        for k, v in counts.items():
            totals[k] += v
        rows.append({
            "section": s.number,
            "title": s.title,
            "total": len(s.items),
            "yes": counts["Yes"],
            "no": counts["No"],
            "na": counts["N/A"],
            "not_answered": counts[""],
            "compliance_rate": compliance_rate(counts["Yes"], counts["No"]),
        })

    all_items = [i for s in sections for i in s.items]
    findings = [asdict(i) for i in all_items if i.status == "No"]
    unanswered = [asdict(i) for i in all_items if i.status == ""]
    total = len(all_items)

    return {
        "company": company,
        "report_date": report_date or date.today().isoformat(),
        "disclaimer": DISCLAIMER,
        "overall": {
            "total": total,
            "yes": totals["Yes"],
            "no": totals["No"],
            "na": totals["N/A"],
            "not_answered": totals[""],
            "compliance_rate": compliance_rate(totals["Yes"], totals["No"]),
            "complete": totals[""] == 0,
        },
        "sections": rows,
        "findings": findings,
        "unanswered": unanswered,
    }


def _pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.1f}%"


def render_markdown(summary: dict) -> str:
    o = summary["overall"]
    lines = [
        f"# Self-Inspection Summary: {summary['company']}",
        "",
        f"_Report date: {summary['report_date']}_",
        "",
        f"> {summary['disclaimer']}",
        "",
        "## Overall",
        "",
        f"- Items reviewed: {o['total'] - o['not_answered']} of {o['total']}",
        f"- Yes: {o['yes']} | No: {o['no']} | N/A: {o['na']} | Not answered: {o['not_answered']}",
        f"- Compliance rate (Yes / (Yes + No)): {_pct(o['compliance_rate'])}",
        f"- Checklist complete: {'Yes' if o['complete'] else 'No'}",
        "",
        "## By section",
        "",
        "| Section | Title | Yes | No | N/A | Not answered | Rate |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in summary["sections"]:
        lines.append(
            f"| {r['section']} | {r['title']} | {r['yes']} | {r['no']} | {r['na']} | "
            f"{r['not_answered']} | {_pct(r['compliance_rate'])} |"
        )
    lines += ["", "## Findings (items marked No)", ""]
    if summary["findings"]:
        lines += ["| ID | Ref | Item | Notes |", "|---|---|---|---|"]
        for f in summary["findings"]:
            lines.append(f"| {f['item_id']} | {f['ref']} | {f['question']} | {f['notes'] or '-'} |")
    else:
        lines.append("None.")
    lines += ["", "## Not yet answered", ""]
    if summary["unanswered"]:
        for u in summary["unanswered"]:
            lines.append(f"- {u['item_id']} ({u['ref']}): {u['question']}")
    else:
        lines.append("None.")
    lines += [
        "",
        "## Next steps",
        "",
        "- Assign an owner and due date to each finding and track it to closure.",
        "- Brief the SMO and other key management personnel on the results (117.7(h)(2)).",
        "",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Summarize a completed self-inspection checklist.")
    p.add_argument("checklist", type=Path, help="Path to the completed checklist Markdown file")
    p.add_argument("--company", default="Larkspur Systems, Inc. (fictional)")
    p.add_argument("--format", choices=["md", "json"], default="md")
    p.add_argument("--output", "-o", type=Path, help="Write report to this file instead of stdout")
    p.add_argument("--date", dest="report_date", help="Report date (YYYY-MM-DD); defaults to today")
    p.add_argument("--fail-on-findings", action="store_true",
                   help="Exit with code 1 if any item is marked No")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        text = args.checklist.read_text(encoding="utf-8")
        sections = parse_checklist(text)
    except (OSError, ChecklistError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    summary = summarize(sections, company=args.company, report_date=args.report_date)
    out = json.dumps(summary, indent=2) if args.format == "json" else render_markdown(summary)

    if args.output:
        args.output.write_text(out, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(out)

    if args.fail_on_findings and summary["findings"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
