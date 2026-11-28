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
