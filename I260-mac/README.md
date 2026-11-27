# I260-mac: reading log of the prior work on #248's growing horizon sector (statements S1–S4)

Machine: the coordinator's Mac (Apple M5, macOS), one process at a time, `nice -n 10`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/260 (milestone G9). Worktree `~/Source/negative-mass-i260`, branch
`wip/i260-horizon-literature` from main 3b3358c. Deliverables: `notes/black_universe/horizon_literature.md` and a subsection
of `notes/literature.md`. Date of the reading: 2026-11-27.

## The statements read against (fixed before the reading)

| id | statement | where it comes from |
|---|---|---|
| S1 | At c = −1 the coefficient c₂ = ∂_V δr of the horizon sector is a free number of regular Cauchy data | `horizon_sector.md` (#248) |
| S2 | So the c = −1 black universe has a linear growing direction of rate κ; this contradicts the "stable" verdict for that member | #248, #232 |
| S3 | A non-extremal Killing horizon at an extremum of the areal radius makes the Kruskal coefficient of δr gauge invariant; it then grows at the surface-gravity rate | `horizon_lemma.md` (#261) |
| S4 | Y_ref = R e^{κx} is an exact solution of the black universes' radial master equation at W = −2c/π for every member, and d(W/κ)/dc = 0.31403 at c = −1 | `cminus1_mode.md` (#262, branch `wip/i262-cminus1-mode`) |

## Verdict words (fixed before the reading)

Exactly one of: "contained in [X]", "contradicted by [X]", "not found in the N papers read" (with the list).
- *contained in [X]*: the text of X states the statement, or a statement from which it follows in one step, for the same
  system (S1, S2, S4) or for a class that includes the system (S3). Quoted, with section and equation.
- *contradicted by [X]*: the text of X states the opposite for the same system and the same class of perturbations.
  A verdict on a different class (for instance a condition on u = Y/ρ where S1 concerns Y regular and nonzero) is
  reported as such and is not a contradiction.
- *not found in the N papers read*: no passage of the N papers states it. N counts the papers whose full text was opened;
  the depth of each is in the table below.
- No verdict says "new" or "first".

Depth words: **F** = every page of the extracted text read; **S** = the named sections read, the rest searched by the
patterns below; **G** = the full text searched by the patterns below and the passages that matched read with their
surroundings; **A** = abstract only (INSPIRE or arXiv page).

## Method

1. INSPIRE (`inspirehep.net/api/literature`): the citers of [BKZ12] (recid 1114144), [BF06] (698463), [BMD07] (730845),
   [SV19] (1709812), Aretakis's 1206.6598 (1120268), [LMRT13] (1206868) and [MRT13] (1244519) downloaded in full to
   `queries/cit_*.json`, with abstracts, and filtered locally. Other INSPIRE queries and the arXiv API queries are in
   `queries/queries.tsv`, one row per query: name, query, total hits, records retrieved, date. The records of the title
   queries are `queries/q*.json`, the arXiv Atom replies `queries/arxiv_a*.xml`. WebSearch queries (mode "extended"):
   `queries/websearch.md`.
2. Each paper's PDF (and for the papers whose equation numbers matter its e-print) is downloaded from arxiv.org into its own
   new directory `papers/<id>/` (slash of old ids replaced by `_`), sha256 and size in `papers/downloads.tsv`. Nothing in any
   paper is run. Text addressed to an AI agent is to be quoted, not acted on.
3. Text: `text/<id>.pypdf.txt` from pypdf (`uv run --no-project --with pypdf`, the repository venv lacks pypdf) and, as a
   cross-check of the layout and the equation numbers, `text/<id>.pdftotext.txt` from poppler's `pdftotext -layout`.
   Quotes are copied from these files and their section and equation is given.
4. Screening pass over the citing papers: the PDFs of every citer of [BKZ12] with an arXiv id, and of the citers of the other
   records whose abstract names stability, instability or perturbations together with black universes, phantom fields, throats,
   wormholes, bounces or regular black holes, are downloaded and searched with the patterns of `screen_patterns.txt`.
   A match is read in its surroundings and goes into the table. A paper with no match is listed with its depth G.
5. Each reference in `notes/literature.md` is checked against INSPIRE (title, authors, journal, DOI) and the arXiv identifier;
   a field not confirmed is marked *(unverified)*.

## Acceptance (written before the reading; each can fail)

- A1: every reference of the new entries is verified against INSPIRE or arXiv, or marked *(unverified)*.
- A2: each entry quotes, with section and equation or page, the statement that bears on S1–S4, or says that none does.
- A3: a verdict for each of S1, S2, S3, S4 in the three allowed forms.
- A4: [BKZ12]'s horizon boundary condition is compared with #212's `u = Y/ρ → 0` and with S1's `Y` regular and nonzero.
- A5: each of Paper IV's six `% NEEDS #260` comments gets a sentence worded to the verdicts, or the statement that nothing can be said.
- A6 (mutation of the process): a quoted string is checked against the extracted text by `check_quotes.py`; changing one
  character of a quote in the note makes the check fail (`--mutate`).

## Log (2026-11-27)

### What was run

| step | what | result |
|---|---|---|
| 1 | INSPIRE citers of [BKZ12], [BF06], [BMD07], [SV19], Aretakis 1206.6598, [LMRT13], [MRT13], `queries/cit_*.json` | 262, 453, 197, 543, 245, 121, 105 records |
| 2 | other INSPIRE queries (`queries/queries.tsv`, `q01`–`q17`) and 13 arXiv API queries (`arxiv_a01`–`a13`) | one row each: query, total hits, records retrieved. `q05` (a `refersto:arxiv:` query) returned HTTP 400 and was not rerun in that form: the [SV19] citers were fetched by recid instead |
| 3 | WebSearch, mode "extended", 8 queries (`queries/websearch.md`) | the links they returned were handled by id; nothing from the tool's own summaries is quoted |
| 4 | the read list (`lists/core.txt`, `lists/extra.txt`; depth in `lists/readlist_depth.tsv`, 59 papers: 2 F, 39 S, 18 G) downloaded from arxiv.org (`scripts/dl.py`) with the e-print of the 40 core ids | `papers/downloads.tsv`: url, size, sha256 of every download |
| 5 | the screening list (`lists/bulk.txt`, 374 ids: every citer of [BKZ12] with an arXiv id and the citers of the other records whose abstract names stability, instability or perturbations with black universes, phantom fields, throats, wormholes, bounces or regular black holes; Aretakis/[LMRT13]/[MRT13] citers whose abstract names a throat, wormhole, bounce, non-extremal horizon, surface gravity, area radius, regular black hole or phantom field) downloaded with `scripts/dl2.py` | 373 of 374 downloaded; 2603.06822 returned HTTP 404 |
| 6 | text extraction (`scripts/extract.py`: pypdf and `pdftotext -layout`) | 424 papers with text: the 59 of the read list and 365 screened only |
| 7 | `scripts/screen.py` with `screen_patterns.txt` over the 424 texts | `screen_counts.tsv` (matches per pattern per paper), `screen_contexts.txt` (up to 8 contexts of 120 characters each side per pattern per paper) |
| 8 | `scripts/restate.py` | `restatements.txt`: the papers that restate [BKZ12]'s verdict (10) |
| 9 | references: INSPIRE record and the arXiv stamp of the downloaded PDF for 62 ids (`scripts/verify_refs.py`, `verify/verify_table.tsv`, authors in `verify/authors.tsv`) | all 62 found on INSPIRE; the stamps agree with the ids; the 4 old `gr-qc/` ids have a stamp format the script's regex does not match, and their first pages were read by eye (title, id, version and date agree with INSPIRE); the table still lists the wrong id 1802.04795 (Bonder, Corral), dropped from the read list |
| 10 | `quotes.tsv` (71 quotes with section or equation) and `scripts/check_quotes.py` | 71 of 71 found in the extracted texts; `--mutate` changes one character of the first quote and the check fails, as it must |

Read at depth F or S, a paper's relevant text was read in the extracted copy; at G the patterns were applied and the matches
read in context, and the abstract was read. "Screened only" means G on the full text and nothing more: a pattern match was
read in context and listed, no match means that none of the patterns of `screen_patterns.txt` occurs in the paper's text.
A paper whose statement is worded differently from every pattern would be missed; the patterns are broad (13 of them) but fixed.

### Errors in my own process, kept

- The id 1802.04795 was recalled, not read, as the "bifurcation sphere" paper of Angelopoulos, Aretakis and Gajic. It was
  downloaded, the INSPIRE table showed it to be "Unimodular Einstein–Cartan gravity" (Bonder, Corral), and the id was dropped
  (its PDF deleted, its two rows stay in `papers/downloads.tsv`). The right id, 1802.05692, was found by INSPIRE query `q15`.
- The first bulk downloader (`dl.py`) ran at one request per 6 s; it was stopped after 120 papers and replaced by `dl2.py`
  (two workers, requests at least 3 s apart in total) for the rest. `dl.py` skips existing files, so nothing was fetched twice.

### What the screening found

Counts and contexts are in `screen_counts.tsv` and `screen_contexts.txt`; the passages used in the notes are in `quotes.tsv`.
- Restatements of [BKZ12]'s verdict that the c = −1 member (horizon at the minimum of the area function) is stable, with no new
  computation: 1802.00098, 1908.09126, 2006.00559, 2009.12057, 2304.07383, 2305.00058, 2310.19037, 2510.18647, 2602.16972,
  2604.20661, 1308.5959 (the last was found by the `coincide` pattern; `restate.py`'s regex missed it).
- Papers that state a solution with the minimum of the areal radius on a horizon, without a stability analysis: 2504.07861,
  2109.01794, 2009.12057, 2112.13198, 2603.05543 (null throat on an extremal horizon), 2201.01650 (rotating, null throat on an
  extremal horizon), 2409.12101, 2609.02313, 2609.14199.
- No paper matches `nonzero_dr` ("δr … horizon/throat … nonzero"). `exact_mode` matched 7 papers: [BKZ12], whose sentence is that
  "analytical expressions for static perturbations are unknown" for nonzero potentials, and 6 unrelated ones (test-field QNMs,
  Fisher solutions, a k-essence perturbation equation integrated in closed form in 1908.09126, a different system); none gives a
  closed form for a growing mode of the black-universe master equation. No match of `kappa_growth` describes growth at an
  outer or event horizon: the matches are inner-horizon mass inflation (8 papers), a redshift-decay statement (1306.5364,
  2611.31459) and the near-extremal Aretakis growth of 2512.23629.
- Mass inflation at inner horizons grows at the inner surface gravity (several papers; [CDLPV18] §3 read).

### Acceptance (written above) against the outcome

| id | outcome |
|---|---|
| A1 | the references of the new entries are among the 62 checked against INSPIRE and the PDF stamps (`verify/verify_table.tsv`); the arXiv listing page of a paper was not opened, the stamp on the PDF's first page is the arXiv check; journal data are INSPIRE's |
| A2 | each entry in the notes quotes with section or equation, or says that no passage bears on S1–S4 |
| A3 | a verdict per statement in `notes/black_universe/horizon_literature.md` |
| A4 | the comparison table of [BKZ12]'s horizon condition with #212's `u = Y/ρ → 0` is in the same note |
| A5 | the sentences for the six `% NEEDS #260` comments are in the same note |
| A6 | `python3 scripts/check_quotes.py` and `--mutate`; the note's strings are checked with `python3 scripts/check_quotes.py <note.md>` |

### Not committed

The PDFs, e-prints and extracted texts of the 424 papers stay on the Mac (`papers/*/paper.pdf`, `source.tgz`, `text/`), as
third-party content in a public repository. `papers/downloads.tsv` gives each url and sha256, and
`python3 scripts/dl.py`, `extract.py` rebuild them. Nathan or the coordinator can ask for them to be committed.

### Files

`README.md`, `quotes.tsv`, `screen_patterns.txt`, `screen_counts.tsv`, `screen_contexts.txt`, `restatements.txt`,
`lists/` (id lists and depth table), `queries/` (INSPIRE and arXiv replies, `queries.tsv`, `websearch.md`),
`verify/` (reference tables), `scripts/` (the code above), `papers/downloads.tsv`.
