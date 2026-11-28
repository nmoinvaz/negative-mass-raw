# I282-mac-review: the coordinator's review of #282 (Ω₆ and the ln 2 factor at ε⁷)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/282. Under review: branch `wip/i282-omega6` at
1929962 (`order8.py` a017a05), raw `I282-rpi5` at 37a7bac3.

## ind282.py: f₇ from the printed Ω against the identified closed form

Written by the coordinator; imports nothing from the repository. W²a² = s·2^{−4/s}·F(1/s), s = 2(D − 3), ε = 1/s, and
W²a²/s = 1 + Ω₀ε + Ω₁ε² + …, so F = (1 + Σ Ω_{k−1}ε^k)·2^{4ε} and f_n = Σ_{k=0}^{n} a_k (4 ln 2)^{n−k}/(n−k)! with a₀ = 1, a_k = Ω_{k−1}.
It takes Ω₀ … Ω₆ as printed in `order8_output.txt` (Ω₃ to 110 digits, Ω₄ … Ω₆ to 180) and Ω₀ … Ω₂ from their closed forms
(−4 ln 2; 2π²/3 + 8 ln²2; 80ζ(3) − (8/3)π² ln 2 − (32/3) ln³2), and evaluates the identified f₇ at 200 digits.

Shared with the runner's code: the printed Ω₃ … Ω₆. Not shared: the series of F, the closed form's evaluation, the comparison.

Criteria, written before the first run:
- K1: f₂ = 2π²/3 and f₃ = 80ζ(3) from the same formula (the known terms, a planted check of the series) to 1e-50.
- K2: f₇ from the printed Ω equals the identified (7656704/2835)π⁶ + (328672/45)π⁴ζ(3) − (74752/5)π⁴ + 30720π²ζ(3) − 2176π²ζ(5)
  + 36864ζ(3)² + 565248ζ(3) − 307200ζ(5) + 974336ζ(7) to 1e-90 relative (the printed digits of Ω₃ limit it).
- K3 (reported): f₄ … f₆ from the same series, beside the values of #263's output if printed there.

Mutations: `zeta3` (565248 → 589824, the tower pattern the runner says fails: K2), `ln2` (2^{4ε} → 2^{−4ε}: K1, K2).
