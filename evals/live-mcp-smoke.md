# Live MCP Smoke Test

Date: 2026-08-30

## Capability inspected

Connector: `paper-search-mcp`

- Unified discovery tool: `search_papers`
- Inputs include query, source list, and per-source depth.
- Results include per-source counts, errors, deduplicated paper records, metadata, possible abstracts, and possible PDF URLs.
- `download_with_fallback` exposes `use_scihub`; the Skill must set it to `false`.

## Search call

Query:

```text
structural batteries multifunctional energy storage mechanical performance
```

Sources:

```text
openalex,crossref,arxiv
```

Depth: 2 results per source.

## Observed result

- 6 records returned: 2 OpenAlex, 2 Crossref, 2 arXiv.
- No connector errors were reported.
- Only one result was directly aligned with multifunctional structural battery composites.
- Crossref results concerned structural thermal-energy-storage book chapters rather than structural batteries.
- arXiv results concerned networked or shared battery-energy-storage systems rather than load-bearing battery materials.
- Some records contained abstracts, while others provided metadata only.
- A returned `pdf_url` cannot be assumed to belong to the canonical paper until title/identifier identity is verified.

## Refined search call

Query:

```text
"structural battery" load-bearing composite mechanical electrochemical performance
```

Sources: OpenAlex and Crossref, 3 results per source.

Observed comparison:

- All 3 OpenAlex records were closely aligned with structural batteries or multifunctional structural lithium-ion battery composites.
- Crossref returned 1 relevant structural energy-storage preprint and 2 lexical false positives about load-bearing composite structures without batteries.
- The refined query materially improved relevance over the broad pilot, while source-level concept screening remained necessary.

## Design conclusions

1. Unified search is useful for discovery but still requires concept-level screening.
2. Query evolution can materially improve relevance; source result counts still do not measure relevant coverage.
3. Metadata, abstract, and candidate PDF URL must remain separate access states.
4. A candidate asset must pass paper-identity verification before it can become full-text evidence.
5. Refined cross-source search should be followed by source-specific screening rather than assuming uniform ranking quality.
6. No download was attempted and no Sci-Hub path was used.
