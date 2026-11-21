# I125-win: eigenvalue arrays and logs of #75's spectral code at m = 21/2, 23/2, 29/2, 35/2 and 41/2, sigma R = 2 and 4

Machine: win (surface-laptop-4, Windows 11, 8 logical CPUs, 32 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/125

## Code and environment

Code: worktree `negative-mass-i125` (beside this clone) on branch `wip/i125-highm75` at 5ed8160,
`notes/warp/tanh_spectrum.py` (#75's spectral code) and `notes/warp/tanh_spectrum_highm.py` (the comparison with
#120), run from the repository root, unmodified.

Python: `negative-mass-venv314\Scripts\python.exe`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1 (the pinned
requirements.txt). Every run has `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1` and `MKL_NUM_THREADS=1`, `--procs=1`,
below-normal priority, and is launched detached with `start`. At most two processes (each is a main process and one
worker). A second one starts only while choptuik-large-d's processes together use under 4 cores (CPU-seconds delta over
10 s, `cores.log`). Memory is reported only: nothing stops or kills a process because of it (`memory-sampler.log`,
once a minute, worker processes included).

Sizes: the script's defaults (no `--quick`). Discretisation A has dK = 28, p = 80 (sigma R = 2) or 100 (sigma R = 4),
Lmap = 2, npan = 160. Discretisation B has dK = 38, p = 90 or 110, Lmap = 3, npan = 240. These are #75's sizes.
`--raw` writes one `tanh_sigma{S}_m{M}.npz` per sector (`vc`, `muA`, `muB`, every eigenvalue of S^-1 M in A and B) to
`eig/`. #120's B-spline files are in `../I120-win/eig`.

## Sectors (10)

sigma R = 2 and 4, m = 21/2 (reproduction of #75's printed values), 23/2, 29/2, 35/2 and 41/2.

## Plan

1. `pilot-s4-m20.5.log`: `--part=vc,planted,tanh --procs=1 --sigmas=4 --ms=20.5 --raw=eig`, the hardest sector, alone,
   with its time, exit code, leading |mu| v_c of A and B and peak memory. Stop condition: more than 30 min, then stop
   it and report before step 2.
2. `solve-s2.log`: `--part=vc,planted,tanh --procs=1 --sigmas=2 --ms=10.5,11.5,14.5,17.5,20.5 --raw=eig` and
   `solve-s4.log`: `--part=vc,planted,tanh --procs=1 --sigmas=4 --ms=10.5,11.5,14.5,17.5 --raw=eig`, one or two at a
   time under the thread rule (`queue.ps1`). A process that dies restarts with the same command (the dead log kept as
   `<job>.died<N>.log`).
3. When all three have exited:
   - `highm.log`: `tanh_spectrum_highm.py --raw=eig --ref=../I120-win/eig` (the same as
     `notes/warp/tanh_spectrum_highm_output.txt` in the code repository). The exit code is reported as it is.
   - `highm-mutate-plant.log` and `highm-mutate-conv.log`: the same with `--mutate=plant` and `--mutate=conv`. Each
     must exit 1 with only its target failing beyond what the unmutated run fails: `vs120` at sigma R = 4,
     m = 29/2 (plant) and `conv` at sigma R = 2, m = 41/2 (conv).

## Files

- `jobs.txt`, `make_launchers.py` (writes `job_<job>.cmd` and `go_<job>.cmd`), `queue.ps1` (starts the jobs under the
  thread rule), `sample.ps1` (the memory sampler), `runs.py` (per-job wall, per-sector time and peak memory).
- `<job>.log` is a job's stdout, `<job>.log.exit` its exit code, `cores.log` the readings before each second start,
  `queue.log` the queue's events, `memory-sampler.log` the sampler.
- `eig/`: the sector files.
