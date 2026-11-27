# I217-mac-review: the coordinator's review of #217 (rerun, independent check ind217)

Machine: macOS (the coordinator's Mac, Apple M5), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`: numpy 2.5.4,
scipy 1.18.1, sympy 1.14.0, numba 0.68.1), nice 10, at most 2 processes. Issue:
https://github.com/nmoinvaz/negative-mass/issues/217. Under review: branch `wip/i217-black-universe-evolution` at 45c261d
(code 9428081), raw `I217-mac` at 059c235. Written 2026-11-27 before the first run of `ind217.py` and before the rerun.

## Rerun

From a detached worktree `~/Source/negative-mass-r217` at 45c261d, in `notes/black_universe`:
- `evolve.py check`;
- `evolve.py analyze --raw=<I217-mac>/runs`;
- one job of record again, `evolve.py job --c=-1.5 --h=0.005`, compared with the runner's.

The expectation, written now: `check` gives 10 of 10. `analyze` prints `evolve_output.txt` again (rc 1: E11 and XC at
c = −1.5 not met) apart from paths and timings. The job's A*ₕ equals the runner's within 1e-13, and its series points with
|A − A*| ≥ 1e-7 have the runner's fate and departure time to 1e-9.

## ind217: the equations with V and the static member, by the coordinator's own derivation

- **K1.** The coordinator's brute-force Ricci tensor (Christoffels from the metric matrix, as in the review of #39) for
  ds² = −2e^{−f}du dv + r²dΩ₂², with R_μν − ε∂_μφ∂_νφ − V(φ)g_μν = 0 and ε□φ = V′(φ), V a generic sympy function. It
  solves R_uv, R_θθ and □φ for r_uv, f_uv and φ_uv. Then:
  - symbolically, against `evolution_design.md` §1's printed forms;
  - numerically, against `evolve.F_np` (the code under test) at 20 random states for each of c = −0.3, −1.5 and −1, with V
    and V′ from `evolve_potential.pot` (the potential is shared, declared).
- **K2.** The closed-form static member, e^{−f} = A(ρ), r = R(ρ), φ = √2 arctan ρ with dρ/dx = A, x = (x⁺ − x⁻)/√2, put into
  K1's three evolution equations and the two null constraints. The coordinator's own expressions are used, at 30 digits
  (mpmath), at 10 points ρ in the static region for each of c = −0.3, −1.5 and −1.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | sympy residual 0 against the printed forms for r_{+−}, f_{+−} and φ_{+−}; `evolve.F_np` agrees with K1's expressions to 1e-12 relative at 60 states |
| K2 | the five residuals on the member are below 1e-25 at the 30 points |

## Mutations (`--mutate=NAME`; each must make ind217 exit non-zero with exactly these criteria failing)

The targets are predicted from the code, not yet computed.

| mutation | change | targets |
|---|---|---|
| `V-sign` | −V in the field equations | K1, K2 |
| `code-Vp` | `evolve.MUT = "Vp_sign"` before the numerical comparison | K1 |

## Amendments

## Runs (filled in as they are done)

| file | what |
|---|---|
