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
