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

See the list at the end of this file (written when the run was complete).

## Run log (UTC, 2026-11-24)

- 01:29–01:38 metadata and publisher pages for the four items (`fetch.log`). Price 1993, Cao 2012 and Paranjape 2025 full texts
  are unavailable (publisher 403 or paywall; no arXiv version; OpenAlex and Semantic Scholar list no open copy). The abstract
  and reference list of Paranjape's chapter and the abstract and reference list of Cao 2012 were read (`quotes.md`).
  DG08 §V (Summary) read in v1, v2 and v3 from #149's TeX (`quotes.md`, `make_quotes.py`).
- `quotes.md` is written by `make_quotes.py` (47 quotes, each found verbatim in its source; `--mutate=textual` exits 1,
  `mutate_quotes.log`).
- Controls of `rerun_queries.py`, run 1 (`run1/`): three planted papers were wrong (2603.04400 for B01: its abstract has no
  "boson star"; 2608.24577 for I02 and I03: its abstract has neither "negative mass" nor "boson"). Cause found by reading the
  abstracts (`run1/`). The plants were replaced, not the criteria: B01 and I02 lost their plant, I03 keeps 2605.10976, and B10
  plants 2603.04400 on terms its abstract holds (ghost, scalar, neutron stars). Run 2 (`ctl_plain.log`): PASS; `--mutate=window`
  (`ctl_window.log`): FAIL on C2 as designed; `--mutate=terms` (`ctl_terms.log`): FAIL on C1 as designed. The raw responses of the
  control runs are not kept (`queries.json` of each holds the parsed hits).
- INSPIRE abstract-field queries: `abstracts.value:"negative mass" and arxiv:<id>` returns the id whatever the first clause says
  (`abstracts.value:"zzzzzz" and arxiv:2608.24577` returned 1), so the first clause is ignored when ANDed with an `arxiv:` clause;
  such tests are not used as controls. The phrase query on its own works (I03 found 2605.10976).
- arXiv API: `lastUpdatedDate` is rewritten by the server to `submittedDate`, so revisions of known papers are read from an
  `id_list` request instead (section K of `queries.json`).
- Web searches: `websearch/01.tsv` to `06.tsv` (34 queries, standard mode).
- Post-window items opened: Shirokov 2608.24577 v2 (2026-10-26), Laguna 2611.14482 (2026-11-10, "Singustars"), and Ivanov
  1204.1269v2 (re-read for the Havas–Goldberg sentence); the files are `shirokov_v1`, `shirokov_v2`, `new_2611_14482_*`,
  `ivanov_*`.

## Result in one paragraph

Price 1993 and the full texts of Cao 2012 and Paranjape 2025 are unavailable (places and statuses in `quotes.md`, last
section, and `fetch.log`); their abstracts and reference lists were read where the publisher or INSPIRE shows them. DG08 §V
(Summary) and §§I-IV were read in v1, v2 and v3. No verdict of RESULTS.md changes; `proposed_text.md` holds the changed
wording. The rerun of the searches (`queries.md`) found one record that bears on a verdict (Laguna 2611.14482) and three
revised known papers (Shirokov 2608.24577 v2, Shirokov and Nachevsky 2610.13206 v2, Caridi et al. 2603.13210 v2).

## Files at the end

| file or folder | what it holds |
|---|---|
| `README.md` | this file: plan, run log, files |
| `quotes.md`, `make_quotes.py`, `make_quotes.log`, `mutate_quotes.log` | 47 quotes found verbatim in their sources; negative evidence for DG08; places sought for each item; the textual mutation (exit 1) |
| `queries.md`, `make_queries_md.py`, `opened.json` | every rerun query with UTC time, counts, new hits, citation trails, revisions of known papers; what was opened |
| `rerun/queries.json`, `rerun/raw/` | the full run: parsed hits and the unchanged API responses (sha256 in the json) |
| `rerun_queries.py`, `run_controls.sh`, `run_controls2.sh`, `run_full.sh`, `ctl_*.log`, `ctl_*.rc`, `rerun_ctl_*/queries.json` | the script, the control runs (plain, `--mutate=window`, `--mutate=terms`) and the full run |
| `run1/` | the failed first runs kept as evidence: three wrong plants, and the INSPIRE `or` precedence bug (I04) caught by C2 |
| `websearch/` | the 34 web queries and the results, as returned |
| `proposed_text.md` | proposed edits for RESULTS.md and search_log.md |
| `fetch.sh`, `fetch.log` | every fetch with UTC time, HTTP status, size and sha256 |
| `price_*`, `cao_*`, `par_*`, `s2_*`, `fatcat_*`, `sec_physl` | metadata and publisher answers for the three unavailable texts (403 pages kept as the record of the status) |
| `shirokov_abs`, `shirokov_v1`, `shirokov_v2`, `ivanov_*`, `new_2611_14482_*`, `new_2603_13210_abs`, `new_2610_13206_abs`, `bp13_*` | post-window items and the Ivanov and Belletete-Paranjape texts that were quoted or searched (TeX only, no figures) |

## Controls, final state (UTC 2026-11-24)

- Full run 1 (`run1/full_run1_I04_precedence.log`, `run1/full_run1_queries.json`) failed C2 on I04 (56 hits dated before
  2026-10-21): the INSPIRE query `t "A" or t "B"` followed by `and de > d` binds as `A or (B and de > d)`. Cause: no
  parentheses around the base query. Fix: every INSPIRE base query is wrapped in parentheses. No threshold changed.
- Full run 2 (final script): `controls: PASS 146 runs` (`full.log`, `full.rc` = 0). `queries.md` is generated from it.
- Final script, control subset: plain PASS (`ctl_plain.log`, rc 0); `--mutate=window` FAIL with 53 C2 lines (`ctl_window.log`,
  rc 1); `--mutate=terms` FAIL with 12 C1 lines (`ctl_terms.log`, rc 1). The earlier runs of the same three are in `run1/*_prev.log`.
