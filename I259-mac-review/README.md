# I259-mac-review: the coordinator's review of #259 (the static coefficient c₁ of the c = −1 black universe)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/259. Under review: branch `wip/i259-static-c1`
at 38a08d4 (script fbc5c8f), raw `I259-mac` at f1d02539.

## ind259.py: the static mass mode from closed forms

Written by the coordinator; imports nothing from the repository. The c = −1 member: A = 1 + c(ρ² + 1) + K(ρ + (ρ² + 1) arctan ρ),
K = −2c/π, R = √(1 + ρ²). The static members of #269's family at β = 0: r = √L R, F_L = A + 1/L − 1. From these alone:
- J1 (sympy): F_L at large ρ in the areal radius r = √L ρ is (1/L)(1 − 2M(L)/r + O(r⁻²)) with M(L) = 2L^{3/2}/(3π);
  dM/dL at L = 1 is 1/π.
- J2 (sympy): c₁ = ∂_L r(S) at L = 1 is 1/2, with S at the zero ρ_h(L) of F_L (ρ_h(1) = 0, R'(0) = 0), and κ = A'(0)/2 = 2/π,
  so κ c₁ = 1/π = dM/dL: κ c₁ = δM_ADM for this mode.
- J3 (mpmath, 30 digits): along the family, dM/dL = κ_ξ (dA_h/dL)/(8π) at L = 0.7, 1, 1.3, 2 to 1e-12, with A_h = 4π L R(ρ_h)²
  and κ_ξ = √L F_L'(ρ_h)/2 (the Killing field normalized at infinity, where g_tt → −1/L).

Shared with the runner's code: the closed forms of A, R and the family (from the notes). Not shared: everything else.

Mutations: `no-norm` (κ_ξ without √L: J3 at L ≠ 1), `c1-one` (c₁ = 1: J2), `mass-exp` (M ∝ L in J3: J3).

## Results

| check | verdict | reading (`run_01.log`) |
|---|---|---|
| J1 | met | L F_L = 1 − (4L^{3/2}/(3π))/r + …, so M(L) = 2L^{3/2}/(3π); dM/dL at L = 1 is 1/π |
| J2 | met | c₁ = 1/2, κ = 2/π, κ c₁ − dM/dL = 0 (sympy); dρ_h/dL at 1 = π/4 |
| J3 | met | the first law along the family at L = 0.7, 1, 1.3, 2: worst relative 2.0e-31 |

Mutations: `no-norm` and `mass-exp` fail J3; `c1-one` fails J2.

## Rerun of the runner's script

From a detached worktree at 38a08d4: `static_c1.py derive` (exit 0), `check` (exit 0, 11 of 11) and `table` (exit 0). The derive and
check logs equal the runner's `runs/derive.log`, `runs/check.log` apart from timings; the table equals `runs/table.log`.
