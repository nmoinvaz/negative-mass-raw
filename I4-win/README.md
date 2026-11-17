# I4-win: logs and partial files of the polar growing-mode scans, convergence variants and kappa_eff at l = 4, 5 and 6

Machine: win (surface-laptop-4, Windows 11, 8 logical CPUs, 32 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/4

## Code and environment

Code: `C:\Users\nathan\Source\negative-mass-i4` on branch `wip/i4-polar-l456`, started at 63682b6, `phase2/nonradial`,
scripts unmodified. The outputs are committed there (`scan_eps-1_w0.7603_l{L}.csv`, `convergence_l{L}_output.txt`,
`kappa_eff_l{L}_output.txt`, `kappa_eff_l{L}_w0.7603.csv`).

Python: `negative-mass-venv314\Scripts\python.exe`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1, sympy 1.14.0, mpmath 1.3.0
(the pinned requirements.txt). Every run has `OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1`, below-normal priority, and
at most 4 processes of mine at a time, launched detached with `start`.

## Task

The phantom star omega = 0.7603 (M = -0.01458), polar modes, real growth rate gamma. For each l the scan covers
gamma in [1e-3, GMAX] on 100 log-spaced points, with GMAX above the point-mass rate k/(2|M|).

| l | k/(2\|M\|) | GMAX |
|---|---|---|
| 4 | 2058 | 3000 |
| 5 | 4801 | 6000 |
| 6 | 9602 | 12000 |

## How the stages ran

The stages overlapped, with the coordinator's agreement (issue comments), because one evaluation of the convergence
variants (rtol 1e-12 at the top gamma) runs for hours on one core.

- l = 4: scan 12:54 to 13:44 (NPROC=4), convergence 13:44 to 18:31 (NPROC=4), kappa_eff after it. The rtol 1e-12
  evaluation at gamma = 3000 took 17168 s, inside the 5 h cap.
- l = 5: scan 15:55 to 18:23 (NPROC=3, beside the l = 4 evaluation), kappa_eff 5 and 6 early on a free core (18:39 to
  about 18:50), convergence from 18:24 (NPROC=3). The rtol 1e-12 evaluation at gamma = 6000 reached the 5 h cap and was
  stopped, see below.
- l = 6: scan started 18:51 with NPROC=1 (1 point, 11252 s), restarted at 23:33 with NPROC=4 from its partial file and
  finished at 03:23 (99 points, 13845 s). Convergence 03:24 to 10:05 (NPROC=4), then the table regeneration and the
  kappa_eff 6 rerun (10:06, identical to the committed file). The rtol 1e-12 evaluation at gamma = 12000 was stopped
  1 h 16 min after the 5 h cap, see below.

## Files

- `mini_bs.log`: `python mini_bs.py`, the known-QNM control (Mini BS I, l = 2). `mini_bs_vs_stored.diff` is
  `diff mini_bs.log mini_bs_output.txt` (14 lines: the four pre-polish shooting rows differ in omega at about 2e-6, and
  the last |D| is 1.35e-15 against 1.45e-16). The sigma, the secant iterates and the target star agree to the printed
  digits; the coordinator took the diff as platform noise.
- `scan_l{L}.log`: `NPROC=N python scan_growing.py -1 0.7603 L 100 0.001 GMAX`, its stdout and stderr. The output
  `scan_eps-1_w0.7603_l{L}.csv` (gamma, D) is committed to the code repository, and the per-point
  `scan_eps-1_w0.7603_l{L}.partial.csv` (index, gamma, D) is kept here.
- `convergence_l{L}_w0.7603.partial.csv`: the per-evaluation records of `GAMS=0.001,0.03,0.3,1,3,10,40,137,300,1000,GMAX
  python convergence.py L` (variant, gamma, D, seconds).
  - l = 4: `convergence_l4.log` is its stdout with stderr merged (`2>&1`), so it carries the RuntimeWarning lines. The
    committed `convergence_l4_output.txt` is the same text with those warning lines (and the source line after each)
    removed. `kappa_eff_l4.log` and `kappa_eff_l4_output.txt` are related in the same way.
  - l = 5, 6: stderr goes to separate files, `convergence_l{L}.stderr` and `kappa_eff_l{L}.stderr`.
- `kappa_eff_l{L}`: `python kappa_eff.py L`. `kappa_eff_l5_output.txt` was produced twice, at 18:39 and again at
  23:28 after the convergence stopped, and `kappa_eff_l6_output.txt` at 18:39 and again at 10:06 after it; the second
  runs are identical to the committed files (`git diff` empty, csv included).
- `stage_l{L}.status`, `stage_kappa.status`: the launchers' own time stamps. In `stage_kappa.status` every line shows
  18:39:35, because `%time%` expands once inside the loop of `run_kappa.cmd`; the real run was 18:39 to about 18:50.
  The l = 5 convergence line `convergence exit -1` at 23:26:51 is my stop of the pool (below). The `regen exit 1`
  line in `stage_l5.status` at 23:27:56 is a failed launch of the table regeneration, because `run_regen.cmd` first
  passed GAMS with its quotes; `convergence_l5_regen.stderr` was overwritten by the relaunch (23:28:22, exit 0).
- `progress.log` and `sample_progress.ps1`: the cpu, memory and partial-file counts sampled every 10 min.
- `run_*.cmd`: the launchers (`run_mini_bs.cmd`, `run_stage.cmd` for l = 4, `run_scan.cmd`, `run_conv.cmd`,
  `run_kappa.cmd`, `run_regen.cmd`; `run_stage2.cmd` was written and not used).
- `cap_row.py`: not part of the repository scripts; it prints a convergence row from a partial file whose rtol 1e-12
  evaluation was stopped at the cap (below).

## The 5 h cap on the rtol 1e-12 evaluations at l = 5 and 6

The coordinator's rule: an rtol 1e-12 evaluation that has not finished 5 h after it started is stopped, its row is
recorded as not completed with its run time, and the other four variants' signs at that gamma stand.

- l = 5, gamma = 6000: the evaluation started with the pool at 18:24:27 plus a start-up of about 1 min, and was still
  running at 23:26. At 23:26:37 I stopped the pool worker that ran it (its wall time since creation was 18129 s, its cpu
  time 17992 s including the start-up). I identified the worker by its pipe write counter (260 bytes, 24 operations,
  against about 3650 bytes for the two others, which had returned 65 results between them) and checked the process
  parent and command line before stopping it. The other 65 evaluations were already in the partial file, so I stopped
  the main process and its workers, and `convergence.py 5` exited with -1.
- `convergence_l5_output.txt` was then written by `run_regen.cmd 5 "0.001,...,1000"` (convergence.py with GAMS
  without 6000, which reads the finished evaluations from the partial file and runs nothing), and the gamma = 6000 row
  was appended with `cap_row.py convergence_l5_w0.7603.partial.csv 6000 18129`, which prints the row in the format of
  convergence.py from base, phi_cut 1e-12, background R = 90, r0 = 3e-3 and q, and marks the rtol 1e-12 variant as not
  completed. The time in parentheses on that row is the sum of the five evaluations that finished.
  A rehearsal on the complete l = 4 partial file with rtol 1e-12 dropped gives the convergence.py row in every field
  that does not depend on the dropped variant.
- l = 6, gamma = 12000: the evaluation started with the pool at 03:24:15 plus a start-up of about 1 min, and the 5 h
  cap was due at about 08:25. Two workers (the rtol 1e-12 and the phi_cut 1e-12 evaluations) had returned nothing, so their
  pipe write counters (260 bytes, 24 operations) were identical, and phi_cut 1e-12 has no cap. I waited for the phi_cut
  1e-12 result, which came at 09:40 after 22534 s, and stopped the worker that still had none (pid 8256, wall time
  since creation 22599 s, cpu 22439 s) at 09:40:55, 1 h 16 min after the cap. After the other 65 evaluations finished I
  stopped the pool (10:05:55, `convergence.py 6` exit -1), ran `run_regen.cmd 6` (exit 0) and appended the row with
  `cap_row.py convergence_l6_w0.7603.partial.csv 12000 22599`.
- `cap_row.py` first said "stopped at the 5 h cap" in the row; it now says "stopped after its worker had run N s of wall
  time, past the 5 h cap (18000 s)", and both capped rows (l = 5 and l = 6) were regenerated with that wording after the
  l = 6 stop (the l = 5 row was reworded in the same commit as the l = 6 table).
