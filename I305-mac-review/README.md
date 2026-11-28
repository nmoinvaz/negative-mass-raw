# I305-mac-review: the coordinator's review of #305 (the frozen refit on a route outside its fitted data)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/305. Under review: branch
`wip/i305-outside-route` at ca6d11a (driver fdc8111), raw `I305-mac` at fd01b448 (rule 94a1cd63, criteria 227ec3bf).

## ind305.py: the miss with the coordinator's own readings

Written by the coordinator; imports nothing from the repository (the reader is ind283's, copied). For the fifteen fitted points
and #305's three (h = 0.005) it reads the member, the plateau and ṙ_th with its own code, and computes:
- K1: M − P4 with #295's frozen (a, b, c) at the three new members, within 5e-6 of the note's +9.00e-5, +2.13e-4, +1.98e-4, and
  each beyond 6e-5;
- K2: the leverage xᵀ(XᵀX)⁻¹x of each new member in the design of the fifteen (x = (γ₁, γ₁², ṙ_th)), within 2 % of the note's
  0.272, 1.975, 3.058, and the largest fitted leverage 0.393;
- K3: ṙ_th of the three within 3e-6 of the note's −1.130e-3, −2.733e-3, −2.439e-3.

Shared: the runs, the stored slices and #225's fit (s_m). Not shared: the reading, the speed estimator, the fit and the leverage.

Mutations: `old-coef` (#267's (0.2300, 0.2724, 0.7835) in place of the frozen fit: K1's match to the note fails), `no-speed`
(c = 0: K1).

## Results

| check | verdict | reading (`run_01.log`) |
|---|---|---|
| K1 | met | M − P4 = +9.00e-5, +2.13e-4, +1.98e-4 (X1–X3), each beyond 6e-5: the frozen refit misses on this route with the coordinator's readings too |
| K2 | met | leverage 0.272, 1.975, 3.058; the fifteen fitted points' largest 0.3932 |
| K3 | met | ṙ_th −1.1304e-3, −2.7327e-3, −2.4394e-3 (a different estimator from the note's) |

Mutations: `old-coef` and `no-speed` fail K1.

## Rerun of the runner's code

From a detached worktree at ca6d11a: the X3 point at h = 0.005 gives a chain, locus, member rows and t_dep bitwise equal to the
runner's; `analyze` (exit 1: P4 and FITQ fail, as declared) equals `settled_mass_route4_output.txt` apart from the header.
