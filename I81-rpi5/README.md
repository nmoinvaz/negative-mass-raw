# I81-rpi5: scalar-form test for the sheared warp shift b = -v f(q), q = X^2 + y^2 + 2 z^2 + X y / 2 (#81)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10, one thread.
Issue: https://github.com/nmoinvaz/negative-mass/issues/81
Worktree: `~/Source/negative-mass-i81`, branch `wip/i81-sheared` (base main 4d77f1d).
Python: `~/Source/negative-mass-venv314/bin/python` (3.14.10, sympy 1.14.0, mpmath 1.3.0, numpy).
Script: `notes/warp/sheared.py` (`--no-controls`, `--mutate=NAME`, `--logdir=DIR`; exits 1 on a failed check or a silent control).
Imports: from `phantom_source.py` `scalar_form`, `ricci_at_point`, `shift_tetrad_ricci`, `JetD`, `shift_metric` (inside),
`X, y, z, v, TX`; from `nonaxisymmetric.py` `q_rule`, `route_T`, `lemma_residues`, `G`, `ETA`, `tanh_jets`, `bump_jets`,
`rational_jets`. Nothing else is imported. `sheared.py` has its own q, closed forms, reduction, points and controls.

## What was done before this README (not committed, not part of any run)

Reading, and two hand derivations. `sheared.py` was compiled (`py_compile`) and not run. The 29 sample points below were
listed with their q and w = grad_perp q (no Ricci tensor, no `scalar_form`). I did not run any route on the sheared shift.

1. From the 3+1 equations of `route_T` (K_ij = (d_i b_j + d_j b_i)/2, lapse 1, flat slices, beta = (b, 0, 0)), for ANY
   b(t, x, y, z), with a, c in {y, z} and D_t b = d_t b - b d_x b:
   R_nn = -(b_y^2 + b_z^2)/2 - b_x^2 + b_xt - b b_xx;  R_xx = b_x^2 - (b_y^2 + b_z^2)/2 - b_xt + b b_xx;  R_nx = -(b_yy + b_zz)/2;
   R_na = b_xa / 2;  R_xa = b_x b_a / 2 - d_a(D_t b) / 2;  R_ac = b_a b_c / 2.
   I matched all ten against #70's printed unsheared components (`nonaxisymmetric.md`, "The Ricci tensor in the frame")
   by hand. They are the content of `closed_form`.
2. For the sheared q, w = grad_perp q = (q_y, q_z) = (2y + X/2, 4z), q_X = 2X + y/2, grad_perp q_X = (1/2, 0), wp = (-q_z, q_y):
   - R_00 + R_11 = -|grad_perp b|^2 and R(w, w) = |grad_perp b|^2 |w|^2 / 2 give (I2) = 0 identically.
   - R(wp, wp) = R(wp, w) = 0, R(wp, E_0) = v f' z, R(wp, E_1) = v^2 f' (1 - f) z. So (I1) fails iff v f' z != 0
     (E_1 component also needs f != 1).
   - grad_perp d_x b x grad_perp b = 2 v^2 f'^2 z, so the premise "grad_perp d_x b along grad_perp b" fails iff v f' z != 0.
   - R(w, E_1) - v (1 - f) R(w, E_0) = v^2 f'^2 q_X |w|^2.
   - The reduction. Take e_2 = w/|w|, e_3 = wp/|w|, M = R - lam eta = s u u^T, s != 0. M_33 = -lam, M_a3 = R(e_a, e_3).
     (A) u_3 = 0 forces lam = 0, R(e_3, E_0) = R(e_3, E_1) = 0, and then the lemma with (I2) gives R = 0.
     (B) u_3 != 0: M_23 = 0 gives u_2 = 0, then M_02 = M_12 = 0, i.e. c1: R(w, E_0) = 0 and c2: R(w, E_1) = 0. With the
     identity above, c1 and c2 give v^2 f'^2 q_X |w|^2 = 0, so q_X = 0 (v f' != 0, w != 0), then c1 gives q_y = 0, so
     X = y = 0: the z axis. M_22 = 0 gives lam = R(e_2, e_2) = |grad_perp b|^2/2; the rest is c3: (R_00 + lam) lam =
     -r0^2, c4: (R_11 - lam) lam = -r1^2, c5: R_01 lam = -r0 r1, with r0 = R(e_3, E_0), r1 = R(e_3, E_1)
     (normalised e_3). They are sufficient too, with M = -(1/lam)(r0, r1, 0, -lam)(r0, r1, 0, -lam)^T. lam > 0 makes s < 0,
     so only eps = -1 can pass. This is the `reducer` of the script. It is by hand and not reviewed.
   - On the z axis X = y = 0 (v = 1, z = 1/2): c3, c4 and (I2) reduce to 32 p^2 + 32 p - 1 = 0 with p = v^2 (1 - f)^2,
     f' = -1/(256 v^2 (1 - f) z^2), and c5 gives f'' = (-(1 - f)/(64 z^2) - 6 f') / (16 z^2). That is the planted point of
     check `zaxis_pass`, built from these formulas, which may be wrong.

## Predictions, written before the first run

- (P1) `closed_form`, `shear_cross`, `shear_I1`, `shear_I2`, `circular_closed`, `reduction_identity` hold as identities in the
  jets, with the formulas of this README and of the docstring.
- (P2) At the 29 points the premises (I1), (I2) of the adapted frame hold at 8 (points 1, 2, 3, 4, 14, 15, 26, 29: z = 0,
  or f' = 0) and (I1) fails at 21. (I2) holds at all 29. At point 25 (f = 1) only the E_0 component of (I1) is nonzero.
- (P3) `scalar_form` returns `algebraic` at both signs at the 28 points with R != 0 and `trivial` at point 29 (R = 0).
  Points 12, 13, 19 are on the z axis, where c1 and c2 hold and c3-c5 are generic conditions on the jets, so I expect
  `algebraic` there too. Any `pass` or `sign` would be a result and is reported as one.
- (P4) The reduction predicts the same status as `scalar_form` at all points and on the planted matrices.
- (P5) At the z-axis point of `zaxis_pass` the sheared Ricci tensor is a phantom scalar form: the largest 2x2 minor of
  R - lam eta is below 1e-40 at 60 digits.

## Sample points (`POINTS` in `sheared.py`; jets in q at the point; v is the shift's speed)

| # | profile | kind | (X, y, z) | v | q |
|---|---|---|---|---|---|
| 1 | tanh, sigma = 8, R = 1 (in r = q^(1/2); 50-digit jets rounded to 45-digit rationals) | axis | (1, 0, 0) | 1 | 1 |
| 2 | tanh | axis | (-1, 0, 0) | 1 | 1 |
| 3 | tanh | z = 0 plane | (3/5, 4/5, 0) | 1/2 | 31/25 |
| 4 | tanh | critical line (w = 0) | (1, -1/4, 0) | 3 | 15/16 |
| 5 | tanh | X = 0 plane | (0, 1/3, 2/3) | 1 | 1 |
| 6 | tanh | y = 0 plane | (1/3, 0, 2/3) | 3 | 1 |
| 7 | tanh | general | (1/2, 1/2, 1/2) | 3 | 9/8 |
| 8 | tanh | general | (4/5, 1/5, 2/5) | 1 | 27/25 |
| 9 | tanh | general | (-1/5, 4/5, 2/5) | 1/2 | 23/25 |
| 10 | tanh | general | (5/6, 1/2, 1/6) | 1 | 29/24 |
| 11 | tanh | general | (-4/7, 1/7, 4/7) | 3 | 47/49 |
| 12 | tanh | z axis | (0, 0, 7/10) | 1 | 49/50 |
| 13 | tanh | z axis | (0, 0, -5/7) | 3/2 | 50/49 |
| 14 | bump (1 - q/4)^3 for q < 4, 0 beyond (exact) | axis | (1, 0, 0) | 7/4 | 1 |
| 15 | bump | z = 0 plane | (3/5, 4/5, 0) | 7/4 | 31/25 |
| 16 | bump | general | (1/2, 1/2, 1/2) | 7/4 | 9/8 |
| 17 | bump | general | (-1/5, 4/5, 2/5) | 7/4 | 23/25 |
| 18 | bump | general | (3/2, 1/3, -1/2) | 7/4 | 28/9 |
| 19 | bump | z axis | (0, 0, 1/2) | 7/4 | 1/2 |
| 20 | 1/(1 + q^2) (exact) | general | (4/5, 1/5, 2/5) | 2 | 27/25 |
| 21 | 1/(1 + q^2) | X = 0 plane | (0, 1/3, 2/3) | 2 | 1 |
| 22 | 1/(1 + q^2) | general | (1/3, -2/5, 3/4) | 3/2 | 2393/1800 |
| 23 | random jets, f' f'' != 0 | general | (1/2, 1/2, 1/2) | 8/3 | 9/8 |
| 24 | random jets | general | (5/6, 1/2, 1/6) | 5/3 | 29/24 |
| 25 | f = 1, random f', f'' | general | (4/5, 1/5, 2/5) | 3/2 | 27/25 |
| 26 | f = 2/3, f' = 0, f'' = -3/5 | general | (4/5, 1/5, 2/5) | 5/2 | 27/25 |
| 27 | f = 1/2, f' = -3/2, f'' chosen so that R(w, E_0) = 0 | general | (1/2, 1/2, 1/2) | 2 | 9/8 |
| 28 | f = 1/2, f' = -3/2, f'' chosen so that R(w, E_1) = 0 | general | (1/2, 1/2, 1/2) | 2 | 9/8 |
| 29 | bump beyond it (f = f' = f'' = 0) | general | (2, 1, 1/2) | 7/4 | 13/2 |

The z = 0 points and the critical line are where the premises are predicted to hold, so they test the lemma's side.
Points 27 and 28 each satisfy one of c1, c2 on purpose.

## Checks: wording, controls and targets

A control is `--mutate=NAME`. It must exit 1 and fail every target check named here. A mutation run executes only the
sections its targets need (docstring), so a control's other checks may not run. A target that does not fire is reported as
silent, and no target list is edited after a run without a dated amendment below.

Section D (general jets, exact):

| check | exact wording | control | change |
|---|---|---|---|
| `closed_form` | Route D's ten frame components of the Ricci tensor equal the closed forms of item 1, evaluated on b = -v f(q) with the sheared q, as polynomial identities in X, y, z, v, f, f', f'' | `form-drop`, `unsheared`, `lapse` | drops -d_a(D_t b)/2 from R_xa; q without X y/2; lapse 1 + b |
| `shear_cross` | d_y(d_x b) d_z b - d_z(d_x b) d_y b = 2 v^2 f'^2 z | `unsheared` | q without X y/2 in the measured side |
| `shear_I1` | With w = (q_y, q_z): (R(wp, E_0), R(wp, E_1), R(wp, w), R(wp, wp)) = (v f' z, v^2 f' (1 - f) z, 0, 0) identically | `unsheared`, `circular`, `lapse` | no shear; w = (y, z); lapse |
| `shear_I2` | \|w\|^2 (R_00 + R_11) + 2 R(w, w) = 0 identically | `circular`, `lapse` | w = (y, z); lapse |
| `circular_closed` | With c = (y, z), cp = (-z, y), cpw = z (2y - X/2), q_X = 2X + y/2, h = f'(1 - f), h' = f''(1 - f) - f'^2: R(cp, E_0) = -(v/2)(f'' q_X cpw - f' z/2), R(cp, E_1) = (v^2/2)(f'^2 q_X cpw - h' q_X cpw + h z/2), R(cp, c) = (v^2 f'^2/2) cpw (y q_y + 4 z^2), R(cp, cp) = (v^2 f'^2/2) cpw^2, and \|c\|^2 (R_00 + R_11) + 2 R(c, c) = -v^2 f'^2 cpw^2 | `circ-swap`, `unsheared` | circle from (z, y); no shear |
| `reduction_identity` | R(w, E_1) - v (1 - f) R(w, E_0) = v^2 f'^2 q_X \|w\|^2 | `red-coef`, `unsheared`, `lapse` | 2 v^2; no shear; lapse |

Section X (8 random exact points, seed 7, random v, t, point and jets):

| check | exact wording | control | change |
|---|---|---|---|
| `xcheck_E` | Route D equals route E (`ricci_at_point`, Christoffel at a point, explicit b) in all 16 frame components | `static` | no t-derivatives in D |
| `xcheck_T` | Route D equals route T (3+1 equations) | `static`, `lapse` | the same; lapse 1 + b in D and E |

Section P (the 29 points; `scalar_form` at eps = -1 and +1):

| check | exact wording | control | change |
|---|---|---|---|
| `points_xcheck` | Route D equals route E (explicit b with the point's jets) in all 16 components at every point | `jet-g2`, `static` | f'' + 1/7 in E; no t-derivatives |
| `points_residues` | At every point the exact residues of (I1) in the adapted frame equal (v f' z, v^2 f' (1 - f) z, 0, 0) and (I2) = 0. (At the critical line the frame is (E_2, E_3).) The numbers of points where (I1) fails and where the premises hold are printed | `circular`, `unsheared`, `planted-in-data` | circular frame; no shear; planted form in the data |
| `points_outcome` | At every point with R != 0, `scalar_form` returns `algebraic` at both signs, and `trivial` where R = 0 | `broken-test`, `planted-in-data` | a test that always passes; planted form in the data |
| `lemma_agree` | At the points where (I1) and (I2) hold in the adapted frame, `scalar_form` returns `algebraic` (R != 0) or `trivial` (R = 0) at both signs | `broken-test` | the same |
| `reduction_agree` | The reducer returns the same status as `scalar_form` at every point, both signs | `broken-test` | the same |

Section L (planted at the 29 points, random rational lam and u, seed 8181):

| check | exact wording | control | change |
|---|---|---|---|
| `planted_pass` | R = lam eta - 8 pi u u^T, eps = -1: `pass`, lam and u u^T recovered exactly, at every point | `planted-sign` | lam eta + 8 pi u u^T |
| `planted_sign` | the same with eps = +1: `sign` at every point | `planted-sign`, `broken-test` | the same; always `pass` |
| `planted_deform` | plus 1/10 on E_3 E_3: `algebraic` at every point | `planted-null`, `broken-test` | deformation by zero; always `pass` |
| `planted_premise` | the planted form violates (I1) or (I2) of the adapted frame at every point | `planted-flat` | planted R = 0 |

Section R (planted on the reduction; 4 matrices R = r (eta - m m^T) in the frame (E_0, E_1, e_2, e_3), m = (alpha, beta, 0, 1),
alpha^2 + beta^2 = 2, rotated to the coordinate frame; w = (3,4), (5,12), (8,15), (4,-3)):

| check | exact wording | control | change |
|---|---|---|---|
| `reduction_pass` | `scalar_form` gives `pass` with lam = r at eps = -1 and `sign` at eps = +1, and the reducer gives `pass` and `sign`, for the 4 matrices | `red-sign` | the reducer returns `pass` for both signs |
| `reduction_deform` | Adding 1/10 to R_02 (c1), R_12 (c2), R_00 (c3), R_11 (c4) or R_01 (c5): `scalar_form` and the reducer both return `algebraic` at both signs, for the 4 x 5 matrices | `red-no-c1`, ..., `red-no-c5` | the reducer ignores that condition |

Section Z (60 digits, mpmath): v = 1, X = y = 0, z = 1/2, p = (3 sqrt 2 - 4)/8, 1 - f = sqrt p, f' and f'' from item 2.

| check | exact wording | control | change |
|---|---|---|---|
| `zaxis_pass` | Route D's R at that point, with lam = R(E_3, E_3): the largest 2x2 minor of R - lam eta is below 1e-40, every diagonal entry of R - lam eta is below 1e-40 and its trace is negative; with f'' + 1/10 the largest minor exceeds 1e-6 | `zaxis-off` | f'' + 1/10 on the pass side |

## Runs

- `run_dev.sh` / `run_final.sh` in this folder launch detached units `nm-i81-<step>` (`systemd-run --user --nice=10`),
  stdout to a log here, exit code to a `.rc` file. Logs are never overwritten; reruns are numbered.
- Stop condition: a single run unfinished after 1 h wall time is stopped by its exact PID and reported. Memory is only reported.
- Final: `notes/warp/sheared_output.txt` is the stdout of `python notes/warp/sheared.py --logdir=<this folder>/final_mut`.

## Amendments

(none yet)
