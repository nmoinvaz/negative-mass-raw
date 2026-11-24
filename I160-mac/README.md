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

| file | what |
|---|---|
| `rerun/mult_classify_full.*` | the rerun at ab9cefd: stdout, `/usr/bin/time -l`, exit code |
| `ind160_run1.py`, `.txt`, `.time` | run 1; `ind160_mut_*_run1.txt` its 8 mutations |
| `ind160_run2.py`, `.txt`, `.time` | run 2, with `expo2` added; `ind160_mut_*_run2.txt` its 9 mutations |
| `ind160_run3.py`, `.txt` | run 3, with `expo58` added; `ind160_mut_expo58_run3.txt` (`ind160.py` is the same version as run 3) |

**Rerun** (exit 1, 13 min, 93 MB peak): 21 of 22 checks pass, and `add_perturbed` fails as #160 reports. 21 controls
fire on their targets; `m-unit-sign` is silent, as declared in #160's README A7. The output equals rpi5's apart from
the timings.

**ind160 run 1** (exit 0, 0.6 s): every criterion passes.

| criterion | run 1 |
|---|---|
| N0 | E/X₀² = s² − δ² − τ² from the own block |
| N1 | the six-term static separation; Lemma K's coefficient R²(c + 4λ²)(c + 5λ²) |
| N2 | the ten-term traveling separation, symbolic v |
| N3 | β = (am + b)(cm + d)/(ad − bc); Ψ ∉ span{1, m, 1/(cm + d)} (unit ideal); c = 0: m³ coefficient 18a/d |
| N4 | the consistency identity by the chain rule; polynomial P, S force q ≡ 0 |
| N5 | β = X m_X/2; leading pole coefficients −k²X₁²μ² for k = 1 … 4 |
| N6 | admissible top and bottom exponents both exactly {−2, −1, 0, 1} |
| N7 | X⁶ coefficient 20R⁴k₁²; X⁴ coefficient R⁴(c + 4k₀)(c + 5k₀); unit ideal in both branches |

Re-solve: steps 4 to 6 of #160's §4. They were reviewed by hand and recomputed: the pole order (N5), the exponent range
by a different count (N6) and the Laurent unit ideals (N7).

N6 is the coordinator's own form of step 5. Only F₅ = X², F₈ = X⁴ and F₆ have leading coefficients that never vanish at
integer b. F₆'s factor is −b² + 3b/2 + 13, and F₁₀'s factor 20 + b − b² vanishes only at b = 5 and −4. So the count
does not depend on v. #160's step 5 used tables that include F₁ and F₃, whose leading coefficients vanish at special v
(F₃'s at b = 0, v² = 1/3). Its conclusion, exponents in [−2, 1], is the same.

**Silent mutations.**
- In run 1, `expo` (F₁₀'s exponent counted as 4 + b) was **silent**: 4 + b always lies in {b + 1, …, b + 4}, and F₁₀ is
  never decisive in the count.
- In run 2 the coordinator added `expo2` (at most two exponents outside), predicted by guess rather than computed. It
  was also **silent**: every excluded b has three exponents outside.
- In run 3 `expo58` (F₅ and F₈ dropped from the count) was added after computing its effect. It fires: the admissible
  set becomes {−4, …, 1, 5}.

None of these changed a criterion. Runs 2 and 3 equal run 1 apart from the timings.

| mutation | exit | failed | target met |
|---|---|---|---|
| `Dsign` | 1 | N0, N1, N2 | yes |
| `theta` | 1 | N1 | yes |
| `trav` | 1 | N2 | yes |
| `mob` | 1 | N3 | yes |
| `qid` | 1 | N4 | yes |
| `pole` | 1 | N5 | yes |
| `expo` | 0 | none | **silent** |
| `expo2` | 0 | none | **silent** |
| `expo58` | 1 | N6 | yes |
| `lau` | 1 | N7 | yes |
