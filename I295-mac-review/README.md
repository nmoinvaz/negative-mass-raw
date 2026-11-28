# I295-mac-review: the coordinator's review of #295 (a frozen refit of G's settled-mass relation, tested on a third route)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/295. Under review: branch
`wip/i295-third-route` at f9e5998, raw `I295-mac` at a40fb5ff (refit frozen 305e5fee, criteria 6bdd3c69, both before the runs).

## ind295.py: the refit and the prediction with the coordinator's own readings

Written by the coordinator; imports nothing from the repository. It reads every member with ind283's code (copied: t_dep
from the locus, the member by linear interpolation of the stored slices, the plateau over the last 1.0 of x⁺, and ṙ_th by a
quadratic fit of r against τ over ±0.5), at h = 0.005, for the fifteen points (#266's four B, #267's δ = 1e-7, 1e-9 … 1e-12,
#283's six) and #295's three. M₀ = 0.223086.

Criteria, written before the first run:
- K1: its own least-squares fit over the fifteen points gives (a, b, c) within (2e-3, 2e-2, 2e-2) of the frozen (0.22963,
  0.28342, 0.76577).
- K2: with the frozen coefficients and its own readings, every third-route member is within 6e-5 of its settled mass, and
  within 5e-6 of the note's residuals.
- K3: with its own refit, the same three are within 6e-5.
- K4 (reported): the third route's γ₁, r_th and ṙ_th against the convex hull of the fifteen points in (γ₁, r_th, ṙ_th)
  (inside or outside), and each new point's distance to the nearest fitted point.

Mutations: `no-speed` (c = 0 in the prediction: K2), `drop-routes` (the fit without #283's six: K1).

## Results

| check | verdict | reading (`run_01.log`) |
|---|---|---|
| K1 | met | own fit (0.229631, 0.283430, 0.765761) against the frozen (0.2296319, 0.2834170, 0.7657657): differences 7.5e-7, 1.3e-5, 5.0e-6 |
| K2 | met | frozen coefficients, own readings: M − predicted −4.84e-7, −2.14e-6, +1.21e-6 (N1–N3); 7.5e-9 from the note's |
| K3 | met | own refit: max 2.14e-6 |
| K4 | reported | all three new points lie inside the fitted points' bounding box in (γ₁, r_th, ṙ_th), at 0.07, 0.18 and 0.36 of its scale from the nearest fitted point: an interpolation test, as the note says |

Mutations: `no-speed` fails K2 and K3. `drop-routes` fails nothing, and K1's bars were too loose to see it: the nine-point fit
(0.2300, 0.2724, 0.7835) differs from the frozen one by 3.6e-4, 1.1e-2, 1.8e-2, inside (2e-3, 2e-2, 2e-2). That fit also predicts the
three new members within 2.2e-5.

## Rerun of the runner's code

From a detached worktree at f9e5998: the N3 point at h = 0.005 (`job`, `member`, rc 0) gives a chain, locus, member rows and t_dep
bitwise equal to the runner's; `analyze` (rc 0: 26 checks, none failed) equals `settled_mass_route3_output.txt` apart from the header.
