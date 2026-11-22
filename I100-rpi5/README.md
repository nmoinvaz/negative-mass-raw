# I100-rpi5: logs and timings of the boundary term of item 6's identity against E - P.xi_0 (#100)

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/100

## Code and environment

Code: worktree `~/Source/negative-mass-i100` on branch `wip/i100-boundary`, started at main 29e395d. The script is the new
`notes/warp/weitzenbock_boundary.py`, with its stdout stored as `notes/warp/weitzenbock_boundary_output.txt`. It writes no
file of `weitzenbock_conf.py`, which it loads read-only (its argv hidden) for `note_gammas`, `inner`, `re`, `Geo`, `constraints`,
`christoffel` and `sym_K`.

Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0). Every run is `nice -n 10` with `OMP_NUM_THREADS=1`, one
process at a time, and any run longer than a few minutes is a systemd user unit `nm-i100-<step>` that writes its exit code to
`done/<step>.rc`. `memwatch.sh` only reports load, free memory and the rss of this task's python processes to
`memwatch.log`. Memory is never a stop condition. Nothing of choptuik-large-d is touched.

## What is computed

Data on psi^4 delta in #87's frame e_i = psi^-2 d_i, as polynomials in n_i and s = 1/r with independent symbolic coefficients:
psi = 1 + (m/2) s + psi_2(n) s^2 + psi_3(n) s^3 with psi_2, psi_3 angular; K_ij (frame) = psi^-6 Khat_ij with Khat the
Bowen-York form of momentum P plus a symmetric s^3 term; eps = eps_0 + eps_1(n) s + eps_2(n) s^2 with eps_0 a constant spinor
and eps_1 a polynomial in n_i with independent coefficients. The flux (1/4 pi) lim of the integral of psi^4 V^a n_a r^2 dOmega
with #87's V is the s^0 coefficient of its expansion, integrated over the sphere by exact monomial moments. E and P are the
ADM surface integrals of the same data, with the same machinery but a separate code path from V's.

## Steps

| step | what | log | stop condition |
|---|---|---|---|
| 2 | planted cases first: derivative and sphere-moment checks, flux formula, Schwarzschild (E = m, boundary term m), a dipole in psi, Bowen-York P | `step2.log` | none |
| 3 | the general boundary term against E - P.xi_0, the eps_1 terms, the pointwise identity on the data at exact points | `step3.log` | any single sphere integral not finished in 4 h wall: stop it and report what finished |
| 4 | every mutation `--mutate=NAME`, each must exit 1 and fire on its targets | `mutate_<name>.log`, `step4.time` | none |
| 5 | `python notes/warp/weitzenbock_boundary.py > notes/warp/weitzenbock_boundary_output.txt`, must exit 0 | `final.log` | none |

The pass criteria and the controls' target lists are in the script (`CONTROLS`) and are committed before step 4 starts.

## Results

(filled in as the steps finish)
