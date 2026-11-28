# I230-mac-review: the coordinator's review of #230 (the expanding throat's late state in closed form)

Issue https://github.com/nmoinvaz/negative-mass/issues/230; branch `wip/i230-throat-kn` at bab2391, raw `I230-dh610` at 7ea342f0.

## Criteria, written before any run

`ind230.py`, in the coordinator's double-null forms (those of `I217-mac-review/ind217.py`, verified there against a brute-force Ricci
tensor) at n = 2, with V = 0 and the sphere term e^{−f}/2 dropped from r_uv:
- K1: the closed form r² = u + v, φ = A arcsin((u − v)/(u + v)), e^f = C (uv)^{A²} ((u + v)/2)^{1/2 − A²} solves the five equations
  symbolically, for A and C symbolic. Mutations `exp` (the exponent 1/2 → 0.6) and `amp` (φ's amplitude times 1.01) must fail it.
- K2: on the throat u = v, the rate H and the remaining proper time give k = 2/(2A² − 3) at A = 3/2, exactly.
