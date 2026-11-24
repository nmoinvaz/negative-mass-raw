# I160-rpi5: logs of notes/warp/mult_classify.py (multiplicative separable shifts u = X(x) R(rho) + v with det R3 = 0)

Machine rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process, one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/160. Branch `wip/i160-mult-classify`, worktree
`~/Source/negative-mass-i160` (main f50f14f). Python `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0,
mpmath 1.3.0). Written 2026-11-24, before the first run of record. Stop condition: a single run not finished after 1 h
of wall time is stopped and reported. Memory is reported, never a stop condition.

## Question

On an open box I x J in (x, rho), rho > 0, with X X' R R' != 0, does D = det R3 = 0 for the static shift
u = X(x) R(rho) + v have a solution (X, R real, C^2)? v = 0 is the static case, v != 0 the traveling case
(`det_classify.md` Setup: B(x - vt, rho) with u = B + v; a bubble of speed v is a static u tending to v). Route 1 of the
issue: finish the prolongation of `det_classify.md` section 5 and decide the unit ideal, or give an explicit solution.

## What was explored before this README (not of record)

Scratch scripts in the scratchpad (not kept, no run of record). They showed:

1. E = 8D/R'^2 equals `det_classify.E_mult_poly` and, in the variables U = X R, m = (X'/X)^2, beta = (ln X)'', c = (R'/R)^2,
   s2 = S/R (S = R'' + R'/rho), has the form E/X^2 = s^2 - delta^2 - tau^2 with
   s = U^2 c + m (W^2+1)/2, delta = 2 u U (beta + m) + m (4 U^2 + 1 - W^2)/2, tau = U s2 + m W, u = U + v, W = 3U + v.
2. The prolongation of section 5 in jets (E, E_x -> X''', E_rho -> S', E_x_rho) gives one irreducible polynomial Gamma,
   345 terms, degree 15 in (U, p1, p2, c1, s2, w = 1/rho, v); at v = 0 and with U^2 eliminated, 190 terms, degree 16 in
   (p1, p2, c1, s2, w). Its x- and rho-derivatives have 526 and 720 terms. At random real points of Gamma = 0 the
   derivatives are nonzero. sympy's `groebner` (grevlex, modulus 32003) of Gamma and its x-derivative in the four variables
   (p1^2, p2, c1, s2 at w = 1) did not finish in 7 min (stopped by hand). So a modular Groebner basis in sympy is not a
   feasible route on this machine; route 1 is done by separation of variables instead (next point).
3. E is a bilinear form in x-jets and rho-jets: E = sum_i F_i(X, X', X'') G_i(R, R', S). If E = 0 on a box, then
   span{F(x)} and span{G(rho)} are orthogonal subspaces of R^r, so d_F + d_G <= r, with d_F the dimension of the span of
   the functions F_i (and d_G of the G_i). The minimal r is 6 at v = 0 and 10 at the four values v in {1/3, 2, 5/7, 3/2}
   tried. At v = 0 hand arguments (section "Method") give d_F >= 4 when m is not constant and d_G >= 3, which contradicts
   d_F + d_G <= 6; m constant is excluded by a sign. At v != 0 the same bound does not decide: R = rho^2 has d_G = 5.
4. The ansatz u = X(x) rho^2 + v (and rho^2 + r0) gives eight coefficient equations in (X, X', X'') whose Groebner basis in
   (X'', X', X, r0, v) was printed but not read as a unit ideal; it is not used here.

Everything below was fixed after this exploration and is not changed after the first run of record, except by a dated
amendment written before the run it concerns.

## Notation

x-jets a = (X0, X1, X2) = (X, X', X''), rho-jets b = (R0, R1, S0) with S0 = R'' + R'/rho; u = X0 R0 + v;
u_x = X1 R0, u_rho = X0 R1, u_xx = X2 R0, u_x_rho = X1 R1, u_rho_rho + u_rho/rho = X0 S0. D = h (h^2 - P^2 - Q^2 + Y^2 + Z^2)
- P (Y^2 - Z^2) + 2 Q Y Z with P = -(u_x^2 + u u_xx), Q = -(u_rho_rho + u_rho/rho)/2, Z = u_x_rho/2, Y = u_x u_rho + u u_x_rho/2,
h = u_rho^2/2 (`det_classify.md` Setup at b_t = 0, retyped in the script, not imported). E = 8 D / R1^2.
Log variables: p1 = X1/X0, m = p1^2, beta = X2/X0 - m, c = (R1/R0)^2, s2 = S0/R0, U = X0 R0.

## Method (what the script does)

Imported from `det_classify.py`: `E_mult_poly` and `E_add_poly`, only as comparison targets of C1 and C8. Shared with it: the
formula for D (#65's lemma), which is retyped.

1. Bilinear separation. `bilinear_form(E, xvars, rvars)` returns the coefficient matrix M of E in the x-monomials and
   rho-monomials, its exact rank r, and a rank-r factorization E = sum_{i<=r} F_i G_i. `span_dim(rows)` is the exact rank
   (Fractions) of the matrix of values of functions at sample points, or the numerical rank (mpmath, 130 digits, singular
   values below 1e-40 times the largest count as zero).
2. Lemma L (linear algebra, checked in C3). If sum_i F_i(x) G_i(rho) = 0 on a box, then d_F + d_G <= r.
3. Static case v = 0, E = R0^2 X0^4 Ehat with Ehat = a T_- T_+ + m T_- - (s2 + 3m)^2, a = X0^2 R0^2, T_- = c + 5m - 2 beta,
   T_+ = c + 4m + 2 beta (#80's A = T_- T_+, B). Ehat = sum_{i=1}^6 f_i g_i with
   f = (X0^2, X0^2 m, X0^2 Theta, m, Psi, 1), g = (R0^2 c^2, 9 R0^2 c, R0^2, c - 6 s2, 1, -s2^2),
   Theta = 20 m^2 + 2 m beta - 4 beta^2, Psi = -4 m^2 - 2 m beta.
   - Lemma X (by hand, checked in C4): if m is not constant on any subinterval, then d_f >= 4. Proof sketch: pass to a
     subinterval with m' != 0. If 1, m, E_x = X^2, m E_x are dependent then E_x is a Moebius function rho(m) = (am+b)/(cm+d),
     ad - bc != 0 (E_x' = 2 p1 E_x and m' = 2 p1 beta give beta = rho/rho' = (am+b)(cm+d)/(ad-bc)); then for c != 0
     span{1, m, rho, m rho} = span{1, m, 1/(cm+d)} and Psi is a polynomial in m that is not of degree <= 1; for c = 0
     span = span{1, m, m^2} and rho Theta has degree 3. Either way d_f >= 4.
   - Lemma R (by hand, checked in C5): d_g >= 3. If d_g <= 2 then span = <1, R^2>, R'^2 = alpha + gamma R^2, alpha = 0,
     R = a e^{kappa rho}, and s2^2 contains kappa^2/rho^2, not in span{1, e^{2 kappa rho}}.
   - Lemma K (C6): m constant (X = e^{lambda x}) gives d_f = 2 and the coefficient of X^2 forces
     R^2 (c + 4 lambda^2)(c + 5 lambda^2) = 0, impossible for real c >= 0, lambda != 0.
   Then d_f + d_g >= 7 > 6 for m not constant: no solution, and m constant has none.
4. Planted truth, additive u = X + R (`det_classify.md` section 4): E_add = sum_{i<=5} f_i g_i with
   f = (1, X1^2, X2^2, X0 X2^2, X1^4 - X0^2 X2^2), g = (A^2 - B, 2A, -R0^2, -2R0, 1), A = R1^2/2, B = S0^2/4. The
   x-curves with f constant (d_f = 1) are found by an elimination (C9), giving X'' = 0, X' = c, any c; then f.g = 0 is
   (A + c^2)^2 = B, the Bessel equation of #80 (u = c x - eps ln(alpha J0(sqrt2 c rho) + beta Y0(sqrt2 c rho)) + d).

## Checks, criteria and tolerances (exit code 1 if any fails)

All "exact" checks are sympy identities (expand to 0) or exact Fraction ranks. Numerical checks use mpmath at 130 digits.

| id | name | criterion (pass iff all hold) |
|---|---|---|
| C1 | `e_from_d` | (i) E - `det_classify.E_mult_poly` expands to 0 for symbolic v. (ii) With the log variables substituted, E/X0^2 - (s^2 - delta^2 - tau^2) expands to 0 for symbolic v (s, delta, tau as in exploration point 1). (iii) At v = 0, E - R0^2 X0^4 Ehat expands to 0. (iv) At five fixed exact points (x, rho) and X = exp(x) + x^2, R = rho^3 + rho/2 + 1, v in {0, 1/3}, the numerical 8D/R'^2 from mpmath numerical derivatives of u(x, rho) equals the polynomial E at the jets, relative error <= 1e-40. |
| C2 | `decomp_static` | (i) At v = 0, Ehat - sum_{i<=6} f_i g_i expands to 0. (ii) The exact rank of the coefficient matrix of E (v = 0) in x-monomials x rho-monomials is 6. |
| C3 | `rank_lemma` | Planted lemma test, r = 6, five seeded random draws (seed 160): f(x) = B phi(x) with B a random 6x4 integer matrix of rank 4 and phi = (1, x, x^2, x^3); g(rho) = N psi(rho), N a basis of the orthogonal complement of col(B) (6x2), psi = (1, rho). Pass iff sum f_i g_i = 0 at 12 x 12 exact sample points, d_F = 4, d_G = 2 (exact ranks), d_F + d_G <= 6. Planted failure: with N replaced by a random 6x3 matrix (d_G = 3), sum f_i g_i != 0 at some sample point in all five draws. |
| C4 | `lemma_x` | (i) Symbolic: the Moebius step (E_x = rho(m) gives beta = (am+b)(cm+d)/(ad-bc)); for c != 0 the 4x3 matrix of {1, m, rho, m rho} in the basis {1, m, 1/(cm+d)} has rank 3, and Psi, expanded in m, has m^3 coefficient -2ac/(ad-bc) and, at a = 0, m^2 coefficient -2; for c = 0 the cubic coefficient of rho Theta is 18 a/d. (ii) Exact ranks: for every (a, b, c, d) in {-2, -1, 0, 1, 2, 3}^4 with ad - bc != 0 and for 60 seeded random rationals (seed 160), the six rational functions {1, m, rho, m rho, rho Theta, Psi} (evaluated at 14 fixed rational m-values avoiding poles) have rank >= 4. |
| C5 | `lemma_rho` | (i) Symbolic: (alpha + gamma y)^2/y = p + q y as polynomials in y forces alpha = 0; for R = a exp(kappa rho), the coefficient of 1/rho^2 in s2^2 is kappa^2. (ii) Numerical ranks of the six g_i (130 digits, 14 sample points rho in [1, 3]) are >= 3 for R in {exp(rho/2), exp(-rho), exp(2 rho), rho^(1/2), rho, rho^2, rho^3, rho^(-1), rho^(5/2), rho^4, rho^2 + 1, rho + rho^3, cosh(rho)}. |
| C6 | `const_m` | Symbolic: with m = lambda^2, beta = 0 the coefficient of X^2 in Ehat is R^2 (c + 4 lambda^2)(c + 5 lambda^2), and d_f = 2 (numerical rank, 130 digits, of f at 10 points x, X = exp(lambda x), lambda in {1/2, 1, 3/2}). Exact: for c = n/10 and lambda = k/4, n in 0..60, k in 1..8, the product is > 0. |
| C7 | `mult_subcases` | Planted (same `bilinear_form`): with X1 = X2 = 0 (u = X0 R(rho) + v, #65's b(rho)), E = X0^6 R1^4 - X0^4 S0^2 = f1 g1 + f2 g2 with f = (X0^6, X0^4) constant at constant X0 (d_f = 1) and g = (R1^4, -S0^2), exact rank 2. The relation f.g = 0 is S0^2 = X0^2 R1^4 and has solutions: for eps = +-1, R = -(eps/X0) ln(C1 + C2 ln rho) gives E_sub = 0 (sympy simplification, symbolic X0, C1, C2). With R1 = 0 (planar) E = 0 and D = 0 (exact). |
| C8 | `add_decomp` | E_add built from the retyped D with u = X0 + R0, divided by h, minus `det_classify.E_add_poly`, expands to 0; and E_add - sum_{i<=5} f_i g_i expands to 0; exact rank 5 (the same `bilinear_form`). |
| C9 | `add_stratum` | The x-curves with all f_i constant, found by a Groebner elimination of {f_i(a) - k_i} (k_1 = 1) with X0 free: the result is X2 = 0 and X1^2 = k_2 =: c^2 free, k_5 = c^4, k_3 = k_4 = 0 (the script prints the elimination ideal). Pass iff X2 = 0 and k_5 = k_2^2 are in it and k_2 is not constrained. Then f.g reduces to (A + c^2)^2 - B. |
| C10 | `add_planted` | For c in {3/10, 1/2, 1, 3/2, 2}, eps in {+1, -1}, R(rho) = -eps ln(J0(z) + 0.3 Y0(z)), z = sqrt2 c rho in {0.4, 0.8, 1.2, 1.6, 2.0} (so psi > 0): relative residual |f0.g| / sum|f_i g_i| <= 1e-50 at all 50 points (f0 = (1, c^2, 0, 0, c^4)); d_F = 1 (exact) and numerical d_G <= 4 at each (c, eps); amplitude c >= 3/10 for every case. |
| C11 | `add_perturbed` | Perturbed additive shift rejected: for the same (c, eps, z) and R replaced by R + delta with delta in {rho^2/10, rho^3/10}: relative residual >= 1e-3 at every one of the 100 points. |
| C12 | `add_xperturbed` | Rejected by Lemma L: X = c x + x^2/10, same R as C10: exact d_F >= 2 from the x-values at 10 points, numerical d_G = 4 (130 digits), so d_F + d_G = 6 > 5 for every (c, eps). |
| C13 | `trav_decomp` | v != 0. (i) Symbolic: E/X0^2 = sum_{k=1}^4 U^k E_k with E_1 = -2 m v ((1-v^2)(beta+m) + s2), E_2 = -4 beta^2 v^2 + 6 beta m v^2 - 2 beta m + c m (v^2+1) + 12 m^2 v^2 - 4 m^2 - 6 m s2 - s2^2, E_3 = 2 v (-4 beta^2 + 3 beta m + 3 c m + 13 m^2), E_4 = T_- T_+. (ii) The ten-term separation F = (X0 m(beta+m) [-2v(1-v^2)], X0 m [-2v], X0^2 Phi_2, X0^2 m, X0^2, X0^3 Phi_3 [2v], X0^3 m [6v], X0^4, X0^4 m, X0^4 Theta), G = (R0, R0 s2, R0^2, R0^2((v^2+1)c - 6 s2), -R0^2 s2^2, R0^3, R0^3 c, R0^4 c^2, 9 R0^4 c, R0^4), with Phi_2 = -4 v^2 beta^2 + (6v^2-2) beta m + (12v^2-4) m^2, Phi_3 = -4 beta^2 + 3 beta m + 13 m^2, is an exact identity for symbolic v. (iii) The exact rank of the coefficient matrix of E in the monomials of (X0, X1, X2) x monomials of (R0, R1, S0) is 10 at v in {1/3, 2, 5/7, 3/2, -2}. |
| C14 | `trav_gap` | An observation check, it passes when its statement holds: for R = rho^2 and v = 1/3, the numerical d_G = 5 (the rank bound alone does not exclude the traveling case). |

Observations, not criteria (printed): the rank at v = 1 and v = -1; the rank at v = 0 of the traveling matrix (6).

Part B (v != 0) beyond C13 and C14 is not specified here. If I add checks for it they are added by a dated amendment below
before they are run, with criteria and control targets. If none is added, the traveling case is reported as **not decided**.

## Controls (`--mutate=NAME` must exit non-zero and fail exactly its target check)

| control | target | change |
|---|---|---|
| `m-d-sign` | C1 `e_from_d` | Y := u_x u_rho - u u_x_rho / 2 in D |
| `m-theta` | C2 `decomp_static` | Theta with 19 m^2 in place of 20 m^2 in f_3 |
| `m-rank-off` | C3 `rank_lemma` | the planted pass uses N' = N with one column replaced by a vector not orthogonal to col(B) |
| `m-fdrop` | C4 `lemma_x` | f_3 and f_5 (rho Theta and Psi) set to 0 in the rank test |
| `m-gdrop` | C5 `lemma_rho` | g_4 := c and g_6 := 1 (so R = exp(kappa rho) has rank 2) |
| `m-const-sign` | C6 `const_m` | the exact product test over c = -n/10 (n in 0..60) instead of c = +n/10 |
| `m-sub-drop` | C7 `mult_subcases` | E_sub built with S0 in place of S0^2 |
| `m-add-drop` | C8 `add_decomp` | (X0 + R0)^2 replaced by X0^2 in E_add |
| `m-stratum` | C9 `add_stratum` | f_4 = X0 X2^2 dropped from f in the elimination |
| `m-add-freq` | C10 `add_planted` | J0(c rho), Y0(c rho) in place of J0(sqrt2 c rho), Y0(sqrt2 c rho) |
| `m-perturb-zero` | C11 `add_perturbed` | delta = 0 |
| `m-xperturb-zero` | C12 `add_xperturbed` | X = c x (no x^2/10) |
| `m-trav-rank` | C13 `trav_decomp` | rank expected 9 at v = 1/3 |
| `m-gap-d` | C14 `trav_gap` | R = rho^2 replaced by R = exp(rho) (d_G = 7) |

A control passes when the script's exit code is 1 and the failed checks are exactly its target. A control that is silent
(exit 0, or the target passes) is reported as silent, and no target is changed after the run without an amendment here, in the
note and in the closing comment. A control that crashes or hangs before its target runs counts as silent.

## Runs

Logs go to this folder, numbered (`dev_*.runN.log` for development, `run_01.log` for the run of record, `ctl_<name>.log`
and `.rc` for controls, exit codes in `.rc` files). Nothing is overwritten.

## Amendments

(none yet)
