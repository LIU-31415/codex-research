# Real-paper full-text appraisal: He et al. (2024)

## Scope and source

This is a targeted appraisal of one independently selected public experimental paper, not a literature-retrieval benchmark: He et al., *A recirculating device of cooling water powered by solar energy for the laboratory*, Scientific Reports 14, 15572 (2024), [DOI 10.1038/s41598-024-66215-6](https://doi.org/10.1038/s41598-024-66215-6), PMC11227590.1.

The package contains the eight-page published PDF, four main figure images, Supplementary Legends and Supplementary Information 1 (DOCX), and two demonstration videos. The PDF came from the current PMC Open Access AWS dataset; the other originals came from Europe PMC's supplementary-files ZIP. All nine matched the MD5 values supplied by the current PMC metadata. Exact source URLs and local SHA-256 values are in [the source manifest](real-paper-20260927-sources.json). The article states [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); attribution belongs to He et al. Original binaries are retained locally, not bundled in this repository.

Acquisition on 2026-09-27 encountered publisher redirects, a PMC page challenge, and obsolete PMC API routes. The [current official PMC dataset documentation](https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/) and [dataset README](https://pmc-oa-opendata.s3.amazonaws.com/README.txt) supplied the working metadata and HTTPS asset route. These are observations of the primary agent's acquisition, not retrieval performed by the evaluated model. The metadata reported `is_retracted: false`; this is a dated repository status, not an exhaustive publication-status guarantee.

## Pre-run checks and neutral inputs

Before the first model run, the primary agent read the full PDF text and inspected all eight rendered pages, main tables and figures, and read the extracted supporting text/tables. Both supporting documents were extracted with paragraph/table/image links. A separate reviewer completed the supporting-text/image check after launch but before inspecting the model answer; later discoveries are distinguished below. The initial gold notes were kept outside the staged case. No expected conflicts, scores, or appraisals were included in the first two model prompts or entry files.

The model was asked in Chinese to read the full paper, including main figures/tables and relevant supplements, and assess the evidence for cooling performance, water saving, power supply and replacement of laboratory tap-water cooling. It was asked for results, conditions, limitations, locators and actual reading coverage; external paper discovery was outside this supplied-material case.

Important checks included:

| Source assertion | Original finding and disposition |
|---|---|
| Abstract, p.1: temperature difference below 4 degrees Celsius | Table 2, p.6 reports 4.2 for acetic acid at 5 V with an open condenser. The universal bound needs a condition-specific exception. |
| Abstract, p.1: largest solvent loss below 6% | Tables 2 and 3, p.6 include 6%; Results, pp.5–6 says no more than 6%. Preserve the strict-inequality difference without inventing measurement precision. |
| Methods, p.2 and series discussion, pp.5–6: eight hours | Table 3, p.6 lists ten hours. Keep both locators and the unresolved duration; Table 3 also has no temperature row despite the narrative temperature assertion. |
| Abstract/introduction: no additional water/electricity | Results, pp.3–4 describes electrically powered components and pp.6–7 gives conditional resource estimates; SI Part III derives 240 Wh/day from a 10 W continuous load. Distinguish recirculation/grid substitution from zero energy or a measured lifetime water balance. |
| Abstract/conclusion: nearly matching reaction yields | Table 4, p.6 lists three values per group/product with descriptively close means. No equivalence or non-inferiority result follows. |
| Long operation and applicability | The 38-hour test is the specific water case in p.5/Fig.4b. It does not establish all-solvent endurance, arbitrary load, or subambient refrigeration. |
| SI battery paragraph: one week; body p.7: three days | SI Part III sizes 75 Ah from 20 Ah/day, three days and a 0.8 factor. Under those assumptions 100 Ah corresponds to about four days; distinguish design sizing from field endurance. |
| SI configurations and container comparison | Tables S1/S2 distinguish demonstration and working configurations, so differing ratings are not inherently conflicting. Fig.S9 and its methods compare containers with partly different water volumes/geometries; do not infer an isolated material effect. |

A further unit-conversion problem was verified **after the first run launched**, so it was not retroactively required for the initial score. SI Part III Eq.(2) uses 1.63 Wh/kcal. [NIST's conversion table](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8) gives 4184 J per thermochemical kcal and 3600 J per Wh: about 1.16222 Wh/kcal. Keeping the other SI inputs unchanged gives approximately 3.50 equivalent sun-hours and 117 W in Eq.(3), rather than 4.91 hours and 83 W. This is an audit derivation, not a validated replacement photovoltaic design.

## Execution and first result

All three executions use `gpt-5.6-terra`, `medium` reasoning, Codex CLI 0.153.4, read-only sandbox, Skill-only mode, and the existing runner. An ignored local launcher sets the runner's `CASES_PATH` to the local case list; binary staging, source-safety restrictions, frozen input snapshots and normal output capture remain unchanged. The public case catalog does not depend on ignored downloads. This adds no public runner API or dependency.

First run: `20260927-real-paper`, runtime fingerprint `e4f9089b7387551b04d3574aeb6db18144b0dfceb3db994d376bb434ef2ccf94`. Execution completed; the independent reviewer and primary adjudication accepted these item scores:

| Check | Score | Observed basis |
|---|---:|---|
| EVIDENCE_BOUNDARY | 1 | Disclosed missing visual verification but asserted no reported ambient-temperature range despite unread Fig.4b. |
| ORIGINAL_TEXT_USE | 1 | Events show body/SI text reads and recovery of later pages; no successful visual read. |
| FACT_CHECKING | 1 | Recovered 8/10 hours and bounded yields; omitted explicit temperature/loss abstract conflicts and SI duration mismatch. |
| CHECKPOINT_CLOSURE | 1 | Correct table values appeared, but the omitted comparisons were not closed in the final judgment. |
| COMPARABILITY | 2 | Kept the limited load/yield comparison and did not claim general chiller equivalence. |
| PROPORTIONATE_COMPLETION | 1 | The requested figure-inclusive appraisal remained incomplete. |

Total: **7/12, partial**. The reviewer's initial headline said 8/12, but its six component scores sum to 7; the accepted record uses the component scores.

The native image-view attempt is important provenance: it is absent from the JSONL item list but present in stderr. `view_image` attempted `page-4.png` and failed when the Windows filesystem-sandbox helper could not start through `CreateProcessAsUserW`. The subsequent `cua.getState` also failed in sandbox setup. This is not evidence that the model never tried the native viewer. A separate `pdftotext` command was unavailable despite the surrounding command's zero exit status. No screen data or successful image observations were returned. Image coverage failure and unsupported absence wording are separate issues.

## Targeted revision and image-assisted reassessment

Only the full-text reading reference changes:

1. Check boundary entries and strict inequalities under matched conditions; using a corrected number does not replace reporting its material conflict with the abstract.
2. Recalculate decisive design arithmetic/units and compare it with associated duration/performance wording in the body and SI. Preserve configurations and estimate-versus-measurement distinctions.
3. Do not declare information unreported when it may be present in an unread visual object.

The independent reviewer found no substantive issue in this narrow revision. No rule prescribes a table, a fixed tool, or a per-sentence checklist.

Second run: `20260928-real-paper-images`, runtime fingerprint `5d3d94b46dec9dce285294cb5e9fa2e91bc54bf94462d733f9926cbc403dc8e9`. To complete the visual assessment despite the helper error, the local launcher uses the existing CLI `--image` input feature. It attaches 26 source images in recorded order: eight PDF pages, the higher-resolution Fig.4 image, eleven supporting images including a raster rendering of the embedded EMF circuit diagram, and six timestamped video frames. The original DOCX, figures, PDF and videos remain staged; the gold notes remain excluded. The attachment order, source hashes and launcher hash are retained in `image-input-manifest.json`. The case prompt is unchanged apart from neutral instructions identifying those image attachments.

This is a supported alternative input route under the same read-only sandbox, not a sandbox change or repair of native `view_image`. Initial attachments test interpretation of supplied original visuals; they do not demonstrate autonomous image-tool selection or a repaired PDF-viewing environment. The instruction revision and input route both changed, so any difference cannot be attributed to the Skill alone.

The reassessment also **failed**. The independent reviewer scored EVIDENCE_BOUNDARY / ORIGINAL_TEXT_USE / FACT_CHECKING / CHECKPOINT_CLOSURE / COMPARABILITY / PROPORTIONATE_COMPLETION as **2/2/0/0/2/2 (8/12)**. Source images and text were available, but the answer silently chose ten hours and explicitly said the problem was not an obvious abstract/body numerical conflict. The two strict-bound conflicts and SI one-week mismatch were still missing. No unit recalculation was performed. The primary agent additionally flagged an unreported "parallel" trial characterization for correction; retaining the reviewer's score does not endorse that wording. Thus the added instructions are not demonstrated to solve the observed semantic omissions.

## Review-assisted correction

After both unassisted appraisals failed, the workflow changed to explicit source review and targeted correction instead of repeating fresh generations until one passed. The evidence reference now explains that a previously missed material conflict or unsupported consistency assertion warrants a targeted second source check, followed by repair and verification of affected conclusions. Independent review remains conditional; a review report by itself is not a repaired answer.

The correction exercise `20260928-real-paper-review-repair` supplies the previous appraisal, source-grounded review findings, and the same original text/images. It asks the model to verify the findings, retain supported content and correct the complete appraisal. Unlike the two earlier runs, the identified conflicts and the post-run unit audit are intentionally supplied. This is an assisted repair exercise, not a blind detection test, and cannot establish autonomous conflict discovery.

The correction run completed with runtime fingerprint `f3fb3a0b62acac5e6db220446b5cae76d068390d993b43b32aba3cf9de2f002e`. Its final answer now explicitly pairs the two abstract bounds with the table exceptions, preserves eight versus ten hours, separates three-day sizing from the unsupported week claim, and reports the recalculated 3.50 hours / approximately 117.5 W as a derivation rather than a measurement. It also preserves the zero-energy/water distinction, unknown trial independence, room-temperature bars in Fig.4b, and container-volume limits for Fig.S9. Actual events show reads of the original body and SI, not just the review feedback. The image attachment manifest remains available; this does not imply a successful native viewer call.

The independent reviewer scored the assisted output **1/2/1/2/2/2 (10/12)** in the same check order, with CHECKPOINT_CLOSURE now 2 but the raw response still partial. The primary agent and reviewer found wording to correct: the reservoir's 5 L capacity was presented as a specified water charge, and a sentence placing all three voltages beside the bubbler-zero result was ambiguous despite a later correct 5/9 V qualification. These were not accepted as source facts in the user-facing source appraisal. The delivered Chinese report keeps reservoir capacity separate from the 4.5 L hot-water test and explicitly identifies Table 2's 5/9 V and Table 3's 9 V bubbler rows. The reviewer checked that deliverable's specified core comparisons and the primary applied the final condition clarification; no further model run was needed. The raw model output is retained unchanged. Targeted source review and primary repair closed the identified comparisons in the deliverable; the assisted model response is not treated as a flawless autonomous reading result.

## Limits and retained artifacts

Originals, extraction helpers, rendered pages, frames, neutral entry, pre-run gold notes and the Chinese source appraisal are retained under the ignored local `evals/.runtime/real-paper-20260927/` directory. Raw runs, manifests, inputs and score records remain under ignored `evals/runs/`. Do not commit those raw files without privacy and licensing review. Text extraction and page/frame rendering are derived aids; they do not replace reading. Three sampled frames per video do not establish continuous viewing, motion, audio, endurance or quantitative performance.

This is one paper, one model, two unassisted appraisals under different image-input conditions, and one explicitly assisted correction. There is no no-Skill baseline or independent error-rate estimate. Scoring is source-aware, not blinded. Host plugin instructions may remain despite standalone Skill overrides; the correction run also attempted a task-keyword memory search, which failed and returned no memory evidence. Successful execution, a polished answer, valid links and filled scores do not by themselves establish full reading or a stable scientific verification loop.
