---
description: View or modify FDA predicate assistant settings and data directory paths
allowed-tools: Read, Write, Bash
argument-hint: "[--show | --set KEY VALUE | --test-api | --migrate-cache]"
---

# FDA Predicate Assistant Configuration

You are managing configuration settings for the FDA predicate extraction pipeline.

## Settings File Location

Settings are stored in: `~/.claude/fda-predicate-assistant.local.md`

## Available Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `projects_dir` | `/mnt/c/510k/Python/510k_projects` | Root directory for all project folders (each extraction query gets its own folder) |
| `batchfetch_dir` | `/mnt/c/510k/Python/510kBF` | Legacy directory containing 510kBF output (510k_download.csv, merged_data.csv) |
| `extraction_dir` | `/mnt/c/510k/Python/PredicateExtraction` | Directory containing extraction output (output.csv, pdf_data.json) |
| `pdf_storage_dir` | `/mnt/c/510k/Python/510kBF/510ks` | Where downloaded PDFs are stored |
| `data_dir` | `/mnt/c/510k/Python/PredicateExtraction` | Where FDA database files (pmn*.txt, pma.txt, foiaclass.txt) are stored |
| `extraction_script` | `predicate_extractor.py` | Which extraction script to use (bundled in plugin) |
| `batchfetch_script` | `batchfetch.py` | Which batch fetch script to use (bundled in plugin) |
| `ocr_mode` | `smart` | OCR processing mode: smart, always, never |
| `batch_size` | `100` | Number of PDFs to process per batch |
| `workers` | `4` | Number of parallel processing workers |
| `cache_days` | `5` | Days to cache FDA database files |
| `default_year` | `null` | Default year filter (null = all years) |
| `default_product_code` | `null` | Default product code filter |
| `openfda_api_key` | `null` | openFDA API key for higher rate limits (120K/day vs 1K/day) |
| `openfda_enabled` | `true` | Enable/disable openFDA API calls (set false for offline-only mode) |

## Commands

### Show Current Settings

If `$ARGUMENTS` is `--show` or empty, read and display the current settings:

Read the settings file at `~/.claude/fda-predicate-assistant.local.md`. If it doesn't exist, report defaults and offer to create one.

Also report on bundled scripts:
```
Plugin Scripts (at $CLAUDE_PLUGIN_ROOT/scripts/):
  predicate_extractor.py  — Stage 2: Extract predicates from PDFs
  batchfetch.py           — Stage 1: Filter catalog & download PDFs
  requirements.txt        — Python dependencies for both scripts
```

### Set a Value

If `$ARGUMENTS` starts with `--set`, parse KEY and VALUE, then update the settings file.

Validate the key is one of the known settings before writing. For directory paths, verify the directory exists.

Special handling for `openfda_api_key`:
- Accept the key value and store it in settings
- After storing, run a quick validation by hitting the 510k endpoint with `limit=1` to confirm the key works
- Report success/failure

### Test openFDA API

If `$ARGUMENTS` is `--test-api`, test connectivity to all 7 openFDA Device API endpoints.

Use the query template from `references/openfda-api.md`:

```bash
python3 << 'PYEOF'
import urllib.request, urllib.parse, json, os, re, time

# Read settings for API key
settings_path = os.path.expanduser('~/.claude/fda-predicate-assistant.local.md')
api_key = None
api_enabled = True
if os.path.exists(settings_path):
    with open(settings_path) as f:
        content = f.read()
    m = re.search(r'openfda_api_key:\s*(\S+)', content)
    if m and m.group(1) != 'null':
        api_key = m.group(1)
    m = re.search(r'openfda_enabled:\s*(\S+)', content)
    if m and m.group(1).lower() == 'false':
        api_enabled = False

if not api_enabled:
    print("openFDA API is DISABLED (openfda_enabled: false)")
    print("Enable with: /fda:configure --set openfda_enabled true")
    exit(0)

endpoints = [
    ("510k", 'k_number:"K241335"'),
    ("classification", 'product_code:"KGN"'),
    ("event", 'device.product_code:"KGN"'),
    ("recall", 'product_code:"KGN"'),
    ("pma", 'pma_number:"P190001"'),
    ("registrationlisting", 'products.product_code:"KGN"'),
    ("udi", 'product_codes.code:"KGN"'),
]

print("openFDA Device API Connectivity Test")
print("=" * 50)
print(f"API Key: {'Configured' if api_key else 'Not set (1K/day limit)'}")
print(f"Rate Tier: {'120K/day (with key)' if api_key else '1K/day (no key)'}")
print()

passed = 0
failed = 0
for endpoint, search in endpoints:
    params = {"search": search, "limit": "1"}
    if api_key:
        params["api_key"] = api_key
    url = f"https://api.fda.gov/device/{endpoint}.json?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (FDA-Plugin/1.0)"})
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            elapsed = (time.time() - start) * 1000
            total = data.get("meta", {}).get("results", {}).get("total", "?")
            print(f"  {endpoint:25s}  OK  ({elapsed:.0f}ms, {total} total records)")
            passed += 1
    except urllib.error.HTTPError as e:
        elapsed = (time.time() - start) * 1000
        if e.code == 404:
            print(f"  {endpoint:25s}  OK  ({elapsed:.0f}ms, 0 results for test query)")
            passed += 1
        else:
            print(f"  {endpoint:25s}  FAIL  (HTTP {e.code}: {e.reason})")
            failed += 1
    except Exception as e:
        elapsed = (time.time() - start) * 1000
        print(f"  {endpoint:25s}  FAIL  ({e})")
        failed += 1
    time.sleep(0.5)  # Brief pause between requests

print()
print(f"Results: {passed}/7 endpoints reachable, {failed} failed")
if failed == 0:
    print("All endpoints operational.")
elif failed == 7:
    print("No endpoints reachable — check network connectivity.")
else:
    print("Some endpoints failed — may be temporary. Retry in a few minutes.")
PYEOF
```

Report the results to the user.

## Settings File Format

The settings file uses YAML frontmatter:

```markdown
---
projects_dir: /mnt/c/510k/Python/510k_projects
batchfetch_dir: /mnt/c/510k/Python/510kBF
extraction_dir: /mnt/c/510k/Python/PredicateExtraction
pdf_storage_dir: /mnt/c/510k/Python/510kBF/510ks
data_dir: /mnt/c/510k/Python/PredicateExtraction
extraction_script: predicate_extractor.py
batchfetch_script: batchfetch.py
ocr_mode: smart
batch_size: 100
workers: 4
cache_days: 5
default_year: null
default_product_code: null
openfda_api_key: null
openfda_enabled: true
---

# FDA Predicate Assistant Settings

This file stores your preferences for the FDA 510(k) pipeline.

## Directory Paths

- **projects_dir**: Root for all project folders — each `/fda:extract` query gets its own subfolder
- **batchfetch_dir**: Legacy location for 510kBF output (510k_download.csv, merged_data.csv)
- **extraction_dir**: Legacy location for PredicateExtraction output (output.csv, pdf_data.json)
- **pdf_storage_dir**: Where downloaded PDFs are organized by year/applicant/productcode
- **data_dir**: Where FDA database files are stored (pmn*.txt, pma.txt, foiaclass.txt)

## Script Configuration

- **extraction_script**: predicate_extractor.py (bundled in plugin at $CLAUDE_PLUGIN_ROOT/scripts/)
- **batchfetch_script**: batchfetch.py (bundled in plugin at $CLAUDE_PLUGIN_ROOT/scripts/)

## Processing Options

- **ocr_mode**: smart (use OCR only when needed), always, never
- **batch_size**: Number of PDFs per processing batch
- **workers**: Parallel processing workers (adjust based on CPU)
- **cache_days**: How long to cache FDA database files

## Filters

- **default_year**: Set to filter by year automatically
- **default_product_code**: Set to filter by product code automatically

## openFDA API

- **openfda_api_key**: API key for higher rate limits (get free key at https://open.fda.gov/apis/authentication/)
- **openfda_enabled**: Set to false to disable all API calls (offline mode)
```

### Migrate Cache Format

If `$ARGUMENTS` is `--migrate-cache`, migrate from monolithic `pdf_data.json` to per-device cache:

```bash
python3 << 'PYEOF'
import json, os

extraction_dir = '/mnt/c/510k/Python/PredicateExtraction'
pdf_json = os.path.join(extraction_dir, 'pdf_data.json')
cache_dir = os.path.join(extraction_dir, 'cache')
devices_dir = os.path.join(cache_dir, 'devices')
index_file = os.path.join(cache_dir, 'index.json')

if not os.path.exists(pdf_json):
    print('ERROR: pdf_data.json not found — nothing to migrate')
    exit(1)

if os.path.exists(index_file):
    print('WARNING: Per-device cache already exists. Merging new entries only.')
    with open(index_file) as f:
        index = json.load(f)
else:
    index = {}

os.makedirs(devices_dir, exist_ok=True)

print(f'Loading pdf_data.json...')
with open(pdf_json) as f:
    data = json.load(f)

migrated = 0
skipped = 0
for filename, content in data.items():
    knumber = filename.replace('.pdf', '')
    if knumber in index:
        skipped += 1
        continue

    # Normalize content format
    if isinstance(content, dict):
        device_data = content
    else:
        device_data = {'text': str(content)}

    # Write individual device file
    device_file = os.path.join(devices_dir, f'{knumber}.json')
    with open(device_file, 'w') as f:
        json.dump(device_data, f)

    # Add to index
    rel_path = os.path.relpath(device_file, extraction_dir)
    index[knumber] = {
        'file_path': rel_path,
        'text_length': len(device_data.get('text', '')),
        'extraction_method': device_data.get('extraction_method', 'unknown'),
        'page_count': device_data.get('page_count', 0)
    }
    migrated += 1

# Write index
with open(index_file, 'w') as f:
    json.dump(index, f, indent=2)

print(f'Migration complete: {migrated} devices migrated, {skipped} already existed')
print(f'Index: {index_file} ({len(index)} total devices)')
print(f'Per-device files: {devices_dir}/')
print(f'Original pdf_data.json preserved (can delete manually when ready)')
PYEOF
```

Report the migration results and note that the original `pdf_data.json` is preserved as a backup.

## Creating Default Settings

If no settings file exists and user wants to configure, create one with the template above using the default values.
