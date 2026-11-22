# I122-rpi5: logs and evaluation caches of #122's checks that the Zerilli column is D's only pole source

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/122

## Code and environment

Code: worktree `~/Source/negative-mass-i122` on branch `wip/i122-factors`, `phase2/nonradial/d_factors.py` (new), run from
`phase2/nonradial`. The jobs ran 9f34847 until 13:12, then the working tree that became 2222a98 (adds the rtol suffix of the
store files, both stencil Laplacians in the `harm` lines and the `mean` part), and the last output run (`done/final_output.rc`, `final_output.err`) is 7ace97a (adds `--rho`, prints the raw folder as given). It imports `polar_solver.py`, `background.py` and `collect_i126.py` (for the job list) unmodified.

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
| `mean` | mean value property of arg D on a circle (added after `harm` failed), `--rho` the radius | `nonholo` |

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

## Results

Per-job logs are `<name>.log` with the exit code in `done/<name>.rc`:

| jobs | what | exit |
|---|---|---|
| `gap`, `factors_static` | `gap`, `order`, `cols`, planted controls; `moncrief`, `jpoly` | 0 |
| `gap_mut_branch`, `gap_mut_cols`, `factors_mut_singularT`, `factors_mut_jnonlin` | mutations of those checks | 1 (each fails its check) |
| `pole_z`, `pole_s` | pole planted in the Zerilli column and in the scalar plane's first column of `n1_l2` | 0 (winding -2.0000 each) |
| `pole_mut_nophase`, `pole_mut_nogauge`, `pole_mut_reverse` | mutations of `pole` | 1 |
| `factors_<box>` | `harm` in six boxes | 1 in five boxes, 0 in `n1_l4` |
| `harm_diag_p7603_l2_rtol1e-10`, `..._rtol1e-12` | the same check in `p7603_l2` at tighter rtol (own store files) | 1 |
| `factors_mut_nonholo` | mutation of `harm` | 1 |
| `norm_<box>`, `norm_mut_noproj` | eigenvector normalisation in six boxes; its mutation | 0; 1 |
| `axis_n3_l2`, `axis_n3_l3`, `axis_mut_reverse`, `axis_mut_wrongq` | n3 boxes with the continued column; mutations | 0, 0; 1, 1 |
| `mean_<box>`, `mean_mut_nonholo` | the mean value check | 1 in `p085_l3` and `n3_l2`, 0 in the others; mutation 1 |
| `final_output` (`done/final_output.rc`, `final_output.err`) | one run of all six parts from these caches, written to `phase2/nonradial/d_factors_output.txt` | 1 (`harm` and `mean` fail) |

`queue.log` has the start and end of every job. `jobs.txt` holds the arguments, including the `mean_rho*` lines of the
convergence study in `listF_after_report.txt`, which was held back until the required parts were reported.
