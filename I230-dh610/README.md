# I230-dh610: the scaling solution of the expanding symmetric throat and its exponent k(n) (D = 4, 5, 6)

Machine: dh610-fedora (Fedora 45, Linux 7.3.3, Intel i7-12700, 20 threads, 62 GB), shared with choptuik-large-d (load average 18 of 20 during the
development runs). At most 4 processes, one thread each, `nice -n 10`. Issue: https://github.com/nmoinvaz/negative-mass/issues/230.
Worktree `~/Source/negative-mass-i230`, branch `wip/i230-throat-kn`, base main 3ba8819 (`dn.py`, `checks.py`, `expansion.py` unchanged). Python
`~/Source/negative-mass-venv314/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, numba 0.68.1, sympy 1.14.0, mpmath 1.3.0). The evolution is #213's `expansion.stream`
(#39's `dn.row_step`) called from `notes/wormhole_evolution/throat_scaling.py` at **9b6b1f8**, committed and pushed before this README and before any run of record.

**This README was written after the development runs `dev/dev_01` to `dev/dev_07` listed below and before the first run of record.** Everything under "Declared" is
the `CRIT` and `MUTATIONS` tables of `throat_scaling.py` at 9b6b1f8, in words. Nothing there is changed after a run of record has been seen. A criterion that is not
met is reported as not met. A control that fires on real data stops the work until the cause is known. Status words as in AGENTS.md: every number below is
*numerical evidence* unless marked *proved*, *checked symbolically* or *conditional*. No sentence here says a result is new.

## Contents

```
I230-dh610/
├── README.md
├── scripts/            joblane.sh (one lane of jobs, 3 h limit each), mutlane.sh (the mutation runs)
├── dev/                development runs (kept, none edited): dev_NN_*.py, dev_NN*.log, mut/ (the mutation runs of dev_03, dev_05, dev_06), jt/ (dev_07)
└── runs/               runs of record (after the declaration)
    ├── D<D>_A<A>_h<h>_X<X>.npz              one streamed run of family S: the diagonal series, the edge columns x+ = X/4, X/2, X, the horizon contours
    ├── D4_tuned_h0.01_X800.npz              the tuned D = 4 member at X = 800
    ├── D<D>_S_b<b>_h<h>_X<X>.npz            the jump test: S plus a step b in the end value of the field
    ├── *.partial.npz                         the diagonal series so far (written at each tenth of the rows)
    ├── logs/<lane>_<k>.log                  per job: start, progress, end, exit code
    └── analysis*.log                         `throat_scaling.py analyze` on the above
```

## Rulings received (coordinator's brief, over hc)

1. Find the scaling solution of the mirror-symmetric expanding throat near tau_s from the throat relation and the field equations on the symmetric diagonal, as a closed form
   or a numerical self-similar solution, and k(n). Test its prediction at D = 6 (n = 4) by a new run at h <= 0.003. Run the D = 4 tuned member closer to tau_s at X = 800.
2. Project rules: a failed check is a result, never changed to pass; never loosen a criterion after seeing data; never move a declared limit, member, resolution, window or bar
   after a development run without asking; each check has a `--mutate=` whose targets are computed in a development run before they are declared; k = 2(n - 1) stays a
   *conjecture* until derived; no novelty claim; keep every log, number reruns.
3. Threads and memory: at most 4 processes, `nice -n 10`; any single run not finished in 3 h is stopped and reported; memory is reported only; the X = 800 grid is streamed.
4. Files: `throat_scaling.py`, `throat_scaling_output.txt`, `throat_scaling.md` under `notes/wormhole_evolution/`, and this folder. Close with a comment, remove `running`,
   leave the issue open.

## What the development runs showed before anything was declared (reported, none of it fixed)

1. **A closed-form scaling solution exists** (derived by hand, *checked symbolically* for n = 2 to 6, `throat_scaling.py derive`, residuals identically zero). Drop the sphere
   term e^{-f}/2 of r_{+-} = -(n-1)(r_+ r_- + e^{-f}/2)/r. Then (r^n)_{+-} = 0, and with the mirror symmetry and a reparametrization of x+- the throat's late state has
   r^n = x+ + x- = 2T. The scalar equation becomes the cylindrical wave equation phi_TT + phi_T/T = phi_XX (T = (x+ + x-)/2, X = (x+ - x-)/2). Its odd solution that is
   homogeneous of degree 0 is phi = A arcsin(X/T). The constraints give e^f = const (x+ x-)^{A^2} T^{(n-1)/n - A^2}. On the diagonal this is H = k/(tau_s - tau) with
   **k = 2/(n A^2 - n - 1)** and |rho|/H^2 = **c = n^2 A^2/2**, which satisfy the throat relation c = n(1/k + (n+1)/2) identically. A is a free parameter of the solution.
2. **What fixes A (conditional).** The solution tends to phi = +-(pi/2) A on the two null edges x- -> 0 and x+ -> 0 of the quadrant. *Hypothesis H1*: the field's value on the
   null edge of the anti-trapped region is its value at spatial infinity, so that A = (2/pi) phi_inf. For the Ellis family phi_inf = (pi/2) sqrt(n/(n-1)) (the first integral
   r'^2 = 1 - (a/r)^{2(n-1)}, phi' = Q/r^n, Q = sqrt(n(n-1)) a^{n-1}; checked against `dn.ellis_dense`, dev and CF3). Then A^2 = n/(n-1), **k = 2(n-1)** and
   **c = n^3/(2(n-1))**: (D, k, c) = (4, 2, 4), (5, 4, 27/4), (6, 6, 32/3). The two stored data points agree; the D = 6 value is the prediction. k = 2(n-1) is *conditional*
   on H1 until H1 is derived.
3. **The stored runs approach these values; the plain fit does not reach them at D = 5** (dev_02). The local exponent k_loc = H^2/(dH/dtau) at r = 50a is 2.0001 (D = 4)
   and 3.9880 (D = 5) and tends to 2(n-1); |rho|/H^2 at r = 50a is 4.0000 and 6.7525 against 4 and 6.75. #213's fit (1/H linear in tau over the last e-fold of r) gives
   3.9875 and 3.9897 at D = 5, 3.1e-3 and 2.6e-3 below 4 in relative terms. The throat relation makes this a property of c, not of the fit: 1/k = c/n - (n+1)/2, so
   delta k/k = -n^2 (delta c/c) for c = n^3/(2(n-1)), and a c off by 3.7e-4 moves k by 3.3e-3 at D = 5 (16 times the relative change at D = 6). The approach is a power
   of r: a least-squares k_loc(r) = k_inf - a r^-g over the last e-fold of r gives k_inf = 2.00000 (D = 4, four members), 4.00003 (D = 5, two members), 5.99988 to 6.00002
   (D = 6 pilots), with g = 1.7 to 2.9 and rms 1e-6 to 1e-4. The cause of the exponent g is not derived.
4. **The closed form holds in space, not only on the diagonal** (dev_02b below): on the stored columns x+ = X/4, X/2, X, r^n = P(x+) + P(x-) with P = r_diag^n/2 to 1e-5 (D = 4)
   and 3e-4 (D = 5), and phi = sqrt(n/(n-1)) arcsin((P+ - P-)/(P+ + P-)) to 1e-5 (D = 4) and 1.3e-3 (D = 5), with no fitted parameter, for x- >= 20.
5. **A varies with the data's end value** (dev_04, the strongest test of H1). Adding to the field on each ray (odd mirror) a step b in its end value, with the constraint solved
   for the total, the closed form predicts A = (2/pi)(phi_inf + b). The runs follow it in k and c to 4 digits at D = 4, 5, 6 for k from 0.64 to 12.6 (table below). Negative b
   of -0.1 and -0.2 at D = 4 collapses (trapped cells) and is not part of the test.
6. **D = 6 pilots** (dev_01, h = 0.012, X = 60): A = 0.05, 0.2, 0.01 all give k_loc -> 6 (5.992, 5.998, 5.988 at r = 40 to 50) and c = 10.668, 10.667, 10.669. The fit over the last
   e-fold at X = 60 gives 5.983, 5.994, 5.972 (1.7e-2, 6e-3, 2.8e-2 below 6): at that length the fit window is still in the approach.
7. **`ellis_charge` is silent** (dev_03, dev_05): the data's charge q enters only the constraint solve for r along the rays, not the end value of the field that sets A. The late
   state does not depend on the initial r(s) profile to the bars below.

## Development runs (kept, none edited; `dev/`)

| id | what | outcome |
|---|---|---|
| dev_01 | `dev_01_pilot.py`: D = 6, h = 0.012, X = 60, A = 0.05, 0.2, 0.01 (14 to 18 s each) | k_loc, c and k_fit as item 6; r_end 49.8, 55.4, 48.6; min e^{-f} 2.2e-5, 1.9e-6, 4.1e-5; no dead cell |
| dev_02 | `dev_02_estimators.py`: the fit, the local exponent and the extrapolation on the 7 stored #213 runs and the D = 6 pilots | k_inf over the last e-fold: 2.00000, 2.00000, 1.99999, 2.00000, 2.00001 (D = 4); 4.00003, 4.00003 (D = 5); 5.99988, 5.99999, 6.00002 (D = 6); windows of 1.5 e-folds agree to 6e-5 |
| dev_02b | the spatial test in the scratchpad, then as `throat_scaling.py` SP1, SP2 | as item 4 |
| dev_03 | `mut/dev_03_*.log`: the first mutation sweep (before the jump test was added) | superseded by dev_05; kept |
| dev_04 | `dev_04_jump.py`: the step b in the end value, D = 4 (h = 0.02, X = 100), D = 5 (h = 0.00707, X = 60), D = 6 (h = 0.012, X = 60) | table below; `dev_04_run1.log`, `dev_04_run2.log` |
| dev_05 | `mut/dev_05_*.log`: the mutation sweep at the code before 9b6b1f8 (without the expansion guard) | the declared targets below; four BUILD logs have a less explicit message |
| dev_06 | `mut/dev_06_*.log`: the four BUILD mutations and the unmutated `dev` at 9b6b1f8 | BUILD fires with "the diagonal series does not reach r = 20 ... the run does not expand"; the clean suite passes 15 of 15 |
| dev_07 | `dev_07_jt_eval.py` and `jt/`: the 11 jump-test jobs through `throat_scaling.py job` (joblane `dev07`, `dev07b`), then the declared JTK, JTC, WS, SP1, SP2 and the D = 6 pilots through SP1, SP2 | JTK met (2.2e-4); JTC **not met (1.06e-3, D = 4, b = 0.4)**; WS met (4.8e-4); SP1 4.5e-4, SP2 9.5e-4 over 14 runs; `dev_07_eval.log` |

The jump test in the development runs (A = 0.05 pulse plus the step b; k_inf from the last e-fold; c at 0.8 r_end):

| D | b | A = (2/pi)(phi_inf + b) | k predicted | k_inf measured | c predicted | c measured |
|---|---|---|---|---|---|---|
| 4 | 0.05 | 1.44604 | 1.6919 | 1.6920 (k_loc, end) | 4.1821 | 4.1820 |
| 4 | 0.1 | 1.47788 | 1.4617 | 1.4619 | 4.3682 | 4.3681 |
| 4 | 0.2 | 1.54154 | 1.1411 | 1.1413 | 4.7527 | 4.7524 |
| 4 | 0.4 | 1.66886 | 0.7782 | 0.7784 | 5.5702 | 5.5695 |
| 4 | -0.05 | 1.38238 | 2.4332 | 2.4331 | 3.8220 | 3.8220 |
| 5 | 0.2 | 1.35207 | 1.3475 | 1.3475 | 8.2264 | 8.2288 (r = 46) |
| 5 | 0.5 | 1.54305 | 0.6363 | 0.6364 | 10.7146 | 10.7171 (r = 58) |
| 5 | -0.03 | 1.20565 | 5.5440 | 5.5452 | 6.5411 | 6.5453 (r = 42) |
| 6 | 0.1 | 1.21836 | 2.1330 | 2.1330 | 11.8753 | 11.8754 |
| 6 | 0.3 | 1.34569 | 0.8915 | 0.8915 | 14.4870 | 14.4870 |
| 6 | -0.03 | 1.13560 | 12.6289 | 12.6290 | 10.3167 | 10.3204 (r = 40) |

(The D = 4 column of k measured is k_loc at the last cell in the first development script; the declared check uses the extrapolation k_inf.)

## Declared

### Closed form and Ellis jump (no runs)

| id | check | bar |
|---|---|---|
| CF1 | the closed form (r^n = x+ + x-, phi = A arcsin((x+ - x-)/(x+ + x-)), f as above) solves the flat-limit evolution equations and both constraints, A free (sympy, n = 2 to 6) | residuals identically zero |
| CF2 | on its diagonal k = 2/(nA^2 - n - 1), c = n^2 A^2/2, and the throat relation c = n(1/k + (n+1)/2) holds (sympy, n = 2 to 6) | identically |
| CF3 | `dn.ellis_dense` at l = 4000 with the tail -q/((n-1) l^{n-1}) restored: phi_inf = (pi/2) sqrt(n/(n-1)) and q = sqrt(n(n-1)), n = 2 to 6 | 1e-9, 1e-12 |
| CF4 | A^2 = n/(n-1) gives k = 2(n-1) and c = n^3/(2(n-1)) as exact rationals, n = 2 to 8, equal to the numbers the checks use | exact |

### Planted cases (through the same code as the runs)

| id | case | bar |
|---|---|---|
| PF | synthetic H = k/(tau_s - tau), k = 2, tau_s = 17.8902, 40000 points to tau_s - tau = 0.31, relative noise 1e-4, seeds 1, 2, 3, through #213's fit (last e-fold of r) | k and tau_s within 1e-3 (dev: 5e-5 and 1e-5) |
| PX | synthetic k_loc(r) = k - a r^-g with noise 1e-4 and the deviation at r_end: (n, g, dev, r_end) = (3, 2.0, 4e-3, 84), (2, 2.5, 2e-4, 190), (4, 2.4, 5e-3, 50), seeds 1, 2, 3, through the extrapolation | k_inf within 1e-3 relative (dev: 2e-5) |
| PS | the spatial test on the closed form itself (n = 3, P(x) = (1 + 3x^2)/2, h = 0.01), and with A 2 % high | exact case within the bars of SP1, SP2; the 2 % case outside SP2 (dev: 4e-9, 1e-8; 2.3e-2) |

### On the stored #213 runs (h = 0.01 at D = 4: tuned = p*_h + 1e-6 (A = 1.2884160339832307e-05), 0.01, 0.05, 0.2; h = 0.00354 at D = 5: tuned (A = 7.309088653326034e-05), 0.05)

k_fit is #213's fit (1/H linear in tau over the last e-fold of r); k_inf is the least-squares k_loc(r) = k_inf - a (r/r_end)^-g over the same window (3 parameters, g in [0.05, 12]);
c is |rho|/H^2 at r = 50a (at 0.8 r_end if the run stops short). "Relative" means |value/prediction - 1|.

| id | check | bar | expected from the development runs |
|---|---|---|---|
| K4F | D = 4: k_fit within 1e-3 (relative) of 2, every member | 1e-3 | met (worst 2.0e-4) |
| K4X | D = 4: k_inf within 1e-3 of 2 | 1e-3 | met (worst 4e-6) |
| C4 | D = 4: c within 1e-3 of 4 | 1e-3 | met (worst 3.7e-4) |
| K5F | D = 5: k_fit within 1e-3 of 4 | 1e-3 | **not met (3.1e-3 and 2.6e-3, from #213's table; declared as the issue states it)** |
| K5X | D = 5: k_inf within 1e-3 of 4 | 1e-3 | met (8e-6) |
| C5 | D = 5: c within 1e-3 of 27/4 | 1e-3 | met (3.7e-4) |
| WS | k_inf over the last 1.0 and the last 1.5 e-folds of r differ by at most 1e-3 (relative), every gated run | 1e-3 | met (worst 3e-5) |

The issue's acceptance reads "k and c match #213's stored runs to 1e-3 at D = 4 and 5". K5F is that sentence applied to #213's fitted k. It is declared as met or not met by
the number, and its failure at D = 5 is known from #213's table before the declaration. K5X and C5 are the same sentence applied to the exponent the runs approach and to c.
**Which reading counts for the acceptance table is for the coordinator; both are reported.**

### Spatial test (every gated run; the columns x+ = X/4, X/2, X with x+ >= 30 and x- in [20, x+ - 3h])

| id | check | bar |
|---|---|---|
| SP1 | r^n = P(x+) + P(x-), P(x) = r_diag(x)^n/2 from the run's own diagonal | 1e-3 relative (dev: 3e-4 worst, D = 5) |
| SP2 | phi = A arcsin((P+ - P-)/(P+ + P-)) with A = (2/pi)(phi_inf + b) (b = 0 except in the jump test) | 1e-2 absolute (dev: 1.3e-3 worst, D = 5) |

### The jump test (A = 0.05 pulse plus a step b in the end value of the field on each ray; `dphi` pulse, centre 3, width 0.5, odd mirror)

| D | h | X | b |
|---|---|---|---|
| 4 | 0.02 | 100 | 0.05, 0.1, 0.2, 0.4, -0.05 |
| 5 | 0.00707 | 60 | 0.2, 0.5, -0.03 |
| 6 | 0.012 | 60 | 0.1, 0.3, -0.03 |

| id | check | bar |
|---|---|---|
| JTK | k_inf within 1e-3 (relative) of 2/(nA^2 - n - 1), A = (2/pi)(phi_inf + b), every run | 1e-3 (dev_07: 2.2e-4 worst) |
| JTC | c within 1e-3 of n^2 A^2/2 with the same A, c read at r = 50a (at 0.8 r_end if the run stops short of 62a) | 1e-3 (dev_07: **1.06e-3 at D = 4, b = 0.4, r = 50a: expected not met**; 6.4e-4 at D = 5, b = -0.03; 3.6e-4 at D = 4, b = 0.2) |

dev_07 ran these 11 jobs once, with `throat_scaling.py job` at 9b6b1f8, before this README. At D = 4, b = 0.4 the approach is slower than at b = 0 (A^2 = 2.79, k = 0.78): c is 5.5643
at r = 50a (1.06e-3 below 5.5702) and 5.5691 at r = 117a (2e-4 below). The check is declared as committed (c at r = 50a); it is expected to miss its bar by 6 % of the bar in that
one run. Replacing the read-off by the extrapolated c over the last e-fold (the estimator of K4X, K5X, K6X) was considered and **not done**: it would change a declared
estimator after a development run. It is put to the coordinator below.

### New runs at D = 6 (n = 4; prediction k = 6, c = 32/3 = 10.6667), family S, X = 200 (t = 283)

| member | h | N | role |
|---|---|---|---|
| A = 0.05 | 0.003 | 66667 | gated (K6F, K6X, C6, SP1, SP2, WS) |
| A = 0.2 | 0.003 | 66667 | gated |
| A = 0.01 | 0.003 | 66667 | gated |
| A = 0.05 | 0.006 | 33333 | RES6 partner |

h = 0.003 is #39's resolution at D = 6 (the issue's h <= 0.003). The amplitude does not set the late state at D = 4 (#213), so no tuned member is run at D = 6 (no bisection).

| id | check | bar |
|---|---|---|
| K6F | k_fit (last e-fold of r) within 1e-2 (**absolute**) of 6, the three h = 0.003 runs | 1e-2 (the issue's "within 1e-2", read as absolute, the stricter reading) |
| K6X | k_inf within 1e-2 of 6 | 1e-2 |
| C6 | c within 1e-3 (relative) of 32/3 | 1e-3 |
| RES6 | h = 0.006 against h = 0.003, A = 0.05: H at r = 10, 25, 50 within 1e-2 (relative) and the fitted k within 1e-2 (absolute) | as stated (#213's bar 1e-2) |

### The D = 4 tuned member at X = 800 (N = 80000, h = 0.01, t = 1131; the member of `D4_tuned_h0.01.npz`, A as above)

| id | check | bar |
|---|---|---|
| T800 | tau_s from the fit (last e-fold of r) within 1e-3 of 17.8902 | 1e-3 |
| K800 | k = 2.000 +- 1e-3 | 1e-3 (absolute) |
| KT800 | K (tau_s - tau)^2 at the last cell, K = H^2 + 1/r^2, within 1e-3 (relative) of 4 | 1e-3 |

### Other checks and reports

- BUILD: the reduced suite builds (the diagonal series reaches r = 20 with at least 100 cells) and its diagnostics are finite.
- Reported, not gated: tau_s and the distance of the last cell from it, K (tau_s - tau)^2, k_loc and c/c_pred - 1 at r = 10, 20, 50, 100, the exponent g and the rms of the extrapolation,
  the spatial deviations per column, min e^{-f}, the first dead cell, wall time and memory.

## Mutations (`throat_scaling.py mutate --mutate=NAME`, the reduced suite D = 4, h = 0.02, X = 100: A = 0.05 and the jump test at b = 0.2, plus the planted cases)

Each mutation must fire exactly its declared set (computed in dev_05 and dev_06 before this declaration). Checks that already fail on the stored data (K5F) cannot show sensitivity and are not in the reduced suite.

| mutation | what is broken | fires |
|---|---|---|
| `exp_n` | r = (x+ + x-)^{1/(n-1)} in the closed form and in the spatial test | CF1, CF2, PS, SP1 |
| `f_coef` | (n-1)/n replaced by 1/n in f | CF1, CF2 |
| `c_formula` | c = n^2 A^2/4 | C4, CF2, CF4, JTC |
| `k_formula` | k = 2n | CF4, K4F, K4X |
| `A_scale` | A^2 1 % high | C4, CF3, CF4, JTC, JTK, PS, SP2 |
| `jump_off` | the step b ignored in the prediction | JTC, JTK, SP2 |
| `fit_unit` | tau scaled by sqrt 2 in the fit | K4F, PF |
| `extrap_mean` | the mean of k_loc over the window instead of the extrapolation | PX |
| `scalar_coef`, `theta_coef`, `ghost_sign`, `data_constraint_sign` | dn.py's kernel and data inputs | BUILD (the reduced run collapses, r_end < 0.5) |
| `ellis_charge`, `no_corrector`, `constraint_sign`, `flux_sign`, `mass_exponent`, `finder_sign` | dn.py inputs | nothing: q enters only the constraint solve for r on the rays (the end value of phi sets A); at h = 0.02 the bars are above the predictor's error; the others only change diagnostics this script does not read |

## Runs of record (queue)

| lane | jobs (`throat_scaling.py job ...`) | estimate |
|---|---|---|
| 1 | `--D=4 --A=from:.../I213-dh610/runs/D4_tuned_h0.01.npz --h=0.01 --X=800` | 60 to 90 min |
| 2 | `--D=6 --A=0.05 --h=0.003 --X=200` | 45 to 75 min |
| 3 | `--D=6 --A=0.2 --h=0.003 --X=200` | 45 to 75 min |
| 4 | `--D=6 --A=0.05 --h=0.006 --X=200`; the 11 jump-test jobs; then `--D=6 --A=0.01 --h=0.003 --X=200` | 20 min; 10 min; 45 to 75 min |

Stop condition: a job not finished in 3 h of wall time is stopped (`timeout`, exit 124) and reported, not rerun. Memory is reported only. A lane that fails to start is rerun with a new log number.

## Questions for the coordinator (none blocks the runs of D = 6 and X = 800; the jump-test jobs run too, only their analysis could change)

1. K5F against K5X and C5 (above): which reading is the acceptance at D = 5?
2. H1 is not derived. The report says k = 2(n-1) is *conditional on H1* and supported by SP2, C4 to C6 and the jump test, and does not call it proved.
3. JTC (above): keep the declared read-off (c at r = 50a; expected 1.06e-3 against the bar 1e-3 at D = 4, b = 0.4) and report it not met, or replace it before the analysis
   by the extrapolated c, the same estimator as K4X, K5X, K6X and JTK (not computed in any development run)? The declared form is used unless the coordinator rules otherwise.

## Stage 2: results

(to be written after the runs of record)
