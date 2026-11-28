# I324-dh610: departure-time lifetime of family G on the throat locus, pairs at p*ₕ ∓ 1e-12 at D = 4, 5, 6

Machine: dh610-fedora (Fedora, shared with choptuik-large-d's runners; at most 4 threads, nice 10, transient systemd units `nm-i324-<name>`).
Issue: https://github.com/nmoinvaz/negative-mass/issues/324 (task #324, "Define G's lifetime on the throat locus by the mode's departure time at D = 4, 5, 6").
Script: `notes/wormhole_evolution/departure_lifetime.py` on branch `wip/i324-departure-lifetime` of nmoinvaz/negative-mass (imports `dn`, `threshold`, `throat_locus`, `throat_drift`, `g_d6`
unchanged). Status words as in AGENTS.md; every number is *numerical evidence*.

Layout: `dev/` development runs (`pairs/`, `plx/`, `mut/`, logs of the pilot and of the development analyses), `runs/` the runs of record (`pairs/`, `plx/`, `analysis/`, `mut/`),
`scripts/run_unit.sh` (the launcher: a transient unit, one thread, nice 10, 2 h limit, `<name>.{log,err,rc,time,start}`; it refuses to overwrite a log, a rerun takes a new name).
Raw folders `I225-dh610`, `I228-dh610`, `I255-dh610` are read-only inputs.

## Part 1: method and criteria (written before the runs of record)

### The definition

A *pair* is the two runs of G (ghost pulse A tuned, normal pulse B = 0.1 on the same ray) at A = p*ₕ ∓ δ, kept as the locus series of #225 (slice t = const, minimum of r, its proper time
τ; no grid is stored). `mean r` of the pair is the tuned throat's radius r_th(τ); `odd = (r₊ − r₋)/2` is the unstable mode; `u = odd/δ` is its response per unit δ.
By linearity the run at p*ₕ + d deviates from the tuned throat by d·u(τ). The **departure time** τ_dep(d) is the first τ at which that deviation reaches

- REL: ε r_th(τ) (the issue's definition; ε = 0.03, 0.1 (primary), 0.3), that is ln(u/r_th) = ln ε + e ln 10 with d = 10⁻ᵉ;
- ABS: ε in units of a (what #228's `PH` lines compute although its text says "of r_th"), that is ln u = ln ε + e ln 10.

Exact identity (checked by IDN): dτ_dep/dln(1/δ) = 1/(λ − ṙ_th/r_th) for REL and 1/λ for ABS, with λ = d ln u/dτ. REL therefore differs from the mode's e-fold by the growth of r_th itself.

Readings are on a grid e = 3, 3.5, …, 11; windows are [a, a + 2] for a = 3, 4, …, 9 (two decades each). Per window: the end-point slope (τ_dep(a + 2) − τ_dep(a))/(2 ln 10) (primary; the
OLS slope over the grid is reported), the reference r_th(τ_dep)/W as the window mean over the grid (trapezoid in e; the value at the middle is reported), W of #195.
The growth branch starts at t = 4 (the pulse has left; below that |odd| is roundoff) and ends at the first slice where ln u stops rising.

### Pairs, δ and the splice

| D | h of the runs of record | pair A (stored, read-only) | pair X (stored) | pair B (new) | tcap of B |
|---|---|---|---|---|---|
| 4 | 0.01, 0.005 (0.02 coarse) | 1e-9, #225 `I225-dh610/runs/stall` | 1e-10, #255 `I255-dh610/runs/stall` (h = 0.02, 0.01 only) | 1e-12 | 28 |
| 5 | 0.00354, 0.00177 (0.00707 coarse) | 1e-9, #225 | 1e-10, #255 | 1e-12 | 26 |
| 6 | 0.0025, 0.00125 (0.005 coarse, dev only) | 1e-9, #228 `I228-dh610/runs/stall` | 1e-10, #228 `I228-dh610/runs/stall_drift` | 1e-12 | 30 |

p*ₕ is #40's (the merged record `I228-dh610/runs40`), bit for bit (PST). The development record uses the two coarsest h of each D (D = 6: 0.005 with a new pair A at 1e-9, and 0.0025);
the runs of record use the two finest. Development and record files are separate runs of the same job.

Found in the pilot: roundoff in the first time units shifts a pair's effective amplitude by a constant n (u → u(1 + n/δ)): the stored pairs at 1e-9 and 1e-10 differ in u by a constant
1e-4 (D = 4), 1e-3 to 3e-3 (D = 5, 6), and the pair at 1e-12 by 1 % (D = 4) to 9 and 44 % (D = 6, h = 0.005, 0.0025). The pair's own nonlinearity is (u_A/(c u_B) − 1) = 2.05 ρ² (D = 4),
4.3 ρ² (D = 5), 7.4 ρ² (D = 6) with ρ = |odd|/r_th. So: the 1e-9 pair reads to e ≈ 8.5 (ρ ≤ 0.04); a pair at 1e-12 reaches e = 11 but carries the shift. The reading therefore **splices**
two pairs by linearity: u from pair A up to the slice where |odd_A|/r_th = 1e-4, and from pair B beyond it, B scaled by c = median(u_A/u_B) over the slices with |odd_A|/r_th in [1e-5, 3e-3] (both
pairs linear, the shift constant); r_th and τ come from the same pair as u. The linear gate: a reading is used only where its pair's |odd|/r_th ≤ 0.04 (nonlinearity ≤ 1.2 % at D = 6, a shift of τ_dep by ≤ 0.012).
The pair X is not part of the splice; it is an independent δ for XPAIR.

### Checks (ids; each can fail; none is changed after data)

Gated; D-specific checks are evaluated for each D (suffix 4, 5, 6) at the finest h of the record unless stated.

| id | statement | bar |
|---|---|---|
| CTL | the reader in #228's rule (pair A alone, ABS, mask of rising ln\|odd\|) reproduces every printed number of #228's `PH` lines at ε = 0.1, both h | 98 numbers at the printed digits |
| PLR | planted synthetic pairs with the response u ∝ exp ∫W/r_th dτ, r_th = 1.2 + ṙ τ (ṙ = 0.09 and 0), roundoff shifts −3e-4 (A) and +30 % (B), nonlinearity 7ρ², through splice and reader: REL window slopes against the exact closed form; ABS window slopes against the window mean of r_th/W (the rate W/r_th recovered) | 5e-3 |
| PLX | #225's planted drifting throat (family S, static throat drifting at v = 0.1, 0.5 in the grid by the pair rescaling; D = 4; p*ₕ bisected to 1e-13 on the locus's fate; h = 0.02, 0.01) through the same reader (pair at 1e-9 alone): the e-fold 1/W in τ in every window | 5e-3 |
| LBL | each pair's label δ is half the amplitude difference in its files and its centre is p*ₕ | 1e-6 |
| PST | pairs A and B are centred on #40's p*ₕ | bit for bit |
| CAL(D) | u_A/u_B is constant over the calibration window (p1 to p99 spread) and \|c − 1\| is a fraction of δ_B (not a mislabelled δ) | 2e-3; 0.5 |
| XPAIR(D) | the stored pair X (1e-10) alone, gated, gives the spliced τ_dep(e) (ε = 0.1, REL) at every common e | ≥ 8 readings, max \|Δτ\| ≤ 0.02 |
| IDN | the window slope equals the mean over the window of 1/(d ln(u/r_th)/dτ) (REL; ABS 1/(d ln u/dτ)) at the departures, from the series' own derivative | 2e-3 |
| RA(D) | window slopes at the two finest h agree (ε = 0.1, REL and ABS) | 5e-3 |
| **MAIN(D)** | REL: dτ_dep/dln(1/δ) in each window of two decades equals r_th(τ_dep)/W (ε = 0.1) | **2 %**, ≥ 5 windows |
| MAINa(D) | the same with ABS (#228's rule) | 2 %, ≥ 5 windows |
| **D4** | D = 4: the OLS slope of τ_dep over e = 3 to 11 (the window of #225's fits), ε = 0.1, REL, against #225's 0.8495 | **0.5 %** |
| EPSr(D) | ε = 0.03, 0.1, 0.3 agree on the raw slope in each window of e (REL), as the issue states it | 2 %, ≥ 5 windows |
| EPSn(D) | ε = 0.03, 0.1, 0.3 agree on the slope in units of r_th(τ_dep)/W (REL) in each window | 2 %, ≥ 5 windows |

Not gated (reported): the slope against the model r_th/(W − ṙ); ṙ at the departures; the OLS slope; the reference at the middle of a window; the slope read in t; the nonlinearity coefficient and the
times at which |odd|/r_th reaches 1e-5, 0.01 and 0.04 for each pair (where the pair stops being linear); the comparison with #228's `PH` table.

What an error bar is, here: the **resolution** difference (RA, two finest h); the **choice of ε** (EPS); the **calibration** (CAL, XPAIR: the constant c, an independent δ); the **linear gate**
(≤ 1.2 % in u at ρ = 0.04, a shift of ≤ 0.012 in τ_dep that changes a window slope by ≤ 0.3 %). There is no statistical error: the pairs are deterministic.

### What was known before the runs of record (no criterion was moved for it)

- #228's `PH` lines (ABS, pair A alone, e ≤ 9) and the pilot: at D = 6 the REL slopes are +3.4 to +5.6 % above r_th/W in the windows e = 3–5 … 6–8 and the ABS slopes −1.1 to +1.8 % (+2.0 % at
  7–9 in the dev record). MAIN6 (REL, the issue's definition) is therefore expected to fail and MAINa6 to sit at its bar; both are gated and reported.
- At D = 6 the raw slope's ε-dependence (EPSr6) is expected to fail (the departure at larger ε is later, where r_th has grown; #228's `PH` lines show 12 % between ε = 0.03 and 0.3 in the window
  e = 3–5 in ABS). EPSn is the form of the statement that can hold. Both are gated.
- #228's text says the departure is "the deviation reaches ε = 0.1 of r_th" while its code compares |odd| with ε δ₀/δ (ε in units of a). Reported as a discrepancy.

### Choices made in the development runs (sized the bars, before the declaration)

- δ_B = 1e-11 at D = 5, 6 was tried first and replaced by 1e-12 at every D so that e = 11 is readable (the calibration absorbs the shift).
- The calibration window was ρ ∈ [1e-6, 3e-3] and became [1e-5, 3e-3]: at D = 6 the shift of the 1e-12 pair is not constant before t ≈ 9. The spread is p1 to p99 (one slice has a 5e-3 glitch).
- CAL's spread bar 1e-3 became 2e-3 (D = 6, h = 0.0025: 1.0e-3 with c = 1.44; a 1e-3 error in c moves τ_dep by 1e-3). PLR's bar 2e-3 became 5e-3 (the planted case with a 30 % shift on B reads 2.3e-3
  at the gate; the first planted case with 3 % read 1.6e-3). Both are declared here, before any run of record.
- The first launch of the two planted evolutions failed at once (a relative log directory in the launcher, no output); the launcher takes an absolute path since.

### Mutations (`--mutate=NAME`; the effect is computed in the development record and declared here; on the record each is recomputed and reported)

Each flips exactly the listed checks of the development record (`dev/mut/mutate_dev1.log`, `dev/mut/mutate_dev2.log`). Checks that already fail in a record cannot flip there (RA6 fails in the
development record, MAIN6, MAINa6, EPSr6 fail by construction).

| mutation | what it does | flips in the development record |
|---|---|---|
| `tau_t` | the reader takes t instead of the locus's proper time τ (the observer is the grid's time) | CTL, D4, IDN, MAIN4, MAIN5, MAINa4, MAINa5, PLX, RA6 |
| `eps_abs` | ε in units of a instead of r_th(τ) in the REL readings | IDN, PLR, RA6 |
| `rw_const` | r_th = 1 in the reference r_th/W | MAIN5, MAINa5 |
| `delta_label` | every pair's δ labelled 10 times too large | CTL, D4, LBL, RA6 |
| `gate_off` | the linear gate \|odd\|/r_th ≤ 0.04 removed | PLX, XPAIR4, XPAIR5, XPAIR6 |
| `cal_off` | the splice without the calibration constant c | EPSn5, EPSn6, EPSr5, IDN, MAINa5, PLR, RA5, XPAIR5, XPAIR6 |
| `w_scale` | W of #195 scaled by 1.01 | MAIN5, MAINa5, PLR, PLX |
| `ra_scale` | the finer h's slopes scaled by 1.01 | RA4, RA5 |
| `pstar_off` | p*ₕ shifted by 3e-9 in the check of the pairs' centre | PST |

(`RA6` flips from fail to pass under the three mutations that change the slopes because it fails by 5.1e-3 against 5e-3 in the development record, whose two h are 0.005 and 0.0025.)

## Part 2: runs of record (2026-11-28, dh610-fedora)

Script commits on `wip/i324-departure-lifetime`: 134cfe3 (criteria and mutations declared in Part 1), adb40b6 (note, outputs, figure). The pairs of record were run after Part 1 was pushed (raw 79cfa8b1).

- Pairs of record, `runs/pairs`: A and X are the stored pairs (read-only); B at 1e-12 for D = 4 (h = 0.02, 0.01, 0.005), D = 5 (h = 0.00707, 0.00354, 0.00177), D = 6 (h = 0.0025, 0.00125);
  tcap 28, 26, 30. The analysis uses the two finest h of each D. The longest run took 6.2 min wall (D = 6, h = 0.00125, one side per unit); none was near the 2 h stop. 4 units at most at a time.
- Planted evolutions, `runs/plx`: family S in the drifting coordinates of #225, v = 0.1, 0.5, h = 0.02, 0.01, p*ₕ bisected to 1e-13 on the locus's fate, then the pair at 1e-9.
- **Added after the pairs of record, reported and not gated** (a diagnosis of the two failures CAL6 and RA6): B2, a second new pair at 2e-12 (another roundoff realization), at D = 5 (h = 0.00354, 0.00177) and D = 6 (h = 0.0025,
  0.00125); the contamination κ of the new pair's mean radius; the lists of τ_dep; #225's level lifetimes in the same windows and their offset to τ_dep; the A-to-X shift. The gates were not changed.
- Analyses: `runs/analysis/analyze_record1` to `5` (28 checks, 23 pass, 5 fail: CAL6, RA6, MAIN6, MAINa6, EPSr6, rc 1; the same verdict on every check in all five; `analyze_record5` is the output of record, copied to
  `notes/wormhole_evolution/departure_lifetime_output.txt`). Mutations on the record: `runs/mut/mutate_record1` to `3` (`mutate_record3` is `departure_lifetime_mutate_output.txt`). Development: `dev/pilot_run2` (the pilot,
  rerun as a unit; its first run was in the foreground and is not kept), `dev/analyze_dev1` to `3`, `dev/mut/mutate_dev1`, `2`.
- Results are in `notes/wormhole_evolution/departure_lifetime.md`: MAIN6 (REL, the issue's definition) +3.4 … +5.6 % and MAINa6 (ABS) −1.1 … +2.2 % against the 2 % bar; D4 0.84924 against 0.8495; EPSr6 6.25 %;
  CAL6 |c − 1| = 0.527 against 0.5; RA6 1.3e-2 (window e = 9–11 only).
- The first launch of the planted evolutions (PLX, v = 0.1, 0.5) failed at once with no output (relative log directory in `run_unit.sh`); the launcher was fixed and the units rerun under the same names.

### Units

| unit `nm-i324-<name>` (log dir/name) | rc | wall | max RSS |
|---|---|---|---|
| `dev/analyze_dev3` | 0 | 0:01.09 | 112 MB |
| `dev/mut/mutate_dev1` | 0 | 0:04.18 | 112 MB |
| `dev/mut/mutate_dev2` | 0 | 0:05.72 | 112 MB |
| `dev/pairs/D4_h0.01_d1e-12` | 0 | 0:09.68 | 192 MB |
| `dev/pairs/D4_h0.02_d1e-12` | 0 | 0:04.71 | 188 MB |
| `dev/pairs/D5_h0.00354_d1e-12` | 0 | 0:59.71 | 202 MB |
| `dev/pairs/D5_h0.00707_d1e-11` | 0 | 0:18.06 | 193 MB |
| `dev/pairs/D5_h0.00707_d1e-12` | 0 | 0:16.82 | 194 MB |
| `dev/pairs/D6_h0.0025_d1e-12_s-1` | 0 | 1:21.66 | 204 MB |
| `dev/pairs/D6_h0.0025_d1e-12_s1` | 0 | 1:22.76 | 206 MB |
| `dev/pairs/D6_h0.005_d1e-09` | 0 | 0:39.94 | 196 MB |
| `dev/pairs/D6_h0.005_d1e-11` | 0 | 0:40.54 | 197 MB |
| `dev/pairs/D6_h0.005_d1e-12` | 0 | 0:40.59 | 200 MB |
| `dev/pilot_run2` | 0 | 0:00.64 | 110 MB |
| `dev/plx/plx_h0.01_v0.1` | 0 | 4:41.53 | 192 MB |
| `dev/plx/plx_h0.01_v0.5` | 0 | 4:11.64 | 194 MB |
| `dev/plx/plx_v0.1` | 0 | 1:20.09 | 204 MB |
| `dev/plx/plx_v0.5` | 0 | 1:19.43 | 207 MB |
| `runs/analysis/analyze_record1` | 0 | 0:01.51 | 120 MB |
| `runs/analysis/analyze_record2` | 0 | 0:01.08 | 123 MB |
| `runs/analysis/analyze_record3` | 1 | 0:01.05 | 124 MB |
| `runs/analysis/analyze_record4` | 1 | 0:01.06 | 124 MB |
| `runs/analysis/analyze_record5` | 1 | 0:01.12 | 124 MB |
| `runs/mut/mutate_record1` | 0 | 0:07.12 | 120 MB |
| `runs/mut/mutate_record2` | 0 | 0:06.85 | 125 MB |
| `runs/mut/mutate_record3` | 0 | 0:07.80 | 125 MB |
| `runs/pairs/D4_d1e-12_h0.02_0.01_0.005_D5_h0.00707` | 0 | 1:26.06 | 198 MB |
| `runs/pairs/D5_d2e-12_h0.00354_h0.00177` | 0 | 2:54.80 | 218 MB |
| `runs/pairs/D5_h0.00177_d1e-12` | 0 | 3:16.81 | 219 MB |
| `runs/pairs/D5_h0.00354_d1e-12` | 0 | 1:23.72 | 203 MB |
| `runs/pairs/D6_h0.00125_d1e-12_s-1` | 0 | 6:11.95 | 223 MB |
| `runs/pairs/D6_h0.00125_d1e-12_s1` | 0 | 6:05.92 | 227 MB |
| `runs/pairs/D6_h0.00125_d2e-12_s-1` | 0 | 3:15.77 | 222 MB |
| `runs/pairs/D6_h0.00125_d2e-12_s1` | 0 | 3:10.81 | 227 MB |
| `runs/pairs/D6_h0.0025_d1e-12` | 0 | 3:08.03 | 213 MB |
| `runs/pairs/D6_h0.0025_d2e-12` | 0 | 1:37.25 | 210 MB |
| `runs/plx/plx_h0.01_v0.1` | 0 | 4:42.72 | 192 MB |
| `runs/plx/plx_h0.01_v0.5` | 0 | 4:07.81 | 194 MB |
| `runs/plx/plx_h0.02_v0.1_then_v0.5` | 0 | 2:38.46 | 191 MB |

(`dev/` rows are development runs, `runs/` rows are runs of record; `D6_h0.00125_d1e-12_s-1` and `_s1` are the two sides of one pair; the planted chain `plx_h0.02_v0.1_then_v0.5` is one unit.)
