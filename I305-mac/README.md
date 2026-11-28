# I305-mac: the frozen refit of family G's settled-mass relation tested blind on a route chosen for its leverage, outside the fitted data (D = 4, δ = 1e-8)

Machine: the coordinator's Mac (Apple M5, macOS, shared and heavily loaded), Python 3.14.7, numpy 2.5.4, scipy 1.18.1, numba 0.68.1, one thread per process (`NUMBA_NUM_THREADS=1`), `nice -n 10`, at most 2 processes.
Runner negative-mass-mac-i305 on the claude-me2 account. Issue https://github.com/nmoinvaz/negative-mass/issues/305 ("Test the frozen settled-mass refit on a route outside its fitted data, blind").
Worktree `~/Source/negative-mass-i305`, branch `wip/i305-outside-route` from main (ef3e81e). Code: `notes/wormhole_evolution/settled_mass_route4.py` (to be written; a driver over #295's `settled_mass_route3.py`, which imports
#283's `settled_mass_route.py`, #266's `settled_mass_b.py`, #267's `settled_mass_member.py` and everything below them unchanged). Status words as in AGENTS.md: every mass and every member parameter here is *numerical evidence*.

This file is written in stages. **Stage 1 (this commit, before any run of #305, development included): the frozen refit restated, the fitted design, what was known before the rule, the choice rule and the candidates.**
Stage 2 (the route chosen by the rule, the criteria, the planted cases, the mutations with their computed effects) is appended before the runs of record. Nothing in stage 1 is edited after it is committed.

## Stage 1: the frozen refit (#295's; not refitted here)

M_pred = r_th (M₀ + a γ₁ + b γ₁² + c ṙ_th) at h = 0.005, M₀ = 0.223086, **(a, b, c) = (0.2296318924, 0.2834170383, 0.7657657062)** (#295's stage 1, raw `I295-mac` 305e5fee, over the fifteen members of routes B, δ, W, C).
`settled_mass_route3.py refit` run today in this worktree (main ef3e81e) prints the same text as `I295-mac/refit_frozen.log` (`diff` of the two outputs without their first line: empty). The coefficients are not refitted after any run of this issue; the analysis recomputes them
from the stored fifteen points and compares (the check FRZ of #295).
Errors of the refit on its fifteen (frozen in #295): in-sample up to 5.51e-5 (e12), leave-one-out up to 7.90e-5 (e12; W3 7.53e-5), the bar 6e-5. **A held-out point is expected to miss by about the leave-one-out size, and a point with leverage above the fitted maximum by more.**

## Stage 1: the fitted design and the leverage

The design of the frozen fit is A = (γ₁, γ₁², ṙ_th) over the fifteen points at h = 0.005; the **leverage** of a point with row a is L = aᵀ(AᵀA)⁻¹a (for a fitted point this is the diagonal of the hat matrix). From `dev/devselect.0.log` (the script `scripts/devselect.py`, exit 0):

| quantity | value |
|---|---|
| largest leverage of the fifteen | 0.3932 (W3) |
| mean leverage (3 parameters / 15 points) | 0.2000 |
| γ₁ range of the fifteen | 0.00294 to 0.07545 |
| ṙ_th range of the fifteen | −6.6526e-4 to +1.5945e-3 (the issue's [−6.7e-4, +1.6e-3]) |
| condition number of the design | 101.77 |

Leverage of the fifteen: B0.025 0.005, B0.05 0.055, B0.1 0.114, B0.125 0.385, e7 0.259, e9 0.135, e10 0.199, e11 0.268, e12 0.303, W1 0.080, W2 0.268, W3 0.393, C1 0.064, C2 0.160, C3 0.313.
The new members of the third route (N1, N2, N3 of #295) have leverage 0.070, 0.189, 0.328: inside the fitted maximum, so #295's test was an interpolation.

## Stage 1: what was known before the rule below was written (stated so that the rule is read as what it is)

1. The issue's example (x_c, w) = (2.5, 0.35), whose h = 0.02 members have ṙ_th = −2.4e-4, +2.9e-4, +1.9e-3 (from #295's `dev/logs/tune_xc2.5_w0.35_h0.02.log`).
2. Before writing the rule I read the TUNED lines of #295's eight stored h = 0.02 tunings and computed their leverage in the fitted design (`dev/devselect.0.log`). Stored candidates, leverage at γ₁ = 0.012, 0.048, 0.075:
   (2.5, 0.35) 0.052, 0.114, 0.452; (3.5, 0.35) 0.056, 0.118, 0.358; (4.0, 0.35) 0.060, 0.136, 0.344; (4.0, 0.7) 0.075, 0.236, 0.367; (3.5, 1.0) 0.092, 0.358, 0.490; (4.5, 0.7) 0.086, 0.342, 0.514; (2.5, 0.7) has no stall at 0.048 and 0.075.
   Leverage grows toward wide, late pulses (ṙ_th at the high γ₁ falls below the fitted points') and toward narrow, early ones (ṙ_th at the high γ₁ rises above them): two directions out of the cloud.
3. **A draft of the rule** with a separation guard of D ≥ 1.0 (copied from #295) excluded the issue's own example (2.5, 0.35) (D = 0.60 against family B at γ₁ = 0.012). The issue says to choose for leverage rather than for separation, so the guard was relaxed to D ≥ 0.1
   before this README was written (SEP at the runs of record needs D of about 0.003). The draft's table is kept as `dev/devselect.0.draft.log`; no run of #305 had been made. On the stored candidates alone the rule below selects (4.5, 0.7) (S 0.942), with (3.5, 1.0) (S 0.941) and (2.5, 0.35) (S 0.618)
   also counting; **the scan of new candidates can change that.**
4. The nine new candidates below were chosen to extend the two directions of item 2. They are fixed here, before any new run.

## Stage 1: the choice rule (fixed before the development scan; the scan is at h = 0.02)

**Tuning.** For a candidate Gaussian normal pulse (x_c, w) (family G with its ghost pulse unchanged, as #283's `route_family`, the pulse kind `phi`), B is tuned to within 1 % of γ₁ = 0.012, 0.048 and 0.075 at h = 0.02 by #295's secant iteration in (ln B, ln γ₁)
(`scripts/devtune.py`, a copy of #295's with this folder's paths: at most 6 runs per target; a point counts only if it stalls, T gains ≥ 2.0 per side from 1e-6 to 1e-8, and has a member). The member's (γ₁, r_th, ṙ_th) are read at h = 0.02.

**Candidates.**
- *Stored* (the TUNED lines of `I295-mac/dev/logs/tune_*_h0.02.log`, read, not rerun): (2.5, 0.35), (2.5, 0.7), (3.5, 0.35), (3.5, 1.0), (4.0, 0.35), (4.0, 0.7), (4.5, 0.7). (3.5, 0.75) is #295's route N, a reference curve below, not a candidate.
- *New* (tuned here, `scripts/dev_scan.sh 0` and `1`, two lanes): wide and late (4.0, 1.0), (4.5, 1.0), (5.0, 0.7), (5.0, 1.0), (4.0, 1.5); narrow and early (2.0, 0.35), (2.5, 0.25), (3.0, 0.25), (2.0, 0.25).
- At most these sixteen are used. Another pulse kind (`dphi`, in `dn.py`) would need a new spec and tag in the driver; it is used only if no Gaussian candidate counts (then a new rule is written before it is run).

**A candidate counts only if**
- (a) all three targets stall and have a member;
- (b) D ≥ 0.1, where D is the smallest over the three γ₁ and the four reference curves (family B, route W, route C, #295's route N; each at h = 0.02, anchored at B = 0's member, interpolated in γ₁ by a piecewise-linear and a PCHIP curve, the smaller difference) of
  sqrt((Δr_th/1e-3)² + (Δṙ_th/1e-4)²). This is a guard against a route that coincides with an earlier one, not a selection by separation;
- (c) at least one of the three ṙ_th is outside [−6.7e-4, +1.6e-3];
- (d) the largest leverage of its three points is at least 0.43 (10 % above the fitted maximum 0.393; the margin covers the change from h = 0.02 to 0.005 and the tuning's 1 % in γ₁).

**Selected:** the counting candidate with the largest S = L₁ + L₂ + L₃, the leverage of its three points at h = 0.02 in the frozen design (γ₁ and ṙ_th only: r_th and M are not used, and **the frozen refit is not evaluated on any development point**).
Candidates whose S is within 0.01 of the largest are ordered by their largest single leverage. `scripts/devselect.py DEV_LOGS` prints every candidate and the selection (`dev/devselect.1.log`).
If no candidate counts, I stop and report to the coordinator instead of relaxing (b), (c) or (d).

## Stage 1: the procedure after the selection (stages 2 and 3 follow below, before the runs of record)

1. Development set at h = 0.01 and 0.005 for the three tuned points, bracket scan inside `devpoint.py`, plus #295's N3 at h = 0.005 from its stored bracket (the reproduction point); analysis of the development set; mutations computed on it.
2. Stage 2 (route, criteria, planted cases, mutations with their computed effects) is written after the development set and before the runs of record; the runs of record take the development set's brackets and are expected to equal it bit for bit.
3. Stop condition: a single run not finished in 2 h of wall time is stopped and reported. A check that fails on the runs of record is reported as not met; nothing in the criteria is changed after the first run of record.
4. Post hoc blocks (refits with the new points, the second roundoff realization, #283's description of P3's residual) are written into the driver before the analysis of the development set, so the runs of record do not force a rerun of the mutations (#295's mistake).

## Stage 1b: the development scan and the selection (h = 0.02; `dev/logs/tune_*`, `dev/devselect.1.log`; the rule of stage 1 applied unchanged)

Nine new candidates tuned (`scripts/dev_scan.sh 0` and `1`, two lanes, 3 to 7 runs each, 11 to 15 s per run, all exit 0, started 00:40 and finished 00:48 on 2026-11-28). (2.0, 0.35) and (2.0, 0.25) have no stall at any target (rejected by (a)).
Leverage at γ₁ = 0.012, 0.048, 0.075 (S = their sum), ṙ_th and D (smallest distance from B, W, C, N; guard only) of every candidate that has members at all three targets:

| (x_c, w) | source | B at the three γ₁ | ṙ_th (×1e-4) | leverage | S | D | counts |
|---|---|---|---|---|---|---|---|
| (4.0, 1.5) | new | 0.09112, 0.1695, 0.2044 | −11.3, −27.3, −24.4 | 0.272, 1.977, 3.061 | **5.310** | 6.38 | yes |
| (5.0, 1.0) | new | 0.05128, 0.09842, 0.1202 | −8.8, −20.3, −15.6 | 0.173, 1.189, 1.854 | 3.216 | 4.48 | yes |
| (4.5, 1.0) | new | 0.05628, 0.108, 0.1319 | −7.5, −15.5, −8.4 | 0.134, 0.774, 1.131 | 2.039 | 3.14 | yes |
| (5.0, 0.7) | new | 0.0394, 0.0768, 0.09431 | −6.2, −11.8, −4.1 | 0.103, 0.521, 0.773 | 1.397 | 2.33 | yes |
| (4.0, 1.0) | new | 0.06225, 0.1196, 0.1463 | −6.5, −11.8, −2.6 | 0.109, 0.518, 0.714 | 1.341 | 2.17 | yes |
| (4.5, 0.7) | stored | 0.04333, 0.08449, 0.1045 | −5.4, −8.5, +1.9 | 0.086, 0.342, 0.514 | 0.942 | 1.56 | yes |
| (3.5, 1.0) | stored | 0.06962, 0.1342, 0.1646 | −5.7, −8.8, +2.0 | 0.092, 0.358, 0.490 | 0.941 | 1.06 | yes |
| (2.5, 0.25) | new | 0.0407, 0.08452, 0.1105 | −2.3, +3.3, +19.8 | 0.051, 0.117, 0.497 | 0.665 | 0.91 | yes |
| (2.5, 0.35) | stored | 0.04845, 0.1002, 0.1301 | −2.4, +2.9, +18.8 | 0.052, 0.114, 0.452 | 0.618 | 0.60 | yes |
| (3.0, 0.25) | new | 0.03498, 0.06964, 0.08746 | −2.6, +2.1, +17.9 | 0.053, 0.112, 0.426 | 0.591 | 1.26 | no, (d): max L 0.426 < 0.43 |
| (4.0, 0.7), (4.0, 0.35), (3.5, 0.35) | stored | | | max L 0.367, 0.344, 0.358 | | | no, (c) and (d) |

**Selected: (x_c, w) = (4.0, 1.5), S = 5.310**, B = 0.09112, 0.1695, 0.2044 (γ₁ at h = 0.02: 0.011999, 0.047546, 0.074911; r_th 0.99370, 0.98380, 0.98397; ṙ_th −1.131e-3, −2.734e-3, −2.441e-3).
**What this means, written before the development set:** the rule picked the most extreme candidate scanned. Its leverage at γ₁ = 0.075 is 7.8 times the fitted maximum and its ṙ_th at γ₁ = 0.048 and 0.075 is about four times the fitted
minimum (−6.65e-4), so this is an extrapolation of the frozen fit far beyond the edge of its data, not a step outside it. A miss of the bar 6e-5 is expected here and is not a ground to move the bar. The issue's own example (2.5, 0.35) counts (S 0.618, max L 0.452) and
was not selected. A graded test of how the error grows with leverage (the routes (4.0, 1.0), (4.5, 1.0), (4.0, 1.5) have leverage up to 0.71, 1.13, 3.06 at h = 0.02) is a recommended task, not part of this issue.

## Stage 2a: the development set's P4 and FITQ, the coordinator's ruling, and where the note will place a miss (declared before the runs of record)

**Seen on the development set** (`dev/set_a`, `dev/ana_dev1.log`, h = 0.005, before any criterion of stage 2 was written): M − P4 = +9.0e-05, +2.1e-04, +2.0e-04 at X1, X2, X3 (bar 6e-5), so P4 fails on this route as it stands;
the member's static-fit rms (FITQ, #283's bar 1e-4) is 6.5e-5, 1.46e-4, 2.09e-4, so FITQ fails at X2 and X3. `scripts/fitq_diag.py` (`dev/fitq_diag.1.log`): over 22 stored members at h = 0.005 the rms correlates with |ṙ_th| at +0.95
(with |r_th − 1| at +0.80, with |γ₁| at +0.55), and the fitted point B0.125 (ṙ_th = +1.59e-3) is at 1.07e-4, above the bar too; the rms of X2 falls with t from 1.5e-4 at t_dep = 13.6 to 1.1e-4 at t = 15 (and is 4.6e-3 at t = 10).
The planted cases (PMEM, PTD: exact static members with the speeds of this route) recover γ₁, r_th, ṙ_th to 5e-10, 2e-5 and 1.4e-6, so the extraction code is not what fires FITQ: the state at departure is not an exact static member.
FITQ is a gating check of #283's, kept at its bar; it fires on real data and its bar is not moved.

**The coordinator's ruling (hc, 2026-11-28, after the heads-up on these numbers):** continue with the declared route (4.0, 1.5); switching to a milder route after the development residuals would choose the test by its outcome. Report P4 as it falls with FITQ beside it;
say which of two the miss belongs to as far as the data allow, without deciding it post hoc: (form) the three-term form does not hold outside its fitted data, (reading) the member's (γ₁, r_th) of a state that a static member describes poorly are not what the form assumes.
In the recommended tasks, propose a route with leverage between 0.4 and 1.0 chosen by a rule declared before any run.

**Readings that bear on the placement** (post hoc blocks of the analysis of record; they gate nothing; stored runs only, no new run), and the verdict map, fixed here:
- **M1 (the confound).** rms of the static fit against |ṙ_th|, |r_th − 1|, |γ₁| over the stored members (21 plus the new three) and its Pearson correlation. A correlation of at least 0.9 with |ṙ_th| says: in these data a poor member fit and a large throat speed are one coordinate, so the new route cannot by itself tell the form from the reading.
- **M2 (common mechanism).** The ratio |M − P4| / rms at the six held-out members (#295's N1 to N3 and the new X1 to X3), geometric mean g_N over N and g_X over X. If g_X/g_N is within [1/3, 3] a common mechanism proportional to the misfit is consistent; if g_X/g_N is above 10 or below 0.1 the misfit alone does not carry the miss. (Known from the development set: N's ratios are 0.03 to 0.09 and X's 0.95 to 1.4, so this reading is **not blind**.)
- **M3 (the reading's own ambiguity against the shift that would close the miss).** For each new member the shift of one reading that would bring P4 to M, δ*_q = (M − P4) / (∂P4/∂q) for q = γ₁ (∂ = r_th (a + 2 b γ₁)), r_th (∂ = M₀ + a γ₁ + b γ₁² + c ṙ_th) and ṙ_th (∂ = r_th c);
  and the ambiguity A_q = |q(ε = 1e-2) − q(ε = 1e-3)| of that reading in the same stored run (the definition of departure, #266's `eps_alt`; ṙ_th at its own t_dep). R_q = A_q / |δ*_q|. A point is *reading-compatible* if the largest R_q is at least 1, *form-side* if all three R_q are below 1/3, otherwise in between.
  (The ε = 1e-2 readings of X1 to X3 are not computed before this section is committed.) Caveat, stated now: the coefficients were fitted on ε = 1e-3 readings, so a definitional shift that is the same on every route is absorbed by them; A_q measures how loosely the reading is defined, not an error, which is why M3 alone does not decide.
- **Verdict map.** *Reading*: M2 consistent and all three new points reading-compatible. *Form*: M2 apart and all three new points form-side. Anything else: *not separable by these data*, and the note names the measurement that would separate them (a route at leverage 0.4 to 1.0 whose speed is within the fitted range, and the refit at another departure definition, #296's third task).
  Whatever the verdict, a reading error larger than M3 measures is not excluded by the data, and the note says so.
The verdict logic is also run on planted inputs (PBEL) before the real ones.

## Stage 2b: the route, the criteria, the planted cases and the mutations (written after the development set and its mutations, before any run of record)

Code at negative-mass `fdc8111` (`settled_mass_route4.py`, branch `wip/i305-outside-route`; `scripts/` here). Development runs in `dev/`: scan `dev/logs/tune_*`, set `dev/set_a`, analysis `dev/ana_dev3.log` (final; `ana_dev1.log`, `ana_dev2.log` are earlier drafts of it), mutations `dev/mut_a/`.

### The route (selected by the stage 1 rule, stage 1b)

Family G, ghost pulse unchanged, normal pulse a Gaussian of centre x_c = 4.0 and width w = 1.5, B tuned at h = 0.02 to within 1 % of the targets:

| point | target γ₁ | B | γ₁ (h = 0.02) | r_th | ṙ_th | leverage (h = 0.02) |
|---|---|---|---|---|---|---|
| X1 | 0.012 | 0.09112 | 0.011999 | 0.99370 | −1.131e-03 | 0.272 |
| X2 | 0.048 | 0.1695 | 0.047546 | 0.98380 | −2.734e-03 | 1.977 |
| X3 | 0.075 | 0.2044 | 0.074911 | 0.98397 | −2.441e-03 | 3.061 |

### What the development set at h = 0.01 and 0.005 found (`dev/set_a`, `dev/ana_dev3.log`; the runs of record take its brackets and are expected to equal it bit for bit)

Seven jobs (the three points at both h, 26 to 91 s each; and #295's N3 at h = 0.005, 87 s), all exit 0. 31 checks, 30 gating, 2 gating fail (P4, FITQ), 1 post hoc fails (P4-ph). **These results are seen before the criteria below; they do not change a criterion.**

| point | γ₁ (h = 0.005) | r_th | ṙ_th | leverage | M | M − P4 | static-fit rms | M − P3 (#267's) | M − P2' |
|---|---|---|---|---|---|---|---|---|---|
| X1 | 0.011999 | 0.993694 | −1.130e-03 | 0.2717 | 0.223687 | **+9.00e-05** | 6.46e-05 | +1.07e-04 | −6.72e-04 |
| X2 | 0.047545 | 0.983798 | −2.733e-03 | 1.9752 | 0.228997 | **+2.13e-04** | **1.46e-04** | +2.68e-04 | −1.97e-03 |
| X3 | 0.074911 | 0.983968 | −2.439e-03 | 3.0575 | 0.236361 | **+1.98e-04** | **2.09e-04** | +2.74e-04 | −2.45e-03 |

- **P4 fails** (bar 6e-5) at all three, by 1.5, 3.6 and 3.3 times the bar; the same fit without the speed misses by 6.7e-4 to 2.5e-3; #267's P3 also misses (1.1e-4 to 2.7e-4). The misses are positive at all three.
- **FITQ fails** at X2 and X3 (bar 1e-4), see stage 2a for its cause. LEV passes (X2, X3 above 0.3932), OUTR passes (all three ṙ_th below −6.7e-4), SEPB, SEPW, SEPC and SEPN pass (r_th separations 1.3e-3 to 3.5e-2 against h differences of 3e-7 to 1e-6; ṙ_th separations 6e-4 to 4e-3),
  HST passes (γ₁ ≤ 1.1e-5, r_th ≤ 1.0e-6, ṙ_th ≤ 4.9e-7), RH passes (1.0e-5, 1.2e-5, 9.0e-6), TGT passes (γ₁ within 9.5e-3 of its target), REP4 passes bit for bit.
- Post hoc (gate nothing): refits including the new points move (a, b, c) to (0.2292, 0.2993, 0.7130) (18 points) and (0.2290, 0.3018, 0.7133) (21 points) with in-sample errors up to 1.0e-4; #283's description of P3's residual (K = −3.365e-3 × (r_th − B's)) gives +1.6e-5, +6.4e-5, +1.1e-4 against observed +1.1e-4, +2.7e-4, +2.7e-4.

### The issue's acceptance bars, as I read them (mine to be overruled)

| bar | id | reading | gating |
|---|---|---|---|
| at least one new point with leverage above 0.393 in the frozen fit's design | **LEV** | L = aᵀ(AᵀA)⁻¹a at the new members' (γ₁, ṙ_th) at h = 0.005, A the design of the fifteen fitted points; at least one above the fitted maximum computed here (0.3932, W3; the issue's 0.393 is its rounding) | yes |
| ṙ_th outside the fitted range (the task's choice condition) | **OUTR** | at least one new member's ṙ_th at h = 0.005 outside [−6.7e-4, +1.6e-3] | yes |
| every new member within 6e-5 of the frozen fit, or the failure reported with the residuals | **P4** | \|M − M_pred\| ≤ 6e-5 at all three, h = 0.005, M_pred = r_th (M₀ + a γ₁ + b γ₁² + c ṙ_th), the frozen constants. A failure is reported as not met, with the residuals | yes |
| SEP against routes B, W, C and #295's route | **SEPB, SEPW, SEPC, SEPN** | as #295: r_th or ṙ_th at departure differs from the route's curve at the same γ₁ by more than 5 times the point's own h difference, all three points; each curve is B = 0's member plus the route's points, piecewise-linear and PCHIP, the smaller difference; N is #295's three stored points | all three points |
| the member at the two h as in #283 | **HST** | γ₁ and r_th to 1e-4 relative, ṙ_th to 2e-5 absolute, h = 0.01 against 0.005 | yes |
| reproduction of one stored #295 point bit for bit | **REP4** | N3 = (0.136, 3.5, 0.75) at h = 0.005 from #295's stored bracket (0.0064, 0.0128): p*ₕ, the chain's series, the locus, the member rows (all but the wall time), the plateau and (γ₁, r_th, ṙ_th, t_dep) equal #295's stored run exactly | yes |

Other checks, all gating, as #295 (same bars): **CFG, FAM0, RUNS, BR, STL, EVT, RC5, RC4, RC8, RH (5e-5), TGT (3 %), FITQ (rms ≤ 1e-4, #283's)**, and **FRZ** (the refit recomputed from the stored fifteen equals the frozen constants and errors).
**FITQ stays at its bar; it fails on the development set and is expected to fail on the runs of record, and will be reported as not met beside P4.**
Post hoc, gating nothing: P4-ph (h = 0.01), the comparison columns, leverage in the eighteen-point design, refits over 18 and 21 points, #283's description of P3's residual, the static-fit rms at every stored member, the placement block of stage 2a (M1, M2, M3 and its calibration on N, the verdict), `--rn`.
RC4 cannot see the normal field (`normal_drop` fires nothing). `lev_rdot` (ṙ_th set to 0 in the leverage row) fires nothing either: LEV does not depend on the sign or size of ṙ_th at these points (leverage of X2 and X3 stays above 0.3932 without it).

Planted cases (before real data, the same code path): **PMEM, PDEP, PTD, PFIT, PPRED4, PSEP3** (#295's, passing: errors γ₁ 5.8e-7, t_dep 6.3e-6, ṙ_th 1.4e-6, refit 2e-15, planted P4 data pass at 1e-12 and miss by 8.7e-4 with a × 1.05, by 1.9e-4 with c × 0.8);
**PLEV** (the leverage function equals the hat-matrix diagonal at the fitted points to 1.5e-15, the SVD form at random rows to 5.7e-15, is quadratic in the row to 6e-15, and 'above the fitted maximum' is false at 0.9 and 1.0 and true at 1.1 times W3's row);
**PBEL** (the verdict map of stage 2a on six planted inputs: reading, form and four combinations that must come out 'not separable').

### Mutations (each `--mutate=NAME`, 35; the effect computed on the development set before being declared; "newly fires" = fails with the mutation and not without)

The baseline (`dev/ana_dev3.log`) fails FITQ, P4 and P4-ph, so those three cannot newly fire: P4 and FITQ show that they can fail by failing on the data, and PPRED4 shows P4 passing planted data that follow the fit.

| mutation | what it does | newly fires (declared) |
|---|---|---|
| asym_sign | #225's `fit_asym` with the sides swapped | FRZ, PMEM, PTD, SEPC, SEPN, SEPW, TGT |
| bel_swap | the verdict labels reading and form swapped | PBEL |
| bisect_early | the bracket replayed after 30 steps | BR |
| coef_a | a × 1.05 in the predictions | PPRED4 |
| coef_c | c × 0.8 in the predictions | PPRED4 |
| crit_dm | `settled_mass.CRIT["dm"] = 2.0` | CFG |
| dep_eps | ε × 10 in `departure_time` | FRZ, PDEP, PTD |
| drop_point | the refit over 14 points (W3 dropped) | FRZ |
| eps_h | ε × 100 at h = 0.005 only | FRZ, HST, LEV, PLEV, PTD, SEPB, SEPC, SEPN, SEPW |
| evt_side | the pair's expansion-side event in place of the collapse-side one | EVT |
| fitq_scale | the fit rms × 10 | **nothing** (FITQ fails without a mutation) |
| flux_sign | the horizon flux with the wrong sign | RC4 |
| frz_a | the frozen a × (1 + 1e-3) in the comparison with the recomputed refit | FRZ |
| frz_m0 | M₀ = 0.223095 in the refit and the predictions | FRZ, PPRED4 |
| lev_bar | the leverage bar × 10 (a × 1.6 first tried did not fire: the route's leverage reaches 3.06) | LEV |
| lev_design | the leverage computed in the design without the γ₁² column | PLEV |
| lev_rdot | ṙ_th set to 0 in the new members' leverage row | **nothing** (LEV does not depend on it here) |
| loo_off | the leave-one-out errors replaced by the in-sample ones | FRZ |
| mass_exponent | M = r^n/2 (chain rerun) | RC4, REP4 |
| no_rscale | the prediction without the r_th factor | PPRED4 |
| no_run | X1's h = 0.005 member output treated as missing | HST, LEV, RH, RUNS, SEPB, SEPC, SEPN, SEPW, TGT |
| no_settle | the series truncated 3.0 before its end | RC5, RC8, REP4 |
| normal_drop | the normal field dropped from the flux (#283's blind spot: it is 1e-8 of the flux) | **nothing** (blind spot) |
| outr_range | the ṙ_th range widened to [−1e-2, +1e-2] | OUTR |
| rdot_nolapse | τ = t in the speed | FRZ, PTD |
| rep_off | the reproduction compared with the stored N2 | REP4 |
| rh_swap | the plateau at h = 0.005 of the next point | RH |
| sep_k | the factor 5 → 0.005 in the separation test | PSEP3 |
| sep_self | the four reference curves replaced by the new member's own values | SEPB, SEPC, SEPN, SEPW |
| short_limit | K = 12 (chain rerun) | RC5, RC8, REP4 |
| spec_w | the declared w × 1.1 | CFG |
| stl_flat | the lifetimes at 1e-6 and 1e-8 taken equal | STL |
| tgt_scale | the targets × 1.1 | TGT |
| w_scale | the normal pulse's width × 1.1 in `set_route` (the chain is rerun from the stored p*ₕ) | FAM0, HST, LEV, OUTR, REP4, RH, RUNS, SEPB, SEPC, SEPN, SEPW, TGT |
| xc_offset | the normal pulse's centre + 0.1 (chain rerun) | FAM0, HST, LEV, OUTR, REP4, RH, RUNS, SEPB, SEPC, SEPN, SEPW, TGT |

### Changes made after the development set and before this section (the bars of the issue and the frozen constants were not touched)

1. The placement readings of stage 2a (M1, M2, M3, PBEL) were added to the driver after the development set showed P4 and FITQ failing, at the coordinator's request; the stage 2a commit (811e32ab) precedes the first computation of M3 on this route. M2's ratios were known from the development set.
   The **M3 calibration on #295's held-out members** was added after the development run showed R_q of order 0.1 to 7 on the new members: on N the same R_q are 3 to 514, so R_q ≥ 1 is satisfied almost everywhere and M3 alone cannot place a miss. It is not part of the verdict map.
2. `lev_bar`'s factor 1.6 → 10 (it did not fire); two mutations (`lev_rdot`, `normal_drop`) are declared to fire nothing; `fitq_scale` fires nothing because FITQ already fails.
3. The leverage guard of the selection rule was relaxed from D ≥ 1.0 to D ≥ 0.1 before this folder's README was written (stage 1, item 3).

### Run procedure (the runs of record)

`scripts/make_jobs.py dev/set_a jobs_rec.txt jobs_rep.txt` (6 lines "B XC W H LO HI" for the three points at both h, brackets from the development set's `points.jsonl`; 1 line for N3 from #295's stored bracket); `scripts/run_jobs.sh RAW/runs jobs_rec.txt LANE 2` and `scripts/run_jobs.sh RAW/runs_rep jobs_rep.txt 0 1`
(two lanes, nice 10, `NUMBA_NUM_THREADS=1`, `scripts/run_one.sh`: pstar, chain, member; logs never overwritten, reruns numbered); `python settled_mass_route4.py analyze --raw=RAW [--rn=RAW/runs_rn]`; `scripts/run_muts.sh RAW RAW/mut LANE 2 RAW/analyze_record.log`.
Stop condition: a single run not finished in 2 h of wall time is stopped and reported (development: 26 to 91 s). A check that fails on the runs of record is reported as not met. Nothing above is changed after the first run of record.
