# I295-mac: a frozen refit of family G's settled-mass relation over fifteen points, tested blind on a third route to the member (D = 4, δ = 1e-8)

Machine: the coordinator's Mac (Apple M5, macOS, shared and heavily loaded), Python 3.14.7, numpy 2.5.4, scipy 1.18.1, numba 0.68.1, one thread per process (`NUMBA_NUM_THREADS=1`), `nice -n 10`, at most 2 processes.
Runner negative-mass-mac-i295 on the claude-me2 account. Issue https://github.com/nmoinvaz/negative-mass/issues/295 ("Test a frozen refit of G's settled-mass relation on a third route, blind").
Worktree `~/Source/negative-mass-i295`, branch `wip/i295-third-route` from main (5796a03). Code: `notes/wormhole_evolution/settled_mass_route3.py` (a thin driver over #283's `settled_mass_route.py`,
which imports #266's `settled_mass_b.py` and #267's `settled_mass_member.py` and everything below them unchanged). Status words as in AGENTS.md: every mass and every member parameter here is *numerical evidence*.

This file is written in stages. **Stage 1 (this commit, before any run of the third route, development included): the refit, frozen.** Stages 2 and 3 (the route, the criteria, the planted cases, the mutations) are
appended below it before the runs of record; nothing in stage 1 is edited after it is committed.

## Stage 1: the refit, frozen

**What.** Plain least squares over the fifteen members at h = 0.005, y = M/r_th − M₀ = a γ₁ + b γ₁² + c ṙ_th, M₀ = 0.223086 (the coordinator's ruling; B = 0's plateau is 0.2230862), no intercept, no weights.
M is the plateau mean of M_AH over the last 1.0 of x⁺ (`summary_g`, `plat1`); γ₁, r_th are the member at departure (ε = 1e-3, #266's `member_at`) and ṙ_th = dr_th/dτ there (#267's `speed_at`); all read
from the stored runs with #283's code (`settled_mass_route3.py refit`, log `refit_frozen.log` in this folder, exit 0; the raw repository was at 9f25c3e8, `I266-mac`, `I267-mac`, `I283-mac` last changed at 4df36dd4).
The fifteen points are the four B of #266 (δ = 1e-8), the five δ = 1e-7, 1e-9 … 1e-12 of #267 (B = 0.1; δ = 1e-8 is #266's B = 0.1) and the six of #283 (route W: w = 1.0 at centre 3; route C: centre 4.0 at w = 0.5).

| point | route | γ₁ | r_th | ṙ_th | M | y = M/r_th − M₀ |
|---|---|---|---|---|---|---|
| B0.025 | B | 0.002936 | 0.999446 | −9.6904e-05 | 0.22356345 | +0.00060127 |
| B0.05 | B | 0.011844 | 0.998356 | −3.0256e-04 | 0.22523526 | +0.00252006 |
| B0.1 | B | 0.048316 | 1.002878 | +6.5048e-05 | 0.23554841 | +0.01178634 |
| B0.125 | B | 0.075449 | 1.015883 | +1.5945e-03 | 0.24710048 | +0.02015113 |
| e7 | δ | 0.048511 | 1.003370 | −6.3158e-04 | 0.23519848 | +0.01132250 |
| e9 | δ | 0.048159 | 1.003477 | +5.0940e-04 | 0.23599108 | +0.01208746 |
| e10 | δ | 0.048013 | 1.004787 | +8.0517e-04 | 0.23649657 | +0.01228378 |
| e11 | δ | 0.047870 | 1.006583 | +1.0109e-03 | 0.23705124 | +0.01241501 |
| e12 | δ | 0.047732 | 1.008642 | +1.0957e-03 | 0.23762213 | +0.01250014 |
| W1 | W | 0.012003 | 0.994956 | −5.0483e-04 | 0.22436705 | +0.00241847 |
| W2 | W | 0.047982 | 0.989179 | −6.6526e-04 | 0.23174045 | +0.01118956 |
| W3 | W | 0.075022 | 0.993634 | +4.9885e-04 | 0.24079399 | +0.01925067 |
| C1 | C | 0.011989 | 0.999623 | −3.8877e-04 | 0.22548919 | +0.00248812 |
| C2 | C | 0.048006 | 1.006321 | −2.9163e-04 | 0.23599547 | +0.01142704 |
| C3 | C | 0.074833 | 1.019366 | +9.9490e-04 | 0.24727837 | +0.01949453 |

**The frozen coefficients (P4).** M_pred = r_th (M₀ + a γ₁ + b γ₁² + c ṙ_th), h = 0.005, M₀ = 0.223086:

| a | b | c |
|---|---|---|
| +0.2296318924 | +0.2834170383 | +0.7657657062 |

(#267's post hoc fit over nine points: 0.2300, 0.2724, 0.7835; #283's over ten: 0.2269, 0.3294, 0.7096. Design's singular values 0.190, 3.1e-3, 1.9e-3.) They are not refitted after any run of the third route.

**Errors of the refit, M − predicted (frozen with the coefficients).**

| point | in-sample | leave-one-out |
|---|---|---|
| B0.025 | −1.12e-06 | −1.13e-06 |
| B0.05 | −7.69e-06 | −8.14e-06 |
| B0.1 | −2.01e-05 | −2.27e-05 |
| B0.125 | −8.86e-06 | −1.44e-05 |
| e7 | −5.97e-07 | −8.06e-07 |
| e9 | −1.89e-05 | −2.19e-05 |
| e10 | −1.15e-05 | −1.44e-05 |
| e11 | −1.13e-06 | −1.54e-06 |
| e12 | +5.51e-05 | **+7.90e-05** |
| W1 | +7.99e-06 | +8.69e-06 |
| W2 | +2.79e-05 | +3.81e-05 |
| W3 | +4.57e-05 | **+7.53e-05** |
| C1 | −7.87e-06 | −8.41e-06 |
| C2 | −2.65e-05 | −3.16e-05 |
| C3 | −3.93e-05 | −5.72e-05 |
| max \|·\| | 5.51e-05 | 7.90e-05 |

Leave-one-out in y (`refit_frozen.log`) differs from these by at most 2e-6 (the factor r_th); the closed form e_k/(1 − H_kk) agrees with the explicit leave-one-out to 1.2e-17.
**What the frozen errors say about the test, written before it is run:** the bar of the issue, 6e-5, is exceeded by two of the fifteen leave-one-out errors (e12, W3: the points at the largest |ṙ_th| or γ₁ of their group) and
is 76 % of the largest leave-one-out error. A held-out point is expected to miss by about the leave-one-out size, 1e-6 to 8e-5: a miss of the new member at γ₁ = 0.075 is not surprising, and is not a ground to move the bar.
For context (form without the speed, refit over the same fifteen points, **P2'**: y = 0.2177664539 γ₁ + 0.5888595816 γ₁²): in-sample residual up to 7.7e-04, leave-one-out up to 8.7e-04. P2' gates nothing.

## Stage 1: the route, its selection rule and the development procedure (declared before any run of the third route)

The third route changes both the normal pulse's width and its centre (family G with its ghost pulse unchanged, as #283's `route_family`). The member parameters of each route are
read at h = 0.02 in development; the rule below uses (γ₁, r_th, ṙ_th) only, and **P4 and the frozen errors are not evaluated on any development point** (the coefficients are for h = 0.005, and the development runs are at 0.02).

- **Candidates** (x_c, w): (3.5, 0.75) (the issue's example), (4.0, 0.7), (4.0, 0.35), (3.5, 0.35), (2.5, 0.35), (3.5, 1.0), (2.5, 0.7), (4.5, 0.7). Each differs from family B (3.0, 0.5), route W (3.0, 1.0) and route C (4.0, 0.5) in both its width and its centre
  from at least two of the three. At most these eight are tried; the selection below is applied to those that stall.
- **Tuning**: B per candidate by #283's secant iteration in (ln B, ln γ₁) at h = 0.02 to within 1 % of each of γ₁ = 0.012, 0.048, 0.075 (the targets of the issue; `dev/devtune.py`-style, a copy of #283's with this folder's driver).
- **Stall filter**: a candidate counts only if all three targets stall at h = 0.02 (T gains ≥ 2.0 per side from 1e-6 to 1e-8) and have a member.
- **Rule**: among the candidates that stall at all three targets, the one with the largest D = min over the three γ₁ and over the three reference curves (family B, route W, route C; each at h = 0.02, interpolated in γ₁ to the candidate's γ₁ by a piecewise-linear and by a PCHIP curve, the smaller
  difference) of sqrt((Δr_th/1e-3)² + (Δṙ_th/1e-4)²). The scales 1e-3 and 1e-4 are the separations #283's smallest accepted point had (C1: Δr_th 1.3e-3, Δṙ_th −8.8e-5). Route W and C's h = 0.02 members are #283's `dev/logs/tune_*.log` TUNED lines.
- The runs of record are at h = 0.01 and 0.005 for each of the three tuned points, p*ₕ bisected, chain at p*ₕ − 1e-8, the pair p*ₕ ∓ 1e-8, member and ṙ_th as #283.

*Stages 2 and 3 (criteria, planted cases, mutations with their computed effects, run procedure) follow below, before the runs of record.*
