# I7-win2: non-radial scans and winding counts of the ω = 0.70 and 0.85 phantom stars

Machine: win2 (Windows desktop, 20 cores, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/7

Worktree: `C:\Users\nathan\Source\negative-mass-i7`, branch `wip/i7-phantom-scans` from origin/main 606874f, with two
commits (f9907f7 `convergence.py` takes ω as an optional argument, 731cac8 `control_winding2.py` finds its modules beside
the script). The jobs run from `phase2/nonradial` of that worktree.

Python: `C:\Users\nathan\Source\negative-mass-venv`, Python 3.12.8, numpy 2.5.4, scipy 1.18.1, sympy 1.14.0, mpmath
1.3.0. The queue sets `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`, so each job uses one core per process.

## What runs

One detached queue (`queue.py`, started by `launch.cmd`) runs the jobs in this order, each appending to `<job>.log`.
`scan_*` jobs set `TAG=_n100`. The control must print winding +1.0000 around the QNM and 0 displaced, otherwise the
queue stops (`STOPPED_control.txt`). A job that exits non-zero is logged in `queue.log` and the queue continues.

| job | command |
|---|---|
| control | `control_winding2.py` |
| scan_085_l3 (pilot) | `scan_growing.py -1 0.85 3 100 1e-3 2000` |
| scan_070_l2 | `scan_growing.py -1 0.70 2 100 1e-3 300` |
| scan_070_l3 | `scan_growing.py -1 0.70 3 100 1e-3 1000` |
| scan_085_l2 | `scan_growing.py -1 0.85 2 100 1e-3 300` |
| wind_070_l2, wind_070_l3, wind_085_l2, wind_085_l3 | `winding2.py -1 <w> <l> 0.1 2.0 2.5` |
| conv_070_l2, conv_070_l3, conv_085_l2, conv_085_l3 | `convergence.py <l> <w>` |

## Files

- `queue.py`, `launch.cmd`, `memwatch.ps1`: the launcher, and a reporter that logs the queue's cpu and memory. Nothing
  here stops or kills a process.
- `scan_085_l2_hang.txt`: why `scan_085_l2` did not finish in the queue (a pool worker crashed). `diag_085_l2.py`,
  `.log`, `.jsonl`: a serial run of D(g) on that scan's grid. `retry_scan_085_l2.py`, `retry.log`: the one retry of the
  scan and its comparison with the diagnostic (`--selftest` shows that the comparison can fail). `retries.py` runs
  `python -X faulthandler -u convergence.py 2 0.85` and then that scan, one after the other.
  `retry_conv_085_l3.py` then runs `python -X faulthandler -u convergence.py 3 0.85` once, and `compare_conv_rows.py`
  compares a convergence rerun's printed rows with the first run's, digit for digit (`--selftest` shows it can fail).
- `queue.log`: start, exit code and time of every job. `queue_done.txt` lists the jobs that finished.
- `<job>.log`: the job's output. `memwatch.log`: one line per minute, the queue's process tree.
- `scan_eps-1_w0.7_l*_n100.csv`, `scan_eps-1_w0.85_l*_n100.csv`: the real-γ scans (γ, D).
- `winding2_cache_eps-1_w0.7_*.pkl`, `winding2_cache_eps-1_w0.85_*.pkl`: the per-evaluation caches of the windings.
