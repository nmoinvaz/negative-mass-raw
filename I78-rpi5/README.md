# I78-rpi5: logs of notes/warp/same_sign_scalars.py (two scalars of one sign, Alcubierre wall)

Machine rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process, one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/78. Branch `wip/i78-same-sign`, worktree
`~/Source/negative-mass-i78`. Python `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0, mpmath 1.3.0).
Written 2026-11-24, before the first run of the script. Stop condition: a single run not finished after 1 h of wall
time is stopped and reported.

## Question

Two minimally coupled scalars of one sign, (+,+) or (-,-), with any potential V. Pointwise
R_ab = lam g_ab + s (a_a a_b + b_a b_b), s = +1 or -1, lam = 8 pi V, a, b = sqrt(8 pi) d phi_I. The test has four stages,
as in two_scalars.md (#65):

1. algebraic: some real lam makes M = R - lam g semidefinite (positive for s = +1, negative for s = -1) of rank <= 2;
2. closure: some O(2) rotation Lambda(x) of (a, b) makes both closed. For a rank-2 form M with kernel plane field
   K this holds iff (i) K is integrable, (ii) L_X M = 0 for X in K, (iii) the quotient 2-metric q of M by K is flat
   (Gauss curvature 0). Claim to test, with a proof by hand in the note;
3. potential: K(lam) = 0 on the kernel, so lam is a function of the fields;
4. residual: G_ab - 8 pi T_ab = 0 with the fields substituted back.

## Claims the script tests, and the criteria (each can fail)

Algebraic stage on the wall (by hand, to be checked by the script). Let R_a3 = 0 and R_00 + R_11 + 2 R_22 = 0 ((I1),
(I2) of #57), N = R_3 - lam eta_3 on (E_0, E_1, e_rho). Then M = N + (-lam): the form holds iff R = 0 or lam != 0 and
rank N = 1. The sign is automatic: (+,+) iff lam < 0, (-,-) iff lam > 0 (weighted trace of N is -2 lam). A necessary
condition without lam or case split: F = R_01 (R_0rho^2 + R_1rho^2) + 2 R_rho,rho R_0rho R_1rho = 0, from the minors
N_00 N_1rho - N_01 N_0rho and N_11 N_0rho - N_01 N_1rho and (I2). On the wall (w' != 0) F is s^2 c^2 times a polynomial
in s^2 whose constant term is 2 w' (u^2 + v^2) with u = r w'' - w', v = w u + 2 r w'^2; u = v = 0 forces w' = 0. So at
each r the angles that pass are finitely many and no open set passes. For the accelerating bubble A = v_s'/v_s enters
R_00, R_11, R_1rho and the c^0, c^1 coefficients of the bracket force w' = 0 when A w' != 0.

| id | criterion |
|---|---|
| C1 | planted forms: 12 random lam eta + s (a a + b b), six with s = +1 and six with s = -1, in random rational Lorentz frames, lam of either sign: the algebraic stage returns lam with pattern (+,+) resp. (-,-) at all 12. 12 random forms with squares (+,-), (-,+), (+,+,+), (-,-,-), (+,+,-), (+,-,-), two of each: no admissible root at all 12 |
| C2 | lemma on 24 random tensors with (I1), (I2), each in a random Lorentz frame, 8 of each kind: (i) R_3 = lam eta_3 + eps n n^T with lam fixed by the weighted trace, (ii) a mixed rank-2 R_3 = a a^T - t b b^T (passes #65, fails here), (iii) a generic R_3. The test's outcome (found or not, and the pattern) equals the prediction from the 3 x 3 criterion "some real lam != 0 has rank(R_3 - lam eta_3) = 1" computed by exact 2 x 2 minors, at all 24 |
| C3 | planted metrics P1 = AdS_2 x R^2 (two normal scalars, lam = -1) and P2 = dS_2 x R^2 (two phantoms, lam = +1), in sheared polar coordinates, pass all four stages: lam is a root with inertia (2,0) resp. (0,2) at 3 exact points; the kernel basis commutes, L_X M = 0 for both vectors, the quotient is flat; Lambda(x) is built from the Lagrange split, satisfies Lambda A = J, Lambda^T Lambda = 1, J^T S J = M, and varies with the point; K(lam) = 0; G - 8 pi T = 0 |
| C4 | deformed metrics pass the algebraic stage at their planted lam (inertia (2,0) or (0,2)) and fail closure at their own sub-test. D1: plane R^2 -> R^2 (1 + R^2/10): kernel integrable, L_X M = 0, quotient not flat. D2: ds^2 = -dtau^2 + dz^2 + E^2 (dX^2 + dY^2), E = 1 + (z^2 - tau^2)/10, lam = -4 gamma / E with gamma = 1/10 (exact solution of the rank-2 condition off shell): L_X M != 0 and K(lam) != 0. D3: the shift b = C ln rho + b_0 (ds^2 = -dt^2 + (dx + b dt)^2 + drho^2 + rho^2 dphi^2): algebraic stage passes on an open set with lam = h = C^2/(2 rho^2), inertia (0,2), kernel not integrable |
| C5 | wall, constant v, general profile, symbolic: (i) R(e_phi, .) = 0 and (I2); (ii) the entries 2 r R_01 = -(2 w' + u s^2), 2 r R_0rho = u s c, 2 r R_1rho = v s c, R_rho,rho = w'^2 s^2/2; (iii) F = s^2 c^2 (-z (u^2 + v^2) + 2 r u v w'^2 s^2)/(8 r^3) and the certificate R_0rho m_d + R_1rho m_e + F = 0 for the generic N(lam); (iv) the ideal of the two s^2 coefficients with 1 - zz w' r is the unit ideal; (v) R_ab at lam = 0 is indefinite (both signs) at every off-axis exact point |
| C6 | wall exact points (32 points of #77: tanh sigma = 8 R_b = 1 with v = 1, 1/2, 3; bump (1 - r^2/4)^3 with v = 7/4; random jets; on and off the axis, one on the equator): the same function as C1 finds no admissible root, lam = 0 or lam != 0, at every point |
| C7 | accelerating bubble: (i) route D's frame block depends on (w~, w~', w~'', A) only (as #65's acc_jets); (ii) the entries differ from the constant-speed ones by R_00 += A w' c, R_11 -= A w' c, R_1rho = s (v c - A r w')/(2 r); (iii) the bracket B(c) of F has c^0 coefficient -(2 w' + u) A^2 r^2 w'^2 and c^1 coefficient 2 A r w' (v (2 w' + u) - r w'^2 u), and with A w' r != 0 all coefficients generate the unit ideal; (iv) at v_s = 0 (w' = 0, k = v_s' f' != 0) N has rank >= 2 at every off-axis point; (v) 6 exact points with random jets and v_s' != 0: no admissible root |
| C8 | shifts b(rho): the rank-1 condition has the solutions Q = 0, lam = h (h != 0) and no other (Groebner basis), i.e. b'' + b'/rho = 0, b = C ln rho + b_0; D3 of C4 is this shift |

Closure on the wall is reached only where the algebraic stage passes on an open set. C5 and C7 assert that this never
happens for the wall, so the wall's closure stage has no input. The closure code is exercised by C3, C4 and D3.

Status words for the verdict: the identities of C5 and C7 are *checked symbolically*; the argument from them to "no
open set passes" is *proved* by hand. The verdict does not use #65's lemma or its determinant ideal (#79, not yet
reviewed). It uses #57's (I1), (I2) and frame Ricci tensor (#59). The tanh points of C6 have rounded jets (numerical
evidence); the general-profile result does not depend on them.

## Controls (`--mutate=NAME`), written before the first run

Every control must make the script exit non-zero, with at least these target checks failing.

| mutation | change | target checks |
|---|---|---|
| planted-sign | planted forms built as lam eta + a a - b b | planted_pass |
| planted-fail-sign | planted failures built as two squares of one sign | planted_fail |
| lemmaS-weight | samples with R_00 - R_11 + 2 R_22 = 0 in place of (I2) | lemmaS_samples |
| p1-mixed | P1's plane given signature (-,+): -dR^2 + R^2 dTheta^2 | p1_algebraic |
| p2-mixed | the same for P2 | p2_algebraic |
| p1-fiber | P1's plane curved, R^2 (1 + R^2/10) | p1_closed |
| p1-lambda | lam + T/10 in P1's potential stage | p1_potential |
| p2-lambda | lam + T/10 in P2's potential stage | p2_potential |
| p1-sign | one kinetic sign flipped in T of P1 | p1_residual |
| p2-sign | one kinetic sign flipped in T of P2 | p2_residual |
| d1-flat | D1's curvature set to 0 | d1_closure_fails |
| d2-gamma0 | D2 with gamma = 0 (M = 0) | d2_algebraic, d2_closure_fails |
| d3-bracket | the commutator of the kernel basis computed without the term K_2(K_1^mu) | d3_closure_fails |
| alc-drop-w2 | shift's square dropped from g_tt in the spherical route (as in phantom_source.py) | wall_identities, wall_entries, wall_F |
| wall-F-sign | the claimed F formula with +z in place of -z | wall_F |
| ideal-nosat | the ideal without the saturation 1 - zz w' r | wall_ideal |
| wall-planted | R at the off-axis exact points replaced by a planted lam eta + a a + b b | wall_points |
| wall-psd | R at the off-axis exact points replaced by a positive definite tensor | wall_lambda0 |
| acc-static | every t-derivative dropped from route D's jets (as #65) | acc_entries |
| acc-drop-A | the A terms dropped from the expected entries | acc_entries |
| acc-drop-odd | only the even powers of c in the accelerating ideal | acc_ideal |
| brho-q | the expected rank-1 solution with Q = h in place of Q = 0 | brho_rank1 |

Predictions: each target fails and nothing else needs to. A control that is silent, or that fires another check, is
reported, not adjusted.

## Files

- `final.log`, `final.rc`: stdout and exit code of the final run.
- `ctl_<name>.log`, `ctl_<name>.rc`: one per control.
- `pilot_*.log`: runs while the script was written.
- `explore/`: scratch scripts and logs from before this README (not claims): `explore_alg0` (R_3 of the wall and its
  characteristic cubic), `explore_alg1` (the entries in u, v, z, F, the certificate), `explore_acc0` (route D's R_3 with
  A), `explore_iso0` (a numerical search for isolated wall points that pass the stage).

## Changes and results recorded after this README

### 2026-11-24, after pilots 1 to 5 and before the final run

Pilot logs: `pilot_01_stop2.log`, `pilot_02_stop3.log` (stopped by hand after 2 min 52 s inside D1's `closure2`, see
below), `pilot_03_stop3.log`, `pilot_04_stop5.log`, `pilot_05_full_nocontrols.log` (all sections, 27 s, ~100 MB:
30 of 31 checks pass, `brho_rank1` fails), `pilot_ctl_<name>.log` for the first three controls.

- **Geometry change in the planted metrics.** The first shear, Ro = Rn + T/3 + Z/11, made `closure2` on D1 run for more
  than 2 min 52 s (killed, log kept). The final shear is to = T + Z/3, zo = Z, Ro = Rn, Tho = Th + T/7 + Z/5. The kernel
  vectors K_1 = d_T - d_Th/7, K_2 = d_Z - d_Th/5 are still not coordinate vectors and Lambda(x) still depends on the
  point. No criterion changes. Section 3 now takes 6 s.
- **C8 as coded: FAIL.** `brho_rank1` tested equality of ideals, <minors, 1 - zz h> = <lam - h, Q, 1 - zz h>
  (`pilot_05_full_nocontrols.log`). The inclusion "minors in <lam - h, Q>" holds, the converse does not: the Groebner
  basis with h != 0 is {lam - h, Q^2} (`explore/explore_brho_radical.log`), so the ideal is not radical. The criterion C8
  says "has the solutions Q = 0, lam = h (h != 0) and no other", a statement about the zero set. The code tested more
  than the README says. The failing log stays as the record.
- **C8 recoded as worded (coordinator, hc 2026-11-24), written before the rerun.** Let I be the ideal of the nine 2 x 2
  minors of R_3 - lam eta_3 (symbols lam, h, Q) and I_h = I + <1 - zz h> the saturation by h. (a) Every generator of I
  reduces to 0 modulo <lam - h, Q>: the points lam = h, Q = 0 are solutions. (b) lam - h and Q are in the radical of
  I_h: 1 is in I_h + <1 - y (lam - h)> and in I_h + <1 - y Q> (Rabinowitsch, no exponent chosen). Both directions pass
  or the check fails. The basis {lam - h, Q^2} is printed as information and does not gate the result. The rest of the
  check (R_3 of b(rho) equals [[-h, Q, 0], [Q, -h, 0], [0, 0, h]]; Q = 0 for b = C ln rho + b_0) is unchanged.
- **Control `brho-q` kept.** Expected solution lam = h, Q = h in place of Q = 0. Prediction: (b) fails for Q - h (Q - h
  is not in the radical, since lam = h, Q = 0 is a solution with h != 0) and (a) fails too (the generator
  h^2 - lam^2 - Q^2 equals -h^2 at lam = h, Q = h). Target check: `brho_rank1`.
- **Other facts recorded.** `explore_iso0`: 0 of 40 random trials found an isolated wall point that passes the stage
  (a weak search, not a claim). `lemmaS-weight`: 8 of the 24 samples disagree with the lemma in that control
  (`pilot_ctl_lemmaS-weight.log`), so it is strong. The first twenty controls (all but `brho-q` and `d3-bracket`) run
  as one detached batch (`run_controls.sh`, unit `nm-i78-ctl1`, `ctl_batch.log`) on the script at 714a211, before the
  C8 recoding; none of them reaches section 7.

## Results of the final run (2026-11-24)

Script `notes/warp/same_sign_scalars.py` at 479a357 (branch `wip/i78-same-sign`), run as systemd unit `nm-i78-final`
(`run_final.sh`): exit 0 in 351 s wall, stdout in `final.log` (same as `notes/warp/same_sign_scalars_output.txt`),
`final.rc` = 0, `final.err` empty. 31 of 31 checks pass, 22 of 22 controls fire. The checks alone take 26 s at 72 MB
peak resident (`mem_nocontrols.time`). `PYTHONHASHSEED` 1 and 42 give the same output apart from the timings
(`hashseed_1.log`, `hashseed_42.log`, empty `.diff` files).

| id | verdict | number |
|---|---|---|
| C1 planted forms and failures | pass | 12 of 12 recovered with lam and pattern; 12 of 12 failures without an admissible root |
| C2 lemma on 24 tensors | pass | 0 disagreements; `lemmaS-weight` makes 8 of 24 disagree |
| C3 planted P1 (+,+), P2 (-,-) | pass | all four stages; Lambda(x) error below 1e-60, varies by 0.61 and 1.01 between points |
| C4 deformed D1, D2, D3 | pass | D1 quotient not flat; D2 L_X M != 0, K(lam) != 0; D3 kernel not integrable ([K_1, K_2] = (0, 2/rho, 0, 0)) |
| C5 wall, general profile | pass | entries, F and the certificate exact; unit ideal (basis [1]); R indefinite at 25 of 25 off-axis points |
| C6 32 exact points | pass | no admissible root at any; off axis the rank-<=2 locus has no real root, on axis only lam = 0 with inertia (1,1) |
| C7 accelerating bubble | pass | entries, F, c^0 and c^1 coefficients exact; unit ideal; v_s = 0 block exact, unit ideal; 6 of 6 points |
| C8 shifts b(rho), as coded in the first run | **FAIL** | ideal equality with <lam - h, Q> fails; the basis is {lam - h, Q^2} (pilot_05) |
| C8 as recoded (a) and (b) | pass | (a) every minor reduces to 0 modulo <lam - h, Q>; (b) lam - h and Q in the radical (Rabinowitsch) |

Controls, from `final.log` (the logs `ctl_<name>.log` come from the earlier batch, `run_controls.sh`, and agree):

| mutation | target checks | failed in the final run | extra |
|---|---|---|---|
| planted-sign | planted_pass | FIRED, exit 1: planted_pass | - |
| planted-fail-sign | planted_fail | FIRED, exit 1: planted_fail | - |
| lemmaS-weight | lemmaS_samples | FIRED, exit 1: lemmaS_samples | - |
| p1-mixed | p1_algebraic | FIRED, exit 1: p1_algebraic | - |
| p2-mixed | p2_algebraic | FIRED, exit 1: p2_algebraic | - |
| p1-fiber | p1_closed | FIRED, exit 1: p1_closed | - |
| p1-lambda | p1_potential | FIRED, exit 1: p1_potential | - |
| p2-lambda | p2_potential | FIRED, exit 1: p2_potential | - |
| p1-sign | p1_residual | FIRED, exit 1: p1_residual | - |
| p2-sign | p2_residual | FIRED, exit 1: p2_residual | - |
| d1-flat | d1_closure_fails | FIRED, exit 1: d1_closure_fails | - |
| d2-gamma0 | d2_algebraic, d2_closure_fails | FIRED, exit 1: d2_algebraic, d2_closure_fails | - |
| d3-bracket | d3_closure_fails | FIRED, exit 1: d3_closure_fails | - |
| alc-drop-w2 | wall_identities, wall_entries, wall_F | FIRED, exit 1: wall_identities, wall_entries, wall_F | - |
| wall-F-sign | wall_F | FIRED, exit 1: wall_F | - |
| ideal-nosat | wall_ideal | FIRED, exit 1: wall_ideal | - |
| wall-planted | wall_points | FIRED, exit 1: wall_points, wall_lambda0 | wall_lambda0 |
| wall-psd | wall_lambda0 | FIRED, exit 1: wall_lambda0 | - |
| acc-static | acc_entries | FIRED, exit 1: acc_jets, acc_entries, acc_const_limit, acc_vs0 | acc_jets, acc_const_limit, acc_vs0 |
| acc-drop-A | acc_entries | FIRED, exit 1: acc_entries | - |
| acc-drop-odd | acc_ideal | FIRED, exit 1: acc_ideal | - |
| brho-q | brho_rank1 | FIRED, exit 1: brho_rank1 | - |

Two controls fire more checks than the README predicted: `acc-static` (the jets stop depending on the t-derivatives, so
`acc_jets`, `acc_const_limit` and `acc_vs0` fail as well) and `wall-planted` (the planted tensor has both signs, so
`wall_lambda0` fails as well). They are reported, not adjusted. `d3-bracket` was run twice (`ctl_d3-bracket.log`,
`ctl_d3-bracket_run2.log`): the second run follows a change of the check's message text only.

Commands and exit codes: pilot_01 (`--stop=2`) 0, pilot_02 (`--stop=3`) 143 (killed by hand), pilot_03 0, pilot_04
(`--stop=5`) 0, pilot_05 (all sections, no controls) 1 (`brho_rank1`); the batch of 20 controls and `brho-q`, `d3-bracket` all exit 1 (a fired control); the final
run exits 0.
