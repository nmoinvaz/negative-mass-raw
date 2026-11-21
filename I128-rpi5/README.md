# I128-rpi5: logs of #128's dense-chain replay of the 61 boxes recounted in #126, and of the mutations of its scripts

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/128

## Code and environment

Code: worktree `~/Source/negative-mass-i128`, branch `wip/i128-replay-all`, `phase2/nonradial/` at 716ce01 (fd16713 gave
`diagnose_plant.py` its `--y0`): `diagnose_plant.py`, the new `replay_i126.py` and `collect_i126.py` with `--mutate=nolog`.

Python: `~/Source/negative-mass-venv314/bin/python`. One process at a time, `nice -n 10`, `OMP_NUM_THREADS=1`,
`OPENBLAS_NUM_THREADS=1`. No evaluation of D or Z: every run reads the pickle caches of `../I126-rpi5/cache` in place and
writes nothing there. A full replay takes about 11 s.

## What is replayed

Each of the 61 boxes of `../I126-rpi5/jobs.txt` (31 of D, 30 of Z; not the five controls) is replayed on its cache with
`diagnose_plant.py --guard=all --expect=none`, the box's x0, x1, y1, its `--y0` if any (20 upper boxes: 11 of D, 9 of Z)
and its planted zero. `replay_i126.py` runs it and prints one row per box (`phase2/nonradial/i126_replay_output.txt`).

## Commands (from `phase2/nonradial`, raw repository cloned beside the checkout, `RAW=../../../negative-mass-raw`)

```
python replay_i126.py $RAW/I126-rpi5 > i126_replay_output.txt            exit 0
python replay_i126.py $RAW/I126-rpi5 --mutate=NAME                        exit 1 for sparse, noy0, misplant, nocache, nojobs
python collect_i126.py $RAW/I126-rpi5 --mutate=nolog                      exit 1
python synthetic_y0.py $PWD/diagnose_plant.py [--mutate=wrongcount]       exit 0, and 1 with the mutation
python cross_replay_i126.py $RAW/I126-rpi5 i126_replay_output.txt [--mutate=thin]   exit 0, and 1 with the mutation
```

## Files

- `exit_codes.txt`: the exit code of each run above. The last line of each `.log` below is `exit N`.
- `replay_mutate_<name>.log`: the five mutations of `replay_i126.py`. `sparse`: `w_h1_l2` passes the replay and fails its
  chain check (48 chain points, 126 cached on the contour); `noy0`: the 20 upper boxes stop on a point their cache lacks,
  the 41 symmetric boxes pass; `misplant`: `w_h1_l2` finds 1 planted zero, 0 expected; `nocache`: `w_h1_l2`'s cache is
  missing; `nojobs`: jobs.txt differs from the job list.
- `collect_mutate_nolog.log`: `collect_i126.py --mutate=nolog` ("not run" for `w_s1_l2`, exit 1).
- `regenerate_unchanged.log`: `i115_replay_output.txt` regenerates byte for byte with the command of RESULTS.md §5.4 and
  `i126_guard_output.txt` byte for byte from the unmutated collector, with the edited scripts.
- `synthetic_y0.py`, `synthetic_y0.log`, `synthetic_y0_mutate_wrongcount.log`: the planted-truth control of `--y0` on
  caches of known functions, run before the real caches. Its pass criteria are in its docstring; one (A1's F times the
  factor) was changed before any real cache was replayed, and the docstring says how. The pickles it writes are not kept.
- `cross_replay_i126.py`, `cross_replay_i126.log`, `cross_replay_i126_mutate_thin.log`: a recomputation of the table's chain
  points and largest increments by code that shares with `replay_i126.py` and `diagnose_plant.py` only the cache files,
  `jobs.txt` and the contour's geometry (it orders by arclength). All 61 boxes agree, to 0.0006 rad.

## Not as the issue assumed

- `diagnose_plant.py --mutate=sparse` with `--expect=none` exits 0 on a normal box: a chain cut to the accepted steps' end
  points agrees with the steps whatever they are. #126's sparse log failed only against `--expect=MEASURED,CHAIN`. So
  `replay_i126.py` also requires each chain to hold every cached point on the contour (counted from the pickle by
  comparing coordinates), and that is the check `--mutate=sparse` fires.
- A `--y0` box replayed without `--y0` fails because the symmetric contour starts at (x1, 0), which the cache lacks, not
  because the fourth edge is missing.
- The largest increment is 0.3137 rad (`z_n1_l2`, Z times the factor; 0.313 rad for D, `w_s2_l2`). The coordinator's review of
  #126 quotes 0.313 rad.
