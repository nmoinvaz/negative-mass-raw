# I224-mac-review: the coordinator's review of #224 (rerun, independent check ind224)

Machine: macOS (the coordinator's Mac), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`, sympy 1.14.0), nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/224. Under review: branch `wip/i224-junction` at 42a76a3, raw `I224-rpi5`
at 2517fef. Written 2026-11-27 before the first run of `ind224.py` and before the rerun.

## Rerun

`python baby_universes_junction.py` from `notes/` of a detached worktree at 42a76a3. Expectation: 28 checks, 0 failed, the
output equal to `baby_universes_junction_output.txt` apart from timings.

## ind224: the Schwarzschild–de Sitter gluing by the coordinator's own derivation

Derived by hand for this review, then coded in sympy without the runner's script.
- Past side, the Schwarzschild interior at r = r₀ < r_s, F = r_s/r₀ − 1, unit normal n^r = −√F (r decreases to the future):
  K^x_x = (F + 1)/(2 r₀ √F), K^θ_θ = −√F/r₀.
- Future side, de Sitter beyond its horizon, G = H²r₀² − 1 > 0, n^r = +√G (r increases to the future):
  K^x_x = H² r₀/√G, K^θ_θ = +√G/r₀.
- Israel's condition for a spacelike shell, κ p_x = −2[K^θ], κ p_θ = −([K^x] + [K^θ]).

Consequences, by hand:
- κ p_x = −2(√G + √F)/r₀ < 0 for every r₀ > 1/H, r_s and H, so no shell-free matching exists.
- An isotropic shell ([K^x] = [K^θ]) needs 1/√(u² − 1) = (3F + 1)/(2√F), u = H r₀, so u = √((F+1)(9F+1))/(3F+1). This lies
  between 1 and 2/√3, with its maximum at F = 1/3, and its tension κσ/2 = (√G + √F)/r₀ > 0.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | The isotropic gluing value u(F) above equals the note's H r₀ = √((F+1)(9F+1))/(3F+1) (sympy, residual 0), and at that u the two jumps are equal (residual 0) |
| K2 | p_x < 0 at 200 random (F, u) with F > 0, u > 1, and the maximum of u(F) over F > 0 is 2/√3 at F = 1/3 |

## Mutations

| mutation | change | targets |
|---|---|---|
| `dS-normal` | n^r = −√G on the de Sitter side | K1, K2 |

## Runs (filled in as they are done)

| file | what |
|---|---|
| `rerun.log`, `rerun_diff.txt` | the rerun: **28 checks, 0 failed**; the output equals `baby_universes_junction_output.txt` apart from the Python version line and the timing |
| `ind224_run1.txt` | run 1: **exit 0, 2 of 2.** K1: the isotropic gluing u(F) equals the note's, residual 0, and solving [K^x] = [K^θ] for u returns it. K2: p_x < 0 at 200 random points; u(F) is stationary only at F = 1/3, where u = 2/√3 |
| `ind224_run1_mut_dS-normal.txt` | `dS-normal` fails exactly K1 and K2 |
