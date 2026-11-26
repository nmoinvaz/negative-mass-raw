# I169-mac: the coordinator's review of #169 (rerun of the default mode, independent check ind169)

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0 (`/Users/nathan/Source/negative-mass/.venv`),
at nice 10 with at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/169. Under review: branch
`wip/i169-sum-products` at 64e6b43, raw `I169-rpi5` at 9af50f6. Stop condition: any single run not finished after 1 h of
wall time is stopped (by its PID) and reported. Written 2026-11-26 before the first run of `ind169.py`.

## Rerun of the runner's default mode

`python3 notes/warp/sum_products.py` from a worktree at 64e6b43: the 13 checks, then the controls.

## ind169.py: what it shares with #169

Shared: sympy; the formula D = h(h² − P² − Q² + Y² + Z²) − P(Y² − Z²) + 2QYZ with P = −(u_x² + u u_xx), Q = −½(u_ρρ +
u_ρ/ρ), Z = ½u_xρ, Y = u_xu_ρ + ½u u_xρ, h = ½u_ρ² (#65, #80, #158; reviewed there); and the claims under test. Not
shared: ind169 imports nothing from the repository; its E, coefficient extraction, ranks and Gröbner calls are its own.

Jets: A_k = X₁^(k), B_k = X₂^(k) (k = 0, 1, 2); a₀, a₁, a₂ = R₁, R₁′, S₁ = R₁″ + R₁′/ρ and b₀, b₁, b₂ likewise;
u = A₀a₀ + B₀b₀ + v, u_x = A₁a₀ + B₁b₀, u_xx = A₂a₀ + B₂b₀, u_ρ = A₀a₁ + B₀b₁, u_xρ = A₁a₁ + B₁b₁, u_ρρ + u_ρ/ρ = A₀a₂ +
B₀b₂. E = 8D.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| J1 | E is a polynomial of 376 terms in the 12 jets and v, and E at B₀ = B₁ = B₂ = 0 is divisible by a₁² exactly |
| J2 | Compact form: 4hD = C² − A² − B² with A = 2hP + Y² − Z², B = 2hQ − 2YZ, C = Y² + Z² + 2h², for abstract P, Q, Z, Y, h, exactly |
| J3 | Exact separation ranks: the matrix of E's coefficients (x-monomials in A_k, B_k × ρ-monomials in a_k, b_k) has rank 59 at v = 0 and 93 at v = 1/3 |
| J4 | Theorem K's coefficient: with a₂ = (γ + ι)a₁ + δa₀, b₂ = (γ + ι)b₁ + δb₀, E is a polynomial of degree 2 in ι with ι² coefficient −u_ρ⁴, exactly |
| J5 | Theorem E's top coefficient: with A_k = k₁^k z₁ and B_k = 0, the coefficient of z₁⁶ in E is a₁²(a₁² + 4k₁²a₀²)(a₁² + 5k₁²a₀²), exactly |
| J6 | Theorem E's unit ideals. With a₀ = c₁, a₁ = a₂ = 0, A_k = k₁^k z₁, B_k = k₂^k z₂: E = z₂²b₁²E″ exactly. (a) The coefficients of the monomials z₁^iz₂^j of E″, with t·c₁k₁k₂(k₁ − k₂)b₁ − 1, have reduced Gröbner basis [1] over ℚ. (b) ind169's own list of resonant ratios q = k₁/k₂ (two monomials of E″ with iq + j = i′q + j′, \|q\| ≥ 1, q ≠ 1) equals {−2, −1, 4/3, 3/2, 2, 3, 4}. (c) For each, the coefficients summed by frequency at k₁ = qk₂, with t·c₁k₂b₁ − 1, have basis [1] |
| J7 | Planted: the additive u = cx + g(ρ) (X₁ = x, R₁ = c, X₂ = 1, R₂ = g), g = −ε ln ψ with ψ″ = −ψ′/ρ − 2c²ψ, gives E = 0 identically for ε = ±1 and symbolic c; and g + ρ²/10 in place of g gives E ≠ 0 at the exact point (c, ε, ψ, ψ′, ρ) = (1/2, 1, 1, 1/3, 2) |

Read and rederived by hand by the coordinator, not coded: Lemmas 1–4, Theorem K's frequency argument (both root cases),
Theorem E's steps (1)–(3).

## Mutations (`--mutate=NAME`; each must make ind169 exit non-zero with exactly these criteria failing)

| mutation | change | targets |
|---|---|---|
| `j1-v0` | J1 builds E with v = 0 | J1 |
| `j2-sign` | J2 with B = 2hQ + 2YZ | J2 |
| `j3-claim` | J3 expects 59 at v = 1/3 | J3 |
| `j4-iota` | J4 with a₂ = γa₁ + δa₀ (ι dropped) and the same for b₂ | J4 |
| `j5-factor` | J5 expects a₁²(a₁² + 4k₁²a₀²)² | J5 |
| `j6-undivided` | J6 (a) uses the coefficients of E itself, and no saturation generator | J6 |
| `j7-freq` | J7 with ψ″ = −ψ′/ρ − c²ψ | J7 |

## Runs (filled in as they are done)
