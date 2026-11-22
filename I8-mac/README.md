# I8-mac: coordinator's review of #8 (rerun and independent re-derivation)

Machine: the coordinator's MacBook Air M5. Issue: https://github.com/nmoinvaz/negative-mass/issues/8

- `derive.log`: `python derive_nonradial.py` from `phase2/nonradial` of `wip/i8-polar-exact` at f42f9b9 (47 s, exit 0).
- `sym.log`: `python verify_polar_exact.py --method=symbolic` (exit 0, every residual exactly zero, 1 s);
  `sym_mut_bg_u.log`: the same with `--mutate=bg:u` (exit 1, detected).
- `matter_sv_m1_2.log`: `python matter_sv.py -1 0.7603 2`. It is identical to the runner's output except max sv3/sv1,
  7.1e-17 here against 6.1e-17 there.
- `ind8.py`: an independent check. It linearizes G_ab - 8 pi eps T_ab for the polar ansatz itself, solves its own
  background equations, and tests (tt) and the angular trace on y' = J y exactly at 6 random rational points (l = 2, 3;
  eps = +1, -1). It shares only `polar_matrix_generated.J_and_h` with the scripts under test. Its criteria are in its
  docstring, fixed before the first run.
  - `ind8_run1.txt`: failed at every point by a harness bug, because the perturbation values were not substituted.
  - `ind8_run2.txt`: after that fix, PASS.
  - `ind8_mut_{coef,eps,nojp}.txt`: each exits 1.
