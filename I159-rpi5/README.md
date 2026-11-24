# I159-rpi5: logs of notes/warp/conical_limit.py (do conical shifts with det R3 = 0 have limits at infinity?)

Machine rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process, one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/159. Branch `wip/i159-conical-limit`, worktree
`~/Source/negative-mass-i159` (main abcdf73). Python `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0,
mpmath 1.3.0). Written 2026-11-24, before the first run of record. Stop condition: a single run not finished after 1 h
of wall time is stopped and reported. Memory is reported, never a stop condition.

## Question

#80's `conical_limit` failed as written: for u = F(eta), eta = x/rho, the ODE N(F, F', F''; eta) = 0 of
`det_classify.md` section 6 allows F = F_inf (1 - 2/eta^2) at leading order for every F_inf != 0, and the pure power
series F_inf + a_2/eta^2 + a_3/eta^3 + ... fails at eta^-10 (condition F_inf^4 (F_inf^2 + 7) = 0). Question: does N = 0
have a real solution on (eta_0, infinity), eta_0 large, with F -> F_inf as eta -> infinity, for F_inf = 0 and for
F_inf != 0, and the same at eta -> -infinity? Logarithms (F = F_inf + sum a_{k,j} eta^-k (ln eta)^j), the branch
a_2 = 0, other Newton-polygon balances and exponentially small terms are to be tested.

## What was explored before this README (not of record)

Exploration scripts in the scratchpad (not kept) showed: N in the variables G = F, p = eta F', q = eta^2 F'' + eta F'
(theta = eta d/d eta) and nu = 1/eta contains nu only as nu^0, nu^2, nu^4; a pure series stops at eta^-10 as #80's
coordinator found, and with a log term the stage-by-stage solution exists through eta^-9; an inward mpmath
integration from eta = 1000 to 100 of F_inf = 1, a_4 = 0 matched the series to 6e-15. The eta values, case parameters and
series order below were fixed after that exploration, so that the series truncation error (about 1e-14 there) is
far below the issue's tolerance 1e-10; they are not changed after the first run of record. The solver stage-by-stage
code used one `sp.solve` of an overdetermined system and gave a wrong stage with too small a log degree; the script's
solver therefore checks the full residual (C7) and takes the log degree jmax = k/2.

## Method (what the script does)

1. N = 8 rho^6 D for u = F(x/rho) is rebuilt from D = h (h^2 - P^2 - Q^2 + Y^2 + Z^2) - P (Y^2 - Z^2) + 2 Q Y Z with
   P = -(u u_xx + u_x^2), Q = -(u_rhorho + u_rho/rho)/2, Z = u_xrho/2, Y = u u_xrho/2 + u_x u_rho, h = u_rho^2/2
   (the static block of det_classify.md Setup, retyped, not imported), from the jets of an undefined F(x/rho).
   Imported from `det_classify.py`: only `conical_N` (the typed N, as a comparison target). Shared with it: the
   formula for D, which is #65's lemma.
2. theta-form: with G = F, p = eta F', q = eta^2 F'' + eta F', nu = 1/eta, F' = p nu, F'' = (q - p) nu^2, N becomes a
   polynomial in (G, p, q, nu); the transseries are in nu = e^-t with T = t = ln eta, d/dt nu^k T^j = -k nu^k T^j + j nu^k T^(j-1).
3. Formal solver `formal_series(N, k0, c0, kmax, jmax)`: g = F - F_inf = c0 nu^k0 + sum over k0 < k <= kmax of
   nu^k (u_0 + u_1 T + ... + u_jmax T^jmax); at each k the lowest nonzero order of N is a polynomial in T that is linear in
   the u_j; it is solved (sympy `linsolve`), free u_j become named parameters, and if the lowest order contains no u
   the stage reports an obstruction (a condition on earlier coefficients). The same code is used for every ODE in
   this issue (planted ones included).
4. Newton polygon: N(G = F_inf + g, p, q, nu) as a polynomial in (g, p, q, nu); a monomial g^i p^b q^c nu^m is the point
   (d = i + b + c, m). For g ~ c nu^k T^alpha the weight of a point is k d + m. The lower hull gives the exponents k
   for which two or more points balance (edges), and the vertex polynomial in (k, c) when one point alone dominates
   (p -> -k c, q -> k^2 c for the leading nu^k).
5. Numerics: mpmath (40 digits), `odefun` (tolerance 1e-25, degree 14) in t = ln eta (reversed to integrate inward)
   on the state (G, p); q is the root of N(G, p, q, e^-t) = 0 found by `findroot` from the leading guess
   q = -p^2/(2 G nu^2). The series is the K = 9 series (through eta^-9, residual checked to nu^15).

## Criteria and tolerances (written before any run of record; each can fail)

Every criterion is exact (sympy) unless it says "numerical".

| id | check name | criterion |
|---|---|---|
| C1 | `n_build` | N built from the jets of F(x/rho) equals (a) `det_classify.conical_N()` as a polynomial; (b) the printed degree-3 part 2 F w^2 ((F^2 - 1) F'' - eta w) and degree-4 part -w^2 ((eta^2 + 1)(eta^2 + 2) F'^2 + 2 F (eta w + F'')) of det_classify.md section 6 (w = F' + eta F''), with every lower part zero; (c) 8 rho^6 D at 5 exact rational points (x, rho) for F = eta^3 - 2 eta + 1/3, with D from the jets of u(x, rho) = F(x/rho) by direct differentiation, equals N(F, F', F''; eta). |
| C2 | `theta_parity` | In (G, p, q, nu) N has only the powers nu^0, nu^2, nu^4, with coefficients A_0 = p^2 (p^4 - q^2), A_2 = 2 (G (q - p) + p^2)(G^2 q^2 + 2 G p^3 + 2 G p^2 q + 2 p^4 - q^2), A_1 = G^2 p^2 q^2 + 4 G p^4 q - 2 G q^3 + 4 p^6 - 3 p^2 q^2 (as the exploration printed them, retyped); so N(F0, -F1, F2; -eta) = N(F0, F1, F2; eta), and F(-eta) solves N = 0 when F(eta) does (the end eta -> -infinity is the mirror of eta -> +infinity). |
| C3 | `planted` | The solver of method 3, unchanged, on four planted ODEs written in (G, p, q, nu). P1: F'' + 2F'/eta = 0 (nu^2 (q + p) = 0): from k0 = 1 with c0 = c_1 free it returns the series F_inf + c_1/eta: coefficients at k = 2..8, every j, all zero. P2: the stage k = 0, j = 1..3 (the terms c ln(eta)^j) is forced to zero (rejected). P3: F'' + F'/eta = 0 (nu^2 q = 0): the stage k = 0 leaves the T coefficient free (F_inf + c ln eta accepted) and k0 = 1 with c_1 != 0 is an obstruction (c_1 = 0 forced). P4: the resonance mechanism with a known answer, q + 4p = 8 nu^4: no pure series (obstruction at k = 4 with jmax = 0), with logs g = (C - 2 T) nu^4 exactly (log coefficient -2, C free), all other coefficients to k = 8 zero. |
| C4 | `polygon` | Newton polygon of N. F_inf symbolic (nonzero): exactly one edge, at k = 2, edge polynomial proportional to c^3 (c + 2 F_inf), real roots c = 0 (multiplicity 3, excluded as a leading coefficient) and c = -2 F_inf; no vertex polynomial has a real root k > 0 with c != 0. F_inf = 0: no edge with k > 0, no vertex polynomial with a root k > 0, c != 0. With a logarithmic factor T^alpha, alpha != 0, at the edge the two monomials have different log orders, so one alone dominates and its coefficient is nonzero. |
| C5 | `a2_zero` | The branch a_2 = 0 and every other start: for g = nu^k (u_0 + u_1 T + u_2 T^2) from g = 0, k = 1, ..., 8, F_inf symbolic nonzero and F_inf = 0, the lowest-order condition has only u = 0 as solution except (F_inf != 0, k = 2) where it has the solutions u = (-2 F_inf, 0, 0) and u = 0. |
| C6 | `series_pure` | Solver with jmax = 0, k0 = 2, c0 = -2 F_inf, F_inf symbolic: the stage k = 3 gives u = 0 (a_3 = 0) at order nu^9, and the stage k = 4 reports an obstruction at order nu^10 with condition -512 F_inf^4 (F_inf^2 + 7) = 0 (the coordinator's K7 of `I80-mac/ind80.py`, not imported). |
| C7 | `series_log` | Solver with jmax = k/2 (rounded down, at least 1), through k = 9: every stage solved; exactly one free parameter, C = a_{4,0}; a_{4,1} = F_inf (F_inf^2 + 7); odd coefficients a_{3,j} = a_{5,j} = a_{7,j} = a_{9,j} = 0; the series substituted into N leaves zero residual in every order up to and including nu^15 (the first possibly nonzero order is nu^16); a_{4,1} != 0 for every real F_inf != 0 (the only real zero of F_inf (F_inf^2 + 7) is 0). |
| C8 | `reduced_system` | The reduced first-order system: with p = nu^2 r the equation divided by nu^8 is solved for r' (implicit function theorem: the partial derivative of the divided equation in r' at (G, r, nu^2) = (F_inf, 4 F_inf, 0) is nonzero for F_inf != 0), and the system G' = nu^2 r, r' = f(G, r, nu^2), (nu^2)' = -2 nu^2 has the line of equilibria r = 4 G, nu^2 = 0 with Jacobian eigenvalues (0, -2, -2). |
| C9 | `linear_modes` | The linearization of N about the C7 series: A = dN/dq, B = dN/dp, C = dN/dG at the series; the leading-order characteristic polynomial for delta ~ nu^k, A k^2 - B k + C, has roots k = 0 and k = 4 only, and A != 0 (so the linearized equation is a regular second-order equation and has no exponentially small, exp(-kappa eta), modes). |
| C10 | `num_inward` | Numerical. Four cases (F_inf, C) = (1, 0), (-1, 2), (1/3, -1), (2, 1/2) (C = a_{4,0}). Start at eta_1 = 1000 from the K = 9 series (values of G and p), integrate N = 0 inward, compare at eta_2 in {100, 50} with the K = 9 series: |G_num - G_series| <= 1e-10 and |p_num - p_series| <= 1e-10 (the issue's tolerance). The error bar reported is the spread of the comparison with the K = 8 series (a truncation estimate, not an enclosure). |
| C11 | `num_outward` | Numerical. From eta_0 = 100 take (G, p) = (G_s + 1/100, p_s * 6/5) of the (1, 0) series and integrate N = 0 outward to eta = 1e5 (t from 4.6 to 11.5). Fit (F_inf', C') by a 2 x 2 root find so that the K = 9 series matches (G, p) at eta = 1e5; then |G_num - G_series(F_inf', C')| <= 1e-10 and |p_num - p_series| <= 1e-10 at eta in {1e3, 1e4}. F_inf' != 1 is expected and reported (the limit of that solution). |
| C12 | `farfield_scale` | det_classify.md section 7's far-field condition uses the epsilon^3 coefficient of D for u = u_inf + epsilon w. For w = -2 u_inf rho^2/x^2 (the leading conical term) the epsilon^3 and epsilon^4 coefficients of D are both nonzero and proportional to rho^2/x^8, and their sum is zero at that order. (A discrepancy with section 7's "leading order" wording, reported not fixed.) |

## Planted truth

C3: the same solver on F'' + 2F'/eta = 0 (solutions F_inf + c/eta, no log) and F'' + F'/eta = 0 (solutions F_inf + c ln
eta), and on q + 4p = 8 nu^4 (known log coefficient -2).

## Controls (`--mutate=NAME`: the script exits non-zero and the named checks fail, no others of those run)

A control run skips the two numerical checks unless it names one of them as a target; the baseline run holds those.

| name | target | the change |
|---|---|---|
| `d-sign` | `n_build` | Y built as u u_xrho/2 - u_x u_rho |
| `parity-break` | `theta_parity` | one term eta^3 of the typed N replaced by eta^2 in the parity test |
| `theta-sub` | `theta_parity` | F'' = (q + p)/eta^2 in the substitution |
| `plant-wrong` | `planted` | P1 uses F'' + F'/eta |
| `plant-res` | `planted` | P4 with the forcing 0 in place of 8 nu^4 |
| `poly-drop` | `polygon` | the term -p^2 q^2 dropped from N before the polygon |
| `poly0-edge` | `polygon` | N + nu^4 q^2 (an edge at k = 2 appears for F_inf = 0) |
| `a2zero-edge` | `a2_zero` | the term -2 G nu^2 q^3 replaced by -2 G nu^3 q^3 (an edge at k = 3) |
| `series-8` | `series_pure` | expects F_inf^4 (F_inf^2 + 8) |
| `series-nolog` | `series_log` | jmax = 0 in the log run |
| `reduced-eig` | `reduced_system` | expects the eigenvalue +2 in place of -2 for r |
| `modes-a2` | `linear_modes` | the series with a_2 = -(11/5) F_inf in place of -2 F_inf |
| `num-nolog` | `num_inward`, `num_outward` | the series without the term a_{4,1} (data and comparison) |
| `ff-drop` | `farfield_scale` | the epsilon^4 coefficient dropped |

## Files

`README.md` (this file), `dev_*.log` (development runs, numbered, kept), `run_NN.log` and `run_NN.rc` (runs of record),
`ctl_<name>.log` and `.rc` (controls). Raw output of every run goes here; the script's own output is
`notes/warp/conical_limit_output.txt` in the repository.
