# I99-rpi5: logs and timings of the Weitzenböck identity on a diagonal slice (#99)

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/99

## Code and environment

Code: worktree `~/Source/negative-mass-i99` on branch `wip/i99-diag`, started at main 4a52469. The script is
`notes/warp/weitzenbock_conf.py`, extended from #87's from a conformally flat slice psi^4 delta to a diagonal slice
diag(A^2, B^2, C^2)(x, y, z) with e_i = d_i / A_i, an arbitrary symmetric K_ij and an arbitrary spinor. #87's checks and
controls stay as they are.

Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0). Every run is `nice -n 10` with `OMP_NUM_THREADS=1`
and `OPENBLAS_NUM_THREADS=1`, one process at a time, and any run longer than a few minutes is a systemd user unit
`nm-i99-<step>` that writes its exit code to `done/<step>.rc`. `memwatch.sh` only reports load, free memory and the rss
of this task's python processes once a minute to `memwatch.log`. Memory is never a stop condition. Nothing of
choptuik-large-d is touched.

## Steps

| step | what | log | stop condition |
|---|---|---|---|
| 2 | planted flat case (A = B = C = 1) and Lichnerowicz case (K = 0) on the general diagonal slice, through the code path of the general case | `step2_*.log` | none |
| 3 | the general identity, A, B, C, K_ij and eps arbitrary, as a systemd unit | `step3_*.log` | 12 h wall; then report the largest case that finished |
| 4 | every mutation, old and new (27), each must exit 1 and fire on its targets | `mutate_<name>.log`, `step4.time` | none |
| 5 | `python notes/warp/weitzenbock_conf.py > notes/warp/weitzenbock_conf_output.txt`, must exit 0 | `final.log` | none |

The pass criteria and the controls' target lists are in the script (`CONTROLS`) and were written before the controls ran.

## Results in one paragraph

Code commits on `wip/i99-diag` of nmoinvaz/negative-mass: the diagonal checks at c1567ef, their controls at 0b9d38f, two
stronger planted cases at ffd8f93, the run that produced the output at 8016151, the output at f91280a, and the docstring's
memory unit at cef6d1a. Step 2 (planted flat and K = 0 cases, 40 checks): exit 0, 23.8 s wall, 73.4 MiB peak. Step 3
(`identity_diag_Kdiag`, `identity_diag_general`): exit 0, 19.5 s, 72.1 MiB, both identities expand to 0 (360 and 480 terms a
side), so the 12 h stop condition never applied. Step 4: the first run of the 27 mutations (0b9d38f, `step4_first_0b9d38f/`)
had 25 FIRED and 2 SILENT (`ricci-sign` and `J-christoffel`, whose target `planted_trace_diag` and `planted_K0_diag` used a
metric with no Gamma Gamma terms in R and d_b g_bb = 0). Both checks then also ran on a(x)^2 dx^2 + w(x)^2 (dy^2 + dz^2). The
rerun on 64c77e6 has 27 FIRED, every run exit 1, 640 s in all. Step 5 (`python notes/warp/weitzenbock_conf.py`, the full
run, 8016151): exit 0, 42 checks pass, 27 controls fire, 11 min 8 s, 86.1 MiB peak. Memory: `memwatch.log` has 50 samples, the
lowest available memory is 5247 MiB, the highest 15-minute load 3.42, and no process was limited by memory.

## Files

| file | what |
|---|---|
| `step2_planted.log`, `.time.v` | step 2: `--no-controls --skip=identity_diag_Kdiag,identity_diag_general` at c1567ef, with wall time and peak rss |
| `run_step3.sh`, `step3_general.log`, `step3.time`, `step3.time.v` | step 3: `--only=identity_diag_Kdiag,identity_diag_general` at c1567ef |
| `run_step4.sh`, `mutate_<name>.log`, `step4.time` | step 4 (rerun, 64c77e6): one log per mutation, one line per mutation in `step4.time` (exit code, seconds, FIRED or SILENT) |
| `step4_first_0b9d38f/` | the first run of step 4, with the two SILENT controls, kept as it was |
| `run_step5.sh`, `run_step45.sh`, `final.log`, `final.err`, `final.time`, `final.time.v` | step 5 at 8016151: the full run, stdout (= `notes/warp/weitzenbock_conf_output.txt`), stderr (per-identity seconds), wall time and peak rss |
| `final_first_64c77e6/` | the same run at 64c77e6, which differs from the final one in two check texts and the docstring |
| `memwatch.sh`, `memwatch.log`, `memwatch.err` | report-only sampler of load, available memory and rss, once a minute; stopped at the end |
| `done/` | exit codes (`*.rc`) |

## Mistakes and discrepancies

- Two controls were SILENT in the first run of step 4, see above. The plants were strengthened, no criterion was loosened.
- `ricci-sign` and `inv-typo` first listed no diagonal identity as a target, which the plan had; they were added for the
  rerun and fired.
- The issue's estimate was 2 to 10 h; the general identity takes 4 s.
- The commit `8016151` (`git commit -a`) also stored the output of the first full run, which `f91280a` replaces by the
  output of the final run (two check texts differ). `cef6d1a` changes only the docstring's memory unit, after the final run.
- The progress posts on #99 gave 75 MB and 74 MB for steps 2 and 3, which were KiB read as MB. The values are 73.4 and
  72.1 MiB.
