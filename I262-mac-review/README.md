# I262-mac-review: the coordinator's review of #262 (the c = −1 mode in closed form, and dW/dc)

Machine: the coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/262. Branch
`wip/i262-cminus1-mode` at 43d0d08, raw `I262-mac` at 06b4cb04.

## Criteria, written before any run

**Rerun (R).** `cminus1_mode.py` (its default run) in a detached worktree: 13 of 13 checks, as in the output of record.

**Independent check (`ind262.py`).** The claim: for every member, Y = R e^{Kt} e^{Kx} with K = −2c/π solves the linear radial problem
exactly. That would make the c = −1 mode (K = κ) Y = c₂ V R. Checked in the coordinator's own forms of the double-null equations
(ind217's r_uv, F_uv, φ_uv and the two null constraints, verified against a brute-force Ricci tensor). Static null coordinates
u = t − x, v = t + x, metric −A du dv (e^{−F} = A/2), every background function explicit in ρ (A, R = √(1 + ρ²), φ = √2 arctan ρ, the
BF06 potential). Gauge δφ = 0, so Y = δr. The perturbation is δr = R(ρ) e^{Kv} and δF = h(ρ) e^{Kv}, with h from the linearized
φ_uv equation, which is algebraic in h. Shares nothing with `stability.py`, `cminus1_mode.py` or the master equation.

| check | what | pass |
|---|---|---|
| K1 | the remaining four linearized equations (r_uv, F_uv, C_uu, C_vv) at that h | each residual simplifies to 0 for symbolic c; if sympy cannot simplify, below 1e-25 at c = −1, −0.3, −1.5, −10, ρ at 8 points each (30 digits) |
| K2 | the same at c = −1 with the closed form's W = κ | as K1 |

Mutations, each with the check it must fail:
- `w-off`: the rate K(1 + 1e-3) in place of K. K1 must fail (residuals of order 1e-3 of the terms).
- `r-to-rho`: δr = ρ e^{Kv} in place of R e^{Kv}. K1 must fail.
- `k-kappa`: K replaced by κ(c) = A′(ρ_h)/2 at c = −1.5. K1 must fail at c = −1.5, where κ ≠ K.

## Amendment A1 (after run 1, before any change to the claim's test)

Run 1 (`ind262_run1.txt`): K0 passes (the background solves the five equations to 2e-39), and K1 and K2 fail with O(1) residuals. The
defect is the check's. It imposed δφ = 0 together with the double-null form, which is three gauge conditions for two gauge
functions. In double-null gauge δφ is not zero in general, so the residuals test an over-determined ansatz, not the claim.

Replacement, written before its first run. The static gauge δg_tρ = 0 and δφ = 0 is reachable: ξ^ρ sets δφ = 0 because φ′ ≠ 0, and
ξ^t sets δg_tρ = 0. Then
ds² = −A(1 + H₀) dt² + (1 + H₂) dρ²/A + (R + Y)² dΩ², with Y the gauge-invariant δr − (ρR/√2) δφ.

The linearized equations come from a brute-force Ricci tensor (R_ab = ε φ_a φ_b + V g_ab, ε□φ = V′). The perturbation is
Y = R Q e^{Kt}, H₀ = a Q e^{Kt} and H₂ = b Q e^{Kt}, with Q = e^{Kx}, so Q′ = K Q/A. The steps:
1. E_tρ gives b.
2. The scalar equation and E_ρρ give a and a′.
3. Consistency (a′ against d a/dρ) and E_tt and E_θθ are the residuals.

K1b passes if every residual is below 1e-25, relative to its largest term, at the members and points of K1. Same mutations.

**A2 (after ind262b's run 1).** ind262b's run 1 was stopped after 40 minutes in sympy's expansion of the explicit background. It
printed no residual, so it is not a result (`ind262b_run1.txt`). `ind262c.py` is the same check: the same equations, gauge,
unknowns, solve order, members, points, bar and mutations. The background functions A, R, P, V(P) and V′(P) are abstract in the
algebra, and their derivatives are evaluated at each point from the explicit forms by mpmath at 40 digits.

**A3 (after ind262c's run 1, a crash).** E_ρρ contains a″, which the first solve order left as a free symbol, so the scale evaluation
crashed (`ind262c_run1.txt`, no residual printed). Fix: a″ is the total derivative of the scalar equation's a′ = a′(ρ, a), with a′
substituted again, and then E_ρρ is solved for a. The checks, points and bars are unchanged.

**A4 (after ind262c's run 3).** Run 3 gave about 1e-36 at c = −1, −1.5 and −10, and 1.11e-14 at c = −0.3, which does not fall at
80 digits. The cause is the check's: it took W = −2 float(c)/π, and float(−3/10) is 1e-17 from the exact −3/10 the algebra
substitutes, so W − K ≈ 1e-17 there. The residual is proportional to W − K. The values at the other members are exact in binary. Fix:
W and κ come from the exact rational c. Nothing else changes.

## Results

| check | result | verdict |
|---|---|---|
| R | `derive` 4 of 4, `check` 9 of 9, `table`: every verdict line equal to the output of record (one timing differs) | pass |
| K0 | the background solves the five equations at 4 members × 4 points: 2.2e-39 | pass |
| K1b (`ind262c_run4.txt`) | at W = K the equations E_ρρ, E_tt and E_θθ become independent of H₀'s amplitude a, and all residuals vanish: c = −1 4.1e-36, −0.3 3.9e-38, −1.5 3.8e-37, −10 1.2e-32 (relative, 40 digits; 2e-76 at 80 digits) | pass |
| K2 | c = −1, K = κ: 4.1e-36 | pass |
| `w-off` | 1.0 at every member | fires |
| `r-to-rho` | 1.0 at every member | fires |
| `k-kappa` | 1.0 at c = −0.3, −1.5, −10; passes at c = −1, where κ = K, as predicted | fires |

Run history: run 1 of `ind262.py` failed from the over-determined gauge (A1). `ind262b.py` was stopped (A2). `ind262c.py` run 1
crashed (A3), and run 3 failed at c = −0.3 from float(c) (A4). Run 4 is the result. Every log is kept.

Reading: the closed form is confirmed by a derivation that shares no code with `cminus1_mode.py`, `stability.py` or the master equation.
Y = R e^{K(t+x)} with K = −2c/π solves the linearized Einstein–scalar equations for every member tested. At W = K the amplitude of
H₀ drops out of the remaining equations, so the solution is determined up to a free H₀ multiple.
