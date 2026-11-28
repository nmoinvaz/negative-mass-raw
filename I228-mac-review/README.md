# I228-mac-review: independent check of #228 (family G at D = 6, third h; locus; drift)

Machine: the coordinator's Mac (Nathans-MacBook-Air-M5-3). Issue: https://github.com/nmoinvaz/negative-mass/issues/228

`ind228.py` reads `I228-dh610` and `I246-dh610` only and imports nothing from the repository. It shares with #228 the raw files and
nothing else: its own midpoint, order, Richardson, regression (within-side demeaning, not a design matrix) and drift estimator.
Run from this folder: `python3 ind228.py [--mutate=order1|no-sides|t-not-tau]`. Exit 1 when a check fails.

## Criteria (written 2026-11-28 before the first run)

- **K1.** p*ₕ = (lo + hi)/2 of `runs40/D6_G_h{0.005,0.0025,0.00125}/summary.json`; the order log2((p₀ − p₁)/(p₁ − p₂)) lies in
  [1.75, 2.25] and within 0.005 of the note's 2.005; the Richardson p* = p₂ + (p₂ − p₁)/3 lies within 1e-9 of the note's
  1.0567197e-2; and lo, hi at h = 0.00125 equal #246's `runs/pstar_D6_G_k2.json` bit for bit.
- **K2.** The diagonal slope: T = c_side + s ln(1/δ) over the series points with a time, fate equal to side, δ = |A − p*ₕ| in
  [1e-11, 1e-3], one intercept per side. At the three h, within 1e-6 of the note's 0.990046, 0.994756, 0.996251; the two finest
  agree within 0.5 % (RA).
- **K3.** The drift at B = 0.1, h = 0.00125 from `runs/stall_drift/stall_D6_B0.1_h0.00125_d1e-10_side{-1,1}.npz`: the pair's mean
  over common slices of r against τ, ṙ = the slope of a straight line over |τ − τ(t)| ≤ 0.5. At t = 8, 10, 12 within 5e-4 of the
  note's 0.09382, 0.08723, 0.07901 (5e-4 is the note's window part at B = 0.1), and r_th − 1 within 1e-4 of 0.35006, 0.51492,
  0.66809.

## Mutations (each must fire the named check)

- `order1`: Richardson at first order, p* = 2p₂ − p₁ → K1.
- `no-sides`: one intercept for both sides → K2.
- `t-not-tau`: ṙ against t instead of τ → K3.

## Amendment A1 (2026-11-28, after run 1)

Run 1 (`ind228_run1.txt`) failed K1: the fixed-order Richardson p₂ + (p₂ − p₁)/3 = 1.0566586e-2 is 6.1e-7 from the note's
1.0567197e-2. The cause: `threshold.py` (line 571) and the note extrapolate with the observed order q = 2.005,
p* = p₂ + (p₂ − p₁)/(2^q − 1), and the criterion above named order 2. K1 now compares the observed-order value with the bar
unchanged (1e-9), and prints the fixed-order value as a report. The `order1` mutation uses q = 1. Runs from run 2 on use A1.

## Amendment A2 (2026-11-28, after the mutation runs of A1)

`no-sides` passes K2 (`ind228_mut_no-sides.txt`): both sides of the series sit at the same δ = 10^-e, so the side intercept is
orthogonal to ln(1/δ) and one intercept gives the same slope. It cannot fire and is kept as a record. Added `collapse-only`
(the collapse side alone, slope 0.857 by the note) → K2.
