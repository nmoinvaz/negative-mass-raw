# I103-rpi5: logs of the exact sign test of D in he_type_exact (#103)

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/103

## Code and environment

Code: worktree `~/Source/negative-mass-i103` on branch `wip/i103-dsign`, started at main 29e395d. Files written there:
`notes/warp/he_type.py` and `notes/warp/he_type_output.txt` only. `he_surface.py`, its output and `he_type.md` are not
edited.

Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0). Every run is `nice -n 10` with `OMP_NUM_THREADS=1`,
one process at a time, and any run longer than a few minutes is a systemd user unit `nm-i103-<step>` that writes its exit
code to `done/<step>.rc`. Memory is reported only and never a stop condition. Nothing of choptuik-large-d is touched.

## What is computed

`he_type_exact` replaces `sp.nsimplify` of the discriminant D by an exact sign test that keeps D as given, and returns D
unchanged. `planted_cases` gains tensors with D = 10^-60 (Type I) and D = -10^-60 (Type IV). A new control
`--mutate=nsimplify` restores the old call and must make `planted` fail.

## Runs

Written as they happen, one log per step (`<step>.log` stdout, `<step>.err` stderr, `done/<step>.rc` exit code).

| step | what | log |
|---|---|---|
| 1 | `he_type.py --no-controls` on the unchanged code (1 m 49 s wall, 102 s user, peak rss 1.5 GB, exit 0), diff against the committed output in `s1_diff_vs_committed.txt` | `s1_base_nocontrols.log` |
| 2 | `exact_sign` against sympy's `evalf(400)` on random algebraic expressions, 400 each at seeds 103 and 104 (`fuzz_sign.py`; 320 and 322 outside the rational branch; exit 0, 0 mismatches). With the old rounding restored the same run fails (147 mismatches, exit 1) | `s3_fuzz_sign.log`, `s3_fuzz_sign2.log`, `s3_fuzz_sign_mutate_nsimplify.log` |
| 3 | new code, `he_type.py --no-controls` (exit 0, 8 of 8, 1 m 52 s), `--mutate=nsimplify` (exit 1, `planted` fails, as targeted), `--mutate=disc-sign` (exit 1, `planted` fails) | `s3_nocontrols.log`, `s3_mutate_nsimplify.log`, `s3_mutate_disc-sign.log` |

Scripts: `run_step.sh` and `run_any.sh` (run one step and write `<step>.time` from `/usr/bin/time -v`, `<step>.err`, `done/<step>.rc`),
`step3.sh`, `step4.sh`. Support: `support/search_tridiagonal_R0.py`, `support/search_symmetric_R0.py` and
`support/search_elliptic_points.py` (the search for rational tensors with D = +-j^6), `support/probe_old_code.py`.
