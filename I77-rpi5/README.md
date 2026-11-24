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
