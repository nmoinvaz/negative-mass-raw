# I218-dh610: polar l = 1, 2 modes of the black universes, radial modes of the M-AdS wormholes

Machine: dh610-fedora (20 cores, shared with choptuik-large-d; at most 4 processes, `nice -n 10`, one thread each).
Issue: https://github.com/nmoinvaz/negative-mass/issues/218. Worktree `~/Source/negative-mass-i218`, branch `wip/i218-polar-mads`
(from main at 6760601). Code: `notes/black_universe/polar_derive.py` (derivation and its checks) and `polar.py` (numerics), in that
worktree; note `polar.md`. This README was written before the runs of record. Status words as in AGENTS.md.

## What is computed

The phantom family of #212 (`notes/black_universe/README.md`; units b = 1, R² = ρ² + 1, φ′ = √2/R², A(ρ; c), 3m = −2c/π):

- **polar (even-parity) modes, l = 1 and l = 2**, e^{Wt} Y_l(θ), of the 20 members c = −10 … −0.01 of #212 and of the Ellis wormhole
  (c = 0): the number of growing modes (real W in [0.01, 8] per b);
- **radial modes of the M-AdS wormholes** (c > 0), Dirichlet at the AdS end, W in [0.01, 24] per b, at 12 values of c.

Gauge. l ≥ 2: Regge–Wheeler (H0, H1, H2 = H0, K, δφ = F): complete, regular where φ′ ≠ 0 and R ≠ 0, so no singular point at the throat
(the δR = 0 gauge of [BKZ12] has one at R′ = 0). The first-order system is 4-dimensional in (H0, H1/W, K, F) and linear in W². l = 1: h_tA = h_ρA = h_tρ = 0, a
3-dimensional system in (H0, H2, F) with one pure-gauge solution g(ρ) known in closed form; the determinant is det[L | R | g]. Radial: the
δφ = 0 gauge and the equation of #212. At a horizon the RW fields are singular like z^(W/A′ ∓ 1) (gauge, not solution); the ingoing solutions are Frobenius
series of the Fuchsian system obtained with F = F̃/z (l = 2) and H2 = z H̃2 (l = 1).

## Methods

- **Shooting** (`polar.py count`, `mads`). Right: Gram–Schmidt-orthonormalized frame from ρ_far = max(rmax0, rmaxW/W), dominated by the decaying
  solutions on inward integration (2 columns for l = 2, 1 for l = 1). Left: ingoing Frobenius frame at the horizon (exponents 1 + W/A′, −1 + W/A′ for l = 2;
  W/A′ for l = 1), or the second infinity at c = 0. Determinant of the frames at the matching point ρ_m (1.0, or ρ_h + 1 when ρ_h ≥ 0.5, or 0 at c = 0).
  Real roots: sign changes on a log grid in W plus Brent; even-multiplicity roots (the Ellis polar fields are degenerate) as interior minima of |D|
  below 1e-3 of both neighbors, refined by a bounded search and counted twice. The range searched is W in [0.01, 8] (polar), [0.01, 24] (M-AdS).
- Two resolutions, R1 and R2 (same code, tighter settings):

| | rtol | rmax0 | rmaxW | W grid (polar) | W grid (M-AdS) | Frobenius z0, terms | M-AdS δ, AdS start |
|---|---|---|---|---|---|---|---|
| R1 | 1e-9 | 150 | 30 | 60 | 70 | 0.04, 10 | 0.3, 1× |
| R2 | 1e-12 | 300 | 45 | 150 | 176 | 0.03, 12 | 0.2, 2× |

- **Independent checks.** (i) M-AdS: Chebyshev collocation of the Y-form on [x_L, X] (`polar.py spectral`, N = 240, X = 40 and N = 360, X = 60); it shares the
  background A and the Y-form coefficients and nothing of the AdS series, the throat crossing, the matching or the root search. (ii) Ellis l = 1, 2: the master equations
  of [ABCKY23] by two other 1D codes (shooting; complex-scaled eigenvalue problem). (iii) The derivation is checked in sympy (`polar_derive.py check`), including a pure-gauge
  identity and the published equations.

## Criteria (declared before the runs of record; coded as worded)

**A. Derivation** (`polar_derive.py check`, exit 0; every line PASS). D1 background residual 0 (sympy) and V of the family against stability.py to 1e-30;
D2 pure-gauge perturbation satisfies the linearized equations (8 residuals 0); D3a–e RW reduction: traceless equation H2 = H0, tt = rr = trace-angular
equations are one algebraic relation, constraint propagation, the four second-order equations vanish on the 4-system, matrix polynomial of degree 1 in W²;
D4a the Ellis limit reproduces [ABCKY23] (44)–(46); D4b the printed (47) differs from the derived u′ by exactly K(ℓ+2)(ℓ−1)/2 (recorded, not corrected); D5a, b F decouples at c = 0
and Z = R F obeys Z″ = (V + W²)Z with V = L/R² − 3/R⁴, the printed (52), (53); D5c with (47) as printed F does not decouple (added, see Amendment 1); D6a–c the l = 1 system is consistent and the pure-gauge solution solves it;
D6d at c = 0 the gauge-invariant scalar of l = 1 obeys χ″ + (2ρ/R²)χ′ − W²χ = 0, i.e. Z″ = (1/R⁴ + W²)Z; D6e 1/R⁴ = w² − w′, 2/R² − 3/R⁴ = w² + w′ with w = −ρ/R²
(Darboux partners); D6f w is regular on the real line and w → 0 at both ends, so the map keeps the quasinormal-mode conditions; D7 the coefficient table in `polar.py` equals the
derived matrices to 1e-12 at 6 random points.

**B. Planted cases** (`polar.py planted`, exit 0).

| id | what | reference | declared tolerance |
|---|---|---|---|
| P2 | Ellis polar l = 2, 3, 4 quasinormal modes ω r0, derived 4-system, complex W on the rotated contour (θ = 0.5) | [ABCKY23] Table 1, row M/r0 = 0: 1.74 − 0.305i, 2.95 − 0.410i, 4.08 − 0.449i | \|ΔRe\| ≤ 5e-3, \|ΔIm\| ≤ 5e-4 (half a unit of the last printed digit) |
| P3a | Ellis polar l = 1 quasinormal mode of the derived 3-system (with g) | the mode of [ABCKY23] (52), (53) at L = 2 by 1D shooting, start 0.6814 − 0.6177i | \|Δω\| ≤ 1e-7 |
| P3b | same | the mode of the same master equation as an eigenvalue of the complex-scaled operator (θ = 1.1, X = 60, N = 20000, Richardson in h²) | \|Δω\| ≤ 1e-8 |
| P4 | Ellis at the unphysical L = −1: the double roots of the polar determinant, W in [0.2, 8], R1 | bound states W of the master equation by finite differences (X = 400, N = 160001, Richardson) | relative 5e-5, same number, no sign change |
| P5 | M-AdS radial mode as c → 0⁺: W²(c) − 1.39705243433350684 for c = 1e-4, 1e-3, 1e-2 (R1), quadratic extrapolation to c = 0 | the Ellis value of `../wormhole_largeD/w2_output.txt`, #212's plant | extrapolated intercept ≤ 1e-8 |

l = 1 has no published number: [ABCKY23] say only that l = 1 "corresponds to the scalar branch" of [BCK18] (figures only) and print its equation (69). The coordinator ruled (2026-11-27,
by hc) that P3a, P3b and the symbolic checks D6c–f (the pure-gauge solution, the Darboux relation with w regular and → 0 at both ends) are the planted case for l = 1, and asked for the
control `l1_pot` (the test-scalar potential 2/R² + 1/R⁴ in place of the master equation) to miss P3. The l = 2 plant is P2.

**C. Counts.**
- Polar (`polar.py count`, R1 and R2, `polar.py report`): 21 members × l = 1, 2. Criterion: the same count at R1 and R2, and the determinants at W = 0.01, 0.1, 1, 3, 8 agree to
  a relative 1e-6 (development: 2e-9 at worst). The count of record is `n_roots`.
- M-AdS: c = 1e-4, 1e-3, 1e-2, 0.03, 0.1, 0.2, 0.5, 1, 2, 3, 5, 10. Criterion: same count at R1 and R2, rates within 1e-6 (relative), the relative imaginary part of Y after the throat arc ≤ 1e-6
  (no logarithm). Spectral check (`polar.py spectral`): the same count; for c ≥ 0.01, |ΔW|/W ≤ 2e-3 (N = 240) and ≤ 2e-4 (N = 360); no complex eigenvalue with Re λ > 1e-4;
  for c < 0.01 only the count is compared (the AdS end is at |ρ| > 70 and the finite domain does not resolve it: development gives 6e-2 at c = 1e-4).
- No statement is made about complex W for the black universes (Sec. "What this does not cover" of the note).

**D. Controls** (`polar_derive.py controls`, `polar.py controls`; each is computed in a development run, below, before it is declared; every `--mutate=` must fire on its target).

## Controls and their development outcomes

`polar_derive.py controls` (`dev/derive_controls_dev1.log` for the first eight, `dev/derive_controls_dev3.log` for the final list; checks in `dev/derive_check_dev3.log`, 19 PASS lines, no FAIL):
`bg_V` fires D1 and D1b; `lin_sign` fires D2; `ang_L` was silent on its first target D2 (the pure-gauge identity does not depend on the angular eigenvalue) and is retargeted to D4a, where it
fires; `alg_coef` fires D3c; `ellis_sign` fires D4a; `pot` fires D5b; `l1_gauge` fires D6c; `susy` (wrong sign of the superpotential) fires D6e; `susy_end` (w = −ρ/R, not → 0) fires D6f; `code` fires D7; `print47` (the derived row in place of the printed one, Amendment 1) fires D5c (`dev/derive_check_print47_dev4.log`; the unmutated check, `dev/derive_check_dev4.log`, has 20 PASS lines, no FAIL).

`polar.py controls` (`dev/controls_dev2.log`). A "count" control must change the count of its member at R1; the others must make their target check FAIL.

| mutation | what it breaks | development outcome |
|---|---|---|
| `L_sign` | l(l+1) → −l(l+1) in the l = 2 system | c = −0.3: 23 against 0 |
| `hz_out` | outgoing instead of ingoing Frobenius exponents at the horizon, l = 2 | c = −1.5: 3 against 0 (at l = 1 it aborts with the recursion check at half-integer W/A′: a clean refusal, not used as a control) |
| `rmax` | far boundary at ρ = 4 | l = 1, c = −0.3: 6 against 0 |
| `g1_wrong` | third column of the l = 1 determinant is (0, 1, 0) instead of the pure-gauge solution | l = 1, c = −1.5: 3 against 0. The first version (H0 and H2 of g exchanged) was **silent** (0 against 0) and is replaced |
| `scan_range` | M-AdS W range starts at 3 | c = 0.5: 0 against 1 |
| `ads_bc` | the non-normalizable AdS condition Y = ρ in place of Y → 1 | c = 0.5: count 1 against 1 (W 1.7098 → 1.5761): **silent as a count control** and silent on P5 (the c → 0⁺ limit does not see it); fires on the spectral check, 8.5e-2 against 2e-3 (target S6) |
| `qnm_L` | l(l+1) + 1 in the Ellis QNM | P2 fails: 1.982217 − 0.335140i against 1.74 − 0.305i |
| `l1_pot` | test-scalar l = 1 potential 2/R² + 1/R⁴ in place of the master equation at L = 2 | P3a and P3b fail |
| `spec_sign` | sign of the potential term in the collocation | S6 fails (no eigenvalue) |

## What `dev/` holds

Logs of every development and stopped run (`*.log`, `*.err`), the development result files (`json/`; some were overwritten by a naming slip in the M-AdS development loop and rerun, the
R1/R2 M-AdS files are the rerun's), my exploration scripts (`scripts/`: the first derivations, the sympy reductions, the QNM searches, the timing tests), and the two source texts read for the
published values (`literature/`: the TeX source and the PDF text of arXiv:2212.12601 as downloaded 2026-11-27; the parser used to read the plotted points of the EPS figures of arXiv:1806.03282).

## Development history

- **Ruling on l = 1** (hc, 2026-11-27): see above.
- The first controls run (`dev/polar_controls_dev1.log`) used the earlier control list and was stopped at its qnm_L step; the list above supersedes it.
- First attempts at the l = 1 comparison with a root finder on |D| ran off to |ω| → ∞ (the vectors are normalized, so D → 0 numerically); a QNM with arg ω below the contour angle θ is not
  found at all (the l = 1 mode has arg ω = −0.73, θ = 0.5 was too small). Fixed by θ = 0.9 (shooting) and by a complex-scaled eigenvalue code (θ = 1.1); the early scripts are not kept.
- The first R2 runs at l = 2 took minutes per determinant (a frame spanning more than 30 e-folds per chunk at the horizon, and absolute tolerance 1e-30 on a unit-norm frame); stopped, fixed
  (geometric chunks near the horizon, atol = 0.1 rtol); the stopped runs' logs are in `dev/polar_dev_l*.log`.
- M-AdS: the first development range W ≤ 8 lost the mode at c = 5 (W = 8.06); the range is [0.01, 24] and c = 10 (W = 15.2) is included.
- The Ellis polar spectrum is two-fold degenerate (two identical master equations), so the determinant has double roots there and a sign-change search is blind to them
  (development: D ∝ (W − W0)² at the bound state of L = −1). Hence the dip search and plant P4.
- The independent eigenvalue code at θ = 0.9 and X = 40 differed from shooting by 5e-6 (the outgoing solution decays slowly along the contour); θ = 1.1, X = 60 agrees to 1e-9.

## Amendments

1. (2026-11-27, after the declaration, before the derivation's runs of record and after the counts of record had started) Check D5c and its control `print47` were added to `polar_derive.py`: the printed
   (47) of [ABCKY23] does not decouple the scalar at c = 0, which D4b only implies. Development: D5c passes, `print47` fires it. The polar and M-AdS runs are unaffected (they do not import it).
2. (after the runs of record, no criterion changed) The spectral run of record crashed at c = 10 (`logs/spectral_run1_crash_c10.txt`): the bracket for ρ(x) at x > 0 assumed ρ(x) < x + 10, false
   where A > 1 (large c). Fixed. The second run (`logs/spectral_run2_window100_c10_fail.txt`) found no eigenvalue at c = 10: the eigenvalue window was λ < 100, narrower than the declared range
   W ≤ 24 (λ < 576). Fixed to the declared range. The third run (`logs/spectral.txt`) passes everywhere except S-B at c = 10, 5.9e-4 against the declared 2e-4: **not met**, reported. The `report`
   header printed the polar W range for the M-AdS table; text only, fixed. Code at the runs of record: counts (`results/`), planted, polar controls and derive check/controls at `polar.py` of commit
   7dcd80c (identical in e8696be, which added only `polar_derive.py` D5c); spectral and report at 23c2165 (the final `polar.py`).

## Results of record

Code `wip/i218-polar-mads` at 4c8c5ca (code 23c2165; 4c8c5ca adds the note and the assembled outputs). Runs (all exit 0 unless stated; `logs/`): 84 polar counts (`results/polar_l<ell>_<c>_<res>.json`; R1 and R2, 21 members, l = 1, 2) and 24 M-AdS counts
(`results/mads_<c>_<res>.json`), run by `run_polar.sh`, `run_mads.sh` (units `nm-i218-rec-*`), 84 min of CPU in total; `planted.txt` (7 PASS); `report.txt`; `spectral.txt` (exit 1: one tolerance not met, above);
`controls.txt` (9 of 9 fire); `derive_check.txt` (20 PASS); `derive_controls.txt` (11 of 11 fire). The tables and the note: `notes/black_universe/polar.md`; the outputs of record assembled
in `polar_output.txt` and `polar_derive_output.txt` there.

- polar l = 1, 2: 0 growing modes at every member, R1 = R2, determinants agree to 5.1e-9; no interior minimum of |D| anywhere.
- M-AdS: 1 growing mode at each of 12 values of c in [1e-4, 10], W = 1.1820485273 … 15.2213845506 per b.
- Planted: P2 (2.3e-3, 1.4e-4 / 2.4e-3, 1.6e-5 / 3.7e-3, 1.1e-4 against 5e-3, 5e-4), P3a 1.5e-12, P3b 2.8e-11, P4 0.421976 and 1.473675, P5 3.1e-10.
