![Version](https://img.shields.io/badge/version-5.7.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Commands](https://img.shields.io/badge/commands-35-orange)
![Agents](https://img.shields.io/badge/agents-4-purple)
![Tests](https://img.shields.io/badge/tests-712-brightgreen)
![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-blueviolet)
![FDA 510(k)](https://img.shields.io/badge/FDA-510(k)-red)

> **CONFIDENTIAL DATA WARNING**
>
> This plugin processes text through Anthropic's Claude LLM. **Do not submit trade secrets, proprietary device designs, unpublished clinical data, or confidential regulatory strategies.** See [Protecting Your Data](#protecting-your-data) below for details on training policies and opt-out options by account type.

# FDA Predicate Assistant

**Your AI-powered regulatory assistant for FDA 510(k) submissions.**

From predicate research to CDRH Portal submission — 35 commands, 4 autonomous agents, and 712 tests that handle the data work so you can focus on the science and strategy. Search FDA databases, identify predicates, analyze safety histories, look up standards, generate substantial equivalence comparisons, draft all 18 eSTAR sections, simulate FDA review, maintain your extraction corpus, assemble submission-ready packages, and get step-by-step submission guidance, all from within Claude.

---

## Installation

### From your terminal

```bash
claude plugin marketplace add andrewlasiter/fda-predicate-assistant
claude plugin install fda-predicate-assistant@fda-tools
```

### From inside a Claude Code or Claude Desktop session

```
/plugin marketplace add andrewlasiter/fda-predicate-assistant
/plugin install fda-predicate-assistant@fda-tools
```

Start a new session after installing to load the plugin.

### Co-work / Autonomous Sessions

Co-work uses your existing plugin installation — install using either method above first. Once installed, the plugin is automatically available in all Co-work sessions.

### Verify It Works

```
/fda:status
```

You should see a summary of available FDA data files, script availability, and record counts.

---

## Quick Start

```
/fda:status                              # Check what data is available
/fda:validate K241335                    # Look up any device number
/fda:research QAS                        # Full submission research for a product code
/fda:ask "What class is a cervical fusion cage?"   # Regulatory Q&A
/fda:pipeline OVE --project demo         # Run the full pipeline end-to-end
```

---

## Commands

### Getting Started

| Command | What it does |
|---------|-------------|
| `/fda:status` | Shows what FDA data you have downloaded, how fresh it is, and what's available |
| `/fda:configure` | Sets up API keys, data directories, and your preferences |
| `/fda:ask` | Answers regulatory questions in plain language — classification, pathways, testing |
| `/fda:validate` | Checks any device number (K, P, DEN, N) against FDA databases |

### Research & Intelligence

| Command | What it does |
|---------|-------------|
| `/fda:research` | Comprehensive submission research — predicates, testing landscape, competitive analysis |
| `/fda:pathway` | Recommends the best regulatory pathway (Traditional/Special/Abbreviated 510(k), De Novo, PMA) |
| `/fda:literature` | Searches PubMed and the web for clinical evidence, then identifies gaps vs. guidance |
| `/fda:lineage` | Traces predicate citation chains across generations and flags recalled ancestors |
| `/fda:safety` | Pulls adverse events (MAUDE) and recall history for any product code or device |
| `/fda:standards` | Looks up FDA Recognized Consensus Standards by product code, standard number, or keyword |
| `/fda:udi` | Looks up UDI/GUDID records from openFDA — search by device identifier, product code, company, or brand |

### Data Extraction & Maintenance

| Command | What it does |
|---------|-------------|
| `/fda:extract` | Downloads 510(k) PDFs and extracts predicate relationships from them |
| `/fda:analyze` | Runs statistics and finds patterns across your extraction results |
| `/fda:summarize` | Compares sections (testing, IFU, device description) across multiple devices |
| `/fda:monitor` | Watches FDA databases for new clearances, recalls, and MAUDE events |
| `/fda:gap-analysis` | Cross-references FDA PMN database vs. your data to find missing K-numbers, PDFs, and extractions |
| `/fda:data-pipeline` | 4-step data maintenance pipeline — gap analysis, download missing PDFs, extract predicates, merge results |

### Review & Planning

| Command | What it does |
|---------|-------------|
| `/fda:review` | Scores and triages extracted predicates — accept, reject, or flag each one |
| `/fda:propose` | Manually propose predicate and reference devices — validates against openFDA, scores confidence, compares IFU |
| `/fda:guidance` | Finds relevant FDA guidance documents and maps them to testing requirements |
| `/fda:test-plan` | Generates a risk-based testing plan with gap analysis |
| `/fda:presub` | Creates a Pre-Submission meeting package (cover letter, topics, questions) |

### Document Generation

| Command | What it does |
|---------|-------------|
| `/fda:submission-outline` | Builds a full 510(k) submission outline with section checklists and gap analysis |
| `/fda:compare-se` | Generates substantial equivalence comparison tables, auto-populated from FDA data |
| `/fda:draft` | Writes regulatory prose for 18 submission sections with citations |
| `/fda:pccp` | Creates a Predetermined Change Control Plan for AI/ML or iterative devices |
| `/fda:calc` | Regulatory calculators — shelf life (ASTM F1980), sample size, sterilization dose |

### Assembly & Validation

| Command | What it does |
|---------|-------------|
| `/fda:import` | Imports eSTAR data from PDF or XML into project data |
| `/fda:export` | Exports project data as eSTAR-compatible XML or zip package |
| `/fda:assemble` | Assembles an eSTAR-structured submission package from your project data |
| `/fda:traceability` | Generates a requirements traceability matrix (guidance → risks → tests → evidence) |
| `/fda:consistency` | Validates that device descriptions, intended use, and predicates match across all files |
| `/fda:portfolio` | Cross-project dashboard — shared predicates, common guidance, submission timelines |

### Quality & Pre-Filing

| Command | What it does |
|---------|-------------|
| `/fda:pre-check` | Simulates an FDA review team's evaluation — RTA screening, deficiency identification, readiness score |
| `/fda:pipeline` | Runs all stages autonomously: extract → review → safety → guidance → presub → outline → SE |

---

## Agents

The plugin includes 4 autonomous agents that can run multi-step workflows without manual intervention. Agents are invoked automatically by Claude when relevant, or can be triggered via the Task tool.

| Agent | What it does |
|-------|-------------|
| `extraction-analyzer` | Analyzes predicate extraction results — identifies patterns, reviews quality, auto-triages by confidence |
| `submission-writer` | Drafts all 18 eSTAR sections sequentially, runs consistency checks, assembles the package, and reports a readiness score |
| `presub-planner` | Researches the regulatory landscape, analyzes guidance, gathers safety intelligence, reviews literature, and generates a complete Pre-Sub package |
| `review-simulator` | Simulates a multi-perspective FDA review — each reviewer evaluates independently, findings are cross-referenced, and a detailed readiness assessment is generated |

---

## Autonomous Mode

The plugin can run fully unattended — no prompts, no manual steps. This is ideal for Co-work sessions, batch processing, or overnight runs.

| Flag | What it does |
|------|-------------|
| `--full-auto` | Makes all decisions automatically using score thresholds (never prompts) |
| `--infer` | Auto-detects your product code from project data |
| `--headless` | Non-interactive mode for use inside Python scripts |

**Example — fully autonomous pipeline:**

```
/fda:pipeline OVE --project my-device --full-auto \
  --device-description "Cervical interbody fusion cage" \
  --intended-use "For fusion of the cervical spine"
```

---

## openFDA Integration

The plugin connects to all 7 openFDA Device API endpoints for real-time access to clearances, classifications, adverse events, recalls, registrations, UDI data, and COVID-related authorizations.

**API features used:** `sort`, `skip` (pagination), `_count` (aggregations), OR-batched multi-value queries, wildcard search, field-specific queries. Responses are cached with 7-day TTL and exponential backoff retry.

It also works offline using cached FDA flat files — no internet required for basic lookups.

**First run:** The plugin detects when no API key is configured and offers guided setup:

```
/fda:configure --setup-key
```

---

## Data Pipeline

The plugin bundles Python scripts for batch processing and corpus maintenance:

1. **Gap Analysis** — Cross-references FDA PMN database, your extraction CSV, and downloaded PDFs to identify what's missing
2. **BatchFetch** — Filters the FDA catalog by product code, date range, or company, then downloads 510(k) summary PDFs
3. **Predicate Extractor** — Extracts device numbers from downloaded PDFs with OCR error correction and FDA database validation
4. **Merge** — Combines per-year extraction CSVs into the master baseline

Run `/fda:data-pipeline status` to see the current state, or `/fda:data-pipeline run --years 2025` to execute the full pipeline for a specific year.

---

## Section Detection

510(k) PDFs vary widely in formatting — different section headings, OCR artifacts from scanned documents, EU-style terminology. The plugin uses a **3-tier section detection system** to handle this:

1. **Tier 1: Regex** — Fast deterministic matching against 13 universal and 5 device-type-specific heading patterns
2. **Tier 2: OCR-Tolerant** — Applies an OCR substitution table (e.g., `1→I`, `0→O`, `5→S`) and retries Tier 1, allowing up to 2 character corrections per heading
3. **Tier 3: LLM Semantic** — Classifies sections by content signals (2+ keyword matches in a 200-word window) and maps non-standard headings (34 EU/novel terms) to canonical FDA section names

All commands that read PDF sections (`/fda:summarize`, `/fda:research`, `/fda:review`, `/fda:compare-se`, `/fda:lineage`, `/fda:presub`, `/fda:propose`) use this system. The patterns are maintained in a single canonical file (`references/section-patterns.md`) to prevent drift.

---

## Requirements

- Claude Code 1.0.33 or later
- Python 3.x (for extraction scripts)
- `pip install requests tqdm PyMuPDF pdfplumber` (for PDF processing)

---

## Updating

To update to the latest version:

```
/plugin update fda-predicate-assistant
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Commands don't appear after install | Start a new session — plugins load at startup |
| `/plugin install` fails | Check your internet connection; verify the marketplace is registered with `/plugin list` |
| Python errors during extraction | Run `pip install requests tqdm PyMuPDF pdfplumber` |
| "Rate limited" from openFDA | Set up a free API key: `/fda:configure --setup-key` |
| Plugin seems outdated | Run `/plugin update fda-predicate-assistant` |

---

## Protecting Your Data

All text you provide to this plugin — device descriptions, intended use statements, file contents, command arguments — is sent to Anthropic's Claude LLM for processing. Your data protection depends on your Anthropic account type.

### Training Policy by Account Type

| Account Type | Data Used for Training? | Retention | How to Opt Out |
|-------------|------------------------|-----------|----------------|
| **Free / Pro / Max** (consumer) | **Yes, by default** (since Sep 28, 2025) | 5 years if training enabled; 30 days if disabled | [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls) |
| **Team / Enterprise** (commercial) | **No** — Anthropic does not train on commercial data | 30 days (customizable for Enterprise) | Already protected by commercial terms |
| **API** (direct) | **No** (unless opted in to Developer Partner Program) | 30 days (7 days for API logs) | Already protected by API terms |
| **Bedrock / Vertex / Foundry** | **No** — third-party provider terms apply | Provider-specific | Already protected |

### Recommendations for Confidential Work

1. **Use a Team or Enterprise account** — commercial terms explicitly prohibit training on your data
2. **If on a consumer plan**: disable model improvement at [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls) before using the plugin with any sensitive content
3. **Enterprise users**: configure custom data retention (minimum 30 days) via Admin Settings > Data and Privacy
4. **Zero data retention**: available for Enterprise and API customers by arrangement with Anthropic
5. **Never submit**: trade secrets, unpublished clinical data, proprietary designs, patient-identifiable information, or confidential regulatory strategies through any consumer account regardless of settings

### What This Plugin Sends to Claude

- Device descriptions and intended use statements you provide
- K-numbers, product codes, and regulatory identifiers (public FDA data)
- File contents when you use `/fda:import` or reference local files
- Command arguments and conversation context

The plugin does NOT send your files to any server other than Anthropic's API. openFDA queries go directly to api.fda.gov. PDF downloads come directly from accessdata.fda.gov.

> **Sources**: [Anthropic Data Usage (Claude Code)](https://code.claude.com/docs/en/data-usage) | [Anthropic Privacy Center](https://privacy.claude.com) | [Consumer Terms Update (Sep 2025)](https://www.anthropic.com/news/updates-to-our-consumer-terms)

---

### Important Notices

**Research purposes only.** This tool analyzes publicly available FDA data (510(k) summaries, classification databases, MAUDE reports, and other records published by the U.S. Food and Drug Administration).

**LLM accuracy is not guaranteed.** Large language models make mistakes. Device number extraction, predicate identification, section classification, and all other outputs may contain errors, omissions, or hallucinations. Always independently verify every device number, predicate relationship, regulatory citation, and testing recommendation before relying on it.

**Not legal or regulatory advice.** Consult qualified regulatory affairs professionals and legal counsel before making submission decisions. The developers and Anthropic accept no liability for regulatory outcomes based on this tool's output.

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history.

## License

MIT
