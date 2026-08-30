# Interactive Research Workflow

## Purpose

Treat literature research as a collaboration that can change the question, not as a one-shot report generator. Move only as deep as the current decision requires. Pause when new evidence creates a meaningful branch, risk, or need for user input.

The stages below are states that Codex may revisit. They are not a mandatory sequence for every task.

## Entry modes

Infer the entry mode from the conversation. Ask only when the distinction changes the next action.

### Direction finding

Use when the user has a broad interest, an observation, a material or system, but no stable research question.

Goal:

- discover the field's language and major branches;
- expose assumptions and adjacent directions;
- help the user formulate candidate questions.

### Question deepening

Use when the user has a question but its scope, variables, comparison, or intended conclusion remains unclear.

Goal:

- make the question answerable;
- identify the evidence dimensions required;
- distinguish background, mechanism, performance, method, risk, and gap questions.

### Focused evidence review

Use when the user already has a precise question, known papers, a protocol, or explicit inclusion boundaries.

Goal:

- verify identities and coverage;
- retrieve the most decision-relevant evidence;
- synthesize within the confirmed scope.

### Known-paper or claim verification

Use when the user provides a DOI, title, PDF, or scientific claim.

Goal:

- verify the paper or claim first;
- avoid restarting broad discovery unless verification exposes a larger gap.

## Lightweight orientation

For broad or uncertain topics, begin with Codex Web Search and Web Fetch when available. Use authoritative pages to learn terminology, subfields, institutions, standards, and candidate primary sources.

Do not treat search snippets or general web pages as empirical paper evidence. Trace consequential scientific claims to primary literature before relying on them in synthesis.

Skip or abbreviate orientation when the user supplies a precise research question, a mature query strategy, or asks to continue an existing review.

## Direction checkpoint before heavy paper search

Before broad academic retrieval, return a compact field map:

- current interpretation of the user's goal;
- important terms or ambiguities discovered;
- plausible research branches;
- what paper search would resolve;
- a recommended direction;
- one decision question.

Wait for the user's answer unless the user explicitly delegated the choice or requested uninterrupted execution.

## Risk-triggered checkpoints

Use these state names in working notes when useful. They describe decision conditions, not a mandatory sequence:

- `SCOPE_UNCLEAR`
- `MCP_CAPABILITY_INSUFFICIENT`
- `DIRECTION_CONFIRMATION_REQUIRED`
- `COVERAGE_GAP`
- `FULLTEXT_REQUIRED`
- `CONFLICT_REQUIRES_DECISION`
- `READY_TO_DELIVER`

For each triggered checkpoint, state the trigger, Codex's recommendation, the user's meaningful options, and the safe degraded path if the user defers. Simple, precise, or explicitly delegated tasks may skip checkpoints that cannot change the outcome.

### Scope checkpoint

Trigger when the question has multiple reasonable populations, systems, settings, outcomes, comparisons, time ranges, or evidence standards.

Present the consequence of each option and recommend one. Ask one question.

### Coverage checkpoint

Trigger when a major source, date range, language, discipline, or publication type remains uncovered, or when source failures materially limit the map.

State what was covered, what was not, and whether the gap could change the conclusion.

### Direction checkpoint

Trigger when initial results reveal distinct research branches, a mistaken term, an overlooked variable, or a more promising question.

Do not silently redirect the research. Explain what changed and ask the user whether to revise the direction.

### Full-text checkpoint

Trigger when a consequential conclusion requires methods, conditions, numbers, figures, tables, limitations, or mechanism details unavailable from the abstract.

List only the papers worth the user's effort. For each, explain:

- stable identifier and link;
- why it is decision-relevant;
- what cannot be verified without the full text;
- whether an accessible substitute exists.

Offer to continue at abstract level with an explicit limitation, wait for a user-provided PDF, or pursue an alternative source. If the user does not decide, preserve the claim as unresolved and do not silently upgrade it.

### Conflict checkpoint

Trigger when comparable studies materially disagree or when competing explanations remain plausible.

Before weighing the disagreement, check whether the publications represent independent studies or reuse the same dataset, sample, project, implementation, or policy intervention. Then classify the conflict by scope, conditions, measurement, design, analysis, or reporting. Offer choices such as further retrieval, narrowing the scope, or retaining parallel conclusions.

### Delivery checkpoint

Trigger before turning exploratory work into a formal report, proposal input, or decision document.

Confirm the intended evidence standard and the unresolved items that must remain visible.

## Progress updates

A checkpoint update should be concise and decision-oriented. Do not narrate Skill loading or internal evaluation instructions. Adapt the headings rather than forcing a template. It normally contains:

- what is currently understood;
- what changed in this round;
- evidence level and important limitations;
- Codex's recommended next step;
- one question the user can actually decide.

Do not repeat the entire history at every checkpoint. Show the delta.

## Asking well

- Ask one decision at a time.
- Propose a recommended answer and briefly explain why.
- Avoid asking for information that tools or existing files can provide.
- Avoid turning the session into an intake questionnaire.
- Preserve the user's terminology while introducing more precise field terms.
- When the user is uncertain, offer concrete alternatives grounded in preliminary findings.
- When the user delegates, make the decision and report it at the next meaningful checkpoint.

## When not to interrupt

Do not pause for routine searches, metadata normalization, deduplication, citation formatting, or minor query refinements. Continue when the next action is reversible and unlikely to change the research direction.

## Ending or pausing

Before a long pause, context reset, or handoff, recommend creating or updating `research_state.md` as described in [research-state-and-delivery.md](research-state-and-delivery.md).

A task can end with an unresolved result. State the most informative next evidence or experiment instead of manufacturing closure.
