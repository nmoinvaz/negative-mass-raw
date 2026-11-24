# I77-rpi5: logs of notes/warp/three_scalars.py (three scalars of mixed signs, Alcubierre wall)

Machine rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process, one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/77. Branch `wip/i77-three-scalars`, worktree
`~/Source/negative-mass-i77`. Python `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0, mpmath 1.3.0).
Written 2026-11-23, before the first run of the script.

## Question

Three minimally coupled scalars with kinetic signs (+, +, -) or (+, -, -) and any potential V. Pointwise,
R_ab = lam g_ab + sum_I s_I a^I_a a^I_b with lam = 8 pi V. The test has four stages, as in two_scalars.md (#65):
algebraic (some real lam makes R - lam g of rank <= 3 with at most 2 positive and 1 negative squares, or the mirror),
closure (some field-space O(2,1) or O(1,2) map Lambda(x) makes all a^I closed), potential (dlam in span(a^I)) and
residual (G - 8 pi T = 0 with the fields substituted).

## What the script claims, and the criteria (each can fail)

Closure for a rank-3 form M = R - lam g with kernel K is: L_K M = 0 and the quotient (the 3 x 3 block of M on a slice
transverse to K) is flat. With the Cartan structure equation da^I = -Omega^I_J a^J, Omega is the Levi-Civita connection
of that block, and Lambda exists iff its curvature vanishes. For the wall at lam = 0, K = d_phi and the block is the
orbit-space metric h on (t, r, theta). This is the claim to test, not a premise.

| id | criterion |
|---|---|
| C1 | the planted controls P1 (lam = 0, signs +,-,-) and P2 (lam = -3, signs -,+,+), in sheared coordinates, pass all four stages; Lambda(x) is built and is in O(p,q) with d(Lambda a) = 0 |
| C2 | the deformed controls D1 (curved fiber, K and L_K M fine, quotient not flat) and D2 (a(l) off shell, L_K M != 0) pass the algebraic stage and fail closure, each at its own sub-test |
| C3 | wall, lam = 0: rank 3 exactly where D = det R_3 != 0; signature (2,1) where D < 0 and (1,2) where D > 0; both patterns occur at exact points |
| C4 | wall, lam != 0: exact points list the real roots of det(R - lam g) with signatures; the admissible roots are counted |
| C5 | wall, lam = 0, general profile, constant v: Ricci numerators of h at several theta_0 generate the unit ideal with r w' != 0, so no open set of the wall admits closure. If they do not, the remaining variety is the result and no criterion changes |
| C6 | the same closure function, on explicit profiles at exact points: planted flat, wall not flat (Ricci of the block != 0 at every point) |
| C7 | wall, lam != 0, exact points: dlam(K) != 0 or L_K M != 0 at every admissible root (numerical evidence, 50 digits) |
| C8 | accelerating bubble: exact points with random jets, same function, and the stated reduction to constant v |

Not a claim: rank <= 2 remainders with two squares of one sign (two scalars of one sign, #78). They are listed.

## Controls (`--mutate=NAME`), written before the run

Every control must make the script exit non-zero, with exactly these target checks failing (at least).

| mutation | change | target checks |
|---|---|---|
| planted3-sign | planted forms built as lam eta + a a + b b + c c | planted3_pass |
| planted3-fail-sign | planted failures built with an admissible pattern | planted3_fail |
| lemma3-weight | samples with R_00 - R_11 + 2 R_22 = 0 in place of (I2) | lemma3_samples |
| p1-sign | one scalar's kinetic sign flipped in T | p1_residual |
| p2-lambda | lam + 1/10 in the potential stage | p2_potential |
| p2-fiber | P2's fiber curved | p2_closed |
| d1-flat | D1's curvature set to 0 | d1_closure_fails |
| d2-onshell | D2's a(l) set to the P2 solution | d2_closure_fails |
| alc-drop-w2 | shift's square dropped from g_tt in the wall (as in phantom_source.py) | wall_identities, wall_D, wall_points |
| wall-flat-sub | the wall's block replaced by a flat one | wall_flat_points |
| ideal-equator-only | only the equator numerators in the ideal | wall_flat_ideal |
| lam-const | the wall's lam made constant in the potential test | wall_lam_potential |

Predictions: each target fails and nothing else needs to. A control that is silent is reported, not adjusted.

## Files

- `final.log`: stdout of the final run (exit code in `final.rc`).
- `ctl_<name>.log`, `ctl_<name>.rc`: one per control.
- `pilot_*.log`: earlier runs while the script was written.

## Changes and results recorded before the final run (2026-11-23, after the pilots)

Pilot logs: `pilot_full_nocontrols.log` (+ `.time`: 118 s, 86 MB peak) at b56280c, `pilot_ctl_<name>.log`.

- **C7 as coded failed.** README's C7 is "dlam(K) != 0 or L_K M != 0 at every admissible root". The pilot at b56280c
  coded only K(lam) != 0 and gave: K(lam) != 0 at 23 of 27 admissible roots lam != 0, K(lam) = 0 at 4, all four at
  c = 0 (the equator). "C7 as coded: FAIL at 4 of 27 roots, all at c = 0." The log stays as `pilot_full_nocontrols.log`.
  The coordinator ruled (hc, 2026-11-23): compute C7 as written, with L_K M at the 4 roots, before any change.
- **C5 is not decided.** The Groebner computation on the equator Ricci numerators did not finish (killed at 20 min,
  one run of the modular variant at 20 min). No `wall_flat_ideal` check exists, so the control `ideal-equator-only` is
  *not run*. The arbitrary-profile ideal step is a follow-up for the coordinator.
- **Checks added after the README was written** (all in the pilot): `wall_flat_explicit` (C6, explicit bump profile),
  `acc_const_limit` and `acc_flat_points` (C8). Control added: `acc-static` -> `acc_const_limit`. Predictions: the
  lab-route Ricci tensor of the accelerating block equals the comoving polar one only if the t-derivatives are kept;
  dropping them breaks `acc_const_limit`. `wall-flat-sub` has targets `wall_flat_points` and `wall_flat_explicit`
  (the explicit one is not substituted, so only `wall_flat_points` is predicted to fire).
- **C7 as written, the test and its control.** At every admissible root lam != 0 the script computes (a) K(lam) from the
  implicit-function theorem and (b) L_K M of M = R - lam g along its kernel K, as fields, at 120 digits, by central
  differences (h = 1e-35) of lam, K and M on the Taylor polynomial of w with the point's jets W0..W3. C7 passes iff
  (a) != 0 or (b) != 0 at every root (relative size > 1e-8). The independent finite-difference K(lam) must agree with
  (a) to 1e-20, else the check fails. Control `lam-const`: takes d lam = 0 and L_K M = 0 at every root; target
  `wall_lam_potential`, which must then fail. (Coordinator's step 3, C7b, is added to this README only if L_K M = 0 at
  one of the 4 equator roots.)
- **C7 as written: PASS** (pilot `pilot_c7_written.log`, b56280c + the OR test). L_K M != 0 at all 27 admissible
  roots, including the 4 roots at c = 0 (relative sizes 1.5e+01, 3.5e+01, 3.6e+00, 1.0e+00); K(lam) alone != 0 at 23 and
  = 0 at 4, all four at c = 0. The finite-difference K(lam) agrees with the implicit-function one to 5e-67. C7b is
  therefore not written. The line "C7 as coded at b56280c: FAIL at 4 of 27 roots, all at c = 0" stays in the record.
- Controls added: `lie-dk` (drops the dK terms of L_K M; target `wall_lam_potential`, which tests the identity
  (L_K M)(K, .) = 0 inside its condition) and `acc-static` (target `acc_const_limit`); `lam-const` now takes d lam = 0
  and L_K M = 0 at every root (target `wall_lam_potential`). Each control stops after the last section holding its
  targets (`STOP_AT` in the script); the targets are unchanged.
