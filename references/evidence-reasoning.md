# Evidence and Reasoning

## Core contract

Let Codex reason adaptively. Constrain the observable justification of consequential claims.

Do not ask Codex to reveal a private chain of thought or to follow a fixed sequence of mental steps. Require a concise, auditable account of:

- what evidence was observed;
- why it bears on the claim;
- what assumptions connect evidence to claim;
- how far the inference extends;
- where the claim may fail;
- what contradictory or alternative evidence remains.

## Consequential claims

Apply the full claim contract when a statement:

- changes the research direction or another consequential decision;
- reports a decision-relevant quantitative value;
- synthesizes multiple studies;
- asserts a mechanism or causal relation;
- compares effectiveness, performance, safety, risk, or superiority;
- asserts universality, absence, consensus, or sufficient evidence;
- extrapolates beyond studied conditions;
- claims a research gap;
- proposes a research hypothesis or recommendation;
- resolves or suppresses a material conflict.

Ordinary definitions, bibliographic facts, and low-stakes background can remain lighter, with appropriate sources.

## Preserve evidence boundaries

Use one ordered access-state vocabulary:

- `SEARCH_HIT`: discovery lead or snippet only;
- `METADATA_ONLY`: paper identity and bibliographic facts were obtained;
- `ABSTRACT_READ`: an explicit abstract was opened and read;
- `FULLTEXT_FILE_AVAILABLE`: an accessible asset passed the paper-identity gate;
- `FULLTEXT_TEXT_READ`: verified article body text was parsed or read;
- `FULLTEXT_LOCATED`: a supporting passage, table, figure, equation, or section was located in the verified full text.

A discovered or downloaded asset remains a candidate asset until its title, authors, stable identifier, and publication-version relationship are checked against the target paper. Do not promote it to any `FULLTEXT_*` state before that identity gate passes.

Record `HUMAN_VERIFIED` as an orthogonal verification flag when the user or researcher explicitly checks a relevant source detail. It does not replace or automatically upgrade the access state.

Full-text access does not imply validation of methods, figures, statistics, retraction status, or scientific truth.

## Publication status

Before relying on a paper for a consequential conclusion, inspect the publisher's current article page and any linked correction, retraction, withdrawal, or expression-of-concern notice. Record the status, source link, check date, and effect on the specific claim separately from the access state. Before formal delivery, resolve missing status checks and refresh them when a new notice or elapsed research interval could change the judgment; do not repeat an unchanged check within a short session.

Use corrected findings where a correction affects the claim. Do not use a retracted or withdrawn finding as affirmative support; retain it only when needed to explain the research history or the notice itself. An expression of concern requires stating the affected uncertainty and seeking independent support. If status cannot be checked, record it as unknown rather than assuming the paper is unaffected.

## Claim types

### Source report

Faithfully describes what one source reports without strengthening its scope or causal language.

Preferred language:

> The study reports...
> The abstract states...
> Under the tested conditions...

### Synthesis

Combines comparable evidence to identify a pattern. State the scope, evidence types, comparability, independence, and important heterogeneity.

### Interpretation

Explains why a pattern may occur. Separate compatibility with a mechanism from evidence that discriminates that mechanism from alternatives.

### Extrapolation

Transfers evidence to a different population, material, scale, setting, operating condition, metric, or time. Name the changed dimension and the assumption required.

### Hypothesis

A plausible, testable proposition not adequately established by current evidence. State what would support, distinguish, or falsify it.

Never present an interpretation, extrapolation, or hypothesis as a direct finding.

## Minimal evidence and claim contracts

An important evidence record should preserve, when available:

```text
Evidence ID
Paper ID or stable identifier
Publication version and underlying study relationship
Evidence access level
Verbatim excerpt or faithful data observation
Locator: section, page, paragraph, table, figure, equation, or data row
Target object, population, system, or material
Conditions, comparator, measurement, and time boundary
Result, direction, and units when relevant
Relation: SUPPORTS | CONTRADICTS | LIMITS | CONTEXT
Source URL and access date
Paper identity status
```

For each consequential claim, maintain enough information to answer:

```text
Claim ID and claim text
Type: report | synthesis | interpretation | extrapolation | hypothesis
Scope and boundary conditions
Supporting Evidence IDs and precise locator when available
Contradicting, limiting, or contextual Evidence IDs
Warrant: why the evidence supports the claim
Assumptions and inference distance
Evidence independence
Uncertainty and confidence rationale
What evidence would change the judgment
```

This may remain in working state and be summarized naturally for the user. Expand it when the user requests an audit or when the claim carries high research consequence.

## Warrant and inference distance

The warrant is the bridge between evidence and claim. If it cannot be stated clearly, weaken or withhold the claim.

Use qualitative inference distance:

- `NONE`: faithful source report;
- `SHORT`: direct comparison or tightly scoped synthesis;
- `MODERATE`: interpretation requiring explicit assumptions;
- `LONG`: extrapolation, causal attribution from indirect evidence, or a new hypothesis.

A long inference is not automatically invalid. It carries a higher burden to expose assumptions and alternatives.

## Match evidence to the research question

Adapt appraisal to the claim rather than applying one cross-disciplinary hierarchy.

Examples:

- theoretical claims require valid assumptions, definitions, and derivation or proof;
- experimental performance claims require suitable controls, measurements, uncertainty, and operating conditions;
- simulation claims require model assumptions, calibration, verification, validation, and sensitivity where relevant;
- algorithmic comparisons require comparable datasets, baselines, metrics, leakage controls, and reproducibility details;
- observational claims require attention to selection, confounding, measurement, and temporal order;
- prototype and systems claims require realistic workloads, interfaces, failure modes, and transfer to deployment conditions;
- qualitative or case-based claims require transparent sampling, interpretation, context, and rival accounts.

Use domain-specific appraisal standards when available, but do not pretend to have completed a formal checklist unless it was actually applied.

## Independence and corroboration

Use the dependency chain `Publication → Study → Dataset/Sample/Implementation → Evidence`. Count support by underlying studies, datasets, samples, implementations, experiments, or independent causal pathways, not by publication count.

Check when feasible:

- shared datasets, samples, cohorts, specimens, or code;
- preprint, conference, journal, correction, and repository versions;
- overlapping authors, laboratories, institutions, or funders;
- repeated use of the same model, benchmark, measurement method, or source data;
- reviews that echo the same primary evidence;
- citations that ultimately trace to one original result.

If independence is unknown, mark it `INDEPENDENCE_UNKNOWN` and say so. Multiple publications with unknown dependence provide apparent corroboration, not confirmed independent replication.

## Evidence quality dimensions

Assess only the dimensions relevant to the claim. Common dimensions include:

- identity and provenance;
- directness to the research question;
- methodological adequacy;
- completeness of accessible reporting;
- independence;
- consistency and heterogeneity;
- precision and measurement uncertainty;
- applicability and transferability;
- risk of bias or selective reporting;
- model and mechanism dependence;
- vulnerability to plausible alternatives.

Do not collapse these into an unsupported universal score. Confidence labels require reasons.

## Conflict handling

Before aggregating disagreement, classify it:

- direction;
- magnitude;
- scope or boundary conditions;
- population, system, material, or setting;
- measurement or outcome definition;
- design or comparator;
- model, analysis, or adjustment;
- publication version or reporting layer.

Then decide whether the evidence should be combined, stratified, explained as heterogeneity, retained as competing conclusions, or left unresolved.

Do not use majority vote. Do not remove a material contradiction to make prose smoother.

## Causal and mechanism claims

Association, prediction, temporal change, simulation fit, author speculation, and mechanistic plausibility do not by themselves establish causation.

For a causal claim, identify as applicable:

- intervention or exposure;
- comparator or counterfactual;
- target system or population;
- temporal order and horizon;
- outcome;
- design and identifying assumptions;
- confounding, selection, measurement, and alternative paths.

Match wording to the actual design. Prefer “associated with,” “consistent with,” or “the authors propose” when causal support is incomplete.

For mechanism claims, ask what observations discriminate the proposed mechanism from alternatives. A mechanism compatible with results remains an interpretation until discriminating evidence exists.

## Uncertainty

Treat uncertainty as part of the conclusion. Identify material sources such as:

- bias or design limitations;
- imprecision or measurement uncertainty;
- inconsistency;
- indirectness;
- selective reporting and publication bias;
- missing full text or inaccessible details;
- model dependence;
- unknown evidence independence;
- extrapolation.

Avoid invented numerical probabilities. Use calibrated qualitative language tied to explicit reasons.

## Research gaps

A search gap, reporting gap, methodological weakness, inconsistent result, and genuinely unstudied question are different.

A defensible research-gap claim should state:

- what was searched and accessed;
- what evidence exists nearby;
- what exact relation, condition, comparison, or validation remains unresolved;
- whether the gap reflects absence, insufficient quality, conflicting evidence, or inaccessible information;
- what study could reduce it.

## Publication audit

Before presenting a formal synthesis, verify:

- every consequential scientific claim has a traceable source or is labeled as inference;
- citations support the adjacent claim, including numbers, direction, objects, and conditions;
- metadata, abstract, and full-text evidence are not mixed;
- causal language matches the design;
- versions and shared evidence are not double-counted;
- contradictions and unresolved gaps remain visible;
- venue prestige and citation count did not substitute for appraisal;
- source or access failures were not written as evidence of absence;
- the organization and wording did not strengthen the epistemic status established during analysis.

A clear unresolved answer is preferable to a fluent overclaim.

## Method inspirations

These principles draw on, without mechanically reproducing:

- OpenAI reasoning prompting guidance: https://developers.openai.com/api/docs/guides/reasoning-best-practices
- Toulmin argument structure: https://owl.purdue.edu/owl/general_writing/academic_writing/historical_perspectives_on_argumentation/toulmin_argument.html
- Cochrane/GRADE evidence certainty: https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-14
- Cochrane interpretation and conclusions: https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-15
- National Academies causal inference overview: https://www.ncbi.nlm.nih.gov/books/NBK588337/
- National Academies reproducibility and replicability: https://www.nationalacademies.org/read/25303/chapter/3
