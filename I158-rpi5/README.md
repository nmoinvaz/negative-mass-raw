# I158-rpi5: logs of notes/warp/one_sign_classify.py (shifts that pass the one-sign scalar stage on an open set)

Machine rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process, one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/158. Branch `wip/i158-one-sign`, worktree
`~/Source/negative-mass-i158` (main 548a59a). Python `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0,
mpmath 1.3.0). Written 2026-11-24, before the first run of the script. Stop condition: a single run not finished after
1 h of wall time is stopped and reported. Memory is reported, never a stop condition.

## Question

Shifts b(t, x, rho) of ds^2 = -dt^2 + (dx + b dt)^2 + drho^2 + rho^2 dphi^2. With (I1), (I2) of #57 the one-sign
algebraic stage holds iff R = 0, or lam != 0 and rank(R_3 - lam eta_3) = 1 on the frame (n, d_x, e_rho), n = d_t - b d_x
(Lemma S of #78). It implies F = R_01 (R_0rho^2 + R_1rho^2) + 2 R_rhorho R_0rho R_1rho = 0. For each reduction below:
which solutions exist on an open set, is any localized in x, and what does closure (Lemma K of #78) say about each
family that passes. Localization is #80's definition: on a strip, u(., rho) has limits as x -> +-infinity for each rho
and u_x != 0 (compact support is the limit 0); "bubble-like" adds u_rho != 0.

Notation (#80): block R_3 = [[P - h, Q, Z], [Q, -P - h, Y], [Z, Y, h]], P = n(b_x) - b_x^2, Q = -(b_rhorho + b_rho/rho)/2,
Z = b_xrho/2, Y = -n(b_rho)/2 + b_x b_rho, h = b_rho^2/2. Static or traveling b = B(x - vt, rho) is the static shift
u = B + v. In the static case n = -u d_x.

## Hand results the script is to check (each is stated in the note with its status word)

- **Lemma R** (by hand). For real lam != 0, rank(R_3 - lam eta_3) = 1 iff N = -v v^T for v in R^3 when h > 0, with
  P = -(v0^2 + v2^2), Q = -v0 v1, Z = -v0 v2, Y = -v1 v2, h = (v0^2 + v1^2)/2, lam = h + v2^2 > 0, so the pair is two
  phantoms. When h = 0 (b_rho = 0) the condition is Q = Z = Y = 0 and lam = -P != 0, either sign.
- **Lemma E** (by hand, ends). If the second jets of u converge along x -> +-infinity to (P, Z, Y) = 0, the limit
  satisfies Q = 0, so u_+- = C_+- ln rho + b_+-.
- **b(rho)**: b = C ln rho + b_0 (planted), fails closure.
- **Planar b(t, x)**: every planar shift passes with lam = K = -P = -a_x, a = b_t - b b_x; closure iff K is constant; K
  constant != 0 is AdS_2 or dS_2 x R^2 (#78's P1, P2); **Theorem P**: no such shift is bounded at fixed t over x, so
  none is localized.
- **Additive Z = 0 (u = X(x) + R(rho), + v)**: with R' != 0 and X' != 0 the solutions are u = c x + C ln rho + d; closure
  fails for C != 0 (non-integrable kernel) and passes for C = 0 (the planar K = c^2).
- **Multiplicative u = X R + v**: F = 0 alone leaves only X' R' = 0 (b(rho) or planar).
- **Conical u = F(x/rho) + v** (static and traveling alike): no solution with F' != 0 on an open set.
- **Spherical profile u = w(r)** (the bubble at constant speed, #78): F = s^2 c^2 B/(8 r^3), no open set passes.
- **General static Z != 0**: reduced to two resolved second-order equations plus the free mixed derivative; the
  compatibility condition C of the resulting finite-type system is not identically zero. Not classified.

## Criteria (each can fail)

Every criterion is exact (sympy rational or symbolic) unless it says "60-digit". `rank1_lams` and `same_sign_form` are
the functions of #78's `same_sign_scalars.py`, imported unchanged. `closure2` likewise (Lemma K).

| id | check name | criterion |
|---|---|---|
| C1 | `block` | For ds^2 with an undefined function b(t, x, rho), the coordinate Ricci tensor (phantom_source.ricci) on the frame (n, d_x, d_rho) equals the block above in all six entries, R(e_phi, .) = 0, and R_00 + R_11 + 2 R_22 = 0 |
| C1b | `travel` | For b = B(x - vt, rho) the five jets (P, Q, Z, Y, h) equal those of the static shift u = B + v (symbolic jets); for b~(t, x) = b(t, x - D(t)) - D'(t), the five jets at (t, x) equal those of b at (t, x - D(t)) (`gauge`, same check name `travel`) |
| C2 | `lemmaR` | (a) N = R_3 - (h + v2^2) eta_3 = -v v^T identically in symbolic v for the block built from v; (b) F = 0 on it; (c) R_0rho m_d + R_1rho m_e + F = 0 for a generic symbolic R_3 with (I2), m_d = N00 N1rho - N01 N0rho, m_e = N11 N0rho - N01 N1rho; (d) planted: 16 random rational v (h > 0): `rank1_lams` returns exactly [(h + v2^2, 'MM')]; 8 random planar blocks (h = Q = Z = Y = 0, P != 0): exactly [(-P, 'PP' if P > 0 else 'MM')]; P = 0: []; 16 random generic (P, Q, Z, Y, h > 0) with F != 0: [] |
| C3 | `brho_solve` | Block of b(rho) = [[-h, Q, 0], [Q, -h, 0], [0, 0, h]] (substituted into the generic block). With P = Z = Y = 0 in Lemma R's five equations, v0 and v2 lie in the radical of the ideal (Rabinowitsch, exact), so Q lies in it, and lam = h; dsolve of Q = 0 gives b = C1 + C2 ln rho. This is also Lemma E |
| C4 | `brho_points` | b = 2 ln rho + 1/3 (4D Ricci, ln rho as a symbol with derivative 1/rho): at 3 exact points `same_sign_form` has a root lam = h with inertia (0, 2) and pattern MM. Planted failure: b = 2 ln rho + rho^2/10: at 3 exact points no candidate has an admissible pattern |
| C5 | `brho_closure` | For b = 2 ln rho + 1/3, `closure2` of M = R - h g: kernel dimension 2, plane not integrable (planted closure failure, #78's D3) |
| C6 | `planar_stage` | (a) The block of a generic planar b(t, x) is diag(P, -P, 0) and lam = K = -P is the only root; (b) 4D, exact points: b = (3/2) x (K = 9/4), b = tan(t) x (K = -1), b = -tanh(t) x (K = 1): `same_sign_form` has the root lam = K with inertia (0, 2), (2, 0), (0, 2) at 3 exact points each; (c) K = -(b_tx - b b_xx - b_x^2) = -a_x as an identity |
| C7 | `planar_closure` | `closure2` of M = R - K g for the three metrics of C6: kernel dimension 2, integrable, L_X M = 0, quotient flat. For b = x^2/10 and b = 1/(1 + x^2): kernel dimension 2, integrable, L_X M != 0 |
| C8 | `planar_thm` | Theorem P's steps: the ODE x'' = K0 x - alpha(t) along dx/dt = -b when b_t - b b_x = -K0 x + alpha(t) (symbolic chain rule), the closed-form solution x_X(t) solves it, and b(t*, x_X(t*)) = -x_X'(t*) is linear in X with slope -kappa sinh(kappa (t* - t1)) (K0 = kappa^2) or kappa sin(kappa (t* - t1)) (K0 = -kappa^2); the three planar solutions of C6 are linear in x |
| C9 | `additive_block` | For u = X(x) + R(rho) + v the block is Z = 0, Y = X' R', Q = -S/2 (S = R'' + R'/rho), P = -(u) X'' - X'^2, h = R'^2/2 (substitution into the generic static block) |
| C10 | `additive_solve` | With X' R' != 0, S, (X + R) X'' (u without v; with v: u = X + R + v) and v0 lie in the radical of Lemma R's ideal (Rabinowitsch); X'' alone does not (reported). By hand: X'' = 0, u = c x + C ln rho + d. `rank1` branch X' = 0 is b(rho) |
| C11 | `additive_points` | u = 3/2 x + 2 ln rho + 1/5 and u = x + 3 ln rho: at 3 exact points `same_sign_form` has the root lam = C^2/(2 rho^2) + c^2 with inertia (0, 2). Planted failure: u = 3/2 x + 2 ln rho + x^2/10: no admissible candidate at 3 exact points |
| C12 | `additive_closure` | `closure2` of M = R - lam g for the two shifts of C11: kernel dimension 2, plane not integrable. For u = x (C = 0): integrable, L_X M = 0, flat |
| C13 | `mult` | For u = X R + v: F = -X X'^2 R'^2 (S (1 + W^2) - 2 X R'^2 W)/8 with W = 3 X R + v, identically; the three coefficients of X^2, X, 1 in S (1 + W^2) - 2 X R'^2 W and 1 - t R R' generate the unit ideal |
| C14 | `conical_entries` | For u = F(x/rho) + v (U = F + v): rho^2 (P, Q, Z, Y, h) = (-(G^2 + U H), -eta w/2, -w/2, -(eta G^2 + U w/2), eta^2 G^2/2), w = G + eta H, G = F', H = F''; Q = eta Z |
| C15 | `conical_solve` | Lemma R's five equations in these jets, saturated by eta G U w: E_a = w (1 + U^2) + 2 eta U G^2 and E_b = (eta^2 + 1) eta H + (eta^2 - 1) G reduce to 0 modulo the Groebner basis; the branch w = 0 with 1 - t eta G U is the unit ideal. dsolve of E_b (H = G') gives G = C eta/(eta^2 + 1); then E_a is 1 + F^2 + C eta^2 F = 0 (C != 0), its derivative gives F = -C eta^2/(2 (eta^2 + 2)), and G - F' = C eta ((eta^2 + 2)^2 + 2 (eta^2 + 1))/((eta^2 + 1)(eta^2 + 2)^2) != 0 for C eta != 0 |
| C16a | `bubble_F` | For u = w(r), r = sqrt(x^2 + rho^2), with jets w0, w1, w2: 8 r^3 F = s^2 c^2 (-z (a1^2 + a2^2) + 2 r a1 a2 w1^2 s^2) times 1, a1 = r w2 - w1, a2 = w0 a1 + 2 r w1^2, z = 2 w1 + a1 s^2 (identically, with chain-rule jets checked against a sample w); the two coefficients of s^0, s^2 of the bracket and 1 - t w1 r generate the unit ideal |
| C16b | `bubble_points` | 20 exact points (random w0, w1 != 0, w2, r, and (s, c) from a rational angle with s c != 0): `rank1_lams` of the block returns [] at all 20 |
| C17 | `static_system` | With h > 0, Z Y Q != 0: A = Q (Z^2 + Y^2) + 2 h Z Y and B = P Q Y - Z (Q^2 + Y^2) lie in the radical of Lemma R's ideal saturated by Z Y Q (Rabinowitsch). Parametrization v0 = beta cos(th), v1 = beta sin(th), v2 = a/(u cos th - sin th), beta = u_rho, a = u_x: the five entries built from u_xx = Phi1, u_xrho = Psi, u_rhorho = Phi3 reproduce Lemma R's relations identically. Planted: on the jets of u = c x + C ln rho + d (s = tan(th/2) = 1) the two compatibility equations E1, E2 hold with sigma = 0 and the compatibility C vanishes at 6 exact points |
| C18 | `static_compat` | At 3 exact points (rho, u, a, beta, s) with s not in {0, 1, -1}: the 2 x 2 matrix of (E1, E2) in (sigma_x, sigma_rho) has non-zero determinant and C != 0. This is a result either way; it decides "not Frobenius closed" |
| C19 | `linearized` | For u = u0 + eps w, u0 = C ln rho + b0 (C u0 != 0), the O(eps) parts of Z and P are w_xrho/2 and -u0 w_xx, and those of the other three relations of Lemma R's reduced form (Z v1^2 = -Q Y, P v1^2 = -(Q^2 + Y^2), v1^4 - 2 h v1^2 + Q^2 = 0) vanish identically at O(eps) in Z, P; hence w_xrho = 0 and w_xx = 0, w = c x + g(rho) (symbolic expansion, then by hand) |

Closure is reached only on a family that passes the algebraic stage on an open set: b = C ln rho + b_0 (C5), planar
(C7), additive (C12). Multiplicative, conical and spherical profiles have no input for it. The general static Z != 0 case
is not classified, and has no closure test.

Status words for the note: C1, C1b, C2, C9, C14, C16a identities, the Groebner membership of C3, C10, C13, C15, C17,
and the exact points are **checked symbolically**; the passages from them to the open-set statements, Lemma R, Lemma E,
Theorem P, the additive and conical case analyses are **proved** by hand. C18 and the part of C17 on C are **checked
symbolically** at exact points. The statement about the general static class is "not classified".

## Controls (`--mutate=NAME`), written before the first run

Every control must make the script exit non-zero, with at least the target checks failing.

| mutation | change | target checks |
|---|---|---|
| block-Y-sign | Y built as +n(b_rho)/2 + b_x b_rho | block |
| travel-offset | u = B without + v | travel |
| gauge-drop | the gauge-transformed shift without - D'(t) | travel |
| lemmaR-sign | planted blocks built with P = +(v0^2 + v2^2) | lemmaR |
| lemmaR-F | F with 2 h Z Y replaced by h Z Y | lemmaR |
| brho-Q | claimed rank-1 solution with Q = h in place of Q = 0 | brho_solve |
| brho-pert | the planted solution replaced by b = 2 ln rho + rho^2/10 | brho_points |
| brho-bracket | the kernel commutator without the term K_2(K_1^mu) (as #78's d3-bracket) | brho_closure |
| planar-sign | lam expected as +P in place of -P | planar_stage |
| planar-constK | the two planar shifts that must fail closure replaced by b = x and b = 2 x | planar_closure |
| planar-ode | the comoving ODE with x'' = -K0 x + alpha | planar_thm |
| add-quad | the claimed radical membership of X'' in place of (X + R) X'' | additive_solve |
| add-pert | the planted solution replaced by u = 3/2 x + 2 ln rho + x^2/10 | additive_points |
| add-bracket | the kernel commutator without the term K_2(K_1^mu) | additive_closure |
| mult-W | W = 2 X R + v in the claimed F | mult |
| conical-Q | Q = -eta w in place of -eta w/2 | conical_entries |
| conical-Eb | E_b with (eta^2 - 1) replaced by (eta^2 + 1) | conical_solve |
| bubble-sign | the claimed bracket with +z in place of -z | bubble_F |
| bubble-planted | the block at the exact points replaced by a planted rank-1 block | bubble_points |
| compat-Phi1 | Phi1 built with the opposite sign of a^2 | static_system |
| lin-claim | the claimed first-order part of P with +u0 w_xx | linearized |

A control that is silent on its target, or that crashes before its target runs, is reported as silent, and the target
list is not edited after a run without saying so here, in the note and in the closing comment.

## Not criteria (reported, not gating)

Values of C and determinants at the exact points of C18; the number of generators of each Groebner basis; timings;
which of the five Lemma R relations the non-solution of C10's X'' membership violates. The general static Z != 0 class,
time-dependent shifts beyond the planar and gauge-equivalent ones, the Galilean-dilation similarity forms
b = mu ln rho + F((x - mu t ln rho)/rho, t/rho), three or more scalars, non-axisymmetric shifts and non-minimal coupling
are not classified.

## Files

Every stdout goes to a log in this folder: `run_<n>.log` for the checks, `ctl_<mutation>.log` and `.rc` for each
control. Reruns are numbered, never overwritten.
