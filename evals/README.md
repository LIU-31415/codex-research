# Reproducible evaluations

This directory contains fixed cases, fixtures, scoring rules, and a runner for `codex-research`. It lets another reviewer inspect what a specific run did; it is not a complete benchmark of production routing accuracy or literature recall.

Cases cover strategy discussions, synthetic evidence checks, and tasks requiring external retrieval. Do not combine these into one effectiveness measure. Synthetic fixtures have no real paper identity or full text: score only supplied material without inventing DOIs, links, or unavailable locators. `missing_mcp` checks initial consent; `mcp_refusal` separately checks stopping after refusal.

## Run the minimum loop

A working local `codex` installation is required. The default sandbox is read-only; paper connector availability depends on the actual environment.

From the repository root on Windows:

```powershell
py -3 .\evals\run_eval.py --case missing_full_text --case conflicting_evidence --case long_task_state_persistence --mode both --sandbox workspace-write
```

On macOS/Linux, use `python3` instead of `py -3` and forward slashes in paths. The safety fixture runs only the Skill side by default and keeps the read-only sandbox:

```powershell
py -3 .\evals\run_eval.py --case untrusted_source_material --mode skill
```

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

Repeated `--case` selections run once, in first-selected order. Case IDs must not differ only by letter case. Each case needs a non-empty string `prompt`. If supplied, `checks`, `files`, and `output_files` must be arrays of non-empty strings; arrays may be empty. Each check must be defined in `rubric.md`. `baseline_allowed` must be a JSON boolean, not a string. Invalid inputs are rejected before creating a run directory or launching a model.

The runner normally executes each case twice:

1. `baseline`: the repository Skill is not staged in the workspace.
2. `skill`: `SKILL.md` and the entire `references/` directory are staged, with explicit use of the temporary name `codex-research-eval`. The alias avoids selecting a user-level Skill with the same name; the source is the current working tree.

The runner discovers standalone Skills under the user's `.agents/skills`, `.codex/skills`, and selected `CODEX_HOME/skills`. It disables them in both subprocesses using `skills.config` overrides without modifying user configuration or Skill files. These overrides follow user-supplied `--config` entries. Disabled paths and effective overrides are recorded. The staged evaluation Skill remains available in the Skill workspace.

This isolates only those standalone user Skills, not plugins, administrator instructions, memory, or other host configuration. Before scoring, inspect events to confirm baseline did not load a Skill and the Skill side used the staged copy. Mark contaminated comparisons invalid and correct the evaluation configuration before rerunning. Use a dedicated clean environment for strict isolation. See the [official Codex Skill documentation](https://learn.chatgpt.com/docs/build-skills).

Cases containing active prompt injection may declare `baseline_allowed: false` in `evals.json`. Only the Skill side then runs, avoiding exposure of an unguarded baseline to material that might induce unsafe file or command operations.

## Saved outputs

Results are stored under `evals/runs/<run-id>/`, with a scoring template:

```text
manifest.json
score-template.json
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

Fixture paths in prompts are relative to the subprocess working directory. `prompt.txt` preserves the actual prompt sent to Codex. This avoids inserting temporary absolute paths into fixture instructions, but does not sanitize events, configuration overrides, errors, or other outputs.

Raw outputs may contain user questions, local paths, tool traces, credentials, private text, or source excerpts. They are ignored by Git by default and must be reviewed and redacted before publication. On Windows, a subprocess may temporarily retain a handle to the workspace; cleanup failures are recorded in `manifest.json`. Cleanup status is separate from evaluation execution status.

Cases may declare required workspace-relative `output_files`. The state-recovery case updates `fixtures/research_state.md`; the runner saves it as `artifacts/fixtures/research_state.md` for each side before deleting the temporary workspace. Compare saved content with the original fixture. File existence alone does not establish correct state recovery.

Launch failures, timeouts, nonzero subprocess exits, missing final answers, and missing required outputs produce `execution_ok: false` and a nonzero runner exit. Execution success means outputs are complete; scientific quality still requires scoring.

## Scoring procedure

1. Record the Skill commit, dirty-worktree status, runtime source fingerprint, evaluation alias, Codex version, model, tool configuration, date, and case IDs in `manifest.json`. `skill_source_sha256` covers source `SKILL.md` and every file recursively under `references/`, including relative paths and bytes. It identifies source files before the evaluation alias is applied, not the transformed workspace, fixtures, or runner. The maintenance lock at `evals/mcp-compatibility.json` is not a runtime file.
2. Inspect `events.jsonl` to ensure the final answer does not conceal actual tool calls or failures. For state recovery, also inspect the preserved artifact rather than relying on a claim that it was updated.
3. Score baseline and Skill separately using [rubric.md](rubric.md), recording the supporting output passage or event.
4. Copy `score-template.json` to `scores.json` and enter scores, scorer identity, and notes. Do not retain only verbal conclusions.
5. Mark a Skill case as passed only when every declared check passes.
6. Report case-level outcomes. Do not present a small sample as a percentage improvement on real tasks.

## Current minimum coverage

Four search-decision cases use independent synthetic records in [search-decisions.md](fixtures/search-decisions.md): `cross_source_query_behavior`, `restrictive_query_recall`, `coverage_depth_and_overlap`, and `available_tools_without_mcp`. They examine decisions after interface descriptions and results are supplied. Scoring accepts different sources and operation orders that satisfy the task, without prescribing a database bundle. These cases have not been run against a model. Structural checks do not establish behavioral success or improved real-world recall.

- `missing_full_text`: boundaries between abstracts, full text, and mechanism claims.
- `conflicting_evidence`: conflict classification, underlying study independence, and continued synthesis within confirmed scope.
- `long_task_state_persistence`: state recovery, preservation of unresolved items, and saving a next action tied to a specific evidence gap. Use `--sandbox workspace-write`.
- `untrusted_source_material`: prompt-injection handling. The user prompt does not explain the malicious passage in advance, so it does not substitute for the Skill's own rules.

`smoke-results.md` and `trigger-results.md` are historical smoke records. They provide design context but do not replace raw run records. After cases or rubrics change, old scores apply only to the tested version. New continuation and gap-follow-up requirements need new runs; static checks cannot establish that they pass.

## Privacy and live connector boundary

Public evaluations use neutral synthetic research descriptions, not the maintainer's real research topics, paper lists, local paths, or research state. Webpages, papers, PDFs, metadata, and other source material in evaluations are untrusted data.

`live-mcp-smoke.md` is a historical manual record, not an automated CI task. The next live MCP run requires explicit user authorization and must record actual installation, authentication, restart, and handshake results. Do not fill in results without performing the run. CI performs offline repository and simulated regression checks; it does not launch a model or MCP.
