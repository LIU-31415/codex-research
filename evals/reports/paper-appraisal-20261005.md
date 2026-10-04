# Candidate appraisal and reading depth — 2026-10-05

## Rule change

The existing relevance, original-reading and claim-checking rules were retained and connected to explicit decisions:

- Establish relevance to the intended question using the studied target, relation, outcome and decisive conditions, with provisional fit when necessary details are missing.
- After relevance is established, checked journal/venue and citation context may inform provisional credibility and reading priority. Consider age, field and citation meaning; keep article-level design and support controlling the result-specific judgment.
- Choose screening, original-structure orientation, targeted contextual verification or article-wide appraisal according to the uncertainty and requested scope. A contents scan is orientation; a paragraph hit is not a completed evidence check.
- Locate the result together with its methods, controls, uncertainty, relevant objects and limitations; close the source–claim pairing as supported, limited, contradictory or unresolved. Key evidence requires more than topical fit or accessible full text.

Rules are in [question-specific fit and reliability](../../references/evidence-reasoning.md#assess-fit-to-the-actual-question), [publication/citation context](../../references/evidence-reasoning.md#publication-and-citation-context-after-relevance), and [reading depth and original navigation](../../references/fulltext-reading.md#choose-reading-depth), with entrypoint, search and MCP routing links.

Method inspiration includes [Cochrane's result-specific/domain-based bias appraisal](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-07) and [DORA's limits on journal metrics as article-quality proxies](https://sfdora.org/read/). These sources do not validate the Skill or establish that venue/citation metrics measure correctness. The auxiliary-context use is the user's requested decision rule; no formal RoB/GRADE checklist or universal quality score is claimed.

## Executed case

`paper_appraisal_and_reading_depth` used six fictional candidate records, two linked original-material stand-ins and a supplement. A prominent/highly cited pilot had a simultaneous sampling change and no concurrent control; a newer, less-cited study had a controlled comparison. Other candidates were unrelated, method-only, derivative review and abstract-only records. No live literature, journal metric or current external publication status was checked.

Run `20261005-paper-appraisal` completed in 177.669 seconds, exit 0, with `execution_ok=true`. It used the configured default model and an invocation-only `low` reasoning setting. Host diagnostics named `gpt-6.1-sol` but warned of unknown model metadata/fallback; exact model attribution is limited. No baseline was run, and host plugin guidance was active, so this is not a causal comparison of Skill effectiveness.

The first relative-path reads failed because the shell started outside the staged workspace. The model recovered with the supplied absolute paths, loaded the staged Skill and action references, read both article bodies and followed the supplement link. Later line-numbered reads supported accurate source locators. Large combined reads led to additional targeted guidance/source reads; this does not establish an optimized reading cost. Events show local shell reads and no external research or artifact writes.

## Primary-agent adjudication

The primary agent read the final answer and actual command events, then compared numerical findings, conditions and locators with the source fixtures. All nine declared checks scored 2 under the saved rubric:

| Check | Observed basis |
|---|---|
| SCREENING_TRACEABILITY | Excluded the economic-forecast lexical neighbor; kept method/context, directly relevant findings and the abstract-only pending candidate distinct. |
| CANDIDATE_PRIORITIZATION | Established relevance before venue/citation context; preferred the controlled study without treating its recent low count as invalidity or high counts as endorsement. |
| RESULT_APPRAISAL | Connected the pilot's design defect to unresolved intervention attribution; retained the controlled study's small sample/site boundary and unknown blinding. |
| ORIGINAL_TEXT_USE | Actually read structure, bodies, tables/footnotes and the decisive supplement rather than returning only a reading plan. |
| FACT_CHECKING | Verified MAE 6→4, the controlled difference in changes of −1.0 unit and interval −1.5 to −0.5, and correct units/direction. Locators matched source lines/sections. |
| CHECKPOINT_CLOSURE | Compared distinct pilot abstract assertions with body evidence; retained the attribution/duration overclaim and the compatible controlled-study comparison in the final answer. |
| STUDY_INDEPENDENCE | Distinguished twelve devices from 120 device-days and a derivative review from independent validation. |
| EVIDENCE_BOUNDARY | Preserved fictional/source-excerpt scope, unverified 90-day support and supplied-date status; invented no real access, citation endorsement or reproduction. |
| PROPORTIONATE_COMPLETION | Completed the bounded local task, answered the question with conditions and stopped without new research or a user decision gate. |

Local private run records: [answer](../runs/20261005-paper-appraisal/paper_appraisal_and_reading_depth/skill/final.md), [events](../runs/20261005-paper-appraisal/paper_appraisal_and_reading_depth/skill/events.jsonl), [result](../runs/20261005-paper-appraisal/paper_appraisal_and_reading_depth/skill/result.json), [manual scores](../runs/20261005-paper-appraisal/scores.json), [manifest](../runs/20261005-paper-appraisal/manifest.json). Raw records remain ignored and require privacy review before sharing.

## Validation boundary

Offline regressions, Skill frontmatter and local diff checks passed. The scoped public-content check passed with the unchanged local audit report excluded; the full check remains blocked by that pre-existing report's private path. Runtime synchronization preserves installed extras and checks the thirteen runtime files against source hashes.

This is one supplied-material behavior check with primary-agent manual scoring, not blind independent review, real-paper appraisal accuracy, visual/PDF parsing, broad retrieval precision/recall or experimental reproduction. The existing venue-only case's expected outcome was aligned afterward and was not separately rerun. Prior real-paper failures remain in their original reports; this run does not supersede them or establish general reliability.
