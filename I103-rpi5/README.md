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
| 1 | `he_type.py --no-controls` on the unchanged code, for the run time | `s1_base_nocontrols.log` |
