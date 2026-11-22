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

Code commits on `wip/i100-boundary` of nmoinvaz/negative-mass: dd91e9a (the first draft, step 2 ran on 6f2d7c2's predecessor 5f002b2 for step 3),
746ed46 (the checks and the controls' target lists, frozen before the first control run), d74edc7 (the `eps-O1` control on
lighter data) and 3d15e19 (the final script).

| step | command (args to `weitzenbock_boundary.py`) | commit | exit | wall | peak rss | result |
|---|---|---|---|---|---|---|
| 2 | `--no-controls --only=clifford,dagger,planted_derivation,planted_sphere,omega_vs_conf,div_formula,planted_E,planted_B_schwarzschild,planted_dipole,planted_P,planted_BY` | dd91e9a | 0 | 10 s | 70 MiB | 11 checks pass |
| 3 | `--no-controls --only=bdy_vs_adm,bdy_vs_adm_T,no_divergence,limit_exists,eps1_drops,free_symbols,identity_points,flip_consistent` | 5f002b2 | 0 | 9 min 24 s | 302 MiB | 8 checks pass |
| 3b | the same plus `eps1_hand,aligned_eps0` | 6f2d7c2 | 0 | 10 min 31 s | 305 MiB | 10 checks pass (the general-data series alone 420 s) |
| 4 | `--mutate=NAME` for 17 controls, `step4.sh`, `mutations.txt`, one `mutate_NAME.log` each | 746ed46 | all 1 | 71 min, longest 1310 s (`Dhalf`) | not timed per run | 17 FIRED, 0 SILENT |
| 4 (`eps-O1`, first try) | `--mutate=eps-O1` with every symbol group and the O(1) term | 746ed46 | stopped | 2 h 14 min | 1.2 GiB | flux series not finished, stopped by the runner for run time, not memory (`mutate_eps-O1.stopped`) |
| 4b | `--mutate=eps-O1` on lighter data (Bowen-York K, eps = eps_0 + eta(n)), the target list unchanged | d74edc7 | 1 | 8 min 9 s | 268 MiB | FIRED |

The controls, each of which must fail its target list and exit 1 (the target lists were committed before the first run and not
changed; `failed` is the set of checks that failed, and only a control's targets run under it):

| control | verdict | failed | wall |
|---|---|---|---|
| `gamma` | FIRED | ['clifford', 'identity_points'] | 42 s |
| `no-conj` | FIRED | ['dagger', 'identity_points'] | 40 s |
| `deriv` | FIRED | ['planted_derivation', 'planted_E', 'planted_B_schwarzschild'] | 2 s |
| `sphere` | FIRED | ['planted_sphere', 'planted_P', 'planted_BY'] | 5 s |
| `omega-sign` | FIRED | ['omega_vs_conf', 'planted_B_schwarzschild', 'identity_points'] | 42 s |
| `weight` | FIRED | ['div_formula', 'planted_B_schwarzschild', 'identity_points'] | 42 s |
| `Vsign` | FIRED | ['planted_BY', 'aligned_eps0', 'bdy_vs_adm', 'bdy_vs_adm_T', 'identity_points', 'flip_consistent'] | 568 s |
| `sign` | FIRED | ['planted_BY', 'aligned_eps0', 'bdy_vs_adm', 'bdy_vs_adm_T', 'identity_points'] | 551 s |
| `Jsign` | FIRED | ['identity_points'] | 41 s |
| `Kdiv` | FIRED | ['planted_BY', 'aligned_eps0', 'bdy_vs_adm', 'bdy_vs_adm_T', 'identity_points', 'flip_consistent'] | 280 s |
| `Vspin` | FIRED | ['planted_B_schwarzschild', 'planted_dipole', 'bdy_vs_adm', 'eps1_drops', 'eps1_hand', 'free_symbols', 'identity_points'] | 611 s |
| `Dhalf` | FIRED | ['planted_B_schwarzschild', 'planted_dipole', 'bdy_vs_adm', 'eps1_drops', 'eps1_hand', 'free_symbols', 'identity_points'] | 1310 s |
| `trace` | FIRED | ['bdy_vs_adm_T', 'identity_points'] | 54 s |
| `adm-E` | FIRED | ['planted_E', 'planted_dipole', 'bdy_vs_adm'] | 499 s |
| `adm-P-sign` | FIRED | ['planted_P', 'bdy_vs_adm', 'bdy_vs_adm_T'] | 507 s |
| `adm-frame` | FIRED | ['planted_P'] | 5 s |
| `adm-trace` | FIRED | ['bdy_vs_adm_T'] | 12 s |
| `eps-O1` | FIRED | ['no_divergence', 'limit_exists'] | 8 min 9 s (step 4b) |

`memwatch.log` has the load and free memory once a minute (report only, nothing stopped).
