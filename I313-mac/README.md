# I313-mac: the frozen refit of family G's settled-mass relation tested blind on a route of leverage 0.4 to 1.0 (D = 4, δ = 1e-8)

Machine: the coordinator's Mac (Apple M5, macOS, shared and heavily loaded), numba one thread per process (`NUMBA_NUM_THREADS=1`), `nice -n 10`, at most 2 processes; Python `~/Source/negative-mass/.venv/bin/python`.
Runner negative-mass-mac-i313 on the claude-me2 account. Issue https://github.com/nmoinvaz/negative-mass/issues/313 ("Test the frozen settled-mass refit on a route of leverage 0.4 to 1.0").
Worktree `~/Source/negative-mass-i313`, branch `wip/i313-moderate-route` from main (d799aa0). Code: `notes/wormhole_evolution/settled_mass_route5.py` (to be written; a driver over #305's `settled_mass_route4.py`, #295's `settled_mass_route3.py`,
#283's `settled_mass_route.py` and everything below them, all unchanged). Status words as in AGENTS.md: every mass and every member parameter here is *numerical evidence*.

This file is written in stages. **Stage 1 (this commit, before any run of #313, the development scan and the retune included): the frozen refit restated, what was known before the rule, the choice rule, the bars, the planted cases and the post hoc readings.**
Stage 2 (the route chosen by the rule, the mutations with their computed effects) is appended after the development set and before the runs of record. Nothing in stage 1 is edited after it is committed.
Every bar below is written before any member of the new route is run at h = 0.01 or 0.005, so no bar is written after P4 or FITQ has been seen on the new route.

## Stage 1: the frozen refit (#295's; not refitted here)

M_pred = r_th (M₀ + a γ₁ + b γ₁² + c ṙ_th) at h = 0.005, M₀ = 0.223086, **(a, b, c) = (0.2296318924, 0.2834170383, 0.7657657062)** (#295's raw README stage 1, `I295-mac` 305e5fee, over the fifteen members of routes B, δ, W, C).
The driver recomputes the coefficients from the stored fifteen points and compares them with the frozen ones (the check FRZ); they are not refitted after any run of this issue.
Errors of the refit on its fifteen (frozen in #295): in-sample up to 5.51e-5, leave-one-out up to 7.90e-5, the bar 6e-5.
The design of the fit is A = (γ₁, γ₁², ṙ_th) of the fifteen at h = 0.005; the leverage of a point is L = aᵀ(AᵀA)⁻¹a (largest of the fifteen 0.3932, W3; mean 0.2000; γ₁ in [0.00294, 0.07545]; ṙ_th in [−6.65e-4, +1.59e-3]).
#305 (route X, normal pulse width 1.5 at centre 4.0; leverage 0.27, 1.98, 3.06; ṙ_th −1.1e-3 to −2.7e-3): M − P4 = +9.00e-5, +2.13e-4, +1.98e-4 and the static-member fit's rms 6.5e-5, 1.46e-4, 2.09e-4 (bar 1e-4).
#295 (route N, width 0.75 at centre 3.5; leverage 0.07 to 0.33, inside the data): M − P4 = −4.8e-7, −2.2e-6, +1.2e-6. **Between the two the relation has not been tested; this issue tests it.**

## Stage 1: what was known before the rule below was written

1. I read `notes/wormhole_evolution/settled_mass_route4.md` (#305) before this README. Its recommended task 1 lists the stored h = 0.02 candidates with their leverage, and says that the rule as worded **selects (5.0, 0.7)** from the stored table (S 1.397, largest leverage 0.773), whose ṙ_th at γ₁ = 0.048 (−1.2e-3) is outside the fitted range.
2. The rule below is the issue's, word for word. What I added: the candidate set (the sixteen scanned in #295 and #305, fixed here; **no new candidate is tuned**, because a larger set would be a larger choice made by me), the leverage definition (#305's), and the reading of "ties within 0.01".
3. So the selection by the rule is known to me in advance; this README says so rather than presenting the scan as blind. The bars of stage 1 do not depend on which route is selected.

## Stage 1: the choice rule (the issue's; the scan is the stored tuning at h = 0.02, read by `scripts/devselect5.py`)

**Tuning.** A Gaussian normal pulse (x_c, w) (family G, ghost pulse unchanged, as #283's `route_family`) with B tuned to within 1 % of γ₁ = 0.012, 0.048 and 0.075 at h = 0.02 by #295's secant iteration (`devtune.py`; a point counts only if it stalls and has a member).
The tunings are the TUNED lines of `I295-mac/dev/logs/tune_xc*_h0.02*.log` and `I305-mac/dev/logs/tune_xc*_h0.02*.log`, read as stored. (3.5, 0.75) is #295's route N and is a reference, not a candidate.

**A candidate counts only if**
- (a) all three targets stall and have a member;
- (b) every one of its three leverages (at h = 0.02, in the frozen design) is at most 1.0, and the largest is at least 0.43 (10 % above the fitted maximum 0.393, the margin for the change from h = 0.02 to 0.005 and the tuning's 1 % in γ₁).

**Selected:** the counting candidate with the largest S = L₁ + L₂ + L₃; candidates whose S is within 0.01 of the largest are ordered by the smaller largest |ṙ_th| of their three points.
No condition on ṙ_th and no separation guard. D (distance from the reference curves B, W, C, N, X) and the position of ṙ_th against the fitted range are printed for information only. If no candidate counts, I stop and report instead of relaxing (a) or (b).
Leverage uses γ₁ and ṙ_th of the member at h = 0.02 only (r_th and M are not used, and the frozen refit is not evaluated at h = 0.02 or on any development point).

**After the selection.** The three points are retuned at h = 0.02 (`devtune.py`, a reproduction check of the stored B, expected equal; the stored B are used regardless), then run at h = 0.01 and 0.005 (the development set, bracket scan inside `devpoint.py`), plus one stored #305 point at h = 0.005 from its stored bracket (the reproduction point).

## Stage 1: the bars (all written before any new member is run at h = 0.01 or 0.005; mine to be overruled)

Gating checks of the analysis (`settled_mass_route5.py analyze`); a failure is reported as *not met* with its numbers, and no bar is changed after the first run of record.

| id | bar |
|---|---|
| **P4** | \|M − M_pred\| ≤ 6e-5 at all three new members, h = 0.005, M_pred the frozen refit. A failure is reported with each residual beside the member's leverage, ṙ_th and FITQ's rms (the issue's first two acceptance lines) |
| **FITQ** | the rms of the member's static-profile fit of M(r) at the slices within 0.5 of departure is ≤ 1e-4 (#283's bar), reported beside each P4 residual |
| **LEVB** | at h = 0.005, in the frozen design: every new member's leverage ≤ 1.0 and the largest ≥ 0.40 (the issue's 0.4 to 1.0; the fitted maximum is 0.3932) |
| **SEPB, SEPW, SEPC, SEPN, SEPX** | against family B (#266), routes W and C (#283), N (#295) and X (#305): the new members' r_th or ṙ_th at departure differs from the route's curve (B = 0's member plus the route's points, piecewise-linear and PCHIP, the smaller difference) at the same γ₁ by more than 5 times the point's own h difference; all three points |
| **HST** | the member at h = 0.01 and 0.005: γ₁ and r_th to 1e-4 relative, ṙ_th to 2e-5 absolute (#283's) |
| **REP5** | #305's X2 = (B, x_c, w) = (0.1695, 4.0, 1.5) at h = 0.005 from #305's stored bracket reproduces #305's stored run bit for bit: p*ₕ, the chain's series, the locus, the member rows (all but the wall time), the plateau and (γ₁, r_th, ṙ_th, t_dep) |
| inherited, as #305 | CFG, FAM0, RUNS, BR (hi − lo ≤ 1e-14), STL (T gains ≥ 2.0 per side), EVT, RC5, RC4 (first law), RC8, RH (\|plat(0.01) − plat(0.005)\| ≤ 5e-5), TGT (γ₁ within 3 % of its target), FRZ |

REP5 uses X2 (the middle point of #305's route) in place of #305's choice of #295's N3; any stored point serves, X2 is fixed here before its timing is known to me.
Not gating, printed for information: whether each ṙ_th is inside [−6.7e-4, +1.6e-3] (OUTR of #305 is not a bar of this issue, whose rule has no ṙ_th condition).

**Planted cases (before real data, the same code path; all gating):** PMEM, PDEP, PTD, PFIT, PPRED4, PSEP3 (#295's six) and PLEV (#305's), and **PBAND** (new): the LEVB decision on planted leverage triples ((0.1, 0.2, 0.39) false: largest below 0.40; (0.1, 0.2, 0.41) true; (0.2, 0.5, 1.0) true; (0.2, 0.5, 1.01) false; (0.45, 0.2, 0.1) true).
**Mutations:** each check can be broken with `--mutate=NAME`; their effects are computed on the development set and declared in stage 2.

## Stage 1: post hoc readings, declared now so that the runs of record do not change (they gate nothing)

- *Table of the nine held-out members* N1 to N3, X1 to X3, Y1 to Y3 (Y the new route): leverage in the fifteen's design, γ₁, r_th, ṙ_th, M − P4, the static fit's rms, |M − P4|/rms, and the position of ṙ_th against the fitted range.
- *M1 as in #305*: the correlation of the static fit's rms with |ṙ_th|, |r_th − 1| and |γ₁| over the stored members (the 22 of #305 plus the three new).
- *#305's post hoc description* (M − P4 = k ṙ_th with k the mean of X's three (M − P4)/ṙ_th = −0.0796) applied to Y without refitting k: the predicted and the observed miss; it is "better than no correction" if |observed − k ṙ_th| < |observed| at all three. A description of one route tested on another, not a bar.
- *Refits including the new points* (post hoc; descriptions, not tests) over the fifteen and Y, the eighteen of #295 and Y, and all twenty-one with Y.
- *#283's description of P3's residual* (K = −3.365e-3 × (r_th − family B's)) on Y, not refitted.
- *P4-ph*: the frozen constants at h = 0.01 with M₀(0.01) = 0.223095 (as #305).
- *The second roundoff realization* (`--rn`): p*ₕ bisected from another bracket (0.98 and 1.02 p*ₕ), M and M − P4 compared.

## Stage 1: procedure and stop condition

1. Scan: `scripts/devselect5.py` (the rule, the stored tunings) → `dev/devselect.1.log`; retune of the selected route at h = 0.02 (`scripts/dev_retune.sh`).
2. Driver `settled_mass_route5.py` (commands `tag`, `bracket`, `pstar`, `job`, `member`, `planted`, `analyze`; `--mutate=`, `--baseline=`, `--rn=`) written and its planted cases run before any run of the new route.
3. Development set at h = 0.01 and 0.005 (`scripts/dev_set.sh`), its analysis, the mutations on it; then stage 2; then the runs of record from the development set's brackets (expected equal to it bit for bit), the analysis of record, the mutations on the runs of record.
4. A single run not finished in 2 h of wall time is stopped and reported. Logs are never overwritten; reruns are numbered. Processes are stopped only by PID.
