# I221-mac-review: the coordinator's review of #221 (rerun, independent check ind221)

Machine: macOS (the coordinator's Mac), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`), nice 10. Issue:
https://github.com/nmoinvaz/negative-mass/issues/221. Under review: branch `wip/i221-growth-lowD` at e13d161, raw
`I221-rpi5` at 64e147f. Written 2026-11-27 before the first run of `ind221.py` and before the rerun.

## Rerun

From a detached worktree `~/Source/negative-mass-r221`, in `notes/wormhole_largeD`: `profiles.py` (growth.csv must come
out byte-identical; profiles.csv is restored afterwards, as in #200's review), `check_growth.py`, `ts13_digits.py`,
`ts13_digits.py --selftest` and `paper_numbers.py`, each against its committed log.

## ind221

The review's own parse of `w2_output.txt` (the method of `I200-mac-review/ind200.py`), applied to all sixteen rows.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | All 16 rows of growth.csv equal the crate's qd values rounded to 12 decimals, as strings, with source `w2_crate qd (#195)`, and the file has exactly three columns |

## Mutations

| mutation | change | targets |
|---|---|---|
| `row4` | K1 reads D = 4's crate value with its 12th decimal +1 | K1 |

## Runs

| file | what |
|---|---|
