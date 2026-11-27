# I200-mac-review: the coordinator's review of #200 (rerun, independent check ind200)

Machine: macOS (the coordinator's Mac), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`), nice 10. Issue:
https://github.com/nmoinvaz/negative-mass/issues/200. Under review: branch `wip/i200-growth-csv` at 799b22a, raw
`I200-rpi5` at ae77cef. Written 2026-11-27 before the first run of `ind200.py` and before the rerun.

## Rerun

From a detached worktree `~/Source/negative-mass-r200`, in `notes/wormhole_largeD`: `profiles.py`, `check_growth.py` and
`paper_numbers.py`. The expectation: the same growth.csv byte for byte, and the same check and paper_numbers output
(`logs_check_growth.txt`, `logs_paper_numbers.txt`), apart from timings.

## ind200

The review's own parse of `w2_output.txt` (the "growth.csv against the crate" table, the crate's qd column) and its
own arithmetic in mpmath at 40 digits. It shares no code with `profiles.py` or `check_growth.py`.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | Each of growth.csv's eight D ≥ 20 rows equals the crate's qd value rounded half-even to 12 decimals, as a string, with source `w2_crate qd (#195)`. The eight D = 4 … 11 rows equal main's (613e866) byte for byte |
| K2 | (W²a² − [s − 4 ln 2 + Ω₁/s])·s² from the new rows, with s = 2(D − 3) and Ω₁ = 2π²/3 + 8 ln²2, matches growth_update.md's column to its printed digits at D = 200, 500, 1000 and 2000 (72.63, 73.70, 74.04, 74.21) |

## Mutations

| mutation | change | targets |
|---|---|---|
| `row` | K1 reads D = 500's crate value with its 12th decimal +1 | K1 |
| `omega1` | K2 uses Ω₁ + 1e-6 | K2 |

## Runs

| file | what |
|---|---|
