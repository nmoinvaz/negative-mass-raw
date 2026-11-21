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

- `queue.ps1`, `queue.log`: started (4, B), (4, A), (2, B), (2, A) in that order, a second one only while choptuik-large-d
  used under 4 cores, and only while every finished job had exited 0. `report-wide.log` and `report-wide-mutate-next.log`
  have their `.exit` files; the first is also `notes/warp/tanh_spectrum_check_wide_output.txt` in the code repository.

## Outcome

Every run exited 0 except `--mutate=next`, which must exit 1 and did (22 failed `next` checks, no others).

| run | exit | wall | peak working set (sampled each minute) |
|---|---|---|---|
| planted, m = 19/2, 21/2, n = 72240, 78010 | 0 | 2813 s | 6.5 GiB |
| pilot, sigma R = 4, B, m = 21/2, n = 102414 | 0 | 1591 s | 8.7 GiB |
| solve sigma R = 4, B (m = 21/2 from the pilot) | 0 | 1515 s | 8.2 GiB |
| solve sigma R = 4, A | 0 | 2564 s | 6.5 GiB |
| solve sigma R = 2, B | 0 | 2594 s | 8.7 GiB |
| solve sigma R = 2, A | 0 | 2277 s | 6.5 GiB |
| report, #118 and #111 files | 0 | 0 s | |
| report, `--mutate=next` | 1 | 0 s | |

Two solves ran at once from 16:22 to 17:30 on 2026-11-20, started when choptuik-large-d used 1.2 to 1.7 cores. The
machine's free memory stayed between 12.9 and 26.7 GiB. No process was stopped.

Derived results (the four new table rows, the checks and the speed-bound lines) are in the code repository at
`notes/warp/tanh_spectrum_check.md`, section "Wider windows (#111)", on branch `wip/i118-wide-m19-21`.
