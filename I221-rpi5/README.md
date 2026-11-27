# I221-rpi5: growth.csv's D = 4 … 11 rows from #195's crate, and what reads them

Machine: rpi5-ubuntu (4 cores, 8 GB, aarch64, Python 3.14.10 venv `negative-mass-venv314`, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0,
matplotlib 3.11.2). Issue: https://github.com/nmoinvaz/negative-mass/issues/221 (option B of #202). Code: branch
`wip/i221-growth-lowD` of negative-mass (base 4bced01), worktree `~/Source/negative-mass-i221`. Runner: `negative-mass-rpi5-i221`,
started by the coordinator over hc. One process at a time, `nice -n 10`, in the foreground; every stdout is logged here; reruns are
numbered and no log is overwritten. Load at the start: 0.33.

## What is done

1. `profiles.py` writes all 16 rows of `growth.csv` from the table "growth.csv against the crate (qd)" of
   `notes/wormhole_largeD/w2_output.txt`: the crate's quad-double value rounded to 12 decimals (half to even on the printed
   decimal digits, no float), source `w2_crate qd (#195)`. growth.csv keeps three columns and no comma in the source
   (`w2_highprec.py`'s `read_csv` is a plain `split(",")`). The `TS13` dict stays in profiles.py: `write_profiles` takes the D = 10
   profile's eigenvalue from it, `profiles.csv` stays as committed, and `ts13_digits.py` T2 and `check_growth.py` read the dict.
   Torii and Shinkai's printed values are `ts13_digits.py`'s `PRINTED`.
2. `check_growth.py` checks all 16 rows against the crate (below).
3. `paper_numbers.py` is rerun unchanged; `logs_paper_numbers.txt` is the new output (old: 4bced01), every printed number that
   changed is listed in the note.
4. `notes/wormhole_largeD/growth_lowD.md`: the eight rows old and new; every number in README.md and Paper III that reads them and
   whether it changes at its printed digits; proposed text where one does.

Files written: `profiles.py`, `growth.csv`, `check_growth.py`, `logs_check_growth.txt`, `logs_paper_numbers.txt`, `growth_lowD.md`.
Nothing else in the repository. Read-only runs on the new csv, logged here and not committed to the repository: `ts13_digits.py`
(it reads growth.csv, so its C1 is expected to fail, see below), `paper/figures/make_figures.py`'s `fig6_wormhole` into a scratch
folder (its reader splits the markers on `source.startswith("TS13")`), `w2_highprec.py`'s `read_csv` on the new file.

## Criteria (coded as worded here; written before the first run of the new `check_growth.py`)

Rows (the csv written by profiles.py; the crate column is w2_output.txt):
- **G1** unchanged: header `D,W2a2,source`, exactly the 16 rows D = 4, 5, 6, 7, 8, 9, 10, 11, 20, 30, 50, 100, 200, 500, 1000, 2000,
  once each, in this order, three fields each.
- **G2** (the issue's acceptance, widened from D >= 20 to all rows) the W2a2 field of every row equals the crate's qd value rounded to
  12 decimals, as a string of exactly 12 decimals, with `check_growth.py`'s own parser and rounding (exact rationals, not
  profiles.py's `Decimal`). Met only if 16 of 16.
- **G3** the source field of every row is `w2_crate qd (#195)`.
- **G4** (was: D <= 11 rows equal TS13's value at 12 decimals; retargeted to the cross-check that shares nothing with the crate) for
  each D <= 11 the W2a2 field is within relative 1e-8 of profiles.py's `TS13[D]`, read from the dict's source text (ast), not by
  import. The bar is `ts13_digits.py` K1's, set by #202 before this task: the digits README.md quotes for TS13 at D = 4 and 10.
  The worst relative difference known from #202 is 4.4e-10 (D = 4). 8 of 8.
- **G5** unchanged: the table's D = 50 value equals the 64-value list's D = 50 value rounded to the table's decimals.
- **G6** (was: D <= 11 rows equal 613e866's; retargeted to #221's scope) each D >= 20 row, all three fields, equals the same row of
  `git show 4bced01:notes/wormhole_largeD/growth.csv`: those rows are not touched by #221. 8 of 8. The D <= 11 rows differ from
  4bced01's by design; their old and new values are *reported, not gated*. `--old-rev=REV` as before, default now 4bced01.
- *Reported, not gated:* csv against the crate (exact) and the margin of each crate value from a rounding tie, for all 16 rows; TS13's
  printed values against the crate and against the old and new rows.

Remainder (unchanged in method; s = 2(D − 3); Ω0 … Ω3 closed forms of #26 and #208, Ω4 the fit of #195):
- **R0, R1, R2** exactly as in #200 (I200-rpi5/README.md). The enclosure of the reported columns is now 5e-13 s^p for all 16 rows (the
  rounding of the 12th decimal given the crate's value); for D <= 11 it was |crate − csv| s^p.

An error bar here is an enclosure of the rounding of the 12th decimal given the crate's value. It is not the crate's own error and not
a fit spread.

## What the change is expected to do elsewhere (predictions, written before any run)

- `ts13_digits.py`: **C1 fails** at 8 of 8 rows (the csv now holds the crate's digits, which differ from TS13's by 9.9e-12 to 6.4e-10,
  more than the half unit of the 12th decimal), and so `--selftest` fails at its baseline. T1, T2, T3, R1, K1, P1, O1, W1, W2 pass.
  The file is not on this task's list, so it is not edited; the retarget is proposed in the note.
- `make_figures.py` `fig6_wormhole`: runs; all 16 markers take the "this work" style because no source starts with `TS13`; the
  legend keeps an entry for an empty series. Not on the list; reported.
- `paper_numbers.py`: exit 0, "checks failed: 0". The D = 4 … 11 rows move at the 10th to 11th decimal (the crate against TS13), so
  the printed 10-decimal W²a² change at D = 4 … 11; the relative differences from the 3-term formula, the (data − 3 terms) s²
  column, the e-folding times and the ST17 slopes do not change at their printed digits. The source column changes for 8 rows.
  Paper III's printed values are expected not to change (the issue's expectation); the note lists each place and checks it.
- `w2_highprec.py`'s `read_csv` reads the new file (16 rows).

## The mutation, and the declared targets

`check_growth.py --mutate=NAME` breaks the data as read, in memory; it never writes the csv. Names: `last_digit:D` (the last digit of
row D's W2a2, + 1 unit of the 12th decimal; D any of the 16), `drop_row:D`, `source:D` (row D's source replaced by the label it had
before: `TS13 Table I` for D <= 11, `modes_r.py` for D >= 20), `revert_lowD` (rows D = 4 … 11 put back to TS13's rounded values and
label: the change not applied), `ts13_swap` (the W2a2 of rows 4 and 5 swapped), `ts13_digit:D` (D = 4 … 11; profiles.py's TS13 value
with its 6th decimal + 1, at least 7e-8 relative, over G4's bar), `crate_scale` (every crate value times 1 + 1e-12), `round_trunc`
(the reference truncates instead of rounding), `list50` (the list's D = 50 value + 2e-18), `wrong_om2` (the π² ln 2 term of Ω2
flipped), `wrong_om3` (the 384ζ(3) term of Ω3 flipped), `s_off` (s = 2(D − 2)). 65 runs with the unmutated one.

**Predictions** (before the development run; the declared targets come from the development run, as amendment A1, before any run
of record):

| mutation | predicted failing checks |
|---|---|
| none | none, exit 0 |
| `last_digit:D`, D = 4 … 11 | G2 |
| `last_digit:D`, D = 20, 30, 50, 100 | G2, G6 |
| `last_digit:D`, D = 200 … 2000 | G2, G6, R1, R2 |
| `drop_row:D`, D = 4 … 11 | G1, G2, G3, G4 |
| `drop_row:D`, D = 20 … 100 | G1, G2, G3, G6 |
| `drop_row:D`, D = 200 … 2000 | G1, G2, G3, G6, R1, R2 |
| `source:D` | G3 |
| `revert_lowD` | G2, G3 |
| `ts13_swap` | G2, G4 |
| `ts13_digit:D` | G4 |
| `crate_scale` | G2, G5 |
| `round_trunc` | G2 |
| `list50` | G5 |
| `wrong_om2` | R0, R1, R2 |
| `wrong_om3` | R0, R2 |
| `s_off` | R1, R2 |

A run of record is on target when `compare_targets.py` finds exactly the declared checks, no more and no fewer (the script and the
driver `run_mutations.sh` are #200's, with the path and the names changed). A mutation that fires nothing is reported as silent.

## Amendment A1: declared targets (after the development run, before any run of record)

Development run: `dev_03_summary.log` (65 runs, `run_mutations.sh`, one log each in `dev_03_mutations/`); `declare_targets.py` wrote
`declared_targets.json` from it. The unmutated checker, `dev_02_check_growth_unmutated.log`, passes G1 to G6 and R0 to R2 (exit 0).
64 of 65 runs matched the predictions above. **One prediction was wrong:** `source:D` for D >= 20 fires G3 **and G6**, not G3 alone,
because G6 compares all three fields of a row with 4bced01's and the mutation changes the third (a slip in my prediction table; G6's
text above says "all three fields"). No criterion or tolerance was changed. Declared targets:

| mutation | checks that fail (and no other) |
|---|---|
| none | none, exit 0 |
| `last_digit:D`, D = 4 … 11 | G2 |
| `last_digit:D`, D = 20, 30, 50, 100 | G2, G6 |
| `last_digit:D`, D = 200 … 2000 | G2, G6, R1, R2 |
| `drop_row:D`, D = 4 … 11 | G1, G2, G3, G4 |
| `drop_row:D`, D = 20 … 100 | G1, G2, G3, G6 |
| `drop_row:D`, D = 200 … 2000 | G1, G2, G3, G6, R1, R2 |
| `source:D`, D = 4 … 11 | G3 |
| `source:D`, D >= 20 | G3, G6 |
| `revert_lowD` | G2, G3 |
| `ts13_swap` | G2, G4 |
| `ts13_digit:D`, D = 4 … 11 | G4 |
| `crate_scale` | G2, G5 |
| `round_trunc` | G2 |
| `list50` | G5 |
| `wrong_om2` | R0, R1, R2 |
| `wrong_om3` | R0, R2 |
| `s_off` | R1, R2 |

The issue's acceptance "the row mutation fires on each row": `last_digit:D` fires G2 at all 16 D (G2 alone at D <= 11, where G4's
bar is 1e-8 and G6 reads D >= 20 only).

## Runs

(filled in as they are done)
