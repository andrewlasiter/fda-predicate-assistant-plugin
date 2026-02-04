---
description: View or modify FDA predicate assistant settings
allowed-tools: Read, Write
argument-hint: "[--show | --set KEY VALUE]"
---

# FDA Predicate Assistant Configuration

You are managing configuration settings for the FDA predicate extraction tool.

## Settings File Location

Settings are stored in: `~/.claude/fda-predicate-assistant.local.md`

## Available Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `ocr_mode` | `smart` | OCR processing mode: smart, always, never |
| `batch_size` | `100` | Number of PDFs to process per batch |
| `workers` | `4` | Number of parallel processing workers |
| `cache_days` | `5` | Days to cache FDA database files |
| `default_year` | `null` | Default year filter (null = all years) |
| `default_product_code` | `null` | Default product code filter |

## Commands

### Show Current Settings

If `$ARGUMENTS` is `--show` or empty, read and display the current settings:

```bash
cat ~/.claude/fda-predicate-assistant.local.md 2>/dev/null || echo "No settings file found, using defaults"
```

### Set a Value

If `$ARGUMENTS` starts with `--set`, parse KEY and VALUE, then update the settings file.

## Settings File Format

The settings file uses YAML frontmatter:

```markdown
---
ocr_mode: smart
batch_size: 100
workers: 4
cache_days: 5
default_year: null
default_product_code: null
---

# FDA Predicate Assistant Settings

This file stores your preferences for the FDA predicate extraction tool.

## Notes

Add any personal notes about your configuration here.
```

## Creating Default Settings

If no settings file exists and user wants to configure, create one with defaults:

```markdown
---
ocr_mode: smart
batch_size: 100
workers: 4
cache_days: 5
default_year: null
default_product_code: null
---

# FDA Predicate Assistant Settings

Configuration for the FDA 510(k) predicate extraction tool.

## Available Options

- **ocr_mode**: smart (use OCR only when needed), always, never
- **batch_size**: Number of PDFs per processing batch
- **workers**: Parallel processing workers (adjust based on CPU)
- **cache_days**: How long to cache FDA database files
- **default_year**: Set to filter by year automatically
- **default_product_code**: Set to filter by product code automatically
```
