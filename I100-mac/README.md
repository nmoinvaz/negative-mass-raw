# I100-mac: coordinator's review of #100 (rerun and independent numerical check)

Machine: the coordinator's MacBook Air M5. Issue: https://github.com/nmoinvaz/negative-mass/issues/100

- `rerun.txt`: stdout of `python notes/warp/weitzenbock_boundary.py` from `wip/i100-boundary` at fd55c4e (Python
  3.14.7, sympy 1.14.0, nice 10, one thread), exit 0: 21 checks pass and all 18 controls fire. With timings and the
  Python version masked it equals the committed `weitzenbock_boundary_output.txt`. `rerun.time`: `/usr/bin/time -l`,
  1343.07 s wall, 556744704 bytes (531 MiB) maximum resident.
- `mut_Vsign.txt`: `--mutate=Vsign` alone, exit 1, fails its six targets (`planted_BY`, `aligned_eps0`, `bdy_vs_adm`,
  `bdy_vs_adm_T`, `identity_points`, `flip_consistent`), 141 s.
- `ind100.py`: an independent check of the boundary term (1/4 pi) lim oint psi^4 V^a n_a R^2 dOmega against
  E |eps_0|^2 - P.xi_0, for explicit data with fixed numbers (m = 0.7, P = (0.3, -0.5, 0.4), psi with dipole and r^-3
  terms, K = psi^-6 (Bowen-York + r^-3 terms), eps = eps_0 + eps_1(n)/r + eps_2(n)/r^2). omega from the Koszul formula;
  float64 sphere quadrature (48 x 96) at R = 100 * 2^k and R = 150 * 2^k, k = 0..5, and an exact fit in 1/R for the
  limit. Shares no code with weitzenbock_boundary.py, weitzenbock_conf.py or conventions.py. Criteria in its
  docstring, fixed before the first run.
  - `ind100_run1.txt`: PASS, every criterion within 1e-14, 2 s.
  - `ind100_mut_{Vsign,Dhalf,omega}.txt`: each exits 1 on its required criteria.
