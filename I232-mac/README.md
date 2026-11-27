# I232-mac: linear double-null response of the black universes against #212's master equation (c = -1)

Machine: the coordinator's Mac (Apple M5, macOS), session negative-mass-mac-i232, account claude-me2. Issue: https://github.com/nmoinvaz/negative-mass/issues/232
Code: negative-mass `notes/black_universe/linear_derive.py` (sympy derivation and checks) and `linear.py` (solver, comparators, checks), worktree ~/Source/negative-mass-i232, branch
`wip/i232-c1-linear` on #217's head 45c261d. Python `~/Source/negative-mass/.venv/bin/python`; one thread per process (`NUMBA_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1`), `nice -n 10`, at most two processes.
Status words as in AGENTS.md: rates and ratios are *numerical evidence*; the algebra of `linear_derive.py` is *checked symbolically* (40 digits where numbers appear).

Layout: `dev/` the development logs (`dev_70` derivation, `dev_80` to `dev_93` check, table and mutation runs, `scripts/` the exploratory scripts, whose terminal output was not logged;
the declared checks reproduce their numbers), `runs/` the runs of record (after this README is committed).

## Method in one paragraph

The three evolution equations of #217 with the potential are linearized about the static member (`linear_derive.py`), and the linear system `U_pm = B0 U + Bp U_p + Bm U_m`,
`U = (dr, df, dphi)`, is marched with an implicit second-order cell scheme on a chart `(p, sigma)` that reaches and crosses the future horizon: `p` is #217's advanced tortoise time,
`Q(sigma) = sinh(b (s* - sigma))/sinh(b s*)`, `b = sqrt2 kappa`, `s* = 16`, vanishes linearly at the horizon and is negative inside; the member is analytic in the Kruskal product `Pi = e^{bp} Q`.
It shares with `evolve.py` only the static member and the potential (`evolve_potential.py`). Comparators: #212's master equation in characteristic form (`u = Y/rho` on the same rays),
#217's `evolve_master1d.py`, #217's nonlinear kernel on member +- the same data, and at c = 0 the frequency-domain master equation.

Data (all runs): the corner `rho_c = 1`; on each ray `df = 0`, `dphi` a Gaussian pulse (amplitude 1e-3 unless stated, centre 3, width 0.5, zero at the corner), `dr` from the linearized constraint along the
ray with corner constants. Classes: R pulse on the right ray only; L left only; G both; A0, A1R, A1L corner constants `dr`, `dr_p`, `dr_sigma` = 1e-3 with no pulse. The rate of `Y` is the slope of ln|Y(x = 0, t)|
over a window of t = (p + m)/sqrt2; "Richardson" is (4 r(h/2) - r(h))/3 of the rates at h = 0.01 and 0.005.

## Declared before the runs of record

Each criterion below can fail; the prediction column is from the development runs and is not a criterion. A criterion that fails is reported as not met; nothing is moved after the runs of record.
`linear.py check` prints one [pass]/[FAIL] line per id; `linear_derive.py` prints its own (A0, A1, B1-B3, C1, C2, D1, D2, D3a, D3, E1).

| id | criterion | tolerance | development value |
|---|---|---|---|
| derive A0, A1 | the linearization is a linear form in (dr, df, dphi) and first derivatives; equals the central difference of the nonlinear right-hand sides at 40 digits | 1e-20 | 1.8e-25 |
| derive B1-B3 | `L_xi(member)` solves the linearized evolution equations and both constraints on six members; `Y` vanishes on it | 1e-25, 1e-30 | 5.8e-41, 2.3e-41, 1.2e-41 |
| derive C1, C2 | `M = u_pm + Vhat u/2` on solutions has no `dphi_p`, `dphi_m`; `(d/dt) M = 0` on solutions with the constraints: the master equation holds up to a static term | 1e-25 | 4.6e-41, 9.1e-40 |
| derive D1-D3 | horizon: Raychaudhuri `dr_pp + f_p dr_p = 0`; exponents `+-W/A'` at c = -1.5; exponents `1 -+ W/(2 kappa)` at c = -1 and the logarithm coefficient `pi w (1 - w)/8` (zero at W = kappa) | exact / 1e-8 | pass |
| derive E1 | `V''` of `linear.py` equals the second derivative of V | 1e-30 | 9.2e-41 |
| C1 | `coef()` equals the sympy matrices at 40 random chart points (c = -1.5, -1, -0.3, 0) | 1e-12 | 6.4e-17 |
| C2, C2h | the chart solves the nonlinear equations across the horizon (Richardson finite differences); on the horizon node `r_p = phi_p = 0`, `f_p = -sqrt2 kappa` | 1e-6, 1e-9 | 5.6e-10, 0 |
| C3 | the scheme on exact pure-gauge solutions: error ratios per halving of h in [3.5, 4.5] and the error at h = 0.01 below 3e-4 (c = -1.5, -1, -0.3, 0) | | ratios 4.00; 9.3e-8 ... 2.9e-5 |
| C5 | both constraints along the evolution fall by a factor in [3.3, 4.7] from h = 0.02 to 0.01 and are below 5e-3 of the largest term (c = -1.5, -1) | | 4.00; below 2.7e-5 |
| P1a | planted, c = 0: the linear solver's rate over [10, 14] (Richardson), squared, within 1e-4 of `W^2 a^2 = 1.39705243433350684` | 1e-4 | 8.0e-6 |
| P1b | planted, c = 0: the frequency-domain master equation (even solution shot from the throat to rho = 14) has exactly one root in [0.3, 3] within 1e-8 of the same | 1e-8 | 2.1e-10 |
| P1c | planted, c = 0: #39's kernel on member +- the same data: its odd response's rate over [6, 10] minus the linear solver's, Richardson of h = 0.01, 0.005, moves `W^2 a^2` by less than 1e-4 | 1e-4 | 1.4e-5 |
| R1 | the issue's criterion: the linear rate over [16, 20] (data G, Richardson) equals #212's W within 1e-3 at c = -1.5 and -0.3; the same gate at -1.01 and -0.99 | 1e-3 | 9.2e-5, 2.0e-7, 1.3e-5, 1.1e-5 |
| R3 | c = -1, data G: the rate equals kappa = 2/pi within 1e-3 (it grows) | 1e-3 | 1.2e-5 |
| Q1 | the three #217 slopes quoted in the table occur in `evolve_output.txt` | exact | pass |
| L1 | kernel: #217's nonlinear kernel on member +- eps data (eps = 1e-6; c = -1.5, -1; data G and A0): the odd part of Y equals the linear solver's within 3e-3 from t = 3 until the even part (the untuned member's drift) reaches 5e-4 | 3e-3 | 2.3e-3 |
| L2 | variable: the 1D master equation in characteristic form (`u = Y/rho` on the two rays of the same data) reproduces the double-null `Y(x = 0)` within 2e-3 of its running maximum for data R, L, G at c = -1.5, -1.01, -1 (R at c = -1 to t = 10) | 2e-3 | 8.8e-4 |
| L3a | horizon sector at c = -1: `Y_h(p) = c1 + c2 e^{bp}` for three left pulses: least-squares residual over p in [1, 16] at most 5e-4 at h = 0.005 and falling by 4 (+-0.5) from h = 0.01; late exponent (Richardson) equals b within 1e-5 | | 3.0e-4, ratio 3.99, 7.4e-8 |
| L3b | the combination of the three pulses with `c1 = c2 = 0` (from Y_h at p = 0 and p = 2) has `|Y(x = 0, t = 14)|` smaller by at least 1e3 than one pulse and a rate over [10, 14] below 0.25 kappa | | 2.4e4, -0.177 |
| L3c | control, c = -1.5: the same operation reduces by less than 100 and the rate stays within 15% of W | | 40, 0.4777 |
| L4 | profile near the horizon at the row p = 8, delta = rho - rho_h in [2e-4, 2e-3]: `d ln|Y e^{-W t}| / d ln delta` is 1/2 +- 0.02 at c = -1 (W = kappa; the u -> 0 branch would give 3/2) and `W/A'(rho_h)` +- 0.02 at c = -1.5 | 0.02 | 0.4995, 0.4475 (0.4479) |
| L5 | seeds: at c = -1 with data R (c2 = 0 in the continuum) the linear solver's `Y_h(p = 14)` and the nonlinear kernel's drift of the untuned member at t = 10 both fall by 4 (+-0.3) per halving of h = 0.02, 0.01, 0.005 | 0.3 | 4.00, 4.00; 3.97, 4.01 |

**Verdicts.** "The linear solver grows at kappa at c = -1" is R3 together with L3a. "The disagreement is not in the nonlinear kernel" is L1; "not in the equation or the variable
`u = Y/rho` for pulse data" is L2 together with derive C1, C2; "the data of the nonlinear code carry the horizon sector through truncation error" is L5; "the horizon boundary condition is the cause" is L3, L4 and derive D3:
the growth is carried by `c2` of `Y_h = c1 + c2 e^{bp}`, which the branch `u -> 0` (`Y = O(rho^{3/2})`) of #212 sets to zero. If one of L1 to L5 fails, the corresponding statement is not met and is reported so.

Reported, not gated (`linear.py table`, `linear.py c1`): the comparison table at c = -1.5, -1.01, -1, -0.99, -0.3 (1D time domain, 1D characteristic, linear, #217's slope and untuned-seed rates, nonlinear same-data
difference); at c = -1 the data classes R, L, G, A0, A1R, A1L (rates, horizon exponent, 1D/double-null ratio), the projection, the profile slope.

## Mutations (`linear.py check --mutate=NAME`, exit 1)

Targets computed in the development runs `dev_92` (all) and `dev_93` (`freq_V`, `proj_node` after fixes) before they were written here; `linear.py mutations DIR PREFIX` compares a directory of logs with them.

| name | what it breaks | checks that must fire (and no others) |
|---|---|---|
| V_sign | sign of the V terms of the dr row | C1 C3 C5 R1 R3 L1 L2 L3a L3b L3c L5 |
| Vp_sign | sign of the V' terms | C1 C3 C5 R1 R3 L1 L2 L3a L3b L3c L5 |
| Vpp_zero | the V'' term dropped | C1 C3 C5 R1 R3 L1 L2 L3a L3b L5 |
| eps_sign | kinetic sign eps in the df cross terms and the V', V'' terms of the dphi row | C1 C3 C5 P1a P1c R1 R3 L1 L2 L3a L3b L3c L5 |
| cross_sign | sign of the (r_p/r) dphi_m + (r_m/r) dphi_p terms | C1 C3 C5 P1a P1c R1 R3 L1 L2 L3a L3b L5 |
| df_zero | the df couplings of the three rows dropped | C1 C3 C5 P1a P1c R1 R3 L1 L2 L3a L3b L5 |
| rm_sign | sign of the first-derivative terms of the dr row | C1 C3 C5 P1a P1c R1 R3 L1 L2 L3a L3b L5 |
| bg_b | b of the chart 1% off | C2 C2h C3 C5 R1 R3 L1 L2 L3a L3b L5 |
| mirror | Pi = e^{bp}|Q|, the interior reflected | C2 C3 C5 |
| interior_scale | Pi times 1.5 inside the horizon | C2 C3 C5 |
| con_sign | sign of the f' dr' term of the ray constraint (data violate it) | C5 R1 R3 L2 L3a L4 L5 |
| vhat_sign | the 1D master equation with Vhat -> -Vhat | L2 |
| data_shift | the nonlinear kernel's left ray one node off | L1 |
| seed_h | h_p held at 0.01 while h_sigma halves | L5 |
| proj_node | the horizon values of Y taken one unit of sigma outside the horizon | L3a |
| freq_V | -1/R^2 for -2/R^2 in the frequency-domain equation at c = 0 | P1b |
| quote | a quoted slope with an extra digit | Q1 |
| prof_rate | the profile of L4 divided by e^{1.1 kappa t} | L4 |

`linear_derive.py --mutate=`: `lin_Vpp` (B1 C2), `lin_cross` (A1 B1), `gauge_sign` (B1 B2), `frob_log` (D3), `V2_coef` (E1), computed in `dev_70`-`dev_74` before declaration.

## What changed during development before this declaration

- C5: the first monitor sampled nodes with a fixed stride in nodes, so two resolutions looked at different physical points and the ratio read 2.97; it now samples the same physical nodes (ratio 4.00).
- P1b: the first frequency-domain solve gave `W^2 = 1.39712` (5e-5): the series start omitted the `rho^4` term of Y, whose derivative at rho = 1e-3 mixed in the odd solution; with it, 2.1e-10.
- L2: a ratio test failed where Y crosses zero (c = -1.01, data R); it is now the difference over the running maximum.
- L3a: a fixed 2e-4 residual failed at h = 0.01 (1.2e-3); the residual is O(h^2) (4.7e-3, 1.2e-3, 3.0e-4 at h = 0.02, 0.01, 0.005) as is the exponent's error, so the criterion became the residual at h = 0.005, its ratio and the Richardson exponent.
- L3b: the rate test was two-sided by mistake (a decaying -0.177 failed); it is one-sided.
- C9 (convergence of node values across the horizon) was dropped: it passed under `mirror` and `interior_scale`, so it could not fail; the horizon crossing is checked by C2 and C3 (both fire). L2s (the corner-constant ratio) is a reported number in `c1`, not a check.
- `proj_b` (a wrong exponent in the projection) fired nothing, because cancelling Y_h at two points removes `c2` whatever exponent is used; it is replaced by `proj_node`. `freq_V` and `proj_node` crashed in `dev_92` (empty root list; L4 used the shifted node) and were fixed to fail cleanly (`dev_93`).
- `dev_90` (first sweep, 14 mutations; the lane names A and B ran as unmutated checks) is kept; it lacked C2h targets, which `dev_92` has after C2h was changed to compare with the member's kappa.

## Budget

Development to this point about 4 h; the runs of record (check 2 min, table 1 min, c1 1 min, 18 mutations about 20 min on two lanes, derivation 3 s) well under 1 h. No run lasts more than 3 minutes; the 2 h stop does not bind.
