# codex-research

`codex-research` is a lightweight, interactive literature-research Skill for Codex. It helps a user move from a vague research interest to a clearer question, progressively retrieve academic evidence, inspect key full text, reason across studies, and preserve a traceable evidence boundary.

It is driven by the research question and evidence type rather than a fixed discipline. It is intended to work across engineering and scientific research, subject to the sources available in the user's Codex environment.

## What makes it different

- Starts with lightweight Web Search / Web Fetch orientation when the field is unclear.
- Confirms direction before broad academic retrieval.
- Returns preliminary findings and asks one meaningful decision question at a time.
- Escalates from discovery to metadata, abstracts, and located full-text evidence.
- Requests user-supplied PDFs only when they can change an important conclusion.
- Keeps internal reasoning adaptive while requiring an auditable evidence contract for consequential claims.
- Distinguishes source reports, synthesis, interpretation, extrapolation, and hypotheses.
- Can maintain one `research_state.md` for long or resumable work.
- Produces an output suited to the research decision instead of forcing a generic review template.

## Installation

Copy or install the `codex-research` folder into a Codex Skill location, for example:

```text
$HOME/.agents/skills/codex-research/
```

The folder name must remain `codex-research` so it matches the `name` in `SKILL.md`.

Restart Codex if the Skill does not appear immediately. Invoke it explicitly with:

```text
$codex-research
```

Codex may also invoke it automatically when the user's request matches its description.

## Academic search dependency

The Skill does not bundle or maintain an academic connector. Users who want multi-source paper search, download, and reading should configure the upstream project in their own Codex environment:

- [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp)

Follow that project's current official installation and configuration instructions. Source capabilities differ: some provide metadata or abstracts, while others may provide open full text. The Skill checks what was actually retrieved instead of assuming that a configured connector guarantees full-text evidence.

Web orientation can still proceed when Codex exposes Web Search and Web Fetch but no academic connector is configured.

## Example prompts

```text
$codex-research I am interested in structural batteries but do not yet know which research question is worth pursuing. Explore the field with me and stop before the heavy paper search so we can choose a direction.
```

```text
$codex-research Compare physics-informed and purely data-driven approaches for remaining-useful-life prediction. Help me refine the comparison and build an evidence-grounded judgment rather than immediately writing a report.
```

```text
$codex-research These papers disagree about the dominant degradation mechanism. Check whether the conflict comes from conditions, measurement, or genuinely competing explanations. Ask me for important missing PDFs when needed.
```

```text
$codex-research Resume from research_state.md and continue with the unresolved full-text and mechanism questions.
```

## Skill structure

```text
codex-research/
├─ SKILL.md
└─ references/
   ├─ interactive-workflow.md
   ├─ search-strategy.md
   ├─ evidence-reasoning.md
   └─ research-state-and-delivery.md
```

- `SKILL.md`: routing and core behavior.
- `interactive-workflow.md`: collaboration checkpoints and interaction policy.
- `search-strategy.md`: progressive search and query evolution.
- `evidence-reasoning.md`: evidence boundaries and consequential-claim contract.
- `research-state-and-delivery.md`: resumable state and adaptive outputs.

## Boundaries

The Skill does not:

- install or operate an MCP service;
- build source adapters, databases, or download infrastructure;
- bypass paywalls;
- guarantee exhaustive literature coverage;
- treat journal prestige or citation count as evidence quality;
- automatically turn abstracts into full-text confirmation;
- treat repeated publications as independent studies;
- upgrade association or plausibility into causation;
- claim completion of a formal systematic review without its full protocol;
- replace experiments, domain experts, or human verification of consequential details.

## License

MIT
