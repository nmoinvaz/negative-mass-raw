# I114-win: controls of the cap in `convergence.py` and the two rtol 1e-12 evaluations #4 capped, l = 5 at gamma = 6000 and l = 6 at gamma = 12000

Machine: win (surface-laptop-4, Windows 11, 8 logical CPUs, 4 physical cores, 32 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/114

## Code and environment

Code: worktree `negative-mass-i114` (beside this clone) on branch `wip/i114-convergence-cap` at 2447e1c (main 51ced6d),
`phase2/nonradial/convergence.py` with its per-evaluation wall-time cap (`CAP_S`) and its `--mutate=nocap`, run from
`phase2/nonradial`, unmodified.

Python: `negative-mass-venv314\Scripts\python.exe` (Python 3.14.10, numpy 2.5.4, scipy 1.18.1, the pinned
requirements.txt). Every run has `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1` and `NPROC=1`,
below-normal priority, and is launched detached with `start` (`go_<job>.cmd` starts `job_<job>.cmd`, which writes
`<job>.log` (stdout), `<job>.stderr` and `<job>.log.exit`). `jobs.txt` and `make_launchers.py` write the launchers.
At most two processes of mine at a time (each is a main process and one pool worker, one of them computing). A second
starts only while choptuik-large-d's processes together use under 4 cores (CPU-seconds delta over 10 s, one reading per
start, in `cores.log`; `queue.ps1`). Memory is reported only: nothing stops or kills a process because of it
(`memory-sampler.log`, once a minute, pool worker included).

Keep-awake: `keepawake.ps1 -QueuePid <queue pid>` (copied from `I129-win`) holds `SetThreadExecutionState(ES_CONTINUOUS |
ES_SYSTEM_REQUIRED)` until the queue's process exits, then releases it. It changes no power setting or plan. Its start
and end are in `queue.log`. The laptop has to stay plugged in.

## Task

#4's `convergence.py` rows at l = 5, gamma = 6000 and l = 6, gamma = 12000 lack the rtol 1e-12 variant: it was stopped
by hand at a 5 h cap and the rows were added with `cap_row.py` (`../I4-win`), not a repository script. `convergence.py`
now caps each (variant, gamma) evaluation by itself. This folder holds

1. the controls of that cap (`ctl_cap`, `ctl_nocap`, `regen5`, `regen6`),
2. the two evaluations run with the caps CAP5 and CAP6 the coordinator names (`run_l5`, `run_l6`; see Plan),
3. the regenerated `convergence_l5_output.txt` and `convergence_l6_output.txt` (no new evaluation).

The partial files of #4 (`convergence_l{5,6}_w0.7603.partial.csv`, 65 evaluations each) are copied from `../I4-win`.

## Plan and acceptance

Controls, each with a result that can fail:

| job | command (from `phase2/nonradial`) | passes when |
|---|---|---|
| `ctl_cap` | `CAP_S=4 GAMS=0.001,40 PARTIAL_DIR=ctl_cap python convergence.py 2` | gamma = 40 row carries "not completed" (all six tasks), gamma = 1e-3 row does not, exit 0 |
| `ctl_nocap` | the same with `--mutate=nocap`, `PARTIAL_DIR=ctl_nocap` | no row carries "not completed", exit 0 |
| `regen5` | `CAP_S=1 GAMS=<G5> PARTIAL_DIR=regen5 python convergence.py 5` on a copy of #4's partial file | stdout differs from `convergence_l5_output.txt` in the top row's bracketed note only; only the missing task starts, and is capped |
| `regen6` | the same for l = 6 with `<G6>` | the same for `convergence_l6_output.txt` |

G5 = `0.001,0.03,0.3,1,3,10,40,137,300,1000,6000`, G6 = `0.001,0.03,0.3,1,3,10,40,137,300,1000,12000` (#4's gammas).

Runs: `run_l5` = `CAP_S=CAP5 GAMS=<G5> PARTIAL_DIR=. python convergence.py 5` and `run_l6` = the same for l = 6, each on a
copy of #4's partial file in this folder, each starting only the one missing task (rtol 1e-12 at the top gamma; checked
in the partial file's `start` line). The caps are the stop condition; a capped evaluation is a result. Acceptance of
the issue: both finish with D < 0, each within 2.1e-4 relative of its base value, or the row is reported as it is.

Then `convergence_l{5,6}_output.txt` in the code repository are regenerated from the partial files here (same GAMS and
`CAP_S`, nothing evaluated) and diffed against the committed versions: only the top row may change.

## Controls (step 2, 19:41 to 19:47, all four exit 0, stderr empty)

| job | result |
|---|---|
| `ctl_cap` | gamma = 1e-3 row complete, no note, and equal to `convergence_l2_output.txt`'s row (time column aside). gamma = 40 row: all six tasks "not completed, stopped after 4s of wall time at the cap (CAP_S = 4s)", "signs and spread are over 0 variants". The partial file has 12 `start`, 6 `done`, 6 `capped` records, each capped one 4.04 to 4.05 s. Exit 0. **Passes.** |
| `ctl_nocap` | `--mutate=nocap` with the same `CAP_S=4`: 0 rows carry "not completed", both rows equal `convergence_l2_output.txt`'s (time column aside), 12 `start` and 12 `done` records, no `capped`. Exit 0. **The check fires: the mark is gone when the cap is ignored.** |
| `regen5` | stdout differs from the committed `convergence_l5_output.txt` in line 17 only, and only in the bracketed note (`[rtol 1e-12 not completed, stopped after 1s of wall time at the cap (CAP_S = 1s); signs and spread are over 4 variants]`). One new `start` and one `capped` record, both for `rtol 1e-12` at gamma = 6000 (wall 1.003 s). Exit 0. **Passes.** |
| `regen6` | the same for l = 6, line 17 (gamma = 12000), `capped` wall 1.010 s. Exit 0. **Passes.** |

The queue (`queue.log`) started `ctl_cap` at 19:41:37, `ctl_nocap` at 19:42:07 (choptuik-large-d 1.65 cores), `regen5` at
19:45:38 (1.79) and `regen6` at 19:46:08 (1.72), and ended at 19:47:28. The keep-awake ended at 19:47:37. The sampler's
largest working set was 84 MB.

## Files

- `jobs.txt`, `make_launchers.py`, `job_<job>.cmd`, `go_<job>.cmd`: the launchers. `queue.ps1`, `queue.log`,
  `cores.log`: the queue and its core readings. `keepawake.ps1`, `sample.ps1`, `memory-sampler.log`: keep-awake and
  memory sampler. `partial_records.py`: counts the records of a partial file and lists those after a given line.
- `<job>.log` (stdout), `<job>.stderr`, `<job>.log.exit` for each job; `ctl_cap/`, `ctl_nocap/`, `regen5/`, `regen6/`
  hold each control's partial file.

(the two evaluations and the regeneration are added when they finish)
