# I131-rpi5: logs of he_surface.py's equality check of he_type_exact's D (#131)

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/131

## Code and environment

Code: worktree `~/Source/negative-mass-i131` on branch `wip/i131-dexact`, started at main 111d812. Files written there:
`notes/warp/he_surface.py`, `notes/warp/he_surface_output.txt` and `notes/warp/he_surface.md` (discrepancy 1 and
recommended task 4) only.

Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0). Every run is `nice -n 10` with `OMP_NUM_THREADS=1`,
one process at a time. A run of more than a few minutes is a systemd user unit `nm-i131-<step>`. `run_step.sh` writes
`<step>.log` (stdout), `<step>.err`, `<step>.time` and `done/<step>.rc` (exit code). Memory is reported only and never a
stop condition. Nothing of choptuik-large-d is touched.

## What is computed

`classify` compares he_type_exact's D with the exact D by equality (`Dsp == Dq`) and records a failure instead of
aborting. `NSIMP` and the printed note about `sp.nsimplify` are removed. A new control `nsimplify-back` sets
`ht.MUT = "nsimplify"` before the points are classified.

## The point #72 found, and the control's target list (written before any control ran)

`support/locate_nsimp_point.py` (step s0) runs `he_surface.py --no-controls` with `classify` wrapped. It applies
`sp.nsimplify` to the script's own exact D at each of the 356 points and records the calling check. No control runs and
`ht.MUT` is untouched. Result (`s0_locate.log`): 1 of 356 points changes, the same count as #72's. It is in `check_axis`,
in the second loop, the 20 axis points with a != 0 (Type IV, D < 0): v = 7/4, F = 1/8, a = -3/2, b = 0, u = 2/3, c = 1,
s = 0, D = -2100108180625/67108864, `nsimplify(D)` = -3024*2**(117/178)*3**(159/178)*5**(28/89)*7**(18/89). The other
three callers (locus_points 60, null_points 250, designated 6 through `check_designated`) have no changed value.

Target list of `nsimplify-back`: `["axis"]`. It is fixed here and does not change.

Prediction, before the control runs: `exact_sign` under `MUT == "nsimplify"` rebinds a local D and returns only the
sign, and `he_type_exact` returns the D that `disc` gave. So `Dsp == Dq` holds at every point under that mutation, the
sign of the changed point is unchanged (D < 0, Type IV), and `ht.MUT = "nsimplify"` alone does not fire in he_surface.py.

## Runs

| step | what | log |
|---|---|---|
| s0 | locate the point #72 found (`support/locate_nsimp_point.py`, exit 0, 13 s) | `s0_locate.log` |
