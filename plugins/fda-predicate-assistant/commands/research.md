---
description: Research and plan a 510(k) submission — predicate selection, testing strategy, IFU landscape, regulatory intelligence, and competitive analysis
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "<product-code> [--project NAME] [--device-description TEXT] [--intended-use TEXT]"
---

# FDA 510(k) Submission Research

You are helping the user research and plan a 510(k) submission. Given a product code (and optionally a device description and intended use), produce a comprehensive research package drawing from ALL available pipeline data.

**KEY PRINCIPLE: Do the work, don't ask the user to run other commands.** If PDF text is available, extract predicates from it yourself. If a data file exists but has no relevant records, don't mention it. The user should get a complete answer, not a todo list.

## Parse Arguments

From `$ARGUMENTS`, extract:

- **Product code** (required) — 3-letter FDA product code (e.g., KGN, DXY, QAS)
- `--device-description TEXT` — Brief description of the user's device
- `--intended-use TEXT` — The user's intended indications for use
- `--years RANGE` — Focus on specific year range (default: last 10 years)
- `--depth quick|standard|deep` — Level of analysis (default: standard)
- `--project NAME` — Use data from a specific project folder

If no product code provided, ask the user for it. If they're unsure of their product code, help them find it:
```bash
grep -i "DEVICE_KEYWORD" /mnt/c/510k/Python/PredicateExtraction/foiaclass.txt /mnt/c/510k/Python/510kBF/fda_data/foiaclass.txt 2>/dev/null | head -20
```

## Step 1: Discover Available Data

### If `--project NAME` is provided — Use project data first

```bash
PROJECTS_DIR="/mnt/c/510k/Python/510k_projects"  # or from settings
ls "$PROJECTS_DIR/$PROJECT_NAME/"*.csv "$PROJECTS_DIR/$PROJECT_NAME/"*.json 2>/dev/null
cat "$PROJECTS_DIR/$PROJECT_NAME/query.json" 2>/dev/null
```

### Also check for matching projects automatically

If no `--project` specified, check if a project exists for this product code:
```bash
ls /mnt/c/510k/Python/510k_projects/*/query.json 2>/dev/null
```

### Check data sources silently — only report what's RELEVANT

Check these locations, but **only mention sources to the user if they contain data for the requested product code**:

```bash
# FDA database files (always relevant — contain ALL product codes)
ls /mnt/c/510k/Python/PredicateExtraction/pmn*.txt 2>/dev/null

# PDF text cache (check if it has relevant PDFs)
ls -la /mnt/c/510k/Python/PredicateExtraction/pdf_data.json 2>/dev/null

# Download metadata (check if it has relevant product code records)
ls -la /mnt/c/510k/Python/510kBF/510k_download.csv 2>/dev/null

# Device classification
ls /mnt/c/510k/Python/510kBF/fda_data/foiaclass.txt /mnt/c/510k/Python/PredicateExtraction/foiaclass.txt 2>/dev/null
```

**IMPORTANT**: Do NOT report files that exist but contain no data for this query. For example, if `merged_data.csv` has 100 records but none match the requested product code, do not mention it at all. The user doesn't care about files that aren't relevant to their device.

## Step 2: Product Code Profile

Look up the product code in foiaclass.txt (if available):

```bash
grep "^PRODUCTCODE" /mnt/c/510k/Python/510kBF/fda_data/foiaclass.txt /mnt/c/510k/Python/PredicateExtraction/foiaclass.txt 2>/dev/null
```

Report:
- **Device name** (official FDA classification name)
- **Device class** (I, II, III)
- **Regulation number** (21 CFR section)
- **Advisory committee** (review panel)
- **Definition** (if available in foiaclass)

Then count total clearances for this product code:
```bash
grep -c "|PRODUCTCODE|" /mnt/c/510k/Python/PredicateExtraction/pmn96cur.txt /mnt/c/510k/Python/PredicateExtraction/pmn9195.txt 2>/dev/null
```

## Step 3: Regulatory Intelligence

### From FDA database files (pmn*.txt)

Filter all records for this product code:

```bash
grep "|PRODUCTCODE|" /mnt/c/510k/Python/PredicateExtraction/pmn96cur.txt 2>/dev/null
```

Analyze and report:
- **Total clearances** all-time and by decade
- **Decision code distribution**: SESE (substantially equivalent), SEKN (SE with conditions), SESK, etc.
- **Submission type breakdown**: Traditional vs Special 510(k) vs Abbreviated
- **Statement vs Summary ratio**: What percentage file summaries (more data available) vs statements
- **Third-party review usage**: How common for this product code
- **Review time statistics**: Average, median, fastest, slowest (compute from DATERECEIVED to DECISIONDATE)
- **Recent trend**: Are submissions increasing or decreasing in the last 5 years?

### From 510k_download.csv (only if it contains this product code)

```bash
grep "PRODUCTCODE" /mnt/c/510k/Python/510kBF/510k_download.csv 2>/dev/null
```

Additional metadata available: expedited review, review advisory committee details.

## Step 4: Predicate Landscape

### Extract predicates directly from PDF text

**Do NOT tell the user to run `/fda:extract stage2`.** Instead, extract predicate K-numbers yourself from `pdf_data.json`:

```python
# Extract K-numbers cited in each document's text
import json, re
from collections import Counter

with open('pdf_data.json') as f:
    data = json.load(f)

k_pattern = re.compile(r'K\d{6}')
cited_by = Counter()  # predicate -> count of devices citing it
graph = {}  # device -> set of predicates it cites

for filename, content in data.items():
    text = content.get('text', '') if isinstance(content, dict) else str(content)
    source_k = filename.replace('.pdf', '')
    found_ks = set(k_pattern.findall(text))
    found_ks.discard(source_k)  # Remove self-reference
    graph[source_k] = found_ks
    for k in found_ks:
        cited_by[k] += 1
```

This gives you the same predicate relationships that `output.csv` would contain, without requiring any separate extraction step.

### Also check output.csv and merged_data.csv if they exist AND have relevant data

These are supplementary sources. Only use them if they contain records for the requested product code.

### Rank predicate devices by:
1. **Citation frequency** — How often is this device cited as a predicate?
2. **Recency** — When was the predicate cleared? More recent = stronger
3. **Chain depth** — Is the predicate itself well-established (cited by many others)?
4. **Same applicant** — Predicates from the same company may indicate product line evolution
5. **Device similarity** — Match device name keywords to user's device description

### Build predicate chains

For the top predicate candidates, trace their lineage:
- What predicates did they cite?
- How many generations deep does the chain go?
- Is there a "root" device that anchors this product code?

### Cross-Product-Code Predicate Search

**CRITICAL**: If the user's device description mentions features that have little or no precedent in the primary product code, **automatically search other product codes** for supporting predicates.

For example, if the user describes a "collagen wound dressing with silver antimicrobial" and silver has <5% prevalence in KGN:

```bash
# Search ALL product codes for devices with the novel feature
python3 -c "
import csv
results = []
with open('/mnt/c/510k/Python/PredicateExtraction/pmn96cur.txt', encoding='latin-1') as f:
    reader = csv.reader(f, delimiter='|')
    header = next(reader)
    for row in reader:
        d = dict(zip(header, row))
        name = d.get('DEVICENAME','').upper()
        if 'SILVER' in name or 'ANTIMICROBIAL' in name:
            results.append(d)
# Group by product code and report
"
```

This helps identify **secondary predicates** from adjacent product codes that support novel features. Report these separately with clear rationale:

```
Secondary Predicate (for silver/antimicrobial claim):
  K123456 (Product Code: FRO) — Silver Wound Dressing
  - Supports your antimicrobial claim
  - Different product code but same wound management category
  - Consider citing alongside your primary KGN predicate
```

### Predicate recommendation

Based on the analysis, recommend the **top 3-5 predicate candidates** with rationale:

```
Recommended Predicates for [PRODUCT CODE]:

1. K123456 (Company A, 2023) — STRONGEST
   - Cited by 12 other devices
   - Most recent clearance with same intended use
   - Traditional 510(k) with Summary available
   - Review time: 95 days

2. K234567 (Company B, 2021) — STRONG
   - Cited by 8 other devices
   - Broader indications (your device fits within)
   - Has detailed clinical data in summary
   - Review time: 120 days
```

If the user provided `--intended-use`, compare their intended use against the indications associated with each predicate candidate.

If the user provided `--device-description` with novel features not found in the primary product code, include a **Secondary Predicates** section with candidates from other product codes that support those features.

## Step 5: Testing Strategy

### From PDF text (pdf_data.json)

If PDF text is available for devices with this product code, analyze the testing sections directly. Use regex to search for testing-related content:

```python
patterns = {
    'ISO 10993': r'(?i)ISO\s*10993',
    'Biocompatibility': r'(?i)(biocompatib|cytotox|sensitiz|irritat)',
    'Sterilization': r'(?i)(steriliz|sterility|ethylene oxide|EtO|gamma)',
    'Shelf Life': r'(?i)(shelf\s*life|stability|accelerated\s*aging)',
    'Clinical': r'(?i)(clinical\s*(study|trial|data|evidence|testing))',
    'Animal Testing': r'(?i)(animal\s*(study|model|testing)|in\s*vivo)',
    # Add patterns specific to the user's device features
}
```

For each type of testing found, summarize:

**Non-Clinical / Performance Testing**:
- What test methods and standards are commonly cited? (ASTM, ISO, IEC, etc.)
- What performance endpoints are measured?
- What sample sizes are typical?

**Biocompatibility**:
- Which ISO 10993 endpoints are evaluated?
- Is this consistent across all devices or does it vary?

**Clinical Data**:
- What percentage of devices included clinical data?
- What type? (literature review, clinical study)
- Were any devices cleared WITHOUT clinical data?

**Sterilization** (if applicable):
- What sterilization methods are used?
- What validation standards are cited?

**Device-Specific Testing**: Based on the user's `--device-description`, add testing pattern searches for novel features. For example, if "silver" is mentioned, search for:
- Antimicrobial effectiveness (zone of inhibition, MIC/MBC)
- Silver content/release testing
- Silver-specific biocompatibility

### Testing recommendation

Provide a recommended testing matrix with Required/Likely Needed/Possibly Needed/Not Typically Required categories.

## Step 6: Indications for Use Landscape

Search for IFU content in PDF text for this product code. Analyze:
- **Common IFU elements**: What anatomical sites, patient populations, clinical conditions are covered?
- **Broadest cleared IFU**: Which device has the widest indications?
- **Narrowest cleared IFU**: Which is most restrictive?
- **Evolution over time**: Have indications expanded or narrowed?
- **If user provided --intended-use**: Compare their intended use against cleared IFUs. Flag any elements that go beyond what's been cleared before.

## Step 7: Competitive Landscape

### Top applicants

```bash
grep "|PRODUCTCODE|" /mnt/c/510k/Python/PredicateExtraction/pmn96cur.txt 2>/dev/null | cut -d'|' -f2 | sort | uniq -c | sort -rn | head -15
```

Report:
- **Market leaders**: Top companies by number of clearances
- **Recent entrants**: Companies that filed their first device in the last 3 years
- **Device name clustering**: Group device names to identify sub-categories
- **Active vs inactive**: Companies still submitting vs those who stopped

### Timeline

- Clearance volume by year (chart-like visualization using text)

## Output Format

Structure the research package as:

```
510(k) Submission Research: [PRODUCT CODE] — [DEVICE NAME]
============================================================

1. PRODUCT CODE PROFILE
   [Device class, regulation, advisory committee]

2. REGULATORY INTELLIGENCE
   [Clearance stats, review times, submission types]

3. PREDICATE CANDIDATES (Ranked)
   [Top 3-5 primary predicates from same product code]
   [Secondary predicates from other product codes if needed]

4. TESTING STRATEGY
   [Required, likely needed, possibly needed testing]

5. INDICATIONS FOR USE LANDSCAPE
   [IFU patterns, breadth analysis]

6. COMPETITIVE LANDSCAPE
   [Top companies, trends, sub-categories]

7. RECOMMENDATIONS & NEXT STEPS
   [Specific actionable next steps — NOT "run this command"]
```

**IMPORTANT**: The output should NOT have a "Data Gaps" section that lists files the user needs to create. If you can do the analysis with available data, just do it. Only mention data limitations if they genuinely limit the analysis AND explain what the limitation means in plain language (e.g., "No PDFs are available for this product code, so testing strategy and IFU analysis are based on database records only" — NOT "output.csv is missing, run /fda:extract stage2").

## Depth Levels

### `--depth quick` (2-3 minutes)
- Product code profile + basic regulatory stats
- Top 3 predicate candidates (citation count only)
- Competitive landscape overview
- Skip PDF text analysis

### `--depth standard` (default, 5-10 minutes)
- Full regulatory intelligence
- Top 5 predicate candidates with chain analysis
- Cross-product-code search for novel features
- Testing strategy from PDF text (if available)
- IFU comparison
- Competitive landscape

### `--depth deep` (15+ minutes)
- Everything in standard
- Full predicate chain mapping (all generations)
- Document-by-document section analysis
- Detailed testing method comparison tables
- IFU evolution timeline
- Export-ready tables and findings

## Recommendations Section

End with specific, actionable next steps in plain language:

- If predicate candidates identified: "Use `/fda:validate K123456 K234567` to get detailed profiles of these predicate candidates"
- If testing strategy identified: "Use `/fda:summarize --product-codes PRODUCTCODE --sections 'Non-Clinical Testing'` to compare exact test methods across devices"
- If novel features found: "Your [feature] has limited precedent in [product code]. Consider consulting with your regulatory team about whether a secondary predicate from [other product code] strengthens your submission."
- Always: "Consult with regulatory affairs counsel before finalizing your submission strategy"

**NEVER recommend**: "Run `/fda:extract stage1`" or "Run `/fda:extract stage2`" — these are pipeline internals. If PDFs aren't available, say "No summary PDFs are available for analysis yet. You can use `/fda:extract` to download them if needed."
