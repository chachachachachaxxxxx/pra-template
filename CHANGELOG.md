# Changelog

All notable changes to PRA Template are recorded here.

This project uses semantic versioning for the template and schema surface:

- Patch: documentation updates or validator fixes that do not require project data changes.
- Minor: backward-compatible fields, relation labels, directories, or validator checks.
- Major: breaking schema, directory, or field changes that require migration.

## 0.1.0 - 2026-06-29

- Initial public PRA template.
- Added empty PRA project skeleton under `template/`.
- Added core PHO model documentation.
- Added JSON Schema references for entities, edges, traces, staging items, and sources.
- Added `scripts/pra_validate.py` structural validator.
- Added Codex skill drafts for paper compilation, session compilation, rigor review, and graph curation.
