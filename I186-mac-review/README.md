# I186-mac-review: the coordinator's review of #186 (rerun, independent check ind186)

The runner's raw folder for #186 is `I186-mac` (it ran on this Mac), so the review uses this folder name.

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`: numpy, scipy
1.18.1), Rust 1.94.0, at nice 10 with at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/186.
Under review: branch `wip/i186-taylor-polar` at f4edcb1, raw `I186-mac` at 2a4fbb7. Stop condition: 1 h per run.
Written 2026-11-26 before the first run of `ind186.py`.

## Rerun

`python3 phase2/nonradial/taylor_polar.py` from a worktree at f4edcb1 (`rerun_default_1.log`).

## ind186.py: an out-of-sample comparison

The runner compared the crate with scipy at the stored rows' γ and at 11 points of its own choosing. ind186 compares
them at three points neither used: (l, γ) = (2, 50), (3, 10), (4, 300), base variant (rtol 1e-10, φ_cut 1e-9, R = 60,
r0 = 1e-3). Shared: scipy's D comes from `polar_solver.PolarProblem(...).D` with `background.solve_star(0.7603, -1)`,
the existing reference path. The crate's D comes from the crate through `taylor_polar.d_values`, the runner's thin
wrapper of its command line. So the reference and the object under test are what they are; what is new is the choice of
points, the comparison and the timing.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| R1 | At each of the three points, \|D_crate(dd)/D_scipy − 1\| ≤ 1e-7, and the signs agree |
| R2 | At each point, \|D_crate(f64)/D_crate(dd) − 1\| ≤ 1e-6 |
| R3 | Timing (reported, not a pass condition): the wall time of each scipy and crate evaluation, with the machine load |

## Mutations (`--mutate=NAME`; each must make ind186 exit non-zero with exactly these criteria failing)

| mutation | change | targets |
|---|---|---|
| `wrong-l` | the crate is evaluated at l + 1 | R1, R2 |
| `f64-claim` | R2 expects 1e-15 | R2 |

`wrong-l` changes the crate's D in both lanes, so R2 can still pass if the two lanes agree at l + 1; its declared
targets are R1 and R2 as predicted, and an R2 that passes under it will be reported as off target.

## Runs (filled in as they are done)
