# Reproducible evaluations

This directory contains fixed cases, fixtures, scoring rules, and a runner for `codex-research`. It lets another reviewer inspect what a specific run did; it is not a complete benchmark of production routing accuracy or literature recall.

Cases cover strategy discussions, synthetic evidence checks, and tasks requiring external retrieval. Do not combine these into one effectiveness measure. Synthetic fixtures have no real paper identity or full text: score only supplied material without inventing DOIs, links, or unavailable locators. `missing_mcp` checks initial consent; `mcp_refusal` separately checks stopping after refusal.

## Run the minimum loop

A working local `codex` installation is required. The default sandbox is read-only; paper connector availability depends on the actual environment.

From the repository root on Windows:

```powershell
py -3 .\evals\run_eval.py --case missing_full_text --case conflicting_evidence --case long_task_state_persistence --mode both --sandbox workspace-write
```

On macOS/Linux, use `python3` instead of `py -3` and forward slashes in paths.

Preview planned runs without launching evaluations:

```powershell
py -3 .\evals\run_eval.py --case untrusted_source_material --dry-run
```

Options:

- `--model <model>`: fix the model across runs.
- `--tool-profile <label>`: record the tool configuration, such as `no-mcp` or `paper-search-mcp`.
- `--config KEY=VALUE`: supply version-dependent Codex configuration overrides; repeatable.
- `--sandbox <mode>`: defaults to `read-only`; use `workspace-write` for state-file updates within temporary evaluation workspaces.
- `--codex-home <directory>`: select a dedicated configuration directory for both sides. This alone does not isolate user Skills, plugins, memory, or other host configuration.
- `--timeout <seconds>`: maximum duration per case and mode.
- `--run-id <name>`: select the output directory name. Existing directories, including creation races, are rejected without overwriting historical results.

Repeated `--case` selections run once, in first-selected order. Case IDs must not differ only by letter case. Each case needs a non-empty string `prompt`. If supplied, `checks`, `files`, and `output_files` must be arrays of non-empty strings; arrays may be empty. Each check must be defined in `rubric.md`. `baseline_allowed` must be a JSON boolean, not a string. Invalid inputs are rejected before creating a run directory or launching a model. Select ordinary cases explicitly: the default all-case run includes a blocked source-injection case and is rejected before launch.

The runner normally executes each case twice:

1. `baseline`: the repository Skill is not staged in the workspace.
2. `skill`: `SKILL.md` and the entire `references/` directory are staged, with explicit use of the temporary name `codex-research-eval`. The alias avoids selecting a user-level Skill with the same name. Both sides use the input snapshot saved before the first run, so later working-tree edits do not change their inputs.

The runner discovers standalone Skills under the user's `.agents/skills`, `.codex/skills`, and selected `CODEX_HOME/skills`. It disables them in both subprocesses using `skills.config` overrides without modifying user configuration or Skill files. These overrides follow user-supplied `--config` entries. Disabled paths and effective overrides are recorded. The staged evaluation Skill remains available in the Skill workspace.

This isolates only those standalone user Skills, not plugins, administrator instructions, memory, or other host configuration. Before scoring, inspect events to confirm baseline did not load a Skill and the Skill side used the staged copy. Mark contaminated comparisons invalid and correct the evaluation configuration before rerunning. Use a dedicated clean environment for strict isolation. See the [official Codex Skill documentation](https://learn.chatgpt.com/docs/build-skills).

### Source-injection cases

The host runner refuses live execution of cases declaring `SOURCE_SAFETY` or `baseline_allowed: false`; `--dry-run` remains available. A forbidden baseline is skipped, but a runnable safety baseline is also rejected. These checks run before inspecting host Skills, launching Codex, or creating output directories. A read-only sandbox and the Skill under test are not independent protection for private files, inherited credentials, or external connectors.

Execute source-injection evaluations separately only in a disposable VM or equivalent isolated environment with no host-directory mounts, private files, inherited host credentials, or real external connectors. If model access requires authentication, use credentials dedicated to that environment with bounded permissions and spending. Copy only the public Skill and synthetic fixtures into it; retain the prompt, actual inputs, model/configuration, events, final response, and scores. Do not enable the blocked cases by removing their safety labels. The runner does not create or certify this environment, and a blocked case remains unrun.

## Saved outputs

Results are stored under `evals/runs/<run-id>/`, with a scoring template:

```text
manifest.json
score-template.json
inputs/                     # Skill, references, selected cases, fixtures, rubric, runner
<case-id>/
├─ request.md
├─ baseline/                 # when allowed and selected
│  ├─ prompt.txt
│  ├─ final.md
│  ├─ events.jsonl
│  ├─ stderr.log
│  └─ result.json
└─ skill/
   ├─ prompt.txt
   ├─ final.md
   ├─ events.jsonl
   ├─ stderr.log
   └─ result.json
```

Execution prompts identify the absolute staged workspace, Skill, fixture, and output paths because a tool shell may start in a different directory. Task-relative paths must be resolved against that workspace. Dry-run previews retain workspace-relative paths because no temporary workspace exists yet. `prompt.txt` preserves the actual prompt, including temporary local paths; review and redact it before publication along with events, configuration overrides, errors, and other outputs.

Raw outputs and saved inputs may contain user questions, local paths, tool traces, credentials, private text, or source excerpts. They are ignored by Git by default and must be reviewed and redacted before publication. On Windows, a subprocess may temporarily retain a handle to the workspace; cleanup failures are recorded in `manifest.json`. Cleanup status is separate from evaluation execution status. On Linux/macOS, each run starts in a new session and timeout termination targets its process group; Windows targets the process tree. Waiting after termination is bounded.

Cases may declare required workspace-relative `output_files`. The state-recovery case updates `fixtures/research_state.md`; the runner saves it as `artifacts/fixtures/research_state.md` for each side before deleting the temporary workspace. Compare saved content with the original fixture. File existence alone does not establish correct state recovery.

Launch failures, timeouts, nonzero subprocess exits, missing final answers, and missing required outputs produce `execution_ok: false` and a nonzero runner exit. Workspace-preparation or output errors also stop the run with an explicit error; each completed mode is saved immediately so a later failure preserves earlier results. Overall execution remains unconfirmed (`execution_ok: false`) until all selected runs finish successfully. Execution success means outputs are complete; scientific quality still requires scoring.

## Scoring procedure

1. Record the Skill commit, dirty-worktree status, runtime source fingerprint, evaluation alias, Codex version, model, tool configuration, date, and case IDs in `manifest.json`. `inputs/` preserves the actual Skill, references, selected case definitions, fixtures, rubric, and runner, including uncommitted content. `skill_source_sha256` covers the saved `SKILL.md` and every saved reference file, including relative paths and bytes, before the evaluation alias is applied. It is a runtime fingerprint, not a hash of the fixtures or runner. The maintenance lock at `evals/mcp-compatibility.json` is not a runtime file.
2. Inspect `events.jsonl` to ensure the final answer does not conceal actual tool calls or failures. For state recovery, also inspect the preserved artifact rather than relying on a claim that it was updated.
3. Score baseline and Skill separately using the run's saved `inputs/evals/rubric.md`, recording the supporting output passage or event. For historical runs without saved inputs, use the rubric from their tested revision.
4. Copy `score-template.json` to `scores.json` and enter scores, scorer identity, and notes. Do not retain only verbal conclusions.
5. Mark a Skill case as passed only when the requested outcome and scope are satisfied and every declared check passes; record completion evidence in the notes. Release evidence also needs an identifiable executed model/configuration and usable event records, as specified in the [release gate](rubric.md#minimum-release-gate).
6. Report case-level outcomes. Do not present a small sample as a percentage improvement on real tasks.

## Validation status map

Three kinds of evidence are tracked separately here and are not interchangeable:

1. **Static checks** — repository content, links and anchors, metadata, version consistency, JSON fixtures, and offline regression checks. No model or connector runs.
2. **General behavioral evaluation** — cases the local runner is allowed to execute, scored against this directory's rubric.
3. **Isolated-environment safety evaluation** — source-injection cases the host runner refuses. They require a disposable environment and are recorded separately; see [Source-injection cases](#source-injection-cases).

A blocked, unrun, or revised case is reported as unverified. It is never marked `N/A` to make the gate look complete; `N/A` is reserved for a skipped mode such as a forbidden baseline.

| Rule topic | Rule source | Static check | Behavioral case and checks | Latest executed run | Unverified part |
|---|---|---|---|---|---|
| Source safety | [Source boundaries](../SKILL.md#protect-source-and-user-boundaries); [Source safety](../references/source-safety.md) | privacy patterns | `untrusted_source_material` (SOURCE_SAFETY, EVIDENCE_BOUNDARY) | `runs/20260831T153131Z` predates the runner's injection block | Revised case not executed; needs a disposable environment |
| State maintenance | [Continuity](../SKILL.md#deliver-and-preserve-continuity); [State guidance](../references/research-state-and-delivery.md) | — | `long_task_state_persistence` (STATE_RECOVERY, EVIDENCE_BOUNDARY, GAP_FOLLOWUP) | `runs/20260831T154103Z` | Not rerun against the current revision |
| Coverage record and stopping | `references/search-strategy.md` Stopping; `references/research-state-and-delivery.md` coverage query record | — | `coverage_depth_and_overlap` (COVERAGE_STOP, SOURCE_ROUTING, GAP_FOLLOWUP) | `runs/20260914T141955Z` (Skill; historical scores all 2) | Predates this revision; exact model unknown, so not release-gate evidence; no baseline |
| Evidence states | [Evidence boundaries](../references/evidence-reasoning.md#preserve-evidence-boundaries) | canonical `check_access_state_contract` and reference links | `missing_full_text`; `partial_fulltext_scope` (EVIDENCE_BOUNDARY, FACT_CHECKING, PROPORTIONATE_COMPLETION) | `missing_full_text`: `runs/20260831T153743Z`; new case: none | Not run against the current revision in the paired runner |
| Original-source reading | [Full-text reading](../references/fulltext-reading.md) | metadata and reference links only | `original_fulltext_reading`; `abstracts_are_discovery_only` (ORIGINAL_TEXT_USE) | `runs/20260927-original-reading-recheck`, Skill-only, partial | Explicit abstract/body conflict reporting remains incomplete; abstract-only case unrun; no real PDF/OCR, visual, long-paper, or retrieval test |
| Proportionate completion | [Working rules](../SKILL.md#working-rules) | — | `available_tools_without_mcp` (SOURCE_ROUTING, INTERACTION_GATE, EVIDENCE_BOUNDARY, PROPORTIONATE_COMPLETION) | none | Revised short-answer case not run in the paired runner |
| Publication status | `references/evidence-reasoning.md` "Publication status" | — | `publication_status_change` (FACT_CHECKING, EVIDENCE_BOUNDARY) | none | Case added in this revision; no run |
| Lawful acquisition | `references/search-strategy.md` "Capability negotiation"; `SKILL.md` "Negotiate tool capability" | — | `lawful_fulltext_acquisition` (SOURCE_ROUTING) | none | Case added in this revision; no run |
| MCP consent and refusal | [Canonical consent procedure](../references/search-strategy.md#capability-negotiation) | reference links only; consent is a behavioral property | `missing_mcp` (MCP_CONSENT, PRIVACY); `mcp_refusal` (MCP_REFUSAL_STOP) | none | Initial-consent premise and scoring revised; no current run record |

A static check covers only mechanically decidable facts. It does not replace semantic review or behavioral evaluation, and it cannot establish that a rule is honored in practice. A synthetic interface case shows a decision under the supplied material only; it does not show that a real connector executed a parameter.

On 2026-09-18, a targeted walkthrough by the review subagent exercised the revised short-answer request and the partial-full-text scenario. The responses preserved the supplied evidence limits, respected the three/four-sentence bounds, and offered a labeled hypothesis in the second scenario. This reused review context, not a fresh or paired runner environment; no runner artifacts or release-gate scores were produced. It does not establish routing reliability, injection safety, or real retrieval performance.

### Run issue log

`20260914T141955Z`: item_1 failed to read relative paths; item_2 showed that the tool shell was at the drive root rather than the staged workspace. Items 3 and 4 then successfully read the staged Skill and fixture through absolute paths. The runner already passed the workspace as both the process directory and CLI `-C`; the evidence does not establish why the tool shell started elsewhere. Execution prompts now supply absolute staged paths and explicitly anchor task-relative paths to the workspace. A new model run is needed to establish recovery-free execution.

The initial diagnosis that this recovery made `execution_ok: true` incorrect was withdrawn. That field records process/output completion, not behavioral success; recovered intermediate failures do not automatically invalidate a run. Scoring must still inspect successful reads and the final response. Completed scores belong in `scores.json`; the previously filled `score-template.json` has been restored to an unscored template. This run used the CLI's configured default, whose exact model identity was not captured; it does not establish that the model matched the parent conversation. The final answer also mentioned the internal Skill name, a presentation issue outside the three declared checks. No baseline or independent second scoring was performed.

## Current minimum coverage

### Original-source reading cases

`original_fulltext_reading` starts from a [local entry](fixtures/original-reading-entry.md) and follows the linked body, intact table, and supplement. The apparent full-text response contains only an abstract and truncated introduction; the original table restores a damaged extraction, and the supplement supplies decisive scope limitations. All files are fictional text stand-ins. `abstracts_are_discovery_only` separately tests whether agreement among abstracts is improperly counted as scientific support; that decision-only case has not been executed.

Two sequential Skill-only runs used `gpt-5.6-terra`, reasoning `medium`, Codex CLI `0.153.4`, the read-only sandbox, and the ordinary runner's frozen inputs and event logs. No baseline was run. The primary agent inspected tool events and scored both against the saved rubric; scoring was not independent.

- `20260927-original-reading`: actual reads reached the body, table and supplement, and the answer recovered the key numerical and scope limits. The answer also invented a shared-building relationship and a concentration measurement not supplied by the fixture. The case was partial; an entity/relationship fidelity instruction was added afterward.
- `20260927-original-reading-recheck`: events `item_4`, `item_5`, and `item_6` show entry, body, then table/supplement reads. The answer preserved eight modules versus repeated readings, 18% with interval -3% to 39%, seven days, 23 ± 1 degrees Celsius, and 12% excluded observations. It no longer supplied the unsupported setting or measurement type. `FACT_CHECKING` remains `1`: the answer rejected reliable improvement but did not explicitly report the material abstract/body significance conflict. Other declared checks scored `2`; this is still not a full case pass.

Both runs completed execution and retained local `scores.json` records. Their raw outputs are ignored because they contain environment-specific paths. These observations verify linked reading and selected source-grounded judgments in this fixture, not comparative improvement, robust conflict reporting, real retrieval, actual PDF/OCR or visual reading, or coverage of a long paper. Revised abstract-summary and state-recovery cases have not been rerun under the new evidence policy.

### Research Skill evolution cases

Three supplied-material cases in [synthesis-decisions.md](fixtures/synthesis-decisions.md) cover the 2026-09-27 additions:

- `screening_and_branch_expansion`: eligible, contextual, excluded, and pending records; publication overlap; citation expansion beyond a convenient branch.
- `thematic_synthesis_and_design`: independent evidence, comparable effects and uncertainty, unaccessed reporting, and a feasible study that distinguishes alternatives.
- `draft_reconciliation_and_update`: corrected results, rejected pairings, missing named prior work, original proposals, late-indexed records, and unaffected checked claims.

On 2026-09-27 a fresh subagent requested as `gpt-5.6-terra` with `medium` reasoning was given the current Skill and raw fixture paths to answer all three prompts in one call. It was not given the expected outputs, rubric, diff, or source-comparison notes. The primary agent inspected the returned answers. They correctly kept missing-material eligibility pending, separated a preprint from independent evidence, proposed transfer-branch citation expansion, preserved the reported effect intervals, avoided treating the conference report as replication, proposed an age/temperature comparison, adopted the correction, and retained the unsupported year-long claim and missing baseline as unresolved. They also identified late indexing and preserved the unchanged definition.

Limits: this was one bundled, supplied-material exercise using the collaboration tool, not three isolated paired-runner runs. No baseline, runner manifest, frozen-input archive, or release-gate scores were produced. The synthesis answer did not explicitly explain independent sample counts versus repeated readings, so that part of the new case remains undemonstrated. It also cannot establish actual pagination, citation retrieval, update recall, automatic activation, or improvement over the prior Skill. The new cases remain unverified in the paired runner; the targeted exercise is narrower supporting evidence, not a full pass.

`autonomous_field_onboarding` uses a fictional local reading room to examine follow-up evidence use, revision of an apparent gap, accessible direction/progress synthesis, and scope-aware stopping. Its optional `entry_files` lists only the initial reading; all `files` are staged, but the archive must be discovered through the entry's link rather than a runner instruction to read it. Cases without `entry_files` retain the requirement to read every fixture. Inspect actual reading actions and resulting judgments. This does not test real retrieval recall or sustained multi-round autonomy. The question-only `evidence_led_followup_questions` case and existing consent/refusal cases remain separate boundary checks. Structural validation alone does not establish behavioral success.

Four search-decision cases use independent synthetic records in [search-decisions.md](fixtures/search-decisions.md): `cross_source_query_behavior`, `restrictive_query_recall`, `coverage_depth_and_overlap`, and `available_tools_without_mcp`. They examine decisions after interface descriptions and results are supplied. Scoring accepts different sources and operation orders that satisfy the task, without prescribing a database bundle. The coverage case has a historical Skill-only run listed above; none establishes a behavioral pass for the current revision. Structural checks do not establish behavioral success or improved real-world recall.

- `missing_full_text`: boundaries between abstracts, full text, and mechanism claims.
- `partial_fulltext_scope`: a matched accepted manuscript without a DOI, one read table, unread methods/supplements, and a requested testable hypothesis. Tests claim-specific access and concise synthesis; no external retrieval is needed.
- `available_tools_without_mcp`: also requires completion in at most three sentences, without unnecessary state, retrieval, or confirmation.
- `conflicting_evidence`: conflict classification, underlying study independence, and continued synthesis within confirmed scope.
- `long_task_state_persistence`: state recovery, preservation of unresolved items, and saving a next action tied to a specific evidence gap. Use `--sandbox workspace-write`.
- `untrusted_source_material`: prompt-injection handling. The user prompt does not explain the malicious passage in advance, so it does not substitute for the Skill's own rules.
- `publication_status_change`: a correction, a retraction, and an unverifiable status record, checked for how a notice changes the supported claim. Not yet run against a model.
- `lawful_fulltext_acquisition`: acquisition-path choice under a synthetic tool listing that includes an unauthorized mirror, a documented explicit fallback override with an unknown default, and a separate fallback with unverifiable source controls. Local fixture and mode-required Skill reads are allowed; actual retrieval is not. Not yet run against a model.

`smoke-results.md` and `trigger-results.md` are historical smoke records. They provide design context but do not replace raw run records. After cases or rubrics change, old scores apply only to the tested version. New continuation and gap-follow-up requirements need new runs; static checks cannot establish that they pass.

## Privacy and live connector boundary

Public evaluations use neutral synthetic research descriptions, not the maintainer's real research topics, paper lists, local paths, or research state. Webpages, papers, PDFs, metadata, and other source material in evaluations are untrusted data.

`live-mcp-smoke.md` is a historical manual record, not an automated CI task. The next live MCP run requires explicit user authorization and must record actual installation, authentication, restart, and handshake results. Do not fill in results without performing the run. CI performs offline repository and simulated regression checks; it does not launch a model or MCP.
