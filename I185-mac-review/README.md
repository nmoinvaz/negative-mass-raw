# I185-mac-review: the coordinator's review of #185 (the conical ODE at η = 0 without a leading-power hypothesis)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/185. Under review: branch
`wip/i185-conical-eta0` (note 5d91e35), raw `I185-mac` at 5e2ead3f.

`ind185.py` is the coordinator's sympy. It shares with #185 only the ODE itself, N of `det_classify.conical_N()`, typed into the
script from that definition. Run from this folder: `python3 ind185.py [--mutate=c33|cfac|p0]`. Exit 1 when a check fails.

## Criteria (written 2026-11-28 before the first run)

- **K1.** With F′ = P/η and F″ = (Q − P)/η² (t = ln η, P = F_t, Q = F_tt), η⁴N is a polynomial in η with no odd powers and degree
  ≤ 4, and its η⁰ part is −2AB with A = F(P − Q) − P² and B = (F² − 1)Q² + 2FP²Q + 2FP³ + 2P⁴, identically.
- **K2.** At η = 0, N = 2F′²(F² − 1)(FF″ + F′²), so F(0) = f ∉ {0, ±1} and F′(0) = g ≠ 0 force F″(0) = −g²/f.
- **K3.** For F = f + c/T, T = −ln η: the leading term of B is (4(f² − 1)c² + 2fc³)T⁻⁶, zero only at c = 2(1 − f²)/f (c ≠ 0), and
  with that c, N₀ is O(T⁻⁷).
- **K4.** For F = f + p₀t (P = p₀ ≠ 0, Q = 0), A = p₀F − p₀² and B = 2p₀³F + 2p₀⁴, so N₀ ≠ 0 for large |t|: F′ ~ p₀/η is not a
  local solution of N₀.

## Mutations (each must fire the named check)

- `c33`: N's F₀³F₂³η² coefficient 2 → 3 (`conical_N(c33=3)`) → K1.
- `cfac`: c = (1 − f²)/f → K3.
- `p0`: P = p₀ with Q = p₀ (wrong second derivative) → K4 is not expected to fire; reported.
