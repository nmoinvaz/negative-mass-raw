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

## Answers (quote ids are in `quotes.md`; `S` = 2610.29941 v2, `A` = 2610.38659, `D` = [DFKKR13], `V` = v1 only)

**Q1. System, perturbations, method, range**

| | [DFKKR13] arXiv:1309.2448 | [BGKKKN26] arXiv:2610.38659 | [SN26b] arXiv:2610.29941 v2 |
|---|---|---|---|
| system | 5D, Einstein + phantom field, equal angular momenta J₁ = J₂, cohomogeneity one (D02) | same (A11, A01, A07, A12) | 4D, Einstein + phantom scalar (S07, S08), stationary axisymmetric rotation (S09); drainhole family C = 1 evolved, symmetric family only for solver validation (S10, S33) |
| perturbations | cohomogeneity-one, gauge H₁ = H₃ − H₂, H_φ = 0 for unstable modes (D08, D09, D10) | cohomogeneity-one gravitational sector, same gauge, φ and angular-velocity perturbations decoupled (A19, A43); reflection-symmetric family only (A01) | none added beyond discretization error, except ±10⁻³ radial at D21 (S21, S22); axisymmetric data (S33) |
| method | linear eigenvalue problem for Ω², auxiliary ODE Ω²′ = 0 on a numerical background (D11, D25); time evolution left as future work (D21) | linear modes, Chebyshev collocation, on an exact (Toda) background (A21, A22, A45) | nonlinear 3+1 evolution, CCZ4, adaptive mesh (S20); τ is a fit of the nonlinear areal radius, not a linear-mode eigenvalue (S38) |
| range | \|J\|/A from 0 up to the extremal Myers–Perry value (D26); symmetric and \|a₋∞\| = 1 (D24) | λ from 2 (static) to 4 (extremal Myers–Perry, \|J\|/A = 1/2) (A18, A17); followed to \|J\|/A ≃ 0.48717 (A38) | D0 to D90: v_e from 0 to 0.90, 8πJ/A from 0 to 80.8 % (S15, S16, S13); backgrounds to v_e ≈ 0.99 (S42) |

**Q2. The unstable mode as J grows**

- [DFKKR13]: for J > 0 a second unstable mode appears, descended from the static zero mode (D12, D23). The two get closer and merge at J_cr
  (D14): (\|J\|/A)_cr = 0.10063 for symmetric wormholes and 0.1381 for \|a₋∞\| = 1 (D15, D16). No unstable mode is found beyond it "within
  the type of modes investigated" (D17). Abstract: "vanishes" (D01); Sec. VI: "bifurcate and disappear" (D20); Sec. V B: "rotation may
  stabilize wormholes" if "no new unstable modes of a different type appear" (D18).
- [BGKKKN26]: the same two imaginary frequencies coalesce at \|J\|/A = 0.100628 (λ = 2.190024, ω_EP A^{1/3} = 2.429974 i), with the eigenvectors
  (A03, A26, A27, A28, A29). Beyond it the pair is ω± = ±ω_R + iω_I, ω_I > 0 (A04, A30, A33, A35, A36). ω_I A^{1/3} falls to order 10⁻⁶ and
  Re ω to zero near \|J\|/A ≃ 0.48717; the data are consistent with ω_I ∼ (\|J\|/A − 0.5)⁶ (A37, A38, A39).
- Normalization, copied: J = J₁ = J₂ (A12, D03), read from the asymptotics of the rotation function (A16, D04), A the throat area, A_T(0) in
  [BGKKKN26] (A14, A15) and the minimal-area surface A(0) in [DFKKR13] (D05, D06), with J and M scaled by A (D07). Neither paper states G.
  Recomputed here from [BGKKKN26]'s exact solution: the printed values need 4πG = 1 (`jovera_run1.log`, controls in `controls/`).
- [SN26b] has no mode-merger value. Its collapse rate extrapolates to zero at 32 % of the extremal J, against 33 % from second-order theory
  (S34), an extrapolation not a measured endpoint (S35); the 28.8 % and 33 % models expand (S41); J is a percentage of A/8π (S13), G = c = 1 (S11).
  v1 said the expansion was consistent with a second mode "rather than with the instability ending in a mode merger" (V03); v2 does not (S37).

**Q3. What "no growth through t = 150 at the fastest spin" rests on (v2)**

- Run: D90, 8πJ/A = 80.8 %, L = 128, N = 128/192/256, finest Δx = 0.0625, "scaling as 1/N within a triplet" (Table IV caption), so the three members differ, σ = 0.4, final t = 150 (S15, S14),
  Δt = 0.02 Δx (S20). 150/5.4 = 27.8 static e-folding times, with 5.4 from Table V (S17, S25): hand arithmetic, matches "about 28" (S02).
- Evidence: the areal radius drifts by ≤ 7×10⁻⁵ at all three resolutions (S25, S18), constraint norms converge at every level over the run
  (S28, S29). D75 and D80 show the same over shorter intervals (S26, S31).
- Claim: "no growing departure" (S02); "prolonged absence of detected radial growth ... over finite times from initially axisymmetric data" (S03);
  "evidence of prolonged radial stability under the numerical perturbations present" (S31). Not a claim of stability: growth is bounded "only over
  that span; a slower mode could still emerge later" (S32), only axisymmetric growth is bounded and only C = 1 was evolved (S33), and
  "no detected growth" is not "measured zero eigenvalues" (S30).
- Not tested at D90: perturbations of both signs were added only at D21 (S22). The criteria of S22 (nonzero convergent e-fold time) do not apply when there is no growth.
- v1 was stronger: "no evidence of instability" from 58 % upward (V01) and "addresses the four-dimensional stability question" (V02). v2 removes both.

**Q4. Does 2610.38659 say [DFKKR13]'s "disappears" was wrong?** Refined, and about the same quantity. Same family and J-range, same merger: [DFKKR13]
"correctly located the merger, but could not follow the modes once ω² left the real axis" (A34). The "apparent loss of the radial instability
found in the original real-eigenvalue treatment is therefore not stabilization" (A04); "the merger previously interpreted as the disappearance
of the instability is an exceptional point" (A09); [DFKKR13] "suggested a restoration of radial stability" (A40). Both use the same example
\|J\|/A = 0.05475 (A23, D22) and the numbers agree (0.10063 is 0.100628 rounded, `jovera_run1.log`). "Real-eigenvalue" is [BGKKKN26]'s word; [DFKKR13]
says only that for unstable modes −Ω² is positive (D10) and fixes Ω² by an auxiliary ODE (D11).

**Q5. Where [DFKKR13] makes the claim.** In its own abstract (D01), hedged in Sec. V B (D17, D18) and restated in Sec. VI (D20). It is not
from another paper. 2610.29941 describes it as the instability disappearing "as in five dimensions" (S05; v1: V05).

## Final checks (run `bash run_controls.sh` from this folder; logs in `controls/`)

| check | result |
|---|---|
| C1 118 quotes found in their TeX (comments removed, whitespace collapsed); 5 v1-only quotes absent from v2 | pass, exit 0 |
| C2 each quote's PDF fragment found on one PDF page, numbers on that page | pass |
| C3 each sentence of the two proposed rows cites existing ids, table cell and bullets equal the sentences | pass |
| C4 sha256 of 8 committed files | pass |
| C5 numbers and C6 double-quoted strings of the sentences occur in cited quotes | pass |
| controls, each must exit 1 | `quote` 1 failure, `pdf` 1, `cite` 1, `dangling` 1, `sha` 8, `number` 2, `absent` 5, `cell` 1, `quoted` 2, `bullet` 1: all exit 1 |
| `jovera_check.py` (recompute) | exit 0; `--mutate=G1`, `p0`, `exponent`, `lam` exit 1 |

Run cost: `check_quotes.py` 0.85 s, 21 MB rss (`/usr/bin/time -v`), one process, nice 10, load average 0.3.

## Slips and what they taught

- A prediction was wrong (2 above): I expected the claim to come from another paper and did not check the abstract before the README. It is in the abstract.
- My first milestone comment said "rss < 60 MB" before I had measured it; I measured (21 MB) and corrected the comment by its id.
- Hash abbreviations typed by hand in this README's file table were wrong once (…a1da for …8da1); the table is now generated from `sha256sums.txt`.
- The `quote` control went silent when I inserted a quote ahead of the one it altered (it replaced a word the new first quote lacked); `run_controls.sh` expected rc 1, caught it,
  and the mutation now replaces the first word and fails if inert.
- The first wrap of the proposal bullets broke "second-order" at its hyphen; the diff-equals-sentences check (C3) caught it.
- A recompute (G = 1/(4π)) was not in the plan; it is labelled as a recompute here and in the proposal (R1.15).
