# I226-rpi5: why the null-constraint maximum stops falling at the finest h (D = 5, 6): development runs, criteria, runs of record

Machine: rpi5-ubuntu (Raspberry Pi 5, 4 cores, 8 GB, aarch64, Ubuntu), Python 3.14.10, numba 0.68.1, numpy longdouble = IEEE binary128.
Issue: https://github.com/nmoinvaz/negative-mass/issues/226 (milestone G7). Code: negative-mass branch `wip/i226-constraint-plateau`,
`notes/wormhole_evolution/constraint_plateau.py` (uses `dn.py`, `checks.py`, `threshold.py` unchanged). Runner: negative-mass-rpi5-i226.
At most 3 processes at nice 10, one thread each; a run longer than 2 h is stopped (`timeout 7200`).

This README was written after the development runs below and before the first run of record. Nothing in "Declared" is changed after a run of record.

## Question

#40 measured max |C₊₊|, |C₋₋| over the event cell's past along the two runs that bracket p*ₕ. It falls by 4 per halving at D = 4 and at the first
halving at D = 5, 6, and stops falling at the finest h (D = 5: 1.4 to 1.6, h = 0.00177; D = 6: 0.4 to 0.6, h = 0.00125). The issue asks: on the
unperturbed static wormhole is the ratio 4 over a fixed region, where is the maximum, and if the plateau is not truncation, which candidate sets it
(roundoff, the ray data's RK4 solve, a single cell, the corner)?

## Development runs (before the declaration)

Scripts `dev/scripts/`, logs `dev/logs/`, data `dev/data/`. Row engine = `dn.row_step`. Diagonal engine = `dn.cell_np` swept along anti-diagonals.

1. **The streamed constraint equals `dn.constraints`** (`val1.py`, then K0): prefix maxima over regions of a static, a pulse and a G grid, difference 0.0.
2. **#40's numbers at the coarse h reproduce; its bracket runs do not.** (`repro40.py`, `repro_D5.log`, `repro_D6.log`.) At D = 6, h = 0.005 the two bracket
   runs give max |C₊₊| 7.7755e-05 and 7.7756e-05 against #40's 7.7753e-05, 7.7754e-05. The amplitudes lo and hi of #40 are 1e-14 apart; on this machine their
   events differ from #40's (D = 5, h = 0.00707, lo: expansion at cell 2076 against #40's collapse at 1822), as #40's note says the floor of p*ₕ is about 1e-12.
   Runs at p*ₕ ∓ 1e-8 are insensitive to this.
3. **Where the maximum is** (`prof.py`): in the near-critical runs max |C| per time bin is flat in t at the coarse h and grows with t at the finest h
   (D = 6, h = 0.00125: 2.9e-6 at t = 0.25, 4.6e-6 at 2.25, 7.2e-6 at 7.25, 1.8e-5 at 11.25, 2.8e-5 at 12.25), on the diagonal x⁺ = x⁻, near the throat.
4. **Static case** (`devA.py`, slab t ≤ 4): second-order ratios at the declared h (table below); the plateau appears only at an extension h.
5. **Noise** (`dose.py`, `devE.py`, `devF.py`): relative noise of amplitude a·2⁻⁵² added to every node. First added after the row sweep (`dose.py`); that is
   asymmetric (it does not feed the next node of the same row, C₋₋ barely responds), so the mutation is applied inside the diagonal sweep, to a node as it is computed.
6. **Binary128** (`quaddev.py`): the same sweep in 113-bit precision. D = 6, S at p* − 1e-8, slab t ≤ 8: max |C| 4.6e-6 flat over the slab at h = 0.00125
   (1.86e-5 at h = 0.0025: ratio 4.03), float64 9.9e-6.
7. **A noise model** (`model.py`, then the final `model_job`): the constraint satisfies ∂₋C₊₊ = −(n−1)(r₋/r)C₊₊ on the evolution equations (#40), so C r^{n−1} is
   constant along x⁻; roundoff d in a node of r is a step in the quadrant above it, whose second difference is the pair +d/h², −d/h² in C₊₊ at i−1, i on every later row.
   Summing independent uniform noise of amplitude a·2⁻⁵² r over the rows gives
   `rms C₊₊(i,j) = sqrt(2/3) a 2^-52 / h² · r(i,j)^-(n-1) · ( Σ_{j'<j} r(i,j')^{2n} )^{1/2}` (static r(l), l = (x⁺ − x⁻)/√2). Observed/model of the rms of the extra C
   on the diagonal t = 6, in |l| bands: natural roundoff (float64 − binary128) 0.71 to 1.14, injected a = 16: 0.93 to 1.14, a = 256: 0.91 to 1.14 (D = 5, 6; C₊₊ and C₋₋).
8. **Ray data** (`devB.py`): the RK4 solve of the data at its own step h/4, h/16 changes the finest-h slab maximum by ×0.87, ×0.98 (D = 6); the realization scatter is about 13 %.
   A planted relative bump of 1e-7 in r on the rays: ×27.5; 1e-9: ×0.96.
9. **One cell, the corner** (`devB.py`, `devE.py`): a planted spike of 1e-10 in one node of r persists as a pair along the later rows (slab maximum 3.7e-3, 2 nodes within a factor 2
   of it on the last diagonal); the natural runs have 120 and 103 (C₊₊, C₋₋). A spike at the node (2, 2) puts the maximum at x⁺ = 0.001, x⁻ = 0.003.
10. **Control mutations** (`dev/logs/control_mutations.log`): `cons_sign` fires K0 (difference 9.0), `diag_S` K1 (4.0e+02), `rk4_step` K2 (2.7e-09), `quad_h` K3 (−2.0e-02 against 2e-3).

Development numbers (max |C| over the slab; the last column is the ratio at the last halving):

| set (D) | h₁, h₂, h₃, extension h₄ | ratios h₁→h₂, h₂→h₃, h₃→h₄ |
|---|---|---|
| static, t ≤ 4 (5) | 4.578e-05, 1.140e-05, 2.896e-06, 9.342e-07 | 4.015, 3.937, 3.100 |
| static, t ≤ 4 (6) | 7.841e-05, 1.865e-05, 4.963e-06, 3.713e-06 | 4.204, 3.758, 1.337 |
| S p* − 1e-8, t ≤ 10 (5) | 4.618e-05, 1.165e-05, 3.464e-06 | 3.962, 3.364 |
| S p* + 1e-8, t ≤ 10 (5) | 4.606e-05, 1.159e-05, 3.498e-06 | 3.973, 3.314 |
| S p* − 1e-8, t ≤ 8 (6) | 7.776e-05, 1.909e-05, 9.883e-06 | 4.073, 1.932 |
| S p* + 1e-8, t ≤ 8 (6) | 7.776e-05, 1.905e-05, 8.392e-06 | 4.081, 2.270 |
| bracket lo, t ≤ 16 (5) | 4.606e-05, 1.183e-05, 6.251e-06 | 3.893, 1.892 |
| bracket hi, t ≤ 16 (5) | 4.606e-05, 1.181e-05, 6.456e-06 | 3.900, 1.829 |
| bracket lo, t ≤ 12 (6) | 7.776e-05, 2.192e-05, 2.055e-05 | 3.548, 1.066 |
| bracket hi, t ≤ 12 (6) | 7.776e-05, 2.101e-05, 2.066e-05 | 3.701, 1.017 |

The bracket rows are the amplitudes of #40; #40's own event-past maxima at the finest halving were 0.43 to 0.64 (D = 6) and 1.4 to 1.6 (D = 5).

## Declared

**h.** D = 5: 0.01/√2, 0.005/√2, 0.0025/√2 (= #40's three) and the extension 0.00125/√2 = 0.000884; D = 6: 0.005, 0.0025, 0.00125 and the extension 0.000625.
The criteria below use the three declared h (two halvings); the extension halving is reported, not gated. The extension needs its own p*ₕ (family S, bisected here to 2e-10; `pstar_table.json`).

**Regions.** The slab {nodes (i, j) of the rectangle [0, X]² with t = (i + j)h/√2 ≤ T_c}; the same nodes at every h (to the nearest cell). Chosen from the development runs as the
largest T_c below the first departure of the coarsest h (static) and below the first event of every run of the set (S, bracket); the fixed T_c is not changed.

| set | D = 5 | D = 6 | what runs |
|---|---|---|---|
| static (no pulse) | T_c = 4, X = 6 | T_c = 4, X = 6 | `ellis_rays(pulses=())` |
| S at p*ₕ ∓ 1e-8 | T_c = 10, X = 15 | T_c = 8, X = 12 | p*ₕ = (lo+hi)/2 of #40 (`I40-dh610/runs/D*_S_h*/summary.json`), extension: bisected here |
| bracket (#40's lo, hi) | T_c = 16, X = 18 | T_c = 12, X = 15 | the amplitudes lo, hi of #40 (fates depend on roundoff; the slab ends before every event seen) |

The static case cannot be run longer: its unstable mode, seeded by truncation error ∝ h², departs at t = 6.7, 7.5, 8.3 (D = 5) and 5.1, 5.7, 6.4 (D = 6) for the three h
(ln 4/W later per halving), so a fixed region after that time is not static at the coarse h. Family S at p*ₕ with the seed tuned away (the bracket set) is the nearest to a long static run.

**What is reported for every run:** the slab maximum, its node (i, j), x⁺, x⁻, t, the maximum per time bin of 0.5, ratios per halving, with the band of #39's order test:
a halving is "second order" if the ratio is in [2^1.75, 2^2.25] = [3.364, 4.757] (`CRIT` order_lo, order_hi).

**Checks** (`constraint_plateau.py analyze`; K0 to K3 in `controls`). "Gated" checks set the exit status; R2, R3 are measurements whose verdict is reported.

| id | statement (can fail) | gated |
|---|---|---|
| K0 | the streamed prefix maxima of C₊₊, C₋₋ equal `dn.constraints`' on three small grids (static, S, G), difference 0 | yes |
| K1 | the float64 diagonal sweep equals the numba row sweep bit for bit (bins, nodes, two diagonals) | yes |
| K2 | `ellis_rays_x` (float64, solve step = h) equals `dn.ellis_rays` bit for bit | yes |
| K3 | binary128 and float64 sweeps give the same slab maximum (relative difference < 2e-3) at D = 6, h = 0.005, static, t ≤ 4 | yes |
| R1 | static: ratios of the slab maximum at both halvings of the three declared h are second order, D = 5 and 6 | yes |
| R2 | S at p* ∓ 1e-8: the same ratios (reported, with the extension halving) | no |
| R3 | bracket lo, hi: the same | no |
| C1 | binary128: second-order ratios at both declared halvings in every set (static, S −, S +, bracket lo), D = 5 and 6 | yes |
| C2 | added roundoff: at the finest declared h (S −) a = 256 raises the slab maximum by ≥ 3 and at the coarsest a = 16 by ≤ 1.10; a = 1 and 16 are reported (a = 1 is inside the 13 % scatter) | yes |
| D1 | the data's RK4 solve at h/4 and h/16 leaves the finest-h slab maximum within [0.7, 1.4] of the baseline (S −) | yes |
| L1 | not a single cell: on the last diagonal of the slab at least 5 nodes lie within a factor 2 of the maximum (S −, bracket lo, finest declared h) | yes |
| L2 | not the corner: min(x⁺, x⁻) of the slab maximum ≥ 1 in every declared-h run of every set | yes |
| M1 | the model of development step 7: observed/model of the rms of the extra C₊₊, C₋₋ on the diagonal t = 6 (S −, D = 5, 6, h₂ and h₃), bands |l| < 0.25, 0.25 to 0.5, 0.5 to 1, 1 to 2, 2 to 3, 3 to 5 with ≥ 20 nodes, within [0.5, 2] for natural roundoff (a = 1), a = 16, a = 256 | yes |

**Predictions written before the runs of record:** R1 met; R2, R3 not met at the finest declared halving at D = 6 and at the extension halving at both D (at D = 5 the declared finest halving is 3.3 to 3.4, on
the edge of the band); C1 met (the plateau is removed in binary128); C2, D1, L1, L2, M1 met.

**Independence.** C1 shares the scheme and the constraint formulas with the double run (it changes only the precision, the data included); M1 shares none of the evolution (static r(l) from the dense Ellis solution
and the propagation law); D1, L1, L2 and the mutations share the evolution. An error bar here is the realization scatter of a maximum (about 13 %), not a fit error.

**Mutations** (each effect computed in the development runs above; `analyze --mutate=NAME` or `controls --mutate=NAME` must fire exactly the listed checks):

| mutation | what it changes | fires | computed effect |
|---|---|---|---|
| `cons_sign` | the sign of the scalar term in the streamed C | K0 | difference 9.0 |
| `diag_S` | the diagonal sweep reads S from the wrong diagonal | K1 | slice difference 4.0e+02 |
| `rk4_step` | K2's data built with two RK4 steps per grid step | K2 | difference 2.7e-09 |
| `quad_h` | binary128 constraint uses 1.01 h | K3 | −2.0e-02 against 2e-3 |
| `static_noise256` | R1 reads the static slabs with a = 256 noise | R1 | finest halving 0.662 (D = 5), 0.293 (D = 6) |
| `quad_as_double` | C1 reads the float64 runs as its binary128 runs | C1 | finest halving 1.93 (D = 6, S −), 2.27 (S +); 3.36, 3.31 (D = 5) |
| `noise_inert` | C2 reads the unperturbed run in place of the noisy ones | C2 | ×1.000 against 3 |
| `ray_pert` | D1 includes the run with a planted 1e-7 bump in the data | D1 | ×27.5 against [0.7, 1.4] |
| `spike` | L1 reads the run with a planted spike of 1e-10 | L1 | 2 nodes against 5 |
| `corner` | L2 reads the run with a spike at node (2, 2) | L2 | x⁺ = 0.001 against 1 |
| `model_exp` | M1's model with exponent n instead of n − 1 | M1 | the model is larger by r(i, j) (up to 4 in the bands |l| ≥ 3) |

`quad_as_double` at D = 5 does not fire C1 by the finest halving alone (3.364 is on the band edge); it fires through S +, 3.314, and static is unaffected. The effect for each is recomputed in the runs of record.

## Candidate causes and how each is tested

| candidate | test | result |
|---|---|---|
| roundoff | binary128 removes the plateau (C1); noise of known amplitude moves it in proportion (C2, M1); the natural plateau equals the model with a = 1 (M1) | runs of record |
| the ray data's RK4 solve | the solve at h/4, h/16 (D1), planted data violation as the control (`ray_pert`) | runs of record |
| a single cell | the number of nodes near the maximum (L1), planted spike as the control | runs of record |
| the corner | the location of the maximum (L2), planted corner spike as the control | runs of record |

## Runs of record

106 jobs (`jobs_wave1.txt`: 98 jobs with the three declared h, started 2026-11-27 11:05; `jobs_wave2.txt`: the 8 extension-h jobs, started 11:15), three workers at nice 10 with one thread each, wall 59 min (to 12:05), 8022 CPU s, longest job
1320 s (`sqm_D6_k3`); every job exit 0 (`done/*.rc`), none stopped by the 2 h limit; rss 140 to 150 MB per worker at the one reading (11:15), 6 GB available; no process of another project was touched. The extension p*ₕ are `pstar_ext/` (D = 5: 4.5051120e-06,
bracket 1.8e-10; D = 6: 1.7344915e-05, bracket 1.7e-10); `pstar_table.json` holds #40's three p*ₕ, the bracket amplitudes lo, hi and these. The script's `run` code is the commit 2179de2 of the code repository; its analysis part was changed afterwards
only to count the comparisons each check evaluated (a check with none found fails) and to print section P; the runs were not repeated.

`make_output.sh` writes `notes/wormhole_evolution/constraint_plateau_output.txt` from `runs/` (controls, analyze, every mutation).

| id | verdict | numbers |
|---|---|---|
| K0 to K3 | pass | difference 0.0 (K0), 0.0 (K1), 0.0 (K2), binary128 against float64 −1.2e-05 (K3) |
| R1 | pass | D = 5: 4.015, 3.937 (extension 3.100); D = 6: 4.204, 3.758 (extension 1.337) |
| R2 S −, S + | measurement, band not met at D = 6 and D = 5 S + | D = 5: 3.962, 3.364 (S −: on the edge, met), 3.973, 3.314; D = 6: 4.073, 1.932; 4.081, 2.270; extension halving 0.589, 0.822 (D = 5), 0.386, 0.315 (D = 6) |
| R3 bracket lo, hi | measurement, band not met | D = 5: 3.893, 1.892; 3.900, 1.829; D = 6: 3.547, 1.066; 3.701, 1.017 |
| C1 binary128 | pass | 4.0 to 4.2 at every declared halving in every set; extension halving 4.000, 4.003 |
| C2 added noise | pass | finest declared h, a = 256: ×57 (D = 5), ×113 (D = 6); coarsest, a = 16: ×1.005, ×1.001 |
| D1 ray data | pass | ×1.076, ×1.030 (D = 5), ×0.866, ×0.979 (D = 6) |
| L1 single cell | pass | at least 36 nodes within a factor 2 of the maximum |
| L2 corner | pass | min(x⁺, x⁻) of the maximum ≥ 2.72 |
| M1 noise model | pass | observed/model 0.71 to 1.14 (natural), 0.93 to 1.14 (a = 16), 0.91 to 1.14 (a = 256), 48 values each |

Mutations (`constraint_plateau_output.txt`), each fired exactly its declared check: `cons_sign` K0 (difference 9.0), `diag_S` K1 (4.0e+02), `rk4_step` K2 (2.7e-09), `quad_h` K3 (−2.0e-02), `static_noise256` R1 (finest halving 0.662, 0.293), `quad_as_double`
C1 (finest-halving float64 ratios 1.93, 2.27, 1.07 at D = 6), `noise_inert` C2 (×1.000), `ray_pert` D1 (×15.8, ×27.5), `spike` L1 (2 nodes), `corner` L2 (x⁺ = 0.002, 0.001), `model_exp` M1 (ratios up to 4.5). The effects equal the declared ones; the one
declaration the runs corrected is `quad_as_double` at D = 5, where the finest halving of S − (3.364) is on the band's edge and the mutation fires through the others.

`supplement/` (exploratory, written after the runs of record, not a declared check): `r_roundoff.py` and its logs. Roundoff error of r on the static diagonal t = 3.5: 1.4e-11 (D = 6, h = 0.00125), 4.2e-12 (D = 5, h = 0.00177), against the difference
from the exact static r(l) of 4.1e-4 and 6.4e-5; in family S at p* − 1e-8, t = 7, D = 6: 2.5e-08.

## Files

`README.md` (this), `jobs_wave1.txt`, `jobs_wave2.txt`, `launch_I226.sh` (queue worker, `launch_I226.sh LIST`), `make_output.sh`, `pstar_table.json`, `pstar_ext/` (the extension bisections and their points), `runs/` (one json per job, npz of the slices),
`logs/` (job logs), `done/` (exit codes), `queue.log`, `dev/` (development scripts, logs and data; the scripts are as run, with scratchpad paths), `supplement/`.
