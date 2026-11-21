# I121-win: logs and caches of #121's counts of the zeros of Z(r_m; s), the poles of D, in the boxes of RESULTS.md §5 and §5.1

Machine: win (surface-laptop-4, Windows 11, 8 logical CPUs, 4 physical cores, 32 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/121

## Code and environment

Code: worktree `negative-mass-i121` (beside this clone) on branch `wip/i121-zerilli-zeros` at d801d1e,
`phase2/nonradial/zerilli_zeros.py` and `collect_i121.py`, unmodified, run from `phase2/nonradial`.

Python: `negative-mass-venv314\Scripts\python.exe`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1 (the pinned
requirements.txt). Every run has `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1` and `MKL_NUM_THREADS=1` (the script is
single-threaded), `PYTHONIOENCODING=utf-8`, below-normal priority, and is launched detached with `start`. At most two
processes at a time. A second one starts only while choptuik-large-d's processes together use under 4 cores
(CPU-seconds delta over 10 s, one reading per start in `cores.log`). Memory is reported, never a stop condition.

## Files

- `jobs.txt`: the 25 lines `job|arguments` of `python collect_i121.py --jobs`. Job `<job>` runs
  `python -u zerilli_zeros.py <arguments> --cachedir=<this folder>\cache`.
- `make_launchers.py`: writes `job_<job>.cmd` and `go_<job>.cmd` (as in #118's folder) from `jobs.txt`.
  Each job writes `<job>.log` and, when it ends, its exit code in `<job>.log.exit`.
- `queue.ps1 <job> ...`: starts the listed jobs in order, two at a time under the rule above, and restarts a job whose
  log has no final line (a dead process) with the same command, keeping the dead log as `<job>.died<N>.log`. A nonzero
  exit with a final line is a result (a failed check, or a mutation doing its job), not a death. Records in
  `queue.log` and `cores.log`.
- `cache/`: one `zerilli_zeros_cache_<tag>.pkl` per box, the values of Z(r_m; s) at the contour points. `mut_reverse`
  and `p7603_l2` share one (the reversed contour of the same box), so whichever runs second reports fewer new
  evaluations and a shorter time.

## Plan

1. Controls on the stored box: `flat` (must end "all checks passed"), then `mut_reverse`, `mut_nonorm` and
   `mut_lshift` (each must end "FAILED:" naming `plant`, `holo` and `column`, in that order).
2. Pilot: `n1_l3`, the hardest box (R_z about 10^6). Stop condition: over 1 h.
3. The other 20 box jobs.
4. `python collect_i121.py <this folder> > i121_zeros_output.txt` (exit status as it comes), then `--mutate=box` and
   `--mutate=control` into `collect-mutate-box.log` and `collect-mutate-control.log` here (each must exit 1).

## Result

All 21 boxes count 0 zeros of Z(r_m; s) with the planted zero returned and `all checks passed` (exit 0), so the zeros of
D equal the winding of D, 0, in each. The controls ended as required: `flat` passes, `mut_reverse` fails `plant`,
`mut_nonorm` fails `holo`, `mut_lshift` fails `column`. `collect_i121.py` on this folder exits 0 and its output is
`phase2/nonradial/i121_zeros_output.txt` of the code branch; `--mutate=box` and `--mutate=control` exit 1
(`collect-mutate-box.log`, `collect-mutate-control.log`, with their exit lines in `*.log.exit`).

| step | jobs | started | ended |
|---|---|---|---|
| controls | `flat`, `mut_reverse`, `mut_nonorm`, `mut_lshift` | 18:00:21 | 18:02:32 |
| pilot | `n1_l3` (R_z = 1.0e6), 225 s, 146 s of it the count | 18:02:38 | 18:06:59 |
| boxes | the other 20, two at a time | 18:07:08 | 18:20:15 |

Times are the machine's local time on 2026-11-20. No process died (no `*.died*.log`), and the queue never waited on
choptuik-large-d. Readings in `cores.log` (taken before each start): choptuik-large-d at most 1.78 cores, our one
running process at most 81 MiB of working set, free memory at least 25.3 GiB.

## Notes

- `mut_reverse` and `p7603_l2` share one cache file (the reversed contour of the same box), and `mut_reverse` ran
  first. So `p7603_l2`'s log shows 67 evaluations and 0 s: 63 of its points were already in the cache, and the 10 s it
  took belongs to `mut_reverse`.
- `queue.ps1` leaves its loop when no job is running any more, so it never checks the log of a job that ends after the
  last one started. Those jobs (`mut_nonorm`, `mut_lshift`, `n1_l3`, `s3_l3`) were checked by hand: `n1_l3` and `s3_l3`
  end `all checks passed` with exit 0, the two mutations end `FAILED:` with exit 1, as the collector requires.
