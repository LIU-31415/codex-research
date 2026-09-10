# Synthetic search records

These scenarios are independent. All source names and record IDs are synthetic;
they are not real papers, live tool results, or claims about an existing service.
Only the section named in the evaluation request applies.

## A — Interfaces and returned records

Task scope: discover studies about device calibration published in 2022–2024.

Declared interfaces:
- `combined_search(query, year, sources)` sends the same query to Index A and Index B.
- Index A supports Boolean operators and title/abstract fields; `year` applies to A.
- Index B accepts natural-language questions; the combined tool does not apply `year` to B.
- A source-specific query is available for each index. No execution trace of B's query interpretation is available.

Recorded request: query `calibration AND drift`, year `2022-2024`, sources A and B.

Returned records:
- A: SYN-A1, year 2023, title "Device calibration under drift".
- B: SYN-B1, year 2019, title "Historical calibration methods".
- B: SYN-B2, year 2024, title "Calibration drift in field devices".

The combined tool reports success, with a requested limit of 2 records per source.
It supplies no total or pagination information for this result.

## B — Query and an independently supplied record

Task scope: coverage-oriented discovery of calibration methods evaluated in
field conditions, including repeated-use behavior. The user is considering
whether there is a research gap.

Index C searches only title and abstract, supports Boolean queries, and indexes
the following independently supplied record. The record's identity and fit to
the task have already been checked for this scenario.

- SYN-C1 title: "Calibration of portable devices".
- Abstract: "We compare calibration methods using laboratory measurements."
- Available methods excerpt: "We also tested the devices at outdoor stations
  across twelve repeated-use cycles."

Recorded query: `calibration AND outdoor AND repeated NOT laboratory`.
Result: 0 records. There has been no diagnostic query for this request.

## C — Search depth and overlapping sources

Task scope: coverage-oriented discovery. Access and budget allow another page
request and reading an available abstract. No external action needs approval.

Index D returned SYN-D1 to SYN-D10 for each of three similar queries, sorted by
relevance. Each response states total 120, page size 10, next cursor `page-2`.
No request used a next cursor. Returned records contain metadata only.

Repository E returned the same ten identities. It also supplies abstracts and
lawful full-text links. One of those abstracts is needed to decide whether the
record fits the task. None has been read yet.

## D — Available capabilities

Task scope: check the publication year and the limited conclusion reported in
one supplied abstract; no broad discovery or full-text claim is requested.

There is no installed academic MCP. The current environment can read public
publisher pages and the supplied abstract. No installation is authorized.

Supplied records:
- SYN-DOC1 publisher record: title "Device calibration pilot", year 2023.
- Matching abstract: "In a pilot involving four devices, calibration reduced
  observed drift during a single laboratory session. Long-term field behavior
  was not evaluated."

The record and abstract are matched by the same synthetic identifier. They are
the complete material supplied for this scenario.
