# MCP retrieval repair and verification — 2026-10-05

## Result and installation boundary

The local connector was upgraded from the cached package-registry distribution to a managed upstream-source installation at commit `cab1b5cc276a0cd004a0044003926a6440088049`, with a reproducible local patch. Both distributions label themselves `0.1.4`; the version string alone does not identify these capabilities. The Skill does not bundle or maintain this local connector. The maintenance lock now records the reviewed upstream revision; it does not attest to the local patch or every provider.

Only this connector's launch command/arguments were explicitly changed in the local Codex configuration, with a private backup. Other MCP configuration and credentials were preserved. The evaluation subprocess also automatically registered two temporary evaluation directories in the project-trust table; those entries were retained. Fresh stdio sessions and the evaluation subprocess used the managed installation. An existing app session may retain the old server/tool inventory until restarted.

Repairs cover explicit Semantic Scholar failures and bounded per-source timeouts from upstream; local preservation of warning/error-only empty responses at the common search boundary (including IACR and OA repository fallback); BASE's HTTP-200 access-denied XML; Windows-compatible Semantic Scholar filenames shared by download/read; and a genuine in-memory read-only `fetch_paper_text` tool. Writing/download tool annotations and host approval controls were not weakened. Read-only text supports public arXiv PDF and PMC/Europe PMC XML, returns coverage/truncation, and does not verify visual content.

## Live source checks

Checked all 23 default source names plus Scopus, Web of Science and credential-dependent IEEE; an additional unknown-name control confirmed explicit rejection. Each discovery probe requested at most 2 records. General sources used `machine learning`; biomedical repositories used `coronavirus`; bioRxiv/medRxiv used valid categories; IACR used `encryption`; Unpaywall used a DOI. These demonstrate execution and diagnose failure, not scientific eligibility, historical coverage, precision or recall. Eighteen sources returned records at least once; some varied across calls.

| Source | Observed status | Consequence |
|---|---|---|
| arXiv | Search returned records; original PDF text read | Verified discovery/text route for selected papers only |
| PubMed | Search returned records | Metadata/abstract discovery; use verified original-text alternatives |
| Crossref | Search returned records | Metadata/DOI route; top results can miss a known seed |
| OpenAlex | Search and both citation directions returned records | Index identities/edges require original-source checks |
| PMC | Search returned records | Repository discovery; selected XML access verified via Europe PMC |
| Europe PMC | Search returned records; matched original XML read | Discovery plus selected lawful XML route |
| bioRxiv | Category lookup returned records | Recent/category/DOI semantics; not free-text historical coverage |
| medRxiv | Category lookup returned records | Same distinction; preserve preprint/version status |
| IACR | Search returned records | Relevant disciplinary discovery |
| Google Scholar | Search returned records in this probe | Challenge/rate-limit dependent; not guaranteed availability |
| DOAJ | Search returned records | Article/asset identity and OA access still need checking |
| Zenodo | Search returned records | Screen document type and paper/asset identity |
| HAL | Search returned records | Check deposited version and identity |
| SSRN | Metadata search returned records | Underlying OpenAlex route; not independent native-database coverage |
| OpenReview | Public search returned records | Does not verify arbitrary note/PDF access |
| ACM | Metadata search returned records | Underlying Crossref route; original access separate |
| CORE | First probe throttled; later returned records | Intermittent; failed calls now retain diagnostics |
| Semantic Scholar | First probe returned records; later HTTP 429 | Intermittent; errors now explicit; optional key may improve limits |
| dblp | HTTP-200 browser challenge caused XML parse failure | Unsearched branch; use original conference/discipline sources while access is blocked |
| OpenAIRE | Timed out | Explicit coverage limit; do not loop equivalent requests |
| CiteSeerX | Timed out | Explicit source failure; use suitable alternatives |
| BASE | HTTP-200 XML denied access | Explicit source failure; provider-authorized access is required |
| Unpaywall | Contact email not configured | Explicit missing configuration; not keyword search |
| Scopus | API credential missing | Explicit unavailable institutional-index coverage |
| Web of Science | API credential missing | Same; metadata API rights are separate from full text |
| IEEE | Not enabled without key | Explicit unavailable source; no fabricated credential |

Private raw records are retained in the original local workspace: initial source probes at `evals/.runtime/mcp-20261005/search.json`, repaired diagnostics and citation calls at `evals/.runtime/mcp-20261005-final/calls.json`, read-only arXiv text at `evals/.runtime/mcp-20261005-readonly/arxiv.json`, and matched PMC XML at `evals/.runtime/mcp-20261005-readonly/pmc.json`. These locations describe local provenance; the records are excluded from the public repository and require review before sharing.

## Original text, citations and metadata accuracy

Fresh MCP sessions read arXiv `1706.03762v7`: 15/15 pages, 39,861 characters, no tool-level truncation. A verified DOI-to-PMC identity mapping led to `PMC7314750`; its Europe PMC original XML returned 41,685 characters without truncation. The preliminary XML verification script initially assumed the returned `paper_id` was a PMCID; the connector instead returned a PMID with PMCID in the URL/extra fields. The verifier was corrected to use the matched PMCID, not to guess a different paper. Successful text retrieval does not verify images or every claim in either article.

For the coronavirus DOI seed, each OpenAlex citation direction returned 3 records and `truncated=true`; reported available totals were 43 references and 711 citing works at this checkpoint. These totals are index metadata, not independent eligible studies or full coverage.

The Transformer evaluation exposed a further accuracy limit: OpenAlex node `W2626778328` had a matching title/author set but conflicting year/DOI, and some returned citation records had mixed identities. A separate request to the native OpenAlex API confirmed that the conflicting year/DOI originated in its response rather than the connector's field conversion. These records were not accepted as verified bibliographic identities or supporting studies. The practical guide now explicitly requires validating graph seeds/edges against original identifiers/version/publication context; that clarification followed the evaluation and was not separately model-tested.

## Actual Skill/MCP behavior run

The first bounded run, `20261005-live-mcp-preflight`, requested the existing reasoning setting and timed out after 420 seconds. Writing/cache-related `read_arxiv_paper` and the separate fetch connector were blocked by the subprocess's `approval_policy=never`. Its locally retained result, `evals/runs/20261005-live-mcp-preflight/live_mcp_retrieval_preflight/skill/result.json`, remains failed/incomplete; it is not counted as a pass.

After adding the truly read-only path, `20261005-live-mcp-readonly` requested `gpt-6.1-sol` with an invocation-only `low` reasoning override and completed in 176.784 seconds. The host warned about model-metadata fallback and unsupported priority-tier metadata; those warnings limit model/runtime attribution. Host plugin guidance remained present. No baseline was run and the comparison is not an isolated measure of Skill improvement.

Actual events contain four discovery calls (arXiv, Crossref, dblp failure, OpenAlex), both citation directions, and two successful `fetch_paper_text` calls. The answer noticed the failed source and metadata conflicts, preserved citation truncation, checked a limited original finding against body Table 3/§6.2, handled display truncation with a smaller read and matching HTML, and separated the future coverage plan from the executed demonstration. The primary agent read the answer/events and manually scored all seven declared checks at 2 under the saved rubric. Local run: `evals/runs/20261005-live-mcp-readonly/`; answer and events are `live_mcp_retrieval_preflight/skill/final.md` and `live_mcp_retrieval_preflight/skill/events.jsonl`, with `scores.json` and `manifest.json` at the run root. Both behavior runs' raw records are excluded from the public repository and require review before sharing.

This supports a bounded operational workflow with explicit failures and original-text verification. It does not establish all-provider availability, broad recall, citation-graph correctness or production factual accuracy. The original table observation was separately checked in [the arXiv original](https://arxiv.org/html/1706.03762v7#S6.SS2).

## Validation and continuing research

Relevant connector regressions passed in staged groups: 262 passed/1 skipped for source/fallback/schema/citation/PDF tests; 66 passed/2 skipped for the changed fallback/IACR/search-timeout paths; and 9 passed for the new read-only text/diagnostic/stdio paths. Skips are not validated capabilities. Skill offline regressions and frontmatter validation passed. The existing private audit report still prevents a full public-content check; excluding that unchanged local-only report, public content checking passes.

The Skill's practical retrieval guide is linked from the entrypoint and search strategy. All 13 runtime files were synchronized to the installed Skill and their SHA-256 hashes matched; entrypoint reference links were checked. It covers complementary concept branches, source-specific syntax/filters, verified seeds, backward/forward expansion, caps, language/date/type gaps, independent studies, contrary evidence, source failures and original-text checks before synthesis. Future research can use the verified routes while explicitly retaining missing branches. Exhaustive coverage across blocked/credential-dependent providers remains unavailable until lawful access is supplied; it must not be represented as completed.
