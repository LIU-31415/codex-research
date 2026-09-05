# Search Strategy

## Search as progressive refinement

Use the least expensive source capable of answering the current question. Increase search depth only when the user confirms the direction or when a consequential claim requires stronger evidence.

A typical progression is:

1. conversation and supplied materials;
2. Web Search and Web Fetch for terminology and field orientation;
3. a small academic pilot search;
4. focused multi-source paper retrieval;
5. full-text acquisition and reading;
6. evidence-gap or contradiction-driven retrieval.

This progression is adaptive. Do not restart from the beginning when the user provides a precise question, known papers, or an existing research state.

## Search intent

Infer the least demanding search intent that satisfies the request:

- `EXPLORATORY`: discover vocabulary, branches, and candidate questions;
- `FOCUSED`: answer a defined question with decision-relevant evidence;
- `COVERAGE`: reduce missed literature within declared source, date, language, and publication-type boundaries.

Do not force these labels into user-facing output. In `COVERAGE`, record the important query families and sources, use known-paper recall and citation or related-paper expansion when relevant, and state the remaining coverage limits. This is still not a formal systematic or scoping review unless the required protocol and review procedures were completed.

For each substantial `COVERAGE` query, retain the exact query, source, search date, filters, sorting, requested result limit, pages or cursors covered, and any reported total or truncation. Record these in working notes or the existing research state; no separate logging system is required. Distinguish the publication-date filter from the date the search was run. Mark unknown totals or pagination support as unknown.

## Capability negotiation

Before relying on an academic connector, inspect the tools actually available in the current Codex environment.

Distinguish capabilities rather than assuming that one MCP name guarantees them:

- paper discovery;
- stable identifiers and metadata;
- explicit abstracts;
- PDF or XML download;
- readable full text;
- citation relationships;
- source-specific filters.

For `paper-search-mcp`, prefer its unified `search_papers` capability for initial academic discovery, then use source-specific search, download, or read tools when their coverage or retrieval ability adds decision value. Prefer source-native and open-access retrieval paths. Do not call a Sci-Hub tool. When `download_with_fallback` or an equivalent tool exposes a `use_scihub` option, set it explicitly to `false`. Otherwise use a fallback downloader only when its current configuration and tool description make clear that unauthorized sources are disabled or excluded. Tool names and capabilities may change; inspect the current tool metadata rather than assuming this exact list.

If the agreed evidence level depends on a capability that the current tools do not provide:

1. Explain which capability is unavailable and how that limits the current task.
2. Ask whether the user wants Codex to install or configure a suitable connector, or to continue with existing tools under an explicit coverage or evidence limitation. Present both routes in one checkpoint and recommend one.
3. If the user has not already selected a route, wait for the answer. Before approval, do not install software, edit MCP configuration, start authentication, or request credentials.
4. After approval, inspect the current official instructions and existing configuration, preserve user customizations, complete only the approved setup, restart when required, and verify with one harmless real tool call.
5. If the user declines, stop this MCP-dependent path. Remove only temporary files created by the attempted setup, preserve existing files and configuration, and do not call the connector. Continue with existing tools only when the user selected that route in the same checkpoint or had already requested it; otherwise report the coverage limitation and wait.

The official project reference is:

https://github.com/openags/paper-search-mcp

This Skill does not bundle, host, fork, or maintain the connector. Use only public/open access, the user's lawful institutional access, or user-supplied files. Do not invoke or recommend options that bypass paywalls or access controls.

## Evidence access states

Record what was actually obtained:

- `SEARCH_HIT`: discovery result or snippet only;
- `METADATA_ONLY`: title, authors, year, venue, identifiers;
- `ABSTRACT_READ`: an explicit abstract was opened and read;
- `FULLTEXT_FILE_AVAILABLE`: an accessible asset passed the paper-identity gate;
- `FULLTEXT_TEXT_READ`: verified article body text was parsed or read;
- `FULLTEXT_LOCATED`: the passage, table, figure, or section supporting a claim was located in the verified full text.

Treat every discovered or downloaded PDF, HTML page, XML file, repository copy, or supplement as a candidate asset first. Verify the title, authors, stable identifier, document type, and publication-version relationship against the target paper. Until that identity check passes, retain the paper's existing access state and record the asset separately; do not promote it to any `FULLTEXT_*` state.

Never infer a stronger state from a tool's name or a successful return status.

## Web orientation

Use Web Search to discover language and candidate sources. Use Web Fetch to inspect authoritative pages.

Prefer:

1. standards bodies, government agencies, scientific organizations, and official documentation;
2. universities and research institutes;
3. publisher, journal, repository, and database pages;
4. high-quality reviews for vocabulary and citation discovery;
5. general pages only for orientation.

Search snippets are leads. They are not abstracts or scientific evidence. Web orientation may propose vocabulary and branches, but it must not seed an assumed scientific conclusion that the paper search merely confirms.

## Concept and query evolution

Maintain a concept model rather than a flat keyword list. Concepts may represent:

- object, population, material, system, or phenomenon;
- process, exposure, intervention, or method;
- context, environment, boundary condition, or application;
- outcome, response, performance metric, or failure mode;
- mechanism, mediator, moderator, or explanatory factor;
- comparison, exclusion, or competing interpretation.

Within a concept, expand synonyms, abbreviations, spelling variants, controlled vocabulary, formulas, legacy terms, and field-specific phrases. Across concepts, combine only meaningful intersections.

As research proceeds:

- the vocabulary pool may expand;
- individual queries should become more discriminating;
- exclusions should remove known ambiguities;
- evidence gaps should generate targeted queries;
- ineffective terms should be retired or marked uncertain.

Record where an important term came from and what ambiguity or retrieval gap it resolves.

## Search rounds as purposes

Do not require fixed R1-R5 labels. Select search purposes dynamically:

- vocabulary discovery;
- strict intersection of core concepts;
- known-paper verification;
- citation or related-paper expansion;
- method or measurement retrieval;
- contradictory or null-result retrieval;
- recent update search;
- evidence-gap search.

Every query should have a purpose. Avoid exhaustive keyword permutations.

## Tool-call execution

- Batch independent discovery queries in one call when the tool supports it.
- Normalize paper identities, version relationships, and duplicates before opening or downloading full text.
- Retrieve or parse full text only for papers with high decision value or claims that require it.
- Retry a failed source at most once without a changed reason, then switch to a lawful alternative or record the coverage gap.
- After each substantial batch, assess newly added independent, high-relevance evidence before deciding to continue, refine, or stop.

## Source selection

Choose sources according to the question and available evidence, not a universal database ranking. Broad indexes, disciplinary databases, repositories, preprint servers, standards databases, and patent sources play different roles.

Preserve the source and query path for important papers. A source failure is a coverage limitation, not evidence of absence.

## Candidate identity and deduplication

Prefer stable identities:

1. DOI;
2. PMID, PMCID, arXiv ID, or another source-stable identifier;
3. normalized title with authors and year.

Recognize that a preprint, conference paper, journal extension, correction, and repository copy may represent related publications or the same underlying study. Merge database duplicates while preserving version relationships.

Do not count multiple records, reports, reviews, or versions as independent evidence.

## Known-paper validation

When the user supplies known papers, verify whether they are retrieved and correctly identified. If one is missing, investigate the cause:

- terminology or spelling;
- date or document-type filter;
- indexing delay;
- source coverage;
- title or identifier mismatch;
- query depth or ranking.

Use the result to improve the search strategy. Do not guarantee completeness from known-paper recall alone.

## Prioritizing papers for reading

Prioritize by decision value:

- direct relevance to the current claim;
- ability to distinguish competing explanations;
- methodological adequacy for the question;
- access to conditions, data, or limitations;
- independence from existing evidence;
- role as an original study, method, replication, boundary case, or contradiction;
- recency when the field changes rapidly;
- scholarly influence and venue as secondary navigation signals.

Journal prestige, citation count, author institution, and publication novelty cannot substitute for article-level evidence quality.

## Gap-driven retrieval

After preliminary synthesis, search only for gaps capable of changing the answer, such as:

- a missing research design;
- an untested condition or population;
- conflicting outcomes;
- an alternative mechanism;
- missing negative or null results;
- uncertain independence;
- a key inaccessible full text;
- outdated coverage.

Explain why another round is worth its cost.

## Stopping

Stop or pause when:

- the user's current decision can be supported at the agreed evidence level;
- new searches produce little decision-relevant information;
- remaining gaps require user-provided full text or unavailable access;
- unresolved disagreement cannot be reduced with accessible evidence;
- further work belongs to a formal systematic-review protocol;
- the user chooses to narrow, pause, or conclude.

For `COVERAGE`, decision sufficiency alone is not a stopping condition. First complete the declared query families and sources, address material expansion gaps, confirm that successive batches add little or no new independent high-relevance evidence, and document the remaining coverage limits.

Repeated top-ranked results are not evidence of saturation while a result cap or unvisited pages may hide further matches. Where supported, paginate, increase depth, or use complementary queries to address the truncation within the agreed scope. If that is unavailable or exceeds the agreed budget, stop with the truncation recorded as a coverage limit, without claiming saturation.

Phrase absence cautiously:

> No relevant study was identified in the sources, queries, dates, and access conditions used in this session.

Do not write that no literature exists unless the claim is supported by a suitable, documented search design and even then retain the scope boundary.
