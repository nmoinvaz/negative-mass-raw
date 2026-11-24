# I161-mac: the coordinator's review of #161's closure for planar shifts that cross |u| = 1 or do not travel

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2
processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/161. Reviewed branch `wip/i161-planar-closure` at 1ccf30f and
raw `I161-rpi5` at 6832efe.

## Rerun of the runner's script

`python3 planar_closure.py` from `notes/warp/` of a detached worktree of 1ccf30f, full, with its controls (`rerun/`).
Expected, as #161 reports: exit 1, with `crit_pg_iv` and `E_hol` failing as worded, and `E-ext` silent.

## Independent check `ind161.py` (criteria written before its first run)

ind161 imports nothing from the repository: no `planar_closure.py`, `two_scalars.py` or `phantom_source.py`. Its Ricci
routine is the coordinator's, from `I77-mac` on. Its d'Alembertian, geodesic and Jacobi integrator (classical RK4,
Richardson over the time step) and composite Gauss–Legendre quadrature are its own.

Shared with #161: the closure criterion C[b] = □ ln|K| − 2K; Θ; the profiles u_s = 3/(1 + ξ²) and F = G = u(1 − u)(1 − 2u);
Theorem E's example H = J = (3/2)S, S(x) = f(x)/(f(x) + f(1 − x)), f = e^{−1/x}; and the initial line p + q = −2.

| id | criterion | kind |
|---|---|---|
| Q0 | planted: the own Ricci routine finds Painlevé–Gullstrand Schwarzschild Ricci-flat | symbolic |
| Q1 | for g₂ = −2e^{2σ}dp dq with undefined σ(p, q): own Ricci gives R_ab = K g_ab with K = 2σ_pq e^{−2σ}; own □f = −2e^{−2σ}f_pq; and ∂_p∂_q ln R_pq = −(e^{2σ}/2)(□ ln K − 2K) (taking R_pq = −2σ_pq, K > 0 formally) | symbolic |
| Q2 | planar g₂ = −dt² + (dx + b dt)² with undefined b(t, x): own Ricci gives R_ab = K g_ab with K = −a_x, a = b_t − b b_x. For static u(x): K = (uu′)′, and □ ln K − 2K = Θ′ with Θ = (1 − u²)K′/K − 2uu′ | symbolic |
| Q3 | for u_s = 3/(1 + ξ²): the horizons are ξ = ±√2, where α = −uu′ is +2√2/3 and −2√2/3. On each of the three components of {\|u_s\| ≠ 1}, s′ = 2/(1 − u_s²) has one sign, s diverges at both ends, and Φ = K(1 − u_s²) → 0 at both ends (exact limits). At a simple crossing u = 1 + u₁η + u₂η², the leading order of (1 − u²)K′ − (2α + 2uu′)K for K = κη^γ gives γ = −(α + u₁)/u₁ | exact |
| Q4 | re-solve of Theorem E's example. Own RK4 of the geodesics of −2e^{2σ}dp dq, σ = H(p)J(q), from the unit normals of p + q = −2, with the Jacobi equation A_ττ = K A, A(0) = 1, A_τ(0) = 0, to τ = 10, at dt = 0.01 and 0.005, Richardson. L′(10) = ∫A_τ(10, s) ds over s ∈ [−1/√2, 1/√2] by composite Gauss–Legendre (order 10, 16 and 32 panels): \|L′(10) − 4.5\| < 1e-9. Over all nodes and stored steps, min A ≥ 1 − 1e-12 and A_τ ≥ −1e-12. The normalization 2e^{2σ}ṗq̇ = 1 holds to 1e-10. The two spreads (dt, panels) are printed; they are spreads, not enclosures | floating point |
| Q5 | linear order. For b = εB(t, x) with undefined B, the ε⁰ term of C[b] = □ ln K − 2K equals (−∂_t² + ∂_x²) ln K₁, K₁ = −B_tx. For K₁ = F(t − x)G(t + x), ∫K₁ dx = (F ∗ G)(2t). For F = G = u(1 − u)(1 − 2u) on [0, 1] (zero outside), the exact ∫K₁ dx at t = 1/5, 1/2, 4/5 equals (F ∗ G)(2t) at the same points, and F ∗ G ≢ 0 | symbolic + exact |

Mutations, each must exit 1 with its target failing:

| mutation | change | target |
|---|---|---|
| `pg` | √(2M)/r for √(2M/r) | Q0 |
| `null` | K = σ_pq e^{−2σ} (factor 2 dropped) | Q1 |
| `theta` | Θ = (1 − u²)K′/K + 2uu′ | Q2 |
| `alpha` | α at ξ = −√2 expected +2√2/3 | Q3 |
| `rk` | RK4 weights 1, 2, 2, 1 → 1, 3, 1, 1 | Q4 |
| `conv` | expected (F ∗ G)(t) for (F ∗ G)(2t) | Q5 |

## Results

(after the runs)
