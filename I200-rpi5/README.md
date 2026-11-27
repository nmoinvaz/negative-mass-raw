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

**Declared targets: none yet.** Each mutation's targets are computed in a development run (`dev_*`), then written below under
"Declared targets" in an amendment committed before the runs of record (`run_*`). A mutation is on target when exactly its declared
checks fail and no other; one that fails nothing is reported silent.

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

(filled in as they are made)
