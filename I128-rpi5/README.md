# I128-rpi5: logs of #128's dense-chain replay of the 61 boxes recounted in #126, and of the mutations of its scripts

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/128

## Code and environment

Code: worktree `~/Source/negative-mass-i128` on branch `wip/i128-replay-all`, run from `phase2/nonradial`:
`diagnose_plant.py` (with `--y0`), the new `replay_i126.py` and `collect_i126.py` (with `--mutate=nolog`).

Python: `~/Source/negative-mass-venv314/bin/python`. One process at a time, `nice -n 10`, `OMP_NUM_THREADS=1`,
`OPENBLAS_NUM_THREADS=1`. No evaluation of D or Z: the replays read the pickle caches of `../I126-rpi5/cache` in place
and write nothing there.

## What is replayed

Each of the 61 boxes of `../I126-rpi5/jobs.txt` (31 of D, 30 of Z; not the five controls) is replayed on its cache with
`diagnose_plant.py --guard=all --expect=none`, the box's x0, x1, y1, its `--y0` if any and its planted zero.

## Files

(filled in as the run proceeds)
