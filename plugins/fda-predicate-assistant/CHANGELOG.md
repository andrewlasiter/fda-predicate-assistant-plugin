# Changelog

## [4.1.1] - 2026-02-06

### Fixed
- LYZ product code removed from wound dressing list in section-patterns.md (LYZ is "Vinyl Patient Examination Glove", not a wound dressing)
- plugin.json version aligned from 4.0.0 to 4.1.1
- All command/agent/reference version strings bumped from v4.1.0 to v4.1.1

## [4.1.0] - 2026-02-06

### Changed
- Retired "Level of Concern" references (concept retired by FDA)
- eSTAR mandatory date corrected to October 1, 2023
- `/fda:test-plan` expanded to 11+ device types with device-specific test batteries
- `/fda:pccp` updated with real examples and expanded guidance

### Added
- Basic/Enhanced performance framework for software devices
- MDUFA V fee schedule references
- PubMed E-utilities integration in `/fda:literature`
- Section 524B cybersecurity requirements in `/fda:safety` and `/fda:assemble`
- DEN number handling in `/fda:validate`
- Peer device benchmarking in `/fda:research`
- 5 new skill references: rta-checklist, pubmed-api, special-controls, clinical-data-framework, post-market-requirements

## [4.0.0] - 2026-02-05

### Added — Tier 1: Full Autonomy Fixes
- Guard all `AskUserQuestion` calls behind explicit `--full-auto` conditionals in review, compare-se, presub, submission-outline
- `--infer` fallback chain in compare-se: review.json → output.csv (top 3 by citation) → pdf_data.json → ERROR (never prompts)
- `--full-auto` validation: require `--device-description` and `--intended-use` in presub and submission-outline (with synthesis fallback from query.json + openFDA)
- Placeholder conversion: all surviving `[INSERT: ...]` → `[TODO: Company-specific — ...]` across presub, submission-outline, compare-se
- Pipeline step criticality: Steps 1-2 (extract/review) CRITICAL (halt on failure), Steps 3-7 NON-CRITICAL (continue with DEGRADED warning)
- Pipeline pre-flight validation: writable project dir, valid product code, full-auto requirements, dependency check
- Pipeline argument threading table: explicit mapping of every arg to downstream steps
- Guidance offline fallback: reference-based guidance summary from skill reference data when cache unavailable
- Safety graceful degradation: structured JSON warning with `safety_data_available: false` when API unavailable
- Extract stage defaults: 3 explicit cases, `--full-auto` requires `--project`
- Headless mode in `predicate_extractor.py`: skip manual download messages, one-line error + `sys.exit(2)` on failure
- Audit logging infrastructure: `references/audit-logging.md` schema, JSONL append per command, consolidated `pipeline_audit.json`

### Added — Tier 2: Best-in-Class Feature Parity
- `/fda:lineage` — Predicate citation chain tracer (up to 5 generations, recall checking, Chain Health Score 0-100)
- `/fda:draft` — Regulatory prose generator for 6 submission sections with citation tracking
- `/fda:literature` — PubMed/WebSearch literature review with gap analysis vs guidance requirements
- `/fda:traceability` — Requirements Traceability Matrix (guidance → risks → tests → evidence)
- `/fda:consistency` — Cross-document consistency validation (8 checks, PASS/WARN/FAIL, optional --fix)
- eSTAR auto-population in `/fda:assemble`: Sections 6/7/8/12/15 auto-written from project data (DRAFT/TEMPLATE/READY markers)
- Cybersecurity auto-detection in `/fda:assemble`: threat model, SBOM, and patch plan templates for software/connected devices
- `--watch-standards` in `/fda:monitor`: track FDA recognized consensus standards changes and impact on projects
- `--identify-code` in `/fda:research`: auto-identify product code from device description via openFDA + foiaclass.txt
- Pipeline Step 0: auto-identify product code when `--product-code` not provided but `--device-description` available

### Added — References
- `audit-logging.md` — JSONL audit log schema and pipeline consolidated log format
- `predicate-lineage.md` — Chain Health Scoring methodology and lineage patterns
- `standards-tracking.md` — FDA recognized consensus standards families and alert schema
- `cybersecurity-framework.md` — Cybersecurity documentation framework, templates, and applicable standards

## [3.0.0] - 2026-02-06

### Added — Tier 1: Autonomy
- `--full-auto` and `--auto-threshold` on `/fda:review` for zero-prompt predicate review
- `--infer` flag on guidance, presub, research, submission-outline, and compare-se for auto-detecting product codes from project data
- `--output FILE` on `/fda:summarize` for file persistence
- `--headless` flag on `predicate_extractor.py` with display detection
- TTY-aware prompts in `batchfetch.py` with non-interactive fallback
- `/fda:pipeline` command — full 7-step autonomous pipeline orchestrator
- Placeholder auto-fill: `[INSERT: ...]` → populated from `--device-description` and `--intended-use`
- Default stage selection in `/fda:extract` (no more prompts)

### Added — Tier 2: Best-in-Class Features
- `/fda:monitor` — real-time FDA clearance, recall, and MAUDE event monitoring
- `/fda:pathway` — algorithmic regulatory pathway recommendation (5 pathways scored 0-100)
- `/fda:test-plan` — risk-based testing plan with ISO 14971 gap analysis
- `/fda:assemble` — eSTAR directory structure assembly (17 sections with readiness tracking)
- `/fda:portfolio` — cross-project portfolio dashboard with shared predicate analysis
- `/fda:pccp` — Predetermined Change Control Plan generator for AI/ML devices
- `/fda:ask` — natural language regulatory Q&A
- `--competitor-deep` on `/fda:research` for applicant frequency, technology trends, and market timeline
- Extended confidence scoring (+20 bonus points: chain depth, SE table, applicant similarity, IFU overlap)

### Added — References
- `estar-structure.md` — eSTAR section structure and applicability matrix
- `pathway-decision-tree.md` — regulatory pathway decision flow and scoring weights
- `test-plan-framework.md` — ISO 14971 risk categories and device-type test lists
- `pccp-guidance.md` — FDA PCCP guidance overview and modification categories

## [2.0.0] - 2026-02-05

### Added
- `/fda:review` — interactive predicate review with 5-component confidence scoring
- `/fda:guidance` — FDA guidance lookup with requirements extraction and testing mapping
- `/fda:presub` — Pre-Submission meeting package generator
- `/fda:submission-outline` — full 510(k) outline with gap analysis
- `confidence-scoring.md` reference with scoring methodology
- `guidance-lookup.md` reference with search strategies
- `submission-structure.md` reference with outline templates

### Changed
- `/fda:extract` now includes safety scan integration
- `/fda:configure` now supports exclusion lists
- `/fda:research` now caches guidance for reuse
- `/fda:compare-se` now integrates with submission outline data
- Marketplace renamed from `local` to `fda-tools`

## [1.2.0] - 2026-02-05

### Added
- Disclaimers and warnings across all user-facing surfaces:
  - README.md: "Important Notices" section (privacy, accuracy, training data, not legal advice)
  - SKILL.md: Always-loaded disclaimer context for regulatory guidance responses
  - research.md: Disclaimer footer in research report output
  - compare-se.md: Disclaimer footer in SE comparison table output
- Section-aware predicate extraction in research command (SE sections weighted 3x)
- [SE]/[Ref] provenance tags on predicate candidates
- Extraction confidence transparency caveat in research output

## [1.1.0] - 2026-02-05

### Changed
- Portable plugin root resolution via `installed_plugins.json` runtime lookup
- Removed hardcoded paths; all data directories default to `~/fda-510k-data/`
- Added SessionStart hook as backup for `FDA_PLUGIN_ROOT` env injection
- Fixed SKILL.md frontmatter to comply with official plugin spec

### Added
- `hooks/hooks.json` with SessionStart hook for `CLAUDE_ENV_FILE` integration
- `hooks/export-plugin-root.sh` for deriving plugin root from script location
- `.gitignore` to exclude `__pycache__/`
- `LICENSE` (MIT)
- `CHANGELOG.md`
- `references/path-resolution.md` with standard resolution patterns

## [1.0.0] - 2026-02-04

### Added
- Initial release with 9 commands: extract, validate, analyze, configure, status, safety, research, compare-se, summarize
- 1 agent: extraction-analyzer
- 1 skill: fda-510k-knowledge with reference docs
- Bundled scripts: `predicate_extractor.py`, `batchfetch.py`, `setup_api_key.py`
- openFDA API integration with configurable API key
- K/P/DEN/N device number regex support
