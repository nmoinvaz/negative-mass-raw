# I119-win: logs and eigenvalue arrays of #94's B-spline check of #75's tanh spectra, 18 wide-size sectors re-solved at ARPACK floor 0.04

Machine: win (surface-laptop-4, Windows 11, 8 logical CPUs, 32 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/119

## Code and environment

Code: worktree `negative-mass-i119` (beside this clone) on branch `wip/i119-floor` at a123433,
`notes/warp/tanh_spectrum_check.py`, run from the repository root, unmodified.

Python: `negative-mass-venv314\Scripts\python.exe`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1 (the pinned
requirements.txt). Every run has `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1` and `MKL_NUM_THREADS=1`, below-normal
priority, and is launched detached with `start`. At most two solve processes. A second one starts only while
choptuik-large-d's processes together use under 4 cores (CPU-seconds delta over 10 s, `cores.log`). Memory is reported
only: nothing stops or kills a process because of it (`memory-sampler.log`, once a minute).

Sizes: `NEW` is `--solver=arpack --floor=0.04 --fnth=4 --fh=0.4`. #111 and #118 used `--floor=0.07` and the same
`--fnth` and `--fh`, so n per sector is theirs (#111's for m = 1/2 to 17/2, #118's for m = 19/2 and 21/2). The largest is
n = 102414 (B, m = 21/2).

## Sectors (18)

- sigma R = 2, A and B: m = 1/2, 3/2, ..., 21/2 (11 each).
- sigma R = 4, A and B: m = 9/2, 11/2, ..., 21/2 (7 each). m = 1/2 to 7/2 at sigma R = 4 are `match` in #111 and are not
  re-solved.

## Plan

1. `pilot-s4-B-m10.5.log`: `--part=solve --sigma=4 --disc=B --ms=10.5` NEW `--out=eig`, the largest matrix, with its
   time, k and peak memory. Stop condition: more than 4 h, then stop it and report before step 2.
2. `stage1-s2-A-m4.5.log`, `stage1-s2-B-m4.5.log`: `--part=solve --sigma=2 --disc=<A or B> --ms=4.5` NEW `--out=eig`. The
   one sector whose #111 window (0.0697) was not below #75's own (0.0667).
3. `solve-s<sigma R>-<disc>.log`: `--part=solve --sigma=<sigma R> --disc=<A or B> --ms=<full list>` NEW `--out=eig` for
   (2, B), (4, B), (2, A), (4, A). `solve` skips sectors already written, so each process gets its whole list. A process
   that dies restarts with the same command (`queue.ps1`, the dead log kept as `<job>.died<N>.log`).
4. `report-wide.log`: `--part=report --out=eig,../I118-win/eig,../I111-win/eig` (the same as
   `notes/warp/tanh_spectrum_check_wide_output.txt` in the code repository). `report-wide-mutate-floorup.log`: the same
   with `--mutate=floorup`, which must exit 1 with `match` failing in every sector.
5. `compare-i111.log` and `compare-i118.log`: `--part=compare --out=eig --ref=../I111-win/eig` and `--ref=../I118-win/eig`,
   each must exit 0. `compare-i111-mutate-compare.log`: the first with `--mutate=compare`, which must exit 1.

## Files

- `eig/s<sigma R>_<disc>_m<2m>.npz`: the ARPACK eigenvalues `mu` of S^-1 M (not times v_c) of one sigma R, one
  discretisation and one half-integer m = J_z, down to |mu| v_c below 0.04, with `vc`, `n`, `h`, `nth`, `rout`, `q`,
  `fnth`, `fh`, `solver` and the worst residual `res`.
- `jobs.txt`, `make_launchers.py`: one line `<job>|<arguments>` per job, and the script that writes `job_<job>.cmd` and
  `go_<job>.cmd`. `go_` starts `job_` with `start /BELOWNORMAL /MIN`, and `job_` sets the thread variables, runs the
  command from the checkout root and writes `<job>.log.exit` with the exit code. Paths are relative to the folder.
- `queue.ps1 <job> ...`: starts the jobs in order under the thread rule, restarts a dead one (at most 3 times).
- `sample.ps1`: the memory sampler. `memory-sampler.log`: working set, peak and cpu of each solve, and free memory.
- `cores.log`: choptuik-large-d's cores at each launch of a second process, with our working set and the free memory.

## Run order

The pilot ran alone (51.6 min, k = 256, 9.06 GiB). Then one `queue.ps1` ran `stage1-s2-A-m4.5 stage1-s2-B-m4.5
solve-s4-B solve-s2-B solve-s4-A solve-s2-A`: stage 1 on both slots, then (4, B) and (2, B) when the stage-1 jobs
exited, so no two processes solve the same sector, then (4, A) and (2, A). (4, B) reuses the pilot's m = 21/2 file.

Change at 21:54 (2026-11-20): with (4, B) and (2, B) running, `queue.ps1` was replaced by one that treats them as running
(`+solve-s4-B +solve-s2-B`) and starts the A solves as 17 single-sector jobs `solve-s<sigma R>-A-m<m>` (jobs.txt, longest
expected first), instead of the two jobs (4, A) and (2, A), whose launchers `go_solve-s4-A.cmd` and `go_solve-s2-A.cmd` were
never used. Each job is one sector of the lists above, so the files written are the same. The reason: run in order,
(2, A) would have run alone for about 6 h at the end, with the other slot idle. The old queue's log lines are in
`queue.log`.

## Results

All 22 jobs exited 0 and none died (`*.log.exit`, `queue.log`). 36 sector files in `eig/`. Times and peak memory per job
are in the closing comment of the issue and the note's section "Lower floor (#119)".

| file | what | exit |
|---|---|---|
| `report-old-i118-i111.log` | `--part=report` on #118's and #111's files (floor 0.07), the "before" of the table | 1 (`match` fails in 18 sectors, `own75` at sigma R = 2, m = 9/2) |
| `report-stage1-m4.5.log` | early `--part=report --ms=4.5` after stage 1 | 1 (its sigma R = 4 row is #111's file) |
| `report-wide.log` | `--part=report --out=eig,../I118-win/eig,../I111-win/eig` | 1 (`match` fails at sigma R = 2, m = 19/2 and 21/2) |
| `report-wide-mutate-floorup.log` | the same with `--mutate=floorup` | 1 (`match` and `own75` fail in all 22 sectors) |
| `compare-i111-partial.log` | `--part=compare` after stage 1, against `../I111-win/eig` | 0 (2 files) |
| `compare-i111.log` | `--part=compare --out=eig --ref=../I111-win/eig` | 0 (28 files, worst 2.4e-14) |
| `compare-i118.log` | the same with `--ref=../I118-win/eig` | 0 (8 files, worst 2.1e-14) |
| `compare-i111-mutate-compare.log` | `compare-i111` with `--mutate=compare` | 1 (28 files fail, 1.0e-9) |
| `table.py`, `table.log` | the 18-sector table of the note, from the two reports and `eig/` | 0 |
| `reals.py`, `reals.log` | real eigenvalues returned in the 36 files against the windows | 0 (none returned, A or B) |
| `cost.py`, `cost.log` | solve time per sector at floor 0.04 against floor 0.07 (#111's and #118's logs), ratios by k | 0 |
