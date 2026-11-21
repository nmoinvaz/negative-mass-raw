# I127-win: logs and eigenvalue arrays of #94's B-spline check of #75's tanh spectra, sigma R = 2, m = 19/2 and 21/2 at k = 512

Machine: win (surface-laptop-4, Windows 11, 8 logical CPUs, 32 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/127

## Code and environment

Code: worktree `negative-mass-i127` (beside this clone) on branch `wip/i127-k512` at 4b9a8b9,
`notes/warp/tanh_spectrum_check.py`, run from the repository root, unmodified.

Python: `negative-mass-venv314\Scripts\python.exe`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1 (the pinned
requirements.txt). Every run has `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1` and `MKL_NUM_THREADS=1`, below-normal
priority, and is launched detached with `start`. At most two solve processes. A second one starts only while
choptuik-large-d's processes together use under 4 cores (CPU-seconds delta over 10 s, `cores.log`). Memory is reported
only: nothing stops or kills a process because of it (`memory-sampler.log`, once a minute).

Sizes: `NEW` is `--solver=arpack --floor=0.025 --k0=512 --kmax=512 --fnth=4 --fh=0.4`. #111, #118 and #119 used the same
`--fnth` and `--fh`, so n per sector is theirs: m = 19/2 A 72240, B 94866, and m = 21/2 A 78010, B 102414 at sigma R = 2.
`--k0=512 --kmax=512` makes ARPACK's doubling run once, at k = 512, and stop there whether or not the smallest |mu| v_c
is under the floor.

## Sectors (4)

- sigma R = 2, A and B: m = 19/2 and 21/2. These are the two windows still `floor` after #119 (k = 256 stopped at
  |mu| v_c = 0.0341 and 0.0330).

## Plan

1. `pilot-s2-B-m10.5.log`: `--part=solve --sigma=2 --disc=B --ms=10.5` NEW `--out=eig`, the largest matrix (n = 102414),
   run alone, with its time, k, smallest |mu| v_c and peak memory. Stop condition: more than 5 h, then stop it and report
   before step 2.
2. `solve-s2-B-m9.5.log`: `--part=solve --sigma=2 --disc=B --ms=9.5` NEW `--out=eig`, and `solve-s2-A-m9.5-10.5.log`:
   `--part=solve --sigma=2 --disc=A --ms=9.5,10.5` NEW `--out=eig`, one or two at a time under the thread rule
   (`queue.ps1`). A process that dies restarts with the same command (the dead log kept as `<job>.died<N>.log`);
   `solve` skips finished sectors.
3. When all four sectors have exited 0:
   - `report-wide.log`: `--part=report --out=eig,../I119-win/eig,../I118-win/eig,../I111-win/eig` (the same as
     `notes/warp/tanh_spectrum_check_wide_output.txt` in the code repository). The exit code is reported as it is.
   - `report-wide-mutate-floorup.log`: the same with `--mutate=floorup`, which must exit 1 with `match` failing in all 22.
   - `report-wide-mutate-real.log`: the same with `--mutate=real`, which must exit 1 with `noreal` and `sym` failing at
     sigma R = 2, m = 11/2 and nothing else beyond what the unmutated report fails.
   - `compare-i119.log`: `--part=compare --out=eig --ref=../I119-win/eig`, which must exit 0.
     `compare-i119-mutate-compare.log`: the same with `--mutate=compare`, which must exit 1.

## Files

- `eig/s2_<disc>_m<2m>.npz`: the ARPACK eigenvalues `mu` of S^-1 M (not times v_c) of one discretisation and one
  half-integer m = J_z, k = 512 of them, with `vc`, `n`, `h`, `nth`, `rout`, `q`, `fnth`, `fh`, `solver` and the worst
  residual `res`.
- `jobs.txt`, `make_launchers.py`: one line `<job>|<arguments>` per job, and the script that writes `job_<job>.cmd` and
  `go_<job>.cmd`. `go_` starts `job_` with `start /BELOWNORMAL /MIN`, and `job_` sets the thread variables, runs the
  command from the checkout root and writes `<job>.log.exit` with the exit code. Paths are relative to the folder.
- `queue.ps1 <job> ...`: starts the jobs in order under the thread rule, restarts a dead one (at most 3 times).
- `sample.ps1`: the memory sampler. `memory-sampler.log`: working set, peak and cpu of each solve, and free memory.
- `cores.log`: choptuik-large-d's cores at each launch of a second process, with our working set and the free memory.
- `runs.py`: per-job wall time, peak working set and the residual range of `eig/`.

## Run order

The pilot runs alone, launched by hand with `go_pilot-s2-B-m10.5.cmd`. When it has exited 0, one `queue.ps1` runs
`solve-s2-B-m9.5 solve-s2-A-m9.5-10.5`.
