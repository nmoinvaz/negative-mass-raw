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

## Amendment A2: the printed-digits script (written before it was run)

`printed_digits.py` (this folder; reads the checkout, writes nothing there) answers "does this printed number change?" for the
numbers that read the D <= 11 rows. It parses the printed strings from `paper/3-wormhole-largeD/main.tex` (Table 1: W²a², relative
difference from the three-term formula, (difference)·s², for D <= 11; Table 2: 1/(Wa) and the predicted slope 1/(√2 W a) at D = 4, 5, 6)
and from `notes/wormhole_largeD/README.md` (the table's [TS13] column at D = 4, 10; the e-folding times 0.846, 0.579, 0.462 of
"What it means"), recomputes each from the old rows (`git show 4bced01:…/growth.csv`) and the new rows at the printed number of
decimals or significant digits, and compares. Verdicts: `unchanged` (old = new = printed), `NEW DIFFERS` (new rounding is not the
printed number), `printed != old` (the printed number was not the old rows' rounding: a discrepancy). Exit 1 unless every cell is
`unchanged`. The formula is `paper_numbers.py`'s (OM0 = −4 ln 2, OM1 = 2π²/3 + 8 ln²2, s = 2(D − 3)).

`--mutate=bump:D` adds 1e-6 to the new row D (D = 4 … 11). **Predictions:** `bump:4` and `bump:10` fire the Table 1 W²a² cell and
the README [TS13] cell of that D; `bump:5`, `6`, `7`, `8` fire the Table 1 W²a² cell of that D only; `bump:9` and `bump:11` fire
nothing (those D are printed nowhere in these two files). The relative-difference and (difference)·s² cells and the 1/W cells are
not predicted to fire for a 1e-6 shift (largest shift of any such cell: 1e-6 · s² = 2e-4 at D = 10, against units of 0.1 or 1).
Declared targets come from the development run, as for `check_growth.py`.

## Amendment A3: extension from the coordinator, `ts13_digits.py` retargeted (written before any change to it)

hc, 2026-11-27: `ts13_digits.py` joins the file list, because main must not carry a check that fails at baseline (C1 failed 0 of 8 on
the new csv, `run_05_ts13_digits.log`). The issue stays open; `running` is back. Ruled by the coordinator: `make_figures.py` and every
paper or README text go to #210; `stability.py` and `order4.py` stay as they are (they read `w2_output.txt`, not growth.csv).

Criteria, coded as worded here:
- **C1** (retargeted) TS13's printed values (`PRINTED`), converted, rounded half-even to 12 decimals, equal the old growth.csv's rows
  D = 4 … 11, and TS13 prints more than 12 decimals there. The old rows are a constant `OLD_ROWS` in the script, typed from
  `git show 4bced01:notes/wormhole_largeD/growth.csv` lines 2 to 9 (byte-identical at 613e866) and cited there; C1 does not read the
  current csv. 8 of 8.
- **C2** (new) the current growth.csv's rows D = 4 … 11 equal the crate's qd value (w2_output.txt, the script's own `read_crate`)
  rounded to 12 decimals, as check_growth.py's G2 does for them, with this script's own parser and `Decimal` rounding. 8 of 8.
- All other checks (T1, T2, T3, R1, K1, P1, O1, W1, W2) unchanged. The reported blocks change: the last one compares the old rows
  (`OLD_ROWS`) and the current rows with the crate.
- `OLD_ROWS` against the git file is verified once in a raw script (`verify_old_rows.py`); C1 itself would fire on a typo
  (mutation `old_rows`).

Mutations: the 15 of #202 keep their names; `csv` is retargeted (C2), and two are new: `old_rows` (`OLD_ROWS` D = 6, 12th decimal + 1)
and `crate_lowD` (the crate's D = 6 value, 12th decimal + 1, 9e-12 relative 2e-12, under K1's bar).

**Predictions** (before the development run; targets are declared from it as amendment A3b, before the run of record). Changes
from #202's declared sets (`ts13_digits_output.txt` as committed) are marked:

| mutation | predicted failing checks |
|---|---|
| none | none |
| `digit_last` | T2, T3 |
| `digit_8` | T2, T3, R1, C1 |
| `digit_12` | T2, T3, C1 |
| `digit_6` | T2, T3, C1, K1 |
| `drop_zero` | T1, T3 |
| `sign`, `sqrt` | C1, K1 |
| `csv` | **C2** (was C1) |
| `profiles` | T2 |
| `crate`, `crate_7` | K1, O1 and O1 |
| `onemode` | O1 |
| `wformula` | W1 |
| `upot` | W1, W2 |
| `halfunit` | P1 |
| `old_rows` (new) | C1 |
| `crate_lowD` (new) | C2 |

So the only prediction that differs from #202's declared sets is `csv`; the five that the retarget experiment of `run_06` showed losing
C1 keep it, because C1 again reads TS13's printed value. (That experiment retargeted C1 to the crate; this retarget does not.)

## Runs

All exit 0 unless stated; one process at a time, `nice -n 10`, rpi5. `run_mutations.sh OUTDIR` runs `check_growth.py` with no mutation and
with each of the 64 mutations (65 runs; a mutation exits 1 by design). `compare_targets.py SUMMARY declared_targets.json` compares each
run's failed checks with the declared ones.

| log | what | result |
|---|---|---|
| `growth_4bced01.csv`, `profiles_4bced01.csv`, `logs_check_growth_4bced01.txt`, `logs_paper_numbers_4bced01.txt` | the base commit's files | copies |
| `dev_01_profiles_growth_only.log` | new `profiles.py --growth-only` | 4 s; 8 rows changed, the D >= 20 rows byte-identical |
| `dev_02_check_growth_unmutated.log` | first run of the new checker | G1 to G6, R0 to R2 pass |
| `dev_03_summary.log`, `dev_03_mutations/` | 65 development runs | 64 of 65 as predicted; `source:D` at D >= 20 also fires G6 (A1) |
| `dev_04_printed_digits/` | `printed_digits.py --mutate=bump:D`, 8 runs | all as predicted (A2) |
| `run_01_profiles_growth_only.log` | `profiles.py --growth-only` again | growth.csv byte-identical |
| `run_02_check_growth.log` (= `logs_check_growth.txt`) | checker of record | exit 0; G1 to G6, R0 to R2 pass |
| `run_03_summary.log`, `run_03_compare_targets.log`, `run_03_mutations/` | 65 runs of record | 65 of 65 on target |
| `run_04_paper_numbers.log` (= `logs_paper_numbers.txt`) | `paper_numbers.py` on the new csv | exit 0, checks failed: 0; 8 of 37 lines differ from the base's (the eight rows) |
| `run_05_ts13_digits.log`, `run_05_ts13_digits_selftest.log` | `ts13_digits.py`, `--selftest` on the new csv (read-only) | **exit 1, 1**: C1 fails at 8 of 8 (predicted); selftest baseline fails, 9 of 15 mutations off target |
| `run_06_ts13_digits_C1_retarget_selftest.log`, `ts13_digits_C1_retarget.diff` | C1 retargeted to the crate, on a scratch copy | passes; 10 of 15 mutations on target, five lose C1 |
| `run_07_fig6_reader.log`, `run_07_fig6_committed.png`, `run_07_fig6_new.png`, `fig6_reader_check.py` | `fig6_wormhole` into a scratch folder | runs; 0 of 16 rows start with `TS13`; the D <= 11 markers change style |
| `run_08_read_csv.log` | `w2_highprec.read_csv` on the new file | 16 rows |
| `run_09_printed_digits.log` | `printed_digits.py` | 31 of 31 cells unchanged |
| `run_10_printed_digits/`, `run_10_compare.log`, `declared_printed_digits.json` | its 8 mutations and the unmutated run | 9 of 9 on target |
| `run_11_relabel_readers.log`, `relabel_readers.py` | `stability.py:54` and `order4.py:808` on `w2_output.txt` relabelled | the first raises, the second matches 0 of 16 rows |

Code of record: `wip/i221-growth-lowD` of negative-mass; the note is `notes/wormhole_largeD/growth_lowD.md`.

## Not met, or reported

- **No acceptance criterion of the issue failed.** No criterion or tolerance was changed after a run. No mutation was silent
  (`bump:9`, `bump:11` of `printed_digits.py` fire nothing by declaration).
- **`ts13_digits.py` C1 fails** on the new csv, as predicted; the file is not on the task's list (note, "Reported, not fixed").
- **`make_figures.py`'s marker split** no longer separates the D <= 11 rows; not on the list.
- **`stability.py:54`** (not mentioned by #200) breaks on the next regenerated `w2_output.txt`.
- **One prediction was wrong**: `source:D` at D >= 20 (A1).
