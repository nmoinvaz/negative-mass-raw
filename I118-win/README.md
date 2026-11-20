# I118-win: logs and eigenvalue arrays of #94's B-spline check of #75's tanh spectra, sectors m = 19/2 and 21/2 re-solved at #111's wide sizes

Machine: win (surface-laptop-4, Windows 11, 8 logical CPUs, 32 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/118

## Code and environment

Code: worktree `negative-mass-i118` (beside this clone) on branch `wip/i118-wide-m19-21` at 69f5a61 (main),
`notes/warp/tanh_spectrum_check.py`, run from the repository root, unmodified.

Python: `negative-mass-venv314\Scripts\python.exe`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1 (the pinned
requirements.txt). Every run has `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1` and `MKL_NUM_THREADS=1`, below-normal
priority, and is launched detached with `start`. One solve process at a time. A second one starts only while
choptuik-large-d's processes together use under 4 cores (CPU-seconds delta over 10 s).

Sizes: `WIDE` is `--solver=arpack --floor=0.07 --fnth=4 --fh=0.4`, as in #111. Expected n (from the script's knot rules):

| sector | A, sigma R = 2 | B, sigma R = 2 | A, sigma R = 4 | B, sigma R = 4 |
|---|---|---|---|---|
| m = 19/2 | 72240 | 94866 | 73640 | 96822 |
| m = 21/2 | 78010 | 102414 | 78010 | 102414 |

## Plan

1. `planted.log`: `--part=planted --ms=9.5,10.5` WIDE. Must exit 0, before anything else.
2. `pilot-s4B-m10.5.log`: `--part=solve --sigma=4 --disc=B --ms=10.5` WIDE `--out=eig`, the largest matrix with its time and
   peak memory. Stop condition: more than 3 h.
3. `solve-s<sigma R>-<disc>.log`: `--part=solve --sigma=<sigma R> --disc=<A or B> --ms=9.5,10.5` WIDE `--out=eig`, for
   (4, B) (reuses the pilot's file), (4, A), (2, B), (2, A).
4. `report-wide.log`: `--part=report --out=eig,../I111-win/eig` (the same as `notes/warp/tanh_spectrum_check_wide_output.txt`
   in the code repository). `report-wide-mutate-next.log`: the same with `--mutate=next`, which must exit 1.

## Files

- `eig/s<sigma R>_<disc>_m<2m>.npz`: the ARPACK eigenvalues `mu` of S^-1 M (not times v_c) of one sigma R, one
  discretisation and one half-integer m = J_z, down to |mu| v_c = 0.07, with `vc`, `n`, `h`, `nth`, `rout`, `q`, `fnth`,
  `fh`, `solver` and the worst residual `res`.
- `job_<name>.cmd` and `go_<name>.cmd`: the launchers. `go_` starts `job_` with `start /BELOWNORMAL /MIN`, and `job_` sets
  the thread variables, runs the command from the checkout root and writes `<log>.exit` with the exit code. Paths are
  relative to this folder (`%~dp0`).
- `<log>.exit`: the exit code of the run that wrote `<log>`.
- `memory-sampler.log`: working set, peak working set and CPU time of each compute process once a minute, and the machine's
  free memory, written by `sample.ps1`. `cores.log`: choptuik-large-d's CPU use over 10 s before each launch.

Status: in progress.
