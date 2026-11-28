# I310-mac-review: the coordinator's review of #310 (κ r_S c₁ = −c/π at the 20 black universes)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/310. Under review: branch `wip/i310-c1-all`
(code b54e1f5, note 2e3dffb), raw `I310-rpi5` at dc2c3594.

`ind310.py` is `I301-mac-review/ind301.py` (the coordinator's, closed forms in mpmath and sympy) taken to the 20 members of #212
(`notes/black_universe/README.md` §4, whose ρ_h column seeds the root finder). It imports nothing from the repository. Run from
this folder: `python3 ind310.py [--mutate=no-shift|rs-one]`. Exit 1 when a check fails.

## Criteria (written 2026-11-28 before the first run)

- **K1.** At each of the 20 members, 30 digits: ρ_h from A(ρ_h) = 0 agrees with the README's 6 decimals, and
  κ r_S c₁ = −c/π with κ = A′(ρ_h)/2, r_S = R(ρ_h), c₁ = R_h/2 + R′_h/A′(ρ_h); worst relative error below 1e-25.
- **K2.** The first law dM/dL = κ_ξ (dA/dL)/(8π) along each family r = √L R, F = A + 1/L − 1, at L = 0.7 and 1.3, with
  κ_ξ = √L F′(ρ_h(L))/2 and M = K L^{3/2}/3: worst relative error below 1e-12.
- **K3.** With r_S set to 1, the miss |κc₁/(−c/π) − 1| equals |1 − 1/r_S| to 1e-20 at the 19 members c ≠ −1 and is above 1e-12
  there, and is below 1e-25 at c = −1.

## Mutations (each must fire the named check)

- `no-shift`: c₁ = R_h/2 (the horizon's shift dropped) → K1.
- `rs-one`: r_S := 1 in K1 → K1.
