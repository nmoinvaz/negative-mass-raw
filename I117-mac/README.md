# I117-mac: coordinator's review of #117 (rerun, re-solve and independent check)

Machine: the coordinator's MacBook Air M5. Issue: https://github.com/nmoinvaz/negative-mass/issues/117

- `collect_rerun.txt`: `python collect_i117.py <I117-rpi5>` from `phase2/nonradial` of `wip/i117-boxes` at 8878495 (exit 0;
  identical to `i117_boxes_output.txt`). `collect_rerun_noplant.txt`: the same with `--mutate=noplant` (exit 1).
- `z_b25_l2.log`, `w_b25_l2.log`: the two `b25_l2` jobs of `jobs.txt` rerun by `resolve.sh` from an empty cache
  (`cache/winding2_cache_*`, `cache/zerilli_zeros_cache_*`), nice 10, one thread. Both exit 0, with the same counts as
  rpi5. The 195 points of D agree with rpi5's cache to 2.6e-10 relative (median 6.2e-12).
- `ind117.py`: an independent counter for `b25_l2` on the full rectangle (no doubling). It shares only
  `background.solve_star` and `PolarProblem.D` with the scripts under test. Its criteria are in its docstring, fixed
  before the first run. `ind117_run1.txt` is the first run (exit 0, PASS); `ind117_mut_reverse.txt` and
  `ind117_mut_noplant.txt` are its mutations (each exits 1). `cache/ind117_cache.pkl` holds its 530 points.
