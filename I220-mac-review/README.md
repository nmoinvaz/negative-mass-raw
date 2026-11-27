# I220-mac-review: the coordinator's review of #220 (Ω₄; rerun, independent check ind220)

Machine: macOS (the coordinator's Mac), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`: mpmath 1.3.0, sympy
1.14.0), nice 10, at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/220. Under review: branch
`wip/i220-omega4` at 0e26546, raw `I220-rpi5` at 8a49e76. Written 2026-11-27 before the first run of `ind220.py` and before the
rerun.

## Rerun

`order6.py`'s symbolic check and its closed-form evaluation from a detached worktree at 0e26546 (the grid runs of record take
hours on the Pi; the review reruns the parts that are minutes). Expectation: the same verdict lines.

## ind220: the coordinator's Taylor-jet hierarchy of the reviews of #26, #208 and #209, carried to order 6

`I208-mac-review/ind208.py`, with the order series extended from five to six (Y₀ … Y₆, L₀ … L₆, Ω₀ … Ω₄): order 40 in
v = √l, 70 digits, V = 17. It shares no code with method B (`PanelB`). The order equations are compared symbolically with
`order6.py`'s `hk` and `Fsum` (as K1 of ind208 did with `order5.py`).

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | The order equations derived from #195's ℓ-system equal `order6.py`'s h_k for k = 0 … 6 and dY_k/dl for k = 1 … 6 (sympy residual 0) |
| K2 | Ω₀ … Ω₃ from G₂ … G₅ = 0 equal their closed forms (1e-35, 1e-33, 1e-30, 1e-30 absolute), and Ω₄ from G₆ = 0 equals the closed form of `omega4.md` within 1e-25 relative |
| K3 | the closed form equals #195's fit −12794.49986002 to its 14 digits (difference ≤ 5e-10) |

## Mutations

| mutation | change | targets |
|---|---|---|
| `drop-z5` | the closed form without its −10432ζ(5) term | K2, K3 |
| `short-V` | V = 9 | K2 |

## Amendments

## Runs (filled in as they are done)

| file | what |
|---|---|
