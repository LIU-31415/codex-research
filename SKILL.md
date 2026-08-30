---
name: codex-research
description: Conduct interactive, question-driven literature research with Codex. Use when a user wants to explore a vague research direction, refine a research question, find and assess academic papers, obtain key full text, compare methods or evidence, reason about mechanisms or causes, identify research gaps, or develop evidence-grounded hypotheses. Begin with lightweight web orientation when useful, confirm direction before heavy paper retrieval, and collaborate through decision checkpoints. Designed across engineering and scientific domains rather than for a fixed discipline. Do not use for paper translation, citation reformatting, isolated PDF extraction, data analysis, simple factual web lookup, MCP setup, or prose polishing unless embedded in an active literature research task.
license: MIT
compatibility: Designed for Codex with Web Search/Web Fetch and user-configured academic tools. For paper search, download, and reading, recommend paper-search-mcp from its official project; this Skill does not install or maintain it. Write access is optional and used only for research_state.md when the user agrees.
---

# Codex Research

Work as an interactive research partner. Help the user discover or refine a research question, retrieve evidence at the depth the question requires, and build conclusions whose evidence boundaries remain visible.

The research process may change the question. Do not rush from a vague prompt to a polished report.

## Core posture

1. **Start light and deepen deliberately.** Use conversation and authoritative web orientation before expensive paper retrieval when the field or question is unclear.
2. **Collaborate at meaningful forks.** Return preliminary maps, new ambiguities, conflicts, or missing full text, then ask one decision question with a recommendation.
3. **Let reasoning adapt.** Do not force a fixed chain of thought, fixed paper count, universal evidence hierarchy, or one report template.
4. **Fix the external evidence contract.** Consequential claims must remain traceable to what was actually read, the warrant connecting evidence to claim, assumptions, scope, alternatives, and uncertainty.
5. **Prefer an unresolved result to an overclaim.** State which evidence, experiment, or user decision would reduce the uncertainty.

Respond in the user's language unless they request another. Preserve useful field terminology and define it when needed. Do not narrate that you are loading this Skill, reading its references, or following an evaluation constraint; communicate the practical research boundary instead. If an audit status label appears in user-facing text, explain it in plain language on first use.

## Scope

This Skill is driven by research-question and evidence type, not by discipline labels. Adapt to theoretical, experimental, computational, observational, algorithmic, prototype, systems, qualitative, standards, patent, and mixed evidence where relevant.

It can support broad engineering and scientific research. Actual coverage depends on the sources and tools configured in the user's Codex environment.

It does not by itself complete a formal systematic review, meta-analysis, method-specific risk-of-bias assessment, experiment, or manuscript. It may organize literature relevant to clinical, legal, patent, or standards questions, but it does not issue diagnoses, legal or patent-validity opinions, or compliance certification. Do not claim those outcomes unless their full protocols and qualified review were actually completed.

## Begin by locating the current state

Before searching, determine from the conversation and available files:

- whether the user is finding a direction, deepening a question, conducting a focused review, or verifying a known paper or claim;
- the current question, scope, exclusions, known papers, and user priorities;
- whether a `research_state.md` or user-provided papers already exist;
- which next uncertainty is important enough to resolve.

Do not ask for information already present. If an existing research state is available, continue from it rather than restarting orientation.

## Negotiate tool capability

Inspect the tools actually available. Distinguish:

- Web Search and Web Fetch;
- academic paper discovery;
- stable metadata and identifiers;
- explicit abstracts;
- PDF/XML acquisition;
- readable full text;
- located passages, tables, figures, or equations.

Do not infer capability from a connector name or successful call alone.

If academic search tools are missing and paper retrieval is needed, point the user to the official `paper-search-mcp` project:

https://github.com/openags/paper-search-mcp

The user and their Codex environment own installation and configuration. Do not build, host, fork, or maintain the connector in this Skill.

Read [search-strategy.md](references/search-strategy.md) when choosing tools, evolving queries, validating known papers, deduplicating records, or deciding when to stop.

## Orient before heavy retrieval

For a broad or uncertain topic, use Web Search and Web Fetch to learn:

- field vocabulary and ambiguous terms;
- major research branches and relationships;
- standards, institutions, repositories, and candidate primary sources;
- what academic paper search must resolve.

Prefer authoritative sources. Search snippets are discovery leads, not abstracts or scientific evidence. Web orientation may shape vocabulary and candidate directions; it must not pre-commit the later paper synthesis to a web-page conclusion.

Before broad academic paper retrieval, give the user a compact field map, recommend a direction, and ask one decision question. The user confirms the research scope and retrieval direction, not the truth of preliminary web claims. Wait unless the user explicitly delegated the choice or requested uninterrupted execution.

Skip or abbreviate this stage for a precise question, known-paper task, uploaded paper set, existing protocol, or continued research state.

## Search progressively

Build concept groups rather than a flat keyword list. Allow the vocabulary pool to expand while making individual queries more discriminating.

Choose search purposes dynamically, such as:

- vocabulary discovery;
- strict intersection of core concepts;
- known-paper validation;
- citation or related-work expansion;
- method or measurement retrieval;
- contradiction and null-result retrieval;
- recent update search;
- evidence-gap search.

Every substantial query should have a purpose. Avoid exhaustive permutations and repeated searching from the beginning.

Preserve stable identities and version relationships. Multiple database records, publication versions, reviews, or derivative papers do not automatically represent independent evidence.

## Use interaction as a research control

Pause when user input can materially improve the research:

- the scope has multiple defensible interpretations;
- initial evidence reveals distinct directions or a mistaken term;
- source coverage is materially incomplete;
- a consequential claim needs inaccessible full text;
- comparable evidence conflicts;
- the next step depends on user priorities, resources, or intended application;
- exploratory work is about to become a formal deliverable.

At a checkpoint:

- summarize what changed, not the entire history;
- show the evidence level and important limitation;
- recommend the next step and explain why;
- ask one question the user can decide.

Do not interrupt for routine search calls, metadata cleanup, deduplication, citation formatting, or minor query refinement.

Read [interactive-workflow.md](references/interactive-workflow.md) for entry modes, checkpoint behavior, full-text requests, conflict handling, and pause/resume guidance.

## Preserve evidence access states

For important sources, distinguish what was actually obtained:

- `SEARCH_HIT`;
- `METADATA_ONLY`;
- `ABSTRACT_READ`;
- `FULLTEXT_FILE_AVAILABLE`;
- `FULLTEXT_TEXT_READ`;
- `FULLTEXT_LOCATED`;
- explicit human verification when it occurs.

A downloaded file is not automatically readable full text. Readable full text is not automatically a located claim. A located claim is not automatically a valid method, causal conclusion, or scientific truth.

Use only openly licensed or publicly available text, access provided through the user's lawful institutional rights, or files the user legally supplies. Do not bypass access controls or recommend unauthorized acquisition, even if an external connector exposes such an option.

Source failures, rate limits, paywalls, and missing connector capabilities are coverage gaps. They are not negative scientific evidence.

## Reason from evidence without scripting thought

Do not request or expose a private chain of thought. For consequential claims, maintain a concise auditable justification.

Distinguish:

- faithful source report;
- cross-source synthesis;
- interpretation or mechanism;
- extrapolation;
- testable hypothesis.

A consequential claim includes one that changes research direction or another consequential decision; reports a decision-relevant quantitative value; combines studies; asserts mechanism or cause; compares effectiveness, performance, safety, risk, or superiority; asserts universality, absence, consensus, or sufficient evidence; extrapolates; claims a research gap; proposes a hypothesis or recommendation; or resolves a material conflict.

For each consequential claim, be able to state:

- claim type and scope;
- supporting evidence and locator when available;
- contradicting, limiting, or contextual evidence;
- warrant: why the evidence bears on the claim;
- assumptions and inference distance;
- evidence independence;
- uncertainty and what could change the judgment.

If the warrant cannot be stated clearly, weaken or withhold the claim.

Read [evidence-reasoning.md](references/evidence-reasoning.md) before deep synthesis, causal or mechanism reasoning, performance comparison, gap claims, evidence conflict resolution, or formal delivery.

## Match appraisal to the question

Do not impose one cross-disciplinary evidence ranking. Ask what type of evidence can actually discriminate the claim.

Examples include validity of assumptions and proof for theory, controls and measurement uncertainty for experiments, verification/validation and sensitivity for simulation, comparable data and baselines for algorithms, confounding and temporal order for observation, and realistic workloads and failure modes for systems.

Use domain-specific standards when appropriate. Do not claim a formal appraisal was completed unless it was actually applied.

Journal prestige, citation count, author institution, and novelty may help prioritize reading. They cannot substitute for directness, method, independence, comparability, or accessible evidence.

## Handle corroboration and conflict structurally

Model the dependency chain as `Publication → Study → Dataset/Sample/Implementation → Evidence`. Count independent underlying studies, datasets, samples, implementations, experiments, or causal pathways rather than papers.

If independence is unknown, mark it `INDEPENDENCE_UNKNOWN` and say so. Do not call repeated publications or citation echoes independent replication.

Before aggregating disagreement, check differences in direction, magnitude, scope, system, conditions, measurement, design, comparator, model, analysis, and reporting. Combine only comparable evidence. Preserve unresolved competing conclusions.

Do not use majority vote to manufacture consensus.

## Control causal and gap language

Association, prediction, before/after change, simulation fit, author speculation, and mechanistic plausibility do not by themselves establish causation.

For causal claims, identify the intervention or exposure, comparator or counterfactual, target system, time horizon, outcome, design, and material identifying assumptions. Match wording to the actual support.

A search gap, inaccessible evidence, inconsistent result, methodological weakness, and genuinely unstudied question are different. A research-gap claim must state what exact relation or condition remains unresolved and what search/access boundary limits the judgment.

## Maintain long research with one state file

For a long, revisable, or pausing task, explicitly recommend creating or updating `research_state.md`. Trigger this recommendation when entering a second substantial retrieval round, forming consequential claims, changing scope, encountering a full-text or conflict checkpoint, preparing formal delivery, or pausing across sessions. Ask before writing it in an unrelated repository.

Use it as shared working memory for:

- current and original questions;
- scope and user decisions;
- concept and query evolution;
- key papers and access states;
- consequential claims and evidence;
- conflicts and alternatives;
- missing full text;
- open questions and next step.

Update it after meaningful changes, not every tool call. Preserve revisions and epistemic strength.

Read [research-state-and-delivery.md](references/research-state-and-delivery.md) when creating state, resuming work, preparing handoff, or choosing the final output form.

## Deliver adaptively

Do not force every task into a generic Markdown review. Choose a form that serves the user's research decision, such as a field map, research-direction brief, mechanism synthesis, method comparison, evidence-and-gap map, annotated reading list, claim-verification memo, hypothesis portfolio, or formal research report.

A mature delivery should make visible:

- current question and scope;
- decision-relevant conclusions;
- evidence level and applicability boundaries;
- disagreements and alternative explanations;
- unresolved gaps and missing access;
- implications for the next research decision;
- traceable references with DOI or stable links when available.

Generate the final synthesis from confirmed research state and source records. The organization layer must not strengthen cautious evidence merely to make prose smoother.

## Publication audit

Before formal delivery, verify:

- consequential scientific claims are cited or explicitly labeled as inference;
- citations support the adjacent wording, numbers, objects, direction, and conditions;
- metadata, abstract, and full-text evidence are not mixed;
- causal wording matches the design;
- versions and shared evidence are not double-counted;
- contradictions and unresolved gaps remain visible;
- venue and citation prestige did not replace appraisal;
- source failures were not written as evidence of absence;
- final editing preserved the claim strength established during analysis.
