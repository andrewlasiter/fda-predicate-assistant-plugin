---
description: Run the FDA 510(k) two-stage pipeline — download PDFs with 510kBF then extract predicates
allowed-tools: Bash, Read, Glob, Grep
argument-hint: "[stage1|stage2|both] [--year YEAR] [--product-code CODE] [--directory PATH]"
---

# FDA 510(k) Extraction Pipeline

You are guiding the user through the FDA device data pipeline. This is a **two-stage process**:

- **Stage 1** (510kBF): Filter the FDA catalog and download 510(k) PDF documents
- **Stage 2** (PredicateExtraction): Extract predicate device numbers from downloaded PDFs

## Determine What the User Wants

Parse `$ARGUMENTS` to determine which stage(s) to run:
- `stage1` → Run only 510kBF (download PDFs)
- `stage2` → Run only PredicateExtraction (extract predicates)
- `both` → Run Stage 1 then Stage 2
- No argument → Ask the user which stage they want

## Stage 1: 510kBF — Filter & Download PDFs

**Script:** `/mnt/c/510k/Python/510kBF/510BAtchFetch Working2.py`

This script is **interactive** — it requires user input to set filters. Tell the user:

1. The script will open and prompt for filtering criteria:
   - Year range (e.g., 2020-2025)
   - Product codes (e.g., KGN, DXY)
   - Applicant names
   - Decision codes (SESE = Substantially Equivalent)
   - Advisory committees

2. Run it:
   ```bash
   cd /mnt/c/510k/Python/510kBF && python "510BAtchFetch Working2.py"
   ```

3. **Outputs produced:**
   - `510k_download.csv` — Full metadata (24 columns: KNUMBER, APPLICANT, DECISIONDATE, PRODUCTCODE, TYPE, STATEORSUMM, REVIEWADVISECOMM, etc.)
   - `Applicant_ProductCode_Tables.xlsx` — Analytics (3 sheets: Applicant, ProductCode, Full data)
   - Downloaded PDFs in: `/mnt/c/510k/Python/510kBF/510ks/YEAR/APPLICANT/PRODUCTCODE/TYPE/`

**Note:** This script requires GUI interaction. If running in a headless environment, inform the user and suggest they run it manually first.

## Stage 2: PredicateExtraction — Extract Predicates from PDFs

**Script:** `/mnt/c/510k/Python/PredicateExtraction/Test79.py`

This is the latest version with enhanced error handling and browser headers for downloads.

1. **Determine the PDF directory:**
   - If `--directory PATH` was provided, use that
   - If Stage 1 just ran, use `/mnt/c/510k/Python/510kBF/510ks/` (or a year/applicant subfolder)
   - Otherwise, the script will prompt for a directory via GUI (tkinter)

2. **Run it:**
   ```bash
   cd /mnt/c/510k/Python/PredicateExtraction && python Test79.py
   ```

3. **Outputs produced:**
   - `output.csv` — Main results: K-number, ProductCode, DocType, Predicate1..Predicate100
   - `supplement.csv` — Devices with supplement suffixes (e.g., K240717/S001)
   - `pdf_data.json` — Cached extracted text keyed by filename
   - `error_log.txt` — List of PDFs that failed processing

## Dependencies Check

Before running either stage, verify dependencies are installed:

```bash
python -c "import requests, tqdm, fitz, pdfplumber" 2>/dev/null || echo "Missing dependencies - run: pip install requests tqdm PyMuPDF pdfplumber orjson ijson"
```

## After Extraction

Once either stage completes:

1. **Check output files exist** using Glob in the appropriate directory
2. **Report a summary:**
   - Stage 1: How many records in 510k_download.csv, how many PDFs downloaded
   - Stage 2: How many devices in output.csv, how many had predicates, any errors
3. **Offer next steps:**
   - If Stage 1 just finished → offer to run Stage 2
   - If Stage 2 just finished → offer to run `/fda:analyze`
   - Always offer `/fda:status` to see what data is available

## Error Handling

- If Python is not found: suggest `python3` or check PATH
- If script not found at expected path: use Glob to search for it
- If dependencies missing: provide the pip install command
- If GUI-related error (tkinter): inform user this needs a display, or suggest providing --directory
