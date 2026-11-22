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
| s2 | `he_surface.py --no-controls` on the new code (exit 0, 14 of 14 checks, 11 s) and `--mutate=nsimplify-back` alone (exit 0, 14 of 14 checks pass: the control does not fire, target `["axis"]`) | `s2_nocontrols.log`, `s2_control_nsimplify-back.log` |
| s3 | probes, not controls of the repository. `support/probe_mut_returns_D.py`: at the #72 point, `he_type_exact` returns the exact D under both `ht.MUT = None` and `"nsimplify"` (exit 0). `support/probe_old_return.py`: `he_type_exact` wrapped to return `sp.nsimplify(D)`, the return value before #103, makes exactly `axis` fail, at that one point (exit 1) | `s3_probe_mut_returns_D.log`, `s3_probe_old_return.log` |

## Why `nsimplify-back` as specified does not fire

`he_type.exact_sign` under `MUT == "nsimplify"` rebinds a local D to `sp.nsimplify(D)` and returns only the sign.
`he_type_exact` returns the D that `disc` gave. So `ht.MUT = "nsimplify"` changes the type only when the rounded D has
another sign or is 0, and at the 356 points of he_surface.py it never does (the old assert held at all 356). The
equality `Dsp == Dq` cannot fail under it. Prediction above, confirmed by s2 and s3.

Not changed since: the target list `["axis"]`, and the criterion (exit 1 and `axis` fails). A mutation that restores
the old return value, `sp.nsimplify(D)` itself, does make `axis` fail (s3), and needs a decision of the coordinator
(a wrapper of `ht.he_type_exact` in he_surface.py, or a change to `he_type.py`'s `MUT`).

## Decision of the coordinator, and the final runs

The coordinator chose a wrapper: `nsimplify-back` replaces `ht.he_type_exact` by a function that returns the type it
gave and `sp.nsimplify(D)`, the return value before #103. The first version (`ht.MUT = "nsimplify"`, steps s2 and s3)
was silent for the reason above. The target list `["axis"]` and the criterion did not change. `he_surface.md` line 187
counts 18 controls.

| step | what | log |
|---|---|---|
| s4 | new code, `--no-controls` (exit 0, 14 of 14, 11 s) and `--mutate=nsimplify-back` alone (exit 1, only `axis` fails, at the point v = 7/4, F = 1/8, a = -3/2, u = 2/3: exact D = -2100108180625/67108864, returned a radical) | `s4_nocontrols.log`, `s4_control_nsimplify-back.log` |
| s5 | `he_surface.py > notes/warp/he_surface_output.txt` as systemd unit `nm-i131-s5-full` (exit 0, 14 of 14 checks, 18 of 18 controls fired, 3 m 47 s wall, peak rss 121 MB); the stored output is the repository's, the diff against the committed one is `s5_diff_vs_committed.txt` (2 lines: the note line removed, the `nsimplify-back` line added) | `s5_stored_he_surface_output.txt` (a copy of the stdout, which went to the repository file), `s5_full.time`, `s5_diff_vs_committed.txt`, `committed_he_surface_output.txt` |
