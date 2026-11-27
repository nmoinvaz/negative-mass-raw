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

## Amendments

**A1, after run 1.** Run 1 crashed (KeyError: 20). The review's regex expected the source label `modes_r`, but
`w2_output.txt` prints `modes_r.py`. The regex is fixed; nothing else changes.

## Runs

| file | what |
|---|---|
| `ind200_run1.txt` | run 1: crashed (KeyError 20) on the review's regex (A1) |
| `ind200_run2.txt`, `ind200_run2_mut_*.txt` | run 2: **exit 0, 2 of 2.** K1: the 16 rows (8 crate rows as strings, 8 TS13 rows byte-identical to main). K2: 72.630835, 73.699702, 74.038771 and 74.205123, matching 72.63, 73.70, 74.04 and 74.21. `row` fails exactly K1, `omega1` exactly K2 |
| `rerun_profiles.log`, `rerun_check_growth.log`, `rerun_paper_numbers.log` | check_growth and paper_numbers print exactly the committed logs. profiles.py rewrites growth.csv identically and profiles.csv within 1.9e-9 relative, which is the platform scatter; the committed file is kept |
