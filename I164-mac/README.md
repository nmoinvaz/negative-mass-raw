# I164-mac: the coordinator's review of #164's reading of the slow-rotation and charged-wormhole papers

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/164. Reviewed raw `I164-rpi5` at 208fa2c (a reading task; no
branch, no file in the repository).

## Rerun of the runner's scripts

`bash run_controls.sh` in a copy of `I164-rpi5` (`rerun/`), with the Mac's `pdftotext` (poppler 26.11.0) and the
repository's Python. Output: `rerun_run_controls.txt`.

## Sources, fetched by the coordinator

On 2026-11-25, from arxiv.org and inspirehep.net with a generic client, into a new empty scratch folder outside this
repository. Fetched: the e-prints and PDFs of 2301.05243v1, v2, 2403.08387v1, 2510.11406v1, v2, 2607.18399v1, v2; the
arXiv API record and the abs pages of the four ids; and the INSPIRE records. Each e-print was unpacked into its own new
folder. The sha256 values are in `fetch.txt`. 2610.38659v1 ([BGKKKN26]) and 2610.29941v2 ([SN26b]) come from the
coordinator's fetch for #152 (`I152-mac/fetch.txt`).

## Independent check `ind164.py` (criteria written before its first run)

ind164 imports nothing from `I164-rpi5`. Its TeX normalization is its own, as in `I152-mac/ind152.py`: comments
dropped, `\cite`, `$`, braces, `~`, line breaks and repeated spaces removed. Its table parser and its recompute are its
own. It reads the data folder passed as its argument.

Shared with #164: the proposed text (closing comment 7151606569 and `proposal.md`), from which the strings and numbers
below are copied; the formula ω_I = ω_I^(0) + J²Δω_I^(2) and the area A = 4π r₀² e^{πC/(2r₀)}, as printed in the
sources; and the source files, which are the same bytes (P0).

Sources: L = 2301.05243 v2 (`paper8.tex`), M = 2403.08387 v1, H = 2510.11406 v2, N = 2607.18399 v2, G = 2610.38659 v1,
S = 2610.29941 v2.

| id | criterion |
|---|---|
| P0 | the 8 TeX files and 7 PDFs of the coordinator's fetch have the sha256 that `I164-rpi5/sha256sums.txt` lists |
| P1 | metadata. The arXiv API titles: L "Are slowly rotating Ellis-Bronnikov wormholes stable?"; M "Radial perturbations of Ellis-Bronnikov wormholes in slow rotation up to second order"; H "Radial perturbations of charged wormholes"; N "Nonradial perturbations of static charged wormholes" (case-insensitive). Authors: L, M Azad, Blázquez-Salcedo, Khoo, Kunz; H, N Blázquez-Salcedo, González-Romero, Khoo, Kunz, Navarro Moreno. Latest versions on the abs pages: L v2 23 Nov 2023, M v1 13 Mar 2024, H v2 13 Mar 2026, N v2 8 Oct 2026. INSPIRE journal references: L PLB 848 138349, M PRD 109 124051, H PLB 875 140335, N PRD 114 084019 |
| P2 | each quoted string of the proposed text occurs in its named source, after normalization: L "for every value of C we have studied", "merge and disappear", "slightly above 30\%", "the radial instability will disappear at even smaller values of the angular momentum", "for sufficiently rapid rotation the wormholes will be stable", "is indicating a deficiency of the applied quadratic approximation"; M "independent of C", "is slightly smaller than the angular momentum, where the two perturbatively obtained branches of unstable radial modes cross", "will need more sophisticated methods than perturbation theory", "excellent approximations for most of the range", "up to 50-60"; H "have two radially unstable modes", "merged around 1/3", "can only be confirmed by a non-perturbative study", "one might be tempted to conjecture that the radial instability disappears at the critical value", "not yet fully radially stable", "two modes that possess the same imaginary part but opposite real parts"; N "will therefore be relaxed for fast rotation", "should be clarified", "does not seem to completely vanish as long as"; G "can now be recognized as the same characteristic spectral mechanism"; S "the zero of their second-order rate for this family" and "33\%" |
| P3 | absent: "33\%" (spaces ignored) in none of L, M, H, N; "oscillating growth" and "oscillatory instability" in neither H nor N; "nearly symmetric" and "reliable range" in neither L nor M |
| P4 | re-solve from the own parse of the printed tables. Main mode from M's Table I (`ImOm_coeff_main_moreC`) and L's first table; second mode from M's Table II (`ImOm_coeff_sec`) and L's second table; A = 4π e^{πC/2} (r₀ = 1, its formula found in L). With J_c² = −ω^(0)/Δ and the crossing J_x² = −ω^(0)/(Δ − Δ_s): 8πJ_c/A at C = 1 rounds to 41.9 %; 8πJ_x/A at C = 0, 0.05, 0.1, 0.2 round to 32.6, 32.8, 32.9, 33.0 %; J_x/A rounds to 0.013 at all four; and the L and M tables agree where they share C |

Mutations, each must exit 1 with its target failing:

| mutation | change | target |
|---|---|---|
| `sha` | one hex digit of an expected sha256 flipped | P0 |
| `author` | Khoo → Kho | P1 |
| `quote` | "merge and disappear" → "merge and vanish" | P2 |
| `absent` | "merged around 1/3" required to be absent from H | P3 |
| `area` | A = 4π, without e^{πC/2} | P4 |
| `cross` | J_x² = −ω^(0)/(Δ + Δ_s) | P4 |

## Results

| file | what |
|---|---|
| `rerun_run_controls.txt`, `rerun1_controls/` | rerun 1: run from a copy at the wrong depth, so `../I152-rpi5` was missing; the quote checks crashed (a layout error of the coordinator's, not of #164's code) |
| `rerun_run_controls_run2.txt`, `rerun2_controls/` | rerun 2, from a scratch copy with the sibling layout (`I152-rpi5` beside it) |
| `fetch.txt` | the coordinator's fetch: URLs and sha256 |
| `ind164_run1.py` … `run3.py`, `.txt` | runs 1 to 3 (`ind164.py` is the same version as run 3) |
| `ind164_mut_*.txt`, `ind164_mut_cross_run1.txt` | the 6 mutations; `cross` in its first (crashed) and second form |

**Rerun 2** (exit 0): 28 of 28 runs `ok`. `check_quotes.py` passes plain: 105 records, with the PDF text from
`pdftotext` on the Mac. All 18 of its controls exit 1. `recompute_jc.py` passes, and its 6 controls fire.
`scan_ai_text.py` finds 0 hits, and its planted control fires.

**ind164.** Run 1 failed P0 as coded: the code compared 14 files, not 15. It left out [BGKKKN26]'s TeX, which
`sha256sums.txt` also lists. That is a defect of the coordinator's code; the 14 it did compare matched. Run 2 adds the
file. In run 2 the `cross` mutation crashed (the square root of a negative number) before P4 reported, so it was
**silent** there. In run 3 a missing real crossing is reported as P4's failure, and runs 2 and 3 are identical. Run 3
(exit 0):

| criterion | run 3 |
|---|---|
| P0 | 15 of 15 files have #164's sha256 |
| P1 | titles, authors, latest versions and dates, and INSPIRE journal references, as proposed |
| P2 | 23 of 23 quoted strings found in their sources |
| P3 | 12 of 12 strings absent where required: "33\%" in none of L, M, H, N; "oscillating growth", "oscillatory instability" in neither H nor N; "nearly symmetric", "reliable range" in neither L nor M |
| P4 | the L and M tables agree where they share C; the area formula is in L; at C = 1, J_c = 1.00778 and 8πJ_c/A = 41.90 %; the crossings are 32.58, 32.79, 32.94, 33.03 % at C = 0, 0.05, 0.1, 0.2, with J_x/A = 0.01296 … 0.01314 |

Re-solve: P4, from the coordinator's own parse of the printed tables. The C = 1 zero of the main mode is 41.9 % of the
extremal value, and the two-mode crossing at C = 0.2 is 33.0 %. [SN26b]'s "33 % on this axis", which [SN26b]
attributes to the C = 1 zero, matches the C = 0.2 crossing instead. [ABKK23] and [ABKK24] print no throat area
beyond the static one. A factor between the conventions could reconcile the two numbers: 41.9 % × π/4 = 32.9 %. That
is an observation, not tested here.

Also read in the TeX by the coordinator: [BGKKN26] Sec. 5.1.2 (line 791 of v2): "the fundamental l=2 b_2 branch becomes
unstable for M/r_T⪆0.3", for the uncharged Ellis–Bronnikov family. #164 lists it among its disagreements but not in the
proposal. The note carries it as a coordinator sentence.

| mutation | exit | failed | target met |
|---|---|---|---|
| `sha` | 1 | P0 | yes |
| `author` | 1 | P1 | yes |
| `quote` | 1 | P2 | yes |
| `absent` | 1 | P3 | yes |
| `area` | 1 | P4 | yes |
| `cross` (run 2) | 1 | crashed before P4 (**silent**) | no |
| `cross` (run 3) | 1 | P4 | yes |
