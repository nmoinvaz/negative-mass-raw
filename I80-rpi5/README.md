# I80-rpi5: classification of the shifts b(t, x, rho) whose det R_3 vanishes on an open set (#80)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10, one thread.
Issue: https://github.com/nmoinvaz/negative-mass/issues/80
Worktree: `~/Source/negative-mass-i80`, branch `wip/i80-det-classify` (base main e68973a, after #79's merge).
Python: `~/Source/negative-mass-venv314/bin/python` (3.14.10, sympy 1.14.0, mpmath 1.3.0, numpy).
Script: `notes/warp/det_classify.py` (`--no-controls`, `--mutate=NAME`; exits 1 on a failed check or a silent control).

## What was done before this README (not committed, not part of any run)

Scratch sympy sessions, in the session's scratchpad, to find what to ask. They found, in this order, and the
criteria below are written to test exactly these statements, not to confirm a result:
1. The block of #65 with a = b_t - b b_x: P = a_x, Y = (b_x b_rho - a_rho)/2 equals the coordinate Ricci block of a generic
   b(t, x, rho) (one `phantom_source.ricci` run, 1 s).
2. b = b(t, x) alone gives R_3 = diag(P, -P, 0), so D = 0 for every such b.
3. For b = X(x) + R(rho): D = h [(h + X'^2)^2 - ((X + R) X'')^2 - Q^2]; a hand argument (span of five functions of x
   against five of rho) leaves only X'' = 0, then b = c x + g(rho) with g'' + g'/rho = eps (g'^2 + 2 c^2); that is a Riccati
   equation with solutions g = -eps ln(alpha J0(sqrt2 c rho) + beta Y0(sqrt2 c rho)); numerically D = 0 to 160 digits.
4. The two-scalar closure test run on null-coordinate planar metrics -2 e^(2 sigma) dp dq + dy^2 + dz^2 passes iff
   d_p d_q ln|sigma_pq| = 0 (3 planted passes and 2 planted failures, scratch); for a static planar shift u(xi) the
   obstruction d omega_(t xi) equals Theta'/2 with Theta = (1 - u^2) Phi'/Phi, Phi = (u u')' (1 - u^2) (symbolic, abstract u).
5. For b = F(x/rho) the equation is a cubic in F'' (printed in the script); its cubic and quartic parts in the small
   quantities factor (see C9).
6. For b = X(x) R(rho) + v the equation is quadratic in X'' and in S = R'' + R'/rho. For v = 0 it reads
   u^2 A + B = 0 in the log derivatives (see C8). Eliminating the factor e^(2 psi + 2 chi) leaves one compatibility
   polynomial, the same from d_x and from d_rho. I did not finish the prolongation by hand.
Not yet done at this point: the script itself, any closure on the Bessel family, the closure of the conical family.
A Groebner basis of the first jets of the multiplicative equation (12 variables) ran 3.5 min without finishing and was
stopped by me (exact PID). It is not used.

## Imports and independence

Imported from `phantom_source.py`: `ricci` (coordinate Christoffel Ricci, tested there and reviewed in #59, #79) and
`ricci_at_point` (frame Ricci of a shift at an exact point). Imported from `two_scalars.py`: `closure` (the omega
construction), `two_scalar_form` (algebraic stage), `dform`. These are the project's own code, so the checks that use
them are not independent of #65. Not imported: the Cartan routine of `review_cartan.py`. Everything else (the reduced
equations, the separable and conical analysis, the planar criterion) is new code in `det_classify.py`.
The independent check of D itself is #79's; here D is re-derived from `ricci` once and then used as a formula.

## Definitions (fixed here, before the runs)

Metric ds^2 = -dt^2 + (dx + b dt)^2 + dy^2 + dz^2, rho^2 = y^2 + z^2, n = d_t - b d_x, Delta_perp b = b_rho,rho + b_rho/rho.
P = n(b_x) - b_x^2, Q = -Delta_perp b / 2, Z = b_x,rho / 2, Y = -n(b_rho)/2 + b_x b_rho, h = b_rho^2 / 2 (#65's).
D = h (h^2 - P^2 - Q^2 + Y^2 + Z^2) - P (Y^2 - Z^2) + 2 Q Y Z. With a = b_t - b b_x: P = a_x, Y = (b_x b_rho - a_rho)/2.
"D = 0 on an open set": D vanishes on an open set of the (t, x, rho)-space with rho > 0. By #65's lemma that is the
algebraic stage of the two-scalar test (with lambda = 0).
Static shift u(x, rho): b independent of t. Traveling shift b = B(x - vt, rho): in the comoving frame it is the static
shift u = B + v (C2).
**x-localized** (my definition, for this issue): on a strip ℝ × I, I an interval in rho > 0, u(., rho) has limits
u_-(rho), u_+(rho) as x -> -inf, +inf for each rho in I (compact support in x is the case u_- = u_+ = 0), and u_x is not
identically 0. **transversally nontrivial**: u_rho is not identically 0 on the strip. A **bubble-like** shift is both.
Status words as in AGENTS.md. Smoothness: C^2 where D is evaluated; the separable theorem (C7) and the planar theorem
(C5) say what they use.

## Acceptance criteria (written before the first run; none is loosened after seeing data)

**C1 `d_block`.** For an undefined function b(t, x, rho): the frame Ricci block of `phantom_source.ricci` for the
metric above in coordinates (t, x, rho, phi) with the frame (n, d_x, d_rho, d_phi / rho) has
R_00 = P - h, R_11 = -P - h, R_22 = h, R_01 = Q, R_02 = Z, R_12 = Y, and R(e_phi, .) = 0, each a simplified difference
equal to 0; and the new forms P = a_x, Y = (b_x b_rho - a_rho)/2 equal #65's P and Y; and det of the block equals D.
Pass: every difference is 0.

**C2 `travel`.** For an undefined B(xi, rho), b(t, x, rho) = B(x - v t, rho): D(b) - D_static(u) = 0 after x = xi + v t,
with u = B + v; and for an undefined b: D of b'(t, x, rho) = b(t, x + c t, rho) + c equals D(b)(t, x + c t, rho) (Galilean
covariance). Pass: both differences are 0.

**C3 `planar`.** For an undefined b(t, x): R_3 = diag(P, -P, 0) and D = 0 (symbolic, from the block formulas of C1). At 8 exact
points of 3 rational planar shifts (b = -2/(1 + (x - t)^2), (t^2 + 2x)/(1 + x^2), x/(1 + t^2); the script asserts P != 0 at
every chosen point) `ricci_at_point` then `two_scalar_form` without closure returns status "form" with lambda = 0; and for
the same shifts plus rho^2/10 it returns status "algebraic" at every point, with D != 0 there.
Pass: all 8 + 8 outcomes as stated.

**C4 `planar_closure`.** (i) For null-coordinate planar metrics g = -2 e^(2 sigma) dp dq + dy^2 + dz^2 with the
Ricci tensor R = K g_2 (K from `ricci`): `closure` with a = (k + m)/2, b = (k - m)/2, k = dp, m = 2 R_pq dq returns ok
exactly when d_p d_q ln|R_pq| = 0 (as a symbolic expression equal to 0). Planted passes: sigma = sin(p) e^(q/2)/3,
p q + p^2 q, (p + q)^2/5. Planted failures: p^2 q/2 + p q^2/2, e^(p q), p^3 q^2/6 + p q. Pass: all six agree with the criterion.
(ii) For a static planar shift u(xi) with k = dt - (dxi + u dt), m = P (dt + dxi + u dt), P = -(u u')': `closure`'s
d omega_(t xi) equals Theta'/2 exactly for undefined u, Theta = (1 - u^2) Phi'/Phi, Phi = (u u')' (1 - u^2).
(iii) a jet with u''''(0) chosen so that Theta'(0) = 0 (random rational u, u', u'', u''') has d omega_(t xi)(0) = 0; the
1+1 rational bubble u = v (1 - f), f = 1/(1 + xi^2)^2, v = 1/2, has Theta' != 0 at 5 exact points. Pass: (i), (ii), (iii).

**C5 `planar_traveling`.** The theorem "a traveling planar shift with |u| != 1 on all of ℝ, u -> u_+- and u', u'' -> 0
at +-inf has closure on {K != 0} only if K = 0" is proved by hand in the note. The script checks its three algebraic
inputs for undefined u: (a) the null coordinates p = t - A(xi), q = t + B(xi), A' = 1/(1 - u), B' = 1/(1 + u) give
-(1 - u^2) dp dq = -dt^2 + (dxi + u dt)^2 exactly; (b) R_pq of the planar metric is Phi/(2 (1 - u^2)) up to the
factor stated in the script, so closure is d_p d_q ln|Phi| = 0, i.e. Theta' = 0 (the relation of C4 (ii)); (c)
ln|Phi(q - p)| = f(p) + g(q) forces ln|Phi| linear in q - p (d_p d_q of it is -(ln|Phi|)'' in s = q - p). Pass: all three.

**C6 `bessel`.** The family u = c x + g(rho), g = -eps ln psi, psi = alpha J0(sqrt2 c rho) + beta Y0(sqrt2 c rho).
(a) Exact: for u = c x + g(rho), D = g'^2 (2c^2 + g'^2 - S)(2c^2 + g'^2 + S)/8 with S = g'' + g'/rho (symbolic factorization).
(b) For c in {1/2, 3/2}, eps = +-1, random rational alpha, beta, D = 0 to 1e-50 at 6 points each (mpmath 60 digits), and for
psi + rho^2/10 D != 0 (above 1e-3) at the same points; and for c = 0, psi = C1 + C2 ln rho, the same (this is #65's b(rho),
g = -eps ln(C1 + C2 ln rho)). (c) R = a a - b b with a = (g' d_rho + 2 c theta^1)/sqrt2,
b = sqrt(g'^2 + 2 c^2) ((1 + eps u) dt + eps dx)/sqrt2, theta^1 = dx + u dt, on the ODE g'' = eps (g'^2 + 2c^2) - g'/rho (symbolic).
(d) `closure` on (a, b) returns not ok for c != 0 and for c = 0 (the latter is #65's b(rho)). Pass: (a) to (d).

**C7 `additive`.** For b = X(x) + R(rho): (a) D = h [(h + X'^2)^2 - ((X + R) X'')^2 - Q^2] exactly (undefined X, R); (b)
E = (R'^2/2 + X'^2)^2 - (X + R)^2 X''^2 - (R'' + R'/rho)^2/4 = sum f_i(x) g_i(rho) with f = (1, X'^2, X''^2, X X''^2, X'^4 - X^2 X''^2),
g = (A^2 - B, 2A, -R^2, -2R, 1), A = R'^2/2, B = (R'' + R'/rho)^2/4 (exact); (c) the elimination step: the polynomial identity
(y^2 - e0 - b5 y)(g0 + b3 y) = (d0 + b4 y)^2 forces b3 = 0, g0 = b4^2, and then X = (+-1/(2m)) y + const for X'' = +-m
gives b4 = +-m/2, so m = 0 (exact, solved by sympy); (d) with X'' = 0, E = 0 is g'' + g'/rho = eps (g'^2 + 2c^2) and
C6 applies. Theorem (proved by hand, the span argument in the note): if R' != 0 on an interval and D = 0 on a box then
X'' = 0. Pass: (a) to (d).

**C8 `multiplicative`.** For b = X(x) R(rho) (v = 0) and traveling b = X(xi) R(rho), u = X R + v: (a) 8D/R'^2 as a polynomial
in the jets equals the printed polynomial of the script (exact, including v); (b) for v = 0 in the variables
p1 = X'/X, p2 = (ln X)'', c1 = R'/R, s2 = R''/R + R'/(rho R): the exact identity 8D/R'^2 = R^2 X^4 [X^2 R^2 A + B],
A = T (9 p1^2 + 2 c1^2 - T), B = p1^2 T - (s2 + 3 p1^2)^2, T = 5 p1^2 + c1^2 - 2 p2 (X, R here are the values X0, R0);
(c) R' = 0 gives planar (D = 0 identically), X' = 0 gives #65's b(rho) equation for R; (d) the compatibility
conditions C1 (d_rho of p3) and C2 (d_x of s2'), computed from (I) and (II) in the script (p3 and s2' solved from
A B_x - A_x B = 2 p1 A B and A B_rho - A_rho B = 2 c1 A B), have equal numerators as polynomials, so the first
compatibility order gives one relation, not two. NOT claimed: a classification of the multiplicative case. Whether a solution with X' R' != 0 exists is
reported as not decided by this issue unless C8 (e) below finds it.
(e) numerical formal-series search (only if time allows; reported as numerical evidence with a planted control).

**C8 (e) `mult_series` (criterion and target written 2026-11-24, before the first run of the search code).** Numerical evidence,
not a proof. At the point (x, rho) = (0, 1) (WLOG: x-translation and the scaling (x, rho) -> s (x, rho) map separable shifts to
separable shifts), unknowns X_0..X_7, R_0..R_7 (jets of X and R) and t_X, t_R; equations E_(m,n) = d_x^m d_rho^n E = 0 for
m + n <= 5 with E = 8D/R'^2 of C8 (a), (S = R'' + R'/rho, d_rho (1/rho) = -1/rho^2), and t_X X_1 = 1, t_R R_1 = 1 (so X' R' != 0).
Levenberg-Marquardt (numpy, finite-difference Jacobian), 60 random starts per equation (seed 80, entries uniform in [-2, 2],
80 iterations), 'converged' = residual norm < 1e-10. Equations: u = X R + v for v in {0, 1/2, 1, 2}. Pass: for each v, no start
converges (the smallest final residual is reported). Planted truth through the same code: for the additive-separable
equation E_add = (R'^2/2 + X'^2)^2 - ((X + R) X'')^2 - (R'' + R'/rho)^2/4 of C7, which has the solutions u = c x + g(rho), at least
one start converges. Control `mult-series-add` (target `mult_series`): the search for u = X R + v is run on E_add instead, so some
start converges and the 'none converges' criterion fails. NOT shown by this check: that the full system has no solution.

**C9 `conical`.** For b = F(x/rho): D = N(F, F', F''; eta)/(8 rho^6), N the polynomial printed by the script (exact); its
part of degree 3 in (F', F'') is 2 F w^2 (F^2 F'' - eta w), w = F' + eta F'' (exact); with F -> 0 its part of degree 4 is
-w^2 ((eta^2 + 1)(eta^2 + 2) F'^2 + 2 eta F w) (exact). Consequence (by hand, conditional on regular asymptotics, stated so in
the note): no solution has a limit at eta -> +-inf with a power or exponential approach. Pass: the three identities.

**C9 outcome (added 2026-11-24 after `dev_mid.run1.log`): parts (b) and (c) as written above FAILED, and that stands.**
The script printed 2 F w^2 ((F^2 - 1) F'' - eta w) for the degree-3 part, and -w^2 ((eta^2 + 1)(eta^2 + 2) F'^2 + 2 F (eta w + F''))
for the lowest part with F, F', F'' small. The hand formula of this README dropped the term -2 F F'' w^2 (and its
partner in (c)). The wording of (b) and (c) above is kept unchanged as the record. Part (a) (the ODE identity) passed.
The script's `conical` check keeps only (a); (b) and (c) are replaced by C9b below, by the coordinator's ruling.

**C9b (written after C9 (b), (c) failed; added 2026-11-24 before the rerun).**
(i) `conical_parts`: the corrected right-hand sides are re-derived by hand in the note from the jets of u = F(x/rho)
(P = -(F'^2 + F F'')/rho^2, Q = -eta w/(2 rho^2), Z = -w/(2 rho^2), Y = -(eta F'^2 + F w/2)/rho^2, h = eta^2 F'^2/(2 rho^2),
w = F' + eta F''), not read off the script's N. The note says the formula came from the script first. The check builds the
degree-3 and degree-4 parts from those hand-derived entries (not from the typed N) and compares them with the parts of
the typed N, and with the sympy jets of F(x/rho). Expected: degree 3 = 2 F w^2 ((F^2 - 1) F'' - eta w), and with F, F', F''
all small, degree 4 = -w^2 ((eta^2 + 1)(eta^2 + 2) F'^2 + 2 F (eta w + F'')). Pass: both equalities and the entries equal
sympy's jets of F(x/rho).
(ii) `conical_limit`: the conclusion C9 was for, tested directly: no solution of N = 0 has a limit as eta -> +inf by a power
law F = F_inf + c eta^(-k) (1 + o(1)), or by an exponential F = F_inf + c e^(-kappa eta) (1 + o(1)). Test, with the typed N
(checked in (i) and C9 (a)): for k in {1/2, 1, 3/2, 2, 5/2, 3, 4, 5, 6}, kappa in {1/2, 1, 2} and F_inf in {0, 1/3, 1, -1, 2}:
power law: the lowest order of N(F_inf + c eta^(-k)) in 1/eta exists (N is not identically zero) and its coefficient, a
polynomial in c, has no real root c != 0 (a root would allow a leading-order solution; degrees 3 and 4 in c can meet at
k = 2); exponential: the lowest order of N(F_inf + u, u = c e^(-kappa eta)) in u has a coefficient that is not the zero
polynomial in eta (the powers e^(-j kappa eta) of different degrees j cannot cancel). This is written before the
first run of C9b and is stronger than the first draft of this paragraph, which asked only for 'not identically zero'. Planted truth through
the same code: for N_pow = F'' + 2 F'/eta (solutions F_inf + c/eta) the code finds the vanishing lowest order at k = 1 for
every F_inf, and not at k = 2; for N_exp = F'' + F' (solutions F_inf + c e^(-eta)) it finds it at kappa = 1 and not at kappa = 2.
Pass: all N tests as stated, all planted detections as stated. What this does not show: no asymptotic form other than these
two (an oscillating or logarithmic approach is not tested).

**C9b (iii) `conical_planted` (criterion and target written 2026-11-24, A3, before its first run of record).** The planted
detections of C9b (ii) are their own check: the scan code applied to N_pow = F'' + 2 F'/eta finds a limit (the lowest order is
identically zero) at k = 1 for every F_inf in {0, 1/3, 1, -1, 2} and at no other of k in {1, 2}; applied to N_exp = F'' + F' it
finds one at kappa = 1 and not at kappa = 2, for every F_inf. Control `conical-plant` (N_pow -> F'' + F'/eta) must fail exactly
this check. History: the same planted detections ran inside `conical_limit` in `dev_conical.run1.log` (all as stated) and the
first run with the separate check is the checks-only development run `dev_all.run1.log`; both stay.

**C10 `farfield`.** For u = u_inf + e w(x, rho): the e^3 coefficient of D is -u_inf Z^2 [(1 - u_inf^2) w_xx + Delta_perp w] with Z = w_x,rho/2,
and the e^0, e^1, e^2 coefficients vanish (exact, undefined w). Pass: both.

**C11 `bubble`.** The constant-speed bubble u = w(r), r^2 = x^2 + rho^2: D computed here (not imported) as a cubic in c^2 (c = x/r)
has the printed c^0 and c^6 coefficients of `two_scalars.md`; its four coefficients and (A, B^2), A = 2w - r w', B = w' + r w'',
generate the same ideal after inverting r w' (sympy Groebner with a saturation variable, both directions); and
2w = r w', w' + r w'' = 0 on an interval force w' = 0 (differentiate and add). Pass: all four.

## Controls (each `--mutate=NAME` must exit non-zero, failing exactly the listed target checks)

| control | target checks | what it changes |
|---|---|---|
| `d-sign` | `d_block` | Y built as (b_x b_rho + a_rho)/2 |
| `travel-offset` | `travel` | the comoving shift u = B, without + v |
| `planar-leak` | `planar` | the planar b gets + rho^2/10 in the symbolic D = 0 check |
| `planar-point` | `planar` | the exact-point shifts get + rho^2/10 in the "form" check (the "algebraic" check then fails too) |
| `closure-deform` | `planar_closure` | the planted passes of (i) get + p q^2/10 (not a product) |
| `theta-factor` | `planar_closure` | (ii) expects Theta'/4 |
| `planted-bubble` | `planar_closure` | (iii) the bubble is replaced by the planted jet with Theta'(0) = 0, so "Theta' != 0" fails |
| `pg-null` | `planar_traveling` | A' = 1/(1 + u) in the null coordinates |
| `bessel-freq` | `bessel` | psi uses J0(c rho), Y0(c rho) |
| `bessel-closed` | `bessel` | (a, b) replaced by (d rho, dt + dx), a closed pair, so "closure fails" fails |
| `add-drop` | `additive` | (X + R)^2 replaced by X^2 in E |
| `add-quad` | `additive` | the elimination step keeps b3 free |
| `mult-drop-v` | `multiplicative` | u = X R without + v in the expected polynomial |
| `mult-series-add` | `mult_series` | the search for u = X R + v is run on E_add (which has solutions), so a start converges |
| `conical-term` | `conical` | one term (F^3 F''^3 eta^2, coefficient 2 -> 3) changed in N |
| `conical-hand` | `conical_parts` | the degree-3 right-hand side is the original wrong one of C9 (b): 2 F w^2 (F^2 F'' - eta w) |
| `conical-limit` | `conical_limit` | N replaced by N_pow = F'' + 2 F'/eta, which has the limit solutions F_inf + c/eta. **DROPPED 2026-11-24 (A3): its target `conical_limit` already fails on the real N, so the control cannot be told apart from the baseline. Target kept here as first written.** |
| `conical-plant` | `conical_limit` (as first written); now `conical_planted` (A3) | the planted N_pow replaced by F'' + F'/eta (solutions c ln eta + d, no limit), so the planted detection fails |
| `far-sign` | `farfield` | the expected e^3 coefficient has + u_inf |
| `bubble-w2` | `bubble` | the shift's square dropped (u u_xx -> w'' only) in P |
| `bubble-ode` | `bubble` | the relation r w'' = +w' in place of r w'' = -w' in the ODE step |

Predictions: each control fails its target and, by design, no other check. A control that fails another check, or none, is
reported as it is. If a control is silent on its target, the target list stays as written here and the result is reported
as silent; any later change of the list is dated and recorded below.

## Not claimed here

- The general static or traveling PDE D = 0 is not classified. Its local solutions are as many as one second-order PDE has
  (the equation is quadratic in b_rho,rho at fixed other jets); whether any solution has u_rho not identically 0 and is
  x-localized is decided only inside the reductions C5 to C9.
- The time-dependent shifts b(t, x, rho) beyond b(t, x) (C3) and the traveling reduction are not classified.
- Closure on the conical family is not run unless the script says so (no closed form).

## Amendments

- 2026-11-24, A2 (coordinator's ruling, hc): `bessel` part (b), perturbed psi + rho^2/10, |D| > 1e-3 at the same points FAILED in
  `dev_bessel.run1.log`: smallest perturbed |D| = 9.06e-6. The threshold stays as written and gates the exit code. For the final
  run the part is its own check `bessel_pert` (the rest of C6, including the first part of (b), D = 0 to 1e-50, stays in `bessel`),
  and the script prints the smallest perturbed |D| with its (c, eps, rho) and all perturbed values, as an observation. No new
  perturbation or threshold replaces it. The controls loop does not count a baseline failure as an 'extra' failure of a control.
- 2026-11-24, A3 (coordinator's ruling, hc): C9b (ii) `conical_limit` FAILS on the real N in `dev_conical.run1.log`: at k = 2 the
  lowest-order coefficient has a real root c = -2 F_inf for F_inf in {1/3, 1, -1, 2} (none at F_inf = 0, none at any other k, none
  for the exponentials). It stays as written and gates the exit code. Verdict for the conical reduction: 'no limit at eta -> inf'
  is not established; not decided. The control `conical-limit` is dropped (see the table). The planted detections are the check
  `conical_planted` (C9b (iii)). Observation, not a criterion: a pure power series F_inf + sum a_j/eta^j with a2 = -2 F_inf fails at
  the third order after the leading one (F_inf^4 (F_inf^2 + 7) = 0); logarithmic terms are not tested.
- 2026-11-24, A1: `dev_mid.run1.log` (the first run of the `conical` check): C9 (b) and (c) as worded FAIL. Cause: my hand
  algebra dropped -2 F F'' w^2 from the degree-3 part (and its partner from the degree-4 part). Ruling by the coordinator
  (hc, 2026-11-24): the failure stands and is recorded here, in the note and in the closing comment; the wording is not changed;
  C9b above (written after the failure) replaces (b), (c). The asymptotic conclusion of C9 is re-derived from the corrected
  forms in the note and tested directly by C9b (ii); it is not carried over.
- 2026-11-24, before the first run of `det_classify.py`: the `conical-term` row said F^2 F''^3; the term is F^3 F''^3 eta^2 (typo).
  Development runs (checks one at a time, to fix bugs in the script) are kept as `dev.*.runN.log`; they are not final runs.
- 2026-11-24, A4: implementation of the numerical part of C6 (b) only, no threshold: `dev_b2` showed the sympy evaluation (`sp.N(..., 60)`,
  adaptive precision, 250 s per run, largest unperturbed |D| 0.0 to 1e-160 in `dev_all.run1.log` and `dev_bessel.run1.log`) is too slow
  for 17 control runs. My first speed-up (mpmath at 60 working digits, `dev_b3.run1.log`) left |D| up to 1.25e-46 > 1e-50 at some points,
  which is cancellation error of the arithmetic, not a feature of D; at 130 working digits (`dev_b4.run1.log`) the largest |D| is 8.9e-117.
  Both failed and passing logs are kept; the thresholds 1e-50 and 1e-3 are unchanged.
- 2026-11-24, A5: C8 (e) `mult_series` and its control `mult-series-add` are WITHDRAWN before any run of record. The first dev run
  (`dev_series.run1.log`) was stopped by me after 9 min with no output (it needed about 10 min). A batched rewrite then converged for
  several starts of the multiplicative equation, and the converged starts have X, X' or R of order 1e-2 to 1e-4 with t_X up to 3e3
  (`scratch_series_search.log`): the normalisation t_X X' = 1 does not bound the amplitude, and every part of D is of order 3 or higher in
  the small shift u - v, so 'residual < 1e-10' is reached at tiny amplitude, also for the additive planted equation. The criterion as I wrote it
  cannot separate a solution from a small amplitude. I did not change it and rerun; the check is dropped and the multiplicative reduction stays
  *not classified*. A recommended task in the closing comment: a properly normalised search (relative residual, amplitude bounded below).

## Final run of record (2026-11-24)

`run_final.sh` (systemd unit `nm-i80-final`, nice 10, one process): `python3 notes/warp/det_classify.py --logdir=final_mut`, script at commit 00d7f4e (unchanged
since), stdout in `notes/warp/det_classify_output.txt` of the repository, stderr empty (`final_stderr.txt`), exit code in `final.rc`: **1**.
Reason: 13 of 15 checks pass; `bessel_pert` and `conical_limit` FAIL, as written, by the coordinator's rulings (A2, A3). All 19 controls fire on their
targets and on no other check. Checks alone 43 s, whole run about 15 min. Each control's full stdout: `final_mut/mut_<name>.log`.
Withdrawn or dropped: `mult_series`, `mult-series-add` (A5), `conical-limit` (A3).
Development runs: `dev_fast.run1/2`, `dev_mid.run1` (the C9 (b), (c) failure), `dev_closure.run1`, `dev_bessel.run1` (the C6 (b) perturbed failure), `dev_conical.run1`, `dev_all.run1`,
`dev_b2.run1`, `dev_b3.run1`, `dev_b4.run1`, `dev_series.run1` (stopped by me), `scratch_series_search.log`.
