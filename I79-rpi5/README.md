# I79-rpi5: independent review of #65's two-scalar result (D, lemma, ideals, omega)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10, one thread.
Issue: https://github.com/nmoinvaz/negative-mass/issues/79
Worktree: `~/Source/negative-mass-i79`, branch `wip/i79-review-two-scalars` (base main 69dbd87).
Python: `~/Source/negative-mass-venv314/bin/python` (3.14.10, sympy 1.14.0, mpmath 1.3.0, numpy 2.5.4).

## Independence

Opened before my own runs: `notes/warp/two_scalars.md` (the claims), `notes/warp/phantom_source.md` (frame, (I1), (I2)),
`notes/warp/review.md` and `notes/warp/review_cartan.py` (#59's Cartan code), the text of issues #79 and #65.
Not opened until my logs are committed here: `two_scalars.py`, `two_scalars_output.txt`, `phantom_source.py`,
`three_scalars.*`, `same_sign_scalars.*`, and the auto-memory notes `i77-handover.md`, `i78-handover.md`.

What I recall about #65 before starting: its verdict, lemma and the claims in `two_scalars.md`, read in this session.
The auto-memory index (MEMORY.md, loaded automatically) has one-line descriptions of #77 and #78 that mention a
closure criterion and a rank-1 condition for one-sign pairs. I read no file behind those lines, and nothing in
them is an input to a check here.

Imported from `review_cartan.py` (shares only sympy with `phantom_source.py`): `Jets`, `axisymmetric_shift`,
`general_shift`, `cartan_ricci` and `ETA`, with its module-level `MUT` set by my controls where noted. Nothing else.
My own, sharing nothing with either: a coordinate-Christoffel Ricci routine at explicit exact functions
(`coord_ricci`), the lemma search, the certificates and the omega code.

## Acceptance criteria (written before the first run; none is loosened after seeing data)

Status words as in AGENTS.md. "Printed" means as written in `two_scalars.md`.

**D (script `review_two_scalars_cartan.py`).** With b = G(t, x, q), q = y^2 + z^2, and n = d_t - b d_x:
P = n(b_x) - b_x^2, Q = -Delta_perp b / 2, Z = d_x b_rho / 2, Y = -n(b_rho) / 2 + b_x b_rho, h = b_rho^2 / 2.
- C1 `blocks_jets`: the Cartan Ricci (imported `cartan_ricci`), in the frame (n, d_x, e_rho, e_phi), has
  R_00 = P - h, R_11 = -P - h, R_01 = Q, R_0rho = Z, R_1rho = Y, R_rho,rho = h, R_a,phi = 0, each an exact identity
  in the jets of G (after multiplying by powers of rho to clear the square root). Pass: every difference expands to 0.
- C2 `D_cartan_jets`: rho^2 det(R_3) from the Cartan Ricci minus rho^2 D(printed) expands to 0 in the jets of G, with
  D(printed) = h(h^2 - P^2 - Q^2 + Y^2 + Z^2) - P(Y^2 - Z^2) + 2QYZ.
- C3 `D_identity`: det [[P-h, Q, Z], [Q, -P-h, Y], [Z, Y, h]] minus D(printed) expands to 0 in the symbols P, Q, Z, Y, h.
- C4 `D_coordinate`: my coordinate-Christoffel Ricci of ds^2 = -dt^2 + (dx + b dt)^2 + dy^2 + dz^2 at 9 exact rational
  points (3 explicit rational shifts b(t, x, rho), 3 points each, off the axis) gives det R_3 in the frame
  (n, d_x, e_rho) exactly equal to D(printed) from the derivatives of the same b.
- C5 `axis_D`: D(printed) = 0 on the axis (rho = 0) for every G, and the Cartan R(E_2, .) = R(E_3, .) = 0 there.
- C6 `cartan_planted`, `coord_planted`: both Ricci routines give R_ab = 3H^2 g_ab for de Sitter (flat slicing), and
  R_ll = -2a^2/(l^2 + a^2)^2 as the only nonzero component for Ellis-Bronnikov (D = 4).
- C7 `planted_D`: through the coordinate route and the jet route, b = k rho^2 gives D = h(h^2 - 4k^2) with
  h = 2k^2 rho^2 (zero at rho^2 = 1/|k|); b = -eps ln|C - eps ln rho| gives D = 0 identically (eps = +-1).
- C8 `D_slice_nonaxi` (added 2026-11-24, see A1).
Verdict wording: *checked symbolically* if C1 to C5 pass; any failing line is a reported discrepancy, with the
failing identity printed.

**Lemma (script `review_two_scalars_lemma.py`, and by hand in the note).** R real symmetric on an orthonormal frame,
R_a3 = 0 for all a (including a = 3), R_00 + R_11 + 2 R_22 = 0. Then R = lambda eta + a a - b b with lambda real and a, b
real covectors iff lambda = 0 and det R_3 = 0.
- L1 `ricci_from_T`: T_ab = d_a phi1 d_b phi1 - d_a phi2 d_b phi2 - g_ab (...) with G = 8 pi T gives
  R_ab = 8 pi (d phi1 d phi1 - d phi2 d phi2) + 8 pi V g_ab, in symbols, exactly.
- L2 `weighted_trace`: N = R_3 - lambda diag(-1, 1, 1) has N_00 + N_11 + 2 N_22 = -2 lambda under the hypotheses, exactly.
- L3 `search_planted`: the lambda search (below) finds lambda_0 for 30 planted lambda_0 eta + a a - b b (lambda_0 = 0
  and != 0), in random rational Lorentz frames, and returns the empty set for 30 planted (+,+), (-,-), (+,-,+)
  forms and for 20 generic symmetric 4 x 4.
- L4 `lemma_if`: 40 random rational tensors with the hypotheses and det R_3 = 0 (R_3 != 0 in 38 of them, R_3 = 0 in 2)
  have lambda-set {0}, and a, b rebuilt to 1e-40 (mpmath, 60 digits) reproduce R.
- L5 `lemma_onlyif`: 40 random rational tensors with the hypotheses and det R_3 != 0 have empty lambda-set.
The lambda search: the candidates are the real roots of det(R - lambda eta) (a quartic, exact real-root isolation), not the
gcd of 3 x 3 minors; at each root the inertia of the symmetric matrix R - lambda eta at 60 digits must have at most
one positive and at most one negative eigenvalue (zero eigenvalues counted by |ev| < 1e-40). Verdict: *proved* by hand
(note), with L1 to L5 as exact or high-precision checks of the statement.

**Constant speed and the ideals (script `review_two_scalars_ideals.py`).** w = v(1 - f), w1 = w', w2 = w'', c = cos theta,
A = 2w - r w1, B = w1 + r w2.
- I1 `r3_const`: R_3 for b = w(r) - v from P, Q, Z, Y, h (my sympy differentiation in (xi, rho)) equals the imported Cartan
  R_3 for b = -v H(r_s^2) (jets H_k) exactly, and the note's frame table (typed from phantom_source.md).
- I2 `coeffs_const`: 16 r^3 D = c_0 + c_1 u + c_2 u^2 + c_3 u^3, u = c^2. My c_0 and c_3 equal the printed
  c^0: 2 w1^2 r (w1^4 r^2 - 4 w^2 w1^2 - (w1 + r w2)^2) and
  c^6: -2 (2 r w w2 - 2 w w1 + r w1^2)(r w w2 - w w1 + r w1^2)^2. The other two are reported.
- I3 `ideal_const`: in R = Q[r, w, w1, w2][1/(r w1)], ideal(c_0..c_3) = ideal(A, B^2). Pass: explicit cofactors, found
  by linear algebra (no Groebner basis), with c_k = alpha_k A + beta_k B^2 and A = sum gamma_k c_k, B^2 = sum delta_k c_k,
  every identity verified by exact expansion. If only ideal(A, B) holds (B in place of B^2), that is a discrepancy
  to report, since the conclusion for real jets is unchanged.
- I4 `zero_set_const`: planted jets with A = B = 0 give D = 0 for 10 random c; planted jets with A = 0, B != 0 and with
  B = 0, A != 0 give D != 0.
- I5 `no_open_set`: d/dr A = 2 w1 - B (exact). On an interval A = 0 gives w = C r^2 and B = 0 gives w = K ln r + L; both
  force w = 0. Checked by exact substitution of both families.
- I6 `acc_R3`: for b = -V(t) H(((x - X(t))^2 + y^2 + z^2)), the imported Cartan R_3 in lab coordinates (generic jets of
  V, X, H) equals my comoving form with w~ = X' - V f, w~', w~'', A = V'/V: P and Y of the constant case get +A w~' c and
  -A w~' s / 2. Exact identity in the jets.
- I7 `acc_coeffs`: 16 r^3 D is a degree-6 polynomial in c with 7 coefficients; the odd ones carry the factor A w~1 r; at
  A = 0 it is I2's polynomial.
- I8 `acc_unit`: with A w~1 r inverted, the 7 coefficients generate the unit ideal: explicit cofactors with
  sum g_k c_k = 1 (in Q[r, w, w1, w2, A][1/(A r w1)]), verified by exact expansion. If I cannot find the cofactors
  within the stop condition, I report the largest sub-claim proved (for example the resultant elimination) and say so.
- I9 `brho_D`: for b(rho): R_3 = [[-h, Q, 0], [Q, -h, 0], [0, 0, h]], D = h(h^2 - Q^2); b = -eps ln|C - eps ln rho| solves
  b'' + b'/rho = eps b'^2 (exact); D = 0 identically on those two families.
Verdict wording: *checked symbolically* where the certificates verify exactly; "reported discrepancy" otherwise.

**omega (script `review_two_scalars_omega.py`).** k = a + b, m = a - b. omega = dm(K, M) k + i_K dk, with k(K) = m(M) = 1,
k(M) = m(K) = 0, for the two conditions omega ^ k = -dk, omega ^ m = dm.
- W1 `omega_planted`: 8 planted pairs (phi1, phi2 random polynomials in (t, x, y, z); chi random polynomial; a, b the boost
  of (d phi1, d phi2) by -chi) give omega = d chi exactly, with two different choices of (K, M), omega ^ k = -dk,
  omega ^ m = dm and d omega = 0 exactly.
- W2 `omega_planted_fail`: 4 planted pairs with k ^ dk != 0 give a candidate that violates omega ^ k = -dk (nonzero residual).
- W3 `omega_eb`: Ellis-Bronnikov with a normal scalar: my coordinate Ricci equals lambda g + a a - b b with lambda = 2 kappa^2,
  a = sqrt(2) kappa dt, b = sqrt(8 pi) phi2' dl (exactly, symbolic in l, 0 < beta < 1), omega = 0, and also omega = -d chi
  after a planted boost chi(t, l); and G - 8 pi T = 0 with the printed fields.
- W4 `omega_brho`: for b(rho) = -eps ln|C - eps ln rho|: my coordinate Ricci (symbolic in rho) equals
  h((theta^rho)^2 - (theta^0 + eps theta^1)^2) with theta^0 = dt, theta^1 = dx + b dt; k, m proportional to
  dρ ± ((1 + eps b) dt + eps dx); nu ^ d nu = b' dx ^ drho ^ dt (exact); the omega candidate violates its equation.
Verdict wording: *proved* by hand for the formula (note), *checked symbolically* for W1 to W4.

## Controls (each is `--mutate=NAME`; it must exit 1 with its named target checks failing; named before any run)

`review_two_scalars_cartan.py`:
| control | change | targets |
|---|---|---|
| `d-qyz-sign` | printed D with -2QYZ | `D_identity`, `D_cartan_jets`, `D_coordinate` (+ `D_slice_nonaxi`, A1) |
| `d-drop-z2` | printed D without the Z^2 terms | `D_identity`, `D_cartan_jets`, `D_coordinate` (+ `D_slice_nonaxi`, A1) |
| `blocks-q-sign` | expected R_01 = +Delta_perp b / 2 | `blocks_jets`, `D_cartan_jets` |
| `cartan-lapse` | imported routine with lapse 1 + b | `blocks_jets`, `D_cartan_jets` |
| `cartan-sign` | imported routine, sign of omega ^ omega flipped | `cartan_planted`, `blocks_jets`, `D_cartan_jets` |
| `nonaxi` | shift a function of y^2 + 2 z^2 | `blocks_jets`, `D_cartan_jets` (original prediction; silent on `D_cartan_jets`, amended to `blocks_jets`, `planted_D`, A1) |
| `coord-gamma` | my Christoffel symbol with a wrong index order | `coord_planted`, `D_coordinate`, `planted_D` (+ `D_slice_nonaxi`, A1) |
| `planted-h` | planted expectation with h doubled | `planted_D` |

`review_two_scalars_lemma.py`:
| control | change | targets |
|---|---|---|
| `lemma-weight` | hypothesis R_00 - R_11 + 2 R_22 = 0 | `lemma_if`, `weighted_trace` |
| `lemma-r33` | R_33 allowed nonzero | `lemma_if` |
| `planted-sign` | planted lambda_0 eta + a a + b b expected to pass | `search_planted` |
| `trace-sign` | trace reversal with the wrong sign | `ricci_from_T` |
| `search-eig` | inertia from eigenvalues of eta^{-1} M | `search_planted` |

`review_two_scalars_ideals.py`:
| control | change | targets |
|---|---|---|
| `alc-lapse` | imported Cartan with lapse 1 + b | `r3_const`, `acc_R3` |
| `coef-c0-sign` | expected c_0 with the opposite sign | `coeffs_const` |
| `ideal-cofactor` | one cofactor of the certificate altered | `ideal_const` |
| `planted-ideal` | planted jets with A = 1, expecting D = 0 | `zero_set_const` |
| `ode-sign` | second relation r w2 = +w1 | `no_open_set` |
| `acc-no-A` | my comoving R_3 without the A terms | `acc_R3` |
| `acc-drop-odd` | odd coefficients dropped from the certificate | `acc_unit` |
| `brho-h2` | expected h doubled | `brho_D` |

`review_two_scalars_omega.py`:
| control | change | targets |
|---|---|---|
| `omega-sign` | omega = -dm(K, M) k + i_K dk | `omega_planted`, `omega_eb` |
| `omega-swap` | omega = dm(K, M) m + i_M dm | `omega_planted` |
| `omega-nodk` | omega = dm(K, M) k | `omega_planted` |
| `plant-open` | planted k replaced by a non-closed form, recovery expected | `omega_planted` |
| `eb-lambda` | lambda = 2 kappa^2 replaced by kappa^2 | `omega_eb` |
| `brho-eps` | split with theta^0 - eps theta^1 | `omega_brho` |

A control whose targets do not all fail is SILENT and is reported as a failure of the check, not hidden.


### Amendments made after runs began (2026-11-24; each is written here before the run it governs)

A1. `nonaxi` (coordinator's point 1). Record: **`nonaxi` was silent on its named target `D_cartan_jets`; it fired `blocks_jets` and
`planted_D`; the target list was changed after the run** (log `cartan.mut_nonaxi.run1.log`). Reason, a claim to be checked: D(printed)
is det R(n, d_x, d_y) for EVERY b(t, x, y, z), with b_rho read as b_y and Delta_perp b = b_yy + b_zz, because review.md's R_00, R_0x,
R_0A, R_xA, R_AB hold with no symmetry. So `D_cartan_jets` is blind to a loss of axisymmetry, which only `blocks_jets` sees (R(e_phi, .) = 0).
`D_cartan_jets` keeps other controls that make it fail: `d-qyz-sign`, `d-drop-z2`, `blocks-q-sign`, `cartan-lapse`, `cartan-sign`.
New check C8 `D_slice_nonaxi`, criterion written now, before it runs: for 3 explicit rational shifts b(t, x, y, z) that are NOT functions of
rho (for example y + 2 z^2 terms), at 3 exact points each with z != 0, my coordinate-route Ricci gives (a) det R(n, d_x, d_y) equal to
D(printed) built from b_y, b_x, n and Delta_perp b = b_yy + b_zz, entry by entry R_3 = [[P-h, Q, Z], [Q, -P-h, Y], [Z, Y, h]] with
h = b_y^2/2, exactly; and (b) R(d_z, d_z) - b_z^2/2 = 0 exactly while R(d_z, d_z) != 0 at every point, so the missing axisymmetry shows
up in the e_phi row and not in D. Controls for C8, named before the run: `d-qyz-sign`, `d-drop-z2` and `coord-gamma` must make
`D_slice_nonaxi` fail (these three controls now also list it as a target). `nonaxi` keeps targets `blocks_jets`, `planted_D`.
The axis check `axis_D` gains one condition, R_00 + R_11 = 0 on the axis (the lemma needs it there; added before its rerun).

A4. (Coordinator approved 2026-11-24 with conditions; everything here is written after `D_slice_nonaxi` failed and before the rerun.)
**Result on record: claim A1 (det R(n, d_x, d_y) at z = 0 equals the printed D for every b(t, x, y, z)) is false.** `D_slice_nonaxi` failed
0 of 9 (`cartan.run2.log`, kept). The reason is that for a general b, R_00 = P - h - b_z^2/2 and R_11 = -P - h - b_z^2/2 with h = b_y^2/2;
the block has the printed form only where b_z = 0. What is true: `nonaxi` was silent on `D_cartan_jets` because b = G(t, x, y^2 + 2z^2) has
b_z = 4 z G_001 = 0 on the slice z = 0 that `D_cartan_jets` uses. `D_slice_nonaxi` is removed from the script and replaced by two checks,
both "written after D_slice_nonaxi failed":
- (i) `D_slice_bz0` (written after D_slice_nonaxi failed). For 3 explicit rational shifts that are NOT functions of rho and are even in z
  (y + 2 z^2 terms), at 3 exact points each with z = 0, my coordinate-route Ricci gives R(n, d_x, d_y) = [[P-h, Q, Z], [Q, -P-h, Y], [Z, Y, h]]
  entry by entry and det = D(printed), with h = b_y^2/2, Q = -(b_yy + b_zz)/2. Also, for the axisymmetric b = G(t, x, y^2 + z^2) of
  `blocks_jets`, b_z = 0 on z = 0 exactly in the jets of G (so #65's D is unaffected by the correction). Controls named before the rerun:
  `d-qyz-sign`, `d-drop-z2`, `coord-gamma`, `blocks-q-sign` must make `D_slice_bz0` fail.
- (ii) `D_slice_offslice` (written after D_slice_nonaxi failed). For 3 explicit rational non-axisymmetric shifts (including ones not even in z),
  at 3 exact points each with z != 0, compare all six entries of R(n, d_x, d_y) with the block [[P-h, Q, Z], [Q, -P-h, Y], [Z, Y, h]]
  (h = b_y^2/2): the claim is that ONLY R_00 and R_11 differ, each by exactly -b_z^2/2 (b_z != 0 at every point), the other four entries agree
  exactly, and det R(n, d_x, d_y) != D(printed). R_00 = P - h - b_z^2/2 and R_11 = -P - h - b_z^2/2 are checked in code from the derivatives
  of b; review.md is not the evidence. Controls named before the rerun: `coord-gamma`, `blocks-q-sign` must make `D_slice_offslice` fail
  (`d-qyz-sign` and `d-drop-z2` change only D(printed), which this check uses for an inequality, so they are not targets here).
- `D_cartan_jets` keeps controls that fire on it, in `cartan.mut_<NAME>.run1.log`: `d-qyz-sign` (difference -8 G_000 G_001 G_011^2),
  `d-drop-z2`, `blocks-q-sign`, `cartan-lapse`, `cartan-sign`. `nonaxi` was never needed for it.
- Status word to give in the note for "#65's D is unaffected": *checked symbolically* (b_z = 0 on z = 0 for G(t, x, q) is an exact identity in the jets;
  D_cartan_jets and D_coordinate already use the slice y = rho, z = 0 or e_rho and pass).

A2. `acc-drop-odd` (coordinator's point 2). Original control: the certificate search of `acc_unit` run with the support c_0, c_4, c_6
(odd coefficient c_5 dropped), by rref over Q(r, w1, aa) at degrees 2 to 5. It ran 12 min wall in the symbolic rref of a system with no
solution; I stopped it by SIGTERM (the partial log, ending after `acc_coeffs`, is `ideals.mut_acc-drop-odd.run1.log`, with a stop note
appended). Change: `find_cert2` now first solves the same system at the numeric point (r, w1, aa) = (2, 3, 5) over Q; if that has no
solution there is none over Q(r, w1, aa) with monomial denominators either (it would specialize), and the search reports "none"; if
it has one, the symbolic solve runs as before. Reason: the symbolic rref of an inconsistent system is slow. The same function serves the real
check `acc_unit`; it decides the same thing (`ideals.run3.log` passes after the change, with the same certificate). Targets of the control
did not change: `acc_unit`. Rerun: `ideals.mut_acc-drop-odd.run2.log`, fired in 16 s.

A3. Other script changes after a first run, all bug fixes of my own checks, none loosened: `lemma.run1.log` crashed in a format string;
`ideals.run1.log` failed `brho_D` because my Laplacian test used an abstract function with sympy's Abs(y) (replaced by three explicit test
functions, `ideals.run2.log` passes); `omega.run1.log` crashed after section 2 in `dict(par, **{Symbol: ...})` (fixed, `omega.run2.log`).
`--certs` options print the certificates (no change to a check).

## Run protocol

Every stdout goes to a numbered log here (`<script>.runN.log`); a log is never overwritten. A script exits 1 if a check fails or a
control does not fire. Final runs (stdout only, exit 0) go to `notes/warp/review_two_scalars_*_output.txt` in the worktree and
are copied here. A run that exceeds 1 h of wall time is stopped and reported. Memory is reported only. The scripts
use no /proc and no Linux-only path.

## Log

2026-11-24, step 2 (D and the lemma). Logs: `cartan.run1_trial.log` (first run of `review_two_scalars_cartan.py --no-controls`,
exit 0, 8 checks pass, 8 s; it was started from a scratch path and copied here unchanged), `cartan.mut_<NAME>.run1.log` (eight controls),
`lemma.run1.log` (crashed: a format-string bug in the detail line of `search_planted`, nothing computed after section 3),
`lemma.run2.log` (exit 0, 6 checks pass, 18 s), `lemma.mut_<NAME>.run1.log` (five controls).
Controls: 12 of 13 fired on every named target. `nonaxi` exited 1 and fired `blocks_jets` and `planted_D`, but NOT its named target
`D_cartan_jets` (SILENT in `cartan.mut_nonaxi.run1.log`). The prediction was wrong, not the check: D(printed) is the determinant of
R(n, d_x, d_y) at z = 0 for every b(t, x, y, z), because review.md's formulas for R_00, R_0x, R_0A, R_xA, R_AB hold with no symmetry,
so D_cartan_jets cannot see a loss of axisymmetry; what axisymmetry adds is R(e_phi, .) = 0, which `blocks_jets` tests.
Amendment (made after seeing this run, listed for the coordinator to veto): the `nonaxi` targets in the script are now
`blocks_jets`, `planted_D`. The README table above keeps the original prediction.
