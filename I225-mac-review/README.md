# I225-mac-review: the coordinator's review of #225 (rerun, independent check ind225)

Machine: macOS (the coordinator's Mac), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`), nice 10. Issue:
https://github.com/nmoinvaz/negative-mass/issues/225. Under review: branch `wip/i225-throat-locus` at ed26e65, raw `I225-dh610`
at 982783a. Written 2026-11-27 before the first run of `ind225.py` and before the rerun.

## Rerun

`throat_locus.py analyze --raw=<I225-dh610>/runs` from a detached worktree at ed26e65. Expectation: 55 of 59 checks, every line
of `throat_locus_output.txt` again apart from paths and timings.

## ind225: the stall member's e-fold time without #151's code

The note compares the locus's growth rate with the asymmetric static member's e-fold time T(γ₁) r_th, from #151's code, at
γ₁ = 0.048, r_th = 1.0028: 0.8472 against the measured 1/λ = 0.8475. T is even in γ₁ (T(γ₁) = e^{2γ₁ arctan γ₁}/(√(1+γ₁²) β)).
ind225 interpolates T as a + b γ₁² + c γ₁⁴ through three published values, which share no code with #151's T at 0.048:
T(0) = 1/W = 0.846045 (#195), T(1/2) = 0.758357 (#151, [GGS09a] 0.758), T(1) = 0.675 (critical_ghost.md §1.1, [GGS09a]).

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | the interpolated T(0.048) × 1.0028 is within 1e-3 of the note's 0.8472 and of the measured 1/λ = 0.8475 |

## Mutations

| mutation | change | targets |
|---|---|---|
| `odd` | T fitted as a + b γ₁ + c γ₁² (not even) | K1 |

## Runs (filled in as they are done)

| file | what |
|---|---|
