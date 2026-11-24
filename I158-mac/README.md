# I158-mac: the coordinator's review of #158's classification of the shifts that pass the one-sign stage

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2
processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/158. Reviewed branch `wip/i158-one-sign` at 04a30d8 and raw
`I158-rpi5` at 42837a5.

## Rerun of the runner's script

`python3 one_sign_classify.py` from `notes/warp/` of a detached worktree of 04a30d8, full, with its 23 controls
(`rerun/`).

## Independent check `ind158.py` (criteria written before its first run)

ind158 imports nothing from the repository: no `one_sign_classify.py`, `same_sign_scalars.py`, `phantom_source.py` or
`two_scalars.py`. Its Ricci routine is the coordinator's, from `I77-mac` to `I81-mac`. Its rank test, ideal
computations, vector-field brackets and jet-space compatibility test are its own. For the static class it does not use
#158's parametrization (s, σ, C). Instead it tests formal integrability directly, by linear algebra on third- and
fourth-order jets.

Shared with #158: the frame (n = ∂_t − b∂_x, ∂_x, e_ρ, e_φ); the printed block formulas, typed here from
`one_sign_classify.md`; Lemma R's parametrization; the reductions and the printed identities; and the equations
A = Q(Z² + Y²) + 2hZY and B = PQY − Z(Q² + Y²) of §General static.

| id | criterion | kind |
|---|---|---|
| K0 | planted: the own Ricci routine finds Painlevé–Gullstrand Schwarzschild Ricci-flat | symbolic |
| K1 | block: for an undefined b(t, x, ρ), the own Ricci tensor in the frame (n, ∂_x, ∂_ρ, ρ⁻¹∂_φ) has R₃ = [[P − h, Q, Z], [Q, −P − h, Y], [Z, Y, h]] with P = n(b_x) − b_x², Q = −½(b_ρρ + b_ρ/ρ), Z = ½b_xρ, Y = −½n(b_ρ) + b_xb_ρ, h = ½b_ρ², and R(e_φ, e_a) = 0 for every a | symbolic |
| K2 | Lemma R: (a) for R₃ built from v, R₃ − (h + v₂²)η₃ = −vvᵀ identically; (b) with v₀² = −QZ/Y, v₁² = −QY/Z, v₂² = −ZY/Q, the relations h = ½(v₀² + v₁²) and P = −(v₀² + v₂²) are equivalent to A = 0 and B = 0 (identities h − ½(v₀² + v₁²) = A/(2YZ) and P + v₀² + v₂² = B/(QY)), and A = 0 with YZ ≠ 0 forces QYZ < 0, so v is real; (c) at 30 random rational v-blocks the 2 × 2 minors of R₃ − λη₃ have exactly one common nonzero root, λ = h + v₂²; at 30 random rational generic blocks they have none | symbolic + exact points |
| K3 | b(ρ): the block has P = Z = Y = 0 and Q = −½(b″ + b′/ρ); for b = C ln ρ + b₀ the kernel of M is span(n, ∂_ρ) and [n, ∂_ρ] = b′∂_x is not in it (closure fails) | symbolic |
| K4 | planar b(t, x): R₃ = diag(P, −P, 0) and rank(R₃ − λη₃) = 1 iff λ = −P. Theorem P's growth: for x″ = K₀x − α(t), the coefficient of X (the initial position, with the initial velocity independent of X) in x′(t₁ + Δ) is κ sinh κΔ for K₀ = κ² and −κ sin κΔ for K₀ = −κ², and in x(t₁ + Δ) it is cosh κΔ, resp. cos κΔ | symbolic |
| K5 | additive u = X(x) + R(ρ) + v: the block is Z = 0, Y = X′R′, Q = −S/2, P = −uX″ − X′², h = R′²/2. With Lemma R's relations and the saturation by X′R′v₂, v₀, S and uX″ lie in the radical. For u = cx + C ln ρ + d the kernel span(n, v₂∂_x − v₁∂_ρ) is not involutive for C ≠ 0 and is involutive for C = 0 | symbolic |
| K6 | multiplicative u = X(x)R(ρ) + v: F = Q(Z² + Y²) + 2hZY equals the printed −XX′²R′²(S(1 + W²) − 2XR′²W)/8, W = 3XR + v; the three coefficients of the quadratic in X, with 1 − tRR′, generate the unit ideal | symbolic |
| K7 | conical u = F(x/ρ) + v: the own block gives the printed ρ²(P, Q, Z, Y, h). E_a = w(1 + U²) + 2ηUG² and E_b = (η² + 1)ηH + (η² − 1)G lie in the ideal of Lemma R's relations saturated by ηGUwv₀. G = Cη/(η² + 1) solves E_b = 0. At it, E_a = (2G/(η² + 1))(1 + F² + Cη²F). At F = −Cη²/(2(η² + 2)), F′ − G equals the printed −Cη(η⁴ + 6η² + 6)/((η² + 1)(η² + 2)²) | symbolic |
| K8 | static u(x, ρ), u_xρ ≠ 0. At 3 rational points (ρ, u, u_x, u_ρ, u_xρ) with YZ ≠ 0, u_ρρ and u_xx are solved from A = B = 0. The third-order jet equations (D_x, D_ρ of A and B: 4 equations in u_xxx, u_xxρ, u_xρρ, u_ρρρ) have a nonsingular matrix. The fourth-order equations (D_x², D_xD_ρ, D_ρ² of A and B: 6 in 5 unknowns) are inconsistent, so no solution passes through those 2-jets. Planted, through the same code: u_xx = 0, u_ρρ + u_ρ/ρ = 0 is consistent at both orders; u_xx = u², u_ρρ = 0 is inconsistent at fourth order | exact |

Mutations, each must exit 1 with its target failing:

| mutation | change | target |
|---|---|---|
| `pg` | √(2M)/r for √(2M/r) | K0 |
| `Ysign` | Y = +½n(b_ρ) + b_xb_ρ | K1 |
| `lemR` | P = +(v₀² + v₂²) in the v-block | K2 |
| `brho` | b = C ln ρ + b₀ + ρ²/10 claimed to have P = Z = Y = 0 and Q = 0 | K3 |
| `growth` | coefficient κ cosh κΔ claimed for K₀ = κ² | K4 |
| `addP` | P = −X″ − X′² in the additive block | K5 |
| `multW` | W = 2XR + v | K6 |
| `conEb` | (η² + 1)G for (η² − 1)G in E_b | K7 |
| `jet4` | the D_x² equation of B dropped at fourth order | K8 |

## Results

(after the runs)
