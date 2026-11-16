# I94-win: logs and eigenvalue arrays of the independent B-spline check of #75's tanh spectra in every J_z sector

Machine: win (surface-laptop-4, Windows 11, 8 logical CPUs, 32 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/94

## Code and environment

Code: `C:\Users\nathan\Source\negative-mass-i94` on branch `wip/i94-sector-check` at 6f7d199,
`notes/warp/tanh_spectrum_check.py`, run from the repository root, unmodified.

Python: `negative-mass-venv314\Scripts\python.exe`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1 (the pinned
requirements.txt). Every run has `OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1`, below-normal priority, at most four
processes at a time.

## Files

- `planted.log`: `--part=planted`, the planted tau = 6/(1 + r^2) in every sector, discretisation A. Must exit 0.
- `control-kterm.log`, `control-half.log`: `--part=planted --ms=0.5 --mutate=kterm` and `--mutate=half`. Each must exit 1.
- `pilot-s4B-m10.5.log`: `--part=solve --sigma=4 --disc=B --ms=10.5`, the largest matrix, with its time and peak memory.
- `solve-s<sigma R>-<disc>.log`: `--part=solve --sigma=<sigma R> --disc=<A or B>`, one process per (sigma R, disc).
- `eig/s<sigma R>_<disc>_m<2m>.npz`: all Galerkin eigenvalues `mu` of S^-1 M (not times v_c) of one sigma R, one
  discretisation and one half-integer m = J_z, with `vc`, `n`, `h`, `nth`, `rout` and `q`.
- `report.log`: `--part=report`, the tables and checks, also saved as `notes/warp/tanh_spectrum_check_output.txt` in the
  code repository.
- `memory-*.log`: the sampled working set and CPU time of each solve process, for the progress posts.

Derived results (tables, the speed bound line, notes) are in the code repository at `notes/warp/tanh_spectrum_check.md`
on branch `wip/i94-sector-check`.
