# I77-mac: the coordinator's review of #77's test of three mixed-sign scalars on the Alcubierre wall

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2
processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/77. Reviewed branch `wip/i77-three-scalars` at 12e13c0
(`three_scalars.py` sha256 39aa2bc4…) and raw `I77-rpi5` at d1880b5.

## Rerun of the runner's script

`python3 notes/warp/three_scalars.py`, full, with its 20 controls, from a detached worktree of 12e13c0 (`rerun/`).

## Independent check `ind77.py` (criteria written before its first run)

ind77 imports nothing from the repository: no `three_scalars.py`, `two_scalars.py` or `phantom_source.py`, so no
`form3`, `closure3`, `ricci_pt`, `lie_numeric`, frame Ricci tensors or jets. It has its own Christoffel and Ricci
routine for a metric in coordinates. It works in comoving polar coordinates (t, r, θ, ϕ) with a generic w(r) (a sympy
Function), where the wall reads ds² = −dt² + (w dt + cos θ dr − r sin θ dθ)² + (sin θ dr + r cos θ dθ)² + r² sin²θ dϕ²,
w = v(1 − f). That is #77's lab metric, with x − vt = r cos θ and ρ = r sin θ; the coordinate change is the
coordinator's. The quotient block h is the (t, r, θ) block of the coordinate Ricci tensor. Ric(h) comes from its own
3D formula on the values of h and its first and second derivatives. The kernel and the λ ≠ 0 roots use the 4D
coordinate matrices R_μν and g_μν. dλ comes from Jacobi's formula, dK from the bordered system (dN) K + N dK = 0,
Kᵀ dK = 0, and L_K M from its coordinate formula, all at 60 digits. #77 used central differences instead. The
accelerating bubble uses a second route: Cartesian (t, x, y, z) with a polynomial shift, its Taylor series truncated
at degree 4 around the point (a sympy PolyRing), and the 3D block on z = 0.

Shared with #77: the metric, the frame (n = ∂_t − b∂_x, ∂_x, ∂_ρ), the profiles (tanh σ = 8, R_b = 1; the bump
(1 − r²/4)³), #77's point lists (copied from `three_scalars.py`), the polynomial q printed in `wall_D` (read from
`rpi5_output.txt`), and the claims tested.

| id | criterion | kind |
|---|---|---|
| B0 | planted, own Ricci routine: Painlevé–Gullstrand Schwarzschild is Ricci-flat. #77's P1 (a = l, λ = 0, κ² = 2, signs (+,−,−) of (t, X, Y)) and P2 (a = cosh l/√2, λ = −3, κ = 1, signs (−,+,+)) in the sheared coordinates t = T + L/3, Θ = Th + L/5, l = L give R_μν = λ g_μν + κ² Σ_I s_I ∂_μX^I ∂_νX^I exactly, with X = (t, R cos Θ, R sin Θ) | symbolic |
| B1 | planted, own 3D Ricci and L_K M routines. Ric = 0 for −dt² + dR² + R²dΘ². Ric = diag(0, 1, sin²θ) for −dt² + dθ² + sin²θ dϕ² at cos θ = 3/5. Ric = 0 for the quotient blocks of P1 and P2 (slice T = const) at 3 exact points. Ric ≠ 0 for D1's block (fiber R²(1 + R²/10)dΘ²) at those points. At the simple root λ = −3a″/a: L_K M = 0 (relative < 1e-30) for P2, and ≠ 0 (relative > 1e-8) for D2′ (a = 1 + L²/2). (L_K M)(K, ·) = 0 (relative < 1e-30) in both | symbolic + 60 digits |
| B2 | the wall, own route: R_ϕμ = 0 for all μ; R(E₀,E₀) + R(E₁,E₁) + 2R(E_ρ,E_ρ) = 0; and 16 r³ det R₃ − (1 − c²) q(c²) = 0 mod s² + c² − 1, with R₃ the frame block on (E₀, E₁, E_ρ), W0, W1, W2 = w, w′, w″, and q as printed in `wall_D` | symbolic |
| B3 | λ = 0 at the off-axis points. λ = 0 is a root, ∂_ϕ spans the kernel, and h is nondegenerate. The inertia of R_μν is (2,1) where 16r³ det R₃ < 0 and (1,2) where it is > 0: pattern A at the 3 bump points (v = 7/4) and B at the 18 tanh points, as #77 prints. Ric(h) ≠ 0 at the 3 bump points and at the 18 points of the explicit bump (v ∈ {1, ½, 7/4}, r ∈ {1, 3/2}, (c, s) ∈ {(3/5, 4/5), (5/13, 12/13), (−4/5, 3/5)}), exactly. Ric(h) ≠ 0 at 4 points of the coordinator's own random rational jets (seed 2026), exactly, and at the 18 tanh points (relative > 1e-8, 60 digits) | exact + 60 digits |
| B4 | λ ≠ 0 at the 21 non-random off-axis points (3 bump, 18 tanh). The number of real roots λ ≠ 0 of rank 3 with an admissible inertia is 1 at each point, 21 in all, as #77 prints. Each pattern-A root has λ < 0 and each pattern-B root λ > 0. L_K M ≠ 0 at every one (relative > 1e-8), and (L_K M)(K, ·) = 0 at every one (relative < 1e-30). K(λ) = 0 (relative < 1e-30) at the 4 roots with c = 0 (the bump point (0, 3, 4)/5 and the tanh point (0, 5, 12)/13 at its 3 speeds). K(λ) ≠ 0 (relative > 1e-8) at the other 17 | 60 digits |
| B5 | the accelerating bubble, Cartesian route: b = −v_s(t)(1 − Q/4)³, Q = (x − x_s(t))² + y² + z², v_s = 1 + t/2 + t²/3, x_s = t + t²/4 + t³/5. At 3 exact points (t, x, y, 0) with y > 0 and Q < 4: R_zμ = 0, and Ric(h) ≠ 0 for the (t, x, y) block, exactly. Cross-check of the two routes: at constant speed (v_s = 1, x_s = t), the scalar curvature of h at (0, 3/5, 4/5, 0) equals the polar route's at r = 1, (c, s) = (3/5, 4/5) with the bump at v = 1, exactly | exact |

Mutations, each must exit 1 with its target failing:

| mutation | change | target |
|---|---|---|
| `pg` | √(2M)/r for √(2M/r) in the planted metric | B0 |
| `p2lam` | λ = −2 in P2's identity | B0 |
| `sph` | expected R_θθ = 2 on the sphere | B1 |
| `d2shell` | D2′'s warp factor set to cosh L/√2 | B1 |
| `qtyped` | W0³W1³c⁴ added to the parsed q | B2 |
| `flat` | h replaced by diag(−1, 1, r²) in B3 | B3 |
| `nodk` | the ∂K terms dropped from L_K M | B4 |
| `refl` | the 4 equator roots replaced by the same points at (c, s) = (3/5, 4/5) in the K(λ) = 0 test | B4 |
| `xcheck` | the Cartesian cross-check point moved to x = 3/5 + 1/50 | B5 |
| `accflat` | the accelerating block replaced by diag(−1, 1, 1) | B5 |

## Results

Written after the runs.
