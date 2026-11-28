# I322-mac-review: the coordinator's review of #322 (the remainder of smooth c = −1 data)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/322. Under review: branch `wip/i322-remainder`
(code 50e1d53, note dfd2cee), raw `I322-mac` at db712d27.

`ind322.py` checks the closed-form side of the note with its own quadrature (mpmath tanh-sinh, nested), and the printed fits
against it. It imports nothing from the repository and shares with #322 only the definitions of #262 (A, R, K, H, J, I₀ and
Π = ρe^{2H}). Run from this folder: `python3 ind322.py OUTPUT [--mutate=j-sign|rho-is-pi]`, OUTPUT = `remainder_output.txt`
of the branch. Exit 1 when a check fails.

## Criteria (written 2026-11-28 before the first run)

- **K1.** I₀ = ∫₀^∞ 2Kr e^{−2H}/(AR²) dr, with H(ρ) = ∫₀^ρ (K/A − 1/(2r)) dr, equals #262's 1.0149036099284090 to 1e-12 relative.
- **K2.** ρ(Π) from ρe^{2H(ρ)} = Π at Π = −0.1, 0.5, 1, and Q = −J(ρ)/I₀ there, equal the output's closed-form line
  (ρ = −0.3114, 0.6819, 1.0000; Q = +0.296062, −0.573712, −0.732706) to half a unit of the last printed digit.
- **K3.** Every "Q fit" of the growth-coefficient table (11 data with c₂ ≠ 0, three Π) lies within 4.3e-4 + 5e-6 of K2's Q,
  as the note's Answer claims.

## Mutations (each must fire the named check)

- `j-sign`: Q = +J/I₀ → K2, K3.
- `rho-is-pi`: ρ = Π (H dropped in the map) → K2.
