# I157-mac: the coordinator's review of #157's ideal step for three mixed-sign scalars

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, at nice 10 with at most 2 processes. No
Singular on this machine. Issue: https://github.com/nmoinvaz/negative-mass/issues/157. Reviewed branch
`wip/i157-three-scalars-ideal` at 41ed7f8 and raw `I157-rpi5` at 0053c30.

## Rerun of the runner's script

`python3 notes/warp/three_scalars_ideal.py --raw=<this repository>/I157-rpi5`, the default mode (checks, planted cases,
stored certificates, the 9 controls; no Singular), from a detached worktree at 41ed7f8. Output: `rerun_default.txt`.
