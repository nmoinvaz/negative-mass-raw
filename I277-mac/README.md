# I277-mac: #269's exact time-dependent family as planted truth for #217's nonlinear double-null code (criteria, development logs, runs)

Machine: the coordinator's Mac (Apple M5, macOS, shared), negative-mass-mac-i277, worktree `~/Source/negative-mass-i277`, branch `wip/i277-planted-family`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/277 ("Use #269's exact family as planted truth for the black-universe nonlinear code", milestone G9).
Python 3.14.7, numpy 2.5.4, numba, scipy, sympy, mpmath (`~/Source/negative-mass/.venv`), `nice -n 10`, `NUMBA_NUM_THREADS=1`, one process at a time.
Code: `notes/black_universe/planted_family.py`; the criteria below are declared at commit 4ee1c6b, before any run of record. Status words as in AGENTS.md.

## What the folder holds

```
README.md        this file: the chart map, the declared design, the criteria, the mutations with their computed effects
dev/             development logs dev_01 ... dev_11 (kept, never overwritten); dev/scripts/ the scratch drivers of dev_04, 05, 06, 09
runs/            the runs of record (written after this file is committed): check_none.log, check_<mutation>.log, .rc, .err, results_*.json
```

## The chart map (the question the issue leaves to the runner)

The family is in the ingoing null chart (v, rho): ds^2 = -F dv^2 + 2 dv drho + r^2 dOmega^2, r = lam(v) R(rho), phi = sqrt2 arctan(rho), F = A - 2 rho lam'/lam + 1/lam^2 - 1,
lam^2 = L + beta e^{Kv}, K = -2c/pi (exact_mode.md). The code is double null, ds^2 = -2 e^{-f} dx+ dx- + r^2 dOmega^2, with data r, f, phi on x- = 0 and on x+ = 0.

- **x+ is v.** x+ and v are both constant on ingoing rays, so x+ = (v - v0)/sqrt2 on the whole rectangle (v0 = 0). The ray x- = 0 is parametrized by it.
- **x- labels the outgoing rays**, drho/dv = F(v, rho)/2. The ray x+ = 0 (v = v0) is an ingoing ray; its parameter is the tortoise-like x- with drho/dx- = -F(v0, rho)/sqrt2,
  rho(0) = rho_c = 1, that is e^{-f} = F(v0, rho) there. At beta = 0 this is #217's gauge e^{-f} = A, so the member's data are the special case.
- **The gauge on the other ray follows.** The metric is 2 rho_{x-} dv dx- = -2 e^{-f} dx+ dx-, so e^{-f} = -sqrt2 w with w = d rho/d x- at fixed v. Differentiating the characteristic equation,
  w_v = F' w/2 (F' = dF/drho = A' - 2 lam'/lam). Along an outgoing ray, d rho/dv = F/2 and d ln e^{-f}/dv = F'/2. The ray x- = 0 starts at rho_c with e^{-f} = F(v0, rho_c).
- **The exact fields on the whole rectangle** are the same flow for every x- (rho0 from the left ray), then r = lam(v) R(rho), f = -ln e^{-f}, phi = sqrt2 arctan(rho).
- **A gauge-invariant read-out.** Lambda^2 = r^2 cos^2(phi/sqrt2) = r^2/(1 + rho^2) = lam(v)^2 at every x-, from the evolved r and phi only. v* = ln(-L/beta)/K is where it vanishes.
- **What the chart cannot show.** For beta < 0 every outgoing ray reaches rho = +infinity as v -> v* (1 + K rho ~ (v* - v)^{-1/2}) while r stays finite there; r -> 0 only at fixed rho, which the rectangle
  does not contain, so v* is not an event of the code's grid: it is read from Lambda^2. For beta > 0 the outgoing rays run to rho = -infinity at a finite v (F < 0 at late v), where the integration of the exact map fails
  (dev_02: the flow stops between v = 4.24 and 5.66 at c = -1.5, x- extent 8). The rectangles below stay clear of both.

## Declared design

| item | value |
|---|---|
| members | c = -1.5 (K = 0.95493, v* = 3.137124 at beta = -0.05), c = -1 (K = 0.63662, v* = 4.705685) |
| beta | +0.05 and -0.05 at each member, L = 1, so four cases |
| corner | v0 = 0, rho_c = 1 |
| rectangle | x+ in [0, 2.16] at c = -1.5 (v up to 3.0547, lam^2 = 0.076 at beta = -0.05), x+ in [0, 3.20] at c = -1 (v up to 4.5255, lam^2 = 0.108); x- in [0, 16] (f up to 14) |
| resolutions | h = 0.02, 0.01, 0.005, 0.0025, 0.00125 (four ratios per case); the largest rectangle has 2560 x 12800 cells |
| kernel | `evolve.row_step` of #217, unchanged, imported; excision off (rcut 0, fcut 1e300); `evolve.params(Member(c))` |
| exact map | outgoing-ray flow, DOP853 rtol 1e-12, atol 1e-13; the left ray rtol 1e-13 |

The x+ extents come from the development runs (dev_05): the error ratio stays within 3.8 to 4.0 down to lam^2 = 0.04 to 0.02 at beta = -0.05 and degrades to 3.49, 3.77, 3.92 at lam^2 = 0.007 (c = -1, h = 0.02 to 0.0025), so the
declared rectangles end where lam^2 is 0.08 to 0.11. The x- extent is not a tuned value: the error ratio and the sup error do not change between 4 and 16 (dev_06). The same x+ extent is used for both signs of beta.

## Criteria (each can fail; written before the runs of record; an unmet criterion is reported as not met)

Data path, all at the four cases:

| id | what | bar |
|---|---|---|
| D1 | the module's closed forms r = lam R, F and the potential V(phi(rho)), V'(phi) (`evolve_potential.pot`) equal exact_mode's sympy forms at 50 digits, 20 random points per case | relative 1e-13 |
| D1b | the module's hand-written jets (r, f, phi; their x+ and x- derivatives, mixed and second) equal the chain-rule jets of exact_mode's closed forms at 50 digits, 12 points per case, 13 jets | relative 1e-12 |
| D2 | **the family's residuals in #217's equations**: `evolve.F_np` and the numba `_F` on the family's jets give r+-, f+-, phi+- (the three evolution equations, with V); residuals printed per case and component, 400 random points (v, rho, e^{-f}, gauge q) | relative 1e-12 |
| D3 | the family's jets satisfy the null constraints C++ and C-- (eps = -1), 400 points per case | relative to the largest term 1e-12 |
| D4 | C++ on the stored right-ray data, central differences, relative to its largest term | at most 1e-3 at h = 0.00125, falls by at least 2.5 per halving |
| D5 | the exact map's tolerances tightened to 1e-13: change in r, f, phi | 1e-10 |
| D6 | the module's row sweep equals `evolve.run_grid` on the family's data (N = 100, h = 0.02) | numba bit-identical, numpy 1e-12 |
| PL1 | planted errors C h^p through the ratio band: p = 2 accepted, p = 1.8, 2.2, 1 rejected | as stated |
| PL2 | planted Lambda^2 = 1 + beta e^{Kv}: the v* finder recovers v* to 1e-10 (three beta), stays inside 1e-3 at noise 1e-5 (40 seeds); a finder with the rate x 1.01 misses by more than 1e-3 | as stated |

Acceptance of the issue:

| id | what | bar |
|---|---|---|
| O | the evolved r against lam(v) R(rho) at every node of the rectangle: the sup error falls by **4.0 +- 0.3 per halving of h** (all four ratios of the five h, all four cases) | ratios in [3.7, 4.3] |
| V | for beta < 0, v* is found from the evolved interior Lambda^2 (rows i >= 1, columns j >= 1, mean over j, least-squares fit of a + b e^{Kv}, v* = ln(-a/b)/K) | within 1e-3 at every h and both members |
| S | the beta sign mutation (data from -beta, compared with +beta) exits 1 and fires O and V | as stated |

Reported, not criteria: the ratios for f and phi; the sup error relative to r; the direct estimate v* = v - ln(1 - Lambda^2)/K of the last row (needs L = 1); the running sup error over the first 1/4, 1/2, 3/4 of v;
the error ratios of the v* finder.

**What the error bars are.** The sup errors are the discretization error of the kernel against an independently integrated exact map (D5 bounds its own error at 1e-11); they are not fit errors.
The v* error is the difference between the zero of a two-parameter fit of the evolved Lambda^2 and the closed-form v*.

## Mutations (declared fired sets; computed in the development runs dev_11_mut_<name> before declaration)

| mutation | what | fires | effect at c = -1.5, beta = -0.05, h = 0.00125 |
|---|---|---|---|
| beta_sign | data from -beta, truth +beta | O, V | sup abs err r 0.435, ratios 1.000; no v* (a = 1, b = +0.05) |
| kh | the 1/lam^2 - 1 coefficient 1 -> 1.01 | D1, D1b, D2, D3, D4, O, V | sup abs err r 1.2e-2, ratios 1.00; v* error +6.5e-3 |
| kf | the 2 rho lam'/lam coefficient 2 -> 2.02 | D1, D1b, D2, D3, D4, O, V | sup abs err r 4.7e-2, ratios 1.00; v* error +1.1e-2 |
| rate | K -> 1.001 K inside lam^2 only | D1, D1b, D3, D4 | O and V and D2 stay pass (ratios 4.00): this family solves the three evolution equations but not the constraints, so the code evolves it faithfully |
| gauge_frozen | right ray's e^{-f} = F(v0, rho(v)) (the static rule) | D4, O, V | sup abs err r 0.176, ratios 1.00; v* error +3.5e-2 |
| th_coef, vterm_sign, vterm_coef, Vp_sign, V_sign_f | `evolve.py`'s own kernel mutations | D2, O, V | sup abs err r 37, 4.6, 0.35, 1.2, 0.26 respectively; no ratio near 4 |
| eps_sign | the kernel run with eps = +1 | D2, O, V | sup abs err r 7.8, no ratio near 4 |
| vfit_K | the v* finder's rate x 1.01 | PL2, V | v* error -3.0e-3 (c = -1.5) and -4.9e-3 (c = -1); O passes |

The `rate` row is a result of the development: the evolution test O cannot see a wrong rate in lam(v) when the rest of F is consistent, because the three evolution equations hold for every lam(v)
(exact_mode.md Sec. 2: the rate enters only through (vv), a constraint-type equation). D1 (against exact_mode), D3 and D4 see it.

## Development findings that shaped the declaration

- dev_01 to dev_04: second-order convergence at the four cases at first try (ratios 3.99 to 4.00 over h = 0.02 to 0.0025).
- dev_05: approach to v*. Chosen rectangle ends where lam^2 is 0.08 to 0.11 (see above). v* from the fit is found to 3e-5 (c = -1.5) and 1.4e-4 (c = -1) at h = 0.02, error ratios 4.0.
- dev_06: the x- extent (4 to 16) and the expanding sign at the chosen x+ extents: ratios 3.98 to 4.00.
- dev_07 to dev_10: D4 as first designed (both rays, five h, ratio band 4.0 +- 0.3) FAILED (dev_08): sup |C++| along the right ray at beta < 0 (c = -1.5) falls by 2.57, 3.10, 3.48, 3.72 (the last nodes sit near v*, where the higher
  derivatives are large; the asymptotic ratio is reached late), and sup |C--| along the left ray stops falling at fine h (ratios 3.25, 2.18 at c = -1.5, beta = +0.05; dev_09: its relative residual rises as h falls, 5.0e-6 to 8.7e-5 at c = -1.5, beta = +0.05 and 8.5e-5 to 2.6e-2 at c = -1, beta = -0.05, which is
  consistent with roundoff in second differences of exponentially small derivatives, about 1e-16/h^2; I did not separate it further). The check was redesigned
  before declaration: the right ray only, relative to its largest term, with the bars above. D6 first used N = 150, beyond v* at c = -1.5, beta < 0 (the flow stops; dev_08 keeps the traceback).
- The beta > 0 mutated cases of `gauge_frozen` with the first form of that mutation (e^{-f} = F(v, rho(v))) produced negative F (nan logs); the mutation was changed to F(v0, rho(v)).

## Commands (from `notes/black_universe`, `~/Source/negative-mass/.venv/bin/python`, `NUMBA_NUM_THREADS=1`, `nice -n 10`)

```
planted_family.py check [--mutate=NAME] --out=DIR            # about 50 s; exit 1 when a check fails
planted_family.py mutations DIR check_                        # fired sets of DIR/check_<name>.log against the declared ones
planted_family.py case --c=-1.5 --beta=-0.05 --h=0.005       # one run, JSON
```

## Runs of record (added after the runs; the criteria above are unchanged)

Script commits: 4ee1c6b (the runs of record: `runs/check_none.*`, `runs/check_<mutation>.*`, `runs/mutations.log`, `runs/results_*.json`), c883a16 (adds the reported `rays` diagnostic, `runs/rays.log`), 5f2b81c (note and output).
`runs/final_check_none.log` is `check` of the final script: identical to `check_none.log` apart from the date line and the timings. `runs/assemble.sh` writes `planted_family_output.txt` from these logs.

| id | verdict | numbers |
|---|---|---|
| D1, D1b | met | 2.2e-15, 6.5e-15 |
| D2 | met | 2.0e-14 (r+-), 2.5e-15 (f+-), 1.6e-15 (phi+-); numba `_F` 2.0e-14 |
| D3 | met | 8.2e-14 |
| D4 | met | 3.5e-6, 6.1e-5, 5.3e-7, 1.4e-5 at h = 0.00125; falls by at least 3.10 |
| D5, D6, PL1, PL2 | met | 5.1e-12; bit-identical and 0; as stated; as stated |
| O | met | 16 of 16 ratios in 3.977 to 4.003; sup error of r at h = 0.00125: 7.4e-8, 1.7e-6, 2.1e-6, 6.9e-7 |
| V | met | v* errors -3.6e-5 ... -1.4e-7 (c = -1.5), +2.0e-4 ... +7.9e-7 (c = -1) |
| S | met | beta_sign fires O and V |
| mutations | 12 of 12 | fired sets equal the declared ones (`runs/mutations.log`) |

Exit codes: `check` rc 0 (47 s); the twelve mutated runs rc 1; `mutations` rc 0; `rays` rc 0. Two lanes, nice 10, one thread each. No criterion was loosened or moved after the declaration.
