# I151-mac: the coordinator's review of #151's linear e-folding time of the Ellis family at m/a = 1/2

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, mpmath 1.3.0, numpy 2.5.4, scipy 1.18.1, at
nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/151. Reviewed branch `wip/i151-ellis-efold` at 83e4347 and raw
`I151-rpi5` at 85b6d6c.

## Rerun of the runner's script

`python3 ellis_efold.py` from `notes/` of a detached worktree of 83e4347, full, unmutated (`rerun/`).

## Independent check `ind151.py` (criteria written before its first run)

ind151 imports nothing from the repository and nothing from `ellis_efold.py`. Its Ricci routine is the coordinator's,
from `I77-mac` to `I81-mac`. It uses no scipy: its integrators (Numerov, classical RK4), root finder (bisection then
secant), Taylor coefficients (Cauchy sums on a circle, mpmath) and Frobenius recurrence are its own.

Two routes to β, the growth rate of the unstable mode e^{βt} in [GGS09a]'s units (b = 1, γ₀ = 0):
- **Route 1, printed potential.** −χ_ρρ + Wχ = −β²χ with W retyped by the coordinator from [GGS09a] Eq. (32) (TeX in
  `I151-rpi5/src_ggs09a`). The coordinate x(ρ) comes from x_ρ = e^{2γ₁ arctan x}, x(0) = 0, by RK4 on the grid.
  Numerov is run inward from ρ = ±L (start: the decaying solution e^{−β|ρ|}(1 + 1/(β|ρ|)) of the 2/ρ² tail) and matched
  by the discrete Wronskian at ρ = 0. Steps h and h/2 are Richardson-extrapolated (h⁴).
- **Route 2, no potential.** The linearized Einstein–ghost equations in the gauge δΦ = 0 are derived from the
  coordinator's own Ricci tensor of the ansatz (Eq. (3) of [GGS09a]) and reduced to a first-order system for
  C = δc and G = δa − δc: C′ = d′C + c′G, and (x − γ₁)G′ = P C + Q G with P, Q analytic. The throat x = γ₁ is a regular
  singular point. The system is integrated by RK4 in ρ from ρ = ±L in to x = γ₁ ± δ (δ = 0.3), with x carried
  outward from x = γ₁ ± δ. It crosses the throat by Frobenius series at x = γ₁ (exponents 0 and 1, 40 terms), whose
  Taylor coefficients come from Cauchy sums of M(z) = (z − γ₁)A(z) on the circle |z − γ₁| = 1/2 (64 points,
  30 digits). The two sides are matched by det[α₊, α₋] = 0, where α± are the coordinates of the integrated solutions
  in the Frobenius basis. Steps h and h/2 are Richardson-extrapolated. There is no complex path and no W.

Shared with #151:
- the papers' formulas: [GGS09a] Eqs. (11)–(13), (32), V and Ψ₀ (pp. 5–6), the time scale of p. 10, Table I;
- [SN26] Eqs. (2)–(3) and its numbers 3.8895, 0.575, 0.7584, 5.13, 5.12, 5.23, 0.2 %, 1.9 %, which the coordinator read
  in `I151-rpi5/src_sn26/numbers.tex`;
- the idea of the gauge δΦ = 0 (#151's method C), but with the coordinator's own derivation and crossing;
- the ODE that `ellis_efold.md` prints for method C, typed here to be compared;
- #151's printed β values, for comparison only.

| id | criterion | kind |
|---|---|---|
| E0 | planted: the own Ricci routine finds Painlevé–Gullstrand Schwarzschild Ricci-flat | symbolic |
| E1 | background: for g = −e^{2γ₁θ}dt² + e^{−2γ₁θ}[dx² + (1 + x²)dΩ²], θ = arctan x, and Φ = Φ₁θ, the own R_μν − κΦ_μΦ_ν vanishes iff κΦ₁² = −2(1 + γ₁²) (checked at that value, and nonzero at κΦ₁² = +2(1 + γ₁²)), and □Φ = 0 | symbolic |
| E2 | the map, sympy, a, m > 0 symbolic: [SN26]'s metric −e^{2u}dt² + e^{−2u}Ω²(dr² + r²dΩ²) equals a²e^{πγ₁} times the b = 1, γ₀ = 0 metric of E1 under ρ_E = r − a²/4r = a x̃, t = a e^{πγ₁} t̃, γ₁ = m/a. The + end's mass from g_tt = −(1 − 2M/R + …) is m. The minimal areal radius sits at x̃ = γ₁ and equals R⋆ = √(a² + m²) e^{(m/a) arctan(a/m)}. α_th = e^{u} there. With τ = a e^{πγ₁}/β: τα_th/R⋆ − e^{2γ₁ arctan γ₁}/(√(1 + γ₁²)β) = 0. Each identity simplifies to 0 in sympy or, where sympy does not close it (the output says which), is below 1e-40 at 5 points (a, m) at 50 digits. Numbers at a = 2, m = 1: \|R⋆ − 3.8895\| ≤ 5e-5, \|α_th − 0.575\| ≤ 5e-4 | symbolic + numbers |
| E3 | linearization, δΦ = 0, own Ricci: δ(□Φ) ≡ 0 when δd = δa − 2δc. Solving δE_θθ for G′ (G″ must not appear in it) gives (x − γ₁)G′ = PC + QG with P, Q continuous across the throat (at x = γ₁ ± 10⁻²⁰, γ₁ ∈ {1/2, 1}, β = 17/10, 50 digits, the two values agree to 1e-15 relative), and then δE_tt, δE_tx, δE_xx, δE_θθ and δ(□Φ) all vanish on the system C′ = d′C + c′G, G′ = (PC + QG)/(x − γ₁). The G′ that #151's printed ODE implies equals this one. Each identity is linear in C and G; every coefficient is evaluated at 6 points (x, γ₁, β) at 50 digits and must be below 1e-40 | symbolic, 50 digits |
| E4 | potential: the typed W at γ₁ = 0 is −3/(1 + x²)² (sympy); W = −V + 2(∂Ψ₀/Ψ₀)², with V from its definition (p. 5) on the E1 background and Ψ₀ printed (b = 1, γ₀ = 0), rel < 1e-30 at 6 points for γ₁ ∈ {1/2, 1}; ∂²Ψ₀ = VΨ₀ at the same points, rel < 1e-30; W(γ₁) = e^{4γ₁ arctan γ₁}[−3/(1 + γ₁²) − 2γ₁²/(1 + γ₁²)²] (printed, p. 7), rel < 1e-30 | symbolic, 40 digits |
| E5 | planted, route 1: W = −ℓ(ℓ + 1)sech²ρ on the same grid, Numerov, matching and Richardson code, ℓ ∈ {1.3, 2.4}: β = ℓ, rel < 1e-9. The map: at 6 grid points of γ₁ ∈ {1/2, 1}, \|ρ_quad(x_n) − ρ_n\| < 1e-10, with ρ_quad(x) = ∫₀ˣ e^{−2γ₁ arctan y}dy by mpmath quad | 15 digits |
| E6 | planted, route 2: the same RK4, Cauchy–Frobenius, matching and root code on C″ = pC′ + qC with p = 2/(x(1 + x²)) (the γ₁ = 0 structure), q = β² + 2/sinh²x − μ(μ + 1)/cosh²x − (2 + 3x²)/(x²(1 + x²)²), μ = 7/2, γ₁ = 0 map. With C = (x/√(1 + x²))u it becomes u″ = (β² + 2/sinh²x − μ(μ + 1)/cosh²x)u, whose solutions sinh^{−1}x cosh^{−μ}x and sinh²x cosh^{−μ}x give β = μ + 1 = 9/2 and μ − 2 = 3/2. Both are found to rel < 1e-9. A scan of 45 points on [0.2, 5.5] finds 4 sign changes (9/2, 5/2, 3/2, 1/2) | 15 digits |
| E7 | route 1 at γ₁ ∈ {0, 1/2, 1}, L = 38, 24, 9, h = 0.002 and 0.001: β rel to #151's β_A (1.181969726488, 1.875127511869, 5.041327581056) < 1e-9; at γ₁ = 0, \|β² − 1.39705243\| < 1e-8 (one_mode.py N4, the repository's value) | 15 digits |
| E8 | route 2 at γ₁ ∈ {0, 1/2, 1}, same L, h = 0.002 and 0.001: M(γ₁) has eigenvalues 0 and 1 (\|Q₀ − 1\| < 1e-25); the no-log condition of the exponent-1 resonance holds to 1e-20 (relative) at the root and at β = 1; β rel to route 1 < 1e-8; a scan of 40 points on [0.2, 1.5 β₁] has exactly one sign change | 15 digits |
| E9 | T(γ₁) = e^{2γ₁ arctan γ₁}/(√(1 + γ₁²)β) from route 1: T(0), T(1/2), T(1) round to Table I's 0.846, 0.758, 0.675; \|T(1/2)/0.7584 − 1\| ≤ 0.002 (the issue's test); T(1/2) rounds to 0.7584; τ_lin = 2e^{π/2}/β rounds to 5.13; 100(5.12 α_th/R⋆/T − 1) rounds to −0.2 and 100(5.23 α_th/R⋆/T − 1) to 1.9 | numbers |

Mutations, each must exit 1 with its target failing:

| mutation | change | target |
|---|---|---|
| `pg` | √(2M)/r for √(2M/r) | E0 |
| `ghost` | κΦ₁² = +2(1 + γ₁²) used as the passing value | E1 |
| `gamma0` | t = a e^{−πγ₁} t̃ in the map | E2 |
| `scalar` | δd = δa − δc in the reduction | E3 |
| `wtyped` | 2(F_x/F)² → 3(F_x/F)² in the typed W | E4 |
| `numerov` | Numerov's 5h²/12 → 6h²/12 | E5 |
| `rho` | x_ρ = e^{−2γ₁ arctan x} in route 1's map | E5 |
| `frob` | the recurrence uses (n + 1)I − M₀ for nI − M₀ | E6 |
| `match` | α₋ computed in the Frobenius basis evaluated at +δ | E6 |
| `tfac` | T without e^{2γ₁ arctan γ₁} | E9 |

## Results

(after the runs)
