# I200-rpi5: logs of regenerating growth.csv from #195's crate and rechecking Paper III's growth rates

Machine: rpi5-ubuntu (4 cores, 8 GB, aarch64, Python 3.14.10 venv `negative-mass-venv314`, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0
with the pure-Python backend, sympy 1.14.0). Issue: https://github.com/nmoinvaz/negative-mass/issues/200. Code: branch
`wip/i200-growth-csv` of negative-mass (base 613e866), worktree `~/Source/negative-mass-i200`. Runner: `negative-mass-rpi5-i200`,
started by the coordinator over hc. One process at a time, `nice -n 10`; every stdout is logged here; reruns are numbered, no log is
overwritten.

## Ruling: the source string

The task's string was `w2_crate qd, #195`. Its comma makes `w2_highprec.py`'s `read_csv` (`line.strip().split(",")`, line 137) raise
`ValueError: too many values to unpack` (tested on a one-row copy; `csv.DictReader` reads it). **At the coordinator's request** (hc, after
I reported this) the string is `w2_crate qd (#195)`, so that #195's file stays untouched. The criteria below use it.

## What is done

1. `profiles.py` writes `growth.csv`. Rows D = 4 … 11 stay as they are (TS13's 15-digit values of profiles.py's `TS13` dict at 12
   decimals, source `TS13 Table I`; #202 decides their digits). Rows D = 20, 30, 50, 100, 200, 500, 1000, 2000 take the crate's
   quad-double value from the table "growth.csv against the crate (qd)" of `notes/wormhole_largeD/w2_output.txt`, rounded to 12
   decimals (half to even on the printed decimal digits), source `w2_crate qd (#195)`. No float enters the D >= 20 rows.
2. `check_growth.py` (new, beside it) reads `growth.csv` and `w2_output.txt` with its own parser and rounding (exact rational
   arithmetic, not profiles.py's `Decimal`), and checks the rows and the remainder columns below.
3. `paper_numbers.py` is rerun unchanged on the new csv; `logs_paper_numbers.txt` is the new output (the old one is in 613e866).
4. `growth_update.md` lists every quoted number that read growth.csv with old value, new value, source line and proposed text.

## Criteria (coded as worded here; written before the first run of `check_growth.py`)

Rows (the csv written by profiles.py; the crate column is w2_output.txt):
- **G1** The file has the header `D,W2a2,source` and exactly the 16 rows D = 4, 5, 6, 7, 8, 9, 10, 11, 20, 30, 50, 100, 200, 500,
  1000, 2000, once each, in this order.
- **G2** (the issue's acceptance) For each D >= 20, the W2a2 field equals the crate's qd value rounded to 12 decimals, as a string of
  exactly 12 decimals. Met only if 8 of 8.
- **G3** The source field is `w2_crate qd (#195)` for D >= 20 and `TS13 Table I` for D <= 11.
- **G4** For each D <= 11, the W2a2 field equals profiles.py's `TS13[D]` rounded to 12 decimals (string of exactly 12 decimals).
  8 of 8. The checker takes `TS13` from the source text of profiles.py (ast), not from an import.
- **G6** (added before the first run of `check_growth.py`) For each D <= 11, the whole row (all three fields) equals the same row of
  `git show 613e866:notes/wormhole_largeD/growth.csv`: those rows stay as they are. 8 of 8.
- **G5** The table's value at D = 50 equals the 64-value list's value at D = 50 rounded to the table's number of decimals (two
  places of the same file that must agree).
- *Reported, not gated:* crate − csv for all 16 rows (the TS13 rows differ from the crate by 9.5e-12 to 6.2e-10 and are expected
  to; the D >= 20 rows by at most 5e-13), and the margin of each D >= 20 value from a rounding tie.

Remainder columns (from the csv rows; s = 2(D − 3); Ω0 … Ω3 the closed forms of #26 and #208, Ω4 the fit of #195):
- **R0** The closed forms Ω0, Ω1, Ω2, Ω3 equal the first block's values of the B4 grid printed in `order5_output.txt` to 1e-50
  (a typing check of the constants against a numeric evaluation that shares nothing with them).
- **R1** At D = 200, 500, 1000, 2000: (W − [s + Ω0 + Ω1/s + Ω2/s²]) s³ from the csv row equals the "crate (qd)" column of
  w2_output.txt's remainder table within 5e-13 s³ + 5e-8 (the csv's rounding, the printed 7 decimals).
- **R2** At D = 200, 500, 1000, 2000: (W − [… + Ω3/s³]) s⁴ from the csv row equals the printed rem·s⁴ of `order5_output.txt` (lines
  of the "reported, not gated" table) within 5e-13 s⁴ + 5e-8.
- *Reported, not gated:* for all 16 rows the three columns (W − 3-term) s², (W − 4-term) s³, (W − 5-term) s⁴ with their
  enclosures ±5e-13 s^k (D >= 20; the rounding of the 12th decimal against the crate, a rigorous enclosure; the TS13 rows add
  |crate − csv| s^k), the same first column from the old csv (`git show 613e866:…/growth.csv`), and the relative differences.

An error bar here is an enclosure of the rounding of the 12th decimal given the crate's value. It is not the crate's own error
(an estimator range, 1e-60 at the digits shown, w2_highprec.md) and not a fit spread.

## The mutation, and the declared targets

`check_growth.py --mutate=NAME` breaks the data as read, in memory; it never writes a csv. Names: `last_digit:D` (the last digit
of row D's W2a2, +1 unit of the 12th decimal; D any of the 16), `drop_row:D`, `source:D` (the source of row D replaced by
`modes_r.py`), `ts13_swap` (the W2a2 of rows 4 and 5 swapped), `crate_scale` (every crate value times 1 + 1e-12), `round_trunc`
(the reference truncates instead of rounding), `list50` (the list's D = 50 value + 2e-18), `wrong_om2` (the π² ln 2 term of Ω2
flipped), `wrong_om3` (the 384ζ(3) term of Ω3 flipped), `s_off` (s = 2(D − 2)).

**Declared targets** (amendment A1, committed before any run of record). The development run is `dev_04_summary.log` (56 runs,
`run_mutations.sh`, one log each in `dev_04_mutations/`); `declared_targets.json` holds the targets as read from it. Summary:

| mutation | declared checks that fail (and no other) |
|---|---|
| none | none, exit 0 |
| `last_digit:D`, D = 4 … 11 | G4, G6 |
| `last_digit:D`, D = 20, 30, 50, 100 | G2 |
| `last_digit:D`, D = 200, 500, 1000, 2000 | G2, R1, R2 (the remainder checks read these four rows) |
| `drop_row:D`, D = 4 … 11 | G1, G3, G4, G6 |
| `drop_row:D`, D = 20, 30, 50, 100 | G1, G2, G3 |
| `drop_row:D`, D = 200, 500, 1000, 2000 | G1, G2, G3, R1, R2 |
| `source:D`, D = 4 … 11 | G3, G6 |
| `source:D`, D >= 20 | G3 |
| `ts13_swap` | G4, G6 |
| `crate_scale` | G2, G5 (the list's D = 50 is not scaled) |
| `round_trunc` | G2 (at D = 50, 100, 200), G4 (at D = 5, 6, 8, 9, 10, 11) |
| `list50` | G5 |
| `wrong_om2` | R0, R1, R2 |
| `wrong_om3` | R0, R2 (R1 stops at Omega_2) |
| `s_off` | R1, R2 |

No mutation was silent in the development run. The predictions I wrote down before it (a one-digit change fails G2 at D >= 20 and
G4, G6 at D <= 11, and also R1, R2 at the four D of the remainder checks) all held. A run of record is on target when
`compare_targets.py` finds exactly the declared checks, no more, no fewer.

## Ruling already made on the data

- The old csv's `modes_r.py` rows do not reproduce across machines: the unmodified `profiles.py` rerun on this machine
  (`dev_01_*`, 1 min) differs from the committed rows by 1e-12 (D = 50) to 2.7e-8 (D = 2000), and `profiles.csv` by up to 1.8e-9
  relative (270 of 600 cells in the D = 10 column, whose eigenvalue is TS13's fixed value). The new D >= 20 rows do not depend on
  the machine.

## Files that read, or quote, growth.csv (found by grep of the worktree, 613e866)

Read the file:
- `notes/wormhole_largeD/profiles.py` (writer), `paper_numbers.py` (csv.DictReader), `w2_highprec.py` (`read_csv`, a plain
  `split(",")`: only as Newton starts, and `check_growth`'s G1), `paper/figures/make_figures.py` `fig6_wormhole` (csv.DictReader;
  `source.startswith("TS13")` separates the two markers).
Quote its values or numbers derived from them (listed in growth_update.md):
- `notes/wormhole_largeD/README.md` (the table, "73", "66 ± 6", the 1/D fit, "4×10⁻¹⁰ to 1.5×10⁻⁶"), `paper/3-wormhole-largeD/main.tex` (abstract,
  Sec. 2 text and Table 1, Sec. 4 "settles near 73", "66 ± 6", Fig. 1 data), `notes/wormhole_largeD/one_mode.py` line 145 (a
  hard-coded copy of the D = 20, 50 values; N4's bar is 1e-6) with `one_mode.log` and `one_mode.md`, `notes/wormhole_next.md` line 241,
  `logs_paper_numbers.txt`.

## Runs

All exit 0 unless stated; one process at a time, `nice -n 10`, rpi5. `run_mutations.sh OUTDIR` runs `check_growth.py` with no mutation
and with each of the 55 mutations (56 runs; a mutation exits 1 by design). `compare_targets.py SUMMARY declared_targets.json` compares
each run's failed checks with the declared ones.

| log | what | result |
|---|---|---|
| `dev_01_profiles_baseline_613e866.log` + `dev_01_growth_baseline_rpi5.csv`, `dev_01_profiles_baseline_rpi5.csv` | unmodified `profiles.py` | 60 s; rows differ from the committed ones by 1e-12 to 2.7e-8, profiles by up to 1.8e-9 relative |
| `dev_02_profiles_growth_only.log` | new `profiles.py --growth-only` | growth.csv, TS13 rows byte-identical to 613e866 |
| `dev_03_check_growth_unmutated.log` | first run of the checker | G1 to G6, R0 to R2 pass |
| `dev_04_summary.log`, `dev_04_mutations/` | 56 development runs | every mutation fires; targets read from it |
| `dev_05_profile_sensitivity.log` (`profile_sensitivity.py`) | profiles with modes_r's against the crate's W^2 | max relative change 9.5e-10 (D = 20), 1.7e-9 (100), 7.7e-9 (1000); 59 s |
| `dev_06_fit_1overD.log` (`fit_1overD.py`) | README's 1/D fit, old and new rows | −4.772593 (old, cubic, D >= 50), −4.772588 (new, cubic), −4.772589 (new, quartic) |
| `run_01_profiles_full.log`, `run_01_growth.csv`, `run_01_profiles_rpi5.csv` | full `profiles.py` | 36 s; growth.csv equals the growth-only run; profiles.csv not committed |
| `run_02_check_growth.log`, `run_03_summary.log`, `run_03_compare_targets.log`, `run_03_mutations/` | checker and 56 runs, first code | exit 0; 56 of 56 on target |
| `run_04_paper_numbers.log` (+ `logs_paper_numbers_613e866.txt`) | `paper_numbers.py` on the new csv | exit 0, checks failed: 0; only the D >= 20 rows changed |
| `run_05_fig6_reader.log` | `make_figures.fig6_wormhole` on the new csv, output to a scratch folder | runs |
| `run_06_check_growth.log`, `run_07_*` | checker with the reported TS13 block, 56 runs | exit 0; 56 of 56 on target |
| `run_08_check_growth.log`, `run_09_*` | final checker (label-agnostic table parser), 56 runs | exit 0; 56 of 56 on target; output identical to run_06 |

`growth_613e866.csv`, `profiles_613e866.csv` are the files at the base commit. Code of record: `wip/i200-growth-csv` at 799b22a (checker
and profiles.py at a0b616a). The note is `notes/wormhole_largeD/growth_update.md`.

## Not met, or reported

- **Acceptance 1 for the 8 TS13 rows**: they equal TS13's printed values, not the crate's (by 9.5e-12 to 6.2e-10). Kept by the task; #202.
- **The task's source string** `w2_crate qd, #195` was replaced at the coordinator's request (above).
- **No criterion failed.** No mutation was silent. No criterion or tolerance was changed after a run; G6 was added to the criteria
  before the first run of the checker.
