# I263-mac-review: the coordinator's review of #263 (Ω₅, and the ln 2 structure of W²(D))

Issue https://github.com/nmoinvaz/negative-mass/issues/263; branch `wip/i263-omega5` at c618f36, raw `I263-rpi5` at 091e6e1.

## Criteria, written before any run

`ind263.py`, with Ω₀ … Ω₅'s closed forms typed from the notes (README.md, omega3.md, omega4.md, omega5.md):
- K1: Ω₅'s closed form evaluated by sympy and mpmath at 110 digits equals the note's 100-digit value, to 1e-95.
- K2: with ε = 1/s, (1 + Σ Ω_k ε^{k+1}) e^{4 ln 2 ε} = F(ε) has coefficients f₀ … f₆ free of ln 2 (sympy, d/d ln 2 = 0).
- Mutations: `om5` (Ω₅'s ζ(3) ln³2 coefficient changed) must fail K1 and K2; `om3` (Ω₃ gains ζ(3) ln 2) must fail K2.

**Amendment A1 (after run 1).** Run 1's K2 failed because the check typed Ω₁ as π²/3 + 4 ln²2. That is Ω₁/2, the coefficient of
1/(D − 3) in Paper III's abstract. In W²a² = s + Ω₀ + Ω₁/s + … the term is Ω₁ = 2π²/3 + 8 ln²2 (README.md). The other closed forms were
typed correctly (K1 passes for Ω₅). Fix: Ω₁ corrected. The criteria are unchanged.
