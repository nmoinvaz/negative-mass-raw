# I317-mac-review: the coordinator's review of #317 (the corrected ε = 1e-2 reading, frozen, on #305's route)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/317. Under review: branch
`wip/i317-corrected-blind` (note 04b4715), raw `I317-mac` at a34eab4e (frozen fit 7a8a4e8c).

Reruns: `rerun_analyze.txt` (`settled_mass_blind.py analyze`, exit 1, PX fails as stored) and `rerun_post.txt` (`post`, exit 0)
equal the outputs of record apart from the header and the timing.

`ind317.py` uses the coordinator's own reader (copied from `I296-mac-review/ind296.py`, itself from ind283: departure at the
first t ≥ 6 with |r_b − r_a|/(r_a + r_b) ≥ ε, r_th and γ₁ from the member rows, ṙ_th from a quadratic in τ over ±0.5, M the
plateau over the last 1.0 of x⁺). It imports nothing from the repository and shares with #317 the raw runs only. It applies V3
itself (B = 0's r_th − 1 and ṙ_th at ε = 1e-2 subtracted from every member), refits y = M/r_th − M₀ = aγ₁ + bγ₁² + cṙ_th with
M₀ = 0.223086 over the fourteen (B = 0.025, 0.05, 0.1, 0.125; δ = 1e-7, 1e-9, 1e-10, 1e-11; W1–W3, C1–C3), and predicts X1–X3
and N1–N3. Run from this folder: `python3 ind317.py [--mutate=no-sub|eps-1e-3]`. Exit 1 when a check fails.

## Criteria (written 2026-11-28 before the first run)

- **K1.** The residuals M − predicted at X1, X2, X3 are within 1e-5 of #317's +3.35e-5, +7.32e-5, +7.73e-5, and give the same
  verdict against the bar 6e-5 (X1 inside, X2 and X3 outside).
- **K2.** N1–N3 are inside the bar 6e-5.

## Mutations (each must fire the named check)

- `no-sub`: V3's subtraction dropped → K1.
- `eps-1e-3`: the reading at ε = 1e-3 → K1.
