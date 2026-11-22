# I96-win: tanh spectrum of T1 for the thin walls sigma R = 8 and 16 (logs, eigenvalue arrays, box runs)

Machine: win (surface-laptop-4, Windows 11, 8 logical CPUs, 4 physical cores, 32 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/96

## Code and environment

Code: worktree `negative-mass-i96` (beside this clone) on branch `wip/i96-thin` at c5fd40d, `notes/warp/tanh_spectrum.py`
(#75's spectral code, with its options `--p`, `--npan` and `--convtol`) and `notes/warp/frank_loss.py` (#63's FFT box),
run from the repository root, unmodified.

Python: `negative-mass-venv314\Scripts\python.exe`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1 (the pinned
requirements.txt). Every run has `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1` and `MKL_NUM_THREADS=1`, `--procs=1` for
`tanh_spectrum.py`, below-normal priority, and is launched detached with `start`. At most two processes (a
`tanh_spectrum.py` run is a main process and one worker). A second one starts only while choptuik-large-d's processes
together use under 4 cores (CPU-seconds delta over 10 s, `cores.log`).

Launch rule. The task's rule was: beside a sigma R = 16 solve only if the pilot's peak plus the second's expected peak is
under 24 GiB. The pilot (sigma R = 16, p = 320, one sector) peaked at 24.43 GiB, so nothing could run beside such a
solve, and the coordinator ordered the sigma R = 8 sectors to run alone first. After the pilot post the coordinator
replaced the rule for the rest of #96 (2026-11-21, about 14:50): two processes may run together when the sum of their expected
peaks is under 24 GiB, where a process's expected peak is its own measured one if it has run before at that size and
otherwise a scaled estimate (named as one). A sigma R = 16 sector solve (24.4 GiB) still runs alone. No run whose expected
peak exceeds 28 GiB is launched (sectors at P = 360 would, by p^2 scaling, peak near 31 GiB). Why: the sigma R = 16 `conv`
(about 10 GiB, estimated) fits beside the sigma R = 8 sectors (about 9.5 GiB, estimated), which saves about 6.5 h. Memory is
reported only: nothing stops or kills a process because of it (`memory-sampler.log`, once a minute, worker processes included).

Sizes are written in the job lines of `jobs.txt`. `--raw` writes one `tanh_sigma{S}_m{M}.npz` per sector (`vc`, `muA`,
`muB`, every eigenvalue of S^-1 M in A and B) to `eig/`.

## Plan

1. `conv-s8-*`: `--part=conv --sigmas=8 --p=8:P --npan=N --convtol=1e-8 --procs=1`, from P = N = 160. While `conv`
   fails, raise P by 40 or double N, whichever the failing variants point to. At most 4 attempts.
2. `pilot-s16`: `--part=vc,planted,tanh --sigmas=16 --ms=0.5 --p=16:320 --npan=320 --procs=1 --raw=eig`, alone, with its
   time, rho(T1) v_c of A and B, their difference, the window and the peak. Stop condition: more than 4 h, then stop it
   and report before the next step.
3. `sectors-s8` (the coordinator moved this ahead of the sigma R = 16 sizes, after the pilot, because nothing can run
   beside a sigma R = 16 solve; once the rule above changed, `conv-s16-p320-n320` started beside it at 14:53): `--part=vc,planted,shift,tanh --sigmas=8 --p=8:200 --npan=160 --procs=1 --raw=eig`,
   all 11 sectors m = 1/2 to 21/2, alone. A process that dies restarts with the same command (the dead log kept as
   `<job>.died<N>.log`, `queue.ps1`).
4. `conv-s16-*`: as step 1 at sigma R = 16, from the pilot's P and N. At most 4 attempts. Attempt 1 (P = N = 320) failed
   at 2.4e-8. The task's rule (P + 40) would give P = 360 for attempt 2; the coordinator changed the step to +20 here
   (attempt 2: P = 340, N = 320, tolerance still 1e-8), because sigma R = 16 sectors at P = 360 would peak near 31 GiB
   (scaled) and cannot run on this laptop, and ordered that no run be made at P = 360.
5. `sectors-s16`: `--part=vc,planted,shift,tanh --sigmas=16 --p=16:P --npan=N --procs=1 --raw=eig`, all 11 sectors.
6. `box-*`: `frank_loss.py --part=krylov --sigmas=S --Ns=N --L=L --vs=0.5` at two or three L at one fixed spacing per
   sigma R, as tanh_spectrum.md section 6.

## Files

- `jobs.txt` (`<job>|<script>|<arguments>`), `make_launchers.py` (writes `job_<job>.cmd` and `go_<job>.cmd`),
  `queue.ps1` (starts jobs under the thread rule and restarts a dead one), `after_pilot.ps1` (started `sectors-s8` when
  the pilot exited), `sample.ps1` (the memory sampler), `cores.ps1` (one reading of choptuik-large-d's cores),
  `runs.py` (per-job wall, sector times, peak), `convmax.py` (largest move of a conv log).
- `<job>.log` is a job's stdout, `<job>.log.exit` its exit code, `cores.log` the readings before each second start,
  `queue.log` the queue's events, `memory-sampler.log` the sampler.
- `eig/`: the sector files.

## Results

Filled in at each post.

### Sizes at sigma R = 8 (`convmax.py` reads the logs)

| attempt | P | N | largest move of the leading \|mu\| v_c (relative) | wall | peak working set | exit |
|---|---|---|---|---|---|---|
| `conv-s8-p160-n160` | 160 | 160 | 5.2e-8 (Lmap = 4, m = 3/2); next 2.5e-8 (p = 140) | 2073 s | 2.54 GiB (2599 MiB) | 1, `conv` fails |
| `conv-s8-p200-n160` | 200 | 160 | 1.1e-9 (Lmap = 4, m = 1/2) | 4160 s | 3.90 GiB (3991 MiB) | 0 |

The 320-panel variant moves the leading eigenvalue by 6e-14 at P = 160, so the panels are not the limit; the failing
variants (Lmap = 4, p = 140) point to the radial size. Peaks are the sampler's, once a minute.

### Pilot, sigma R = 16, m = 1/2 (`pilot-s16`, exit 0)

A: dK = 28, p = 320, Lmap = 2, 320 panels. B: dK = 38, p = 330, Lmap = 3, 480 panels.

| quantity | value |
|---|---|
| time | sector 8605 s, wall 8615 s (2.39 h); A (with eigenvectors) about 70 min, B about 70 min |
| peak working set | 24.43 GiB (25014 MiB, sampler once a minute), reached in A; free memory fell to 1.7 GiB |
| rho(T1) v_c | 0.22508330 (A), 0.22508330 (B); the log's difference 4.4e-10 (absolute, 2e-9 relative) |
| leading eigenvalues | +-0.002778 +- 0.225066i (sqrt(3) rho v_c = 0.3899) |
| window (stable to 1e-5 above) | 0.1128; 22 eigenvalues of A and 24 of B in it, no real one |
| real, \|mu\| v_c > 1e-8 | 76 (A) / 70 (B), largest 6.6e-4, none reproduced by B; identity 0 on 124 eigenfunctions (76 real) |
| planted | rho = 1 to 7.3e-15; `real_identity` 2.3e-16 |

`sectors-s8` started at 14:41 (the pilot's exit), alone, as the coordinator ordered.

### Sizes at sigma R = 16

| attempt | P | N | largest move of the leading \|mu\| v_c (relative) | wall | peak working set | exit |
|---|---|---|---|---|---|---|
| `conv-s16-p320-n320` | 320 | 320 | 2.4e-8 (Lmap = 4, m = 3/2); next 1.9e-8 (Lmap = 4, m = 1/2); then p = 300 at 2.4e-9 | 12635 s | 9.78 GiB (10018 MiB), estimate was 10 GiB | 1, `conv` fails |

Only the Lmap = 4 variant fails (as at sigma R = 8, P = 160); the 160 and 640 panel variants move the base by 6.7e-10 and
3.7e-10 at most, so the failing variants point to the radial size. Attempt 2 started 18:27 (P = 340, N = 320), beside
the sigma R = 8 sectors (expected peaks about 11 and 10 GiB, under 24 GiB).

### Box probe

`box-s8-L1-N64`: `frank_loss.py --part=krylov --sigmas=8 --Ns=64 --L=1 --vs=0.5` (dx = 0.03125, 4 points across the
wall 1/8 wide), exit 1 (`gmres` residual 1.1e-2 and `identity` 2.4e-1 fail, as the script's own checks report), 43 s,
rho(T1) v_c = 0.21589. The sampler saw no process over 100 MB, so no peak was recorded; the probe is too small to tell.

### Box comparison, sigma R = 8, dx = 1/32 (step 6)

Four sizes at the fixed spacing dx = 2L/N = 1/32 (4 points across the wall 1/8 wide), `frank_loss.py --part=krylov
--sigmas=8 --vs=0.5`, one thread each, at c5fd40d:

| L | N | where | log |
|---|---|---|---|
| 1 | 64 | win and Mac | `box-s8-L1-N64.log` here, `../I96-mac/box-s8-L1-N64.log` |
| 2 | 128 | Mac | `../I96-mac/box-s8-L2-N128.log` |
| 2.5 | 160 | Mac | `../I96-mac/box-s8-L2.5-N160.log` |
| 3 | 192 | win, started by the coordinator (exit code not captured) | `box-s8-L3-N192.log`, `.err` |
| 3.5 | 224 | win, this runner, detached with `go_box-s8-L3.5-N224.cmd`, alone | `box-s8-L3.5-N224.log`, `.log.exit` |

`box-s8-L3.5-N224` was added to `jobs.txt` by a new runner session after the first one ended at its account's limit. The
peak is the sampler's `peak=` for `frank_loss.py --part=krylov ... --Ns=224` in `memory-sampler.log`, here every 10 s
(the script itself prints `peak nan GB` on Windows).
