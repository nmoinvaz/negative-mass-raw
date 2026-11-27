# I39-dh610: step 1 of #39, the design of a double-null evolution through a wormhole throat (derivation, kernel timings)

Machine: dh610-fedora (Fedora 45, Linux 7.3.3, Intel i7-12700, 20 threads, 62 GB), shared with choptuik-large-d (load average
9 to 18 of 20 during these runs). All runs below are single-thread, `nice -n 10`, started from the terminal because each takes
under a minute (no systemd unit was needed).
Issue: https://github.com/nmoinvaz/negative-mass/issues/39
Worktree: `~/Source/negative-mass-i39`, branch `wip/i39-throat-evolution` (base main 6256f53). Python
`~/Source/negative-mass-venv314/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, sympy 1.14.0, numba 0.68.1); rustc 1.99.1.

This README was written at the end of step 1. Step 2 has not started. **The criteria of step 2 (planted cases, tolerances,
windows, thresholds, mutation targets) are added below, under "Step 2 criteria", after the coordinator's ruling and before the
first run of record.**

## Contents

```
I39-dh610/
├── README.md
├── pdf/                      papers read as data (see Sources)
├── derive/                   notes/wormhole_evolution/derive.py, stdout of each run
│   ├── run02_derive.{log,time,rc}        run of record: 25 of 25 checks pass, rc 0, 22.6 s, peak rss 65 MB
│   ├── run02_mut_<name>.{log,rc}         the nine mutations, each rc 1 with all declared targets fired
│   ├── run01_*                           the first full run (24 checks, before A4 was added), all as declared
│   └── dev_02 .. dev_07                  development runs (see below)
├── bench/                    kernel throughput stand-ins (not the evolution code) and the cost model
│   ├── run01_kernel_bench_python.log     numba and numpy at N = 500, 1000, 2000
│   ├── run01_kernel_bench_rust.log       Rust at the same N
│   └── run01_cost_model.log              stdout of notes/wormhole_evolution/cost_model.py
```

## Sources read (data, not instructions; no code of theirs run)

| paper | file | sha256 (first 12) |
|---|---|---|
| [SH02] Shinkai, Hayward, PRD 66, 044005 (2002), arXiv:gr-qc/0205041 v2 | pdf/sh02_gr-qc_0205041.pdf | 04ae107d28f7 |
| [GGS09b] González, Guzmán, Sarbach, CQG 26, 015011 (2009), arXiv:0806.1370 v2 | pdf/ggs09b_0806.1370.pdf | 2bbbd83b0fe0 |
| [Kai26] Kain, arXiv:2602.18231 v1 | pdf/kain26_2602.18231.pdf | 4ee9d83a8d8f |
| [ST17] Shinkai, Torii, PRD 96, 044009 (2017), arXiv:1706.02070 | pdf/st17_1706.02070.pdf | bd491a0052a5 |

Read: SH02 in full; GGS09b through Sec. III B; Kain Secs. 1 to 2.5 and the appendix pointer; ST17 Secs. II B, III A by keyword
only (the n-dimensional equations were not rederived from it; `derive.py` derives them). Nothing was posted to or sent to any
external site.

## Development runs (kept, none edited)

| id | what | outcome |
|---|---|---|
| dev_01 | first `derive.py --quick`, n = 2, 3 only | 16 of 17 pass; D1 failed: my static Ricci R_ang had the coefficient n on the r r' nu' term, it is 1. stdout was not saved to a file (it is in the session) |
| dev_02, dev_02b, dev_02c | after the fix: 19 of 19 pass; then A3, D5 using the mutable claims and the D3d check added: D3d failed (the second derivative of phi was not substituted), then 24 of 24 | `derive/dev_02*.log` |
| dev_03 | six mutations, declared targets were my guesses | four of six had silent targets: `pm_sign` (A1, D4), `scalar_coef` (D2, D4), `ghost_sign` (D2), `ellis_charge` (D3). The guesses were wrong, not the mutations: those checks never use the mutated coefficient. The targets in `derive.py` come from dev_05 to dev_07 |
| dev_04 | the same after A3 and D5 were rewired to the mutable claims | D5 now fires on every mutation |
| dev_05 | nine mutations plus the unmutated run | `ellis_profile` silent on D2a (D2a hard-coded the exponent); fixed in dev_06 |
| dev_06 | `ellis_profile` | fires D2, D2a, D3, D3b, D3c |
| dev_07 | A4 (stress components) added; all ten variants | 25 of 25 pass; every mutation fires exactly its declared targets |

No tolerance appears in `derive.py`: its checks are exact symbolic zeros.

## What the step 1 runs say

- `derive.py`: 25 of 25 symbolic checks pass, covering the D = 4, 5, 6, 7 Ricci tensors by brute force and the reduced
  equations with n symbolic, constraint propagation, the Misner-Sharp flux law, the Ellis, Tangherlini and Roberts ghost
  solutions. 9 of 9 mutations fire their declared targets.
- Kernel stand-ins, best of three at N = 2000 (4e6 cells, h = 0.001, one thread, load average about 9): numba 61.7 ns per
  cell, Rust 79.6, numpy 192.3. Wall times 0.25 s, 0.32 s, 0.77 s.
- `cost_model.py`: one bisection to |p - p*| = 1e-10 costs 0.2 to 3.6 min in numba and 0.5 to 11 min in numpy over h = 0.01 to
  0.0014 and D = 4 to 6.

## Step 2 criteria

Written after the coordinator's ruling (6b02d78) and after the development runs `dev/dev_s2_01` to `dev_s2_17`, and **before the first
run of record**. The code is `notes/wormhole_evolution/{dn.py,checks.py}` on `wip/i39-throat-evolution` at a00d354 (committed before any run of record); the
numbers below are the `CRIT` and `MUTATIONS` tables of `checks.py` at that commit. Nothing here is
changed after a run of record has been seen. A criterion that is not met is reported as not met.

### What the ruling asked for, and where it is met

| ruling | met by |
|---|---|
| numba kernel for production, numpy kernel as reference; they agree to roundoff on a declared grid | K: three declared grids, tolerance 1e-12 on every field, same dead cells |
| `--kernel=numpy` runs with numba absent | `DN_NO_NUMBA=1 python checks.py --kernel=numpy` (K is then SKIPPED, and reported as skipped, not passed); run of record below |
| P2 Tangherlini with its horizon at r = (2M)^(1/(n-1)); P3 the exact Roberts-form ghost solution; each with a mutation | P2, P3, `MUTATIONS` |
| both throat definitions written, the difference stated | F1 prints the diagonal throat and the minimum-r slice for each pulse |
| excision r_cut = 0.05, F_cut = 25; a sensitivity check with r_cut halved and F_cut doubled; the horizon-formation time within a tolerance declared first | S, tolerance below |
| G1: tune to p*_h, fit the growth, 1 % at D = 4 and D = 5 at two resolutions that agree; the fit window declared after a development run; one untuned departure time as the seed c | G1 and its printed untuned departure |
| static check windowed: second-order deviation for t <= t_c | P1, t_c below |

### Criteria (the CRIT table)

| id | what | criterion |
|---|---|---|
| I1 | constraint solve on the rays returns the Ellis r(l), n = 2, 3, 4, h = 0.02, N = 400 | max error <= 1e-8 |
| K | numba against numpy: Ellis D = 4 with a symmetric pulse (A = 0.05, x_c = 1.5, w = 0.5; h = 0.02, N = 150), Kruskal Tangherlini D = 5 (h = 0.01, N = 60), a collapsing Ellis D = 4 (A = -0.1, same shape, with excision) | max abs difference of every live field <= 1e-12 and identical dead masks |
| P1 | static Ellis, error of (r, f, phi) against the exact static solution over the whole rectangle | D = 4: t_c = 4.0, h = 0.04, 0.02, 0.01; D = 5: t_c = 2.7, h = 0.0283, 0.0141, 0.00707; observed order of each halving in [1.75, 2.25] |
| P2 | Kruskal Tangherlini, r_h = 1, M = 1/2, D = 4, 5, 6, rectangle [0, 0.6]^2, h = 0.005, 0.0025, 0.00125, excision off | orders in [1.75, 2.25] of four errors: max (r, f) against the exact solution; max over interior nodes of M - 1/2; the max deviation of the r_+ = 0 contour (scanned along x-) from x- = -U0 = 0.5; the max deviation of r on that contour from r_h = (2M)^(1/(n-1)) = 1 |
| P3 | Roberts ghost solution, n = 2, a = 3/4, rectangle [1, 3]^2, h = 0.04, 0.02, 0.01 | orders in [1.75, 2.25] of the max (r, f, phi) error, of the r_+ = 0 contour position against x+ = x-/(2a) and of the r_- = 0 contour against x+ = 2a x-; at the finest h the fitted slopes within 1e-3 of 2/3 and 3/2; no more than 3 cells per row of the cell classification (trapped, anti-trapped, neither) differ from the exact r_+, r_- |
| C1 | constraints C_++, C_-- (second-order node differences), D = 4, symmetric ghost pulse A = 0.05, x_c = 1.5, w = 0.5, X = 3 (t <= 4.24), h = 0.04, 0.02, 0.01 | max norm orders in [1.75, 2.25] |
| C2 | M(X, x-) - M(X, 0) against the integral of the flux -(r^n/n) e^f r_+ sum eps phi_-^2 along the edge, same runs | residual orders in [1.75, 2.25], and the M change on the edge > 1e-5 (a pulse really crosses it) |
| G1 | symmetric ghost pulse on the Ellis wormhole (A in phi, x_c = 3, w = 0.5, the pulse on both rays with the parity of phi); bisect A in [-0.01, 0.01] until the bracket is <= 1e-10; run both bracket ends; fit ln\|H\| against tau over the points after the global minimum of \|H\| with \|H\|/W in [1e-3, 1e-2]; W_fit = the mean of the two sides' slopes | D = 4: h = 0.02, 0.01, X = 20; D = 5: h = 0.00707, 0.00354, X = 15. \|W_fit/W - 1\| <= 1 % at each h; \|W_fit(h)/W_fit(h/2) - 1\| <= 0.5 %. W = sqrt(W^2 a^2) of #195: 1.181970 (D = 4), 1.727703 (D = 5). Reported, not gated: A*_h and its ratio between the two h, the untuned (A = 0) departure time of \|H\| = 2e-3 W and the seed constant kappa = 2e-3 W e^(-W tau)/h^2 |
| F1 | one-sided pulses at D = 4, h = 0.02, X = 12, a Gaussian in d phi/dx+ (the form of [SH02] (3.1)): ghost with A = +0.04 and -0.04, normal (second field) with A = +0.04; x_c = 3, w = 1/sqrt3 | qualitative, reported as seen: gated only on a normal pulse collapsing and the two ghost signs ending in a collapse and an expansion. Printed: fate, event time, E0 (M(X,0) minus the unperturbed Ellis M at the same x+), both throat definitions, M at the first trapped cell |
| S | F1's two ghost cases rerun with r_cut = 0.025, F_cut = 50 | same fate; event times within 4 sqrt2 h (four diagonal cells) |

Fixed parameters: ncorr = 1 (predictor + one corrector), excision r_cut = 0.05 a and e^(-f) > F_cut = 25, trapped and anti-trapped tests with
tolerance 1e-2 (r_+ and r_- below -1e-2, or above 1e-2), expansion event: the diagonal cell anti-trapped with r >= 2; collapse event: the
first trapped cell in row order; trapped and expansion events stop a G1 or fate run. t = (x+ + x-)/sqrt2; tau on the diagonal.

### Mutations (the MUTATIONS table; each target list is what fired in development runs dev_s2_16 and dev_s2_17)

| name | what it breaks | must fire |
|---|---|---|
| theta_coef | sphere-term coefficient n - 1 -> n in the kernel | P1 P2 P3 C1 C2 G1 F1 |
| scalar_coef | scalar-equation coefficient n -> n - 1 in the kernel | P1 P3 C1 C2 G1 F1 |
| ghost_sign | sign of the matter source of f in the kernel | P1 P3 C1 C2 G1 F1 |
| no_corrector | the corrector step dropped (predictor only) | P2 P3 C1 C2 |
| numpy_Spert | S multiplied by 1 + 1e-8 in the numpy kernel only | K |
| data_constraint_sign | sign of the constraint in the data solve | I1 P1 C1 C2 G1 F1 |
| ellis_charge | the data's scalar charge q times 1.1 | I1 P1 C1 C2 G1 F1 |
| constraint_sign | sign of the matter term in C_++, C_-- | C1 |
| flux_sign | sign of the flux in the edge identity | C2 |
| mass_exponent | M with r^n instead of r^(n-1) | P2 C2 |
| finder_sign | the sign of the trapped test | P3 G1 F1 S |
| finder_swap | the r_+ contour returned for r_- and the reverse | P2 P3 |
| time_unit | tau times sqrt2 in the G1 fit | G1 |
| cut_extreme | S's variant thresholds r_cut = 1.5, F_cut = 1.5 (above the throat radius) | S |

Silent in development (not predicted, reported): `no_corrector` does not fire P1 (the predictor-only scheme is second order on the static
solution); the kernel mutations do not fire K (they act on both kernels, as designed); no mutation fires I1 except the two data mutations.

### Changes made during development, none after a run of record

- dev_s2_03: exact Tangherlini in Kruskal coordinates replaced the f = 0, linear-r data (Birkhoff), which ran into the singularity within the
  domain for n >= 3. **The design (section 8) said "exterior only" for P2; the ruling asks for the horizon at (2M)^(1/(n-1)), which only the Kruskal
  data contain. P2 as built is the Kruskal one; the exterior-only static tortoise case is not built.**
- dev_s2_07, dev_s2_11: D = 5 at h = 0.0141 has an O(h^2) floor in H (about 1e-3) that hides the growth; the D = 5 pair moved from (0.0141, 0.00707)
  to (0.00707, 0.00354) before any run of record. D = 4 unchanged (0.02, 0.01).
- dev_s2_05b to dev_s2_06: the trapped test needed a tolerance (the static throat is marginally trapped: r_+ = r_- = 0).
- dev_s2_11, dev_s2_14, dev_s2_15: F1's first pulse (a Gaussian in phi) has almost no linear energy overlap with the static flux
  (E0 = +0.0096 A - 4.66 A^2 at h = 0.02), so both signs had E0 < 0 although they ended in different fates. F1 now uses a Gaussian in d phi/dx+
  like [SH02] (3.1). G1 keeps the phi pulse (its threshold is where the linear projection on the unstable mode vanishes, A*_h ~ 5e-5).
- dev_s2_09: P2's finest three h (0.005 .. 0.00125) because M's order approaches 2 from below (1.57 .. 1.77 at h = 0.01 .. 0.0025 for D = 6).
- dev_s2_16, dev_s2_17: `numpy_swapEW` was a no-op (the update is symmetric under E <-> W) and is replaced by `numpy_Spert`; `finder_sign` did not reach
  P3 (P3 had its own classifier) and now does; `cut_extreme` at r_cut = 0.9 was silent (the event comes before the excision), now r_cut = 1.5.
- A defect found in `checks.py`: `check()` kept numpy booleans, so a printed [FAIL] was not counted in the summary or the exit code for K. Fixed
  (coerced to bool) before any run of record; dev_s2_16 and dev_s2_17 summaries and exit codes were affected, their FAIL lines and the target lists
  above were taken from the FAIL lines.

### Runs of record

All by `runs/run01_run.sh`, one thread each, `nice -n 10`, systemd user units `nm-i39-run01-checks`, `nm-i39-run01-numpy`, `nm-i39-run01-mutC`,
`nm-i39-run01-mutD` (four at once), started 2026-11-26 21:25 on dh610-fedora, load average 18 of 20 at the start (shared with choptuik-large-d).
Code `wip/i39-throat-evolution` at a00d354. Logs, `/usr/bin/time -v` files, exit codes and the numbers as JSON are in `runs/`; no run was stopped
and none came near the 2 h stop (the longest, the numpy-kernel run, took 17 min 38 s).

| run | what | result | wall time | peak rss |
|---|---|---|---|---|
| `run01_checks` | all checks, numba kernel | 11 of 11 pass, rc 0 | 4 min 30 s | 270 MB |
| `run01_numpy_checks` | `DN_NO_NUMBA=1 --kernel=numpy` | 10 of 11 pass, K skipped (numba absent), rc 0; the log equals the numba run's apart from timings and K (`diff` of the two logs, all digits) | 17 min 38 s | 2.8 GB |
| `run01_mut_<name>` (14) | one mutation each | each rc 1, and the checks that fired equal the declared list exactly in all 14 | 10 s to 4 min 25 s | 270 MB |
| `run01_probe_expansion` | `notes/wormhole_evolution/probe_expansion.py`, the expansion case on a long rectangle (not a check) | see below | 32 s | |

Numbers of the run of record (from `runs/run01_checks.log`):

| check | numbers |
|---|---|
| I1 | max error 2.9e-9 (n = 2, 3, 4), tolerance 1e-8 |
| K | max difference 0 on all three grids (bit-identical), same dead masks (4536 dead cells on the collapsing grid) |
| P1 | D = 4: errors 1.44e-3, 3.49e-4, 8.86e-5, orders 2.045, 1.978. D = 5: 1.22e-2, 2.92e-3, 7.30e-4, orders 2.059, 2.002 |
| P2 | worst orders: (r, f) 1.972; M 1.767 (D = 6), 1.853 (D = 5), 1.896 (D = 4); horizon position and r on it 1.998 to 2.000; at the finest h = 0.00125: (r, f) errors 3.2e-7, 2.5e-6, 2.2e-5 (D = 4, 5, 6), horizon x- error 2.5e-6, 3.8e-6, 5.0e-6 |
| P3 | (r, f, phi) orders 1.934, 1.969; contour orders 1.98 to 2.00; slopes 0.666668 (2/3) and 1.499991 (3/2); 0 misclassified cells at the three h |
| C1, C2 | orders 1.991, 1.999 and 1.988, 1.995; M changes by 1.18 along the edge |
| G1 D = 4 | A*_h = 4.753e-5 (h = 0.02), 1.188e-5 (0.01), ratio 3.999; W_fit 1.181988, 1.181934 against W = 1.181970 (+1.5e-5, -3.0e-5); the two agree to 4.6e-5 |
| G1 D = 5 | A*_h = 2.885e-4 (h = 0.00707), 7.209e-5 (0.00354), ratio 4.002; W_fit 1.727492, 1.727247 against 1.727703 (-1.2e-4, -2.6e-4); the two agree to 1.4e-4 |
| untuned departure | \|H\| = 2e-3 W at tau = 6.125, 7.306 (D = 4, h = 0.02, 0.01; the shift 1.181 against ln4/W = 1.173); 3.887, 4.689 (D = 5; 0.802 against 0.802). kappa = 2e-3 W e^(-W tau)/h^2 = 0.00424, 0.00420 (D = 4) and 0.0838, 0.0838 (D = 5) |
| F1 (D = 4, h = 0.02) | ghost +A: expands, E0 = -0.0299; ghost -A: collapses at t = 3.73, E0 = +0.0254, M at the first trapped cell 0.4975; normal +A: collapses at t = 6.29, E0 = +0.0022, M 0.4920. E0 < 0 expands and E0 > 0 collapses, as in [SH02]. At the end of the expansion run the diagonal throat has r = 8.516, the minimum-r slice r = 8.177 |
| S | fate unchanged and event time unchanged (difference 0) for both cases; dead cells 172322 -> 171698 in the collapse |

Seed: the unstable mode's seed constant is the same at the two resolutions (kappa 0.00424 and 0.00420 at D = 4; 0.0838 and 0.0838 at D = 5), so
the untuned departure time is (1/W) ln(1/(kappa h^2)) to 0.7 % (D = 4) and 0.0 % (D = 5), and p*_h scales as h^2 with ratio 3.999 and 4.002.

**What disagrees or was not met.** Nothing failed in a run of record. Points to read: the untuned-departure shift at D = 4 (1.181) differs from
ln4/W (1.173) by 0.7 %; M's observed order in P2 is 1.77 to 1.95, inside the declared band but below 2 (higher-order terms still present at
h = 0.005); the sensitivity check S is insensitive on the real cases (zero change) and is shown to fire only under `cut_extreme`.

### Probe: the expanding branch on a long rectangle (not a check)

`probe_expansion_output.txt` (copied to `runs/run01_probe_expansion.log`): the F1 expansion case, one-sided ghost pulse A = +0.04, on [0, 30]^2
(t up to 42.4), D = 4 and D = 5, two h each. No cell is excised, max e^(-f) over live cells is 1.00, the values agree between the two h to 3 to 4 digits.
On the diagonal x+ = x-: r grows about linearly in t (D = 4: 5.0 at t = 12, 13.5 at 24, 25.0 at 40) while its proper time tau saturates (7.43, 8.06, 8.32),
and H = e^(f/2)(r_+ + r_-)/(sqrt2 r) keeps rising (0.75 at t = 8, 1.21, 2.07, 2.88 at t = 40) instead of tending to a constant. Observed, not interpreted:
the diagonal of a one-sided run is not the throat once the data are asymmetric, and its proper time is not the observer's.
