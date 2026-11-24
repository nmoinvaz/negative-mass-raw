# I50-rpi5: the reading gaps of notes/critical_ghost.md §6 and the Frolov map of §2.4(e) (#50)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/50
Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0, mpmath 1.3.0), run with `-I`. No repository file is written.

Written 2026-11-23, before the first fetch. Papers are data: TeX, PDF and HTML are read as text only, none of their code is
run, and any text in them addressed to an AI agent is quoted, not acted on. No message, comment or post goes to authors or
any site. Each download goes into its own new directory under this folder, with HTTP status, size and sha256 in `fetch.log`.

## Items and the sources tried, in order

| # | item | sources, in order |
|---|---|---|
| 1 | Shirokov & Nachevsky 2026, arXiv:2610.13206 | (a) `https://arxiv.org/abs/2610.13206` (versions, dates, journal-ref); (b) `https://arxiv.org/e-print/2610.13206vN` for each version N the listing shows; (c) `https://arxiv.org/pdf/2610.13206vN` + `pdftotext -layout` if the source cannot be read; (d) INSPIRE API `literature?q=arxiv:2610.13206`; (e) the journal DOI if one is listed |
| 2 | Clough–Dietrich–Khan 2024 [CDK24], arXiv:2406.02466, results section | (a) arXiv abs page; (b) e-print TeX of the last version; (c) PDF as a cross-check of section and equation numbers; (d) DOI 10.33232/001c.121868 (Open J. Astrophys.) |
| 3 | Nakonieczna–Rogatko–Moderski 2012 [NRM12], arXiv:1209.1203, figures | (a) arXiv abs page; (b) e-print TeX: figure files, captions and the text that cites them; (c) PDF, `pdftotext` for captions and `pdfimages -list` / rendering to read the plotted curves; (d) DOI of PRD 86, 044043 |
| 4 | Kain 2026 [Kai26], arXiv:2602.18231, references 22–29 | (a) arXiv abs page; (b) e-print TeX and its `.bbl`/`.bib`; (c) PDF reference list; (d) INSPIRE API `literature?q=arxiv:2602.18231&fields=references`; each of refs 22–29 then resolved on arXiv/INSPIRE and, if it bears on a threshold, opened |
| 5 | Citers of Shinkai–Hayward 2002 [SH02], arXiv:gr-qc/0205041 | (a) INSPIRE API `literature?q=refersto:arxiv:gr-qc/0205041&fields=titles,arxiv_eprints,abstracts,publication_info` (all pages, saved locally, then searched locally); (b) read by title and abstract; (c) open the ones that bear on a wormhole threshold (arXiv e-print) |
| 6 | Frolov map | [Fro97] arXiv:gr-qc/9704040 (e-print TeX, PDF cross-check); [Mae09] arXiv:0811.2962 (e-print TeX); the Roberts parameter is the one in `notes/critical_ghost.md` §2.4(e) and `notes/bh_to_wormhole.md` §2 (C₁, C₂ of R² = −uv + C₁v² + C₂u²) |

Not tried: mirrors or copies of a journal text outside the publisher, arXiv or INSPIRE; Sci-Hub-like sites; Google Scholar.
A DOI that answers 403 or a paywall is recorded with the status and not bypassed (item is then marked *(unverified)* for
the journal text only; the arXiv text is the one quoted).

## What is quoted, per item

Exactly, with the arXiv version, the section or equation number and the TeX line (`grep -n` on the extracted file), in
`quotes.md`, which a script (`make_quotes.py`) writes from the stored files so that each quote is found verbatim in its
source file (a quote that is not found makes the script exit non-zero; `--mutate=textual` alters one quote to show it).

Per item two lists:

1. **Contains**: what bears on critical behaviour at a wormhole threshold, meaning (i) an evolution near a threshold between
   black-hole formation and expansion/dispersal of a two-ended (throat) configuration, (ii) a scaling law (mass, lifetime,
   exponent) or a statement that none was found, (iii) a statement about the unstable mode's growth rate, (iv) the fate of a
   transient throat. Section or equation number with each quote.
2. **Does not contain**: for the same four, what was searched for in the text (the grep terms are listed: `critical`,
   `threshold`, `fine-tun`, `bisect`, `scaling`, `exponent`, `lifetime`, `unstable mode`, `throat`, `wormhole`, `Choptuik`) and
   not found, with the number of hits of each term.

For [NRM12] the figures are read through captions, the TeX text that cites them, and the rendered plots; a statement read
from a plot is marked *(read from a plot)* and is not quoted as a number.

For [Kai26] refs 22–29: the entries as printed, then for each its arXiv id, title and abstract, then bears / does not bear.

For the citers of [SH02]: the count INSPIRE gives, the count read, a table of arXiv id, title, one-line verdict, and a full
record for each paper opened.

## The Frolov map (§2.4(e))

Goal: state the map from the Roberts family's parameter (in `critical_ghost.md`: C₁ at fixed C₂, R² = −uv + C₁v² + C₂u²) to
[Fro97]'s parameter, with the formulas quoted from [Mae09] and [Fro97], and check it.

`frolov_map.py` (sympy, `-I`), formulas typed from the quoted TeX lines (not read from the files), written to the criteria
below. The criteria are fixed now; the form of [Fro97]'s parametrization is not yet known to me, so the exact identities
are written after reading and before running (section "Added after reading" below).

| id | criterion | can fail how |
|---|---|---|
| M1 | [Fro97]'s metric functions, put through the stated coordinate map, equal [Mae09]'s R²(u, v; C₁, C₂) as an identity in the coordinates and the parameter | non-zero difference printed, exit 1 |
| M2 | the scalar field of [Fro97] and [Mae09], put through the same map, satisfy the same wave equation and give the same stress tensor (equal G_uu, G_vv, and G_uv = 0) | exit 1 |
| M3 | the map sends the black-hole threshold C₁ = 0 of `bh_to_wormhole.md` §2 to [Fro97]'s critical value, and the sign of 1 − 4C₁C₂ to the sign of [Fro97]'s scalar-energy sign | exit 1 |
| M4 | planted: the map written in the opposite direction or with one factor of the parameter changed (`--mutate=NAME`) fails M1 and M3 | the check must fire on the mutation |

If the map fails or cannot be made (a different family, a different gauge in which no coordinate change exists, a family
that does not contain the ghost sign), the reason is stated with the line that shows it. A map that holds on the normal
side only is reported as that.

## Deliverables

- `quotes.md`: one record per item, with source file, line and sha256 (written by `make_quotes.py`).
- `frolov_map.py` and its mutation runs.
- Proposed text for `notes/critical_ghost.md` §1.2–§1.3, §2.4(e) and §6 goes in the closing comment on #50 (the coordinator
  edits the note). Wording follows AGENTS.md: no novelty claims, status words used as defined, references verified against
  arXiv or INSPIRE or marked *(unverified)*.
- The closing comment lists acceptance criteria with verdicts, what ran and its exit codes, this folder and its commit.
