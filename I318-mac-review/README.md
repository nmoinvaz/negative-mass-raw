# I318-mac-review: the coordinator's review of #318 (the second-order part of the departure reading across members)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/318. Under review: branch `wip/i318-second-order`
(note 5db9c17), raw `I318-mac` at 6c0faa41.

Rerun: `rerun_analyze.txt` (`settled_mass_second.py analyze --raw=<raw>/I318-mac`, exit 1, PD2 and P1G fail as stored) equals the
output of record apart from the header and the timing.

`ind318.py` uses the coordinator's reader of `I317-mac-review/ind317.py` (departure at the first t ≥ 6 with |r_b − r_a|/(r_a + r_b)
≥ ε, r_th and γ₁ by linear interpolation of the member rows, ṙ_th from a quadratic in τ over ±0.5). It imports nothing from the
repository and shares with #318 the raw runs only. For each of the seven members it reads the stored δ = 1e-8 pair at ε = 1e-2 and
#318's δ = 1e-9 pair at ε = 1e-3, which reach the same moment, and forms ρ = (reading at 1e-2 − reading at 1e-3) over B = 0's same
difference, for r_th and ṙ_th. Run from this folder: `python3 ind318.py [--mutate=no-b0|same-eps]`. Exit 1 when a check fails.

## Criteria (written 2026-11-28 before the first run)

- **K0.** The two readings of each member are at the same moment: |t_dep(1e-8 pair, ε = 1e-2) − t_dep(1e-9 pair, ε = 1e-3)| ≤ 0.01.
- **K1.** ρ_ṙ at X1, X2, X3, W3, C3, N3, B0.125 is within 0.02 of #318's 1.002, 1.006, 1.009, 1.009, 1.002, 1.005, 1.003, and below
  1.1 at X1–X3 (where 1.19, 1.41, 1.44 would close #317's miss).
- **K2.** ρ_r (this reader interpolates the rows, as #318's reader A) is within 0.02 of #318's A values 0.954, 0.960, 0.891, 0.965,
  0.905, 0.920, 0.920.

## Mutations (each must fire the named check)

- `swap`: ρ_r divided by B = 0's ṙ_th difference instead of its r_th difference → K2.
- `same-eps`: both pairs read at ε = 1e-2 → K0.

## Amendment A0 (2026-11-28, before the first run)

The declared `no-b0` cannot fire: B = 0's reading at ε = 1e-3 is about 1 % of its reading at 1e-2, below K1's and K2's 0.02. It is
replaced by `swap` before any run of `ind318.py`.
