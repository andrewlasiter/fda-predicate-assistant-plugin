# Changelog

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
