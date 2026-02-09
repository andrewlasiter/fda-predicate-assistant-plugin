# Golden-Path Workflows

Three end-to-end workflows for common FDA 510(k) use cases.

## Workflow 1: Full 510(k) from Scratch

Starting with only a product code and device description, build a complete submission package.

### Prerequisites
- Product code (e.g., `OVE`)
- Brief device description
- Intended use statement

### Steps

```
Step 0: Onboarding (first time only)
/fda:start

Step 1: Research the landscape
/fda:research OVE --competitor-deep

Step 2: Download & extract predicates
/fda:extract both --product-code OVE --years 2020-2025 --project my-device

Step 3: Review extracted predicates
/fda:review --project my-device

Step 4: Analyze guidance requirements
/fda:guidance OVE --save --project my-device

Step 5: Generate testing plan
/fda:test-plan OVE --project my-device

Step 6: Build SE comparison table
/fda:compare-se --predicates K192345,K181234 --project my-device --device-description "Your device" --intended-use "Your IFU"

Step 7: Draft all submission sections
/fda:draft device-description --project my-device --device-description "Your device"
/fda:draft se-discussion --project my-device
/fda:draft labeling --project my-device --intended-use "Your IFU"
/fda:draft performance-summary --project my-device
/fda:draft sterilization --project my-device
/fda:draft biocompatibility --project my-device
/fda:draft clinical --project my-device
/fda:draft cover-letter --project my-device
/fda:draft 510k-summary --project my-device

Step 8: Validate consistency
/fda:consistency --project my-device

Step 9: Assemble eSTAR package
/fda:assemble --project my-device

Step 10: Check project readiness
/fda:dashboard --project my-device

Step 11: Export for submission
/fda:export --project my-device --format xml
```

### Or use the autonomous agent:

```
Invoke the submission-writer agent with your project name.
It will execute Steps 7-10 autonomously.
```

### Expected Output
- `~/fda-510k-data/projects/my-device/estar/` — eSTAR directory structure
- `~/fda-510k-data/projects/my-device/estar_export_nIVD.xml` — XML for import into official template
- `~/fda-510k-data/projects/my-device/draft_*.md` — Individual section drafts
- `~/fda-510k-data/projects/my-device/eSTAR_readiness.md` — Readiness report

---

## Workflow 2: Import & Modify Existing eSTAR

Starting with an existing eSTAR PDF (partially filled), import data and complete the submission.

### Prerequisites
- Existing eSTAR PDF (even partially filled)
- OR exported XML from eSTAR

### Steps

```
Step 1: Import existing eSTAR data
/fda:import /path/to/estar.pdf --project existing-device --validate

Step 2: Review imported data
/fda:status --project existing-device

Step 3: Score imported predicates
/fda:review --project existing-device

Step 4: Fill gaps — generate missing sections
/fda:draft labeling --project existing-device
/fda:draft biocompatibility --project existing-device
(Draft only sections that are empty)

Step 5: Run consistency check
/fda:consistency --project existing-device

Step 6: Export updated data back to eSTAR XML
/fda:export --project existing-device --format xml

Step 7: Import XML into official eSTAR template
(Open eSTAR PDF in Adobe Acrobat → Form → Import Data → select XML)
```

### Expected Output
- `~/fda-510k-data/projects/existing-device/import_data.json` — Imported form data
- `~/fda-510k-data/projects/existing-device/estar_export_nIVD.xml` — Updated XML
- Fills gaps identified in the imported eSTAR

---

## Workflow 3: Pre-Submission Preparation

Prepare a comprehensive Pre-Sub package for an FDA meeting.

### Prerequisites
- Product code or device description
- General idea of device type and intended use

### Steps

```
Step 1: Research and classify
/fda:research OVE --competitor-deep

Step 2: Analyze safety landscape
/fda:safety --product-code OVE

Step 3: Review literature
/fda:literature OVE --project presub-device

Step 4: Identify regulatory pathway
/fda:pathway OVE --device-description "Your device" --intended-use "Your IFU"

Step 5: Generate guidance analysis
/fda:guidance OVE --save --project presub-device

Step 6: Generate Pre-Sub package
/fda:presub OVE --project presub-device --device-description "Your device" --intended-use "Your IFU"
```

### Or use the autonomous agent:

```
Invoke the presub-planner agent with your product code and device description.
It will execute Steps 1-6 autonomously.
```

### Expected Output
- `~/fda-510k-data/projects/presub-device/presub_plan.md` — Complete Pre-Sub package with:
  - Cover letter addressed to correct CDRH division
  - Device description
  - Regulatory strategy and predicate justification
  - 5-7 FDA questions (auto-generated from gaps)
  - Testing strategy
  - Background and literature summary
  - Safety intelligence (MAUDE + recalls)
  - Meeting logistics and timeline

---

## Tips for All Workflows

1. **New users: run `/fda:start` first** — The onboarding wizard guides you through setup and recommends a personalized workflow
2. **Start with `/fda:research`** — It gives you the landscape before diving into extraction
3. **Use `--project NAME` consistently** — All commands build on the same project data
4. **Run `/fda:consistency` before export** — Catches contradictions early
5. **Use `/fda:dashboard --project NAME` for progress tracking** — See your Submission Readiness Index and what's left to do
6. **Fill `[TODO:]` items before submission** — These mark company-specific data only you can provide
7. **Always have regulatory team review** — AI drafts are a starting point, not a finished submission
