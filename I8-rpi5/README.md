# I8-rpi5: logs, timings and the exact check of the polar (tt) and angular-trace equations (#8), and the matter_sv.py runs

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/8

## Code and environment

Code: worktree `~/Source/negative-mass-i8` on branch `wip/i8-polar-exact`, started at main 8eacc4f, `phase2/nonradial`.
The existing scripts (`derive_nonradial.py`, `lincommon.py`, `reduce_polar.py`, `verify_polar.py`,
`polar_matrix_generated.py`, `matter_sv.py`) are run unmodified. The new script is `verify_polar_exact.py`.

Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0, numpy 2.5.4, scipy 1.18.1). Every run is
`nice -n 10` with `OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1`, one process at a time, as a systemd user unit
`nm-i8-<step>` that writes its exit code to `done/<step>.rc`. `memwatch.sh` only reports load, free memory and the rss of
this task's python processes once a minute to `memwatch.log`; memory is never a stop condition. Nothing of
choptuik-large-d is touched.

## Steps

| step | what | log | stop condition |
|---|---|---|---|
| 2 | `python derive_nonradial.py` (writes the git-ignored `polar_eqs.pkl`), wall time and peak rss from `/usr/bin/time -v` | `derive_nonradial.log` | 3 h wall |
| 3 | `python verify_polar_exact.py`: (tt) and the angular trace exactly on solutions of y' = J y; planted (tθ), (tr), (rθ), (rr), KG_R, KG_I; `--mutate=coef`, `--mutate=bg` | `verify_polar_exact*.log` | 8 h wall for the full symbolic simplification; then exact evaluation at 20 rational points |
| 4 | `python matter_sv.py eps w l` for (-1, 0.7603, 2), (-1, 0.7603, 3), (+1, 0.75, 2), (+1, 0.75, 3) | `matter_sv_*.log` | none |

The files of the folder are listed with their roles in the table at the end, which is filled as the steps finish.
