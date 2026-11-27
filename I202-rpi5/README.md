# I202-rpi5: logs of TS13 Table I read against growth.csv and the crate

Machine: rpi5-ubuntu (4 cores, 8 GB, aarch64, Python 3.14 venv `negative-mass-venv314`). Issue:
https://github.com/nmoinvaz/negative-mass/issues/202. Code: branch `wip/i202-ts13-digits` of negative-mass, script
`notes/wormhole_largeD/ts13_digits.py`. Runner: `negative-mass-rpi5-i202`, started by the coordinator over hc.

## What is being checked

Torii and Shinkai 2013 (TS13, arXiv:1309.2058, PRD 88, 064027), Table I, the unstable mode's growth rate at D = 4 … 11.
For each D: the value as printed, its conversion to this repository's W²a², growth.csv's value, and #195's qd value in
`w2_output.txt`. Where growth.csv has digits beyond the printed ones, the source from `git log -p`.

## Plan, written before the reading

- The arXiv text is downloaded to this folder (under `ts13_download/`, see Files) and read as data. No code from it runs.
- The table is copied by eye from the page image and from the text layer, and the two are compared; the copy is
  `ts13_table_I.txt`. If the journal version cannot be fetched, only the arXiv version is recorded, and that is said.
- The conversion to W²a² is stated from TS13's own definitions and checked on one row against the crate's value.
- `ts13_digits.py` holds the printed values as strings. Its check fails on a mistyped digit; `--mutate=` changes one digit.
- Pass criteria: every printed value agrees with the crate to its last printed digit (± half a unit) or the row is
  reported as a discrepancy. A mismatch is reported, not loosened.

## Result

Run on the branch `wip/i202-ts13-digits` (commits a15576a script and output, da61246 literature entry), main at 1839211.

- TS13 Table I prints ω² (a = 1) to 15 significant digits at n = D = 4 … 11, 20, 50, 100. The three readings (page image, PDF
  text layer, TeX source of arXiv v1) agree on all 11 rows (`compare_sources.log`). The journal version was not read: the
  publisher returned HTTP 403 (`ts13_download/aps/abstract.html` is the challenge page).
- Conversion: W²a² = −ω². Checked on every row against the crate, relative difference at most 4.4e-10 (D = 4).
- growth.csv's D = 4 … 11 rows are the printed values rounded to 12 decimals (TS13 prints 14 decimals at D = 4 … 8, 13 at
  D = 9 … 11). No csv digit goes beyond the printed ones. Source: `profiles.py`'s `TS13` dict (typed 15-digit floats,
  lines 23-25), written by `f"{v:.12f}"`, one commit 9bf716e (2026-10-24); the rows are byte-identical on main and on
  `wip/i200-growth-csv` (`git_history.log`).
- TS13's printed digits are not the crate's: all 11 differ by 9.9e-12 to 6.4e-10 (relative 9.4e-13 to 4.4e-10), 9.35 to 12.03
  significant digits agree, none to the last printed decimal. `one_mode.log` N4, which solves TS13's own W(r) of (3.18)
  (checked equal to its U, exactly, W1) and shares no code with the crate, equals the crate at its 12 printed digits at
  D = 4, 10, 20, 50. So the 10th to 12th significant digits of Table I are not reproduced by two solvers; the csv's rows
  carry TS13's error.

## Disagreements with the repository's text

- `w2_highprec.md` (the paragraph under the growth.csv table, and recommended task 4) and #202's "Why" say the csv's last
  digits do not all come from TS13's table, because README.md quotes 8 to 10 digits. They do all come from it: README.md
  quotes roundings of a 15-digit table (R1), and the crate, not the csv, differs from TS13.
- `README.md` References: "Table I read for this note (full-precision values quoted above)". The table above it quotes TS13 to
  8 to 13 digits (D = 4: 1.39705243), not the printed 15.
- Nothing quoted in Paper III changes under either option below (`option_b_paper_numbers/`).

## Recommendation for growth.csv's D = 4 … 11 rows (not applied)

| | A: as is | B: crate rounded to 12 decimals |
|---|---|---|
| csv − crate, D = 4 … 11 | −6.19e-10, −7.38e-11, −1.24e-10, −1.07e-10, −9.5e-12, +2.41e-10, +2.46e-10, +1.69e-10 | at most 4.9e-13 (the rounding; half a unit of the 12th decimal is 5e-13) |
| rows equal to the other at 8 decimals | 7 of 8 (D = 9 differs: 10.15355305 against 10.15355304) | same |
| rows equal at 10 decimals | 1 of 8 (D = 8) | same |
| Paper III table, rows D = 4 … 8, 10 (8 decimals) | unchanged | unchanged |
| `paper_numbers.py` rerun | baseline | exit 0, 0 checks failed; only the W²a² column's 10th decimal and the source label of the 8 rows change |
| cost | none; relabel the source "TS13 Table I, rounded" | `w2_highprec.py` `read_csv` splits each line into exactly 3 fields, so a 4th column raises ValueError: put TS13's strings in a separate file; `check_growth.py` G3, G4, G6 retarget (G1 too if a column were added); Paper III's Table 1 and Fig. 6 captions say "Torii and Shinkai's" for D <= 11 |

Recommend B for the values: one source for all 16 rows, right to the 12th decimal, validated by a second solver at four D, and
no quoted number moves. Keep TS13's printed strings where `ts13_digits.py` holds them, not as a 4th csv column. If the
coordinator prefers A for Paper III's provenance, only the label needs a change, since the rows do not claim more digits than
TS13 printed.

## Slips and lessons

- T2 first failed 0 of 11: profiles.py's dict holds −ω², my strings the printed ω². Fixed the check, not the data.
- The TeX source holds non-UTF-8 bytes in a comment (`open(..., encoding="latin-1")`); `compare_sources.py` first missed the two
  table rows that pdftotext splits over lines (n = 6, 50).
- The selftest caught a wrong declared target: a 7th-decimal change of the crate at D = 20 is 3e-9 relative, under K1's 1e-8
  bar, so only O1 fired. Kept as `crate_7` (O1), added `crate` at the 6th decimal (K1 and O1).
- `one_mode.py`'s N4 shooting is nested inside `numerical()`, so it could not be called per D without copying code; its
  printed values at four D are used as logged.

## Files

```
I202-rpi5/
├── README.md                    this file
├── ts13_table_I.txt             the table as read from the page image, and the paper's conventions
├── compare_sources.py / .log    image reading, text layer and TeX source compared, 11 of 11 equal, exit 0
├── compare_sources_mutated.log  one digit changed in the image reading: 1 differs, exit 1
├── git_history.log              commits and diffs of growth.csv and profiles.py
├── ts13_digits_run.log          plain run of notes/wormhole_largeD/ts13_digits.py, exit 0
├── selftest.log                 --selftest, 15 mutations plus the baseline, exit 0
├── mutations/mutate_*.log       each --mutate=NAME, exit 1, with the checks that fired
├── option_b_paper_numbers/      paper_numbers.py on scratch copies of growth.csv (A as is, B crate rows) and their diff
└── ts13_download/               arXiv abs page, v1 PDF, text layer, e-print and TeX source (figures not kept), page
                                 image and crop, INSPIRE and Crossref records, the APS challenge page (HTTP 403)
```
