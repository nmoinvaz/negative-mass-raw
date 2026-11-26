# I168-rpi5: logs of notes/warp/conical_attraction.py (attraction to the conical family's line of equilibria)

Machine rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process, one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/168. Branch `wip/i168-conical-attraction`, worktree
`~/Source/negative-mass-i168` (main fac9fcf). Python `~/Source/negative-mass-venv314/bin/python` (3.14.10, sympy 1.14.0,
mpmath 1.3.0, numpy). Written 2026-11-25, before the first run of record. Stop condition: a single run not finished
after 1 h of wall time is stopped and reported. Memory is reported, never a stop condition.

## Question and route

#159 left four things conditional (`conical_limit.md` §4, §2, §6): (i) every solution of N = 0 starting near the line of
equilibria {(G, 4G, 0)} of the reduced system converges to a point of it; (ii) the formal series of §3 is the asymptotic
expansion of these solutions; (iii) oscillating approaches (assumption H) cannot occur; (iv) the same for F_inf = 0.

**Route: a written proof, no cited theorem.** The system is reduced to one scalar equation, a Gronwall bootstrap with
explicit constants proves (i), induction on the order proves (ii), and an analysis of the cubic N = 0 in q = F'' decides
(iii) and (iv). Aulbach, LNM 1058 (1984), is looked up at the publisher in the note, but nothing here uses it. A step that is
only cited or sketched makes the result *conditional* on it; the note says which.

## What was explored before this README (not of record)

Scratch scripts (not kept) showed: (a) N / p^6 is a cubic P(w) in w = q / p^2 with coefficients in sigma = nu^2,
a = G sigma, b = G^2 sigma and omega = 2 G sigma / p, written below; a random scan of 2e5 parameter points in the box
sigma + b <= 1/500, |omega| <= 100 found exactly one real root w <= -1/(4a), all other real roots in (-2, 2), such roots
only for |omega| <= 1.0019, and for |omega| <= 1/2 one root in (1/2, 2) and one in (-2, -1/2). (b) The reduced system
with the huge root integrates to the same G as a direct integration of N = 0 (differences 3e-15 in G). (c) Rational
interval arithmetic gives the constants below (c_e on y in [7/2, 9/2] came out 50.9). (d) An exact `Fraction` solver
for the series reproduces #159's coefficients and finds one free parameter C = a_{4,0} (rank 4 of 5 columns at k = 4,
full column rank at every other stage k = 3..9, J = k/2 + 2 unknown log degrees). (e) For data inside the neighborhood of
Theorem A (G_0 = 1, zeta_0 = 0.2, eta_0 = 45, F_inf = 1.001011946801174..., C = -123.0139833...) the normalized errors
e_m(eta) = |F - F^(2m)| / (nu^(2m+2) (1 + ln eta)^m) at eta = 100, 200, 400, 800 were between 9 and 2.5e4 and decrease with eta
for every m = 1..4; the thresholds of M11 were set from that. The constants, the thresholds and the case lists below are
fixed after this exploration and are not changed after the first run of record.

## Notation and facts used

t = ln eta, nu = 1/eta, sigma = nu^2, G = F, p = eta F', q = eta^2 F'' + eta F', r = eta^3 F' = p / sigma, s = eta^4 F'' + eta^3 F'
= q / sigma = r' - 2r (' = d/dt). y = r / G, zeta = y - 4, a = G sigma, b = G^2 sigma, u = sigma + b = sigma (1 + G^2),
omega = 2 G sigma / p = 2 / y, w = q / p^2. N = A0 + nu^2 A1 + nu^4 A2 with A0, A1, A2 of `conical_limit.md` §1.

    kappa = 1 - b + sigma,  mu = 1 + 3 sigma - b + 2 sigma^2 - 6 b sigma,  c = 1 + 2 sigma,  M = mu + (b - sigma) omega
    P(w)  = -2 a kappa w^3 - M w^2 + 4 a c w + c^2 - omega^2           (N = p^6 P(q / p^2))
    N = c3 q^3 + c2 q^2 + c1 q + c0,  c3 = -2 G sigma kappa,  c2 = -p (2 G (G^2 - 1) sigma^2 + p mu),
        c1 = 4 G sigma c p^4,  c0 = p^4 (c^2 p^2 - 4 G^2 sigma^2)
    huge root: w = -x, x >= 1/(4a);   e-hat := y^2 (1 - 2 a x) = (r^2 + 2 G s) / G^2
    y' = y (4 - y) / 2 - sigma y^2 + e-hat / 2,   (ln |G|)' = sigma y,   sigma' = -2 sigma

Assumed, not re-derived here: N = 8 rho^6 D with D of `det_classify.md` Setup (#65's lemma, #80, #159; `conical_limit.md` §1
checked it, and the coordinator's `ind159.py` M1 did independently). The script retypes D and the theta-form and compares.

## Theorems to be written (note `conical_attraction.md`)

- **A (attraction).** G_0 != 0 (G_0 > 0 by F -> -F), |zeta_0| <= 1/4, u_0 = sigma_0 (1 + G_0^2) <= 1/1000, F'' on the huge root:
  then the solution exists on [eta_0, inf), |zeta| <= B e^{-7t/4} with B <= 0.451, |zeta| <= 1.14 (|zeta_0| + 50 ubar t) e^{-2t},
  G -> G_inf != 0 with |ln (G / G_inf)| <= (9/4) sigma. Existence for all such data. Rate (1 + t) e^{-2t} is sharp.
- **B (expansion).** For every m >= 1, |F - F^(2m)| <= M_m nu^(2m+2) (1 + ln eta)^m, F^(2m) the series of §3 truncated at nu^(2m), C = C(solution).
- **O (oscillation, classification).** F in C^2 on [eta_0, inf) with N = 0 and F -> F_inf: F is eventually constant, or
  F_inf != 0 and F is in Theorem A's family; in particular F_inf = 0 only for F eventually 0, and F - F_inf never oscillates.

## Criteria (each is coded exactly as worded; exact = Fraction/sympy equality or rational interval arithmetic)

All interval statements: sigma, b in [0, U], sigma + b <= U = 1/500, a^2 = sigma b (so a <= U/2), intervals over sigma, b, a.

| id | check | statement that must hold | kind |
|---|---|---|---|
| M1 | `n_identity` | (a) N built from D (retyped) = A0 + nu^2 A1 + nu^4 A2; (b) N = c3 q^3 + c2 q^2 + c1 q + c0 with the c_i above; (c) N = p^6 P(q/p^2) with omega = 2 G sigma / p; (d) N(-G, -p, -q) = N; (e) R := N / sigma^4 at p = sigma r, q = sigma s equals sigma^2 r^6 P(s / (sigma r^2)) | exact |
| M2 | `reduction` | (a) from G' = sigma r, r' = 2r + s, s = (G^2 e-hat - r^2) / (2G): y' = y(4 - y)/2 - sigma y^2 + e-hat/2 and (ln G)' = sigma y; (b) e-hat solves rho(e-hat; y, sigma, g2) = 0 with rho = R / G^4, d rho / d e-hat = -y^4/4 at (e-hat, sigma) = (0, 0), and e-hat = -8 (g2 + 3) sigma + O(sigma^2) at y = 4; (c) f(zeta, sigma, g2) = -zeta^2/2 + e-hat/2 - sigma (4 + zeta)^2 has f(0,0) = 0, f_zeta(0,0) = 0, f_sigma(0,0) = -4 (g2 + 7); (d) the Jacobian of (G' = sigma r, r' = 2r + s, sigma' = -2 sigma) at (G, 4G, 0) has eigenvalues 0, -2, -2 and rank(J + 2I) = 2 for every real G | exact |
| M3 | `hyp_line_real` | `hyp_line` (hypotheses of the normally attracting line: analytic, equilibrium set is the line, zero is a simple eigenvalue with the line as eigenvector, the other eigenvalues have Re < 0) says "attracting, Jordan block" at G = -3, -1/2, 1, 2, 7 | exact |
| M4 | `shape` | omega in [-100, 100]: (i) kappa >= 0.99, mu >= 0.99, 1 <= c <= 1.01, M >= 0.79; (ii) 4M - 3 kappa > 0; (iii) 32 a^2 P(-1/(4a)) = kappa - 2M + 32 a^2 (c^2 - c - omega^2) < 0; (iv) P(2) < 0 and P(-2) < 0; (v) a real root w in [-2, 2] forces omega^2 <= c^2 + 16 a kappa + 8 a c <= 1.05^2. For |omega| <= 1/2: P(0), P(1/2), P(-1/2) > 0. The concavity of P' and the root count follow (symbolic: disc P' > 0, P'(0) > 0). Conclusion L1: exactly one real root <= -1/(4a), simple; all other real roots in (-2, 2); for |omega| <= 1/2 one in (1/2, 2) and one in (-2, -1/2) | rational intervals + symbolic |
| M5 | `ehat` | for y >= 1/50 and the huge root x: 1 - 2 a x = (kappa - M)/kappa - (4 a c / x + (omega^2 - c^2)/x^2)/kappa (exact); with 1/x <= 4a the bounds y^2 [2 sigma + 2 sigma^2 + 6 b sigma + 4u^2 (c + c^2)]/kappa <= (51/25) u y^2, 2 y \|b - sigma\|/kappa <= (201/100) u y, 64 a^2/kappa <= (321/10000) u hold, and (321/10000) <= (8/5) y for y >= 1/50, so \|e-hat\| <= u (alpha y^2 + beta y) with alpha = 51/25, beta = 181/50 | exact + rational intervals |
| M6 | `theorem_a` | rational chain: c_e = alpha (9/2)^2 + beta (9/2) <= 58; c_f = 50 >= c_e/2 + (9/2)^2; ubar <= e^{9/2000}/1000 <= 1.0046/1000; B = 1/4 + 4 c_f ubar <= 0.451 < 1/2; kappa_z = 2 - (1/2)/2 = 7/4; H = B/(2 kappa_z) <= 0.129; e^H <= 1.14; sigma_0 <= u_0 <= 1/1000 <= U; y in [7/2, 9/2] subset [1/50, inf) | exact (Fraction, rigorous exp bound) |
| M7 | `numeric_a` | reduced system, float RK4 h = 1/200 to t = 20, at G_0 in {1e-2, 0.3, 1, 3, 30}, zeta_0 in {-1/4, 0, 1/4}, sigma_0 = 1/(1000 (1 + G_0^2)): every step satisfies \|zeta\| <= B e^{-7t/4}, \|zeta\| <= 1.14 (\|zeta_0\| + 50 ubar t) e^{-2t}, \|e-hat\| <= u (alpha y^2 + beta y), \|ln (G/G_inf)\| <= (9/4) sigma; and direct integration of N = 0 (theta-form, Newton in q) agrees with the reduced system to 1e-9 in G and y at t = 6 for two cases | numerical evidence, tolerance 1e-9 |
| M8 | `series` | exact solver (Fractions): at F_inf in {1, -3/2, 2/7, 5}, C in {0, 3, -5/2}: stage k = 3..9 has full column rank except k = 4 (null space dimension 1, direction a_{4,0}); coefficients equal §3's table (a_{2,0} = -2F, a_{4,1} = F (F^2 + 7), a_{6,0}, a_{6,1}, a_{6,2}, a_{8,3} as typed there); the first nonzero N coefficient is nu^16; odd coefficients zero | exact |
| M9 | `stage_symbol` | the linearization of N about g = -2 F nu^2 has leading symbol I(k) = -128 F^3 k (k - 4) (A k^2 - B k with dN/dq = -128 F^3 nu^6, dN/dp = -512 F^3 nu^6), so every stage k >= 3, k != 4 is uniquely solvable for all k | exact, symbolic |
| M10 | `expansion_link` | with the series of M8: zeta~ = eta^3 F~'/F~ - 4 has sigma^1 t^1 coefficient -4 (F^2 + 7) = f_sigma, and its sigma^1 t^0 coefficient is affine in C with slope -4/F != 0; ln (F~/F) = -2 sigma + O(sigma^2 t) | exact |
| M11 | `numeric_b` | mpmath odefun (30 digits) of the reduced system from G_0 = 1, zeta_0 = 1/5, eta_0 = 45 to eta = 1e7; F_inf from G(1e7) e^{2 sigma}; C fitted at eta = 1000; e_m(eta) <= 1e5 for m = 1..4 and eta in {100, 200, 400, 800} | numerical evidence, 1e5 |
| M12 | `local_lemma` | (a) c2 = p c2~, c1 = p^4 c1~, c0 = p^4 c0~ with polynomial c_i~ (divisibility); (b) every real root satisfies \|q\| <= 3 max(\|c2/c3\|, \|c1/c3\|^(1/2), \|c0/c3\|^(1/3)) (proved by hand in the note, tested on 1e4 random roots); (c) N(G, 0, q, nu) = c3 q^3, c3 != 0 iff G != 0 and kappa != 0 | exact + numeric test |
| M13 | `regime_b` | for \|y\| <= 1/50, G sigma <= 1/1000, u <= U: every root has \|s\| <= (1/10) \|r\| (interval constants 3 max(...) <= 0.037) | rational intervals |
| M14 | `small_branch` | on small roots (\|w\| <= 2) with \|omega\| >= 1/2: (ln\|omega\|)' = p/G - 2 - p w <= -1 (needs 4 sigma (1 + 2G) <= 1; G <= g2 gives sigma <= 1/(4 (1 + 2 g2))); the four sign cases of (1/p)' = -w are as in the note | exact + intervals |
| M15 | `huge_branch` | with \|e-hat\| <= u (alpha y^2 + beta y), u <= 1/500: y' >= (149/100) y on [1/50, 1]; y' >= 1/10 on [1, 15/4]; y' <= -(104/1000) y on [17/4, inf); for y >= 8 G^-1... : r' <= 2r - r^2/(4G) | rational intervals |
| M16 | `classify_numeric` | float RK4 of (ln G, y) with the root w tracked by continuity, G_0 in {0.5, 2}, eta_0 = 100: huge root, y_0 in {0.5, 8, 30}: \|y(15) - 4\| <= 1e-6; huge, y_0 in {-0.5, -4}: \|y\| > 1e6 before t = 15; small roots (G_0 = 1, y_0 = 3 and 6, p > 0, both roots) and (y_0 = -3, -6): w stays in (-2, -1/2) or (1/2, 2) on [3, 15] | numerical evidence |

## Planted cases (run first, through the same functions as the real cases)

| id | what | must give |
|---|---|---|
| P1 `planted_hyp` | `hyp_line` on x' = A x, A = [[0,0,0],[0,-2,1],[0,0,-2]] (Jordan block), on diag(0,-2,2) and on diag(0,0,-2) | attracting with Jordan block, and closed form \|x_2,3(t)\| <= (1 + t) e^{-2t} \|x_0\|; "not attracting"; "kernel larger than the line" |
| P2 `planted_gronwall` | the bootstrap chain on zeta' = -2 zeta + ubar e^{-2t} (exact (zeta_0 + ubar t) e^{-2t}) | chain's bound >= exact on a grid, and equal to it in the rate part (c_f = 1) |
| P3 `planted_shape` | root counter on P_pl(w) = -2a (w + 1/(2a)) (w^2 - 1), a = 1/100, and on the same with M < 0 | roots -50, -1, 1 classified as 1 huge + 2 small; the M < 0 variant reported as hypothesis failure |
| P4 `planted_local` | `local_lemma` test on N_osc = nu^2 (q - p) + G (F'' + F = 0) | "not applicable": N_osc(G, 0, q) != c3 q^3, and F = cos eta has F' = 0, F'' != 0 |
| P5 `planted_series` | the solver on q + p = 0 and q + 4 p = 8 nu^4 | F_inf + c nu with no log; the forced log -2 at nu^4 |

## Controls (mutations; targets are declared after a development run, see "Amendments" below)

Names and intended mutations (prediction only until declared): `d-sign` (M1), `P-drop` (M1), `ehat-sign` (M2), `f-sigma` (M2),
`eig-plus` (M2, M3), `shape-3` (M4), `shape-om` (M4), `ehat-alpha` (M5), `A-u0` (M6), `A-cf` (M6), `A-kappa` (P2, M6),
`num-rate` (M7), `series-a2` (M8), `series-8` (M8), `stage-I` (M9), `link-slope` (M10), `numB-coef` (M11), `local-c2` (M12),
`regimeb-y` (M13), `small-sigma` (M14), `huge-thr` (M15), `class-sign` (M16), `plant-hyp` (P1), `plant-gron` (P2),
`plant-shape` (P3), `plant-local` (P4), `plant-series` (P5).

## Run plan

`run_final.sh NN` runs `conical_attraction.py --logdir=RAW` (checks, then every control) detached under systemd, exit code
in `rcNN`. Development logs `dev_NN`, runs of record `run_NN`, controls `ctl_<name>.log/.rc`. A failed check or a silent control
is reported, not repaired, and a criterion is not changed after seeing data (ask the coordinator).

## Amendments

(none yet)
