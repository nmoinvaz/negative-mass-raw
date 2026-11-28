# I227-rpi5: binary128 bisection of the Ellis threshold (D = 4, family S, h = 0.02) and the roundoff seed on the stall (D = 4, 5, 6)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64; `np.longdouble` is IEEE binary128, 113-bit mantissa; `need_binary128` refuses other machines).
Issue: https://github.com/nmoinvaz/negative-mass/issues/227, with #226's added request. Coordinator: t2x. 3 processes at most, nice 10, one thread each.
Code: negative-mass `notes/wormhole_evolution/extended_bisect.py` on `wip/i227-extended-bisect`. It imports `dn.py`, `checks.py`, `threshold.py` and
`constraint_plateau.py` unchanged. Status words as in AGENTS.md: every result below is *numerical evidence*.

## Question

#40 found T(p) a log law down to |p − p*ₕ| ≈ 1e-11 and jitter below, with points on the wrong side at e ≥ 12. Is that floor the evolution's roundoff?
Method: the same discrete problem with every number in binary128, bisected to |p − p*ₕ| = 1e-24 and followed to 1e-20, and the float64 − binary128
difference of r on the stall as the roundoff seed.

## Method

- **Engine.** `sweep`: the anti-diagonal sweep of `dn.cell_np` in `np.longdouble` (≈ 5 µs per cell), with the events of `dn.evolve(stop=True)`
  (first trapped cell by row, diagonal anti-trapped cell with r ≥ 2, collapse wins a tie, trap tolerance 1e-2, excision r < 0.05, e^−f > 25). In float64 it is
  bit-identical to the numba row kernel (K1). T is the event cell's t as in `threshold.point`.
- **Data in binary128** (`rays_ld`): the same algorithm as `dn.ellis_rays` (RK4 constraint solve on each ray, pulse Gaussian centre 3 width 0.5, family S mirror), every
  number in binary128. Two variants of the static Ellis solution:
  - **E (exact)**: from a Taylor series in binary128 (`static_taylor`, order 18, closed form at D = 4 to 2e-32); √2 exact, h = the float64 number 0.02 widened.
  - **F (float64's own inputs)**: the static r(l), φ(l) from `dn.ellis_dense` (float64 DOP853, rtol 1e-13) cast to binary128, as the float64 run reads them. The two precisions then
    differ by arithmetic roundoff only. (#40's data differ from the exact wormhole by 5e-13 in φ and 6e-14 in r; K3.)
- **Bisection and series**: `threshold.bisect` and `threshold.fit_joint` unchanged, with binary128 amplitudes. Bracket [−0.01, 0.01] as #40, hi − lo ≤ 1e-24, p* = midpoint.
  Series p* ∓ 10^−e, e = 3, 3.5, …, 20 (35 values, 70 runs), `LDSink` stores the amplitudes as 34-digit strings.
- **Float64 side**: `f64` runs K = 16 bisections of `threshold.point` (numba, X = 34) from 16 different brackets (`bracket_k`; k = 0 is #40's, bit for bit
  4.7527725346299125e-05 .. 4.752772535539407e-05), tolerance 1e-16, so the roundoff realizations differ. `f64series` runs float64 at float64(p*ₑ ∓ 10^−e).
- **Stall** (`stall_runs`, `stall_profile`): at p = p*_F ∓ δ_k, δ_k = 1e-10 (1 + 0.0731 k), k = 0 … 7 (8 pairs), the float64 run (dn.ellis_rays, the numpy sweep) and the binary128 run
  (variant F data) of the same float64 amplitude to t = 17, 11, 8.5 at D = 4, 5, 6. On each node diagonal over |l| ≤ 4: d = r_f64 − r_b128, the pair's profile
  Q = ∂r/∂p = (r_b128(+) − r_b128(−))/(p₊ − p₋), and ε = ⟨d, Q⟩/⟨Q, Q⟩, the offset in p that the roundoff is equivalent to. A float64 run at p is the exact run at p + ε,
  so p*_f64 − p*_exact = −ε.

## Criteria (declared before the runs of record; every check is in `extended_bisect.py` and prints `[pass]` / `[FAIL]`; a failure is reported, not changed)

Windows in δ = |p − p*ₕ|; W from #195 (D = 4: 1/W = 0.846045); q = √2 h = 0.02828 the row spacing of T.

| id | check (can fail) | bar |
|---|---|---|
| K1 | the float64 anti-diagonal sweep equals the numba row kernel: fate, event cell, T, at 20 amplitudes (D = 4, 5, 6; near p*ₕ ∓ 1e-9) | 20 of 20 equal |
| K2 | binary128 static solution: closed form at D = 4, first integral r'² = 1 − r^−2(n−1) at D = 5, 6 | ≤ 1e-30 |
| K3 | binary128 data against the float64 data at A = p*ₕ, 1200 nodes: E differs by the dense solution's error, F by float64 roundoff; the '+' and '−' rays mirror exactly | E: r 3e-13, φ 2e-12; F: r 1e-13, φ 1e-14 |
| K4 | the binary128 sweep on the float64 data reproduces the float64 events at e = 3, 5, 7, 8 (both sides) | 8 of 8 equal |
| PL1 | a planted fate function with a known threshold (34 digits) and a log-law T on the row lattice, through `threshold.bisect`, the series and `fit_joint` | p* within 1e-24, every point on its side, T monotone, slope on [1e-20, 1e-12] within 3e-3 of 1/W |
| PL2 | a planted linear response p*(η) = p0 + 0.37 η through the perturbation analysis (κ from η = 1e-8, 1e-10, prediction at ±1e-16) | κ agree 1e-3, prediction 1e-4 |
| PL3 | a planted threshold floor of rms 3e-14 (a hash of p), 8 draws: the series check finds the first wrong-side point | first wrong e in [12.5, 15.5] in all 8 |
| BR | the bisection ends with hi − lo ≤ 1e-24 and every run an event (variants E and F) | 1e-24 |
| SR | the series is complete: e = 3 … 20 step 0.5, both sides | 70 points |
| FM | fate monotone: every series point p*ₕ ∓ 10^−e lands on its own side, e ≤ 20 | none wrong; the first failure e is reported |
| TM | T never decreases as δ falls, each side | none |
| EVC | every event within 5 cells of the diagonal (the column cap of the sweep, 40, does not bind) | max \|i − j\| ≤ 5 |
| LL1 | the slope of T against ln(1/δ) over [1e-20, 1e-12] (8 decades the double run could not reach) against 1/W | within 5e-3, and 1/W inside the fit spread (windows and sides, slope ± 2 SE, as #40) |
| LL2 | that slope against the slope over #40's window [1e-11, 1e-3] | within 5e-3 |
| LL3 | the log law over [1e-20, 1e-12]: largest residual of the fit | ≤ q |
| KF | float64 bisections from K ≥ 8 brackets, tolerance 1e-16 | K ≥ 8 |
| A2 | every float64 p*ₕ against the binary128 p*ₕ (E and F): the issue's "agrees with the double one to the double floor" | ≤ 1e-11 |
| A3 | variant F: the float64 offset is roundoff alone | rms ≤ 1e-13 |
| FS | the float64 series about the binary128 p* leaves its side at e = −log10(max offset) ± 1.5 | first wrong side within 1.5 |
| P1 | the data's pulse amplitude scaled by 1 + η, η = ±1e-16: p*(η) = p*/(1 + η) exactly, Δ = ∓4.75e-21 | \|measured − predicted\| ≤ 1.5e-24 (the bracket widths) |
| P2 | a relative bump η exp(−((s − 5)/0.5)²) in r on both rays: κ = Δp*/η from η = 1e-8 and 1e-10 predicts Δp* at ±1e-16 | κ agree 1e-3, prediction 1e-4 |
| S0 | the pair's profile Q grows at W over W t ∈ [10, 17] (D = 4, 5, 6) | within 2 % |
| S1 | rms of r_float64 − r_binary128 over \|l\| ≤ 4 on the stall grows at W over W t ∈ [10, 17] (#226's request) | within 2 % |
| S2 | the floor in p* predicted from the seed (rms of ε over the stall draws) against the rms of the float64 bisections' offsets from the binary128 p* (D = 4; D = 5, 6 when wave 3 runs) | ratio in [1/3, 3] |
| S3 | the mean of −ε against the mean offset | same sign, ratio in [1/3, 3] |

Planted truth first: K1–K4 and PL1–PL3 pass before any run of record. The planted perturbation of the data at 1e-16 relative is P1 (exact prediction) and P2 (prediction from the linear response measured at 1e-8 and 1e-10, which float64 can also resolve).

## Development runs (`dev/`, before the criteria were declared)

Variants E and F bisected from the narrow bracket [4.7527e-05, 4.7528e-05] to 1e-24 (55 runs, 12.5 min each, one process), thinned series e = 3, 6, 9, 11, 12, 13, 14, 15, 16, 18, 20,
8 float64 bisections (k = 0 … 7), three stall pairs per D, the perturbation runs, the mutations. What they set (the bars above were fixed from them; none was moved after):

- **p*ₕ** (D = 4, S, h = 0.02): E 4.75277252764230752630e-05; F 4.75277253411064544586e-05; float64 (#40, k = 0, bit for bit) 4.7527725350847e-05. Float64 − F: mean +1.58e-14, sd 3.0e-15 (K = 8, tolerance 1e-17);
  float64 − E: mean +8.04e-14. So the double-precision p*ₕ is 1.6e-14 (roundoff) above the binary128 p*ₕ of its own inputs, and the dense static solution's error (rtol 1e-13) moves p*ₕ by 6.5e-14.
- **Series**: every point on its own side to e = 20, T increases by 1.9516 per decade between e = 18 and 20, both sides (1/W · ln 10 = 1.9482), slope over [1e-20, 1e-12] 0.845829 (−2.6e-4 against 1/W), residuals
  inside the row lattice (rms 0.0083 = q/√12). The float64 series at the same amplitudes differs from binary128 in its event from e = 12 and leaves its side at e = 14.
- **Stall**: ε settles to a constant after W t ≈ 9 (the roundoff is carried by the unstable mode: after projection on Q the residual falls to 0.00); rms ε 2.05e-14 (D = 4), 1.3e-13 (D = 5), 9.4e-13 (D = 6);
  the difference grows at W to −0.04 %, +0.04 %, +0.6 % (W t in [10, 17]); Q itself grows at W to 2e-5, 1.2e-3, 1.3e-2 (the last is the discrete rate at h = 0.005, #40's coarsest D = 6 member). The window is therefore W t in [10, 17], not an earlier one (W t in [6, 12] gave −3 %, +1 %, −1 %).
- **Perturbations**: P1 measured −4.7522e-21 against −4.7528e-21 (difference 6.1e-25); P2 κ = −0.215729 at η = 1e-8 and 1e-10 (agree to 1.1e-7) and the shift at ±1e-16 matches to 1.1e-8, 2.4e-8.
  The first try at the bump (bracket p* ± 1e-10) and the first try at −1e-16 (± 1e-17) did not straddle and are kept in `dev/pert/*_failed_*`; the bar on P2 was tightened from 1e-2, 1e-3 to 1e-3, 1e-4 after them (the measurement cannot resolve better than about 1e-7).
- **Floor returns with injected noise**: `--mutate=noise_f64` adds uniform relative noise 2⁻⁵² to every node of the binary128 evolution: its p* moves by +3.2e-14 and the series has 6 wrong-side points from e = 15, T not monotone, slope 0.20.
  That is the causal test that the floor is the evolution's roundoff (reported in the note, with the declared effect below).

## Mutations (`--mutate=NAME`), effects computed in the development runs before they were declared

Analysis-level and controls-level effects are in `dev/mut/analysis_table.txt`, `dev/mut/controls_table.txt`; run-level in `dev/mut/runlevel_table.txt`. The runs of record repeat them in `mut/`.

| mutation | what it breaks | checks that fire (computed) |
|---|---|---|
| `diag_S` | the sweep takes S from the wrong diagonal | K1 |
| `taylor_order` | the static Taylor series at order 8 | K2 |
| `ellis_charge` (dn's) | the float64 data's charge × 1.1 | K3 |
| `quad_h` | the step of the binary128 sweep × 1.01 | K4 (and the run fails: T = 1.09 at every amplitude, "bracket does not straddle", the JOB mutation of #40) |
| `float_cast` | the amplitude passes through float64 inside the binary128 run | PL1 (planted p* off by the float grid, 3e-21); P1-scaleP16 on the real run |
| `pert_sign` | the predicted shift's sign | PL2, P1-scaleP16, P2 |
| `floor_off` | the planted floor removed | PL3 |
| `time_unit` (threshold's) | T × √2 in the fits | LL1, LL3 (both variants) |
| `pstar_off` | p* shifted by 1e-18 in the analysis | FM, LL1, LL2, LL3 (both variants), P1-scaleP16, P2 |
| `bisect_loose` | the bisection stopped at 1e-14 | BR, FM, TM, LL1, LL2, LL3 (both variants), P1-scaleP16, P2 |
| `drop_point` | one series point dropped | SR (both) |
| `evc_shift` | event cells shifted by 10 | EVC (both) |
| `offsets_scaled` | the float64 offsets × 1e-4 | FS (both), S2-D4, S3-D4 |
| `drop_k` | 4 of the 8 float64 brackets kept | KF |
| `t_unit` | stall time × √2 | S0, S1 at D = 4, 5, 6 |
| `seed_scale` | the predicted seed × 10 | S2-D4, S3-D4 |
| `noise_f64` | noise 2⁻⁵² on every node of the binary128 evolution | FM, TM, LL1, LL2, LL3 (run level) |
| `h_wrong` | the whole problem at 1.01 h (p* +2.0 %) | A2-E (run level) |
| `eta_dropped` | the amplitude perturbation not applied to the data | P1-scaleP16 (run level) |

The clean analysis fires nothing. The run-level mutations read through `scripts/mut_runs_table.py` (views of the mutated run in place of the unmutated one, `analyze --only=`).

## Plan of the runs of record

Code: the commit named in `commit.txt` of this folder (written when the first job starts). Threads: 3 processes at most, nice 10, queue `scripts/launch_I227.sh` with the lists from `scripts/make_lists.py`.

| wave | jobs | CPU estimate |
|---|---|---|
| 1 | E and F bisections (bracket [−0.01, 0.01], 1e-24), 16 float64 bisections, `controls` | 25 + 25 + 6 + 8 min |
| 2 | E and F series (e = 3 … 20, each side its own job), float64 series, the six perturbation bisections, the stall at D = 4, 5, 6 (8 pairs) | 4 × 8 + 2 + 6 × 9 + 15 min |
| 3 | the floors at D = 5, 6: variant F bisections (±3e-11 round #40's p*, tolerance 1e-16) and 8 float64 bisections each | 2 × 15 + 25 min |
| mut | the run-level mutations (`scripts/run_mut_runs.sh`, two lanes), the analysis-level and controls tables | 60 min |

Stop conditions: a run of more than 2 h of wall time is stopped (none is expected: 12 to 50 s per binary128 run at D = 4); memory is reported, never a stop condition.
If a check fails in a run of record it is reported with its numbers, the criteria stay as declared.
