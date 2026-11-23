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
