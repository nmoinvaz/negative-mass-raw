# I269-mac-review: the coordinator's review of #269 (an exact time-dependent family behind Y = R e^{K(t+x)})

Machine: the coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/269. Branch `wip/i269-exact-solution`
at 118ef9a, raw `I269-mac` at 3b276e1e.

## Criteria, written before any run

**Independent check (`ind269.py`).** The claim: for every member c, the metric
ds² = −F dv² + 2 dv dρ + r² dΩ², with r = λ(v) R(ρ), F = A − 2ρ λ̇/λ + 1/λ² − 1, λ² = L + β e^{Kv}, K = −2c/π and φ = √2 arctan ρ
unchanged, solves R_ab = ε φ_a φ_b + V g_ab (ε = −1, the BF06 potential) and ε□φ = V′(φ) exactly.

The check builds the Ricci tensor by brute force (the coordinator's code of `ind217.py`, coordinates (v, ρ, θ, ϕ)) with abstract
F(v, ρ), r(v, ρ) and φ(ρ). It then evaluates the five residuals (vv, vρ, ρρ, θθ, scalar) with the explicit functions' jets from mpmath
at 40 digits. It shares the member's definition and the potential with the code under test, and nothing else.

| check | what | pass |
|---|---|---|
| K1 | residuals relative to the largest term, at c = −1, −0.3, −1.5, −10; (L, β) = (1, 0.3), (1, −0.4), (2, 0.7); (v, ρ) at 4 points each, with λ² > 0 | all below 1e-30 |
| K2 | the linearization in β at β = 0: δr = (β/2) R e^{Kv} | the coefficient equals R/2 · e^{Kv} to 1e-30 at the same points |

Mutations, each with the check it must fail:
- `no-h`: F without the term 1/λ² − 1. K1 must fail (the θθ equation).
- `k-off`: λ² = L + β e^{1.01 K v}. K1 must fail (the vv equation).
- `phi-scale`: φ = 1.01 √2 arctan ρ. K1 must fail (the ρρ equation).

## Results

| check | result | verdict |
|---|---|---|
| K1 | 47 points (4 members, 3 (L, β), 4 points; λ² > 0): worst relative residual 8.9e-40 | pass |
| K2 | ∂r/∂β at β = 0 against R e^{Kv}/2: 2.3e-41 | pass |
| `no-h` | K1 0.91 | fires |
| `k-off` | K1 4.6e-3, K2 6.2e-2 | fires |
| `phi-scale` | K1 0.30 | fires |

Reading: the exact family is confirmed by a brute-force Ricci tensor that shares no code with `exact_mode.py`, at every member and
every sign of β tested, and its linearization in β is #262's Y_K.
