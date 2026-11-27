# I202-mac-review: the coordinator's review of #202 (rerun, independent check ind202)

Machine: macOS (the coordinator's Mac), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`), nice 10. Issue:
https://github.com/nmoinvaz/negative-mass/issues/202. Under review: branch `wip/i202-ts13-digits` at da61246, raw
`I202-rpi5` at 1df42f1. Written 2026-11-27 before the first run of `ind202.py` and before the rerun.

## Rerun

`ts13_digits.py`, from a detached worktree `~/Source/negative-mass-r202`, against `ts13_digits_output.txt`.

## ind202: an independent reading of TS13's Table I

The review downloads arXiv:1309.2058's e-print (the TeX source, latest arXiv version) into its own folder
`ts13_src/` as data. It reads the source and runs none of it. `ind202.py` extracts Table I's eight entries for
D = 4 … 11 by its own regex, then compares them with the runner's transcription `PRINTED` in `ts13_digits.py`.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | Each of the eight entries in the review's extraction equals `PRINTED[D]` character for character |
| K2 | Each of growth.csv's D = 4 … 11 rows (main) equals the printed entry's magnitude rounded half-even to 12 decimals, so no csv digit goes beyond TS13's |

## Mutations

| mutation | change | targets |
|---|---|---|
| `digit` | the review's extracted D = 9 entry with its last digit changed | K1, K2 |

## Runs

| file | what |
|---|---|
