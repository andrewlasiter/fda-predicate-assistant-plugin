![Version](https://img.shields.io/badge/version-4.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Commands](https://img.shields.io/badge/commands-26-orange)
![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-blueviolet)
![FDA 510(k)](https://img.shields.io/badge/FDA-510(k)-red)

# FDA Tools — Claude Code Plugin Marketplace

AI-powered tools for FDA medical device regulatory work. Built for regulatory affairs professionals working on 510(k) submissions.

## Install

In Claude Code or Claude Desktop, type:

```
/plugin marketplace add andrewlasiter/fda-predicate-assistant-plugin
/plugin install fda-predicate-assistant@fda-tools
```

Start a new session to load the plugin.

## What You Can Do

- **Find predicates** — Search FDA databases, trace predicate lineage, and validate device numbers
- **Analyze safety** — Pull MAUDE adverse events and recall history for any product code
- **Plan your submission** — Get pathway recommendations, generate testing plans, and prepare Pre-Sub packages
- **Generate documents** — Substantial equivalence tables, submission outlines, regulatory prose drafts
- **Assemble for filing** — eSTAR-structured packages, traceability matrices, cross-document consistency checks
- **Run it all at once** — Full autonomous pipeline from extraction through SE comparison

## Plugins

### [FDA Predicate Assistant](./plugins/fda-predicate-assistant/)

26 commands covering every stage of the 510(k) workflow — from predicate research to eSTAR assembly. Integrates with all 7 openFDA Device API endpoints and bundles Python scripts for batch PDF processing.

See the [full documentation](./plugins/fda-predicate-assistant/README.md) for commands, installation details, and quick start examples.

## License

MIT
