# I114-win: controls of the cap in `convergence.py` and the two rtol 1e-12 evaluations #4 capped, l = 5 at gamma = 6000 and l = 6 at gamma = 12000

Machine: win (surface-laptop-4, Windows 11, 8 logical CPUs, 4 physical cores, 32 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/114

## Code and environment

Code: worktree `negative-mass-i114` (beside this clone) on branch `wip/i114-convergence-cap` at f7b8e10 (2447e1c added
the cap, 6e73456 the l = 5 output, f7b8e10 the l = 6 output and RESULTS.md; main 51ced6d),
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

- The two evaluations and the regenerations: see Results: l = 5 and Results: l = 6. Their files: `run_l5.*`, `run_l6.*`
  (run 1), `job_run_l6_run2.cmd` and `run_l6_run2.*` (run 2), `regen_out5.*`, `regen_out6.*`, `check_l5.py`,
  `check_l5.out`, `check_l6.out`, `check_spread.py`, `memory-sampler-run2.log`, `status_run2.ps1`, `register_task.ps1`.

## Runs (step 3)

- `run_l5`: `CAP_S=129600` (36 h, the coordinator's CAP5) `GAMS=<G5> PARTIAL_DIR=. NPROC=1 python convergence.py 5`, on a
  copy of `../I4-win/convergence_l5_w0.7603.partial.csv` (65 results, identical hash). Queue started 2026-11-22 20:02:30
  (`queue.log`). Its only new `start` record is `rtol 1e-12` at gamma = 6000, pid 4940, at 20:03:12 (about 40 s of problem
  setup after the launch). The cap falls at 2026-11-24 08:03; the coordinator's estimate is about 25 h.
- `run_l6` (run 1; it was killed on 2026-11-24 at about 23:06 and run 2, `run_l6_run2`, restarted it, see Amendment 1):
  `CAP_S=432000` (5 days, the coordinator's CAP6) `GAMS=<G6> PARTIAL_DIR=. NPROC=1 python convergence.py 6`, on a copy
  of `../I4-win/convergence_l6_w0.7603.partial.csv` (65 results, identical hash). Started beside `run_l5` after a gate reading
  of 1.77 cores for choptuik-large-d (`cores.log`). Its only new `start` record is `rtol 1e-12` at gamma = 12000, pid 880, at
  2026-11-22 21:41:49. The cap would have fallen at 2026-11-27 21:41; the coordinator's estimate was about 89 h.
- The keep-awake of `run_l5` ended at 21:42:02 with its queue, which I replaced by a queue `+run_l5 run_l6` and its own
  keep-awake (started 21:40:55) so one holds until the last run ends.
- `status.ps1`: elapsed wall time since each run's `start` record, the worker's cpu seconds and their ratio (below 1 or
  gaps in `memory-sampler.log` show a suspended laptop). The one sampler gap so far, 19:46:38 to 20:02:30, is the sampler
  stopped between the controls and `run_l5`, not a standby. cpu counts from the worker's creation, so it exceeds the wall
  time since the start record by the problem setup (about 40 s) at the start of a run.

## Amendments

1. **2026-11-24: run 1 of l = 6 was killed and run 2 restarted it.**
   - Run 1 (`run_l6`, worker pid 880, started 2026-11-22 21:41:49) was killed at about 23:06 on 2026-11-24, after 49.4 h of
     wall time (the memory sampler's last line, 23:05:50, shows 175,540 cpu-s). The coordinator replaced the runner session
     to change accounts, and removing the session's terminal ended the cmd/start chain, which was still inside the
     terminal's job. It left no result, no `done`, `capped` or `died` record and no `run_l6.log.exit`. Its files stay as
     they were: `run_l6.log`, `run_l6.stderr`, `memory-sampler.log` (through 23:05:50) and `queue.log`. The keep-awake,
     queue and sampler of run 1 ended with it. The partial file is not edited: it keeps its 65 results and run 1's `start`
     record (pid 880), and `convergence.py` resumes the one missing task from it, as the regen controls showed.
   - Run 2 (`run_l6_run2`): `job_run_l6_run2.cmd` is written by `make_launchers.py run_l6_run2` from the new line of
     `jobs.txt` and is `job_run_l6.cmd` byte for byte except `run_l6` -> `run_l6_run2` in the three output names: the same
     environment (one thread each, `NPROC=1`), `CAP_S=432000`, `GAMS=<G6>`, `PARTIAL_DIR` this folder and `python
     convergence.py 6`. It writes `run_l6_run2.log`, `run_l6_run2.stderr` and `run_l6_run2.log.exit`. `CAP_S` counts from
     run 2's own start, so the cap falls 120 h after it, at 2026-11-29 23:13. The estimate is about 89 h (about
     2026-11-28 16:00); l = 5 took 0.9 of its estimate.
   - Run 2 is started through Task Scheduler so that it outlives the session that starts it. `register_task.ps1` registers
     a task with no trigger, and `schtasks /run /tn nm-i114-l6-run2` started it at 2026-11-24 23:12:51. Its `start` record
     in the partial file: `rtol 1e-12` at gamma = 12000, worker pid 24560, time 23:13:54 local (the worker was created at
     23:13:24 and set up for about 30 s). Process tree: worker 24560 <- main python 10820 <- venv launcher 7564 <- cmd
     9320 (the wrapper) <- svchost 3420 (the Schedule service) <- services.exe, with no shell of mine in it. Priority class
     BelowNormal. The partial file now has its 65 result lines and two `start` records, run 1's and run 2's.
   - Settings that differ from `schtasks /create /sc once /st 23:59 /f`, which the coordinator proposed: no trigger (the task
     cannot start a second worker at 23:59); no execution time limit (the `schtasks` default is 72 h, which would have
     killed an 89 h run); no stop or refusal on battery (`DisallowStartIfOnBatteries` and `StopIfGoingOnBatteries` are
     false; the laptop is still to stay plugged in); one instance at a time (`IgnoreNew`). An `S4U` logon (survives a
     logoff) was refused without elevation (`Access is denied`), so the tasks use the interactive token: they survive
     the end of the session and of the `hc` call, not a logoff of the Windows user.
   - Keep-awake: task `nm-i114-keepawake-run2` runs `keepawake.ps1 -QueuePid 9320` (the wrapper), started 23:13:15
     (`queue.log`), and releases when the wrapper ends. No power setting or plan is changed.
   - Memory sampler: task `nm-i114-sampler-run2` runs `sample.ps1` once a minute into the new `memory-sampler-run2.log`
     (run 2's worker included), started 23:13:15. `status_run2.ps1` is `status.ps1` for run 2.
   - The row's time column sums the seconds of the results, so it will count run 2's wall time only, not run 1's 49.4 h,
     which produced no result.
   - Stopping, if ever needed: `schtasks /end /tn <name>` of these three tasks only, never a process by name. When run 2
     ends the sampler task is ended and the three tasks are deleted (`schtasks /end`, `/delete /f`), and the end is logged
     here.

## Results: l = 5 (`run_l5`, finished 2026-11-23 18:28, exit 0)

The rtol 1e-12 evaluation at gamma = 6000 finished inside its cap: wall 80728.5 s (22.42 h), cpu 79762 s, worker pid 4940
(`done` record in the partial file; the coordinator estimated about 25 h, the cap was 129600 s). cpu/wall was 0.989 for
the whole run and the sampler shows no gap, so no standby. `check_l5.py` (output in `check_l5.out`) reads the partial
file independently of `convergence.py`'s printing:

| variant at gamma = 6000 | D |
|---|---|
| base | -8.936082976708e-13 |
| rtol 1e-12 (new) | -8.936082955882e-13 |
| background R = 90 | -8.937095724218e-13 |
| r0 = 3e-3 | -8.935196170070e-13 |
| phi_cut 1e-12 (r_m ~ 34) | -4.438951805474e-13 |

rtol 1e-12 against base: relative difference 2.33e-9 (limit 2.1e-4), D < 0. All five D are negative.
`run_l5.log` (stdout) has the top row with no cap note and time (107868s) = 27140 s of the five old evaluations plus the
new 80728 s. `run_l5.stderr` holds the same two kinds of RuntimeWarning as #4's l = 5 stderr (`polar_solver.py:106`
overflow in multiply, scipy's `rk.py` invalid value in dot).

Step 4 for l = 5 (`regen_out5`, exit 0, no new evaluation, stderr empty): stdout went to
`phase2/nonradial/convergence_l5_output.txt`, which equals `run_l5.log` and differs from the committed version in the
top row only, and there only in the time `(27140s)` -> `(107868s)` and the removed note. D_base, signs, spread, D(r_m ~ 34)
and q are the same to the printed digits. Code commit 6e73456 on `wip/i114-convergence-cap`.

Observation, not changed (the script is the coordinator's): `convergence.py` takes the "same r_m" variants as those
without `phi_cut` in their name, and the base variant's name `base (rtol1e-10, phi_cut1e-9, R60)` contains it, so base is
left out of the spread and the spread is over rtol 1e-12, R = 90 and r0. `check_spread.py` shows that including base
changes no printed spread at any of the 11 gammas of l = 4, 5 and 6, nor in the l = 2 control.

## Results: l = 6 (`run_l6_run2`, finished 2026-11-28 05:37, exit 0)

The rtol 1e-12 evaluation at gamma = 12000 finished inside its cap: wall 282227 s (78.40 h), cpu 278516 s, worker pid
24560 (`done` record in the partial file; the coordinator estimated about 89 h, the cap was 432000 s and would have
fallen 2026-11-29 23:13). cpu/wall was 0.987 for the whole run. The sampler has 4703 samples from 2026-11-24 23:13 to
2026-11-28 05:50 and no gap over 150 s, so no standby. Free memory ran from 12.1 GB (2026-11-25 09:52) to 23.1 GB of
31.8 GB, other processes included; reported only, the worker held about 33 MB. `check_l5.py` (output in `check_l6.out`)
reads the partial file independently of `convergence.py`'s printing:

| variant at gamma = 12000 | D |
|---|---|
| base | -1.595791249461e-13 |
| rtol 1e-12 (new) | -1.595791301340e-13 |
| background R = 90 | -1.595972229568e-13 |
| r0 = 3e-3 | -1.595633039949e-13 |
| phi_cut 1e-12 (r_m ~ 34) | -7.926916804460e-14 |

rtol 1e-12 against base: relative difference 3.25e-8 (limit 2.1e-4), D < 0. All five D are negative. The spread over
the same-r_m variants is 2.126e-4 with and without the rtol 1e-12 value. `run_l6_run2.log` (stdout) has the top row with
no cap note and time (349304s) = 67077 s of the 65 earlier results plus the new 282227 s; run 1's 49.4 h left no result
and is not in it. `run_l6.stderr` (run 1), `run_l6_run2.stderr` and `regen_out6.stderr` are empty.

Step 4 for l = 6 (`regen_out6`, exit 0, no new evaluation, stderr empty): stdout went to
`phase2/nonradial/convergence_l6_output.txt`, which equals `run_l6_run2.log` and differs from the version committed in
6e73456 in the top row only, and there only in the time `(67077s)` -> `(349304s)` and the removed note. D_base, signs,
spread, D(r_m ~ 34) and q are the same to the printed digits. Code commit f7b8e10 on `wip/i114-convergence-cap` (with
RESULTS.md section 3a and the section 8 row). The first launch of `regen_out6` at 05:38:18 did not start (`cmd /c` of a
relative path from PowerShell); it was started again by full path at 05:48:28, both in `queue.log`.

The end of the run, all of it mine (`queue.log`): the keep-awake released itself at 05:37:55 when its queue pid 9320
ended; the sampler task was ended with `schtasks /end /tn nm-i114-sampler-run2` at about 05:50 (its process 9284 was
gone afterwards, by pid, not by name); the three tasks `nm-i114-l6-run2`, `nm-i114-keepawake-run2` and
`nm-i114-sampler-run2` were deleted with `schtasks /delete /f` at 05:51. No process of mine is left.
