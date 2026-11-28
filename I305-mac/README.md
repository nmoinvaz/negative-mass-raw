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
