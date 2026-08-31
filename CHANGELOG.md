# Changelog

## v0.2.1 — 2026-09-01

### Changed

- Consolidated installation guidance in `README.md` and removed redundant installation documents.
- Added an explicit user-consent checkpoint before Codex installs or configures an academic MCP connector.
- Added runtime privacy guardrails for local paths, credentials, private research context, external transfers, and public artifacts.
- Removed user-specific paths and research-topic details from public documentation and evaluation records.

## v0.2.0 — 2026-08-31

### Added

- Added a source-safety boundary for webpages, papers, PDFs, metadata, OCR/XML/HTML, code blocks, and user-provided research material.
- Added `references/source-safety.md` with prompt-injection handling guidance.
- Added a minimal reproducible evaluation loop with fixed fixtures, baseline/Skill comparison, event traces, manifests, scoring rubric, and run records.
- Added Codex-oriented and human-oriented installation guides.

### Fixed

- Evaluation prompts are sent as UTF-8 on Windows.
- Evaluation workspaces are explicitly authorized with `--add-dir`.
- Windows evaluation timeouts terminate the complete subprocess tree and release temporary workspaces.
- Evaluation runs use a temporary Skill alias so a stale user-level installation cannot silently replace the tested source.

### Validation

- Codex CLI: `0.116.0`
- Configuration override: `service_tier="fast"`
- Tool profile: `no-mcp`
- The latest successful Skill runs passed every declared check in the four release cases.
- The evaluation remains a small fixture-backed audit, not a production retrieval or reliability benchmark.
