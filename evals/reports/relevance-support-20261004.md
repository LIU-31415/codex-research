# Relevance and claim-support verification — 2026-10-04

## Change and scope

The runtime now distinguishes topical fit from support for a particular claim. Noisy batches require diagnosis of source/query behavior before bulk reading; unified search explicitly selects sources. Context, method references, transferred evidence, contrary results and candidates awaiting original reading retain separate roles. Consequential paraphrases are checked for entity, metric, quantity, condition, duration and causal changes. No fixed paper count or universal database recipe was introduced.

## Sequential supplied-material behavior runs

Both runs requested `gpt-6.1-sol`, used the configured reasoning setting, staged the same runtime text, and ran Skill-only with external retrieval prohibited by the task. The primary agent inspected saved final answers and actual tool events, then scored every declared check against the frozen rubric. No baseline was executed. Standalone user Skills were disabled by the existing runner; host plugin guidance remained available, so these runs do not isolate the Skill's causal contribution.

| Case | Observed result | Scoring and evidence |
|---|---|---|
| `relevance_screening_and_noise` | Excluded economic-model lexical overlap; retained the method reference, finite field result and contrary deployment; kept abstract-only long-term support pending; did not use battery-life results as accuracy evidence. Identified category/free-text mismatch, source-order bias and unknown zero-result execution. | All 7 declared checks scored 2. [Answer](../runs/20261004-relevance-screening/relevance_screening_and_noise/skill/final.md), [events](../runs/20261004-relevance-screening/relevance_screening_and_noise/skill/events.jsonl), [scores](../runs/20261004-relevance-screening/scores.json), [manifest](../runs/20261004-relevance-screening/manifest.json). |
| `claim_support_and_fidelity` | Preserved mean MAE reduction of 30% without turning it into accuracy increase; corrected independent devices, laboratory duration, the worsening device and causal wording; rejected the hedged field-effect attribution. | All 7 declared checks scored 2. [Answer](../runs/20261004-claim-support/claim_support_and_fidelity/skill/final.md), [events](../runs/20261004-claim-support/claim_support_and_fidelity/skill/events.jsonl), [scores](../runs/20261004-claim-support/scores.json), [manifest](../runs/20261004-claim-support/manifest.json). |

The saved runs are local, ignored artifacts and require review before sharing. These are synthetic original-excerpt and screening exercises, not evidence of actual pagination, broad recall or production accuracy.

## Live connector and original-source sample

Separately, the primary agent called `paper-search-mcp.search_papers` with query `"far-UVC" "airborne human coronaviruses"`, `sources="pubmed"`, and `max_results_per_source=3`. The response returned 3 records with no reported errors. The [local call and disposition record](../.runtime/20261004-relevance-live-sample.json) preserves parameters, candidate identities and checked scope. This was a direct primary-agent verification, not an autonomous live evaluation subprocess.

| Returned candidate | Actual use in this verification |
|---|---|
| PMID 32581288, DOI `10.1038/s41598-020-67211-2` | Read the publisher's original Methods, infectivity Results, Figure 1 caption and Discussion for the selected claims. |
| PMID 35458414, DOI `10.3390/v14040684` | Relevant HCoV-OC43 candidate based on the returned abstract; original body and study independence were not verified. |
| PMID 35322064, DOI `10.1038/s41598-022-08462-z` | The returned abstract identifies aerosolized *Staphylococcus aureus* as the tested organism. Retained as a room-scale context/transfer candidate, not direct measured coronavirus evidence; original body was not read. |

For the first paper, the supported observation is reduced infectivity of the two tested aerosolized coronavirus strains, HCoV-229E and HCoV-OC43, under the reported laboratory conditions. The selected locators are Methods → Viral strains / Benchtop aerosol irradiation chamber, Results → infectivity assay, and Discussion. The paper's proposed SARS-CoV-2 applicability is an extrapolation, not a direct SARS-CoV-2 experiment; references to separate safety work do not establish unconditional human safety. [Original article](https://www.nature.com/articles/s41598-020-67211-2).

The publisher's 2021 correction changes the competing-interest disclosure, rather than the checked organism/method/result claims. [Correction](https://www.nature.com/articles/s41598-021-97508-9). No current exposure recommendation or general safety assessment was attempted.

This sample demonstrates why theme overlap cannot determine a paper's evidence role. It does not estimate search precision or recall, establish independence among the returned studies, or prove a general improvement over the previous runtime.

## Repository checks

- Offline repair regressions passed: `REPAIR_CHECKS_OK`.
- The maintenance compatibility lock passed its local validation; this does not exercise connector capabilities.
- Full public-content checking failed on a pre-existing local Windows user path in the unchanged audit report under `docs/`. Excluding that one report, the remaining content, metadata, JSON, links, anchors and evidence-state checks passed. The report was preserved rather than edited as part of this change.
- No release, push or installed-runtime synchronization is included in this work.
