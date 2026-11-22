# I99-mac: coordinator's review of #99 (rerun and independent exact check)

Machine: the coordinator's MacBook Air M5. Issue: https://github.com/nmoinvaz/negative-mass/issues/99

- `rerun.txt`: `python notes/warp/weitzenbock_conf.py` from `wip/i99-diag` at cef6d1a, with stdout and stderr merged
  (exit 0, 2 min 36 s). Its stdout equals the committed `weitzenbock_conf_output.txt` apart from the Python version.
  The per-check timing lines are on stderr. `mut_Jsign.txt`: `--mutate=Jsign` (exit 1, 8 checks fail, among them
  `identity_diag_general`).
- `ind99.py`: an independent check of item 6's identity on diag(A^2, B^2, C^2) with e_i = d_i/A_i, in exact arithmetic
  at random rational points, for explicit random polynomial A, B, C, K_ij and eps. It has its own Christoffel symbols,
  Ricci scalar, spin connection, covariant divergence and spinor algebra, and shares no code with
  `weitzenbock_conf.py` or `conventions.py`. Its criteria are in its docstring, fixed before the first run.
  - `ind99_run1.txt`: stopped with a TypeError before any criterion was evaluated.
  - `ind99_run2.txt`: after that fix, PASS at 8 points (flat with K = 0, diagonal with K = 0, general).
  - `ind99_mut_{Jsign,sign,omega}.txt`: each exits 1.
