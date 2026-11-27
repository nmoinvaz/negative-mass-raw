# I217-mac: the evolution of the phantom black universes along their growing mode (#217)

Machine: the coordinator's Mac (Apple M5, macOS, shared), negative-mass-mac-i217, worktree `~/Source/negative-mass-i217`, branch `wip/i217-black-universe-evolution`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/217 ("Evolve a black universe along its growing mode: is it a critical solution?"). Python 3.14.7,
numpy 2.5.4, scipy 1.18.1, sympy 1.14.0, mpmath 1.3.0, numba 0.68.1 (`~/Source/negative-mass/.venv`), `nice -n 10`, one thread per process
(`NUMBA_NUM_THREADS=1`, `VECLIB_MAXIMUM_THREADS=1`), at most two processes, 2 h stop per job (`gtimeout 7200`). Memory is reported, never a stop condition.

Status words as in AGENTS.md. Every slope, A\*ₕ and finder result is *numerical evidence*. No sentence here names the threshold by a type.

**Criteria declared on 2026-11-27, after the development runs `dev_01` to `dev_122` and before the first run of record.** Code: `notes/black_universe/evolve.py` at commit
`9428081` (branch `wip/i217-black-universe-evolution`); design: `evolution_design.md`, with the coordinator's rulings of 2026-11-27. Any change to the code or to a
criterion after this README is an amendment, written at the end of this file with its reason. The design-stage table of development logs is `dev/README_dev.md`.

## What is measured, in words

- **The member** is the static black universe of [BF06] with the potential V(phi) of `evolve_potential.py`, units b = 1, D = 4, phantom (eps = -1), c = -0.3 (throat in the static region,
  rho_h = -0.926754, W = 0.9700800261), c = -1.5 (rho_h = 0.339617, W = 0.4941711675), and the control c = -1 (rho_h = 0, #212: no growing mode). W is #212's, in units 1/b.
- **Time.** On the member, e^{-f} = A in the tortoise null gauge, so t = (x+ + x-)/sqrt2 is the Killing time of the static member. The observer is the diagonal x+ = x-, the static
  observer at the corner's rho_c (the throat at c = -0.3; rho_c = 1 at c = -1.5 and c = -1). T is the t of the diagonal cell, so the comparison of the lifetime slope with #212's W is in t.
- **The lifetime** is the departure of the gauge-invariant Y = dr - (rho R/sqrt2) dphi on the diagonal: the first row whose diagonal cell has |Y| >= Y0; the fate is the sign of Y there.
  It is a **linear-regime measure**: it tests the growth rate in the nonlinear code. It does not by itself show that generic data approach the member. The finders (the raw `dn.cell_class`
  and the e^{f/2}-weighted test: the signs of r+ and r- and 2 e^f r+ r- >= 0.02) name the outcomes in separate naming runs.
- **The family** is the static member + A x delta-hat, where delta-hat is the mode's shape on the two rays in the code's own gauge, taken from the untuned member's truncation-seeded
  departure at |Y| = 2e-4, divided by Y at the corner node, so that A is Y at the corner. A\*ₕ = O(h^2) is a property of any family through the static member.
  The one-sided pulse of #40's family O is the cross-check that the slope does not depend on the family (criterion XC).

## Declared settings

| setting | value | reason |
|---|---|---|
| departure level Y0 | 2e-5 | **3e-3 (the first ruling) is nonlinear at c = -1.5**: the extracted mode is mostly gauge (df about 10 to 20 times Y), the negative branch reaches Y = -3e-3 and turns positive, so the sign at 3e-3 is not the mode's sign. With 3e-3, A\*ₕ at c = -1.5 was -6.64e-06, -3.60e-06, -4.28e-06 (not second order; `dev_43` to `dev_45`) and the series saturated near 3e-6; with 2e-5: -2.854e-06, -7.041e-07, -1.773e-07 (`dev_82`, `dev_86`, `dev_83`). Approved by the coordinator. |
| extraction level | 2e-4, first row after t = 6 | the linear regime after the start-up transient (`dev_80` to `dev_88`) |
| bracket of the bisection | +-1e-4 (mode family); +-2e-4 (family O) | straddles at every member in the development runs |
| bisection | hi - lo <= 1e-14 | as #40 |
| series | A = A\* -/+ 10^-e, e = 5.0 to 11.5 in steps of 0.25, both sides | the lifetime is run below the fit windows (e > 7) and **not fitted there** |
| fit windows, abs(A - A\*) (mode family) | [1e-7, 1e-5] primary; [3e-7, 1e-5], [1e-7, 3e-6], [3e-7, 3e-6], [1e-7, 1e-6]; each joint, collapse side alone, other side alone: 15 fits | the coordinator's ruling; h <= 0.01. Never widened after the fits are seen. |
| fit windows (family O) | [1e-8, 1e-5] primary; [3e-8, 1e-5], [1e-8, 3e-6], [3e-8, 3e-6], [1e-8, 1e-6] | the pulse's lifetime is a finder event, later than the departure (`dev_122_jobs_*`, `O_c*`) |
| fit | T = c_side + s ln(1/abs(A - A\*)), common slope, one constant per side | as #40 |
| h | 0.02 (coarse member, reported), 0.01, 0.005, 0.0025 | h = 0.02 is gated only in E8 |
| X (rectangle side) | 40 (c = -0.3), 50 (c = -1.5, -1) | the latest time sqrt2 X = 57 and 71 exceeds every departure (about 25) and the naming runs |
| extraction rectangle | X + 25 | the rays through the corner must reach X |
| family O | Gaussian pulse in phi, centre 3, width 0.5, on the + ray at c = -0.3 and the - ray at c = -1.5; fate -1 if a weighted trapped cell appears before the end of the grid (its t is T), +1 otherwise | the ray whose collapse side has finder events (`dev_10`) |

## Error bars, three different things (as #40)

- **OLS SE** of the primary fit: statistical, assumes independent residuals.
- **Fit spread**: the envelope of s -/+ 2 SE over the 15 fits (window and side choice, plus noise). "1/W inside the fit spread" is the statement.
- **Resolution difference**: the two finest h, compared as abs(s1 - s2) <= 2 sqrt(SE1^2 + SE2^2).
- The floor at c = -1.5 (abs(A - A\*) about 3e-8, T about 15 to 18.5 in the development runs `dev_61`, `dev_83`, `dev_86`) is **reported as found**: for each job the largest abs(A - A\*) below the
  primary window at which T leaves the window's log law by more than 0.25.

## Criteria (each can fail; the code is `evolve.py`; mutations are in the next table)

| id | criterion, as coded | pass condition | run |
|---|---|---|---|
| E0 | the new kernel with the potential flag off and on at c = 0 (V = 0) equals `dn.evolve`: three grids (static N = 300 h = 0.02; collapse with excision, one-sided ghost pulse A = -0.05, N = 400 h = 0.04; expansion A = +0.05), numba and numpy kernels | max abs difference 0 and equal dead masks, every case | `check` |
| E1 | the kernel's right-hand side equals the equations with V (V and V' of [BF06] written out and differentiated in sympy), 40 random states at c = -0.3, -1.5, -1, 0 | max relative difference <= 1e-13 | `check` |
| E2 | numba against numpy kernel with V on, c = -0.3, -1.5, -1 (one-sided pulse A = 0.02, h = 0.04, N = 250) | max abs <= 1e-12, same dead masks | `check` |
| E3 | the c = 0 member with a one-sided pulse on the rays equals `dn.ellis_rays` (N = 1000, h = 0.02) | r <= 2e-9 (#39's I1), phi <= 1e-12, f = 0 | `check` |
| E4 | static members c = 0, -0.3, -1.5, -1 against the exact member for t <= 8 (X = 10, h = 0.04, 0.02, 0.01) | both observed orders within [1.75, 2.25] | `check` |
| E5 | growth rate of Y on the diagonal from the untuned member's truncation seed over abs(Y) in [1e-4, 1e-3], t >= 4, against #212's W at c = -0.3 and -1.5, h = 0.01 and 0.005 | within 1.5 % at both h, and the error falls from h = 0.01 to 0.005 | `check` |
| E6 | the 1D master equation in the time domain (no double-null code; shares only #212's V-hat), rate of ln abs(u(x = 0)) over t = 45 to 60, c = -2, -1.5, -1.1, -1.01, -1.001; and c = -1 | within 1e-4 of #212's W; c = -1 decays (rate < 0) | `check` |
| E7 | the shape of the code's growing Y(l) (untuned member, h = 0.005, the slice where the diagonal abs(Y) first reaches 1e-3, normalized at l = 1) against #212's Y(rho(l)) (ingoing from the horizon, matched to the decaying solution, through the throat's arc at c = -0.3), c = -1.5, -1.01, -1.1, -0.3, l in [-6, 6] | max difference relative to the maximum <= 0.01 (development: 4.8e-3, 2.7e-3, 2.6e-3, 5.3e-3) | `check` |
| E8 | A\*ₕ converges at second order: log2 of successive ratios of A\*ₕ over h = 0.02, 0.01, 0.005, 0.0025, c = -0.3 and c = -1.5 | all orders within [1.75, 2.25] | `analyze` |
| E9 | the primary lifetime slope equals 1/W (c = -0.3, -1.5), at the two finest h (0.005, 0.0025) | each primary slope within 2 OLS SE of 1/W; 1/W inside each fit spread; the two slopes within 2 sqrt(SE1^2 + SE2^2) | `analyze` |
| XC | family O, collapse side, h = 0.005: its primary slope equals the mode family's | within 5 %, c = -0.3 and c = -1.5. **In the development run at c = -1.5, h = 0.01 it was 44 % below (1.14 against 2.03): the pulse's first trapped cell comes after a long nonlinear delay and saturates at T = 47. Reported as found if it fails again.** | `analyze` |
| E11 | the control c = -1 (next section) | MET if no lifetime law; NOT MET if one is found | `analyze` |
| PL | planted series (slope 1/W, A\* = -7e-7, constants 5.0 and 6.5, Gaussian noise 0.01 plus the row quantization sqrt2 h, h = 0.005; 40 seeds; `threshold.oracle` of #40) through the same `bisect`, `series`, `fit_set` as the evolution | A\* recovered to 2e-14 in 40 of 40; 1/W inside the fit spread in at least 36 of 40; c = -0.3 and -1.5 | `check` |
| PX | the same with slope 1/(sqrt2 W) (the time unit scaled by sqrt2) | rejected by the comparison with 1/W in 40 of 40 | `check` |

## The control, declared before the runs

**#212's expectation for c = -1: no growing mode, so along the family through this member there is no divergent lifetime at A = 0: perturbations decay or stay static.**
E11 is MET if no lifetime law is found, and NOT MET if one is found, where "found" means all of: the primary slope's OLS SE <= 10 % of the slope at the two finest h; the two finest slopes
agree within 2 sqrt(SE1^2 + SE2^2); A\*ₕ is at second order (orders within [1.75, 2.25]). What the development runs show, written here so that nobody reads it as a surprise:
**a lifetime law with slope 1/kappa (1.57080) to 7.7e-4 at h = 0.005, A\*ₕ at second order, constraints at truncation level, the same growth in a horizon-regular gauge (`dev_74`),
and a linear response to a compact pulse that saturates at Y about 7.7e3 A_p (`dev_78`)**, while the independent 1D master equation (E6) decays at c = -1. So the expectation is that E11 is
NOT MET as found; it is a result, not something to fix. The open question is named for the follow-up issue #232: at c = -1, and at late times at every member, the double-null linear
problem and #212's master equation disagree.

## Reported, not gated

- **Floors** of the series per job (above) and the T at e = 11.5 on each side.
- **E8c**: the orders of A\*ₕ at c = -1; the coarse member h = 0.02's slopes and spreads at every member.
- **Naming runs** (`evolve.py name`, h = 0.005, all three members): at abs(A - A\*) = 1e-4, 1e-5, 1e-6 on both sides, to the end of the grid: the departure, the first trapped and the first anti-trapped cell
  (raw and weighted) with t, l, r; r, r+, r-, 2M/r and the Misner-Sharp mass on the diagonal at t = 10, 20, 30, 40, 50, against the member's ADM mass m = -2c/(3 pi) (0.0637, 0.318, 0.212).
  If a side stays without a finder event it is reported so.
- **Diagnostic D1** (`evolve.py resp`, ruling 2 of the diagnosis; c = -1.5, -1.01, -1, -0.99, -0.3; h = 0.01, X = 40, pulse +-1e-6 on the + ray at centre 3, width 0.5; also +-1e-5): the odd part of Y
  per unit A_p to the end of the grid, its ratio at 10 A_p (linearity), the local growth rate of ln abs(Y), whether and where it saturates (rate below 0.05 in magnitude over the last window and within 10 % of the
  late value), sign changes, and the Misner-Sharp mass at the diagonal cell and at the last column's cell, and the odd parts of both per unit A_p, against the member's m and the static member's M, so that a
  static shift to a neighbouring member can be told from a bounded mode. Whether c = -1.01 and c = -1.5, which have #212 modes, saturate in the linear regime is stated plainly in the note.

## Mutations (targets computed in the development runs before they were declared)

`evolve.py check --mutate=NAME`, development runs `dev_111` to `dev_119` (the unmutated check is `dev_111`):

| mutation | what it breaks | checks that must fire |
|---|---|---|
| `th_coef` | the kernel's sphere coefficient n - 1 replaced by n | E0, E1, E4, E5, E7 |
| `vterm_sign` | the sign of V in r+- (the wrong-sign-V mutation of ruling 2) | E1, E4, E5, E7 |
| `vterm_coef` | the coefficient 1/2 of V r e^{-f} replaced by 1 | E1, E4, E5, E7 |
| `Vp_sign` | the sign of the V' term in phi+- | E1, E4, E5, E7 |
| `V_sign_f` | the sign of the V e^{-f} term in f+- | E1, E4, E5, E7 |
| `numpy_pert` | a transcription slip in the numpy kernel only | E0, E2 |
| `time_unit` | T scaled by sqrt2 in the fits | PL, PX in `check`; E9[c = -0.3], E9[c = -1.5] in `analyze` (`dev_120`; E11 fails without it) |
| `pstar_off` | A\* shifted by 3e-8 in the fits | PL in `check`; E8[c = -0.3] in `analyze` (`dev_121`) |

Silent by design: V = 0 at c = 0, so the V mutations do not fire E0. A check that raises under a mutation counts as fired.

## Runs of record

`scripts/run_lane.sh A` and `B` (two processes, nice 10, one thread each), then `scripts/run_post.sh`. Jobs in `runs/` (`c<c>_h<h>` mode family, `O_c<c>_h<h>` family O: `summary.json`, `points.jsonl`,
`.log`, `.err` with `/usr/bin/time -l`), checks, analysis, naming and D1 in `post/`. The note is `notes/black_universe/evolution.md`; `evolve_output.txt` is assembled from `post/`.
Lane A: c = -1.5 at h = 0.02, 0.01, 0.005, 0.0025, then family O at c = -1.5 (h = 0.01, 0.005). Lane B: c = -0.3, then c = -1 (each at the four h), then family O at c = -0.3.
Estimated from the development jobs: about 30 minutes per lane.

## Development history (every log kept; `dev/`)

| logs | what |
|---|---|
| `dev_01` to `dev_06` | `evolve_derive.py` and its five mutations |
| `dev_07` to `dev_11`, `dev_31` | kernel bit-identity at c = 0, static checks, growth rates, pulse scans, timings, c = 0 data |
| `dev_12` to `dev_29` | superseded mode-family runs (extraction from a pulse run, nonlinear at c = -0.3; a fit sign slip; two failed brackets) |
| `dev_30` | the 1D master equation: #212's W to four digits, decay at c = -1 |
| `dev_40` to `dev_53`, `dev_60` | mode family with the 3e-3 departure; near-threshold outcomes; the pulse family's two boundaries; profiles; the tuned amplitude |
| `dev_61` to `dev_68` | departure thresholds 2e-5, 2e-6, 2e-7 |
| `dev_70` to `dev_78` | horizon-regular gauge, constraints, the linear response to a pulse |
| `dev_80` to `dev_88` | the linear-level mode family at three h |
| `dev_101` to `dev_121`, `dev_122_jobs_*` | `evolve.py check` and its mutations (`dev_101` to `dev_109` crashed under mutation in E5 and were rerun as `dev_111` to `dev_119`), the analysis on the h <= 0.02, 0.01, 0.005 development jobs |

## Amendments

**A1, after the first results of D1 (reported diagnostic, not gated; no criterion changed).** Code `evolve.py` at commit `2a00351` (the criteria were declared at `9428081`; the diff adds `resp --tuned` and `bgdep`).
Reason: the D1 response about the untuned member saturates at every member, but the untuned member's own |Y| on the diagonal reaches 0.1 at t = 13.8 (c = -0.3) to 23.4 (c = -1.5), so the response is then
linearized about a background that has left the member; reading it as the member's linear problem would be wrong. Added: **D1b** (`post/D1b/resp_tuned_c*.log`; the background is the mode family at the job's A\*;
c = -1.01 and -0.99 needed jobs of their own, `post/D1b/jobs/`, h = 0.01, X = 50, rho_c = 1) and **bgdep** (`post/D1b/bgdep.log`). No threshold, window or criterion was moved.

**A2, `mut_analysis_pstar_off`.** The analysis run with `pstar_off` raised in E8's order computation (A\* at c = -0.3, h = 0.0025 changed sign under the 3e-8 shift, so log2 of a ratio failed): E8 fired by raising,
as declared in the development run `dev_121` (E8[c = -0.3]); the rest of its output is the table printed before the raise.
