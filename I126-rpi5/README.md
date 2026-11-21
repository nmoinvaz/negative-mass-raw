# I126-rpi5: logs and caches of #126's recount at winding2's and zerilli_zeros's `--guard=all` of the boxes counted at guard 1

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/126

## Code and environment

Code: worktree `~/Source/negative-mass-i126` on branch `wip/i126-guard-all` at e3bdadd, `phase2/nonradial/winding2.py`,
`zerilli_zeros.py` and `collect_i126.py`, unmodified, run from `phase2/nonradial`.

Python: `~/Source/negative-mass-venv314/bin/python`. Every run is `nice -n 10` with `OMP_NUM_THREADS=1` and
`OPENBLAS_NUM_THREADS=1` (both scripts are single-threaded), detached with `setsid nohup`. At most two processes at a time,
and a second one starts only while the 15-minute load average is below 4. Memory is reported, never a stop condition.

## What is counted

Every box whose count RESULTS.md reports at the default step rule (`--guard=1`), recounted with `--guard=all` on a copy of
its stored cache and with the planted zero of its first run:

| jobs | script | counts | boxes |
|---|---|---|---|
| `w_*` (31) | `winding2.py` | zeros minus poles of D | §5's seven, §5.1's 17 (the `rep` box at l = 2 is §5's `p7603_l2`), #115's eight other than s1 at l = 5 |
| `z_*` (30) | `zerilli_zeros.py` | zeros of Z(r_m; s), D's poles | #121's 21 boxes and #124's nine |
| five controls | both | | `z_flat` must end "all checks passed"; `z_mut_reverse`, `z_mut_nonorm` and `z_mut_lshift` must end "FAILED:" and name `plant`, `holo` and `column`; `w_mut_reverse` must print PLANTED ... FAIL and exit 1 |

## Files

- `jobs.txt`: the 66 lines `job|script|arguments|source folder` of `python collect_i126.py --jobs`, byte for byte. Job `<job>`
  runs as `python -u <script> <arguments> --cachedir=<this folder>/cache`, with stdout and stderr in `<job>.log`.
- `controls.txt` (5), `z_boxes.txt` (30), `pilot.txt` (`w_s2_l2`, the slowest at guard 1: 3.7 h in #5, stop condition 8 h)
  and `w_boxes.txt` (the other 30, longest expected first by the walls in the `queue.log` of I5-rpi5, I54-rpi5 and
  I115-rpi5): the order of the jobs, one name per line. Controls first, then the Z boxes, then the pilot alone, then the W boxes.
- `launch_I126.sh LISTFILE`: queue worker. Exit status of each job in `done/<job>.rc`, start and end times in `queue.log`.
  `start_second.sh LISTFILE` starts a second worker once the 15-minute load is below 4. `memwatch.sh` writes `memwatch.log`
  (load, available memory, cpu and rss of this task's processes; reports only; stopped at the end of the run).
- `launch_I126_gated.sh LISTFILE`: from 02:37 on, the worker for the W boxes. Before each job it counts this task's running
  processes under a lock: none, it starts; one, it starts only while the 15-minute load is below 4 and logs "15-min load X < 4:
  start <job>"; two, it waits and logs the wait. The first second-slot worker (`start_second.sh`) had started `w_s3_l3` at
  02:03 without that test, with the load at about 6. At 02:37 `w_boxes.txt` was renamed `w_boxes.old` (so that worker stopped
  after its box) and `w_boxes_g.txt` lists the 27 W boxes not yet started, in the order of `w_boxes.old`. Two gated workers
  took them. The load stayed above 4 for most of the run, so the W boxes ran mostly on one process.
- `summarize_i126.py` writes `summary.txt`: wall and evaluations per job, and cache points before and after per cache.
  `collect_mutate_<name>.log`: the collector's five mutations. `diagnose_*.log`: four runs of `phase2/nonradial/diagnose_plant.py` that must
  fail, on the 212-point cache of #115 before its guard-all rerun (`--mutate=sparse`, `--mutate=wrongexpect`, `--expect=none`,
  and `--guard=all`, which asks for a point the cache lacks), each ending `exit 1`. The two passing replays are
  `phase2/nonradial/i115_replay_output.txt`.
- `cache/`: the per-evaluation caches (`winding2_cache_<tag>.pkl`, `zerilli_zeros_cache_<tag>.pkl`), restart-safe. Copies of
  every such file in the `cache/` of I5-rpi5, I54-rpi5, I115-rpi5, I121-win and I124-rpi5, so the source folders are never
  written. `cache_sources.sha256` has the sha256 and source path of each of the 65 copied files, and of four files not
  copied (below). The cache name does not contain the guard, so a guard-all run reuses the cached points and adds the ones
  the stricter rule asks for. The cache of s1 at l = 5 (387 points, from #115's guard-all run) is copied and has no job.
- `<job>.log`: the script's output. The collector reads these.

## Four caches that exist in two sources

`zerilli_zeros_cache_eps-1_w0.7603_l2_0.1_2.0_2.5.pkl` and its `_flat`, `_mlshift` and `_mnonorm` variants are in both
I121-win/cache (Windows, #121) and I124-rpi5/cache (this Pi, #124). Each pair holds the same points (67, 67, 67 and 65) with
values that differ by at most 1.3×10⁻¹² relative between the two machines, so the bytes differ. The task stopped there and
the coordinator decided: copy the I121-win versions, since `jobs.txt` names I121-win as their source and the guard-1
values are #121's. `cache_sources.sha256` records the I124-rpi5 hashes as "not copied: same points, cross-machine
difference ≤ 1.3e-12". They serve `z_p7603_l2`, `z_mut_reverse`, `z_flat`, `z_mut_lshift` and `z_mut_nonorm`.

## Result

`python collect_i126.py <this folder> > i126_guard_output.txt` exits 0 (`phase2/nonradial/i126_guard_output.txt`, code branch
`wip/i126-guard-all`). Its last line: "RESULT: all rows complete, every planted check passed, no count changed, every control
as required".

| | |
|---|---|
| boxes recounted at `--guard=all` | 61 (31 `w_*`, 30 `z_*`) |
| counts unchanged from guard 1 | 61 of 61 |
| planted checks PASS | 61 of 61 |
| largest phase step, `w_*` | 0.40 rad |
| controls as required | 5 of 5 |
| exit codes of the 66 jobs | 0, except `w_mut_reverse`, `z_mut_lshift`, `z_mut_nonorm`, `z_mut_reverse` (1, as the controls require) |
| process time, all jobs | 12.06 h in 8.77 h of wall time, 2026-11-21 00:49 to 2026-11-21 09:35 |
| cache points | 6922 before, 9003 after, 2081 new in 65 files (`summary.txt`) |

Walls, evaluations and new cache points per job and per cache: `summary.txt`, from `summarize_i126.py` (run from this
folder with the venv's python). Collector mutations (`noplant`, `shift`, `changed`, `noguard`, `control`), each into `collect_mutate_<name>.log`: exit codes 1, 1, 1, 1, 1.
