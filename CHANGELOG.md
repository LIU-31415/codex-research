# Changelog

## Unreleased

### Changed

- Added explicit topical screening, noisy-batch diagnosis and source-specific query semantics; distinguished claim-specific direct support from context, transferred evidence and unverified candidates. Strengthened clause-level factual fidelity and added two synthetic behavior cases for mixed relevance and draft-to-source support. These changes do not establish general retrieval reliability.
- Added source-first ordering for selective reviews that need to discover omissions: read original material before seeing the draft or earlier findings, then compare, adjudicate and verify the repair. Draft-informed review remains valid but is not labeled source-first; a fresh context is not proof of independent or correct judgment.
- Added targeted full-text checks for quantitative boundary entries and strict inequalities, decisive design arithmetic and unit conversions, and absence claims about unread figures. Both unassisted appraisals of a real paper still failed; their provenance and limits are recorded without claiming that more instructions solved the omissions. Clarified targeted source review, repair and verification after a missed conflict, with assisted correction tracked separately from blind detection.
- Replaced optional blanket comparison notes with a brief paired source comparison for paper appraisals and relevant consequential assertions. Close distinct assertions individually, report compatible material concisely, and repair missing comparison outcomes before delivery without forcing a separate file or generic checklist.
- Added a mixed theoretical-scope/rounding case and reran the original conflict and compatible-material cases, plus one fresh repeat. Targeted closure checks passed; evaluation notes distinguish primary-agent adjudication, interrupted independent scoring, and a separate failed UI-inventory attempt from an all-check batch pass.
- Added three consequential-claim checkpoints with observable evidence, closing decisions, and targeted recovery: after original reading, when forming a judgment, and before delivery. Required explicit comparison of decision-relevant abstract/conclusion statements with original results and propagation of material conflicts into final wording, without manufacturing discrepancies or mandatory per-sentence records.
- Added a checkpoint-closure rubric and a consistent-reporting control alongside the original-reading conflict case. Structural validation and model behavior remain separate; run evidence and limits are recorded in the evaluation guide.
- Made original-source reading the default requirement for substantive scientific support. Abstracts remain discovery/screening leads or explicitly requested summaries, not supporting evidence; unread or inaccessible original material leaves the affected claim unresolved.
- Added a full-text reading reference covering lawful readable copies, article-wide versus claim-specific reading, long-paper coverage, truncated returns, figure/table interpretation, extraction recovery, and relevant supplements. Parsing a document alone no longer qualifies as having read its body.
- Added proportionate eligibility decisions and citation expansion across research branches; inaccessible evidence stays distinct from excluded work.
- Added an action-scoped synthesis reference for comparable evidence views, thematic judgments, and feasible studies that distinguish competing explanations. Preserved short-answer and experimental-transfer boundaries.
- Separated citation consistency, bibliographic identity, and claim support in formal delivery; added draft-to-source reconciliation, reusable rejected pairings, and incremental review updates.
- Consolidated detailed capability negotiation, evidence-state definitions, claim appraisal, and publication audit guidance in the existing references; shortened the entrypoint and description, and routed reference reads by the current action.
- Made user/host precedence, proportionate evidence records, conditional conclusions, and original grounded hypotheses explicit. State files and full evidence schemas are not prerequisites for a short answer or for useful synthesis during writing.
- Made full-text access claim-specific, including partial reads, unread supplements, manuscript versions, and reliable identity matches without a DOI. Distinguished shared authors or methods from duplicated underlying evidence.
- Aligned bounded unresolved delivery with continued independent work and preserved stricter coverage stopping conditions. Field maps are useful research updates, not a mandatory extra deliverable before every search.
- Distinguished source instructions from separately authorized actions, allowed quiet handling of separable injection, and preserved real research topics in intended user deliverables while keeping public Skill examples neutral.
- Aligned research-state writes and setup cleanup with existing authorization; otherwise the target and purpose must be explained before asking for approval.
- Made scoped autonomous investigation the central research loop: analyze questions, check evidence, pursue useful follow-ups, and revise the field map.
- Distinguished in-scope follow-up work from user decisions and deferred extensions; scoped field overviews no longer require choosing a specialty first.
- Added proportionate checks against apparent gaps, incremental explanations for newcomers, and question/gap status in the existing research state.
- Added a synthetic field-onboarding case and rubric for follow-up evidence use, gap revision, and bounded synthesis. This does not establish real-world retrieval performance.
- Removed the conditional "when available" wording from the entrypoint's source-safety read, and rewrote evaluation-framed notes inside the runtime documents as ordinary rules.
- Kept the research-state triggers and structure in one reference; the entrypoint links them instead of enumerating a second trigger list.
- Gave the coverage query record a home in the state template, and made a user-declared time, cost, or retrieval-count limit an explicit stopping boundary while prohibiting fabricated budgets or access limits.
- Added checkpoint closing conditions so a reported checkpoint is not treated as resolved while its blocking condition remains.
- Aligned known-paper validation so the diagnostic paper may come from the user or from an already verified in-scope record, and is run only when it could change a judgment.
- Added conditional guidance for regional or non-English source coverage, for recording data and code provenance when a conclusion depends on it, for distinguishing a retrieval unknown from a source-reporting unknown, and for qualitative weighting after ruling out vote counting.

### Added

- Added a linked synthetic original-reading case and an abstract-only corroboration case, with a rubric that distinguishes observed reading from a proposed reading plan. Preserved explicitly supplied-material tasks.
- Added a pinned comparison of public research Skills, documenting adopted ideas, existing equivalents, and rejected fixed workflows or unsupported gap claims.
- Added synthetic screening, synthesis/design, and draft/update cases with outcome-based rubric checks. Execution evidence and limits are recorded separately in the evaluation guidance.
- Added a validation status map in `evals/README.md` linking each tracked rule topic to its rule source, static check, behavioral case, latest executed run, and unverified part.
- Added two narrow behavioral cases, `publication_status_change` and `lawful_fulltext_acquisition`, with matching rubric conditions for publication status and lawful acquisition.
- Documented three separate validation states — static checks, general behavioral evaluation, and isolated-environment safety evaluation. A case must satisfy its requested outcome and scope as well as pass all declared checks; release evidence also requires identifiable model/configuration and auditable events.
- Added static checks for local Markdown heading anchors, including cross-file and same-page links, and for the canonical access-state vocabulary in the evidence reference.
- Added a partial-full-text case and a proportionate-completion rubric, and strengthened the existing short evidence task to check appropriate stopping.

### Fixed

- Preserved completed evaluation modes in the manifest before starting the next one; workspace-preparation and output errors now return an explicit failed run instead of losing earlier results from the manifest.
- Corrected a platform-dependent regression assertion to require the absolute workspace path in the execution prompt using the same path format on Windows and Linux.
- Corrected the new anchor checker to reject repository escapes before reading targets, skip non-Markdown fragments and fenced examples, decode local fragments, and preserve identifier underscores and distinct duplicate-heading anchors.
- Made the access-state check inspect the canonical declarations, rejecting missing, extra, duplicate, or removed states rather than incidental mentions. Removed exact-sentence consent checks and duplicate entrypoint declarations; link checks and behavioral cases cover their respective contracts.
- Aligned consent/refusal and fact-checking scoring with the case's actual capability gap, authorization, available records, and task boundary, without demanding unperformed future setup or nonexistent cleanup.
- Reconciled state-file recommendations with conversation-only preferences, removed wording that could conceal unintended actions, and aligned the two definitions of `N/A`.
- Allowed fixture reads in the lawful-acquisition case and separated an explicit safe override from an unverifiable fallback, without treating a proposed parameter as executed.
- Reported malformed evaluation arrays and compatibility-lock fields as validation failures instead of crashes; offline lock checks now reject invalid repository URLs.
- Restored location-level evidence as a required capability check when selecting academic tools.
- Rejected active source-injection evaluations in the host runner before launch; kept dry-run previews and documented separate disposable-environment execution.
- Saved Skill, fixture, case, rubric, and runner inputs once per run; both modes now stage from that snapshot and fingerprint the saved runtime.
- Terminated the Linux/macOS process group on evaluation timeout and bounded post-termination waiting; retained Windows process-tree termination.
- Reported malformed metadata values without a misleading secondary length or name error; length errors now include the parsed character count.
- Validated trigger-evaluation queries and boolean expectations, including missing fields.
- Clarified release ZIP placement and the distinction between workflow files and bundled license/version metadata.

### Validation scope

- The goal/connection review passed the offline regression suite and Skill structural validator. A targeted subagent walkthrough produced correct short-answer and partial-full-text responses; it reused the review context and is not a blind or paired evaluation. New and revised cases still lack current paired-run evidence, and no live MCP or real-world retrieval performance was tested. See `evals/README.md` for the validation boundaries.

## v0.2.4 — 2026-09-10

### Changed

- Adapted queries to each interface's declared syntax, fields, and filter scope while distinguishing declarations from observed execution.
- Replaced one-way query narrowing with coverage-aware refinement, separating retrieval concepts from screening criteria and adding proportionate recall diagnostics before consequential gap or completion claims.
- Added four synthetic decision cases for cross-source filters, restrictive queries, truncated results with source overlap, and sufficient capabilities without a named MCP. These cases have not yet been run against a model.

### Fixed

- Validated the project's frontmatter format, duplicate fields, description length, and supported metadata values without adding a dependency.
- Moved the connector revision lock to `evals/` and included all recursive runtime reference files in the source fingerprint.
- Rejected undefined rubric checks before evaluation and handled concurrent run-directory creation without overwriting outputs.
- Used workspace-relative fixture paths in actual and saved prompts, preserving their agreement without claiming that other raw logs are sanitized.
- Made unauthorized fallback download restrictions explicit in the Skill entrypoint and kept evaluation aliasing compatible with quoted names.
- Reported temporary-workspace initialization failures as incomplete regression checks with a distinct exit status.
- Deduplicated repeated case selections and rejected case identifiers that collide on case-insensitive filesystems, preventing evaluation output replacement.
- Validated prompts, list fields, and the baseline permission flag before starting evaluations; rejected failed Codex version probes.
- Limited the privacy scanner's self-exclusion to its own repository path and included tracked environment files in scanning.
- Accepted local Markdown links with spaces or URL encoding, handled empty destinations, and reported unreadable files and missing scoring rubrics as check failures.

### Maintenance

- Unified the evaluation and run-output guides in English and clarified fingerprint, raw-log privacy, and temporary-directory boundaries.
- Added a runtime-only release ZIP, with maintenance and evaluation files retained in source archives only.
- Added offline regression coverage for these failures and validation of the repository's current evaluation cases.
- Consolidated README features, added usage and maintenance instructions, and documented evaluation input and output behavior.
- Expanded environment-file ignore rules to cover `.env.*` and `*.env` files.
- Updated checkout and Python setup actions to v7 in both workflows, replacing their deprecated Node.js 20 runtime with Node.js 24.

### Validation scope

- Maintenance checks use local repository content, synthetic fixtures, and simulated processes. They do not establish model behavior or live MCP compatibility.

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
