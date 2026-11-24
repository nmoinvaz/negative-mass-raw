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

Fetched from arXiv on 2026-11-24 with `fetch.sh` (log: `fetch.log`, every request HTTP 200). arXiv lists one version of 2610.38659
(v1, 28 Oct 2026) and 1309.2448 (v1, 10 Sep 2013), and two of 2610.29941 (v1 21 Oct 2026, v2 6 Nov 2026; v2 is current, and the
unversioned fetch is byte-identical to v2). No journal reference is shown on any of the three abstract pages. Quote locations
are in `quotes.md`; the TeX and PDFs it cites are committed (`sha256sums.txt`). E-prints (tar.gz holding TeX and EPS or PDF
figures) are not committed; their sha256 is below.

| paper | version | TeX committed (sha256) | PDF committed (sha256) | e-print, not committed (sha256) |
|---|---|---|---|---|
| arXiv:2610.38659, Blázquez-Salcedo et al., "Exact Rotating Wormholes in Five Dimensions and Their Exceptional-Point Instability" | v1 | `src/2610.38659/main.tex` (7e3587c2…1167) | `pdf/2610.38659.pdf` (7c69b469…262e) | 28b1856e…e9d9 |
| arXiv:2610.29941, Shirokov and Nachevsky, "Rotation slows the instability of Ellis-Bronnikov wormholes" | v2 (current) | `src/2610.29941v2/research.tex` (988d214d…e4d7) | `pdf/2610.29941v2.pdf` (92d3ad90…8da1) | 97295085…94d1 |
| same | v1 | `src/2610.29941v1/research.tex` (0ad462e1…a6dc) | `pdf/2610.29941v1.pdf` (29824e64…5485) | f3fb7c70…7081 |
| arXiv:1309.2448, [DFKKR13], "Rotating Wormholes in Five Dimensions" | v1 | `src/1309.2448/rotworm.tex` (0262cf1c…b870) | `pdf/1309.2448.pdf` (8b5710d6…0c34) | 1d82a1e7…49b5 |

Full hashes: `sha256sums.txt`. Scripts: `check_quotes.py` (C1-C5), `jovera_check.py` (recompute of |J|/A, below), `fetch.sh`.

Both versions of 2610.29941 were read because they differ (about 1500 diff lines of TeX); the quotes cite v2 unless marked
V (v1 only, checked absent from v2).

## Fetch log

See `fetch.log` (UTC time, HTTP status, content type, bytes, URL, local name, sha256).

## Step 2 findings (all three papers read; proposal not yet written)

Predictions written before the run, compared with what the sources say:

| prediction | found | verdict |
|---|---|---|
| 1. The body of 2610.38659 agrees with its abstract: the mode does not disappear, the same family is refined | A04, A09, A34, A40: same equal-J family, merger at the same J, the continuation is an oscillatory pair | as predicted |
| 2. [DFKKR13] does not contain "the unstable mode disappears above a critical angular momentum" | D01 (abstract): "the unstable mode of the static wormholes solutions vanishes when the angular momentum exceeds some critical value"; D20 (Sec. VI): "the two unstable modes then bifurcate and disappear"; D18 (Sec. V B) hedges: "rotation may stabilize wormholes" if "no new unstable modes of a different type appear" | **wrong**: the claim is in [DFKKR13], hedged in the body, unhedged in the abstract |
| 3. 2610.29941 claims no stability, only no growth seen | S31 (v2, Sec. VI): "evidence of prolonged radial stability under the numerical perturbations present in the sampled high-spin evolutions", bounded by S32 ("a slower mode could still emerge later"); v1 was stronger and v2 removed it (V01, V02) | **partly wrong**: a bounded stability claim is made |

Checks so far (run from this folder, `python3 -I check_quotes.py`): 111 quotes pass C1 (TeX) and C2 (PDF), 0 failures.
Controls, each exits 1: `--mutate=quote` (1 failure), `pdf` (1), `sha` (8), `absent` (5). `jovera_check.py`: exit 0, and `--mutate=G1`,
`p0`, `exponent`, `lam` each exit 1 (logs `jovera_*.log`). C3 and C5 and their controls (`cite`, `dangling`, `number`, `cell`)
need `proposal.md` and are run after it is written.

Unplanned recompute (labelled as such): neither 2610.38659 nor [DFKKR13] states G in the text read. From the exact solution printed
in 2610.38659 (Eqs. (8), (19)-(22)), |J|/A at the printed lambda values (2.190024, 2.059523, 3.948341) reproduces 0.100628, 0.05475,
0.48717 and the limits 1/2 (lambda -> 4) and 0 (lambda -> 2) only with G = 1/(4 pi), that is 4 pi G = 1 (`jovera_run1.log`; with
G = 1 every value is smaller by 4 pi, `jovera_G1.log`). So |J|/A in both papers is in units 4 pi G = 1.
