# I160-mac: the coordinator's review of #160's multiplicative separable shifts with det R₃ = 0

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2
processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/160. Reviewed branch `wip/i160-mult-classify` at ab9cefd and
raw `I160-rpi5` at d7f77da.

## Rerun of the runner's script

`python3 mult_classify.py` from `notes/warp/` of a detached worktree of ab9cefd, full, with its controls (`rerun/`).
Expected, as #160 reports: exit 1, from `add_perturbed` alone.

## Independent check `ind160.py` (criteria written before its first run)

ind160 imports nothing from the repository. D is #65's formula with the coordinator's static block (as in
`I158-mac`/`I159-mac`). Its identities, Gröbner computations and exponent count are its own. For step 5 of §4 it uses a
different argument from #160's tables: only F₅ = X², F₈ = X⁴, F₆ and F₁₀, whose leading coefficients it computes
exactly.

Shared with #160: the log variables (p₁, m, β, c, s₂, U, W), the printed s, δ, τ, the six- and ten-term separations,
Θ, Ψ, Φ₂, Φ₃, the structure of the proof (Lemma L and steps 1–6), and the Laurent ansatz of step 6.

| id | criterion | kind |
|---|---|---|
| N0 | for u = X R + v with jets (X₀, X₁, X₂, R₀, R₁, S₀), E = 8D/R₁² from the own block satisfies E/X₀² = s² − δ² − τ² with the printed s, δ, τ | symbolic |
| N1 | static v = 0: E = R₀²X₀⁴ Σ_{i≤6} f_i g_i with the printed f, g, Θ, Ψ; at m = λ², β = 0 the coefficient of X₀² in Σ f_i g_i is R₀²(c + 4λ²)(c + 5λ²) | symbolic |
| N2 | traveling: E/X₀² = Σ_{i≤10} F_i G_i with the printed F, G, Φ₂, Φ₃, for symbolic v | symbolic |
| N3 | Lemma X. For ρ = (am + b)/(cm + d), β = ρ/ρ_m = (am + b)(cm + d)/(ad − bc). For c(ad − bc) ≠ 0, Ψ = −4m² − 2mβ is not in span{1, m, 1/(cm + d)}: the coefficient equations of Ψ(cm + d) = (α₀ + α₁m)(cm + d) + α₂, with the saturation by c(ad − bc), generate the unit ideal. For c = 0, ρΘ is cubic in m with m³ coefficient 18a/d | symbolic |
| N4 | step 2. The consistency identity q² − (P_R/2)q + Pq_R = 0 holds for q = R′/ρ, P = R′², by the chain rule. With P = a₁R + a₂R², S = s₁R + s₂R² and q = S − P_R/2, the coefficients of the identity in R force q ≡ 0 | symbolic |
| N5 | step 4. β = X m_X/2 as an identity for β = (ln X)″, m = (X′/X)² with X as coordinate. For m = μ(X − X₁)^{−k} + r₀ + r₁(X − X₁), k = 1 … 4, X₁ ≠ 0, the leading coefficient of Θ = 20m² + 2mβ − 4β² at X₁ is −k²X₁²μ², of order 2k + 2 | symbolic |
| N6 | step 5, robust count. For integer b in [−15, 15], with m = κ_b X^b + lower terms, the exact top exponents of F₅, F₈, F₆ = 2vX³Φ₃ and F₁₀ = X⁴Θ, counting an exponent only where its leading coefficient is nonzero. b is admissible iff at most one distinct exponent lies outside {b + 1, …, b + 4}. The admissible b are exactly {−2, −1, 0, 1}, and by the same count at X → 0 so are the admissible bottom exponents a | exact |
| N7 | step 6. For m = k₋₂X⁻² + k₋₁X⁻¹ + k₀ + k₁X, β = Xm_X/2, the X⁶ coefficient of E/X₀² is 20R₀⁴k₁², and with k₁ = 0 the X⁴ coefficient is R₀⁴(c + 4k₀)(c + 5k₀). With R₀ = aY, c = κ², s₂ = κ² + κw (Y = e^{κρ}, w = 1/ρ) and k₀ = −κ²/4 or −κ²/5, the coefficients in (X, Y, w), with 1 − t κ a v, generate the unit ideal in each branch | symbolic |

Mutations, each must exit 1 with its target failing:

| mutation | change | target |
|---|---|---|
| `Dsign` | Y = u u_xρ/2 − u_x u_ρ in the block | N0 |
| `theta` | 19m² for 20m² in Θ | N1 |
| `trav` | F₄ = 2X²m | N2 |
| `mob` | expected m³ coefficient 17a/d | N3 |
| `qid` | the identity with −Pq_R | N4 |
| `pole` | expected +k²X₁²μ² | N5 |
| `expo` | F₁₀'s top exponent counted as 4 + b | N6 |
| `lau` | expected X⁶ coefficient 10R₀⁴k₁² | N7 |

## Results

(after the runs)
