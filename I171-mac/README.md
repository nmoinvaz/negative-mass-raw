# I171-mac: the coordinator's review of #171 (rerun of the default mode, independent check ind171)

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0 (`/Users/nathan/Source/negative-mass/.venv`),
at nice 10 with at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/171. Under review: branch
`wip/i171-planar-residual` at bfab8bf, raw `I171-rpi5` at 8840bed. Stop condition: 1 h per run. Written 2026-11-26
before the first run of `ind171.py`.

## Rerun

`python3 notes/warp/planar_residual.py` from a worktree at bfab8bf (`rerun_default_1.log`): exit 0, 8 of 8 checks, every
control on its declared target; identical to the committed output apart from timings.

## ind171.py: what it shares with #171

Shared: sympy; the metric, the fields φ₁ = α₁(cH − (4/c)J), φ₂ = α₂(cH + (4/c)J), and the convention T_ab = ∂_aφ₁∂_bφ₁ −
∂_aφ₂∂_bφ₂ − g_ab(½(∇φ₁)² − ½(∇φ₂)² + V) (two_scalars.md). Not shared: ind171 imports nothing from the repository;
its Christoffel symbols, Ricci tensor and Einstein tensor are its own (the same construction as I166-mac/ind166.py).

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| M1 | For g = −2e^{2H(p)J(q)} dp dq + dy² + dz², H, J undefined, c a nonzero symbol, α₁ = α₂ = 1/(4√(2π)), V = 0: every component of G_ab − 8πT_ab is 0 exactly |
| M2 | At the exact point (H, H′, H″, J, J′, J″) = (1/2, 1/3, 2, 2, −1/5, 3), c = 3/2: the components of G_ab − 8πT_ab, linear in (A₁, A₂, V) with A_i = α_i², have the unique solution (1/(32π), 1/(32π), 0) |
| M3 | Planted: #78's P1, (−dτ² + dz²)/z² + dR² + R²dΘ² with two normal scalars φ_I = X_I/√(8π), X = R(cos Θ, sin Θ), V = −1/(8π): every component of G_ab − 8π(T₁ + T₂)_ab is 0 exactly |

## Mutations (`--mutate=NAME`; each must make ind171 exit non-zero with exactly these criteria failing)

| mutation | change | targets |
|---|---|---|
| `alpha-11` | M1 with α₁ multiplied by 11/10 | M1 |
| `phantom-sign` | M1 with the phantom entering T with + | M1 |
| `uniq-claim` | M2 expects A₁ = 1/(16π) | M2 |
| `p1-V` | M3 with V = +1/(8π) | M3 |

## Runs (filled in as they are done)

| file | what |
|---|---|
| `rerun_default_1.log`, `.time` | rerun: exit 0, 8 of 8 checks, every control on target, 131 s; identical to the committed output apart from timings |
| `ind171.py`, `run_ind171.sh`, `ind171_run1.txt` | run 1: exit 0, 3 of 3 criteria pass. M1: the residual is 0 for undefined H, J and symbolic c, with G ≠ 0. M2: 5 nonzero component equations at the exact point, unique solution (1/(32π), 1/(32π), 0). M3: #78's P1 residual 0 |
| `ind171_run1_mut_*.txt` | the 4 mutations, each exit 1 with exactly its target failing |
