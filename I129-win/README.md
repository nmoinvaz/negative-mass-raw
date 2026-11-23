# I129-win: caches and logs of `harm_circles.py`, the mean value test of arg D at the 12 harm points of four boxes

Machine: win (surface-laptop-4, Windows 11, 8 logical CPUs, 32 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/129

## Code and environment

Code: worktree `negative-mass-i129` (beside this clone) on branch `wip/i129-circles` at 4636e5c,
`phase2/nonradial/harm_circles.py`, run from `phase2/nonradial`, unmodified. `polar_solver.py` is not changed.

Python: `negative-mass-venv314\Scripts\python.exe`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1 (the pinned
requirements.txt). Every run has `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1` and `MKL_NUM_THREADS=1`, below-normal
priority, and is launched detached with `start` (`go_<job>.cmd` starts `job_<job>.cmd`, which writes `<job>.log` and
`<job>.log.exit`). At most two processes. A second one starts only while choptuik-large-d's processes together use under
4 cores (CPU-seconds delta over 10 s, one reading per start, in `cores.log`; `queue.ps1`). Memory is reported only:
nothing stops or kills a process because of it (`memory-sampler.log`, once a minute).

## What is tested

`harm_circles.py` tests the mean value property of arg D (winding2's D) at the three harm points of each of `p7603_l2`,
`p7603_l3`, `c075_l2` and `p085_l3` (Re s in [0.1, 2], |Im s| <= 2.5, L = 2.5), on 64 points of circles of radius
0.05 L and 0.025 L, with the criterion of RESULTS.md §5.5: |Δφ| L² <= 10⁻⁶ (1 + |∇φ| L). Three settings:

| setting | rtol | `nchunks` | `zerilli_q` rtol |
|---|---|---|---|
| S8 | 10⁻⁸ | as `polar_solver` chooses it, per point | 10⁻¹¹ (its own) |
| S10 | 10⁻¹⁰ | fixed across each circle at the centre's value | 10⁻¹² |
| S12 | 10⁻¹² | fixed across each circle at the centre's value | 10⁻¹³ |

A run is 3 points × 129 evaluations (the centre and 2 × 64 circle points), cached in
`harm_circles_<box>_<setting>.pkl` after every point, so a restarted run resumes. Controls at every point and radius,
through the same circle code: a planted holomorphic phase (must pass) and a planted non-harmonic one (must fail).
Mutations `nonholo` and `half` must each exit 1.

## Plan

1. Pilot, the hardest case alone: `pilot-c075_l2-S12-p2` = `--box=c075_l2 --setting=S12 --points=2` (the worst point of
   #122, 129 times its limit at rtol 10⁻⁸). Records the time per evaluation and the verdicts. Stop condition: one
   evaluation over 10 min, or the pilot over 8 h; then stop it and report before step 2.
2. The twelve runs, two at a time (`queue.ps1`), in this order: S12 for `p7603_l2`, `p7603_l3`, `c075_l2` (resumes
   from the pilot's cache), `p085_l3`; then S10 for the four; then S8 for the four. Default `--points=0,1,2`. Each exit
   code is reported as it is: exit 1 means a failed check, a result, not an error.
3. Mutations on the cached S12 data of `c075_l2`, no new evaluation: `mutate-nonholo` and `mutate-half`, each must
   exit 1.
4. `collect.log`: `--collect` from every cache. The same text is `phase2/nonradial/harm_circles_output.txt` in the code
   repository.

## Files

| file | holds |
|---|---|
| `jobs.txt`, `make_launchers.py` | one line per job (`<job>\|<arguments>`) and the writer of `job_*.cmd` and `go_*.cmd` |
| `queue.ps1`, `queue.log`, `cores.log` | the gated queue, its log, and one reading of choptuik-large-d's cores per second start |
| `keepawake.ps1` | holds `SetThreadExecutionState(ES_CONTINUOUS \| ES_SYSTEM_REQUIRED)` until the queue process exits; started 2026-11-22 13:03 after the laptop was in Modern Standby from 09:41 to 10:01 and 10:47 to 12:51, which suspended the runs; no power setting or plan is changed; start and end are in `queue.log` |
| `sample.ps1`, `memory-sampler.log` | working set, peak working set and CPU of the `harm_circles.py` processes once a minute, with the free memory |
| `<job>.log`, `<job>.log.exit` | stdout and exit code of each job |
| `harm_circles_<box>_<setting>.pkl` | the cache of D at every evaluated point |
| `job_mutate.cmd`, `go_mutate.cmd`, `mutate-nonholo.log`, `mutate-half.log` (+ `.exit`) | the two mutations on the cached S12 data of `c075_l2`, one after the other, no new evaluation |
| `collect.log`, `collect.log.exit` | `--collect` from every cache; the same text is `phase2/nonradial/harm_circles_output.txt` |
| `results_table.py`, `results_table.txt` | the pivot of `harm_circles_output.txt` (ratio per point, setting and radius; first passing setting; worst ratio and smallest explaining point error per setting) quoted in RESULTS.md §5.5 |

## Results (2026-11-22)

Code commit with the output and RESULTS.md §5.5 / §8: `wip/i129-circles` at fb7d97a (script unchanged from 4636e5c).

| step | exit | note |
|---|---|---|
| pilot `c075_l2` S12 point 2 | 0 | 43 s per evaluation (the Mac: 9.7 s) |
| S12 `p7603_l2`, `p7603_l3`, `c075_l2`, `p085_l3` | 0, 0, 0, 0 | all 24 rows pass, ratios 5.0e-6 to 2.5e-3 |
| S10 `p7603_l2`, `p7603_l3`, `c075_l2`, `p085_l3` | 0, 0, 0, 0 | all 24 rows pass, ratios 3.4e-3 to 0.102 |
| S8 `p7603_l2`, `p7603_l3`, `c075_l2`, `p085_l3` | 1, 1, 1, 1 | 16 of 24 rows fail (8 points), ratios 1.07 to 11.8; a failed check, a result |
| `--mutate=nonholo`, `--mutate=half` on `c075_l2` S12 | 1, 1 | as required |
| `--collect` | 0 | `RESULT PASS` |

Queue: 2026-11-22 01:47 to 19:02 (`queue.log`), two runs at a time, choptuik-large-d at 0.06 to 1.94 cores at every
start (`cores.log`). Cost per evaluation on one thread: S12 17.6 to 45.2 s, S8 7.0 to 19.2 s; the S10 values in the logs
(10.7 to 103.3 s) include the slow stretches below.

Episodes that cost time and changed no result:
- The laptop was in Modern Standby from 09:41 to 10:01 and from 10:47 to 12:51 (brief wakes at 12:20 and 12:36), which
  suspended the S10 runs without killing them (gaps in `memory-sampler.log` before 12:20:16, 12:51:18 and 12:59:10).
  `keepawake.ps1` (pid 25836, 13:03:52 to 19:02:29, held `ES_CONTINUOUS | ES_SYSTEM_REQUIRED`; no power setting or plan
  changed) followed the coordinator's go-ahead. No gap in the sampler after 12:59.
- From about 08:48 the S10 evaluations ran 2.3 to 3.3 times slower than the first S10 run, at the time of power-source
  changes (Kernel-Power events). Battery power is the likely cause; not tested.
- The first capture of the mutations' exit codes (PowerShell `Start-Process`) lost them, so both were rerun through
  `job_mutate.cmd` (no new evaluation; the cache of `c075_l2` S12 is byte-identical to before, `git` shows no change). The logs here are
  those of the second run.
