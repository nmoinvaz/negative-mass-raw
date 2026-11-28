# I325-mac-review: the coordinator's review of #325 (the D = 6 throat drift against B from 0.01 to 0.2)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/325. Under review: branch `wip/i325-drift-b6`
(cc39229), raw `I325-dh610` at 30772fa9.

`ind325.py` uses the drift reader of `I228-mac-review/ind228.py` (K3: the pair's mean over common slices, ṙ the slope of a straight
line in τ over ±0.5). It imports nothing from the repository and shares the raw pair files (`stall_drift/*_d1e-10_*.npz` of
I228-dh610 and I325-dh610) only. Run from this folder: `python3 ind325.py [--mutate=t-not-tau|h-coarse]`. Exit 1 when a check fails.

## Criteria (written 2026-11-28 before the first run)

- **K1.** The local exponent α = Δln ṙ(8)/Δln B between neighbouring B of (0.01, 0.014, 0.02, 0.03, 0.04, 0.07, 0.1, 0.15, 0.2), at the
  finest h that both B have (0.00125 to B = 0.1, 0.0025 above), is within 0.01 of #325's 2.250, 2.272, 2.415, 2.617, 2.724, 2.220,
  1.365, 0.757.
- **K2.** ṙ(8) at B = 0.1, 0.15, 0.2 is 0.094, 0.163, 0.203 to 1e-3 (the note's saturation).

## Mutations (each must fire the named check)

- `t-not-tau`: ṙ against t instead of τ → K1.
- `h-coarse`: every B at h = 0.0025 → K1 (the note gives 2.848 at 0.01 → 0.014 there).
