# I165-mac: the coordinator's review of #165 (rerun of the default mode, independent check ind165)

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0 (`/Users/nathan/Source/negative-mass/.venv`),
at nice 10 with at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/165. Under review: branch
`wip/i165-one-sign-static` at f58b0b8, raw `I165-rpi5` at 1b6fed7. Stop condition: any single run not finished after
1 h of wall time is stopped (by its PID) and reported. Written 2026-11-26 before the first run of `ind165.py`.

## Rerun of the runner's default mode

`python3 notes/warp/one_sign_static.py --raw=<this repository>/I165-rpi5` from a worktree at f58b0b8: the checks, then
the 11 controls (each a subprocess, so at most 2 processes).

## ind165.py: what it shares with #165

Shared: sympy 1.14.0; the five-equation system of #158 in Lemma R's parametrization (u_xx = Φ₁ = (v₀² + v₂² − a²)/u,
u_xρ = Ψ = −2v₀v₂, u_ρρ = Φ₃ = −β/ρ + 2v₀v₁, v₀ = β cos θ, v₁ = β sin θ, v₂ = a/(u cos θ − sin θ), s = tan(θ/2)),
reviewed in #158 and by ind158; and the objects under test, read from `I165-rpi5`: `chain/chain.json` (f₀, f₁, f₂, f₁₁,
f₁₂), `chain/delta.txt` (Δ′) and two of the stored modular certificates. Not shared: `one_sign_static.py` and
`one_sign_classify.py` are not imported or read by ind165. The fields, the solve for σ̄, C̄, the stripping of factors, the
certificate expansion and the s-constant and s = 0 derivations are the coordinator's code.

Coordinates and the derivation used by ind165 (different from #165's, which solves E₁, E₂ in 5D and then sets ρ = 1):
the invariant jets u, A = ρu_x, B = b = ρu_ρ, s, and v = A/w with c = (1−s²)/(1+s²), σ = 2s/(1+s²), w = uc − σ,
D = u(1−s²) − 2s. X̄ᵢ = ρXᵢ act on invariants by X̄₁(u, A, B) = (A, ρ²Φ₁, ρ²Ψ), X̄₂(u, A, B) = (B, A + ρ²Ψ, B + ρ²Φ₃), and
on v by the chain rule. With T = ∂_s − (v w_s/w)∂_v (∂_s at fixed u, A, B), X̄ᵢ = X̄ᵢ⁰ + σ̄ᵢ T. Since [ρX₁, ρX₂] =
ρ²[X₁, X₂] − X̄₁, the A and B components of [X̄₁, X̄₂] + X̄₁ vanish iff E₁, E₂ hold; ind165 solves these two linear
equations for σ̄_x, σ̄_ρ, and C̄ is the s component X̄₁σ̄_ρ − X̄₂σ̄_x + σ̄_x.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| P1 | Planted solution. For u = c₀x + C₀ ln ρ + d₀ with (c₀, C₀, u₀) ∈ {(2, 3, 5), (−1, 1/2, 7), (3, −2, 1)} and d₀ = u₀ − c₀x₀ − C₀ ln ρ₀ (so u(x₀, ρ₀) = u₀ and the jets are rational), at (x₀, ρ₀) ∈ {(1/3, 2), (2, 1/5)}, with s = 1 and with s = −1: (a) u_xx = Φ₁, u_xρ = Ψ, u_ρρ = Φ₃ exactly at the jets; (b) ind165's σ̄_x, σ̄_ρ have nonzero denominators and the value 0 at the invariant jets (u, b, v, s); (c) ind165's C̄ has a nonzero denominator and the value 0 there |
| P2 | Planted inconsistency, through the same bracket, apply and strip functions as C2, C3: on (p, q, r) with X₁ = ∂_p, X₂ = ∂_q + p(q²+1)∂_r the r component of [X₁, X₂] is q²+1 up to a constant, f₁ = 0, and sympy's `groebner` of (f₀, f₂) over ℚ is [1]; the flat toy X₂ = ∂_q + q∂_r has bracket 0 |
| C1 | In lowest terms, den(σ̄_x) = k · s · u · Δ′ and den(σ̄_ρ) = k′ · s · u · (1+s²) · Δ′, with k, k′ ∈ ℚ∖{0} and Δ′ the polynomial in `chain/delta.txt` |
| C2 | The numerator of ind165's C̄ in lowest terms, with every power of u, b, v, s, s−1, s+1, s²+1, D and Δ′₁₆₅ removed by exact division (Δ′₁₆₅ = ind165's den(σ̄_x)/(s u), normalized), equals the stored f₀ times a nonzero rational constant |
| C3 | For (F, i, G) ∈ {(f₀, 1, f₁), (f₀, 2, f₂), (f₁, 1, f₁₁), (f₁, 2, f₁₂)}, F and G stored: the numerator of ind165's X̄ᵢF over the common denominator of the components, with the same factors removed as in C2, equals G times a nonzero rational constant |
| C4 | Modular evidence, re-expanded. For (p, s₀) ∈ {(2147483629, 2), (2147483587, 7)}: with g = (f₀, f₁, f₂, f₁₁) stored, at s = s₀, reduced mod p, and g₅ = 1 − t u v b D(s₀) Δ′(s₀) (stored Δ′), the stored cofactors give Σ cᵢ gᵢ = a nonzero constant in GF(p)[t, u, b, v], expanded with sympy's `ring` over GF(p) |
| C5 | s ≡ s* constant, re-solved (c, σ nonzero symbols, κ = 2cσ from v₀v₁ = β²cσ). (a) sympy's `dsolve` of B′ = κB²/ρ (B = ρu_ρ) gives 1/B = const − κ ln ρ; (b) u = −ln(W)/κ + d(x), W = k(x) − κ ln ρ, has ρu_ρ = 1/W; (c) the Ψ residual R = u_xρ (uc − σ) + 2c u_ρ u_x times ρW², written with L = ln W, ln ρ = (k − W)/κ, k′ = K, d′ = E, is a polynomial in (L, W) whose L coefficient is a nonzero multiple of K and which, at K = 0, equals a nonzero multiple of E·W; (d) the Wronskian of (1, W, ln W) in W is nonzero; (e) u_x = 0 at K = E = 0 |
| C6 | s ≡ 0 (c = 1, σ = 0). (a) `dsolve` of u_ρρ + u_ρ/ρ = 0 gives u = f(x) ln ρ + g(x); (b) the Ψ residual R = u u_xρ + 2u_x u_ρ times ρ, with L = ln ρ, has L coefficient a nonzero multiple of f f′ and, at f′ = 0, equals a nonzero multiple of f g′; (c) u_x = 0 at f′ = g′ = 0 |

Hand-checked by the coordinator, no code: Lemma Q (the level curves are lines through one point (x₀, 0)), the corollary
from (H) by the constant-rank theorem and #158's Proposition C, and the s ≡ 0 and s ≡ s* steps from the coefficient
identities to u_x = 0.

## Mutations (`--mutate=NAME`; each must make ind165 exit non-zero with exactly these criteria failing)

| mutation | change | targets |
|---|---|---|
| `plant-xr` | the planted u gets + xρ/7 | P1 |
| `toy-flat` | the flat toy is passed to P2's rejection test | P2 |
| `phi3-cs` | ρ²Φ₃ = −b + b²cσ (factor 2 dropped) everywhere ind165 uses it | C1, C2, C3 |
| `strip-D` | D is left out of C2's list of removed factors | C2 |
| `c3-swap` | C3 applies X̄₂ where X̄₁ is named, and X̄₁ where X̄₂ is | C3 |
| `cert-coef` | one coefficient of the first cofactor of each C4 certificate changed by 1 | C4 |
| `psi-zero` | the Ψ equation of C5 and C6 replaced by u_xρ = 0 | C5, C6 |

P1 is not a target of `phi3-cs`: at s = ±1, c = 0, so the mutated Φ₃ agrees with Φ₃ on the planted family, which
therefore still solves the mutated system with s ≡ ±1; the mutated σ̄ must vanish there unless its denominator does.

## Amendments

**A0 (2026-11-26, before the first run of ind165).** P1 first named d₀ ∈ {5, 7, 1}; then u(x₀, ρ₀) contains ln 2 or ln 5
and the invariant jets are not rational, so (b) and (c) could not be evaluated exactly. The three values now fix u(x₀, ρ₀)
= u₀ through d₀, which the family leaves free. Nothing has been run.

## Runs (filled in as they are done)
