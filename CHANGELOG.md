# Changelog

## Unreleased

### Changed

- Reduced avoidable interaction pauses by treating prior explicit user choices as resolved checkpoints and by offering connector setup and degraded existing-tool routes together.
- Added exploratory, focused, and coverage-oriented search intent, plus batching, deduplication, retrieval escalation, failover, and bounded-saturation guidance.
- Added declared rubric checks to the theory-model evaluation case so it participates in the evaluation gate.
- Removed the unsupported and redundant `compatibility` frontmatter field so the Skill passes the current structural validator.
- Replaced topic-specific public evaluation prompts and fixture names with neutral synthetic descriptions so public examples do not reveal a maintainer's research direction.
- Unified MCP consent behavior across the Skill and references: ask, wait, install only after approval, and stop the MCP-dependent path on refusal while cleaning only attempt-created temporary files.
- Marked the live MCP smoke record as manual-only; CI does not run model or live-connector tests.

### Added

- Added deterministic public-repository checks for sensitive paths, credentials, Skill metadata, JSON fixtures, and Markdown links.
- Added a weekly, manual-review-only compatibility check for the tracked `paper-search-mcp` revision.

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
