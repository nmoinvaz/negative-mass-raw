# I253-rpi5: the settled black-hole mass of the one-sided family G (D = 4), #41's apparent-horizon chain

Machine rpi5-ubuntu (Raspberry Pi 5, 4 cores, 8 GB, aarch64), Python 3.14.10, numpy 2.5.4, scipy, numba 0.68.1, one thread per process, `nice -n 10`, at most 3 processes, runs longer than a few
minutes as systemd user units `nm-i253-*`.
Issue https://github.com/nmoinvaz/negative-mass/issues/253 ("The settled black-hole mass of the one-sided family G (#41's chain, #225's member)"). Worktree `negative-mass-i253`, branch
`wip/i253-g-settled-mass`, from main at 0d1d376. Code: `notes/wormhole_evolution/settled_mass_g.py`, a thin driver that imports #41's `settled_mass.py`, #40's `threshold.py` and #39's `dn.py`
unchanged. This README is written before any chain run of family G (the first commit of this folder); the mutation targets are added in a second commit after the development runs, and nothing
above them is changed after that. Status words as in AGENTS.md: every mass here is *numerical evidence*. No sentence claims novelty.

## Question and plan

Family S (the symmetric ghost pulse) at D = 4 settles at M_AH = 0.22308 a (r_AH = 0.4462 a), to e^{−f} = 1.57e6 on the horizon (#41). Family G of #40 (a ghost pulse A = p*ₕ − δ plus a fixed
normal pulse B = 0.1 on the same ray, one-sided) does not start at the static wormhole; its near-critical state is the static member r_th = 1.0028 a, γ₁ = 0.048 (#225, `throat_locus.md`).
This issue runs #41's chain for G at the three h of #40, on the collapse side, and compares the settled mass with S's, with the error bar named. A settled mass of G different from S's by more
than that bar would not be a property of the static member alone.

## Declared parameters (all of #41's chain unchanged; none is changed after a development run without a ruling)

| quantity | value |
|---|---|
| dimension, family | D = 4 (n = 2), family G of #40 (`threshold.family("G", A)`: ghost pulse A on field 0 and normal pulse B = 0.1 on field 1, both on the + ray, centre 3, width 0.5, one-sided), 8πG = 1, a = 1 |
| h | 0.02, 0.01, 0.005 (the three of #40 for G at D = 4; #40 has no G run at 0.0025) |
| p*ₕ | `(lo + hi)/2` of #40's `D4_G_h{0.02,0.01,0.005}/summary.json` (negative-mass-raw `I40-dh610`), not bisected again; the h of each job.log is `'0.02'`, `'0.01'`, `'0.005'` and equals the h passed here. Hashes in `runs/pstar_G_h*.json` |
| δ | 1e-6 and 1e-8, A = p*ₕ − δ (collapse side); the expansion side p*ₕ + δ must expand. At δ = 1e-8 the amplitude is bit for bit #40's stall run (`stall_e` = 8) |
| chain | F₁ = 1.5, K = 20; level 1 is W₁ = 2.4 wide in x⁻, each box Nc = 2W₁/h cells (240, 480, 960), width h/2^k at level k; first trapped cell of #40 (r₊, r₋ < −1e-2), r_cut = 0.05 |
| **declared limit** | **e^{−f} on the horizon ≤ F_max = F₁ 2^K = 1 572 864**, as #41 |
| rectangle | X = 28 for the fate (#40's G at D = 4); rows: first trapped row + 3 + Nc h/4; columns: first trapped column + 12 (#41's dm = 3, dxp = 12) |

Not run, and why: the anisotropic zoom-free control AN of #41 (it needs a second p* bisection on a different grid for G; the zoom and interpolation code it tests is S's, covered here by PL1,
PL2, PL3 and by the first law RC4); h = 0.0025 (no #40 p*ₕ for G, a bisection of about 4 h in #40); a re-bisection of p*ₕ (the fates at p*ₕ ∓ 1e-10 on this machine, RC1, and at ∓ δ, RC2, decide
whether #40's value serves; #41 found rpi5 and dh610 p*ₕ agree to 5e-14).

## The driver (what it adds to #41's code)

- `run_real_g`: #41's `run_real` for family G (`threshold.family`, `threshold.point` with the G rectangle) and the same `settled_mass.chain`.
- `track_g`: wraps `settled_mass.track` (called unchanged) and adds the normal field's φ₊ on the horizon (`phip1`) and a recomputation of the ghost's (`phip0_re`, for the control TRK).
  `settled_mass.track` is replaced by the wrapper in `settled_mass`'s namespace at import; PL1 and PL2 are run with and without it and must print the same lines.
- The first law and the horizon flux carry both fields: dM/dx⁺ = (r²/2) e^f r₋ (φ₀₊² − φ₁₊²) on r₊ = 0 (the ghost with the sign of #41's `flux_integral`, the normal field with the opposite energy sign).
- `window_scatter` and the noise runs (below).

## Checks, bars, and the mutations that must fire

The bars are #41's, copied, with the same band for the order [1.5, 2.5]. A failed check is reported as not met.

| id | check | bar |
|---|---|---|
| CFG | `settled_mass.CRIT` (F₁, K, W₁, r_cut, tol, dxp, dm) and X of G equal the values above | equal |
| PL1 | #41's planted Schwarzschild (M = 0.3, stretching gauge, four h) through this driver | the five printed lines (four h and the verdict) equal #41's `settled_mass_output.txt` character for character, and equal those of `settled_mass.track` without the wrapper |
| PL2 | #41's planted Roberts ghost solution (moving contour, two forced zoom levels) through this driver | the same, five lines |
| PL3 | #41's level-0 identity (S, h = 0.02, δ = 1e-6, raw I41-rpi5's p*ₕ) through this driver | the printed line equals #41's (nodes and dead flags bit-identical, events (385, 385)) |
| PL3G | the same for G: level 0 of the chain (no zoom) against `dn.evolve` (h = 0.02, δ = 1e-6) | nodes, dead flags and first trapped cell equal |
| TRK | the wrapper's recomputed φ₊ of field 0 equals `settled_mass.track`'s on every column of every G series; φ₊ of the normal field is nonzero | relative 1e-12 |
| RC1 | #40's p*ₕ of G: hi − lo; on this machine fate(p*ₕ − 1e-10) = collapse and fate(p*ₕ + 1e-10) = expansion | hi − lo ≤ 1e-14, fates as stated, all three h |
| RC2 | fates at p*ₕ ∓ δ (all h, both δ); the first trapped cell and its time at δ = 1e-8 against #40's `stall.json` | collapse and expansion; cell equal; \|T − T₄₀\| ≤ √2 h |
| RC3 | M_AH at the first trapped cell against #40's M_hor at p*ₕ − 1e-8 | ≤ 2e-3 |
| RC4 | first law on the horizon, both fields, from the first trapped cell to e^{−f} = 20 | relative ≤ 2e-2 |
| RC5 | every run ends at the declared limit (status "limit", F_max/2 ≤ F_end < F_max), ≥ Nc/8 cells from the box edges, no gaps | all six |
| RC6 | second order of M_AH(x⁺): max \|M_h − M_h/2\| over the windows of x⁺ − x⁺_f [0, 1.5], [1.5, 3], [3, end] (the last reaches the limit), cubic splines, both δ, h = 0.02, 0.01, 0.005 | observed order in [1.5, 2.5] |
| RC7 | the settled value does not depend on δ | plateau means over the last 1.0 of x⁺ at δ = 1e-6, 1e-8 differ by ≤ 1e-4, every h |
| RC8 | M_AH has settled at the limit | plateau mean over the last 1.0 differs from the previous 1.0 by ≤ 1e-4, and the mean horizon flux (both fields) over the last 0.5 is ≤ 1e-5, every run |
| CMPT | the comparison function on planted offsets | an offset of half the planted bar is "equal", three times the bar "differs" |
| RN0 | ulp-noise run with noise 0 | bit-identical series to the run of record (same h, δ = 1e-8) |
| RNR | the noise runs respond: scatter at 64 × 2⁻⁵² is ≥ 3 × the scatter at 2⁻⁵², every window and h | as stated |

The acceptance of the issue is RC5, RC6 (M_AH(t) second order at three h up to the limit), PL1 to PL3 (planted cases unchanged), and the comparison below. RC1 to RC4, TRK, PL3G are the controls under it.

## The comparison with S (declared before the runs; reported, not a pass/fail check)

- **G's settled value** M_G := the plateau mean of M_AH over the last 1.0 of x⁺ (#41's `settled_summary` `plat1`), h = 0.005, δ = 1e-8. S's, M_S, is the same quantity from `I41-rpi5/runs/h0.005_d1e-08`
  (0.223085) with the same function; #41's quoted 0.2231 is given too. A Richardson value (second order, three h) and G − S at each h are reported.
- **Error bar of M_G, three kinds kept separate, summed linearly:**
  - h: |plat(h = 0.01) − plat(h = 0.005)| (the finest pair; the range over the three h is also printed);
  - δ: |plat(δ = 1e-6) − plat(δ = 1e-8)| at h = 0.005;
  - machine to machine: 2e-5, the difference #41's review (negative-mass-raw `I41-mac-review`) found for the same code on another machine (0.223109 against 0.223125 at the end of the run of h = 0.01, δ = 1e-6).
- **Verdict:** "G equals S" iff |M_G − M_S| ≤ the bar; otherwise G's settled mass "differs" from S's by that amount and is not a property of the static member alone.
- What an error bar is: the h and δ terms are differences between runs of this code (the resolution and the dependence on the distance from threshold); the machine term is a measured reproducibility of
  one run, not a bound. None is a rigorous enclosure.

## Roundoff floor (the question put to this task by #226)

#226 found that the null constraint stops converging where roundoff, amplified by (r₀/r)^{n−1}, passes truncation. Whether M_AH(t) reaches such a floor is measured here, not assumed.

- **Runs.** h = 0.01 and 0.005, δ = 1e-8, the same job with relative noise ξ·u on every node but the corner of both rays (ξ uniform in (−1, 1); r and the fields scaled by 1 + uξ, f shifted by uξ;
  `numpy.random.default_rng(seed)`): u = 0 (seed 1), u = 2⁻⁵² (seeds 1, 2, 3), u = 64 × 2⁻⁵² (seed 1). Ten runs.
- **Report (no bar).** max |M_noisy − M| over the three windows of RC6, for u = 2⁻⁵² (max over seeds) and 64 × 2⁻⁵², against E12 (h = 0.02 against 0.01) and E23 (0.01 against 0.005) of RC6 at δ = 1e-8.
  The ratio scatter(2⁻⁵²)/E at the finer h of the pair is read as: ≥ 1 "floor reached", 0.1 to 1 "approached", < 0.1 "not reached".
- **What it is.** An estimator of the sensitivity of M_AH(t) to ulp-sized perturbations of the data; the evolution adds its own roundoff on top. It is not the floor itself. Controls RN0 and RNR.
- #41's review gives a second number for the same thing: 1.6e-5 at the end of the series of h = 0.01 (δ = 1e-6) between two machines.

## Mutations (predictions written now; targets computed in the development runs are added in the second commit)

| mutation | what it breaks | predicted |
|---|---|---|
| `mass_exponent` | M = r^n/2 | PL1, RC3, RC4 |
| `finder_sign` | the finder looks for the − to + crossing of r₊ | PL1, PL2, TRK?, RC2 to RC8 |
| `hm_swap` | the kernel uses h₊ for h₋ | PL1, PL2, RC4 to RC8, others unknown |
| `interp_shift` | left-ray cubic at 1/4 of a cell | PL1, PL2, RC6 to RC8, others unknown |
| `flux_sign` | sign of the first-law integrand | RC4 |
| `normal_drop` | the normal field's flux omitted in RC4 and RC8 | RC4 if the normal flux is ≥ 2 % of ΔM, else silent |
| `normal_sign` | the normal field's flux with the ghost's sign | RC4 if the normal flux matters, else silent |
| `time_unit` | t = x⁺ + x⁻ | RC2 |
| `no_zoom` | K = 0 | PL1, RC5 to RC8, others unknown |
| `short_limit` | K = 12 (F_max = 6144) | RC5, RC8 |
| `pstar_off` | p*ₕ + 2e-8, collapse side lost at δ = 1e-8 | RC2 to RC8 |
| `pstar_shift` | #40's p*ₕ + 3e-10 in RC1 | RC1 |
| `theta_coef` | #39's sphere-term coefficient | everything |
| `rcut_off` | the chain's r_cut × 1.5 | PL3, PL3G |
| `col_shift` | x⁺ of a record at the left edge of the cell | PL2, RC6 |
| `delta_swap` | the δ = 1e-6 runs replaced by a δ chosen from the development scan | RC7 |
| `family_B` | the normal pulse B = 0.11 | RC1, RC2 |
| `crit_dm` | `settled_mass.CRIT["dm"]` = 2 | CFG |
| `trk_shift` | the wrapper recomputes φ₊ one row off | TRK |
| `noise_inert` | the noise injection skipped in the jobs | RNR (only if the jobs are rerun under it; see targets) |
| `rn_ref` | the noise runs compared with the δ = 1e-6 series | RN0, RNR |
| `cmp_bar0` | the comparison bar set to 0 | CMPT |

## Development runs so far

- `dev/planted_dev1.log`: `settled_mass_g.py planted` (PL1, PL2, PL3 through the driver, PL3G, TRK): 5 checks, 0 failed, 46 s. PL1 and PL2 lines are equal to #41's, with and without the wrapper.
  G at h = 0.02, δ = 1e-6: first trapped cell (398, 436); level 0 equals `dn.evolve`.
- `runs/pstar_G_h*.json`: p*ₕ read from #40's raw: 0.014945763570900113, 0.014877359967478583, 0.014860254854126537 (h = 0.02, 0.01, 0.005); hi − lo 5.7e-15 each.

---
# Second commit: development results, changes made during development, and the declared mutation targets (before the runs of record)

Nothing above this line is changed. The development jobs and analyses are in `dev/` (jobs `dev/runs/`, `dev/analyze_dev1.log` to `dev/analyze_dev3.log`, scans, dose runs, 20 + 3 mutated analyses in
`dev/mut/`). The jobs of the runs of record repeat the development jobs (same code, same inputs) and must reproduce them.

## What the development runs showed (not changed afterwards)

- The chain runs for G at the declared parameters, nothing changed: all six runs end at the limit (F_end 1.54e6 to 1.57e6), the horizon at least Nc/8 cells from the box edges. Jobs 2 to 29 s, peak rss 0.73 GB.
- 17 of 19 checks pass in development (`dev/analyze_dev3.log`); **RC7 and RNR fail and stay declared as written, reported as not met**.
  - RC7: the plateau at δ = 1e-6 and 1e-8 differs by 5.9e-4, 5.7e-4, 5.7e-4 (h = 0.02, 0.01, 0.005), bar 1e-4. The difference is the same at the three h, so it is not truncation. The supplementary scan
    (`dev/scan_G_h*.log`) shows G's plateau still rising by 3.5e-4 to 6.0e-4 per decade of δ from 1e-7 to 1e-12 (S's is flat to 1e-3).
  - RNR: scatter at 64 × 2⁻⁵² is 0.5 to 1.4 times that at 2⁻⁵². The injected noise is not what sets the scatter (exploratory dose scan: flat at 6e-6 in the last window from 2⁻⁵² to 2⁻⁴⁰, then growing
    with the noise: 5.5e-4 at 2⁻³², 4.2e-2 at 2⁻²⁴, 2⁻²⁴ ≈ 6e-8; the run at 2⁻¹⁶ ends with an empty series, logs kept). So the noise runs measure the scatter between roundoff realizations, not a calibrated response.
- RC4: the normal field's term is below 1e-5 of ΔM, so RC4 cannot test it (mutations `normal_drop`, `normal_sign` were silent in RC4). A planted check FLX was added (below).
- The comparison (reported, not a check): G's plateau at h = 0.005, δ = 1e-8 is 0.235548, S's 0.223085, difference +1.25e-2 against a bar of 6.0e-4 (h 1.05e-5, δ 5.66e-4, machine 2e-5).

## Changes made during development (all before the runs of record)

- **RNR** now also requires the scatter at 2⁻⁵² to be nonzero (the first form passed vacuously if both scatters were 0).
- **FLX added**: the first-law integrand on planted series with known integrals (ghost only −0.025, normal only +0.025, equal fluxes 0). Mutations `flux_sign`, `normal_drop`, `normal_sign` fire it.
- The scan's δ list extends to 1e-12 (13 values, 1e-12 to 1e-1), at h = 0.01 and 0.005; the dose runs (2^k × 2⁻⁵², k = 6, 12, 20, 28, 36, seeds 1, 2, h = 0.005) and the first law over the whole series are reports.
- The mutation `delta_swap` is dropped: RC7 fails without any mutation, so no mutation can make it fire. `noise_inert` is not an analysis mutation: the job with `--mutate=noise_inert --noise=64` gave a series bit-identical
  to the run of record (`dev/mut_noise_inert_job.log`), so the injection is what makes the noise runs differ.
- `dev/runs/` holds the runs of the first development analysis; no parameter of the chain, bar or limit was changed.
- Baseline failures: RC7 and RNR fail in the analysis of record, so they are in every target set of a mutation whose analysis completes. A mutation whose runs fail (`finder_sign`, `pstar_off`, `theta_coef`,
  `family_B`) reports the checks after the failed runs as failed and skips CMPT and the noise checks.

## Mutations: fired in development = declared (the runs of record must give the same sets)

| mutation | predicted (above) | fired in development = declared |
|---|---|---|
| `mass_exponent` | PL1, RC3, RC4 | PL1, RC3, RC4, RN0 (+ baseline RC7, RNR) |
| `finder_sign` | PL1, PL2, TRK?, RC2 to RC8 | PL1, PL2, RC2 to RC8, TRK |
| `hm_swap` | PL1, PL2, RC4 to RC8, others unknown | PL1, PL2, RC4, RC5, RC6, RC7, RC8, RN0, RNR |
| `interp_shift` | PL1, PL2, RC6 to RC8, others unknown | PL1, PL2, RC6, RC7, RC8, RN0, RNR |
| `flux_sign` | RC4 | RC4, FLX (+ baseline) |
| `normal_drop` | RC4 if the normal flux is ≥ 2 % of ΔM, else silent | **silent in RC4**; FLX only (+ baseline) |
| `normal_sign` | RC4 if the normal flux matters, else silent | **silent in RC4**; FLX only (+ baseline) |
| `time_unit` | RC2 | RC2 (+ baseline) |
| `no_zoom` | PL1, RC5 to RC8, others unknown | PL1, RC5, RC6, RC7, RC8, RN0, RNR |
| `short_limit` | RC5, RC8 | RC5, RC8, RN0 (+ baseline) |
| `pstar_off` | RC2 to RC8 | RC2 to RC8, TRK |
| `pstar_shift` | RC1 | RC1 (+ baseline) |
| `theta_coef` | everything | PL1, PL2, PL3, PL3G, RC1 to RC8, TRK |
| `rcut_off` | PL3, PL3G | PL3, PL3G (+ baseline) |
| `col_shift` | PL2, RC6 | PL2, RC6, RN0 (+ baseline) |
| `family_B` | RC1, RC2 | PL3G, RC1 to RC8, TRK |
| `crit_dm` | CFG | CFG (+ baseline) |
| `trk_shift` | TRK | TRK (+ baseline) |
| `rn_ref` | RN0, RNR | RN0 (+ baseline) |
| `cmp_bar0` | CMPT | CMPT (+ baseline) |

The exact sets are the `MUTATIONS` dictionary of `settled_mass_g.py` at the commit named in the runs of record. Mispredicted targets: `normal_drop` and `normal_sign` (silent in RC4, covered by FLX), `family_B` (also PL3G, RC3 to RC8 and
TRK, because the whole run changes), `col_shift`, `hm_swap`, `short_limit` (RN0 also fires: the stored noise-0 run is from the unmutated code), `rn_ref` (RNR is a baseline failure).
