# I139-rpi5: #2's certified brackets of c·r_* and c·r_neg for every l = 2..3000, and their comparison with #104's

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10, one thread.
Issue: https://github.com/nmoinvaz/negative-mass/issues/139
Worktree: `~/Source/negative-mass-i139`, branch `wip/i139-bracket-csv` (base main 850785b).
Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0, mpmath 1.3.0). The comparison uses only `fractions.Fraction`, no floats.

Written 2026-11-23, before any run of the new code (the csv run, the comparison, the planted cases and the controls).
Nothing below is changed after a run; a result that misses its prediction is reported with the prediction left as written.

## What is compared

- Ours: `threshold_isolation.py --csv=brackets_i2.csv` writes, for every l = 2..3000, the certified brackets of #2 (`rows[l]`,
  keys `lo_n, hi_n` for c·r_* and `lo_s, hi_s` for c·r_neg, exact `Fraction`s) as `p/q`. Columns `l,c,rstar_lo,rstar_hi,rneg_lo,rneg_hi`.
- Theirs: #104's `I104-rpi5/sweep_brackets.csv` (same columns, 20-digit decimal ends; every bracket has width 2.000001e-14).
- Both are brackets of the same two roots, certified by exact interval arithmetic (#2, `rescaled.py`, 90-term series plus a tail
  enclosure, `Fraction` ends) and by mpmath `iv` (#104, written from RESULTS.md alone). An end is a rigorous enclosure bound, not a
  fit or an estimator range. Each bracket is a closed interval holding the root, so two brackets of one root must intersect,
  and touching counts as intersecting.
- What the two codes share: the formulas typed from RESULTS.md (Lemma A's coefficients, N and S), and nothing else.
  `compare_brackets.py` shares no code with either: it reads two csv files.

## Acceptance (written first)

| id | criterion | how it is checked | can fail by |
|---|---|---|---|
| A1 | the csv has 2999 rows, l = 2..3000 once each | `compare_brackets.py` C1 and `wc -l` (3000 lines with the header) | `--mutate=drop`, planted P4 |
| A2 | `threshold_isolation.py` stdout is unchanged apart from timings, with and without `--csv` | `diff` of the `--csv` run against `phase2/dg_proof/threshold_isolation_output.txt` (expected differing lines: the six `... l = N done, Ns` lines and the last line `N s`, nothing else); and old script vs new script without `--csv` at `--lmax 60` (byte-identical apart from the same timing lines) | a diff line that is not a timing |
| A3 | every row's c·r_* brackets overlap and every row's c·r_neg brackets overlap | C4, C5 | `--mutate=shift`, `--mutate=swap`, planted P3 |
| A4 | a row shifted by 1e-12 makes the comparison fail | `--mutate=shift` | the control exits 0 |

`compare_brackets.py --ours=PATH --theirs=PATH [--lmax=3000] [--mutate=NAME]`, from `phase2/dg_proof`. Checks, each printing `PASS` or `FAIL`
(exit 1 if any FAIL, a parse error is a FAIL):

| check | statement |
|---|---|
| C1 | each file has the header `l,c,rstar_lo,rstar_hi,rneg_lo,rneg_hi` and its l values are exactly 2..lmax, each once (reports missing, extra, duplicate l) |
| C2 | c = (l+2)(l-1) in every row, in each file |
| C3 | lo < hi (strict) in both brackets of every row, in each file |
| C4 | for every l in both files, the c·r_* brackets intersect: min(hi) - max(lo) >= 0 |
| C5 | the same for the c·r_neg brackets |

Then it prints the largest bracket width of each file, the smallest overlap (signed min(hi) - max(lo), negative means a gap) and the
largest distance between the midpoints, each with its column and l (first one in l order, c·r_* before c·r_neg), as `d.dddddde±xx`
computed in exact arithmetic. `--lmax` exists so the planted files can be small; it is 3000 in every real run.

## Planted cases (hand-written files in `planted/`, run through the same code, before the real data)

`ours_p*.csv` hold fractions, `theirs_*.csv` decimals. Predicted verdicts, written before the first run:

| case | ours | theirs | --lmax | exit | FAIL lines (exactly these) | widest ours | widest theirs | smallest overlap | largest midpoint gap |
|---|---|---|---|---|---|---|---|---|---|
| P1 overlap | ours_p1 | theirs_a | 4 | 0 | none | 3.000000e-01 | 2.000000e-01 | 1.000000e-02 | 1.500000e-01 |
| P2 touches at an end point | ours_p2 | theirs_b | 3 | 0 | none | 2.000000e-01 | 2.000000e-01 | 0.000000e+00 | 2.000000e-01 |
| P3 disjoint by 1e-15 | ours_p3 | theirs_b | 3 | 1 | C4, `l = 3` | 2.000000e-01 | 2.000000e-01 | -1.000000e-15 | 2.000000e-01 |
| P4 l = 3 missing in ours | ours_p4 | theirs_a | 4 | 1 | C1, `missing in ours: l = 3` | 3.000000e-01 | 2.000000e-01 | 1.000000e-02 | 1.500000e-01 |
| P5 c = 11 at l = 3 in ours | ours_p5 | theirs_a | 4 | 1 | C2 (ours), `l = 3` | 3.000000e-01 | 2.000000e-01 | 1.000000e-02 | 1.500000e-01 |
| P6 lo = hi in ours at l = 3, c·r_* | ours_p6 | theirs_a | 4 | 1 | C3 (ours), `l = 3` | 3.000000e-01 | 2.000000e-01 | 0.000000e+00 | 1.500000e-01 |

P1 to P4 are the four cases the task names. P5 and P6 are added so that C2 and C3 can fail too. In P1 the smallest overlap is at l = 4,
c·r_* (ours [8.79, 8.9] against theirs [8.6, 8.8]) and the largest gap at l = 2, c·r_* (9.35 against 9.2). In P2 the l = 3 c·r_* brackets are
[8.5, 8.7] and [8.7, 8.9]. In P3 ours ends at 8.699999999999999, theirs starts at 8.7.

## Controls on the real data (`--mutate=NAME` of compare_brackets.py, each must exit 1; targets written before the first run)

The mutation changes the ours table after it is read, before the checks. The l of each is fixed in the script.

| mutation | what it does | first FAIL line must contain | the other FAIL lines (exactly) |
|---|---|---|---|
| `shift` | adds 1e-12 to all four ends of ours' row l = 1500 | `C4` and `l = 1500` | `C5`, `l = 1500` |
| `drop` | removes ours' row l = 777 | `C1` and `missing in ours: l = 777` | none |
| `swap` | exchanges the c·r_* and c·r_neg columns of ours' row l = 2000 | `C4` and `l = 2000` | `C5`, `l = 2000` |

Why `shift` uses l = 1500 and 1e-12: a shift of delta separates two brackets that intersect (both hold the root x, ours [a, b], theirs
[c, d]) whenever delta > d - a, and d - a <= (width of ours) + (width of theirs). Theirs has width 2.000001e-14 at every l (measured now from
`sweep_brackets.csv`). Ours has width at most 2e-13 for every l (the line "widest bracket in the table: 2e-13" of
`threshold_isolation_output.txt`). So 1e-12 exceeds the sum 2.2e-13 at every l, in particular at l = 1500, an l that #2's printed table does
not show. After step 2 the two widths at l = 1500 are read from the two csv files and the inequality 1e-12 > sum is confirmed; if it fails,
that is reported and the size is not changed. `swap` at l = 2000 moves c·r_* ≈ 8.4857 onto c·r_neg ≈ 9.636, a gap of 1.15. `drop` at
l = 777 removes a row nothing else depends on.

## Run notes (filled after the runs)

Steps: 1 this README; 2 `--csv` run (about 12 min, 1 h stop); 3 planted, real comparison, controls (seconds); 4 final run into
`phase2/dg_proof/compare_brackets_output.txt`. Launcher: `run_step.sh`. Stop condition: a run still going after 1 h of wall time is stopped.
Memory is only reported.
