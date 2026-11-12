# Annual Self-Inspection Checklist (Study Version)

> **Personal study material for a fictional company, Larkspur Systems, Inc.** Questions are written
> in my own words from the public text of 32 CFR Part 117 and are organized like DCSA's public
> Self-Inspection Handbook. This is not the official DCSA handbook and is not a substitute for it.
> Get the official handbook from
> [DCSA NISP Tools and Resources](https://www.dcsa.mil/Industrial-Security/National-Industrial-Security-Program-Oversight/NISP-Tools-Resources/)
> and read the [current rule text](https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-D/part-117).

## How to use

1. Copy this file and rename it (for example `larkspur_2026.md`). Do not commit filled copies that
   describe a real facility.
2. For each item set **Status** to `Yes`, `No`, or `N/A`. Leave it blank if not yet reviewed.
3. Use **Notes** to record *how* the requirement is met, or the gap if the answer is `No`.
4. Run the report:
   `python src/self_inspection_report.py larkspur_2026.md --company "Larkspur Systems, Inc."`

Rules the parser follows: each `## 117.x` heading starts a section; each table row with an ID like
`PROC-01` is an item; the Status column must be `Yes`, `No`, `N/A`, or blank.

## 117.7 Procedures

| ID | Item | Ref | Status | Notes |
|---|---|---|---|---|
| PROC-01 | Is an SMO named in writing, and does that person understand their accountability for the security program? | 117.7(b)(2) | | |
| PROC-02 | Is an FSO appointed, cleared at the facility level, and trained for the role? | 117.7(b) | | |
| PROC-03 | Is an ITPSO appointed in writing and listed as key management personnel? | 117.7(b)(4) | | |
| PROC-04 | Are written security procedures in place that match the scope of classified work? | 117.7(c) | | |
| PROC-05 | Is there a written insider threat program plan, and is it being carried out? | 117.7(d) | | |
| PROC-06 | Was a formal self-inspection done in the last 12 months, with a written report of findings and fixes? | 117.7(h)(2) | | |
| PROC-07 | Did the SMO certify the self-inspection in writing and brief other key management personnel? | 117.7(h)(2) | | |

## 117.8 Reporting Requirements

| ID | Item | Ref | Status | Notes |
|---|---|---|---|---|
| REP-01 | Do employees know what personal events they must report and who to report them to? | 117.8(c) | | |
| REP-02 | Are changes to cleared employee status (termination, name change, citizenship) reported to the CSA? | 117.8(c)(3) | | |
| REP-03 | Is a refusal to sign the SF 312 reported? | 117.8(c)(6) | | |
| REP-04 | Are changes in ownership, control, name, or address that affect entity eligibility reported? | 117.8(c)(7) | | |
| REP-05 | Is there a process to report suspicious contacts and possible security violations promptly? | 117.8 | | |

## 117.9 Entity Eligibility Determination

| ID | Item | Ref | Status | Notes |
|---|---|---|---|---|
| ENT-01 | Is the facility clearance record (KMP list, legal structure, addresses) current in the system of record? | 117.9 | | |
| ENT-02 | Are key management personnel cleared or excluded as the rule requires? | 117.9 | | |

## 117.10 Personnel Eligibility for Access

| ID | Item | Ref | Status | Notes |
|---|---|---|---|---|
| PER-01 | Are clearance requests limited to employees who need access for a current contract? | 117.10 | | |
| PER-02 | Is eligibility confirmed in the system of record before anyone gets access? | 117.10 | | |
| PER-03 | Has each cleared employee signed an SF 312 before first access? | 117.10 | | |
| PER-04 | Are access records updated promptly when an employee leaves or no longer needs access? | 117.10 | | |

## 117.11 Foreign Ownership, Control, or Influence (FOCI)

| ID | Item | Ref | Status | Notes |
|---|---|---|---|---|
| FOCI-01 | Is the entity's FOCI certification current and accurate? | 117.11 | | |
| FOCI-02 | Is there a process to identify and report changes that could create or change FOCI? | 117.11 | | |
| FOCI-03 | If a mitigation agreement applies, are its terms being followed and documented? | 117.11 | | |

## 117.12 Security Training and Briefings

| ID | Item | Ref | Status | Notes |
|---|---|---|---|---|
| TRN-01 | Do cleared employees get an initial security briefing before first access? | 117.12 | | |
| TRN-02 | Do cleared employees complete annual refresher training, and is completion recorded? | 117.12 | | |
| TRN-03 | Do cleared employees complete initial and annual insider threat awareness training? | 117.12(g) | | |
| TRN-04 | Have ITPSO and insider threat program staff completed the required one-time training? | 117.12(g) | | |
| TRN-05 | Have the FSO and other security staff completed the training their roles require? | 117.12 | | |
| TRN-06 | Is there a debriefing when access ends? | 117.12 | | |

## 117.13 Classification

| ID | Item | Ref | Status | Notes |
|---|---|---|---|---|
| CLS-01 | Do derivative classifiers have the required training before applying classification? | 117.13 | | |
| CLS-02 | Is classification guidance (DD 254, security classification guides) available to the people who need it? | 117.13 | | |
| CLS-03 | Is there a process to challenge classification that seems wrong? | 117.13 | | |

## 117.16 Visits and Meetings

| ID | Item | Ref | Status | Notes |
|---|---|---|---|---|
| VIS-01 | Is visitor clearance and need-to-know confirmed before classified access during a visit? | 117.16 | | |
| VIS-02 | Are visitors identified, logged, and escorted as procedures require? | 117.16 | | |
| VIS-03 | Are classified meetings held only in approved settings with attendance controls? | 117.16 | | |

## 117.15 Safeguarding Classified Information (if the facility stores classified)

| ID | Item | Ref | Status | Notes |
|---|---|---|---|---|
| SAF-01 | Is classified material stored only in approved containers or areas? | 117.15 | | |
| SAF-02 | Are combinations changed when required and limited to authorized people? | 117.15 | | |
| SAF-03 | Are end-of-day security checks done and recorded? | 117.15 | | |
