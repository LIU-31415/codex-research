# Trigger Routing Smoke Result

Date: 2026-08-30

## Setup

A routing evaluator read only the current `SKILL.md` frontmatter name and description, then classified the 20 queries in `trigger-evals.json`.

The set contains:

- 10 positive literature-research tasks;
- 10 near-miss negative tasks covering translation, factual web lookup, citation formatting, data analysis, ungrounded paper writing, MCP troubleshooting, bibliography conversion, PDF table extraction, and prose polishing.

## Result

- Passed: **20/20**
- False positives: **0**
- False negatives: **0**

The explicit exclusion list in the Skill description cleanly separated the negative cases, while the positive cases invoked at least one core behavior: direction exploration, evidence comparison, mechanism reasoning, research-gap identification, full-text verification, or continuation of an active literature-research task.

## Interpretation limit

This is a single-pass model simulation, not a measurement of the production Codex router. The test set emphasizes clearly labeled positives and near-miss exclusions. Future boundary tests should include ambiguous middle cases such as a simple concept-definition search, a request to summarize one paper, a bare request for several references, and a single-paper question that may or may not expand into evidence synthesis.
