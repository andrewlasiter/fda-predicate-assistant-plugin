---
description: Run the 510(k) data maintenance pipeline — gap analysis, download missing PDFs, extract predicates, and merge results
allowed-tools: Bash, Read, Glob, Grep, Write
argument-hint: "[status|analyze|download|extract|merge|run] [--years RANGE] [--product-codes CODES] [--dry-run]"
---

# FDA 510(k) Data Maintenance Pipeline

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

You are running the **data maintenance pipeline** — a 4-step process for keeping the local 510(k) corpus up to date:

1. **Analyze** — Gap analysis: cross-reference FDA PMN database vs existing data to find what's missing
2. **Download** — Fetch missing PDF summaries from FDA with rate limiting and resume support
3. **Extract** — Extract predicate device numbers from downloaded PDFs
4. **Merge** — Merge per-year extraction CSVs into the master baseline CSV

**This is NOT the regulatory submission pipeline** (`/fda:pipeline`). This command manages the raw data that feeds into all other plugin commands.

## Determine Subcommand

Parse `$ARGUMENTS` for the subcommand and flags:

- `status` — Show pipeline state (read-only, no changes)
- `analyze` — Step 1 only: run gap analysis
- `download` — Step 2 only: download missing PDFs
- `extract` — Step 3 only: extract predicates from PDFs
- `merge` — Step 4 only: merge extraction CSVs
- `run` — Run all 4 steps in sequence
- No subcommand → default to `status`

### Common flags (parsed from arguments):
- `--years RANGE` — Year filter (e.g., `2024,2025` or `2020-2025`)
- `--product-codes CODES` — Product code filter (e.g., `KGN,DXY`)
- `--dry-run` — Show what would happen without executing
- `--incremental` — Skip years already up to date (extract/run only)

### Download-specific flags:
- `--delay N` — Seconds between downloads (default: 10)
- `--max-retries N` — Max retries per file (default: 3)

### Extract-specific flags:
- `--workers N` — Parallel extraction workers
- `--batch-size N` — Process PDFs in batches of N

### Run-specific flags:
- `--skip-analyze` — Skip gap analysis step
- `--skip-download` — Skip download step

## Locate Data Directories

Check settings and auto-detect the data layout:

```bash
cat ~/.claude/fda-predicate-assistant.local.md 2>/dev/null
```

### Standard Layout Detection

The pipeline expects this directory structure:

```
/mnt/c/510k/Python/
├── PredicateExtraction/       ← Scripts, PMN files, manifests
│   ├── gap_analysis.py
│   ├── gap_downloader.py
│   ├── Test69a_final_ocr_smart_v2.py
│   ├── merge_outputs.py
│   ├── pipeline.py            ← Orchestrator
│   ├── pmn96cur.txt           ← FDA PMN database
│   ├── gap_manifest.csv       ← Gap analysis output
│   └── download_progress.json ← Download resume state
└── download/510k/             ← PDF corpus + baseline CSV
    ├── 510k_output.csv        ← Baseline extraction results
    ├── 510k_output_updated.csv← Merged results
    └── {YEAR}/                ← PDFs organized by year
        └── {Applicant}/{ProductCode}/{Type}/{K-number}.pdf
```

Auto-detect paths:

```bash
python3 -c "
import os
repo = '/mnt/c/510k/Python/PredicateExtraction'
dl = '/mnt/c/510k/Python/download/510k'
checks = {
    'PIPELINE_SCRIPT': os.path.join(repo, 'pipeline.py'),
    'GAP_ANALYSIS': os.path.join(repo, 'gap_analysis.py'),
    'GAP_DOWNLOADER': os.path.join(repo, 'gap_downloader.py'),
    'EXTRACTOR': os.path.join(repo, 'Test69a_final_ocr_smart_v2.py'),
    'MERGE_SCRIPT': os.path.join(repo, 'merge_outputs.py'),
    'PMN_FILE': os.path.join(repo, 'pmn96cur.txt'),
    'BASELINE_CSV': os.path.join(dl, '510k_output_updated.csv'),
    'PDF_DIR': dl,
}
for k, v in checks.items():
    exists = os.path.exists(v)
    print(f'{k}:{\"OK\" if exists else \"MISSING\"}:{v}')
"
```

If `pipeline.py` is found, use it as the orchestrator. If not, fall back to running individual scripts via `$FDA_PLUGIN_ROOT/scripts/gap_analysis.py` for the analyze step.

**CRITICAL**: The `--pdf-dir` and `--baseline` must point to the `download/510k/` directory, NOT to `PredicateExtraction/`. The bulk PDF corpus lives in `download/510k/`.

## Running Subcommands

### Using pipeline.py (preferred)

If `pipeline.py` exists at the detected path, use it directly:

```bash
REPO_DIR="/mnt/c/510k/Python/PredicateExtraction"
python3 "$REPO_DIR/pipeline.py" {subcommand} {flags}
```

Examples:
- `python3 "$REPO_DIR/pipeline.py" status`
- `python3 "$REPO_DIR/pipeline.py" analyze --years 2025 --product-codes KGN`
- `python3 "$REPO_DIR/pipeline.py" download --delay 10`
- `python3 "$REPO_DIR/pipeline.py" extract --years 2024,2025 --incremental`
- `python3 "$REPO_DIR/pipeline.py" merge`
- `python3 "$REPO_DIR/pipeline.py" run --years 2025 --dry-run`

### Fallback: Using Plugin Scripts

If `pipeline.py` is not found, run steps individually using the plugin's bundled scripts:

**Analyze** (Step 1):
```bash
python3 "$FDA_PLUGIN_ROOT/scripts/gap_analysis.py" \
  --years "$YEARS" \
  --product-codes "$PRODUCT_CODES" \
  --pmn-files "$PMN_FILES" \
  --baseline "$BASELINE_CSV" \
  --pdf-dir "$PDF_DIR" \
  --output "$REPO_DIR/gap_manifest.csv"
```

**Download** (Step 2):
```bash
python3 "$REPO_DIR/gap_downloader.py" --delay 10
```

**Extract** (Step 3) — uses the plugin's predicate_extractor.py:
```bash
python3 "$FDA_PLUGIN_ROOT/scripts/predicate_extractor.py" \
  --directory "$PDF_DIR/$YEAR" \
  --output-dir "$PDF_DIR/$YEAR"
```

**Merge** (Step 4):
```bash
python3 "$REPO_DIR/merge_outputs.py"
```

## Output Format

Present results using the standard FDA Professional CLI format:

### Status Output

```
  FDA Data Pipeline Status
  510(k) Corpus Overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Generated: {date} | v5.15.0

BASELINE
────────────────────────────────────────

  | Dataset      | Records  |
  |--------------|----------|
  | Baseline CSV | {N}      |
  | Updated CSV  | {N}      |

GAP ANALYSIS
────────────────────────────────────────

  | Metric                  | Count |
  |-------------------------|-------|
  | Total in PMN database   | {N}   |
  | Already extracted       | {N}   |
  | Have PDF, need extract  | {N}   |
  | Need download           | {N}   |

DOWNLOAD PROGRESS
────────────────────────────────────────

  | Status    | Count |
  |-----------|-------|
  | Success   | {N}   |
  | 404       | {N}   |
  | Failed    | {N}   |
  | Remaining | {N}   |

PER-YEAR SUMMARY
────────────────────────────────────────

  | Year | PDFs  | Extracted | Status          |
  |------|-------|-----------|-----------------|
  | 2023 | 3,158 | 3,080     | Partial (78)    |
  | 2024 | 2,854 | 2,854     | Complete        |
  | 2025 | 355   | 349       | Partial (6)     |

NEXT STEPS
────────────────────────────────────────

  {Context-dependent recommendations:}
  - If gaps exist: `/fda:data-pipeline analyze` then `/fda:data-pipeline download`
  - If PDFs unextracted: `/fda:data-pipeline extract --years YEAR`
  - If extractions unmerged: `/fda:data-pipeline merge`
  - If everything up to date: "Corpus is current. No action needed."

────────────────────────────────────────
  This report is AI-generated from public FDA data.
  Verify independently. Not regulatory advice.
────────────────────────────────────────
```

### Run/Step Output

For individual steps or full run, display the raw script output and then summarize with the CLI format after completion.

## Long-Running Operations

**Downloads and extractions can take hours.** For these steps:

1. Run the script in the background when appropriate
2. Inform the user of estimated time
3. Note that progress is saved automatically — safe to interrupt and resume later
4. Show how to check progress: `python3 pipeline.py status`

## Error Handling

- If `pipeline.py` not found → Fall back to individual scripts, or guide user to install the PredicateExtraction repo
- If PMN files not found → Guide to download from FDA or run `/fda:extract stage1`
- If download/510k directory not found → Guide to create it and run initial batch fetch
- If extraction fails for a year → Log and continue to next year (pipeline doesn't halt)
- If merge fails → Show the individual per-year CSVs that can be used directly
