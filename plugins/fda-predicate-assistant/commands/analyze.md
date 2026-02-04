---
description: Analyze FDA predicate extraction results with statistics, patterns, and recommendations
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[path/to/output.csv]"
---

# FDA Extraction Results Analysis

You are analyzing the results of an FDA 510(k) predicate extraction to provide insights and recommendations.

## Locate the Results File

If a file path is provided in `$ARGUMENTS`, use that. Otherwise, search for output.csv:

```bash
find . -name "output.csv" -type f 2>/dev/null | head -5
```

## Analysis Components

### 1. Statistical Summary

Read the output.csv and calculate:
- Total number of 510(k) submissions analyzed
- Total unique predicate devices found
- Average predicates per submission
- Product code distribution
- Document type breakdown (Statement vs Summary)

### 2. Pattern Detection

Identify interesting patterns:
- **Most common predicates**: Devices frequently cited as predicates
- **Predicate chains**: Submissions that share the same predicates
- **High predicate count**: Submissions citing many predicates (>10)
- **Zero predicates**: Submissions with no predicates found (may need review)
- **Product code clusters**: Groups of related devices

### 3. Anomaly Flagging

Flag potential issues:
- Devices with unusually high/low predicate counts
- Possible OCR errors (numbers with letters that should be digits)
- Missing data fields
- Duplicate entries

### 4. Recommendations

Based on analysis, suggest:
- PDFs that may need manual review
- Filters to refine future extractions
- Product codes to investigate further

## Output Format

Provide a structured report with:
1. **Executive Summary** - Key findings in 2-3 sentences
2. **Statistics** - Tables with counts and percentages
3. **Notable Patterns** - Interesting relationships discovered
4. **Issues Found** - Problems requiring attention
5. **Recommendations** - Actionable next steps

## Also Check

If available, also analyze:
- `supplement.csv` for supplement device patterns
- `error_log.txt` for processing failures
