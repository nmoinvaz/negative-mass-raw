# I157-mac: the coordinator's review of #157's ideal step for three mixed-sign scalars

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, at nice 10 with at most 2 processes. No
Singular on this machine. Issue: https://github.com/nmoinvaz/negative-mass/issues/157. Reviewed branch
`wip/i157-three-scalars-ideal` at 41ed7f8 and raw `I157-rpi5` at 0053c30.

## Rerun of the runner's script

`python3 notes/warp/three_scalars_ideal.py --raw=<this repository>/I157-rpi5`, the default mode (checks, planted cases,
stored certificates, the 9 controls; no Singular), from a detached worktree at 41ed7f8. Output: `rerun_default.txt`.

## Independent check `ind157.py` (criteria written before its first run)

ind157 imports nothing from `three_scalars.py` or `three_scalars_ideal.py`. It writes the wall metric in Cartesian
coordinates, g = −dt² + (dx + w dt)² + dρ² + ρ² dϕ², w = w(R), R = √(x² + ρ²), with the chain rule through R on symbols
w0..w6. Its 4D Christoffel and Ricci code is its own, and h is the (t, x, ρ) block of Ric(g) (λ = 0, K = ∂_ϕ). Its
numerator det(h)² Ric(h) is assembled at a point from h, ∂h, ∂²h with the adjugate. The result is turned into #157's polar
components (t, r, θ), with N_ab = det_polar(h)² Ric(h)_ab and det_polar = R² det_cart. Jets u_k = r^k w^(k); at r = 1,
u_k = w_k. "On L" means 2u0 = u1 and u1 + u2 = 0, with u1, u3, u4 free symbols. "mod circle" means reduced modulo
S² + c² − 1, c = cos θ, S = sin θ.

Shared with #157: sympy 1.14.0, the definition of the wall metric (the same as `ind77.py`'s and #157's `num_indep`), and
the claims tested below, copied from #157's note and output (the locus L, the exact point of R1, the form of H, the weights
m, the ODE lemma).

| id | criterion |
|---|---|
| P1 | Ric(g)(∂_ϕ, ·) = 0 at 3 random exact points, and Ric(g) = 0 for constant w (planted flat) |
| P2 | the point numerator of the Rindler metric −X² dT² + dX² + dY² (flat) at X = 2 is 0 (planted flat) |
| P3 | the point numerator of the stereographic unit 3-sphere 4δ/(1 + \|y\|²)² at y = (1/2, 1/3, 1/5) equals 2 det(h)² h (planted, Ric = 2h) |
| C1 | det h on L is 0 mod circle, and det h at u = (1/3, 2/7, −1/5), c = 3/5 is not 0 |
| C2 | N_θθ on L is 0 mod circle |
| C4 | on L, some N_ab other than N_θθ is not 0 mod circle. Prediction from #157's mod-p probe that J_all (R3) is the unit ideal |
| C3 | at #157's point u = (2/5, 1, −2/5, −83/75, 0) and θ = π/2, all six N_ab and det h are 0 (re-solve of R1's certificate) |
| C5 | H at 3 random specialized (u1, u3, u4), u1 ≠ 0: N_θθ mod circle is divisible by (1 − c²)³, and the coefficients of N′_θθ in (c, S) have the reduced lex Gröbner basis in Q[u0, u2] of (2u0 − u1, (u1 + u2)²). Evidence for H at those points only, not H |
| C6 | sympy's `dsolve` of 2w = r w′ gives w = C r²; then r w′ + r² w″ vanishes on an interval only for C = 0, which forces w′ = 0 (the ODE step without Singular) |
| C7 | N_ab(r0; W) = r0^m N_ab(1; r0^k W_k) exactly at r0 = 2 and 3/2 with random jets, m = −10, −10, −9, −10, −9, −8 for tt, tr, tθ, rr, rθ, θθ. m is derived by hand from the homothety (t, x, ρ) → r0 (t, x, ρ), under which h pulls back to h: N scales by r0⁸ times one power of r0 for each index t or r |

Mutations, each must exit 1 with its target failing:

| mutation | change | target |
|---|---|---|
| `det-L` | L with u1 − u2 = 0 | C1 |
| `ric-sign` | the Γ Γ terms of the point numerator change sign | P3 |
| `point` | u3 of the R1 point increased by 1 | C3 |
| `ode` | the second relation r w′ − r² w″ = 0, which w = C r² satisfies | C6 |
| `H-b` | the expected basis that of (2u0 − u1, u1 + u2) | C5 |
| `weight` | m = −9 for θθ | C7 |

Before writing these criteria the coordinator checked one property of the machinery, not a criterion: the entries of h
have denominators 2R³ and 2R² only, so the reduction mod circle applies to the point values.
