# I227-mac-review: the coordinator's review of #227 (the Ellis threshold bisected in binary128)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/227. Under review: branch
`wip/i227-extended-bisect` (code 3838b4f, note b6e1592), raw `I227-rpi5` at ff87cdfd.

`ind227.py` reads `I227-rpi5/runs` only and imports nothing from the repository. It does its arithmetic in mpmath at 40 digits
(not `np.longdouble`), with its own midpoint, side test, regression and offset statistics. Run from this folder:
`python3 ind227.py OUTPUT [--mutate=side-flip|log10|f64-lo]`, OUTPUT = `extended_bisect_output.txt` of the branch. Exit 1
when a check fails.

## Criteria (written 2026-11-28 before the first run)

- **K1.** For variants E and F, with p*ₕ = (lo + hi)/2 of `runs/{E,F}/bisect.json`: all 70 series points (`series_p_3_20.jsonl`,
  `series_m_3_20.jsonl`) have fate = side and sign(A − p*ₕ) = side.
- **K2.** For E and F, T = c_side + s ln(1/δ) over the series points with fate = side and 1e-20 ≤ δ ≤ 1e-12 (δ = |A − p*ₕ|, one
  intercept per side): s equals the output's LL1 slope (0.845980) to 1e-6, with the same n (34).
- **K3.** The float64 offsets, `pstar` of `runs/f64/f64_bisect_k*.json` minus p*ₕ: mean, rms and max |·| equal the output's A2
  line to half a unit of the printed digit, for E (+8.17e-14, 8.20e-14, 1.08e-13) and F (+1.70e-14, 1.85e-14, 4.33e-14), K = 16.

## Mutations (each must fire the named check)

- `side-flip`: the side test against −side → K1.
- `log10`: log10 in place of ln → K2.
- `f64-lo`: `lo` of each float64 bracket in place of `pstar` → K3.

## Reruns

- `rerun_analyze_mac.txt`: `extended_bisect.py analyze` on the Mac, exit 1, 32 of 37. `np.longdouble` is float64 on macOS
  arm64, so the five checks that need differences below 1e-16 relative fail there: LL3-E, LL3-F (δ down to 1e-20 against
  p* = 4.75e-5), P1-scaleP16, P1-scaleM16 and P2 (shifts of 4.8e-21). It is not a reproduction.
- `rerun_analyze_rpi5.txt`: the same command on rpi5 (aarch64, binary128), exit 0, 37 of 37, equal to the output of record
  line for line.
