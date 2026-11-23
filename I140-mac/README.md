# I140-mac: the coordinator's review of #140's window helper and split v_c

Machine: macOS (the coordinator's Mac, arm64), Python 3.14, numpy 2.5.4, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/140. Reviewed branch `wip/i140-window-vc` at 93ed6d1, raw
`I140-rpi5` at 06060fe. This machine is the acceptance's second machine.

## Independent check `ind140.py` (criteria written before its first run)

ind140 shares no code with `retab.py`, `drive_part_tanh.py`, `tanh_spectrum.py` or `I96-rpi5/sector_numbers.py`. It shares
the stored arrays (`I96-win/eig` for σR = 8, `I96-dh610/eig` for σR = 16, `I75-dh170` for σR = 2 and 4; μ = muA·vc as stored)
and the definitions: the cut is the modulus of the first eigenvalue of A, by decreasing modulus, above 10⁻³ with no
eigenvalue of B within 10⁻⁵ relative; the window is |μ| ≥ cut. It compares moduli exactly, |μ|² as the square of the
floats' rational values, so no modulus routine enters a count.

| id | criterion | kind |
|---|---|---|
| W1 | in each of the 22 sectors, the window counts of A and B and the cut to 4 decimals equal `I140-rpi5/retab_rpi5.csv` | exact counts |
| W2 | totals A / B: 262 / 284 at σR = 8 and 194 / 216 at σR = 16; the 8 changed rows of the closing comment have A windows 26, 18, 18, 18 (σR = 8, m = 7/2, 13/2, 15/2, 17/2) and 22, 18, 18, 14 (σR = 16, m = 1/2, 7/2, 11/2, 15/2) | exact counts |
| W3 | in every sector the eigenvalues of A with exactly the cut's modulus are the cut's eigenvalue and its conjugate, and no other modulus is within 1.9e-12 of the cut | exact |
| W4 | in every sector the strict window \|μ\| > cut holds exactly 2 fewer eigenvalues of A | exact |
| W5 | the symmetry value max over the window of min \|μ_A + z\|/\|z\| equals `retab_rpi5.csv`'s to 2 digits in all 22 | numerical |
| W6 | supplement, `I75-dh170`: totals A / B 654 / 676 at σR = 2 and 406 / 424 at σR = 4 | exact counts |

Mutations, each must exit 1 with its target failing: `tol4` (match tolerance 10⁻⁴; W1), `strict` (window \|μ\| > cut;
W1, W2, W4), `pair` (the conjugate of the cut's eigenvalue removed from A at σR = 16, m = 15/2; W3).

The Mac rerun of `retab.py --tag=mac` and its csv diff with rpi5's is the acceptance's "identical on two machines".

## Results

| file | what |
|---|---|
| `rerun/` | `retab.py --tag=mac` and its 3 mutations, `tanh_spectrum.py --part=window` and `--mutate=abscut`, `tanh_spectrum_check.py --part=vc` and `--mutate=nosplit`, at nice 10 (`runA.sh`, `runA.log`) |
| `ind140_run1.py`, `.txt` | the independent check (`ind140.py` is the same version) |
| `ind140_mut_*.txt` | its 3 mutations |
| `diag_w3.py`, `.txt` | the margin in retab's units, written after W3 failed |

**Second machine.** `retab_mac.csv` equals `I140-rpi5/retab_rpi5.csv` (`diff` empty): the acceptance's "identical on the two
machines" holds on arm64 macOS and aarch64 Linux. retab's text output differs only in the header and the column of the sign
of np.abs(array) − abs(scalar) at the cut. `--mutate=abscut` exits 1 on the Mac in 7 sectors (σR = 8, m = 7/2, 13/2, 15/2,
17/2; σR = 16, m = 1/2, 7/2, 11/2), on rpi5 in 6. The scalar path depends on the machine, as #96 found. `nearcut` and
`notie` give the same csv as on rpi5. `--part=window` passes and `abscut` fails `window_scalar`. `--part=vc` equals
`tanh_spectrum_check_vc_output.txt` apart from the wall time, and `nosplit` fails at σR = 16 only (−9.7e-6).

**ind140 run 1** (exit 1, W3):

| criterion | run 1 |
|---|---|
| W1 | the 22 windows of A and B and the cuts equal retab_rpi5.csv |
| W2 | totals 262 / 284 (σR = 8) and 194 / 216 (σR = 16); the 8 changed rows as listed |
| W3 | **FAIL**. The tie half passes: in 22 of 22 sectors the cut's modulus is held by exactly its eigenvalue and its conjugate. The margin half fails: the smallest absolute margin is 1.92e-13, against 1.9e-12. #140's 1.9e-12 is relative, \|ab − cut\|/cut (I140-rpi5 README A4), which this criterion did not say. `diag_w3.py` gives 1.871e-12 relative at σR = 16, m = 5/2 and 2.215e-11 at σR = 8, #140's values. A defect of the criterion; it stays failed |
| W4 | the strict window holds exactly 2 fewer in every sector |
| W5 | the symmetry values equal retab's to 2 digits in all 22 |
| W6 | supplement: 654 / 676 (σR = 2), 406 / 424 (σR = 4) |

Re-solve, σR = 16, m = 15/2 (the sector where the two machines' logs disagreed): cut 0.094693747166, window A 14, B 16, tie
group 2, margin 2.51e-12 absolute, symmetry 4.0e-11.

| mutation | exit | failed | target met |
|---|---|---|---|
| `tol4` | 1 | W1, W2, W3, W5, W6 | yes |
| `strict` | 1 | W1, W2, W3, W4, W5, W6 | yes |
| `pair` | 1 | W1, W2, W3 (tie group in 21 of 22), W4 | yes, on W3's tie half |

**Findings on #140.** No discrepancy with #140's numbers. One wording point: the closing comment gives the margin
"≥ 1.9e-12" without saying it is relative to the cut.
