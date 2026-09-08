# Changelog

## v0.2.3 — 2026-09-08

### Changed

- Made source selection question-led, including the choice between unified and source-specific tools; no default source bundle is required.
- Added publication context as an optional candidate-screening prior, without allowing prestige to replace article-level evidence appraisal.
- Added evidence-led follow-up questions and separated experimental source reports, unavailable details, calculations, transfer proposals, and diagnostic hypotheses.
- Connected substantial retrieval batches to claim updates, decision-relevant evidence gaps, and targeted next actions while preserving coverage-oriented stopping requirements.
- Limited interaction pauses to material user choices; evidence conflicts and independent work continue within the confirmed scope and authorization.
- Integrated decisive-claim source verification into the existing publication audit, with reuse of completed checks for unchanged evidence and wording.
- Extended the existing conflict and state-recovery evaluation cases to cover justified continuation and gap-directed next actions. These behavioral expectations require fresh runs; historical scores do not validate them.

### Fixed

- Preserved unresolved discrepancies within a paper, including abstract/table/figure conflicts; prohibited hiding them in averages, rounded values, or ranges.
- Distinguished extraction errors, snippets in abstract fields, connector defaults, and unavailable methods from verified source facts.
- Aligned source-safety instructions, reference entry points, and evaluation scoring with the runtime evidence rules.
- Supplied neutral synthetic records for fact-checking and transfer cases; separated initial MCP consent from refusal and removed impossible source-verification requirements from strategy-only cases.
- Restricted evaluation case/run identifiers and fixture/output paths, aligned dry runs with baseline exclusions, and marked unselected scoring modes as not applicable.
- Added release-version and fixture-reference consistency checks.
- Added publication-status checks for consequential evidence and result-truncation rules for coverage-oriented searches.
- Included tracked evaluation logs and records in public-content scanning, even under normally ignored runtime directories.
- Disabled discovered standalone user Skills in evaluation subprocesses and documented the remaining host-isolation boundary.
- Preserved declared state-file outputs before temporary-workspace cleanup and returned a failing exit status for unsuccessful evaluation execution.
- Added local regression checks using synthetic data and simulated Codex processes; these do not call a model or connector.

### Validation scope

- This release is reviewed across the tracked project files and checked with deterministic repository and runner checks.
- Revised behavioral cases have not been rerun for this release. Historical smoke scores do not establish v0.2.3 model behavior, literature recall, or live connector compatibility.

## v0.2.2 — 2026-09-01

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
