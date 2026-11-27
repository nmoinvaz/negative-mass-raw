# I183-mac-review: the coordinator's review of #183 (rerun, independent check ind183)

Machine: macOS (the coordinator's Mac, Apple M5, arm64), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`:
numpy, scipy 1.18.1, sympy 1.14.0, mpmath 1.3.0), Rust 1.94.0, nice 10, at most 2 processes. Issue:
https://github.com/nmoinvaz/negative-mass/issues/183. Under review: branch `wip/i183-conical-offgrid` at 9debda2, raw
`I183-rpi5` at 61c89c6. Written 2026-11-26 before the first run of `ind183.py`.

## Rerun

`rerun.sh`, from a detached worktree `~/Source/negative-mass-r183` at 9debda2. It runs stage a of the run of record
(`sys/run_record.sh`: every check but `dd_qd`, no controls, `--dump`). Then the default modes of `conical_global.py`
(#167) and `conical_loglog.py` (#184), whose earlier behavior the issue requires unchanged. The verdict records are
compared with `dump_run_03a`.

## ind183.py: an independent integration of four off-grid points

#183's walker is a Taylor stepper in double-double that solves N = 0 for F″ order by order (`conserve`). ind183
integrates the same ODE by an explicit system in f64 with scipy:
- (F, F′, F″) with F‴ = −(N_η + N_F F′ + N_F′ F″)/N_F″, from N's derivatives in sympy (`det_classify.conical_N()`);
- DOP853, rtol 1e-12, atol 1e-14, inward from η = L to η = 1e-6, started from #167's mpmath series
  (`conical_global.series_mp`) at the crate's own start radius L.

The root branch is fixed at the start by the series and kept by the flow. The end is classified by the state where scipy
stops:
- `F->0`: |F| < 1e-3 |F_∞| or |F′| > 1e8;
- `a3->0`: |F² − η² − 1| < 1e-3 (the κ curve);
- `FLOOR`: η = 1e-6 is reached.

Shared: N (#159, reviewed in #167) and the series (#167's Python, reviewed). New: the formulation, the integrator, the
classification and the choice of points.

**Points, fixed now.** In this order, the first four whose crate verdict (`offgrid scan`, dd, conserve) has a start
radius L ≤ 800 are used: (0.05, 100), (0.2, −30), (8, 300), (24, −1000), (0.01, 3), (6, −100), (0.1, 1000), (12, 30).
f64 cannot follow the C mode from larger L (dF·L⁴ at η = 20, #183's O14 ruling).

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | At each of the four points, ind183's end kind equals the crate's. For a SINGULAR kind, \|η_end − η*_crate\| ≤ 1e-4·max(1, η*_crate). For FLOOR, scipy reaches η = 1e-6 and sign(ηF′)·sign(F_∞) > 0 there |
| K2 | \|N\|/Σ\|terms of N\| ≤ 1e-8 at the last accepted step of each integration (the flow keeps N = 0) |

## Mutations (`--mutate=NAME`; each must make ind183 exit non-zero with exactly these criteria failing)

| mutation | change | targets |
|---|---|---|
| `k1-c` | ind183's series start uses C(1 + 1e-3) | K1 (the C mode moves η* and can change the kind) |
| `k2-drift` | K2 is evaluated with F″ perturbed by 1e-6 relative at the last step | K2 |

## Runs (filled in as they are done)

| file | what |
|---|---|
| `ind183_run1.txt` | run 1: exit 1, **K1 fails at (0.2, −30) by a defect of the coordinator's check**. scipy stopped on the terminal event \|F′\| = 1e8 at η = 11.70092677, against the crate's F->0 at 11.70094779 (difference 2.1e-5, inside the bar 1.2e-3). The classification tested \|F′\| > 1e8, which an event root at exactly 1e8 misses, so the point read "other". The other three points agree: (0.05, 100) FLOOR, (8, 300) F->0 at 3.4e-5, (0.01, 3) FLOOR. K2 passes (\|N\|/Σ ≤ 9.5e-13). K1 stays failed as run 1 reports it |

## Amendments

**A1, 2026-11-27, after run 1.** The F->0 test reads \|F′\| ≥ 1e8, so a stop on the event counts. No bar, point or
tolerance changes. Run 2 is the run with the fix, and the mutations are run with it.
