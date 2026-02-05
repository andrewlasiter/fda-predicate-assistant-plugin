---
description: View or modify FDA predicate assistant settings and data directory paths
allowed-tools: Read, Write
argument-hint: "[--show | --set KEY VALUE]"
---

# FDA Predicate Assistant Configuration

You are managing configuration settings for the FDA predicate extraction pipeline.

## Settings File Location

Settings are stored in: `~/.claude/fda-predicate-assistant.local.md`

## Available Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `batchfetch_dir` | `/mnt/c/510k/Python/510kBF` | Directory containing 510BAtchFetch Working2.py |
| `extraction_dir` | `/mnt/c/510k/Python/PredicateExtraction` | Directory containing Test79.py |
| `pdf_storage_dir` | `/mnt/c/510k/Python/510kBF/510ks` | Where downloaded PDFs are stored |
| `extraction_script` | `Test79.py` | Which extraction script version to use |
| `ocr_mode` | `smart` | OCR processing mode: smart, always, never |
| `batch_size` | `100` | Number of PDFs to process per batch |
| `workers` | `4` | Number of parallel processing workers |
| `cache_days` | `5` | Days to cache FDA database files |
| `default_year` | `null` | Default year filter (null = all years) |
| `default_product_code` | `null` | Default product code filter |

## Commands

### Show Current Settings

If `$ARGUMENTS` is `--show` or empty, read and display the current settings:

Read the settings file at `~/.claude/fda-predicate-assistant.local.md`. If it doesn't exist, report defaults and offer to create one.

### Set a Value

If `$ARGUMENTS` starts with `--set`, parse KEY and VALUE, then update the settings file.

Validate the key is one of the known settings before writing. For directory paths, verify the directory exists.

## Settings File Format

The settings file uses YAML frontmatter:

```markdown
---
batchfetch_dir: /mnt/c/510k/Python/510kBF
extraction_dir: /mnt/c/510k/Python/PredicateExtraction
pdf_storage_dir: /mnt/c/510k/Python/510kBF/510ks
extraction_script: Test79.py
ocr_mode: smart
batch_size: 100
workers: 4
cache_days: 5
default_year: null
default_product_code: null
---

# FDA Predicate Assistant Settings

This file stores your preferences for the FDA 510(k) pipeline.

## Directory Paths

- **batchfetch_dir**: Where 510BAtchFetch resides (has 510k_download.csv, merged_data.csv)
- **extraction_dir**: Where PredicateExtraction resides (has output.csv, pdf_data.json)
- **pdf_storage_dir**: Where downloaded PDFs are organized by year/applicant/productcode

## Processing Options

- **extraction_script**: Test79.py (latest), Test78.py, Test76.py
- **ocr_mode**: smart (use OCR only when needed), always, never
- **batch_size**: Number of PDFs per processing batch
- **workers**: Parallel processing workers (adjust based on CPU)
- **cache_days**: How long to cache FDA database files

## Filters

- **default_year**: Set to filter by year automatically
- **default_product_code**: Set to filter by product code automatically
```

## Creating Default Settings

If no settings file exists and user wants to configure, create one with the template above using the default values.
