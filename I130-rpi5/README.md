# I130-rpi5: logs and timings of the Weitzenböck identity in a frame rotated about z (#130)

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/130

## Code and environment

Code: worktree `~/Source/negative-mass-i130` on branch `wip/i130-rot`, started at main 9a5421e. The script is
`notes/warp/weitzenbock_conf.py`, extended from #99's frame e_i = d_i / A_i on diag(A^2, B^2, C^2)(x, y, z) to the frame
e'_1 = c e_1 + s e_2, e'_2 = -s e_1 + c e_2, e'_3 = e_3, c = cos(alpha), s = sin(alpha), alpha(x, y, z) arbitrary, with K'_ij =
K(e'_i, e'_j) and the spinor eps arbitrary. Expressions are reduced modulo c^2 + s^2 = 1 as #86's conventions.py does. #87's
and #99's checks and controls stay as they are.

Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0). Every run is `nice -n 10` with `OMP_NUM_THREADS=1` and
`OPENBLAS_NUM_THREADS=1`, one process at a time, and any run longer than a few minutes is a systemd user unit
`nm-i130-<step>` that writes its exit code to `done/<step>.rc`. `memwatch.sh` only reports load, free memory and the rss of
this task's python processes once a minute to `memwatch.log`. Memory is never a stop condition. Nothing of choptuik-large-d
is touched.

## Steps

| step | what | log | stop condition |
|---|---|---|---|
| 2 | planted parts first: omega' against the closed form and against #86's `slice_data`, orthonormality, Clifford parallelism, mu and J' with hand values, alpha = 0 against `identity_diag_general`, then the flat and Lichnerowicz identities rotated by arbitrary alpha | `step2_*.log` | none |
| 3 | `--no-controls --only=identity_rot_Kdiag,identity_rot_general,V_reduced_rot` | 792fd1d | 0 | 1 min 2 s | 87.6 MiB | `identity_rot_Kdiag` (616 terms a side) and `identity_rot_general` (alpha, A, B, C, K'_ij and eps arbitrary, 848 terms a side) have difference 0 modulo c^2 + s^2 = 1, 25 s and 21 s of sympy; `V_reduced_rot` passes. The 8 h stop condition never applied |
| 4 | `--mutate=NAME` for each of the 35 controls, one after the other (`step4.sh`, `mutations.txt`, one `mutate_NAME.log` each) | 792fd1d | all 35 exit 1 | 55 min 50 s in all, longest 329 s (`inv-typo`) | not timed per run | 35 FIRED, 0 SILENT. 27 old controls (their targets extended by the rotated checks) and 8 new: `rot-dalpha`, `rot-reverse`, `rot-swap`, `rot-ortho`, `rot-k`, `rot-J-frame`, `rot-div`, `rot-reduce`. `sign` fails 14 checks, `Jsign` 13, `rot-dalpha` 8. The target lists were written before the first run and not changed. Failures outside a control's targets: only #87's checks under `psi-frame`, `inv-typo` and `ricci-sign` |
| 3 | the general rotated identity, alpha, A, B, C, K'_ij and eps arbitrary, as a systemd unit | `step3_*.log` | 8 h wall; then stop it and report the largest case that finished |
| 4 | every mutation, old and new, each must exit 1 and fire on its targets | `mutate_<name>.log`, `step4.time` | none |
| 5 | `python notes/warp/weitzenbock_conf.py > notes/warp/weitzenbock_conf_output.txt`, must exit 0 | `final.log` | none |

The pass criteria and the controls' target lists are in the script (`CONTROLS`) and are written before the controls run.

## Results

Code commits on `wip/i130-rot` of nmoinvaz/negative-mass: the rotated-frame checks and controls at 792fd1d.

| step | command (args to `weitzenbock_conf.py`) | commit | exit | wall | peak rss | result |
|---|---|---|---|---|---|---|
| 2 | `--no-controls --skip=identity_rot_Kdiag,identity_rot_general,V_reduced_rot` | 792fd1d | 0 | 2 min 56 s | 102.6 MiB | 58 checks pass, 0 fail: #87's and #99's 42, and 16 rotated ones (planted omega', orthonormality, Clifford, mu and J' with hand values, 4-metric route, alpha = 0 against `identity_diag_general` term for term, and the identities flat, Lichnerowicz, flat with K', Alcubierre rotated) |

Logs: `step2.log`, `step3.log` (stdout), `step2.err` (timings), `step2.time` (`/usr/bin/time -v`), `step2.cmd`, `memwatch.log` (report only).
