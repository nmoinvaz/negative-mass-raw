# I7-mac: conv_085_l2 run on the Mac as a cross-machine check of win2's crashes

Machine: the Mac (Apple M5), run by negative-mass-coordinator. Issue: https://github.com/nmoinvaz/negative-mass/issues/7

win2 had several access violations in #7's ω = 0.85 jobs (I7-win2). This reruns one of them on another machine with
the same numpy 2.5.4 and scipy 1.18.1 (choptuik-large-d's .venv, used read-only), single-threaded, at nice 10.

Code: `git archive 731cac8 phase2` (branch `wip/i7-phantom-scans`), run from `phase2/nonradial`:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
      nice -n 10 python -X faulthandler -u convergence.py 2 0.85

- `conv_085_l2.log`: the run, 17:31:30–17:48:21 UTC, exit 0, every γ to 300.
- `conv_085_l2_importfail.log`: a first attempt that exported only phase2/nonradial and failed on `import boson_star`.
