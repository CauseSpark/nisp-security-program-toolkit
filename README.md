# NISP Security Program Toolkit

[![tests](https://github.com/CauseSpark/nisp-security-program-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/CauseSpark/nisp-security-program-toolkit/actions/workflows/tests.yml)

A study toolkit for building and checking an industrial security program under the National
Industrial Security Program (NISP), written for a **fictional** cleared contractor, *Larkspur
Systems, Inc.* It pairs program documents (plan, SOP outlines, training plan, tracker) with a small
Python tool that turns a completed self-inspection checklist into a summary report.

## Purpose

I'm moving from Army security work into governance, risk, and compliance (GRC). This repo shows how
I turn a compliance rule into a working program: map the requirements, write the procedures, track
training, inspect against the rule, and report the results in a form leadership can act on. It is
built only from **public** rules and guidance.

## Current rule and guidance (checked 2026-11-11)

- **Rule:** The NISPOM is a federal rule at **32 CFR Part 117**, published December 21, 2020
  (85 FR 83312) and **effective February 24, 2021**. It replaced the old DoD 5220.22-M manual and
  incorporated SEAD 3 reporting requirements. It remains the governing rule for cleared contractors.
  Read the current text on the [eCFR](https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-D/part-117).
- **Self-inspections:** 117.7(h)(2) requires a formal self-inspection at least annually, a written
  report of findings and corrective actions, and a written SMO certification. DCSA's public
  [NAESOC guidance](https://www.dcsa.mil/Industrial-Security/The-National-Access-Elsewhere-Security-Oversight-Center-NAESOC/NAESOC-Resources)
  says the report is endorsed by the SMO and uploaded in NISS.
- **DCSA job aid:** DCSA publishes a *Self-Inspection Handbook for NISP Contractors* on its
  [NISP Tools and Resources](https://www.dcsa.mil/Industrial-Security/National-Industrial-Security-Program-Oversight/NISP-Tools-Resources/)
  page. Using it is a recommended best practice, not a requirement.
- **Recent guidance:** [ISL 2026-01, *Insider Threat Program: Minimum Standards*](https://pclt.defense.gov/Portals/140/DCSA_ISL_Insider%20Threat%202026-01%20v2.pdf)
  (May 20, 2026) restates insider threat program and training requirements under 117.7(d) and
  117.12(g) and says the program must be covered in the annual self-inspection.

More detail and the full source list are in [docs/overview.md](docs/overview.md).

## What's inside

```
docs/overview.md                         What the NISP and DCSA cover, with links to public sources
checklists/self_inspection.md            Annual self-inspection checklist, organized by 117.x section
templates/security_program_plan.md       Program plan: roles, elements, reviews, records
templates/sop_visitor_control.md         SOP outline: visitor control (117.16)
templates/sop_incident_reporting.md      SOP outline: incident and event reporting (117.8)
templates/insider_threat_program_outline.md  Insider threat program outline (117.7(d), ISL 2026-01)
templates/training_plan.md               Training matrix and process (117.12)
trackers/training_tracker.csv            Training tracker with fictional sample records
src/self_inspection_report.py            Checklist -> Markdown or JSON summary report
tests/                                   pytest suite, including public-safety guardrail tests
```

## Quick start

Requires Python 3.10+. No runtime dependencies.

```bash
git clone https://github.com/CauseSpark/nisp-security-program-toolkit.git
cd nisp-security-program-toolkit

# Run the report on the fictional sample
python src/self_inspection_report.py tests/fixtures/sample_completed.md

# Fill in your own copy of the checklist (Yes / No / N/A / blank), then:
cp checklists/self_inspection.md my_inspection.md
python src/self_inspection_report.py my_inspection.md --company "Larkspur Systems, Inc." \
    --format json --output my_inspection_report.json

# Exit with code 1 if any finding is open (useful in automation)
python src/self_inspection_report.py my_inspection.md --fail-on-findings

# Run the tests
pip install -r requirements-dev.txt
pytest
```

Sample output (excerpt):

```
## Overall
- Items reviewed: 6 of 7
- Yes: 3 | No: 2 | N/A: 1 | Not answered: 1
- Compliance rate (Yes / (Yes + No)): 60.0%

## Findings (items marked No)
| ID | Ref | Item | Notes |
| PROC-05 | 117.7(d) | Written insider threat plan? | Plan draft not yet approved by SMO |
| TRN-02 | 117.12 | Annual refresher recorded? | 2 of 5 employees overdue |
```

## What this demonstrates

- **Reading a regulation and mapping it to controls** - checklist items and templates trace back
  to specific 32 CFR Part 117 sections.
- **Program documentation** - a security program plan, SOP outlines, an insider threat program
  outline, and a training plan written the way a compliance team would maintain them.
- **Evidence and tracking** - a training tracker with a defined schema that the tests validate.
- **Assessment and reporting** - a tool that turns inspection answers into per-section compliance
  rates, open findings, and unanswered items for leadership briefings.
- **Engineering hygiene** - tested Python, CI on every push, small commits, and guardrail tests
  that fail the build if classification or CUI banner markings ever appear in the repo.
- **Judgment about sensitive information** - fictional company, public sources only, links rather
  than copied text.

## Disclaimer

This repository is **personal study material**. It is not official guidance, not affiliated with or
endorsed by DCSA, DoD, CDSE, or any government agency, and not legal advice. It does not claim any
certification or official status. *Larkspur Systems, Inc.* and every person named in it are
fictional. All content is based on publicly available rules and guidance; it contains no
classified information, no CUI, and nothing from any real facility, inspection, or person. The
checklist is my own wording and is not the DCSA Self-Inspection Handbook. Rules change, so always
check the [current 32 CFR Part 117](https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-D/part-117)
and [DCSA guidance](https://www.dcsa.mil/Industrial-Security/National-Industrial-Security-Program-Oversight/NISP-Tools-Resources/).

## License

[MIT](LICENSE)
