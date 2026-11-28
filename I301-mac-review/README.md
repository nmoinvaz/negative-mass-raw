# I301-mac-review: the coordinator's review of #301 (κ r_S c₁ = δM_ADM at c = −1.5, −0.3 and Schwarzschild)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/301. Under review: branch `wip/i301-c1-members` at
167e537 (script cde8be5), raw `I301-mac` at 38d5d4c5.

## ind301.py: the static mass mode at three members from closed forms

Written by the coordinator; imports nothing from the repository (it extends ind259). For c = −1.5, −0.3 (A = 1 + c(ρ² + 1) +
K(ρ + (ρ² + 1) arctan ρ), K = −2c/π, R = √(1 + ρ²)) and Schwarzschild (A = 1 − 1/ρ, R = ρ), with r = √L R, F_L = A + 1/L − 1:
- J1 (sympy, c symbolic): F_L in the areal radius gives M(L) = (K/3) L^{3/2}, so dM/dL at L = 1 is K/2; Schwarzschild: M = L^{3/2}/2.
- J2 (mpmath, 30 digits): c₁ = ∂_L r(S) with the horizon's shift (dρ_h/dL = 1/A′(ρ_h)), κ = A′(ρ_h)/2, r_S = R(ρ_h):
  κ r_S c₁ = dM/dL to 1e-25 at the three members; with r_S set to 1 it misses at c ≠ −1.
- J3: the first law along each family, dM/dL = κ_ξ (dA_h/dL)/(8π), κ_ξ = √L F_L′(ρ_h)/2, at L = 0.7, 1.3 to 1e-12.
- J4 (reported): κ R_h² + R_h R′_h equals K, the static constant ½(R²A′ − 2ρA) + ρ at the horizon (the hand proof of
  κ r_S c₁ = K/2).

Mutations: `no-shift` (dρ_h/dL = 0: J2), `rs-one` (r_S = 1: J2 at c ≠ −1), `no-norm` (κ_ξ without √L: J3).

## Results

| check | verdict | reading (`run_01.log`) |
|---|---|---|
| J1 | met | black universes: M(L) = −2c L^{3/2}/(3π) = (K/3) L^{3/2}, dM/dL = −c/π = K/2; Schwarzschild: M(L) = L^{3/2}/2, dM/dL = 3/4 |
| J2 | met | κ r_S c₁ = dM/dL to 2e-31 at c = −1.5, −0.3 and Schwarzschild; with r_S = 1 it misses by 5.3e-2 and 0.267 (c = −1.5, −0.3), and not at Schwarzschild 2M = 1, where r_S = 1 (the runner added 2M = 2 for that reason) |
| J3 | met | the first law along each family at L = 0.7, 1.3 to 2e-31 |
| J4 | reported | κ R_h² + R_h R′_h equals the static constant ½(R²A′ − 2ρA) + RR′ at the horizon exactly: κ r_S c₁ = K/2 is that constant's value |

Mutations: `no-shift` and `rs-one` fail J2; `no-norm` fails J3.

## Rerun of the runner's script

From a detached worktree at 167e537: `derive`, `check` and `table` exit 0, and their logs equal the runner's `runs/` logs apart from
timings.
