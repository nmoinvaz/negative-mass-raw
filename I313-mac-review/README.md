# I313-mac-review: the coordinator's review of #313 (the frozen refit on a route of leverage 0.4 to 1.0)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/313. Under review: branch
`wip/i313-moderate-route` at 779a6ba (driver 19866b3), raw `I313-mac` at 3c737b93.

## ind313.py: the prediction with the coordinator's own readings

ind305.py with #313's three points (h = 0.005): the member, the plateau and ṙ_th by the coordinator's reader, #295's frozen
(a, b, c), the leverage in the fifteen-point design.

Criteria, written before the first run:
- K1: M − P4 within 5e-6 of the note's +2.9e-5, +5.3e-5, +1.8e-5, each within 6e-5.
- K2: leverage within 2 % of the note's 0.10, 0.52, 0.77.

Mutations: `old-coef` (#267's coefficients: K1), `no-speed` (c = 0: K1).

## Results

Run 1 (`run_01.log`) printed K1 and K2 (both met) and then stopped on a NameError of this script (an edit removed the line that
counts failures); run 2 is the same script with that line restored.

| check | verdict | reading (`run_02.log`) |
|---|---|---|
| K1 | met | M − P4 = +2.87e-5, +5.28e-5, +1.85e-5 (Y1–Y3), each within 6e-5, within 5e-6 of the note's |
| K2 | met | leverage 0.103, 0.521, 0.771; fitted maximum 0.3932 |

Mutations: `old-coef` and `no-speed` fail K1.

## Rerun of the runner's code

From a detached worktree at 779a6ba: the Y3 point at h = 0.005 is bitwise equal to the runner's (chain, locus, member rows, t_dep);
`analyze` (exit 1: FITQ, as declared) equals `settled_mass_route5_output.txt` apart from the header.
