# I157-rpi5: Singular ideal step for three mixed-sign scalars on the Alcubierre wall, arbitrary profile

Machine rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process, one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/157. Branch `wip/i157-three-scalars-ideal`, worktree
`~/Source/negative-mass-i157`, from main 3ae25be. Python `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0,
mpmath 1.3.0). Singular 4.4.1 at `/usr/bin/Singular`. Written 2026-11-24, before the first run of the wall's ideal step.

## Question

At lambda = 0 three scalars of mixed signs close on an open set of the constant-speed wall iff the orbit-space metric h on
(t, r, theta) is flat on it (#77, Lemma C). Does any C^4 profile w(r) = v (1 - f) make h flat on an open box of (r, theta)
with r w' != 0? #77 found Ric(h) != 0 at every exact point tested; its ideal step (C5) did not finish in sympy.

## The reduction (stated before the runs)

1. The numerators N_ab = det(h)^2 Ric(h)_ab are polynomials in (r, c, S, W0..W4), c = cos theta, S = sin theta, W_k = w^(k)(r),
   linear in W4. If h is flat on a box, h is nondegenerate there, so all N_ab vanish on the box.
2. N is weighted homogeneous (weight r = 1, W_k = -k), so r = 1 loses nothing: with u_k = r^k W_k the conditions are
   polynomials in u0..u4, and the saturation by `r w'` is the saturation by u1.
3. At a fixed r, N_ab is a trigonometric polynomial in theta, A(c) + S B(c) mod S^2 = 1 - c^2. If it vanishes on an interval
   of theta it vanishes identically. So the exact condition for a box is the ideal J_all of ALL coefficients of c^k and
   S c^k of every N_ab (a necessary condition on the jets at each r of the box). Evaluating N at one theta_0 gives
   ℚ-combinations of those coefficients, so each theta_0 rung generates a sub-ideal of J_all. If a sub-ideal together with
   1 - s u1 is the unit ideal, so is J_all, and no jets with r w' != 0 satisfy the conditions.
4. h nondegenerate also means det h = r^2 D != 0 on an open subset of the box (D = det R_3, and #65 shows D = 0 on no
   open subset of the wall). The equator rung may have solutions with det h = 0 (the "Phi = 0" locus of #77's explore/);
   if a rung is not the unit ideal, the next saturation is by the coefficients of q in 16 r^3 D = (1 - c^2) q(c^2).

## Ladder (fixed now; no rung is added or reordered after a run)

| rung | generators | saturation |
|---|---|---|
| R1 | N_ab at theta_0 = pi/2, (c, S) = (0, 1) | 1 - s u1 |
| R2 | R1 and N_ab at (c, S) = (3/5, 4/5) | 1 - s u1 |
| R3 | J_all, all coefficients of c^k, S c^k | 1 - s u1 |
| R4 | only if R3 is not unit: J_all with 1 - s q_k for each coefficient q_k of q, k = 0..3 | |

Verdict "unit" needs a certificate: cofactors c_i over ℚ with sum c_i f_i = 1 in ℚ[s, u0..u4], produced by Singular
(`liftstd`), verified in sympy without Singular. Verdict "not unit" needs an exact point of the variety (sympy) or is
reported "computed by Singular, not certified". A Singular Groebner basis over ℚ is exact computation but not a proof.
A computation modulo a prime is only a probe and is never a verdict.

## Planted cases (before the wall; same `ric_num` function)

| id | case | expected |
|---|---|---|
| PL1 | #77's P1 and P2 quotient blocks (`three_scalars.planted_geometry`, block of M = R - lam g, K normalised by `kernel`) through `ric_num` | all six det^2 Ric components 0: flat |
| PL1b | D1's block (fiber R^2 (1 + R^2/10)) | some component nonzero |
| PL2 | h = -dt^2 + dr^2 + G^2 dtheta^2, G = r (1 + W0), W0 = w the free function (weighted homogeneous, so r = 1 is allowed) | N_rr = -G^3 G'', N_thth = -G^5 G'' with G'' = 2 W1 + r W2. In u: the ideal is ((1 + u0)^3 (2 u1 + u2)); solutions 2 u1 + u2 = 0 (flat: G'' = 0) and the spurious u0 = -1 (det h = 0). After saturating by det h the ideal is (2 u1 + u2), and with 1 - s u1 it is not unit. |
| PL3 | wall numerators with constants shifted, f_i - f_i(j*), j* a random rational jet with W1* != 0 | not unit: the exact point j* is in the variety |

## Certificate format

`certs/<case>.json`: `{"ring": ["s","u0",...], "generators": "<how regenerated>", "gen_sha256": ..., "cofactors": [poly strings]}`.
Polynomials are written `3*u0^2*u1-5/2*u2` as Singular prints them. The default mode of the script regenerates the
generators in sympy, parses the cofactors exactly, and checks sum c_i f_i - 1 = 0 in ℚ[s, u0..u4] (sympy `ring`,
`QQ`). `--compute` runs Singular on `singular/<case>.sing`, stores `<case>.out`, `<case>.err`, `<case>.time`
(`/usr/bin/time -v`: peak resident size) and writes the certificate. Singular input and output stay in this folder.

## Checks (names)

| check | tests |
|---|---|
| `num_cross` | `ric_num` times det^2 agrees with `three_scalars.ricci_pt` on h at 6 exact points of the wall, exactly |
| `num_weights` | N is weighted homogeneous and linear in W4; N = A(c) + S B(c) |
| `planted_blocks` | PL1, PL1b |
| `planted_family` | PL2 |
| `planted_root` | PL3 |
| `coef_reassemble` | J_all's coefficients reassemble N at 7 exact (c, S) points, exactly |
| `wall_<rung>` | the verdict of each rung; "unit" requires `cert_verify_<rung>` |
| `cert_verify_<rung>` | sum c_i f_i - 1 = 0, exactly |

## Controls (`--mutate=NAME`), targets declared now

A control must make the script exit non-zero. Only the targets named here are claimed; a control that is silent on its
named target is reported silent.

| mutation | change | declared target |
|---|---|---|
| `num-sign` | the Gamma Gamma term of the Ricci numerator gets the opposite sign | `num_cross` |
| `num-det` | the det * (A d2Gamma) term loses the factor det | `num_cross` |
| `coef-drop` | the highest-c-degree coefficients are dropped from J_all | `coef_reassemble` |
| `cert-corrupt` | 1 is added to the constant term of the first nonzero cofactor | `cert_verify_*` |
| `cert-satoff` | the verification drops the generator 1 - s u1 | `cert_verify_*` |
| `plant-sat` | PL2 without the saturation by det h | `planted_family` |
| `flat-sub` | h replaced by diag(-1, 1, 1) | `wall_*` |
| `rung-equator` | the wall verdict taken from R1 alone | `wall_R3`, if R1 is not unit and R3 is |

Later targets (the ODE step, if the ideal is not the unit ideal) are added as dated amendments below, never edited here.

## Run rules

One process, `nice -n 10`, one thread. Any run longer than a few minutes is a systemd user unit (`nm-i157-<step>`) with
absolute paths and an exit-code file. Stop condition: any single run not finished after 1 h of wall time is stopped and
reported with what finished. Memory is logged, never a stop condition. Every log is kept; a rerun gets a new number.
Nothing is deleted.

## Files (filled in as they appear)

- `singular/`, `certs/`, `logs/` as above. `<step>_runN.log` + `<step>_runN.rc` for each Python run.

## Amendments

(none yet)
