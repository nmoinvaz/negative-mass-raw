# I7-mac: #7's ω = 0.85 jobs that crashed on win2, run on the Mac

Machine: the Mac (Apple M5), run by negative-mass-coordinator. Issue: https://github.com/nmoinvaz/negative-mass/issues/7

win2 had six access violations in #7's ω = 0.85 jobs (I7-win2), leaving `scan_085_l2` and the γ = 1000 row of
`conv_085_l3` unfinished. These are the same jobs on another machine, with the same numpy 2.5.4 and scipy 1.18.1
(choptuik-large-d's .venv, used read-only), BLAS threads at 1, at nice 10, with `-X faulthandler`.

Code: `git archive 731cac8 phase2` (branch `wip/i7-phantom-scans`, merged as 5bd77a1), run from `phase2/nonradial`:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
      nice -n 10 python -X faulthandler -u convergence.py 2 0.85        # conv_085_l2.log
    ... convergence.py 3 0.85                                           # conv_085_l3.log
    TAG=_n100 ... scan_growing.py -1 0.85 2 100 1e-3 300                # scan_085_l2.log, scan_eps-1_w0.85_l2_n100.csv

- `conv_085_l2.log`: 17:31–17:48 UTC, exit 0, every γ to 300.
- `conv_085_l3.log`: 18:09–19:10 UTC, exit 0, every γ to 1000.
- `scan_085_l2.log`, `scan_eps-1_w0.85_l2_n100.csv`: 19:10–19:39 UTC, exit 0, 0 sign changes.
- `cmp_scan_diag.py`, `cmp_scan_diag.log`: the CSV against win2's serial `I7-win2/diag_085_l2.jsonl` at all 100 points,
  pass if every relative difference is ≤ 1e-8, with a self-test that scales one D by 1 + 1e-7 and must fire. From this
  folder: `python3 cmp_scan_diag.py scan_eps-1_w0.85_l2_n100.csv ../I7-win2/diag_085_l2.jsonl --selftest`.
- `conv_085_l2_importfail.log`: a first attempt that exported only phase2/nonradial and failed on `import boson_star`.
- `cmp_conv_logs.py`: the rows of two `convergence.py` logs digit for digit (timings dropped), exit 1 if the row counts
  or any row differ, with a self-test that changes one digit of D_base and must fire. For #55, from this folder:
  `python3 cmp_conv_logs.py conv_085_l3.log ../I55-win2/conv_085_l3.log --selftest`.
