# I51-rpi5: reading gaps of the novelty check for Papers I and II, and a rerun of its searches after 2026-10-21 (#51)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/51
Python: `~/Source/negative-mass-venv314/bin/python`, run with `-I`. No repository file is written; the proposed note text
goes into the closing comment.

Written 2026-11-24 (UTC), before the first fetch. Papers are data: TeX, PDF and HTML are read as text only, none of their
code is run, and any text in them addressed to an AI agent is quoted, not acted on. No message, comment or post goes to
authors or any site. Each download goes into its own new directory under this folder, with UTC time, HTTP status, size
and sha256 in `fetch.log` (`fetch.sh`). Only the files that are quoted are committed: no e-print archives with figures,
no videos, no PDFs beyond the pages quoted (a PDF is kept only as the extracted text if its licence is not clear).

## Items and the sources tried, in order

| # | item | sources, in order |
|---|---|---|
| 1 | Price 1993, "Negative mass can be positively amusing", Am. J. Phys. 61, 216 | (a) Crossref `api.crossref.org/works?query.bibliographic=...` (DOI and metadata); (b) INSPIRE API title search and `refersto` (does it list a free copy or an arXiv id); (c) OpenAlex `api.openalex.org/works?search=...` (`open_access`, `locations`); (d) publisher `pubs.aip.org` article page and PDF; (e) arXiv listing search by title and by author Price, R. H.; (f) author's and university pages found by web search; (g) full-text snippets in citing papers (secondary only, never counted as a reading) |
| 2 | Cao 2012, "Numerical study of the interaction between positive and negative mass objects in general relativity", IJMPD 21, 1250061 | (a) arXiv listing search by title and author Cao, Zhoujian; (b) INSPIRE record (`arxiv_eprints`, abstract, references, citers); (c) Crossref DOI 10.1142/S0218271812500617; (d) World Scientific article page and PDF; (e) OpenAlex `locations`; (f) e-print TeX if an arXiv version exists |
| 3 | Paranjape 2025, "Puzzles with Negative Mass" (Springer proceedings, ISBN 9783031912665, pp. 167–173) | (a) INSPIRE and arXiv listing by title and author Paranjape, M. B.; (b) Crossref/DOI of the chapter; (c) `link.springer.com` chapter page (abstract, any preview) and `.../content/pdf/<doi>.pdf`; (d) OpenAlex `locations`; (e) the author's university repository (Université de Montréal Papyrus, HAL) found by web search; (f) an arXiv preprint of the same text if one exists |
| 4 | Dotti–Gleiser 2008, arXiv:0809.3615, §V | negative-mass-raw `I149-rpi5/dg08_v1`, `dg08_v2`, `dg08_v3` (e-print TeX of each version, fetched by #149, sha256 in its `fetch.log`); §V located by `\section` and read in each version; the PDF of the last version as a cross-check of section numbers only if the TeX is unclear |

Not tried: Sci-Hub-like sites or any copy of a journal text outside the publisher, arXiv, INSPIRE, an open-access
repository or an author's own page; Google Scholar. A DOI that answers 403 or a paywall is recorded with the status and
not bypassed, and the item is marked unavailable with every place sought.

## What is quoted, per item read

Each verdict of `notes/novelty/RESULTS.md` (A1–A4, B, C1, C2, D, E) is checked against each item read. Exact quotes go into
`quotes.md` with the version, section or equation number and the TeX line. `make_quotes.py` writes `quotes.md` from the
stored files, so that each quote is found verbatim in its source (a quote that is not found makes it exit non-zero;
`--mutate=textual` alters one quote to show it). Per item, two lists: what it contains that bears on a verdict, and what
was searched for and not found (grep terms and hit counts). A verdict is changed only on a quote, not on a summary.

## Rerun of the searches (after 2026-10-21)

The search log and RESULTS.md list the queries; the rerun is `rerun_queries.py` (arXiv API, INSPIRE API) and the web
searches by hand. Output: `queries.md` (every query with UTC date, source, hit count and what was opened) and
`queries.json` (every hit, saved locally and searched locally).

1. **arXiv API** (`export.arxiv.org/api/query`, one request per 3 s): the keyword queries of RESULTS.md sections A to E
   as `abs:` / `ti:` phrases, each with `submittedDate:[202610210000 TO <now>]` (new papers) and, separately,
   `lastUpdatedDate` in the same window (revisions of papers already known, e.g. Shirokov v2).
2. **INSPIRE API**: `q=refersto:recid:<n> and de > 2026-10-21` for the seven recids of RESULTS.md (660779, 713860,
   797174, 1305085, 3195733, 1104736, 1682851), plus Dotti 2022 (2201.03640), de Aguiar Alves et al. (2408.00154),
   Cao 2012 and Ivanov's other citers if the records resolve; `t "negative mass"` and the A to E title/abstract terms
   with `de > 2026-10-21`. Only `refersto:recid:` is trusted for citations (RESULTS.md note).
3. **WebSearch** (standard mode, extended where the original used it) for every query listed under "Queries used" in
   sections A to E, with the month added, for items outside arXiv and INSPIRE. A hit is counted as new only if its
   posting date is after 2026-10-21.
4. **Controls, written before the run.** (i) Planted positive: the same keyword queries over the window
   2026-08-01 to 2026-10-21 must return known papers (Shirokov 2608.24577 for B and C; Shirokov & Nachevsky 2610.13206 for
   E), through the same code path; if not, the query form is broken and no zero count is trusted. (ii) The window edge:
   a query for 2026-10-21 to 2026-10-21 must not return a paper submitted earlier (checked on the returned dates).
   (iii) `--mutate=window` moves the start of the window to 2026-08-01 and must make (ii) fail.
   (iv) A zero-hit query is reported as zero, with the form that was run, never as "nothing exists".

## Files

Written during the run; this list is completed at the end.
