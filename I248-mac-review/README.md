# I248-mac-review: the coordinator's review of #248 (c₂ of the c = −1 black universe is free in regular Cauchy data)

Machine: the coordinator's Mac (Apple M5, macOS), nice 10, at most 2 processes. Issue:
https://github.com/nmoinvaz/negative-mass/issues/248. Branch `wip/i248-horizon-sector` at 0dd8c98 (worktree `negative-mass-r248`,
detached), raw `I248-dh610` at 88ac882. Python `~/Source/negative-mass/.venv/bin/python`.

## Criteria, written before any run

**Rerun (R).** `rerun.sh`: `horizon_sector.py derive`, `check`, `table` in the worktree. Pass: derive 8 of 8 and check 11 of 11, as
on dh610, and the class table's c₂ for class L equal to the note's −9.610862e-04 in its printed digits.

**Independent check (`ind248.py`).** c₂ of class L by transport along the data ray, a computation that uses no 2D solver and none of
#248's or #232's code.

- On the ray V = V_L = −0.05 the data are known: δφ(U) is class L's pulse (amplitude 1e-3, centre U = 0, width 0.3, minus its value at
  U = −2), δF = 0, and δr from the linearized constraint C_UU, δr'' = r φ′ δφ′ − F′ δr′ + ½ φ′² δr, with δr = δr′ = 0 at U = −2.
- The data on the other ray U = −2 vanish, so the transverse derivatives P = (δr_V, δF_V, δφ_V) vanish at the corner. Along the ray,
  ∂_U P is the linearization of the evolution equations r_VU, F_VU, φ_VU in the coordinator's forms (verified against a brute-force
  Ricci tensor in `I217-mac-review/ind217.py`, K1), with ε = −1 and the potential of #212's member. P is integrated from U = −2 to 0.
- c₂ = δr_V(V_L, 0), because the law δr_VV = 0 on U = 0 makes ∂_V δr the same everywhere on the horizon line.
- Background: Π = −VU, Π(ρ) = ρ exp(2κ ∫₁^ρ (1/A − 1/(2κρ′)) dρ′), so Π = 1 at ρ = 1, as #248's chart. G = dρ/dΠ, e^{−F} = G/κ,
  r = √(1 + ρ²), φ = √2 arctan ρ. The ray runs through Π ∈ [−0.1, 0], inside the horizon (ρ < 0). It is computed in mpmath at 30 digits,
  with the ODE by RK4 at two step counts.

Shared with the code under test: the member (A(ρ), the potential), the chart's normalization Π(ρ = 1) = 1, class L's definition and
the gauge δF = 0 on the data rays. Nothing else.

| check | what | pass |
|---|---|---|
| K0 | self-convergence: c₂ at 4000 and 8000 RK4 steps | relative difference ≤ 1e-10 |
| K1 | c₂ of class L against the note's −9.610862e-04 (fit of the 2D solution, Richardson) | relative difference ≤ 1e-6 |
| K2 | pure gauge on the ray: data δr = ζ r_U, δφ = ζ φ_U, δF = F_U ζ − ζ′ with ζ = 1e-3 (1 + tanh((U + 1)/0.2))/2. The transported P against the exact transverse derivatives (ζ r_UV, ζ φ_UV, ζ F_UV) along the whole ray | max \|P − exact\| / max \|exact\| ≤ 1e-8, and \|c₂\| ≤ 1e-12 (r_UV = 0 on U = 0 at c = −1) |

Mutations (`--mutate=`), each with the checks it must fail:

- `eps-sign`: ε = +1 in the evolution equations and the constraint. K2 must fail (the gauge transform of the member no longer solves the
  linearized equations of a different theory), and K1 must fail.
- `no-pot`: the potential's terms dropped from the evolution equations. K2 and K1 must fail.
- `pulse-centre`: class L's pulse centred at U = 0.01 instead of 0. K1 must fail (c₂ depends on the data near the crossing); K2 is
  unaffected.
