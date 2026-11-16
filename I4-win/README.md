# I4-win: logs and partial files of the polar growing-mode scans, convergence variants and kappa_eff at l = 4, 5 and 6

Machine: win (surface-laptop-4, Windows 11, 8 logical CPUs, 32 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/4

## Code and environment

Code: `C:\Users\nathan\Source\negative-mass-i4` on branch `wip/i4-polar-l456` at 63682b6, `phase2/nonradial`, scripts
unmodified.

Python: `negative-mass-venv314\Scripts\python.exe`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1, sympy 1.14.0, mpmath 1.3.0
(the pinned requirements.txt). Every run has `OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1`, below-normal priority, and
at most 4 processes in all (`NPROC=4`), launched detached with `start`.

## Task

The phantom star omega = 0.7603 (M = -0.01458), polar modes, real growth rate gamma. For each l the scan covers
gamma in [1e-3, GMAX] on 100 log-spaced points, with GMAX above the point-mass rate k/(2|M|).

| l | k/(2\|M\|) | GMAX |
|---|---|---|
| 4 | 2058 | 3000 |
| 5 | 4801 | 6000 |
| 6 | 9602 | 12000 |

## Files

- `mini_bs.log`: `python mini_bs.py`, the known-QNM control (Mini BS I, l = 2). Must reproduce `mini_bs_output.txt`
  (sigma = 0.119519 - 5.35e-05 i).
- `scan_l{L}.log`: `NPROC=4 python scan_growing.py -1 0.7603 L 100 0.001 GMAX`, its stdout. The output
  `scan_eps-1_w0.7603_l{L}.csv` (gamma, D) is committed to the code repository, and the per-point
  `scan_eps-1_w0.7603_l{L}.partial.csv` (index, gamma, D) is kept here.
- `convergence_l{L}.log` and `convergence_l{L}_w0.7603.partial.csv`: `NPROC=4 GAMS=0.001,0.03,0.3,1,3,10,40,137,300,1000,GMAX
  python convergence.py L`, its stdout (also in the code repository as `convergence_l{L}_output.txt`) and its
  per-evaluation records (variant, gamma, D, seconds).
- `kappa_eff_l{L}.log`: `python kappa_eff.py L`, its stdout (also `kappa_eff_l{L}_output.txt` in the code repository,
  with `kappa_eff_l{L}_w0.7603.csv`).
- `progress.log`: the hourly cpu and memory samples of the python processes.
