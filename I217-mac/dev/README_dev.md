# I217-mac: design-stage development runs of the black-universe evolution (#217)

Machine: the coordinator's Mac (Apple M5, macOS, shared), negative-mass-mac-i217, worktree `~/Source/negative-mass-i217`, branch
`wip/i217-black-universe-evolution`. Issue: https://github.com/nmoinvaz/negative-mass/issues/217 ("Evolve a black universe along its growing mode: is
it a critical solution?"). Python `~/Source/negative-mass/.venv/bin/python` (numpy 2.5.4, scipy 1.18.1, sympy 1.14.0, mpmath 1.3.0, numba 0.68.1), nice 10,
one thread (`NUMBA_NUM_THREADS=1`, `VECLIB_MAXIMUM_THREADS=1`).

Status: **design stage, after the coordinator's rulings; diagnosis of rulings 4 and 5 done and reported, waiting for a ruling on its result.** Nothing here is a run of record, and no criterion
has been declared. The criteria are written here in step 2 (`notes/black_universe/evolution_design.md`, Sec. 12).

## dev/

Every log is kept, including failed and superseded ones. Reruns carry a new number. Scripts are in the repository, `notes/black_universe/`:
`evolve_derive.py` (sympy), `evolve_dev_runs.py` and `evolve_dev_runs2.py` (the prototype's runs; prototype `evolve_dev.py`, potential `evolve_potential.py`),
`evolve_master1d.py` (the linear master equation in the time domain).

| log | what | result |
|---|---|---|
| `dev_01` to `dev_06` (`dev_0N_derive_*.log`) | `evolve_derive.py` and its five mutations | 6 of 6 pass; each mutation fires exactly its declared checks |
| `dev_07_bitid.log` | prototype kernel against `dn.evolve` at c = 0, potential flag off and on | max abs difference 0 |
| `dev_08_static.log` | static members c = 0, -0.3, -1.5, -1 against the exact solution, h = 0.04, 0.02, 0.01 | second order |
| `dev_09_rates.log` | growth rate of the gauge-invariant Y_inv from the truncation seed against #212's W | c = -0.3, -1.5, -1.01, -0.99 agree to 0.5 to 2 %; c = -1 grows at 0.632 to 0.637 |
| `dev_10_pulse.log` | one-sided pulse scans with the raw finders | three kinds of fate at c = -1.5 |
| `dev_11_timing.log` | full-run times at N = 2000 to 16000 | 0.42 s to 21.4 s |
| `dev_12` to `dev_29` | mode family bisections with an extraction from a pulse run at t >= 14 (c = -0.3 was nonlinear there: the corner node differed from the static member by 0.7). `dev_12` to `dev_19` also had a fit() sign slip (series lines right, fit lines "failed"); `dev_15` and `dev_23` failed their brackets | superseded by `dev_40` to `dev_49`; kept |
| `dev_30_master1d_c*.log` | `evolve_master1d.py`: #212's master equation in the time domain, c = -2 ... -1 | W to four digits at five members; c = -1 decays |
| `dev_31_data0.log` | c = 0 rays against `dn.ellis_rays` | r 1.7e-9, phi 5e-13, f 0 |
| `dev_40` to `dev_49` | mode family from the untuned member's own departure at abs(Y) = 2e-3 (linear), bisection, series, fits; `dev_47` failed its bracket | c = -0.3: slope = 1/W to 1.1e-5 at h = 0.005; c = -1: slope = 1/kappa to 4e-4 at h = 0.01; c = -1.5: floor |
| `dev_50`, `dev_51` | near-threshold outcomes with raw and weighted finders, c = -0.3 and -1.5 | both outcomes at c = -0.3; collapse on one side at c = -1.5 |
| `dev_52_pulseE.log` | c = -1.5, pulse on the + ray: the expansion boundary and the sign change of Y | two boundaries, 2.5e-4 apart at h = 0.02 |
| `dev_53_profile.log` | profile of Y from the truncation seed, c = -1, -1.01, -1.5 | c = -1 equals c = -1.01 to 5 % |
| `dev_54_derive_record.log` | `evolve_derive.py`, the output committed in the repository | 6 of 6 |
| `dev_60_tuned_m15_h01.log` | the mode family at the tuned amplitude (|Y| = 3e-3 departure), local rate of Y on the diagonal; the script stopped at its sixth amplitude (log of a non-positive |Y|), after five were printed | rate 0.489, 0.492, 0.467 (= W), then a stall at |Y| = 1.5e-3 and growth at 2.7 |
| `dev_61` to `dev_68` | departure thresholds 2e-5 (extraction 2e-4), 2e-6, 2e-7 at h = 0.01, c = -1.5, -1, -0.3 | c = -1.5: A* -7.04e-7 and a floor 100 times lower; below 2e-6 the data transient decides (`dev_64`, `dev_68`) |
| `dev_70` to `dev_75` | horizon-regular gauge (`evolve_dev_reg.py`): tortoise and Kruskal x- with separate steps, c = -1.01, -1.5, -1 | the growth at c = -1 is the same in both gauges (0.6334, 0.6357) |
| `dev_76_constr.log` | constraint violation of the growing solution, c = -1, -1.01, -1.5, -0.3 | stays at truncation level |
| `dev_77_resp_*`, `dev_78_resp2_*` | response of Y to a compact pulse, odd part in +-Ap; Ap = 1e-3 (nonlinear by t = 12) and 1e-5, 1e-6 | linear in Ap; c = -1 and -1.01 grow then saturate at 7.7e3 Ap |
| `dev_80` to `dev_88` | linear-level mode family (departure 2e-5, extraction 2e-4) at h = 0.02, 0.01, 0.005, c = -0.3, -1.5, -1 | A* second order; slopes 1/W (1/kappa) to 6.5e-5, 9.9e-4, 7.7e-4 at h = 0.005 |
| `run_dev_mode.sh`, `run_dev_mode2.sh`, `run_dev_mode3.sh`, `run_dev_misc.sh`, `run_dev_lin.sh`, `run_dev_lin2.sh` | the launch scripts of the batches | |

Each `dev_NN_*.err` holds `/usr/bin/time -l` output (and a traceback for the failed one).
