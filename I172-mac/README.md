# I172-mac: logs of notes/warp/conical_closure.py (closure on the conical family's asymptotic series)

Machine: the coordinator's Mac (Apple M5, macOS, shared with other agents), Python 3.14 of `~/Source/negative-mass/.venv`
(sympy 1.14.0, mpmath 1.3.0), nice 10, at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/172.
Branch `wip/i172-conical-closure` at origin/main 3384b61, worktree `~/Source/negative-mass-i172`. Written 2026-11-28, before
the first run of record. Stop condition: a single run not finished after 2 h of wall time is stopped and reported. Memory is
reported, never a stop condition.

## Question

#159 (`conical_limit.md`): for every real F_inf != 0 the ODE N = 8 rho^6 det R3 = 0 of `det_classify.md` section 6 has the
two-parameter family F = F_inf - 2 F_inf/eta^2 + (C + F_inf (F_inf^2 + 7) ln eta)/eta^4 + ... for u = F(x/rho), eta = x/rho
(#168 proves the attraction and that the series is the expansion; #167 found no global member). There R = a a - b b with
real a, b where det R3 = 0, h > 0 and the Schur entry S11 < 0. Closure of `two_scalars.md` (some chi with e^chi k and e^-chi m
closed, k = a + b, m = a - b) needs k ^ dk = 0 and m ^ dm = 0 (`bessel_closure.md` section 1, proved). Closure is local, so
it fails on the region eta > eta_0 if k ^ dk or m ^ dm is nonzero there. Find the lowest order in 1/eta at which either is
nonzero, as a function of (F_inf, C), with its zero set; or show both vanish to every order computed.

## What was explored before this README (not of record)

1. By hand. In the coframe th0 = dt, th1 = dx + u dt, th2 = d rho the Ricci tensor is R = R3_ab th^a th^b with
   R3 = [[A, Q, Z], [Q, B, Y], [Z, Y, h]] (`det_classify.md` Setup; the own Ricci tensor reproduces it, `ricci`). Completing
   the square at h: R3(xi, xi) = h L2(xi)^2 + S00 xi0^2 + 2 S01 xi0 xi1 + S11 xi1^2 with L2 = (Z/h, Y/h, 1) and the Schur
   entries S. On D = det R3 = 0 the Schur block has rank 1, so R3(xi, xi) = h L2^2 + S11 L1^2, L1 = (S01/S11, 1, 0), and with
   w^2 = -S11/h > 0 the two null covectors are L2 +- w L1 (unique up to k -> lam k, m -> m/lam and a swap).
   Normalization: k = u_rho (L2 + w L1), m = u_rho (L2 - w L1), so that both have th2-component u_rho (k m = 2 R(xi, xi)); this
   is the normalization of `bessel_closure.md` (k = sqrt2 (a + b), gamma = g'), where O_k + O_m = 2 g'(g'^2 + 4 c^2). O is
   quadratic in the covector, so the sign of u_rho is irrelevant, and a rescaling by a function lam changes O to lam^2 O: zero
   or nonzero is normalization free, the order and the coefficient are not.
2. By hand. With coordinate components (a0 + a1 u, a1, a2) of a0 th0 + a1 th1 + a2 th2 and Wd(a, b) the coefficient of
   dt ^ dx ^ d rho in a ^ db: for k' = L2 + w L1, k' ^ dk' = E + w B, m' ^ dm' = E - w B with
   E = L2 ^ dL2 + w^2 L1 ^ dL1, B = L2 ^ dL1 + L1 ^ dL2 + L2 ^ d(w^2) ^ L1/(2 w^2) (using dw = d(w^2)/(2w)). So
   O+ = k ^ dk = 2h (E + w B), O- = m ^ dm = 2h (E - w B), O+ + O- = 4 h E, all rational in the jets of u except for w.
3. By hand. For u = F(x/rho) everything is homogeneous: rho^2 R3 depends on eta alone; F' = nu p, F'' = nu^2 (q - p) with nu =
   1/eta, p = theta F, q = theta^2 F, theta = eta d/d eta. A function f(eta) has d/dx f = (nu theta f)/rho and d/d rho f =
   -(theta f)/rho. So rho^3 O is a Laurent series in nu with powers of T = ln eta when F is the series of #159.
4. Scratch runs in the scratchpad, kept here as `scratch_explore_p1.py` ... `scratch_explore_p7.py` and
   `scratch_explore_lser.py` (they import pickles of the series that are not kept; they are not of record). `p1`: own Ricci tensor
   of a generic u(x, rho) against the printed block. `p2`: the same obstruction as exact jets with sympy `together`; it was stopped
   by hand after 3 min (too slow) and replaced by the series route. `p3`-`p5`: the series route; at (F_inf, C) = (1, 0) the
   first run gave E = (-24 + 32 T) nu^2 + ..., B = -8 nu + ...; with symbolic (F_inf, C) and K = 9 it gave rho^3 O+ = -64 F_inf^3
   nu^4 + O(nu^6 ln eta), rho^3 O- = 64 F_inf nu^4 + O(nu^6 ln eta), the same at K = 4, 6, 13. `p6`: with a_{4,0} = C and
   a_{4,1} = Bb both free at K = 4 the nu^4 coefficient of O- is 64 F_inf (no C, no Bb) and of O+ is 16 (Bb - 5 F_inf^3 - 7
   F_inf), which is -64 F_inf^3 at Bb = F_inf (F_inf^2 + 7). `p7`: the Bessel family through the same E, B: on the ODE
   E = (g'^2 + 4 c^2)/g', w^2 = (g'^2 + 2 c^2)/g'^2, so 4 h E = 2 g'(g'^2 + 4 c^2), as #162.
   So the leading coefficients below were known when the criteria were written; what the criteria can still do is fail when
   the pipeline, the series or a coefficient is wrong, and the controls below show that they do.
5. A first run of the draft script, `dev_01_baseline.log` (11 of 11 checks pass, 75 s), then the controls of `dev_02_*` (one
   run per mutation, to compute each mutation's effect before it is declared). The draft is the script of record unchanged
   unless an amendment below says so. The edits after `dev_01`, all before any run of record: the numerical tolerances were set
   from the probes below (1e-9 -> 1e-8 for `jets_num` and `coord_num`, 1e-9 -> 1e-12 for `mirror`); K = 17 was added to the
   truncation list of `truncation` (no flag); `series_resid` prints the lowest nonzero order of the determinant. The three
   controls that this changes (`ser-b8`, `ser-a2`, `trunc-b`) were rerun as `dev_04_*`.

## Notation and imports

Coordinates (t, x, rho, phi); eta = x/rho, nu = 1/eta, T = ln eta; O+ = k ^ dk and O- = m ^ dm are the coefficients of
dt ^ dx ^ d rho (the d phi components vanish since nothing depends on phi and k has no d phi part). `rho^3 O` denotes the
function of eta with the rho^-3 stripped (O has weight rho^-3). Series have coefficients in Q(F_inf, C, Bb) (`Bb` only for the
sensitivity run), powers nu^n T^j, and carry the first order that is not known; the product, the inverse and the square root
propagate it. The formal series of F is generated by `conical_limit.formal_series` (read-only import) applied to this file's own
N (8 det of the hats, compared with `det_classify.conical_N()` and with the typed A0 + nu^2 A1 + nu^4 A2 in `ricci`). Imported,
read-only: `conical_limit` (the series solver and the typed theta-form), `det_classify.conical_N` (a comparison target).
Not imported: `two_scalars` (no exact jet on the family is available, see "Not tested"), `bessel_closure`. Own code: the Ricci
tensor, the frame block, the null pair, the Frobenius coefficients, the series arithmetic, the integration and the numerical
differentiation. Output is stdout only; each run is logged in this folder, reruns are numbered.

The same functions `pair` (the null pair of a block R3) and `EB` (E and B for any calculus with d/dx and d/d rho) serve every
check: exact sympy for the planted cases, exact jets in `jets_num`, series in `obstruction`.

## Checks and criteria (each is a `check(name, ok, detail)`; the script exits 1 if any fails)

Planted truth first (`planted_bessel`, `planted_pairs`), then the family. Thresholds were fixed after the probes below and are
not changed after the first run of record. A failed check is reported as a result; no threshold is loosened after a run of record.

| id | name | pass criterion | kind |
|---|---|---|---|
| C1 | `ricci` | the own Ricci tensor of a generic static u(x, rho) has the frame block [[P - h, Q, Z], [Q, -P - h, Y], [Z, Y, h]] with P = -(u u_xx + u_x^2), Q = -(u_rr + u_r/rho)/2, Z = u_xr/2, Y = u u_xr/2 + u_x u_r, h = u_r^2/2 exactly, and R(e_phi, .) = 0; for u = F(x/rho) the hats rho^2 R3 are the hand entries P = -(F'^2 + F F''), Q = -eta w/2, Z = -w/2, Y = -(eta F'^2 + F w/2), h = eta^2 F'^2/2, w = F' + eta F''; 8 det of the hats equals `det_classify.conical_N()` and its theta-form equals A0 + nu^2 A1 + nu^4 A2 | exact |
| C2 | `factor` | for a symbolic block, R3 - (h L2 L2 + S11 L1 L1) = diag(D/(h S11), 0, 0) and h (L2 + wL1)(L2 - wL1) = R3(xi, xi) - D xi0^2/(h S11); the coefficient of k ^ dk from a direct sympy derivative of the explicit covector L2 +- w L1 equals E +- w B at 2 or more of 4 exact points of a polynomial shift | exact |
| C3 | `planted_bessel` | through `pair` and `EB` with u = c x + g(rho), own Ricci, on the ODE g'' + g'/rho = eps (g'^2 + 2 c^2) for eps = +-1: 4 h E = 2 g'(g'^2 + 4 c^2) exactly, w^2 = (g'^2 + 2 c^2)/g'^2 exactly, and at 5 exact jets (c, g', rho) = (2, 1, 5/7), (6, 17, 5/7), (3, 7/2, 2/3), (-6, 7, 3/11), (-2, 1, 4/39), both eps, {O+, O-} = {O_k, O_m} of `bessel_closure.md` | exact |
| C4 | `planted_pairs` | through the same functions with u = c x + g(rho): the closed pair (a, b) = (d rho, dt) gives (O+, O-) = (0, 0); the boosted closed pair k = e^-chi d(t + x + rho), m = e^chi d(t - x + rho^2/2), chi = c x + g, gives (0, 0); the non-integrable (dt, x d rho) gives {O+, O-} = {-2, 2}, the value predicted from 2 (m_rho/k_rho) O(k) and 2 (k_rho/m_rho) O(m) with O(k), O(m) by direct derivatives | exact |
| C5 | `series_resid` | the K = 13 series: the determinant of the hats of R3 has no nonzero coefficient below its known order, and that order is at least nu^18; h has valuation 4 with leading coefficient 8 F_inf^2, S11 valuation 2 with leading coefficient -2 F_inf^2, w^2 valuation -2 with leading coefficient 1/4 (so h > 0, S11 < 0, w^2 > 0 for every real F_inf != 0) | exact |
| C6 | `obstruction` | the K = 13 series of rho^3 O+ and rho^3 O-, with F_inf and C symbolic: no term below nu^4; the nu^4 terms are exactly -64 F_inf^3 and +64 F_inf, with no log and no C; the sum's nu^4 coefficient is -64 F_inf (F_inf^2 - 1) and the difference's is -64 F_inf (F_inf^2 + 1); known below nu^14 | exact |
| C7 | `truncation` | the series through nu^4, 6, 9, 13, 17 give O+ and O- known below nu^(K+1) and equal to the K = 13 ones wherever both are known; with only a_{2,0} = -2 F_inf, a_{4,0} = C, a_{4,1} = Bb free and nothing beyond nu^4, the nu^4 coefficient of O- is 64 F_inf and of O+ is 16 (Bb - 5 F_inf^3 - 7 F_inf), which is -64 F_inf^3 at Bb = F_inf (F_inf^2 + 7) | exact |
| C8 | `zero_set` | the real zeros of -64 F^3 and 64 F are {0} (outside the family, F_inf != 0); of the sum -64 F (F^2 - 1) they are {-1, 0, 1}; of the difference -64 F (F^2 + 1) they are {0}; at F_inf = +-1 the pair is (-64, 64) and (64, -64) | exact |
| C9 | `jets_num` | N = 0 (own N) integrated inward by `mpmath.odefun` (tolerance 1e-24, degree 12, 40 digits) from the K = 13 series at eta = 1000 for (F_inf, C) = (1, 0), (-1, 2), (1/3, -1), (2, 1/2); F''' from the implicit derivative of N = 0; O+ and O- from the exact-jet formula agree with the K = 13 series of C6 to 1e-8 relative at eta = 200 and 100 | numerical evidence |
| C10 | `coord_num` | k = u_rho (L2 +- w L1) built numerically from u(x, rho) = F(x/rho) (the K = 13 series, exact derivatives, rho = 1/2) and k ^ dk from `mpmath.diff` of its components at 40 digits agree with the series of C6 (times rho^-3) to 1e-8 relative at eta = 200 and 100, same four cases | numerical evidence |
| C11 | `mirror` | F(-x/rho) at -x gives the same unordered pair {O+, O-} as F(x/rho) at +x to 1e-12 relative, for three (F_inf, C) at |eta| = 200, 100 (the isometry (t, x) -> (-t, -x) keeps dt ^ dx ^ d rho and the th2 normalization) | numerical evidence |

`obstruction` is the answer: rho^3 O+ = -64 F_inf^3 eta^-4 + O(eta^-6 ln eta) and rho^3 O- = 64 F_inf eta^-4 + O(eta^-6
ln eta), nonzero for every real F_inf != 0 and every C. If C6 fails the answer is whatever the printed series is, reported as it
stands; the other checks say whether to trust it.

The sum -64 F_inf (F_inf^2 - 1) vanishes at F_inf = +-1: a criterion built on O+ + O- alone (as in the Bessel case, where it
is 2 g'(g'^2 + 4 c^2)) would see a zero there at this order. Closure needs both O+ = 0 and O- = 0, and each is nonzero there
(C8). In the same spirit as the R3 note of the review of #162, the criteria name every factor: the coefficients -64 F^3 and
64 F have the sign of F^3 and F, not a positive sign.

## Probes (one minute each, before the criteria were fixed; `dev_01_baseline.log`)

| parameter | declared | what the probe gave |
|---|---|---|
| K of the run of record | 13, with K = 17 in `truncation` | `formal_series` through nu^13 takes 24 s (K = 9: 4 s); the truncation check with K = 4, 6, 9, 13, 17 took 181 s on a shared CPU (`dev_03_k17.log`, K = 17 agrees with K = 13); det of the hats known to nu^20, O+ and O- to nu^14 |
| nu order at which det of the hats must vanish | at least nu^18 | known to nu^20 and zero |
| planted Bessel jets | 5 jets, both eps | O+, O- = (677/15, -167/15), (1595569/95, -196979/95), (38507/88, -8785/88), (-763, 3465), (0, 34) at eps = +1, the table of `bessel_closure.md` |
| planted pairs | 3 | (0, 0), (0, 0), {2, -2} |
| exact points for `factor` | 4 points, at least 2 with w^2 > 0 | all 4 have w^2 > 0 and h != 0 |
| odefun | tolerance 1e-24, degree 12, 40 digits | 37 s for 4 cases x 2 end points; worst relative difference to the series 6.05e-11 (at eta = 100, F_inf = 2; at eta = 200 it is 1.2e-13, so it is the truncation of the series, which falls as nu^10) |
| `mpmath.diff` at 40 digits | rho = 1/2, eta = 200 and 100 | worst relative difference to the series 3.3e-10 (eta = 100, O+ at (1/3, -1), where F_inf^3 = 1/27 makes O+ small); at eta = 200 the worst is 9.5e-13 |
| numerical thresholds | 1e-8 for C9, C10 | the margins are x165 and x30 over the probes; the first draft had 1e-9 (margin x3 in C10) and was relaxed to 1e-8 here, before any run of record |
| mirror | 1e-12 | relative difference 0.0 at all 6 points (the numerics are the same operations with signs flipped) |

## Controls (`--mutate=NAME`) and their computed effects

Each mutation is local to its target check (it changes that check's input, not the shared functions), so it must fail its
target and no other check. `dev_02_<name>.log` (15 runs on the draft, all exit 1 with only the target failing) and
`dev_04_<name>.log` (the three that call the series or the truncation list, rerun after the K = 17 edit) hold the computed effects below. Controls
whose target is not a numerical check run with `--skip-num`, so they do not test that the numerical checks are untouched;
the baseline run holds those.

| mutation | target | what it changes | computed effect |
|---|---|---|---|
| `ric-ysign` | `ricci` | Y of the printed block and of the hats is built as u u_xr/2 - u_x u_r | block comparison False, hand entries False, 8 det = `conical_N` False, theta-form False; the e_phi row stays True |
| `fac-pivot` | `factor` | L1 = (S01/S00, 1, 0) in place of (S01/S11, 1, 0) | the identity with diag(D/(h S11), 0, 0) False, the product identity False; the direct-derivative test uses the unmutated pair and stays True |
| `eb-cross` | `factor` | drops L2 ^ d(w^2) ^ L1/(2 w^2) from B | both algebraic identities True, the direct derivative of the explicit covector against E +- w B False at the exact points |
| `bes-sum` | `planted_bessel` | expects O+ + O- = 2 g'(g'^2 + 2 c^2) | 4 h E = expected False; w^2 and the 5 jets True |
| `bes-ode` | `planted_bessel` | reduces g'', g''' with -eps | 4 h E = 2 g'(g'^2 + 4 c^2) and w^2 True (E and w^2 are even in eps); the 5 jets against the closed forms False |
| `plant-pass` | `planted_pairs` | the boosted pair's m = e^chi d(t - x + x d rho) in place of rho d rho | P2 gives (O+, O-) = ((x + 1 - sqrt(4x + (x - 1)^2))/(x(x + 1)), (x + 1 + sqrt(4x + (x - 1)^2))/(x(x + 1))), nonzero |
| `plant-fail` | `planted_pairs` | (dt, x d rho) replaced by the closed (dt, rho d rho) | P3 gives {O+, O-} = {0} against the predicted {-2, 2} |
| `ser-b8` | `series_resid` | a_{4,1} = F_inf (F_inf^2 + 8) | the determinant of the hats first differs from 0 at nu^10; the signature stays True |
| `ser-a2` | `series_resid` | a_{2,0} = -F_inf | the determinant first differs from 0 at nu^8; the signature criterion False |
| `obs-sign` | `obstruction` | expects +64 F_inf^3 and -64 F_inf | both leading coefficients False, sum and difference False; C-free and the precision True |
| `trunc-b` | `truncation` | the K = 9 member has a_{4,1} = F_inf (F_inf^2 + 8) | the K = 9 member disagrees with K = 13 (False), K = 4, 6, 13, 17 and the free-coefficient run True |
| `zset-sum` | `zero_set` | the sum's polynomial is -64 F (F^2 + 1) | its real zeros {0} against the required {-1, 0, 1}: False |
| `jets-f3` | `jets_num` | F''' = -(N_eta - F' N_F - F'' N_F')/N_F2 | O+ and O- off the series by factors 5.6 (O-) and 1.5e5 to 3.8e4 (O+): worst relative difference 1.35e6 |
| `coord-u` | `coord_num` | k_t = alpha - beta u | worst relative difference 2.5 (in O+; O- changes only by 5e-4 at (2, 1/2), eta = 100) |
| `mirror-f` | `mirror` | the mirror image is -F(-eta) in place of F(-eta) | the pair is negated: relative differences 1.7e-3 to 8.0 against the threshold 1e-12 |

`mirror-f` fires without a large margin at F_inf = +-1 because O+ and O- are nearly equal and opposite at leading order
(-64 F^3 and 64 F), so the negated unordered pair is close to the original; the threshold 1e-12 is far below the 1.7e-3.

## Not tested, and what the code will not prove

- `two_scalars.closure` is not run on the conical family: it needs the exact jet of a point on N = 0 with the third derivative,
  and (eta, F, F', F'') rational on the cubic N = 0 are not at hand. #162 ran it at exact jets on the Bessel family. Here the
  Frobenius test fails, which is enough (it is necessary, `bessel_closure.md` section 1).
- That the actual solutions with a limit have O+ and O- with this expansion rests on #168's Theorem B read for F', F'', F''' (its
  proof has p and q as analytic functions of (zeta, sigma, G) with the termwise expansions; not written out there or here).
  `jets_num` is the numerical evidence: the integrated solution, not the series, gives O+ and O- equal to the series to the stated
  tolerance at four (F_inf, C).
- Non-axisymmetric or time-dependent deformations; F_inf = 0 (no solution but F = 0, #168); the constants F = F_inf (R = 0).
- Whether a pair (F_inf, C) is realized by an actual solution at all (#168 does not claim every pair); the global question (#167).

## Runs of record

From `notes/warp/` of the worktree at the commit named in `run_final.run1.commit`:

    nice -n 10 python3 conical_closure.py --no-controls                               # the 11 checks, about 5 min (K = 17 included)
    nice -n 10 sh run_mut.sh final                                                    # the 15 controls, one log each

The two run side by side (2 processes); `python3 conical_closure.py` with no flag does both in sequence. Logs: `run_final.run1.log`
(`.rc`, `.time` from `/usr/bin/time -l`, `.commit`), `final_<name>.log` and `.rc` per control. Reruns are numbered `run2`, ...
The checks of the record have to pass with exit 0, and each of the 15 controls has to exit 1 with only its target failing; if one
does not, that is reported with its log. Amendments to this README, if any, are dated and written before the run they concern.

## Amendments

None.

## Files

`scratch_explore_*.py` (the scratch explorations of "What was explored"), `dev_01_baseline.log`, `dev_02_<mutation>.log`,
`dev_03_k17.log` (the K = 17 probe), `dev_04_<mutation>.log`, `run_mut.sh` and `run_mut_some.sh` (the control drivers), then
the runs of record.

## Results of the runs of record (written after them)

Script at a4ee923 (`run_final.run1.commit`), unchanged since the criteria were declared; note and output at 78b6991 on
`wip/i172-conical-closure`.

| run | what | result |
|---|---|---|
| `run_final.run1` | the 11 checks, `--no-controls` | exit 0, 11 of 11 pass, 206 s, peak resident 116 MB (`/usr/bin/time -l`, `run_final.run1.time`) |
| `final_<name>` x 15 | each control once, `run_mut.sh final` (12 with `--skip-num`) | all exit 1, each fails its target check and no other; 2417 s in all, one process at a time |

The controls and the checks ran side by side as two processes. The criteria were not changed after the first run of record, and no
check failed. `conical_closure_output.txt` in the repository is `run_final.run1.log` followed by the 15 control lines assembled from
`final_<name>.log` and `.rc` (the script's own format).
