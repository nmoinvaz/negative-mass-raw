# I166-mac: the coordinator's review of #166 (rerun of the default mode, independent check ind166)

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0 (`/Users/nathan/Source/negative-mass/.venv`),
at nice 10 with at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/166. Under review: branch
`wip/i166-one-sign-time` at 1df365a, raw `I166-rpi5` at 6ee0ec3. Stop condition: any single run not finished after 1 h
of wall time is stopped (by its PID) and reported. Written 2026-11-26 before the first run of `ind166.py`.

## Rerun of the runner's default mode

`python3 notes/warp/one_sign_time.py` from a worktree at 1df365a: the 14 checks, then the 21 controls.

## ind166.py: what it shares with #166

Shared: sympy 1.14.0; the metric ds² = −dt² + (dx + b dt)² + dρ² + ρ² dφ²; #158's block formulas P = n(b_x) − b_x²,
Q = −½(b_ρρ + b_ρ/ρ), Y = −½n(b_ρ) + b_x b_ρ, h = ½b_ρ² and Lemma R's equations (reviewed in #158 and by ind158), used
only in J3 and J5. Not shared: ind166 imports nothing from the repository. Its Ricci tensor is its own (Christoffel
symbols, R_bd = ∂_aΓ^a_bd − ∂_dΓ^a_ba + Γ^a_aeΓ^e_bd − Γ^a_deΓ^e_ba), as are the stage test at exact points, the bracket
and the ODE checks. #166 uses `ricci` of `phantom_source.py`, `same_sign_form` and `closure2` of `same_sign_scalars.py`.

Notation: γ = C′/(2C), w = γ − c, λ = C²/(2ρ²) + w², α = (C/ρ)(dx + b dt) + w dρ, n = ∂_t − b∂_x, K₂ = w∂_x − (C/ρ)∂_ρ,
coordinates (t, x, ρ, φ).

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| P0 | Planted: for b = x, ind166's Ricci tensor equals g_ab − dρ_a dρ_b − ρ² dφ_a dφ_b exactly (the (t, x) block of the metric, curvature K = 1, #158's planar shift with K = −a_x = 1) |
| J1 | For b = c(t)x + C(t) ln ρ + d(t), with c, C, d undefined, after c′ → 2γc − γ² (and c″ → its t-derivative with the same substitution): R_ab − [λ(g_ab − ρ² dφ_a dφ_b) − α_a α_b] = 0 identically |
| J2 | The stage at exact points with ind166's Ricci tensor. At t = 0, ρ = 1, x ∈ {1/3, −2, 5}, for T1 = x/2 + e^{2t} ln ρ, T2 = (1/2 + e^{2t}/3)x + e^{2t} ln ρ, T4′ = −x/(t − 1) + (t − 1)⁻² ln ρ (T4 shifted to t = 1) and the static S = 3x/2 + 2 ln ρ + 1/5: with λ₀ = λ at the point, the characteristic polynomial of the matrix R − λ₀g is x²(x² − τx + e) with τ < 0 < e (rank 2, both nonzero eigenvalues negative, two phantoms). For F1 = S + x²/10 at the same points: the 3 × 3 minors of R − λg, as polynomials in λ, have no common root other than possibly λ = 0 (their gcd is a power of λ or 1) |
| J3 | Lemma Z re-derived: the elimination of (v₁, v₂) from {P + v₂², Q, Y + v₁v₂, 2h − v₁²} (v₀ = 0) gives the ideal ⟨Q, 2hP + Y²⟩ of ℚ[P, Q, Y, h], and the elimination of (v₀, v₁) from {P + v₀², Q + v₀v₁, Y, 2h − v₀² − v₁²} (v₂ = 0) gives ⟨Y, Q² + P(2h + P)⟩ (equal reduced Gröbner bases) |
| J4 | Closure. (a) With M = R − λg from J1's Ricci tensor (ODE substituted): M n = 0 and M K₂ = 0. (b) ind166's Lie bracket gives [n, K₂] − (C′/C)K₂ = r ∂_x with r = w′ + wc − 2γw − C²/ρ², and ∂_ρ r = 2C²/ρ³ |
| J5 | Branch B. (a) For b = κ(t)x + e(t) + m(t)F(ρ) + r₀(t), F′ = f, with the block formulas above: Y = (−m′/2 + κm)f, and at m′ = 2κm, Q² + P(2h + P) = m²g − p m² f² + p² with p = κ² − κ′, g = (f′ + f/ρ)²/4. (b) Re-solved: sympy's `solve` of {m²g_a − p m²F_a + p², m²g_b − p m²F_b + p²} (F = f², F_a ≠ F_b, p ≠ 0) for (p, m²) returns only p = (g_a − g_b)/(F_a − F_b) and a value of m² free of t, so p and m² do not depend on t |
| J6 | The c-ODE re-solved: sympy's `dsolve` of c′ = 2c − 1 (C = e^{2t}) gives c = 1/2 + k e^{2t}, which contains T1 (k = 0) and T2 (k = 1/3); `dsolve` of c′ = −2c/t − 1/t² (C = t⁻²) gives c = −1/t + k/t², which contains T4's c = −1/t; and c = |C|(k₀ − K), K′ = γ²/|C|, solves c′ = 2γc − γ² for undefined C > 0 |

## Mutations (`--mutate=NAME`; each must make ind166 exit non-zero with exactly these criteria failing)

| mutation | change | targets |
|---|---|---|
| `plant-K2` | P0 compares with 2 (g_ab − dρ_a dρ_b − ρ² dφ_a dφ_b) | P0 |
| `ode-flip` | J1 substitutes c′ → 2γc + γ² | J1 |
| `t1-pert` | J2's T1 gets + x²/10 | J2 |
| `lemz-sign` | J3's first claimed ideal is ⟨Q, 2hP − Y²⟩ | J3 |
| `bracket-drop` | the K₂(n^μ) term of ind166's bracket is dropped in J4 (b) | J4 |
| `sep-swap` | J5 (b) expects p = (g_a − g_b)/(F_b − F_a) | J5 |
| `ode-k` | J6 expects c = −1/2 + k e^{2t} for c′ = 2c − 1 | J6 |

## Runs (filled in as they are done)
