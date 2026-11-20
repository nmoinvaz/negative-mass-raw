# I111-win: logs and eigenvalue arrays of #94's B-spline check of #75's tanh spectra, widened by size factors and ARPACK, sectors m = 1/2 to 17/2

Machine: win (surface-laptop-4, Windows 11, 8 logical CPUs, 32 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/111

## Code and environment

Code: `C:\Users\nathan\Source\negative-mass-i111` on branch `wip/i111-wide-windows` at 0e3170f,
`notes/warp/tanh_spectrum_check.py`, run from the repository root, unmodified.

Python: `negative-mass-venv314\Scripts\python.exe`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1 (the pinned
requirements.txt). Every run has `OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1`, below-normal priority, at most two
solve processes at a time, launched detached with `start`.

Sizes: `WIDE` is `--solver=arpack --floor=0.07 --fnth=4 --fh=0.4`. The `base` runs use #94's sizes (no size factors).

## Files

- `base/s<sigma R>_<disc>_m1.npz`, `base-s2A.log`, `base-s4B.log`: ARPACK at #94's sizes, `--part=solve --sigma=2 --disc=A`
  and `--sigma=4 --disc=B`, `--ms=0.5 --solver=arpack`.
- `compare.log`: `--part=compare --out=base --ref=<I94-win>/eig`, ARPACK against #94's stored dense spectra. Must exit 0.
- `compare-mutate-compare.log`: the same with `--mutate=compare`. Must exit 1.
- `planted.log`: `--part=planted` with `--ms=0.5,...,8.5` and WIDE. Must exit 0.
- `control-kterm.log`: `--part=planted --ms=0.5` WIDE `--mutate=kterm`. Must exit 1.
- `pilot-s4B-m8.5.log`: `--part=solve --sigma=4 --disc=B --ms=8.5` WIDE, the largest matrix (n = 93852 on the
  coordinator's Mac), with its time and peak memory. Stop condition: more than 3 h or more than 16 GB.
- `solve-s<sigma R>-<disc>.log`: `--part=solve --sigma=<sigma R> --disc=<A or B>` with `--ms=0.5,...,8.5` and WIDE, one
  process per (sigma R, disc), two at a time.
- `eig/s<sigma R>_<disc>_m<2m>.npz`: the ARPACK eigenvalues `mu` of S^-1 M (not times v_c) of one sigma R, one
  discretisation and one half-integer m = J_z, down to |mu| v_c = 0.07, with `vc`, `n`, `h`, `nth`, `rout`, `q`,
  `fnth`, `fh`, `solver` and the worst residual `res`.
- `report-wide.log`, `report-i94.log`, `report-wide-mutate-next.log`: the three reports of the task, with their `.exit`
  files. The first two are also saved as `notes/warp/tanh_spectrum_check_wide_output.txt` and
  `notes/warp/tanh_spectrum_check_output.txt` in the code repository.
- `memory-sampler.log`: the working set, peak working set and CPU time of each compute process once a minute, and the
  machine's free memory, written by `sample.ps1`.
- `queue.ps1`, `queue.log`: started (2, B) and (2, A) as slots freed (at most two solve processes at a time), only
  while every finished job had exited 0.
- `job_<name>.cmd` and `go_<name>.cmd`: the launchers. `go_` starts `job_` with `start /BELOWNORMAL /MIN`, and `job_`
  sets `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1` and `MKL_NUM_THREADS=1`, runs the command from the checkout root
  and writes `<log>.exit` with the exit code.
- `<log>.exit`: the exit code of the run that wrote `<log>`.

Outcome: the solves, `compare` and `planted` exited 0, and `--mutate=compare` and `--mutate=kterm` exited 1, as
required. The wide report and the regenerated #94 report exit 1 on `AB` failures (sigma R = 4, m = 19/2 and 21/2 in the
wide one, from #94's files; m = 9/2 to 21/2 in #94's). `--mutate=next` exits 1.

Derived results (tables, the speed bound lines, notes) are in the code repository at `notes/warp/tanh_spectrum_check.md`
on branch `wip/i111-wide-windows`.
