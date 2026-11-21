# I122-rpi5: logs and evaluation caches of #122's checks that the Zerilli column is D's only pole source

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/122

## Code and environment

Code: worktree `~/Source/negative-mass-i122` on branch `wip/i122-factors`, `phase2/nonradial/d_factors.py` (new), run from
`phase2/nonradial`. It imports `polar_solver.py`, `background.py` and `collect_i126.py` (for the job list) unmodified.

Python: `~/Source/negative-mass-venv314/bin/python`. Every run is `nice -n 10` with `OMP_NUM_THREADS=1` and
`OPENBLAS_NUM_THREADS=1` (single-threaded), detached with `setsid nohup`. At most two processes at a time, and a second one
starts only while the 15-minute load average is below 4. Memory is reported, never a stop condition.

## What is checked

Whether D, as `polar_solver.PolarProblem.D` computes it with `winding2.py`'s phase factor, has a pole source other than the
Zerilli column in the counted boxes of RESULTS.md §5, §5.1, §3a and §5.3 (the 61 boxes of `I126-rpi5/jobs.txt`). Five parts
of `d_factors.py` (`--part=`), each with the mutation that must make it fail:

| part | checks | mutations |
|---|---|---|
| `factors` | the table of D's factors; `moncrief`, `jpoly`; `harm`: arg D is harmonic (Laplacian at three points of six boxes) | `singularT`, `jnonlin`, `nonholo` |
| `gap` | `gap`, `order`, `cols` in the 61 boxes; planted boxes around s = i(1 - w), i(1 + w) | `branch`, `cols` |
| `norm` | D unchanged when each eigenvector of `np.linalg.eig` in `scalar_plane` is scaled randomly | `noproj` |
| `pole` | a pole planted in the Zerilli column and in the scalar plane's first column of `n1_l2`, recounted | `nophase`, `nogauge`, `reverse` |
| `axis` | `n3_l2`, `n3_l3` with q of `zerilli_zeros.py --axis` in D | `reverse`, `wrongq` |

The criteria are fixed in the script's docstring before any run. Pass and fail are printed per check; the exit status is 1
when a check fails and 3 when the stop condition (`--stop`) ended the run.

## Files

- `jobs.txt`: `name|arguments` of `d_factors.py`; `launch_I122_gated.sh LISTFILE` runs the jobs of a list file (`controls.txt`,
  `pilot.txt`, `main.txt`, `mutations.txt`) at `nice -n 10`, one process, a second only while the 15-minute load is below 4,
  `<name>.log` and `done/<name>.rc` per job. `memwatch.sh` reports load and memory only.
- `d_factors_cache_<part>_<box>.pkl`: every D evaluation of a part and box, keyed by its point, so that a rerun replays from them.
- `<name>.log`: the output of each job.

The caches and logs of `I126-rpi5` (the box caches and the `winding2.py` logs) and `I123-rpi5` (the `--axis` logs) are read in
place and never written.
