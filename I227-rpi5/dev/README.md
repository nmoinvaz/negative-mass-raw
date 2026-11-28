# dev: development runs of I227-rpi5 (before the criteria were declared)

All run on rpi5 with `extended_bisect.py` of the wip branch; the commands are in each folder's `log.txt` / the unit names `nm-i227-dev-*`.

- `bisE1`, `bisF1`: variant E and F bisections of family S, D = 4, h = 0.02, bracket [4.7527e-05, 4.7528e-05] (narrow, around #40's p*), tolerance 1e-24, with the thinned series
  e = 3, 6, 9, 11, 12, 13, 14, 15, 16, 18, 20 (`series_m_*.jsonl`, `series_p_*.jsonl`) and the float64 series at the same amplitudes (`f64series_*.jsonl`).
- `f64a` (tolerance 1e-14, k = 0 … 7), `f64c` (tolerance 1e-17, k = 0 … 7): float64 bisections from the brackets of `bracket_k`; k = 0 reproduces #40's p*ₕ bit for bit.
- `stall/D4`, `D5`, `D6`: three stall pairs each (the runs of record use eight).
- `pert/`: `scaleP16` (eta = 1e-16 on the amplitude), `bumpP8`, `bumpP10`, `bumpP16`, `bumpM16` (bump in r); `bumpP8_failed_bracket1e-10` is a first try whose bracket
  (p* ± 1e-10) did not straddle the shifted threshold (p* moves by −2.2e-9 at eta = 1e-8), kept as it came.
- `controls1`: the first run of `controls` (7 of 7 pass). `mut/`: the controls under each mutation (`controls_table.txt`) and the analysis-level mutation logs on the dev view.
- `mutruns/`: the run-level mutations (float_cast, noise_f64, quad_h, eta_dropped).
- `view/`: symlinks that give the dev data the layout `analyze` reads (`runs/E`, `runs/F`, `runs/f64`, `runs/stall/D*`); `analyze --thin` reads the thinned series.
