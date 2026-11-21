# I120-win: logs and eigenvalue arrays of #94's B-spline check of #75's tanh spectra, sectors m = 23/2 to 41/2 at #94's base sizes

Machine: win (surface-laptop-4, Windows 11, 8 logical CPUs, 32 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/120

## Code and environment

Code: worktree `negative-mass-i120` (beside this clone) on branch `wip/i120-high-m` at ad62a25 (the script at df15164 with
main merged in), `notes/warp/tanh_spectrum_check.py`, run from the repository root, unmodified.

Python: `negative-mass-venv314\Scripts\python.exe`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1 (the pinned
requirements.txt). Every run has `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1` and `MKL_NUM_THREADS=1`, below-normal
priority, and is launched detached with `start`. At most two solve processes at a time. A second one starts only while
choptuik-large-d's processes together use under 4 cores (CPU-seconds delta over 10 s).

Sizes: #94's base sizes, with no `--fnth` or `--fh`, and `--solver=arpack` (default `--floor=0.07`). Expected n, from the
script's knot rules, the same at sigma R = 2 and 4:

| m | 23/2 | 25/2 | 27/2 | 29/2 | 31/2 | 33/2 | 35/2 | 37/2 | 39/2 | 41/2 |
|---|---|---|---|---|---|---|---|---|---|---|
| n, A | 10868 | 11544 | 12464 | 13104 | 13846 | 14520 | 15210 | 16262 | 17088 | 17836 |
| n, B | 14344 | 15548 | 16262 | 17444 | 18300 | 19074 | 20352 | 21276 | 22624 | 23484 |

MS is `11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5` (m = 23/2 to 41/2).

## Plan

1. `planted.log`: `--part=planted --ms=11.5,20.5 --solver=arpack`. Must exit 0, before anything else.
2. `pilot-s4-B-m20.5.log`: `--part=solve --sigma=4 --disc=B --ms=20.5 --solver=arpack --out=eig`, the largest matrix
   (n = 23484), with its time and peak memory. Stop condition: more than 1 h.
3. `solve-s<sigma R>-<disc>.log`: `--part=solve --sigma=<sigma R> --disc=<A or B> --ms=MS --solver=arpack --out=eig`, for
   (4, B) (reuses the pilot's m = 41/2 file), (4, A), (2, B), (2, A).
4. `highm.log`: `--part=highm --out=eig --ms=MS` (the same as `notes/warp/tanh_spectrum_check_high_m_output.txt` in the
   code repository). `highm-mutate-bump.log`: the same with `--mutate=bump`, which must exit 1 with a failed `fall` check.

## Files

- `eig/s<sigma R>_<disc>_m<2m>.npz`: the ARPACK eigenvalues `mu` of S^-1 M (not times v_c) of one sigma R, one
  discretisation and one half-integer m = J_z, down to |mu| v_c = 0.07, with `vc`, `n`, `h`, `nth`, `rout`, `q`, `fnth`,
  `fh`, `solver` and the worst residual `res`.
- `jobs.txt`, `make_launchers.py`: one job per line, and the script that writes `job_<job>.cmd` and `go_<job>.cmd` from
  it. `go_` starts `job_` with `start /BELOWNORMAL /MIN`, and `job_` sets the thread variables, runs the command from the
  checkout root and writes `<job>.log.exit` with the exit code. Paths are relative to this folder (`%~dp0`).
- `<log>.exit`: the exit code of the run that wrote `<log>`.
- `queue.ps1`, `queue.log`: starts the solve jobs in order, a second only while choptuik-large-d uses under 4 cores, and
  restarts a job that dies (log kept as `<job>.died<N>.log`). `cores.log` holds each reading.
- `memory-sampler.log`: working set, peak working set and CPU time of each compute process once a minute, and the
  machine's free memory, written by `sample.ps1`.

## Outcome

Every run exited 0 except `--mutate=bump` and the extra `below` control, which must fail and did.

| run | exit | wall | peak working set (sampled each minute) |
|---|---|---|---|
| planted, m = 23/2 and 41/2, n = 10868 and 17836 | 0 | 46 s | not sampled (the sampler lists processes above 100 MB) |
| pilot, sigma R = 4, B, m = 41/2, n = 23484 | 0 | 76 s | 1.5 GiB |
| solve sigma R = 4, B (m = 41/2 from the pilot) | 0 | 273 s | 1.4 GiB |
| solve sigma R = 4, A | 0 | 208 s | 1.1 GiB |
| solve sigma R = 2, B | 0 | 365 s | 1.5 GiB |
| solve sigma R = 2, A | 0 | 217 s | 1.1 GiB |
| `highm` (`highm.log`, same as `notes/warp/tanh_spectrum_check_high_m_output.txt`) | 0 | 0 s | |
| `highm --mutate=bump` (`highm-mutate-bump.log`) | 1 | 0 s | |
| extra control, `highm` on #118's m = 19/2 and 21/2 files (`highm-control-below.log`) | 1 | 0 s | |

A sector took 11 to 79 s. ARPACK kept 64 eigenvalues per sector, down to |mu| v_c = 0.0336 to 0.0495, all below the
`--floor=0.07`, so k was never doubled, at residuals of 2e-14 or less. The solves ran two at a time from 18:35 to 18:45 on
2026-11-20, started with choptuik-large-d at 1.51, 1.20 and 1.19 cores (`cores.log`). The machine's free memory stayed
between 23.7 and 25.9 GiB. No process was stopped and none died (`queue.log`).

`highm.log`: 42 checks, all pass. `highm-mutate-bump.log`: exit 1, four failed checks, `fall` at both sigma R, and `ABhigh`
at m = 33/2 at both sigma R (the mutation changes A's value only, so A and B differ there by 6e-2). The extra control is
read-only: `--part=highm --out=../I118-win/eig --ms=9.5,10.5`. It has no sector files of this task and shows `below`
failing on real data (m = 19/2 and 21/2 against 0.0830 and 0.0944). The script has no `--mutate` that fires `below`.

- `trend.py`, `trend.log`: written by the runner, reads `eig/` only. Per sector, the signed (A - B) / A, m |mu| v_c, its
  step, the local exponent d ln|mu| / d ln m, the margin to the line, ARPACK's count and smallest modulus. Not part of the
  script's checks.

Derived results (the table, the criteria and the trend) are in the code repository at
`notes/warp/tanh_spectrum_check.md`, section "Sectors m = 23/2 to 41/2 (#120)", on branch `wip/i120-high-m`.
