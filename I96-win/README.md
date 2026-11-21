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
together use under 4 cores (CPU-seconds delta over 10 s, `cores.log`) and, beside a sigma R = 16 solve, only if the
pilot's peak working set plus the second's expected peak is under 24 GiB. Memory is reported only: nothing stops or
kills a process because of it (`memory-sampler.log`, once a minute, worker processes included).

Sizes are written in the job lines of `jobs.txt`. `--raw` writes one `tanh_sigma{S}_m{M}.npz` per sector (`vc`, `muA`,
`muB`, every eigenvalue of S^-1 M in A and B) to `eig/`.

## Plan

1. `conv-s8-*`: `--part=conv --sigmas=8 --p=8:P --npan=N --convtol=1e-8 --procs=1`, from P = N = 160. While `conv`
   fails, raise P by 40 or double N, whichever the failing variants point to. At most 4 attempts.
2. `pilot-s16`: `--part=vc,planted,tanh --sigmas=16 --ms=0.5 --p=16:320 --npan=320 --procs=1 --raw=eig`, alone, with its
   time, rho(T1) v_c of A and B, their difference, the window and the peak. Stop condition: more than 4 h, then stop it
   and report before the next step.
3. `conv-s16-*`: as step 1 at sigma R = 16, from the pilot's P and N. At most 4 attempts.
4. `sectors-s8` and `sectors-s16`: `--part=vc,planted,shift,tanh --sigmas=S --p=S:P --npan=N --procs=1 --raw=eig`, all 11
   sectors m = 1/2 to 21/2 each, one process per line. A process that dies restarts with the same command (the dead log
   kept as `<job>.died<N>.log`).
5. `box-*`: `frank_loss.py --part=krylov --sigmas=S --Ns=N --L=L --vs=0.5` at two or three L at one fixed spacing per
   sigma R, as tanh_spectrum.md section 6.

## Files

- `jobs.txt` (`<job>|<script>|<arguments>`), `make_launchers.py` (writes `job_<job>.cmd` and `go_<job>.cmd`),
  `queue.ps1` (starts jobs under the thread rule and restarts a dead one), `sample.ps1` (the memory sampler).
- `<job>.log` is a job's stdout, `<job>.log.exit` its exit code, `cores.log` the readings before each second start,
  `queue.log` the queue's events, `memory-sampler.log` the sampler.
- `eig/`: the sector files.

## Results

None yet. This section is filled in at each post.
