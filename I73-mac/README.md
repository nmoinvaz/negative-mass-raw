# I73-mac: the coordinator's review of #73's Hawking–Ellis type map of the accelerating bubble

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, numpy 2.5.4, scipy 1.18.1, at nice 10 with at
most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/73. Reviewed branch `wip/i73-he-accel` at d9b2df0 (`he_accel.py`
sha256 5611b27b…) and raw `I73-rpi5` at 800e25e.

## Independent check `ind73.py` (criteria written before its first run)

ind73 imports nothing from the repository. It does not use `phantom_source.py` or `he_type.py`: no `ricci`, no jets, no
`cubic` or `disc`, no `tanh_jets`, no grids. It has its own Christoffel and Ricci routine for a metric given in
coordinates, run on a generic shift b(t, x, y, z) (a sympy Function). The derivatives of b at the point come from its own
chain rule through Q = r_s²: f(r_s) = G(Q) with G′ = f′/(2r), G″ = f″/(4r²) − f′/(4r³), with polynomial 2-jets of v_s,
x_s and G, so v_s″ and x_s″ are free symbols. The characteristic polynomial is sympy's `charpoly` of ηR and the
discriminant is sympy's `discriminant`. The map uses numpy's eigenvalues of ηR, not D.

Shared with #73: the metric ds² = −dt² + (dx + b dt)² + dy² + dz², b = −v_s(t) f(r_s), the frame (n = ∂_t − b∂_x, ∂_x,
∂_y, ∂_z) at z = 0, y > 0, Alcubierre's tanh profile, the parameters of Le's and Rodal's walls, and the printed claims of
`he_accel.md` (typed here from the note) that are tested.

Notation: v = v_s, α = v_s′, u = x_s′, β = v_s″, w = x_s″, f, f₁ = f′, f₂ = f″, c = cos θ, s = sin θ. An identity "mod s²"
means the numerator's remainder on division by s² + c² − 1 in s is 0.

| id | criterion | kind |
|---|---|---|
| A0 | planted, own Ricci routine: Schwarzschild in Painlevé–Gullstrand form ds² = −dt² + (dr + √(2M/r) dt)² + r²dΩ² gives R_μν = 0; de Sitter ds² = −dt² + e^{2Ht}(dx² + dy² + dz²) gives R_μν = 3H²g_μν; both exact after `simplify` | symbolic |
| A1 | the frame block of own Ricci at the point equals the six printed entries (R_00 = T_x − A, R_01 = j₁, R_0ρ = j_ρ, R_11 = A − q − T_x, R_1ρ = B − T_ρ/2, R_ρρ = q/2, with T_x, T_ρ, A, B, q, j₁, j_ρ as printed in "Answer"), mod s², as rational functions of (v, α, u, β, w, f, f₁, f₂, r, c, s); R(e_ϕ, ·) = 0; β and w do not appear in the block | symbolic |
| A2 | for a generic real symmetric block with R_11 = −R_00 − 2R_ρρ, sympy's discriminant of the charpoly of ηR equals the printed D(j₁, j_ρ, q, h, p), with q = 2R_ρρ, h = R_1ρ, p = R_ρρ + R_00; expanded in (j₁, j_ρ, q, h, p) it has 52 terms, degree 4 in p, is homogeneous of degree 6, and has j-degrees 0, 2, 4, 6 only; the j-degree 6 part is −4(j₁² + j_ρ²)³ and the j-degree 0 part is (pq + h²)²[(p + q)² + 4h²] | symbolic |
| A3 | D_b, the discriminant of A2 at A1's own entries, reduced mod s²: (a) at v = 0, D_b = α⁶f₁⁶s⁴/16; (b) at c = ±1, s = 0, D_b = −4j₁²(R_00² + j₁²)² with j₁ = v f₁/r; (c) degree 6 in α with α⁶ coefficient f₁⁶s⁴/16; (d) as a polynomial in (v, α, u) it has 50 monomials v^i α^j u^k, every one with i + k + 2j ∈ {6, 8, 10, 12} and k ≤ i, and the highest powers are v¹², α⁶, u⁶; (e) D_b(v, −α, u; −c, s) = D_b(v, α, u; c, s); (f) at c = 0, s = 1, α = 0, D_b = (q² − 4j₁²)(p² + pq + j₁²)² with q² − 4j₁² = v²[v²f₁⁴ − (f₁ + r f₂)²/r²], for every u | symbolic |
| A4 | Le's wall (σ = 8, R_b = 1, f ∈ [0.1, 0.9]): own root-finding gives r_s ∈ [0.8627, 1.1373] to 4 decimals. The Type I fraction of the proper volume (r² sin θ dr dθ, midpoint rule 1200 × 1200 in (r_s, θ)), with Type I where numpy's eigenvalues of ηR are all real (max \|Im λ\| ≤ 1e-8 max\|ηR\|), equals the printed value within 0.10 percentage points at each of the 12 rows below | numerical |
| A5 | Rodal's equator (σ = 4, ρ = 5, θ = π/2, v = u = 1, r_s ∈ [4.25, 5.75]): the sign changes of the float64 cubic discriminant of ηR (coefficients from the trace, the principal minors and the determinant, own code), found on 30 001 radii and refined by brentq, give Type I intervals whose number equals the printed one and whose ends are within 2e-4 of the printed ones, at α = 0, 0.5 and 4 | numerical |

Rows of A4 (printed in `he_accel.md`):

| wall | v | α | u | printed Type I % |
|---|---|---|---|---|
| Le | 0.5 | 0 | 0.5 | 1.15 |
| Le | 0.5 | 2 | 0.5 | 11.99 |
| Le | 0.5 | −2 | 0.5 | 11.99 |
| Le | 0.5 | 32 | 0.5 | 93.92 |
| Le | 1 | 4 | 1 | 10.55 |
| Le | 2 | 8 | 2 | 15.19 |
| Le | 0.5 | 0 | 0 | 2.50 |
| Le | 0.5 | 0 | 2 | 19.42 |
| Le | P1, t = −0.6 | | | 8.597 |
| Le | P1, t = 0.9 | | | 10.641 |
| Le | P1, t = 0.9, α = 0, u = v | | | 0.045 |
| Rodal band [4.25, 5.75] | 1 | 4 | 1 | 26.24 |

P1 is v_s = sech²(2t), x_s = tanh(2t)/2, so α = −4 sech²(2t) tanh(2t) and u = v; ind73 computes these itself.

Rows of A5: α = 0: [4.9458, 5.0660]; α = 0.5: [4.9438, 4.9656], [4.9945, 5.0191], [5.0509, 5.0683]; α = 4: [4.8981,
5.1036].

Mutations, each must exit 1 with its target failing: `pg` (√(2M)/r for √(2M/r) in the planted metric; A0), `w2` (b²
dropped from g_tt; A1), `tx` (the sign of the v u term of the typed T_x flipped; A1), `disc27` (−26c₀² for −27c₀² in the
typed D; A2), `axis` (+4 for −4 in the typed axis form; A3), `map` (α set to 0 in the map; A4), `rodal` (α = 0 used for
the α = 4 row; A5).

## Rerun of the runner's script

`python3 notes/warp/he_accel.py`, full, with its 13 controls and `phantom_source.py --mutate=accel-static`, from a detached
worktree of d9b2df0.

The first attempt exits 1 after 37 s with FileNotFoundError: `finish()` opens `/proc/self/status`, which macOS does not
have. All 13 checks had printed PASS before the crash, and no control ran. That attempt's files are in `rerun/attempt1/`.

The second attempt uses a local copy with that one read guarded (`rerun/mac_proc_patch.diff`), and nothing else changed.
