---
description: Interactive FDA 510(k) data collection — filter by product codes, years, committees, applicants with AI-guided selection and preview before download
allowed-tools: Bash, Read, Glob, Grep, Write, AskUserQuestion
argument-hint: "[--product-codes CODE] [--years RANGE] [--project NAME] [--quick] [--full-auto]"
---

# FDA 510(k) Batch Fetch — Interactive Filter & Download

> **Important**: This command assists with FDA regulatory workflows but does not provide regulatory advice. Output should be reviewed by qualified regulatory professionals before being relied upon for submission decisions.

> For external API dependencies and connection status, see [CONNECTORS.md](../CONNECTORS.md).

## Resolve Plugin Root

**Before running any bash commands that reference `$FDA_PLUGIN_ROOT`**, resolve the plugin install path:

```bash
FDA_PLUGIN_ROOT=$(python3 -c "
import json, os
f = os.path.expanduser('~/.claude/plugins/installed_plugins.json')
if os.path.exists(f):
    d = json.load(open(f))
    for k, v in d.get('plugins', {}).items():
        if k.startswith('fda-predicate-assistant@'):
            for e in v:
                p = e.get('installPath', '')
                if os.path.isdir(p):
                    print(p); exit()
print('')
")
echo "FDA_PLUGIN_ROOT=$FDA_PLUGIN_ROOT"
```

If `$FDA_PLUGIN_ROOT` is empty, report an error: "Could not locate the FDA Predicate Assistant plugin installation. Make sure the plugin is installed and enabled."

---

## Overview

This command provides an **AI-guided interactive workflow** for filtering and downloading FDA 510(k) data. Instead of terminal prompts, it uses Claude Code's native `AskUserQuestion` interface, allowing the AI to:
- Explain what each filter means
- Recommend selections based on your goals
- Preview results before downloading
- Create organized project structures
- Integrate with the existing pipeline

**Three workflow modes:**
- **Express lane (`--quick`)**: Product codes + years only (2 questions)
- **Full workflow**: 7 filter layers with smart defaults
- **Full-auto mode (`--full-auto`)**: Skip all questions, use CLI args only

---

## Parse Arguments

From `$ARGUMENTS`, extract:

- `--product-codes CODE` — Comma-separated product codes (e.g., "KGN,DXY")
- `--years RANGE` — Year filter (e.g., "2024" or "2020-2025")
- `--date-range KEYS` — Date range keys (e.g., "pmn96cur,pmnlstmn")
- `--committees CODES` — Advisory committee codes (e.g., "CV,OR")
- `--decision-codes CODES` — Decision codes (e.g., "SESE,SESK")
- `--applicants NAMES` — Semicolon-separated company names (e.g., "MEDTRONIC;ABBOTT")
- `--project NAME` — Project name for organized storage
- `--quick` — Express mode: skip most questions
- `--full-auto` — Skip all questions, use only CLI args
- `--resume` — Resume interrupted download from checkpoint
- `--no-download` — Preview only, skip PDF download
- `--save-excel` — Generate Excel analytics workbook

---

## Step 1: Mode Detection & Setup

### 1.1 Determine Workflow Mode

```python
# Determine mode
if '--full-auto' in arguments:
    mode = 'full-auto'
    # Validate required args present
    if not product_codes:
        error("--full-auto requires --product-codes")
elif '--quick' in arguments:
    mode = 'quick'
else:
    mode = 'full'
```

### 1.2 Resolve Projects Directory

```bash
# Check settings for projects_dir
PROJECTS_DIR=$(python3 -c "
import os, re
settings = os.path.expanduser('~/.claude/fda-predicate-assistant.local.md')
if os.path.exists(settings):
    with open(settings) as f:
        m = re.search(r'projects_dir:\s*(.+)', f.read())
        if m:
            print(os.path.expanduser(m.group(1).strip()))
            exit()
print(os.path.expanduser('~/fda-510k-data/projects'))
")
echo "PROJECTS_DIR=$PROJECTS_DIR"
```

### 1.3 Resume Mode Check

If `--resume` is provided:

```bash
# Check if project exists with download checkpoint
if [ -f "$PROJECTS_DIR/$PROJECT_NAME/download_progress.json" ]; then
    echo "Resume mode: Found checkpoint file"
    # Skip all questions, use existing query.json and resume download
    RESUME_MODE=true
else
    echo "Error: No checkpoint file found for project $PROJECT_NAME"
    exit 1
fi
```

If resuming, load filters from `query.json` and skip to Step 4 (Execution).

---

## Step 2: Filter Selection Workflow

### Embedded Reference Data

**Date Ranges:**
```
pmn96cur - 1996-current (~35,000 records, avg review: 142 days)
pmnlstmn - Most current month available (~300 records/month)
pmn9195  - 1991-1995 (~8,500 records)
pmn8690  - 1986-1990 (~6,200 records)
pmn8185  - 1981-1985 (~4,100 records)
pmn7680  - 1976-1980 (~2,800 records)
```

**Advisory Committees (21 total):**
```
AN - Anesthesiology
CV - Cardiovascular
CH - Clinical Chemistry
DE - Dental
EN - Ear, Nose, Throat
GU - Gastroenterology, Urology
HO - General Hospital
HE - Hematology
IM - Immunology
MG - Medical Genetics
MI - Microbiology
NE - Neurology
OB - Obstetrics/Gynecology
OP - Ophthalmic
OR - Orthopedic
PA - Pathology
PM - Physical Medicine
RA - Radiology
SU - General, Plastic Surgery
TX - Clinical Toxicology
```

**Decision Codes (most common):**
```
SESE - Substantially Equivalent (~95% of clearances)
SESK - Substantially Equivalent - Kit
SESD - Substantially Equivalent with Drug
SESP - Substantially Equivalent - Postmarket Surveillance
SESU - Substantially Equivalent - With Limitations
DENG - De Novo Granted
```

### 2.1 Question 1: Date Range Selection

**Context for AI:**
"Date ranges determine which FDA database archives to search. Recent data (pmn96cur + pmnlstmn) covers 1996-present and is recommended for most users. Historical ranges are useful for legacy device research or comprehensive market analysis."

Use `AskUserQuestion`:

```json
{
  "questions": [{
    "question": "Which FDA database date ranges should we search?",
    "header": "Date Range",
    "multiSelect": true,
    "options": [
      {
        "label": "Recent (1996-current + latest month) (Recommended)",
        "description": "Covers ~35,300 records. Best for finding modern predicates with current device features and regulatory expectations."
      },
      {
        "label": "1996-current only",
        "description": "~35,000 records. Excludes the most recent month's submissions."
      },
      {
        "label": "All available ranges",
        "description": "~57,000 total records dating back to 1976. Comprehensive but includes many outdated devices."
      },
      {
        "label": "Custom selection",
        "description": "Let me choose specific date ranges (1991-1995, 1986-1990, etc.)"
      }
    ]
  }]
}
```

**Map responses to CLI arguments:**
- "Recent" → `--date-range pmn96cur,pmnlstmn`
- "1996-current only" → `--date-range pmn96cur`
- "All available" → `--date-range pmn96cur,pmnlstmn,pmn9195,pmn8690,pmn8185,pmn7680`
- "Custom" → Follow-up question with all 6 ranges as options

### 2.2 Question 2: Year Filter (Conditional)

**Only ask if "pmn96cur" is included in date range selection.**

**Context for AI:**
"The pmn96cur database covers 1996-2025 (29 years). Narrowing to recent years finds predicates with modern design features, current regulatory expectations, and active contact information. Older predicates may have outdated technology or discontinued products."

Use `AskUserQuestion`:

```json
{
  "questions": [{
    "question": "Filter to specific years within the selected date ranges?",
    "header": "Year Filter",
    "multiSelect": false,
    "options": [
      {
        "label": "Last 5 years (2020-2025) (Recommended)",
        "description": "~8,500 records. Recent predicates with modern features, active companies, and current regulatory standards."
      },
      {
        "label": "Last 10 years (2015-2025)",
        "description": "~17,000 records. Balance between modern devices and broader predicate pool."
      },
      {
        "label": "Last 15 years (2010-2025)",
        "description": "~25,000 records. Comprehensive recent history including pre-2016 UDI era."
      },
      {
        "label": "No year filter",
        "description": "Use all years in selected date ranges. Maximum predicate pool."
      },
      {
        "label": "Custom year range",
        "description": "Specify exact years (e.g., 2022-2024)"
      }
    ]
  }]
}
```

**Map responses:**
- "Last 5 years" → `--years 2020-2025`
- "Last 10 years" → `--years 2015-2025`
- "Last 15 years" → `--years 2010-2025`
- "No year filter" → (omit --years argument)
- "Custom" → Prompt for year input, validate format

**If quick mode (`--quick`):** Skip to Question 3 (Product Codes) now.

### 2.3 Question 3: Product Codes (REQUIRED)

**Context for AI:**
"Product codes are 3-letter FDA classification codes that define device types (e.g., KGN = wound dressing, DQA = surgical instruments). This is the most important filter. You can enter multiple codes separated by commas."

**Pre-question check:**
```bash
# Check if product codes provided via CLI
if [ -n "$PRODUCT_CODES_ARG" ]; then
    # Validate codes exist in foiaclass.txt
    FOIACLASS="$FDA_PLUGIN_ROOT/data/foiaclass.txt"
    if [ -f "$FOIACLASS" ]; then
        for CODE in $(echo $PRODUCT_CODES_ARG | tr ',' ' '); do
            if ! grep -q "^$CODE|" "$FOIACLASS"; then
                echo "Warning: Product code $CODE not found in FDA database"
                # Show suggestions
                grep -i "$CODE" "$FOIACLASS" | head -5
            fi
        done
    fi
    PRODUCT_CODES="$PRODUCT_CODES_ARG"
else
    # Ask user
    USE_ASK_USER_QUESTION
fi
```

Use `AskUserQuestion`:

```json
{
  "questions": [{
    "question": "Which product codes should we search? (Required)",
    "header": "Product Codes",
    "multiSelect": false,
    "options": [
      {
        "label": "Enter product codes",
        "description": "I know my product code(s). Enter as comma-separated list (e.g., KGN,DXY,FRO)"
      },
      {
        "label": "Search by device description",
        "description": "I need help finding my product code. Search the FDA database by device name or keywords."
      },
      {
        "label": "Show me examples",
        "description": "Show common product code examples by device category"
      }
    ]
  }]
}
```

**Response handling:**

If "Enter product codes":
- Prompt: "Enter product codes (comma-separated, e.g., KGN,DXY):"
- Validate each code against `foiaclass.txt`
- If code not found, show fuzzy matches and ask to confirm or correct

If "Search by device description":
```bash
# Ask for search terms
echo "Enter device keywords (e.g., 'wound dressing', 'surgical instrument', 'ultrasound'):"
read SEARCH_TERMS

# Search foiaclass.txt
grep -i "$SEARCH_TERMS" "$FDA_PLUGIN_ROOT/data/foiaclass.txt" | head -20

# Present top matches as AskUserQuestion options
```

If "Show me examples":
```
Common Product Codes by Category:

Cardiovascular:
  DTK - Catheter, percutaneous
  DQA - Cardiovascular surgical instruments
  DRY - Stents

Orthopedic:
  KWP - Bone plates
  KWQ - Spinal fixation
  OVE - Intervertebral body fusion

Wound Care:
  KGN - Wound dressing
  FRO - Dressing with drug
  MGP - Surgical mesh

Diagnostics (IVD):
  LCX - Clinical chemistry reagents
  JJE - Immunology reagents
  ...
```

**Validation:**
- Must have at least 1 product code
- Warn if code not found but allow continuation (may get zero results)

### 2.4 Question 4: Advisory Committees (Optional)

**Skip condition:** If already filtering by specific product codes (1-3 codes), this filter is usually redundant. Display: "Your product codes already narrow the search. Do you want to further filter by advisory committee?"

**Context for AI:**
"Advisory committees review devices by medical specialty (e.g., Cardiovascular, Orthopedic). This filter is most useful when searching across many product codes or doing broad market research. For targeted predicate searches, it's usually unnecessary."

Use `AskUserQuestion`:

```json
{
  "questions": [{
    "question": "Filter by FDA advisory committee?",
    "header": "Committees",
    "multiSelect": true,
    "options": [
      {
        "label": "All committees (Recommended)",
        "description": "No filter. Your product codes already provide specificity."
      },
      {
        "label": "Cardiovascular (CV)",
        "description": "Heart, vascular, circulatory devices"
      },
      {
        "label": "Orthopedic (OR)",
        "description": "Bone, joint, spine, musculoskeletal devices"
      },
      {
        "label": "Clinical Chemistry (CH)",
        "description": "IVD tests for metabolic, cardiac, renal markers"
      },
      {
        "label": "General Hospital (HO)",
        "description": "Surgical instruments, wound care, general purpose devices"
      },
      {
        "label": "Other committees",
        "description": "Show full list of 21 committees"
      }
    ]
  }]
}
```

**Map responses:**
- "All committees" → (omit --committees argument)
- Specific selections → `--committees CV,OR,...`
- "Other" → Present full 21-committee list as follow-up

### 2.5 Question 5: Decision Codes (Optional)

**Context for AI:**
"Decision codes indicate the FDA's clearance decision. SESE (Substantially Equivalent) represents ~95% of traditional 510(k) clearances. DENG (De Novo) is for novel devices without predicates. Most users should include all decision types."

Use `AskUserQuestion`:

```json
{
  "questions": [{
    "question": "Filter by FDA decision type?",
    "header": "Decision",
    "multiSelect": true,
    "options": [
      {
        "label": "All decision types (Recommended)",
        "description": "Include SE, SE with limitations, De Novo, and all variations. Broadest predicate pool."
      },
      {
        "label": "SESE only (Standard SE)",
        "description": "Only standard Substantially Equivalent clearances. Excludes SE with limitations, kits, drugs, or surveillance requirements."
      },
      {
        "label": "Include De Novo (DENG)",
        "description": "Include De Novo granted devices. Useful for novel device research or when no predicates exist."
      },
      {
        "label": "Exclude SE with limitations",
        "description": "Exclude SESP (postmarket surveillance), SESU (limitations), and other restricted clearances."
      },
      {
        "label": "Custom selection",
        "description": "Choose specific decision codes from full list"
      }
    ]
  }]
}
```

**Map responses:**
- "All decision types" → (omit --decision-codes argument)
- "SESE only" → `--decision-codes SESE`
- "Include De Novo" → `--decision-codes SESE,SESK,SESD,SESP,SESU,DENG`
- "Exclude limitations" → `--decision-codes SESE,SESK,SESD`
- "Custom" → Present full decision code list

### 2.6 Question 6: Applicants (Optional)

**Context for AI:**
"Applicant filtering restricts results to specific companies. Useful for competitive intelligence (e.g., 'what is Medtronic developing?'), tracking specific manufacturers, or excluding certain companies. Most predicate searches should include all applicants."

Use `AskUserQuestion`:

```json
{
  "questions": [{
    "question": "Filter by applicant company?",
    "header": "Applicants",
    "multiSelect": false,
    "options": [
      {
        "label": "All applicants (Recommended)",
        "description": "No filter. Maximum predicate pool from all manufacturers."
      },
      {
        "label": "Enter specific companies",
        "description": "Filter to one or more companies (e.g., MEDTRONIC, ABBOTT, BOSTON SCIENTIFIC)"
      },
      {
        "label": "Use case: Competitive intelligence",
        "description": "I'm researching a competitor's product pipeline"
      }
    ]
  }]
}
```

**Response handling:**
- "All applicants" → (omit --applicants argument)
- "Enter companies" → Prompt for semicolon-separated company names
  - Note: "Company names must match FDA records exactly (usually uppercase)"
  - Validation: Show warning if name format looks incorrect
- "Competitive intelligence" → Provide tips and prompt for company names

---

## Step 3: Preview & Confirmation

### 3.1 Construct CLI Arguments

Build the complete batchfetch.py command:

```bash
BATCHFETCH_CMD="python3 $FDA_PLUGIN_ROOT/scripts/batchfetch.py"

# Add filters
[ -n "$DATE_RANGE" ] && BATCHFETCH_CMD="$BATCHFETCH_CMD --date-range $DATE_RANGE"
[ -n "$YEARS" ] && BATCHFETCH_CMD="$BATCHFETCH_CMD --years $YEARS"
[ -n "$PRODUCT_CODES" ] && BATCHFETCH_CMD="$BATCHFETCH_CMD --product-codes $PRODUCT_CODES"
[ -n "$COMMITTEES" ] && BATCHFETCH_CMD="$BATCHFETCH_CMD --committees $COMMITTEES"
[ -n "$DECISION_CODES" ] && BATCHFETCH_CMD="$BATCHFETCH_CMD --decision-codes $DECISION_CODES"
[ -n "$APPLICANTS" ] && BATCHFETCH_CMD="$BATCHFETCH_CMD --applicants '$APPLICANTS'"

# Add project paths
BATCHFETCH_CMD="$BATCHFETCH_CMD --output-dir $PROJECTS_DIR/$PROJECT_NAME"
BATCHFETCH_CMD="$BATCHFETCH_CMD --download-dir $PROJECTS_DIR/$PROJECT_NAME/510ks"
BATCHFETCH_CMD="$BATCHFETCH_CMD --data-dir $PROJECTS_DIR/$PROJECT_NAME/fda_data"
```

### 3.2 Generate Preview (No Download)

```bash
# Run with --no-download to get preview
PREVIEW_CMD="$BATCHFETCH_CMD --no-download"
echo "Generating preview..."
PREVIEW_OUTPUT=$($PREVIEW_CMD 2>&1)
```

Parse preview output for:
- Total records matched
- Date range of results (earliest to latest)
- Top 5 applicants with counts
- Product code distribution
- Average review time
- Estimated download size (records × 5MB avg)
- Estimated download time (records × 30 sec delay)

### 3.3 Display Summary & Get Confirmation

Present formatted summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FDA 510(k) Batch Fetch Preview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FILTERS APPLIED
────────────────────────────────────────
  Date Range:   pmn96cur, pmnlstmn
  Years:        2020-2025
  Product Code: KGN
  Committees:   All
  Decisions:    All
  Applicants:   All

RESULTS SUMMARY
────────────────────────────────────────
  Total Records:        847
  Date Range:           2020-01-15 to 2025-11-30
  Avg Review Time:      142 days

  Top Applicants:
    1. SMITH & NEPHEW (89 submissions)
    2. 3M (67 submissions)
    3. MOLNLYCKE (54 submissions)
    4. MEDLINE (41 submissions)
    5. CONVATEC (38 submissions)

DOWNLOAD ESTIMATE
────────────────────────────────────────
  Estimated Size:       ~4.2 GB (847 PDFs × 5MB avg)
  Estimated Time:       ~7 hours (847 × 30 sec delay)
  Disk Space Available: 250 GB

PROJECT
────────────────────────────────────────
  Name:    KGN_2020-2025
  Path:    ~/fda-510k-data/projects/KGN_2020-2025/
  Output:  510k_download.csv, 510ks/ directory

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Risk warnings:**
- **> 500 records:** "⚠️  Large download detected. Consider narrowing your filters (e.g., recent years only, specific applicants)."
- **> 1000 records:** "⚠️  VERY LARGE DOWNLOAD. This may take 8+ hours and use significant disk space. Strongly recommend filtering to 500 or fewer records."
- **> 2000 records:** "❌ Downloads over 2000 records are not recommended due to time and disk space requirements. Please narrow your filters."

Use `AskUserQuestion`:

```json
{
  "questions": [{
    "question": "Ready to proceed with download?",
    "header": "Confirmation",
    "multiSelect": false,
    "options": [
      {
        "label": "Download all PDFs (Recommended)",
        "description": "Download 847 PDFs to local storage. Required for predicate extraction."
      },
      {
        "label": "CSV metadata only (no PDFs)",
        "description": "Save 510k_download.csv with metadata but skip PDF downloads. Faster, use for analysis without full text."
      },
      {
        "label": "Refine filters",
        "description": "Go back and adjust date range, years, product codes, or other filters."
      },
      {
        "label": "Cancel",
        "description": "Cancel this operation and exit."
      }
    ]
  }]
}
```

**Response handling:**
- "Download all" → Proceed to Step 4 (Execution)
- "CSV only" → Add `--no-download` flag, proceed to Step 4
- "Refine" → Go back to Step 2 (Filter Selection)
- "Cancel" → Exit with message "Operation cancelled by user"

---

## Step 4: Execution

### 4.1 Create Project Structure

```bash
# Create project directories
mkdir -p "$PROJECTS_DIR/$PROJECT_NAME/510ks"
mkdir -p "$PROJECTS_DIR/$PROJECT_NAME/fda_data"

echo "Created project: $PROJECTS_DIR/$PROJECT_NAME"
```

### 4.2 Save Filter Metadata

Write `query.json` with all filter parameters and timestamp:

```json
{
  "project_name": "KGN_2020-2025",
  "created": "2026-02-13T12:00:00Z",
  "filters": {
    "date_range": ["pmn96cur", "pmnlstmn"],
    "years": [2020, 2021, 2022, 2023, 2024, 2025],
    "product_codes": ["KGN"],
    "committees": [],
    "decision_codes": [],
    "applicants": []
  },
  "cli_arguments": {
    "date_range": "pmn96cur,pmnlstmn",
    "years": "2020-2025",
    "product_codes": "KGN",
    "output_dir": "~/fda-510k-data/projects/KGN_2020-2025",
    "download_dir": "~/fda-510k-data/projects/KGN_2020-2025/510ks",
    "data_dir": "~/fda-510k-data/projects/KGN_2020-2025/fda_data"
  },
  "results": {
    "total_records": null,
    "pdfs_downloaded": null,
    "date_range": null,
    "top_applicants": [],
    "avg_review_time_days": null,
    "last_updated": null
  },
  "execution": {
    "mode": "full",
    "user_selections": {
      "date_range_choice": "Recent (1996-current + latest month)",
      "year_filter": "Last 5 years (2020-2025)",
      "product_codes_method": "Enter product codes",
      "committees": "All committees",
      "decision_codes": "All decision types",
      "applicants": "All applicants"
    }
  }
}
```

```bash
# Write query.json
cat > "$PROJECTS_DIR/$PROJECT_NAME/query.json" << 'EOF'
{JSON content here}
EOF
```

### 4.3 Execute Batchfetch

```bash
# Run batchfetch.py with full arguments
echo "Starting FDA 510(k) batch download..."
echo "This may take several hours depending on the number of records."
echo ""

# Execute command
$BATCHFETCH_CMD

# Capture exit code
EXIT_CODE=$?
```

### 4.4 Parse Results

After execution completes:

```bash
# Check for output files
if [ -f "$PROJECTS_DIR/$PROJECT_NAME/510k_download.csv" ]; then
    # Count records in CSV
    TOTAL_RECORDS=$(wc -l < "$PROJECTS_DIR/$PROJECT_NAME/510k_download.csv")
    TOTAL_RECORDS=$((TOTAL_RECORDS - 1))  # Subtract header

    # Count downloaded PDFs
    PDF_COUNT=$(find "$PROJECTS_DIR/$PROJECT_NAME/510ks" -name "*.pdf" 2>/dev/null | wc -l)

    # Parse CSV for date range
    # (Use Python or awk to extract min/max DECISIONDATE)

    # Parse CSV for top applicants
    # (Use Python to count and sort)

    echo "✓ Batch fetch complete!"
    echo "  Records: $TOTAL_RECORDS"
    echo "  PDFs:    $PDF_COUNT"
else
    echo "✗ Error: Output file not created"
    exit 1
fi
```

### 4.5 Update query.json with Results

```bash
# Update query.json with results
python3 << 'PYEOF'
import json, os
from datetime import datetime

query_path = os.path.join(os.environ['PROJECTS_DIR'], os.environ['PROJECT_NAME'], 'query.json')
with open(query_path, 'r') as f:
    data = json.load(f)

data['results']['total_records'] = int(os.environ['TOTAL_RECORDS'])
data['results']['pdfs_downloaded'] = int(os.environ['PDF_COUNT'])
data['results']['last_updated'] = datetime.utcnow().isoformat() + 'Z'

with open(query_path, 'w') as f:
    json.dump(data, f, indent=2)
PYEOF
```

### 4.6 Handle Errors

Check for common failure scenarios:

```bash
# Check failed downloads log
if [ -f "$PROJECTS_DIR/$PROJECT_NAME/failed_downloads_log.json" ]; then
    FAILED_COUNT=$(python3 -c "
import json
with open('$PROJECTS_DIR/$PROJECT_NAME/failed_downloads_log.json') as f:
    data = json.load(f)
    print(len(data))
")

    if [ "$FAILED_COUNT" -gt 0 ]; then
        echo "⚠️  $FAILED_COUNT PDFs failed to download"
        echo "   Check failed_downloads_log.json for details"

        # Categorize failures
        python3 << 'PYEOF'
import json
with open('$PROJECTS_DIR/$PROJECT_NAME/failed_downloads_log.json') as f:
    failures = json.load(f)

rate_limit = sum(1 for f in failures if 'rate limit' in f.get('error', '').lower())
not_found = sum(1 for f in failures if '404' in str(f.get('status_code', '')))
timeout = sum(1 for f in failures if 'timeout' in f.get('error', '').lower())

print(f"  Rate limit errors: {rate_limit}")
print(f"  404 Not found: {not_found}")
print(f"  Timeouts: {timeout}")
PYEOF

        # Offer to resume
        echo ""
        echo "To resume failed downloads, run:"
        echo "  /fda:batchfetch --project $PROJECT_NAME --resume"
    fi
fi
```

**Disk space check:**
```bash
# Check available disk space before large downloads
if [ "$TOTAL_RECORDS" -gt 500 ]; then
    AVAILABLE_GB=$(df -BG "$PROJECTS_DIR" | awk 'NR==2 {print $4}' | sed 's/G//')
    REQUIRED_GB=$((TOTAL_RECORDS * 5 / 1000))

    if [ "$AVAILABLE_GB" -lt "$((REQUIRED_GB * 2))" ]; then
        echo "⚠️  WARNING: Low disk space"
        echo "   Available: ${AVAILABLE_GB} GB"
        echo "   Required:  ~${REQUIRED_GB} GB"
        echo ""
        # Ask for confirmation to continue
    fi
fi
```

---

## Step 5: Summary & Next Steps

### 5.1 Display Results Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FDA 510(k) Batch Fetch Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROJECT: KGN_2020-2025
────────────────────────────────────────
  Path:     ~/fda-510k-data/projects/KGN_2020-2025/

  Records:  847 submissions
  PDFs:     847 downloaded (100%)
  Failed:   0

  Date Range:   2020-01-15 to 2025-11-30
  Avg Review:   142 days

FILES CREATED
────────────────────────────────────────
  ✓ query.json                  Filter metadata
  ✓ 510k_download.csv           Submission metadata (847 rows)
  ✓ 510ks/                      Downloaded PDFs (847 files, ~4.2 GB)
  ✓ fda_data/                   FDA database archives

NEXT STEPS
────────────────────────────────────────
  1. Extract predicates from PDFs:
     /fda:extract stage2 --project KGN_2020-2025

  2. Review and score predicates:
     /fda:review --project KGN_2020-2025

  3. Draft submission sections:
     /fda:draft --project KGN_2020-2025

OPTIONAL ANALYSIS
────────────────────────────────────────
  • View statistics:        /fda:analyze download --project KGN_2020-2025
  • Gap analysis:           /fda:gap-analysis --project KGN_2020-2025
  • Safety intelligence:    /fda:safety --product-code KGN
  • Competitive analysis:   Open Applicant_ProductCode_Tables.xlsx

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Data collection complete. Ready for predicate extraction.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 5.2 Generate Excel Analytics (If Requested)

If `--save-excel` flag was set:

```bash
# Batchfetch.py automatically generates Excel if --save-excel is passed
# Check if file exists
if [ -f "$PROJECTS_DIR/$PROJECT_NAME/Applicant_ProductCode_Tables.xlsx" ]; then
    echo ""
    echo "📊 Excel Analytics:"
    echo "   $PROJECTS_DIR/$PROJECT_NAME/Applicant_ProductCode_Tables.xlsx"
    echo "   Contains:"
    echo "   • Applicant ranking by submission count"
    echo "   • Product code distribution"
    echo "   • Timeline analysis"
    echo "   • Review time statistics"
fi
```

---

## Error Handling & Edge Cases

### No Results Found

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  No Results Found
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APPLIED FILTERS
────────────────────────────────────────
  Date Range:   pmn96cur
  Years:        2024
  Product Code: INVALID
  Applicants:   NONEXISTENT COMPANY

ISSUE
────────────────────────────────────────
  No 510(k) submissions matched your filters.

SUGGESTIONS
────────────────────────────────────────
  1. Verify product code is correct:
     • Check spelling (e.g., KGN not KNG)
     • Search: /fda:validate --search "wound dressing"

  2. Expand date range:
     • Try removing year filter
     • Include earlier date ranges (pmn9195)

  3. Remove restrictive filters:
     • Remove applicant filter
     • Try "All decision types"

  4. Check product code exists:
     • Some codes are obsolete or merged
     • Use /fda:status to check database

TRY AGAIN
────────────────────────────────────────
  /fda:batchfetch --product-codes KGN --years 2020-2025

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Use `AskUserQuestion` to offer:
- "Refine filters and try again"
- "Search for correct product code"
- "Cancel operation"

### Invalid Product Code

```bash
# Check product code validity
FOIACLASS="$FDA_PLUGIN_ROOT/data/foiaclass.txt"
for CODE in $(echo $PRODUCT_CODES | tr ',' ' '); do
    if ! grep -q "^$CODE|" "$FOIACLASS"; then
        echo "⚠️  Warning: Product code '$CODE' not found in FDA database"
        echo ""
        echo "Did you mean one of these?"
        grep -i "$CODE" "$FOIACLASS" | head -5 | awk -F'|' '{print "  " $1 " - " $2}'
        echo ""

        # Ask to continue or correct
        # Use AskUserQuestion
    fi
done
```

### Download Interruption

If download is interrupted (Ctrl+C, network failure, etc.):

```bash
# batchfetch.py creates download_progress.json checkpoint
# Contains list of successfully downloaded K-numbers

echo "Download interrupted!"
echo ""
echo "Resume from checkpoint:"
echo "  /fda:batchfetch --project $PROJECT_NAME --resume"
echo ""
echo "Or start fresh (deletes existing PDFs):"
echo "  /fda:batchfetch --project $PROJECT_NAME --force"
```

### FDA Rate Limiting

If encountering rate limit errors:

```
⚠️  FDA Rate Limit Detected
────────────────────────────────────────
  Downloaded:  234/847 PDFs (28%)
  Failed:      15 rate limit errors

  The FDA server is throttling requests. This is normal
  for large batch downloads.

OPTIONS
────────────────────────────────────────
  1. Resume with longer delay (Recommended):
     /fda:batchfetch --project $PROJECT_NAME --resume --delay 60

  2. Wait and retry later:
     Try again in 1-2 hours

  3. Split into smaller batches:
     Download by year ranges separately

CURRENT DELAY: 30 seconds between requests
```

### Dependency Missing

```bash
# Check if required packages are installed
python3 -c "import pandas" 2>/dev/null || {
    echo "Error: Required Python package 'pandas' not found"
    echo ""
    echo "Install dependencies:"
    echo "  pip3 install pandas requests"
    echo ""
    echo "Or use requirements file:"
    echo "  pip3 install -r $FDA_PLUGIN_ROOT/requirements.txt"
    exit 1
}
```

---

## Full-Auto Mode Implementation

When `--full-auto` is specified:

```bash
# Validate all required arguments are provided
if [ -z "$PRODUCT_CODES" ]; then
    echo "Error: --full-auto requires --product-codes"
    exit 1
fi

# Apply defaults for optional arguments
DATE_RANGE="${DATE_RANGE:-pmn96cur,pmnlstmn}"
YEARS="${YEARS:-}"  # No year filter by default
COMMITTEES="${COMMITTEES:-}"  # All committees
DECISION_CODES="${DECISION_CODES:-}"  # All decisions
APPLICANTS="${APPLICANTS:-}"  # All applicants

# Auto-generate project name if not provided
if [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME=$(generate_project_name "$PRODUCT_CODES" "$YEARS")
fi

# Skip all questions, proceed directly to preview
# Then execute immediately if preview shows valid results (>0 records)
# If zero results, exit with error
```

**Full-auto example:**
```bash
/fda:batchfetch --product-codes KGN --years 2024 --full-auto
# No questions asked, uses defaults:
#   date_range: pmn96cur,pmnlstmn
#   committees: all
#   decisions: all
#   applicants: all
#   project: KGN_2024
# Previews and downloads immediately
```

---

## Integration with Existing Pipeline

### Project Compatibility

This command creates the same project structure as `/fda:extract`, ensuring seamless pipeline integration:

```
~/fda-510k-data/projects/KGN_2020-2025/
├── query.json                    ← Created by /fda:batchfetch
├── 510k_download.csv            ← Created by /fda:batchfetch
├── 510ks/                        ← Created by /fda:batchfetch
│   ├── K123456.pdf
│   ├── K234567.pdf
│   └── ...
├── fda_data/                     ← Created by /fda:batchfetch
│   ├── pmn96cur.txt
│   └── pmnlstmn.txt
├── output.csv                    ← Created by /fda:extract stage2
├── supplement.csv                ← Created by /fda:extract stage2
├── pdf_data.json                 ← Created by /fda:extract stage2
├── review.json                   ← Created by /fda:review
├── drafts/                       ← Created by /fda:draft
└── estar/                        ← Created by /fda:assemble
```

### Command Chaining

Users can chain commands:

```bash
# Method 1: Separate commands
/fda:batchfetch --product-codes KGN --years 2024 --project my_device
/fda:extract stage2 --project my_device
/fda:review --project my_device --auto
/fda:draft --project my_device

# Method 2: Use existing /fda:extract (which calls batchfetch internally)
/fda:extract both --product-codes KGN --years 2024 --project my_device

# Method 3: Use /fda:pipeline for end-to-end automation
/fda:pipeline --product-codes KGN --years 2024 --full-auto
```

### Resume Across Commands

If download interrupted:

```bash
# Resume batchfetch download
/fda:batchfetch --project my_device --resume

# Then continue with extraction
/fda:extract stage2 --project my_device
```

---

## Usage Examples

### Example 1: Simple Product Code Search

```bash
/fda:batchfetch --product-codes KGN --years 2024 --quick
```
- Express mode: 2 questions only
- Downloads 2024 wound dressing submissions
- Project auto-named: `KGN_2024`

### Example 2: Multi-Code Historical Analysis

```bash
/fda:batchfetch --product-codes KGN,FRO,DQY --years 2015-2025
```
- Full interactive mode
- Multiple product codes
- 10-year analysis
- AI guides through all 7 filter questions

### Example 3: Competitive Intelligence

```bash
/fda:batchfetch --product-codes KGN --applicants "SMITH & NEPHEW;3M;MOLNLYCKE" --years 2020-2025 --project competitors_analysis
```
- Tracks specific companies
- Named project for organization
- Can add `--save-excel` for analytics

### Example 4: Full-Auto Batch

```bash
/fda:batchfetch --product-codes KGN --years 2024 --full-auto --project test_run --no-download
```
- No questions asked
- CSV only, no PDFs
- Fast preview run

### Example 5: Comprehensive Download

```bash
/fda:batchfetch --product-codes OVE,KWP,KWQ --date-range pmn96cur,pmnlstmn --committees OR --save-excel
```
- Orthopedic devices
- All recent data
- Committee filter
- Generate analytics workbook

---

## Tips & Best Practices

**For predicate searches:**
1. Start with last 5 years of data (recent predicates are better)
2. Use your specific product code(s) only
3. Include all decision types (even SESU/SESP may be valid predicates)
4. Don't filter by applicant (you want maximum predicate pool)

**For competitive intelligence:**
1. Filter by applicant company
2. Expand years to see trends (5-10 years)
3. Use `--save-excel` to analyze trends
4. Consider multiple product codes for full portfolio

**For market research:**
1. Use broad filters (all committees, all years)
2. Download CSV only first (`--no-download`)
3. Analyze metadata before committing to full download
4. Use `--save-excel` for market statistics

**To minimize download time:**
1. Filter by recent years (2-3 years max for targeted searches)
2. Avoid downloads over 500 PDFs if possible
3. Use `--quick` mode to skip unnecessary filters
4. Run during off-peak hours for better FDA server performance

**For large downloads (>500):**
1. Split into multiple projects by year
2. Use resume feature if interrupted
3. Monitor disk space
4. Increase `--delay` if hitting rate limits (use 60-90 seconds)

---

## Troubleshooting

**"Could not locate FDA Predicate Assistant plugin"**
- Run: `ls ~/.claude/plugins/installed_plugins.json`
- Check plugin is installed and enabled
- Try: `/fda:status` to verify installation

**"No records matched your filters"**
- Verify product code spelling
- Remove year filter
- Remove restrictive filters (applicants, decision codes)
- Try: `/fda:validate --search "device name"` to find correct code

**"Rate limit errors during download"**
- Use `--resume` to continue from checkpoint
- Increase delay: `--delay 60`
- Split into smaller batches by year
- Try again during off-peak hours (evenings/weekends)

**"Low disk space warning"**
- Check available space: `df -h ~`
- Each PDF is ~5MB average
- Use `--no-download` for CSV-only if disk limited
- Move projects to external drive if needed

**"Python package not found"**
- Install: `pip3 install pandas requests`
- Or: `pip3 install -r $FDA_PLUGIN_ROOT/requirements.txt`
- Check Python version: `python3 --version` (need 3.7+)

---

This command provides a **collaborative, AI-guided experience** for FDA data collection while leveraging the battle-tested `batchfetch.py` script for actual execution. The interactive workflow makes complex filtering accessible to non-technical users while providing expert context at every decision point.
