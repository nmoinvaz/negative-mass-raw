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
