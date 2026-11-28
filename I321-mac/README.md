# I321-mac: criteria, development runs and runs of record for #321, the independent rederivation that the c = -1 growing mode is singular at S

Machine: the coordinator's Mac (Apple M5), runner `negative-mass-mac-i321`, worktree `~/Source/negative-mass-i321` on `wip/i321-log-at-S`, at most 2 processes, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/321. Script: `notes/black_universe/log_at_S.py` (imports nothing from the repository; mpmath, sympy only).
Python: `~/Source/negative-mass/.venv/bin/python`. Code commit of the runs of record: `b1ef08e` on `wip/i321-log-at-S`. Written before the runs of record (`runs/`); development runs are in `dev/` (`logs/d1`-`d4`, mutation development runs `mut_d1`-`mut_d3`).

## Question

#302 (`horizon_basis.md` Sec. 3) found that the exact growing mode of the c = -1 black universe, Y = c2 V R(rho(Pi)) with Y = dr - g dphi gauge invariant, is not the Y of a smooth perturbation at the bifurcation sphere S:
smooth data satisfy Y_N''(0) = -F_Pi(0) Y_N(0), Y = c2 V R violates it, and d_N dphi = -(pi/sqrt2) c2 ln|s| + O(1) there. Paper IV was corrected on that basis. The issue asks for a rederivation by code that shares nothing with
#302's `horizon_basis.py`, its slice constraint M or its Kruskal solvers: does a smooth solution with dr = c2 V on H+ and dr = 0 on H- exist, how does it differ from c2 V R, what is the coefficient of ln V, does a planted
smooth solution (the static mass mode) show no logarithm through the same code, and does a control with A''(0) changed move the coefficient as predicted.

## Method (two routes; neither reads `horizon_basis.py`, `full_slice.py`, `horizon_sector.py` or any solver)

**Route A, a formal series of the linearized equations (derive, series).** My own sympy Ricci tensor of ds^2 = -2 Om dV dU + hv dV^2 + hu dU^2 + r^2 dOmega^2 with R_ab = -2 theta_a theta_b + Vp g_ab (theta = phi/sqrt2, eps = -1),
-2 box theta = Vp_theta; the linearization is d/d eta of the equations at r = r0 + eta dr, Om = Om0 + eta dOm, theta = Th0 + eta dth, hv = eta hv, hu = eta hu (hv = hu = 0 is double-null gauge; all five fields are the general smooth gauge).
The background is the member (b, kappa) of the static family with the horizon at the throat (R^2 = b^2 + rho^2, theta = arctan(rho/b), A = 1 - R^2/b^2 + kappa (rho + R^2 arctan(rho/b)/b)), in Kruskal series
Pi = -VU, rho = G0 Pi + ..., Om0 = A/(2 kappa^2 Pi), with kappa a symbol (exact arithmetic over Q(kappa)). Fields are polynomials in V, U (total degree <= N) with an optional ln V factor; the equations are expanded
to total degree N - 2; the linear system is solved exactly (`DomainMatrix` over Q(kappa)). Y = dr - g dth, g = dr0/dTh0 = r0_Pi/Th0_Pi. Four questions are put to the same system:
(i) which linear relations among the Y coefficients y_ij (Y = sum y_ij V^i U^j) hold for every smooth solution (left nullspace of the map from the solution space to the Y coefficients); (ii) whether a smooth solution with
a prescribed Y exists (consistency of the augmented system); (iii) the same with logarithms allowed in every field, and the coefficient q of V ln V in dth (checked invariant over the whole solution space, gauge freedom included);
(iv) the same for the planted Y = c1 R, for Y = V + t V^2 U + ..., and for members with other (b, kappa, G0).

**Route B, the exact family in a double-null chart built from scratch (check).** #269's family (b = 1, c = -1, K = kappa = 2/pi, L = 1): ds^2 = -F dv^2 + 2 dv drho + r^2 dOmega^2, r = lam R, lam^2 = 1 + beta e^{kappa v},
F = A - 2 rho lam'/lam + 1/lam^2 - 1, phi = sqrt2 arctan rho. B1 checks it against my own Ricci tensor in this chart (own jets, 30 digits). The chart: V = e^{kappa v}, the outgoing null rays d rho/dv = F/2 integrated
with `mp.odefun` backward from a base ray V_b, U = -rho_b/V_b the label of the ray by its rho at V_b (zero gauge vector on the base ray; the label is a smooth function of the Kruskal U). delta phi(V, U) = d_beta phi at fixed (V, U)
by a central difference in beta (step 1e-9), d_V phi = Phi'(rho) F/(2 kappa V) along the ray, so no numerical derivative in V; the slope of d_V delta phi against ln V between decades is compared with -(pi/sqrt2) c2, with c2 read from
delta r = d_beta(lam R) on the ray U = 0 (B5), not assumed. Planted: the static mass mode r = sqrt(L) R, F = A + 1/L - 1 through the same ray and chart code, in its own Kruskal chart (V = e^{kappa_L v},
kappa_L = F'(rho_h)/2, U measured from rho_h) and, as a control of the chart, in the background's chart (V = e^{kappa v}), where the gauge xi^V = (d kappa/kappa) V ln V puts a log proportional to U into d_V delta phi (B4, predicted in closed form).

## What my code shares with #302's and what it does not

Shared (inputs, each tested against my own equations): the background closed forms A, R, theta = arctan(rho/b) and the Kruskal chart V = e^{kappa v}, U = -e^{-kappa u}, Pi = -VU (D1, D2: the series solves my
five equations); the definition Y = dr - (dr0/dTh0) dth (D4: it vanishes on every pure-gauge perturbation); the value of the target, Y = c2 V R(rho(Pi)) (S3: the log-extended system is consistent with it, inconsistent with
Y = V, mutation `rhs`); in Route B, #269's family (B1). Not shared: the equations (own Ricci), the linearization (D3: pure gauge solves it), the series solver, the slice constraint M, #258's slice code, #248's Kruskal solver
and its horizon functionals, the gauge-vector quadrature xi^u of #302's L2, the ray integration. What Route A does not use: any evolution; any numerical data.

## Planted cases (known answers, run before and through the same code as the real case)

| case | known answer | where |
|---|---|---|
| pure-gauge perturbations (xi^V, xi^U arbitrary polynomials) | solve the linearized equations; Y = 0 | D3, D4 |
| the background series | solves the five equations | D1, D2 |
| Y = c1 R, the static mass mode (smooth: exact static family r = sqrt(L) R) | a smooth solution, no log | S2, S4, B3 |
| Y = V + t V^2 U with t = F_Pi/2 | a smooth solution, q = 0 | S6 |
| the static mode in the fixed chart | the closed-form log of the gauge xi^V = (d kappa/kappa) V ln V | B4 |

## Criteria (declared before the runs of record)

Issue acceptance: I1 the coefficient of ln|s| (or ln V) is -(pi/sqrt2) c2 within 1 %, or the difference reported; I2 a planted smooth solution has no logarithm through the same code; I3 a control with A''(0) changed moves the
coefficient as predicted. Route A is exact (equalities of rational functions of kappa); the bars of Route B and of the series' residuals were set from development runs `d1`-`d4`.

| id | check | bar | issue |
|---|---|---|---|
| D1 | static chart, own Ricci: E_tt, E_rr, scalar vanish for the member (b, kappa symbolic) with Vp from E_thth; Vp = (1 - (rho A)')/R^2; A(0) = 0, A'(0) = 2 kappa, A''(0) = -2/b^2 | exact | all |
| D2 | the Kruskal series of the background solves VV, VU, UU, thth, scalar (b, G0) = (1, 1), (2, 1), (3/2, 3), N = 7 | no nonzero residual at total degree <= N + 1 = 8 | all |
| D3 | pure gauge, xi^V, xi^U arbitrary polynomials of degree 5 (general), and xi^V(V), xi^U(U) (double-null), solves the five linearized equations, same members | no nonzero residual at degree <= 8 | all |
| D4 | Y vanishes on those pure-gauge perturbations | no nonzero term at degree <= 8 | all |
| S1 | smooth solutions (truncated system, nullity 33, N = 7; and the general smooth gauge with hv, hu, N = 5): y21 = (F_Pi/2) y10, y12 = (F_Pi/2) y01 (F_Pi read from my Om0), Y_N''(0) = -F_Pi Y_N(0) (Y_N = (d_V + d_U) Y on V = s, U = -s), y_i0 = y_0i = 0 (i >= 2) lie in the span of the relations; y21 = 0 does not | exact (rank test over Q(kappa)) | I1 |
| S1b | a smooth solution with y00 = y01 = 0, y10 = 1 exists | consistent | I1 |
| S2 | smooth ansatz: no solution with Y = V R, Y = U R (also when only the degree <= 3 coefficients are imposed); a solution with Y = R | inconsistent, inconsistent, inconsistent; consistent | I1, I2 |
| S3 | log ansatz, Y = V R (double-null N = 7; general smooth gauge with logs in hv, hu, N = 5): consistent; q = coefficient of V ln V in dth equals -1/kappa for every solution | exact; spread over the solution space: none | I1 |
| S4 | log ansatz, Y = R (planted): q = 0 for every solution | exact | I2 |
| S5 | members (b, G0) = (1, 1), (2, 1), (3/2, 1), (1/2, 1), (1, 3), (2, 5/2), kappa symbolic: q = A''(0) c_h/(2 kappa), A''(0) read from my series | exact | I3 |
| S6 | Y = V + t V^2 U + ... (degrees <= 3 imposed), t = 0, 1/2, 1, 2 times F_Pi/2: q = 2t - F_Pi, a smooth solution iff t = F_Pi/2 | exact | I1, I2 |
| B1 | #269's family against my Ricci in the ingoing chart, 2 values of beta, 3 points | relative residual < 1e-20 (30 digits) | I1 |
| B5 | delta r on the ray U = 0: c1 = 0, c2 = 1/2 per unit beta | c2 to 1e-8, c1 < 1e-12, delta r/V constant to 1e-6 over V = 1e-3 ... 1e-7 | I1 |
| B2 | slope of d_V delta phi against ln V over -(pi/sqrt2) c2: V_b = 1, 0.05 and U = -0.5, -1, between decades down to V = 1e-8 | \|ratio - 1\| < 1e-4 at V = 1e-8 and smaller than at V = 1e-6 | I1 |
| X1 | the ratio of B2 (V_b = 1, U = -0.5) at V = 1e-8 against 1, and against the same with 10x the step in beta | 1e-5; 1e-8 | I1 |
| B3 | planted static mass mode in its own chart, dL = +-1e-9, U = -0.5, -1: slope over (pi/sqrt2)/2 at V = 1e-8 | < 1e-6 | I2 |
| B4 | the same mode in the chart V = e^{kappa v}: slope against the closed form sqrt2 U_K/(2 kappa^2), U_K = -Pi(rho_b)/V_b, Pi = rho exp(2 kappa int_0^rho (1/A - 1/(2 kappa t)) dt) | 1e-3 | I2 |

Error bars are comparisons of two computations, not uncertainties. "Spread" in S3 and S4 is whether the coefficient changes when any vector of the nullspace (gauge freedom, constraint-free parts, the top-degree unknowns
of the truncation) is added to the particular solution.

## Mutations (declared; each effect computed in development before this README: `dev/mut_d1`, `mut_d2`, `mut_d3`)

| name | command | what it breaks | fires |
|---|---|---|---|
| eps | derive | the sign of the scalar's kinetic term (canonical instead of phantom) in every equation | D1, D2, D3 |
| a2 | derive | A''(0): the rho^2 coefficient of A in the background series times 1.01 | D2, D3 |
| om | derive | the normalization Om0 = A/(kappa^2 Pi) instead of A/(2 kappa^2 Pi) | D2, D3 |
| gauge | derive | the sign of Om0 (d_V xi^V + d_U xi^U) in the Lie derivative of the pure-gauge perturbation | D3 |
| gth | derive | g = dr0/dTh0 times 1.01 in Y | D4 |
| fpi | series | F_Pi doubled in the forms of S1 and in the t of S6 | S1, S1g, S6 |
| nolog | series | the log ansatz replaced by the smooth one in the solves of S3 to S6 | S3, S4, S5, S6 |
| pred | series | the predicted q of S5 with A''(0) times 1.01 | S5 |
| rhs | series | the target Y = V (R replaced by 1) in the log solves | S3, S5, S6 |
| hor | series | S1b also imposes y20 = 1, against the horizon law | S1b |
| s2t | series | S2's degree <= 3 target for Y = V R gains the V^2 U term (F_Pi/2) smooth solutions need | S2 |
| rate | check | K = 1.01 kappa in the family (exponent and (1 + K rho)) | B1, B2, B5, X1 |
| h | check | the 1/lam^2 - 1 term dropped from F | B1, B2, X1 |
| beta | check | the sign of beta in F (not in r) | B1, B2, X1 |
| phi | check | dtheta/drho times 1.01 | B1, B2, B4, X1 |
| chart | check | B3 in the background's chart V = e^{kappa v} instead of its own | B3 |
| pgauge | check | B4's prediction with the sign of d kappa/kappa flipped | B4 |
| step | check | the step in beta 0.3 instead of 1e-9 | B5, X1 |

`run_mut.sh` runs one mutation (derive: 7 s, series: 80 s, check: 210 s); the fired sets are compared with this table by `log_at_S.py mutations DIR PREFIX`. The development logs: `mut_d1` (derive), `mut_d2` (fpi, nolog, pred, rhs;
`nolog` first crashed in S6, fixed, rerun in `mut_d3`), `mut_d3` (nolog, rate, h, beta, phi, chart, pgauge; `step` was stopped after 12 min, see below, log `step_aborted_run1.log`), `mut_d4` (step), `mut_d5` (fpi with the final code),
`mut_d6` (hor, s2t).

Blind spots, kept: S1b and S2 are fired only by the contrived `hor` and `s2t`; `a2` and `om` corrupt the background and are run under `derive` only (S1 to S6 under them were not run); `eps`, `a2`, `om`, `gauge` and `gth` are not run under `series`
(`gth` also enters the series' Y; it was not run there); B1 is not fired by `chart`, `pgauge`, `step`; X1 fires whenever B2 does, and fires alone only through the step.

## Changes after development runs (named so the bars of record are not read as pre-registered against data)

- D2, D3, D4: the first draft's bar was "no residual at degree <= TRUNC - 2 = 9"; the residual of the linearized operator on pure gauge first appears at degree 9 (the jets of the truncated background lose two orders), so the bar is degree <= 8 (d1: D3 failed at 9). The solver uses equations of degree <= N - 2 = 5.
- S1 was printed twice (double-null and general gauge); the second carries the id `S1g`.
- S6: a log-ansatz solve without log columns (`nolog`) crashed in `fmt(None)` (mut_d2); it now counts as a failed check.
- X1: the second step in beta was 10 eps; with the mutation `step` (eps = 0.3) it was beta = 3, where lam^2 = 1 + beta V changes sign and `mp.odefun` did not return in 12 min (log `step_aborted_run1.log`, stopped by PID). The second step is eps/10.
- Added `hor` and `s2t` after d3, because no mutation could fire S1b or S2 (mut_d6); `S1` is scored on relations of degree <= 4 (first draft 5) so that the printed relations contain no degree 5 pivots; `--only` works for `series`.
- The bars of B2, B3, B4 were written into the script before the first Route B run (d4) and not changed; d4 gave |ratio - 1| = 1.7e-6, 7.1e-6, 8.7e-7, 1.8e-6 at V = 1e-8 (bar 1e-4), B3 6.3e-8 and 6.8e-7 (bar 1e-6), B4 matches to 5e-6 (bar 1e-3).

## Layout

```
I321-mac/
  README.md          this file
  run_mut.sh         run_mut.sh ABSOLUTE_OUT PREFIX NAME...   (one process each, nice 10)
  dev/               logs/d1-d4 (derive twice, series, check), mut_d1 (derive mutations), mut_d2 (series), mut_d3 (check)
  runs/              the runs of record: derive.log, series.log, check.log, mut_*.log (added after this README)
```

## Runs of record (`runs/`, code commit b1ef08e, `nice -n 10`, one process each, `run_main.sh` and `run_mut.sh`)

| command | exit | time, peak memory | result |
|---|---|---|---|
| `log_at_S.py derive` | 0 | 7 s, 84 MB | 4 of 4 (D1 to D4) |
| `log_at_S.py series` | 0 | 80 s, 88 MB | 8 of 8 (S1, S1b, S1g, S2 to S6) |
| `log_at_S.py check` | 0 | 211 s, 77 MB | 6 of 6 (B1, B5, B2, X1, B3, B4) |
| 18 mutations (`mut_*.log`) | 1 each (each fires) | 7 s (derive), about 85 s (series), about 210 s (check) | `mutations.log`: 18 of 18 fired sets equal the declared ones |

Nothing failed in the runs of record and no check disagrees with #302: the coefficient of ln V is -(pi/sqrt2) c2 exactly in Route A and 1 + 1.7e-6 ... 7.1e-6 of it in Route B at V = 1e-8. Two refinements of #302's text are in
`notes/black_universe/log_at_S.md` Sec. 2 and 9 (the smooth relations hold per branch, y21 = (F_Pi/2) y10 and y12 = (F_Pi/2) y01, not only in the sum). `dev/probes/` holds the development scripts (`lib1-3`, `p1`-`p11`, `pB1`, `pB2`) and
the outputs of `p2`, `p7`, `p9`, `p10`, `p11` rerun after the runs of record (q = -1/kappa at N = 6, 7, 8 and in general smooth gauge, other (b, kappa), the relations at N = 6, 7); the other probes' outputs were on the terminal only.
The stale `E01.pkl` and `__pycache__` of the probes were removed or moved to the Trash.
