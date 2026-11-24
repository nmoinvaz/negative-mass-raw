# I152-rpi5: reading of the two rotating-wormhole stability papers, proposed rewrite of §1.1's row

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64). Issue: https://github.com/nmoinvaz/negative-mass/issues/152

Task: read arXiv:2610.38659 (Blázquez-Salcedo et al., rotating 5D wormholes), arXiv:2610.29941 (Shirokov–Nachevsky,
rotating 4D) and arXiv:1309.2448 ([DFKKR13]) in full, and propose a rewrite of the row "Rotating 5D Ellis wormholes" in
`notes/critical_ghost.md` §1.1 (main at 1305816). Reading only. The note is the coordinator's; this folder holds the
proposal.

Written before any source was fetched. The sections "Files" and "Fetch log" are filled in after step 1.

## Questions

| id | question |
|---|---|
| Q1 | For each paper: system (dimension, field content, rotation: equal angular momenta or not), perturbations (modes, sector), method (linear modes, time evolution, both), parameter range |
| Q2 | What happens to the unstable mode as the angular momentum grows (disappears, merges, becomes oscillatory); the critical value with its normalization (what J and A are, in the paper's words) |
| Q3 | 2610.29941: what "no growth through t = 150 at the fastest spin, over finite times" rests on: run length, resolution, and whether the authors claim stability or only no growth seen |
| Q4 | Whether 2610.38659 says [DFKKR13]'s "disappears" was wrong, refined, or about a different quantity |
| Q5 | Where [DFKKR13] makes the claim "the unstable mode disappears above a critical angular momentum" (quote), or that it does not. If it comes from another paper that [DFKKR13] or 2610.38659 cites, name it and say whether it was read |

## How each answer is checked

- Every answer is a quote from a fetched source, with its section, equation, figure or table number, recorded in
  `quotes.md` (quote id, source file, location, question). What I recall about a paper is not a source. A claim with no
  quote is listed as unsupported, never softened into the proposed row.
- Locations (section, equation and page numbers) come from the TeX (`\section`, `\label`, `\begin{equation}` order) and are
  cross-checked against `pdftotext -layout` of the PDF, because the PDF is what the reader sees.
- A contradiction with the current row, or between two papers, is reported as found.
- The critical value and its normalization are copied, not recomputed, unless the paper gives the inputs. If I recompute,
  the entry says so.

## Checks (each can fail)

| id | check | pass criterion | control |
|---|---|---|---|
| C1 | every quote of `quotes.md` occurs verbatim in its source TeX | `check_quotes.py` exits 0: each quote, after removing TeX markup (`\cite{..}`, `\,`, `$`, `\mathrm`, braces, comments) and collapsing whitespace, is a substring of the equally normalized source | `check_quotes.py --mutate=quote` alters one word of one quote and must exit 1 |
| C2 | every quote also occurs in the PDF text | same, against `pdftotext` output (hyphenation and ligatures normalized) | `--mutate=pdf` checks one quote against the wrong paper's PDF and must exit 1 |
| C3 | every sentence of the proposed row in `proposal.md` cites at least one quote id that exists in `quotes.md` | `check_quotes.py` exits 0 | `--mutate=cite` deletes one citation and must exit 1; `--mutate=dangling` cites `Q99` and must exit 1 |
| C4 | sha256 of each file listed in this README equals the file on disk | `check_quotes.py` exits 0 | `--mutate=sha` flips a digit and must exit 1 |
| C5 | numbers quoted in the proposal (0.100628 etc.) occur in a quote | `check_quotes.py` exits 0 | `--mutate=number` changes one digit in the proposal and must exit 1 |

Predictions written before reading (to be compared with what the papers say; a miss is reported, not adjusted):
1. The abstract of 2610.38659, as quoted in #50, says the two imaginary frequencies merge at |J|/A = 0.100628 and become
   an oscillatory instability. I predict the body of the paper says the mode does not disappear, so the current row's first
   sentence ("disappears") is refined for the same family, not contradicted by a different quantity. Q4 is open until read.
2. I predict [DFKKR13] is a rotating-wormhole construction paper (solutions, not a stability analysis) and does NOT contain
   the sentence "the unstable mode disappears above a critical angular momentum". If so, the claim comes from another paper
   (likely a stability follow-up by Kleihaus, Kunz or Blázquez-Salcedo et al.), named in 2610.38659's introduction.
3. 2610.29941 is a time evolution at finite times, with no claim of stability (only "no growth seen"). Q3 is open until read.

## Files

(filled in after step 1)

## Fetch log

(filled in after step 1)
