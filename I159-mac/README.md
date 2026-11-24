# I159-mac: the coordinator's review of #159's limits of conical shifts with det R₃ = 0

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2
processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/159. Reviewed branch `wip/i159-conical-limit` at ad8dab9 and
raw `I159-rpi5` at b940671.

## Rerun of the runner's script

`python3 conical_limit.py` from `notes/warp/` of a detached worktree of ad8dab9, full, with its 14 controls (`rerun/`).

## Independent check `ind159.py` (criteria written before its first run)

ind159 imports nothing from the repository: no `conical_limit.py` and no `det_classify.py`. It builds D from #65's
formula D = h(h² − P² − Q² + Y² + Z²) − P(Y² − Z²) + 2QYZ with the block entries of a static shift. The coordinator's
`I79-mac/ind79.py` (H1) checked that formula against an own Ricci routine, and `I158-mac/ind158.py` (K1) checked the
entries. Its transseries solver, a truncated polynomial arithmetic in ν = 1/η and T = ln η, is its own. So is its
integrator: classical RK4 in s = ln η at 30 digits, with Richardson extrapolation over h and h/2 and its own Newton step
for q. It uses no `odefun`.

Shared with #159: the θ-form variables (G = F, p = θF, q = θ²F, θ = η d/dη); the printed A₀, A₁, A₂ and series
coefficients, typed from `conical_limit.md`; the reduced variables r = η²p, s = r′ − 2r; and the far-field test shift
w = −2Uρ²/x².

| id | criterion | kind |
|---|---|---|
| M1 | 8ρ⁶D for u = F(x/ρ), built from the own block, equals A₀ + ν²A₁ + ν⁴A₂ with the printed A₀ = p²(p² − q)(p² + q), A₁ = G²p²q² + 4Gp⁴q − 2Gq³ + 4p⁶ − 3p²q², A₂ = 2(G(q − p) + p²)(G²q² + 2Gp³ + 2Gp²q + 2p⁴ − q²) | symbolic |
| M2 | the own solver, with F_∞ and C = a₄,₀ symbolic, a₂ = −2F_∞ and unknowns a_{n,j} for n = 3 … 9 and j ≤ n/2 + 1: every stage is solvable, a₄,₀ is the only free unknown, a₄,₁ = F_∞(F_∞² + 7), a₆,₀, a₆,₁, a₆,₂ and a₈,₃ equal the printed values, odd a_{n,j} vanish, and N vanishes through ν¹⁵. Without logs (j = 0 only) the stage n = 4 has no solution unless F_∞⁴(F_∞² + 7) = 0 | symbolic |
| M3 | numerical, the own RK4 in s = ln η (30 digits, h = 1/400 and 1/800, Richardson), from the own n ≤ 9 series at η = 1000 inward. For (F_∞, C) ∈ {(1, 0), (−3/2, 1), (2, 1/2)}, \|ΔG\| and \|Δp\| against the n ≤ 9 series at η = 200 and 100 are below 1e-10. For (2, 1/2) at η = 50, the difference against an own n ≤ 13 series is below 1e-10. The difference against the n ≤ 9 series is printed, to compare with #159's dev-run 2.24e-10 | 30 digits |
| M4 | far field: for u = U + εw, w = −2Uρ²/x², D has no ε⁰, ε¹, ε² terms; the ε³ coefficient equals det_classify.md §7's −UZ²[(1 − U²)w_xx + w_ρρ + w_ρ/ρ]; and at fixed ρ, as x → ∞, x⁸/ρ² times the ε³, ε⁴, ε⁵, ε⁶ coefficients tends to 128U⁴, −128U⁴, 0, 0 | symbolic |
| M5 | reduced system: with p = ν²r and q = ν²s, N/ν⁸ = R(G, r, s, σ = ν²) is a polynomial, R(G, r, s, 0) = −s²(r² + 2Gs); at (r, s) = (4G, −8G), R = 0 and ∂R/∂s = −128G³; ∂S/∂r = −4, ∂S/∂G = 8; the Jacobian of (σr, 2r + S, −2σ) at (G, 4G, 0) has eigenvalues 0, −2, −2 | symbolic |

Mutations, each must exit 1 with its target failing:

| mutation | change | target |
|---|---|---|
| `Ysign` | Y = u u_xρ/2 − u_x u_ρ in the block | M1 |
| `A1` | −3p²q² → −2p²q² in the typed A₁ | M1 |
| `b` | a₄,₁ expected F_∞(F_∞² + 8) | M2 |
| `rk` | RK4 weights 1, 2, 2, 1 → 1, 3, 1, 1 | M3 |
| `ff` | the ε⁴ limit expected +128U⁴ | M4 |
| `eig` | ∂S/∂r expected −3 | M5 |

## Results

(after the runs)
