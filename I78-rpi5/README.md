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
