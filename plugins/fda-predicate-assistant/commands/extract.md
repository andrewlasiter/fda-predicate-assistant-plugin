---
description: Run FDA 510(k) predicate extraction on PDF documents
allowed-tools: Bash, Read, Glob
argument-hint: "[directory] [--year YEAR] [--product-code CODE] [--ocr MODE]"
---

# FDA 510(k) Predicate Extraction

You are running the FDA predicate extraction tool to analyze PDF documents and identify device relationships.

## Execution

Run the extraction script using the wrapper:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/run-extraction.sh" $ARGUMENTS
```

If no directory is specified and the script requires GUI interaction, inform the user that they need to select a directory in the GUI that appears.

## Arguments Handling

- **directory**: Pass as first positional argument to the script
- **--year YEAR**: Filter processing to specific year
- **--product-code CODE**: Filter to specific FDA product code
- **--ocr MODE**: Set OCR mode (smart/always/never)

## After Extraction

Once extraction completes:

1. **Check for output files:**
   - `output.csv` - Main extraction results
   - `supplement.csv` - Devices with supplement suffixes
   - `error_log.txt` - List of failed PDFs

2. **Report summary:**
   - Total PDFs processed
   - Number of devices found
   - Any errors encountered

3. **Offer analysis:**
   Ask the user if they'd like a detailed analysis of the results using `/fda:analyze`

## Error Handling

If the script fails:
- Check if Python is available
- Verify the script path exists
- Check for missing dependencies (PyMuPDF, pdfplumber, etc.)
- Suggest running: `pip install requests tqdm PyMuPDF pdfplumber orjson ijson`
