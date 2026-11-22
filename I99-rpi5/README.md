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
| 4 | every mutation, old and new, each must exit 1 and fire on its targets | `mutate_<name>.log` | none |
| 5 | `python notes/warp/weitzenbock_conf.py > notes/warp/weitzenbock_conf_output.txt`, must exit 0 | `final.log` | none |

The pass criteria and the controls' target lists are in the script (`CONTROLS`) and were written before the controls ran.

## Files

Filled in as the runs finish.
