# Smoke A/B Results

> Historical record from the initial design review. Run new paired cases with [`evals/README.md`](README.md) and `run_eval.py`; the 3/3 result below is not a reproducible benchmark.

Date: 2026-08-30

Status: **exploratory internal smoke test**, not a reproducible benchmark.

## Method

Three representative first-response tasks were run twice in parallel:

- with `codex-research` loaded;
- baseline without reading any local Skill.

A blind reviewer received candidates as A/B with order swapped for two cases. The reviewer compared stage control, evidence/access boundaries, overclaiming, recommendation quality, and whether the response asked only one decision-changing question. External web and paper search were disabled so the test focused on interaction and evidence discipline rather than retrieval quality.

The raw candidate transcripts, fixed model identifiers, and complete runtime configuration are not committed, so the result cannot be independently reproduced from this repository alone.

## Results

| Case | Winner | Main reason |
|---|---|---|
| Ambiguous direction | With Skill | Preserved the direction-finding stage, exposed evidence limits, recommended a path, and asked one decision-changing question |
| Missing full text | With Skill | Separated abstract-level reporting from mechanism and causal claims requiring full text; produced an actionable full-text gate |
| Conflicting evidence | With Skill | Refused premature synthesis, classified potential disagreement sources, preserved uncertainty, and asked one scope-changing question |

Overall: **3/3 blind comparisons favored the Skill response.**

## Defects exposed

1. The conflict response did not explicitly mention shared datasets, repeated publications, or study independence in its first turn.
2. Two responses narrated internal Skill/evaluation context; production responses should communicate the evidence boundary without exposing internal process.
3. Audit labels such as `ABSTRACT_READ` should be explained in plain language the first time they appear to a user.
4. The direction-finding test did not execute actual Web orientation because the smoke harness disabled external tools; this test does not evaluate retrieval quality.

## Changes made

- Strengthened the conflict checkpoint to check publication and underlying-study dependence before weighing disagreement.
- Added a user-facing communication rule against narrating Skill loading or evaluation constraints.
- Required plain-language explanation when an audit status label is surfaced.

## Remaining evaluation needs

- Live Web orientation and direction checkpoint;
- MCP capability negotiation;
- actual metadata/abstract/full-text state detection;
- citation-to-claim verification;
- long-session `research_state.md` recovery;
- trigger precision against near-miss tasks.
