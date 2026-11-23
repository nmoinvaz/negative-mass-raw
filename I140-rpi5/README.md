# I140-rpi5: a machine-independent window count for the tanh spectrum (#96's 22 sectors, recounted) and an accurate v_c for the B-spline checker

Machine: rpi5-ubuntu (Raspberry Pi 5, Cortex-A76, aarch64, 4 cores, 8 GB, shared with choptuik-large-d), one process, one thread
(`OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`), `nice -n 10`. Python 3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0
(`~/Source/negative-mass-venv314`). numpy's CPU features here: NEON, NEON_FP16, NEON_VFPV4, ASIMD, FPHP, ASIMDHP, ASIMDDP.
Issue: https://github.com/nmoinvaz/negative-mass/issues/140
Worktree `~/Source/negative-mass-i140`, branch `wip/i140-window-vc`, base main 87279bd. Raw clone `~/Source/negative-mass-raw`.

Nothing of #96's runs is recomputed. Everything here reads the stored arrays (`I96-win/eig`, `I96-dh610/eig`) and a quadrature.

## Inputs

| σR | sectors | folder | P |
|---|---|---|---|
| 8 | m = 1/2 .. 21/2 | `I96-win/eig/tanh_sigma8_m*.npz` | 200 |
| 16 | m = 1/2 .. 21/2 | `I96-dh610/eig/tanh_sigma16_m*.npz` | 340 |

Both machines stored σR = 16, m = 1/2: `I96-win/eig/tanh_sigma16_m0.5.npz` is the pilot (P = 320), `I96-dh610/eig/...` is the sector
run (P = 340). The sector of the table is the dh610 file, which is the one §7's table and `sectors-s16-p340.log` quote. The pilot
is recounted beside it and compared (A5).

## What is fixed

Convention. The window of A is {μ : |μ| v_c ≥ cut}. The cut is the modulus of the first eigenvalue of A, in order of decreasing
modulus, that has no eigenvalue of B within 1e-5 relative. So the window includes that eigenvalue and its conjugate, which have
the same modulus. The cut and the window both read one `np.abs` array. `np.abs(array)` and `abs(scalar)` can differ in the last
bit (here, for 309,576 of 825,000 stored values), and that bit decided whether the pair counted.

Count by position. The index k of the cut's eigenvalue in A sorted by decreasing |μ|; the count is the number of eigenvalues up
to and including the last of {z, conj z} (found by exact complex equality), so the pair is counted together.

Count by exact modulus (added, a second independent count). #{j : re_j² + im_j² ≥ re_k² + im_k²} with the squares formed exactly in
rational arithmetic from the stored doubles. No rounded modulus enters it.

Symmetry value. max over z in the window of min over A of |μ + z| / |z|, as in `part_tanh`.

## Criteria, written before the first run

Planted truth, before any stored array.

- A1. Plant P1, hand-made, every modulus exact in binary. A (18 values, shuffled): the quadruples ±5/16 ± 3i/4 (|μ| = 13/16) and
  ±7/32 ± 3i/4 (25/32); the reals ±nextafter(5/8, 1) (one ulp above the cut); the conjugate pair 3/8 ± i/2 (|μ| = 5/8, the cut);
  the reals ±nextafter(5/8, 0) (one ulp below); the quadruple ±5/16 ± 21i/64 (29/64). B: each value above the cut times
  (1 + 1e-8), the cut pair times (1 + 1e-3) (no partner within 1e-5), the pair below times (1 − 1e-3), the last quadruple times
  (1 + 1e-8). Predicted: cut 0.625 exactly, k = 10, window of A 12 (the two quadruples, ±nextafter up, the pair; not the reals
  one ulp below), window of B 12, count by position 12, count by exact modulus 12, symmetry value √137/40 = 0.292617 (the pair's
  −z is missing from A; the nearest value is −5/16 − 21i/64, at distance √137/64). Fail: any of these differs.
- A2. Plant P2, the same layout with the cut pair replaced by a pair found on this machine whose `np.abs(array)` is smaller than
  its `abs(scalar)` (seeded search, `default_rng(140)`; the reals one ulp above and below are taken from the array value).
  Predicted: window of A 12, k = 10, window of B 12. If no such pair exists on a machine, P2 is vacuous and says so.
- The planted checks run first; the real arrays are not read if one fails.

Stored arrays, 22 sectors (σR = 8 and 16, m = 1/2 .. 21/2).

- A3. The window count of A equals the count by position and the count by exact modulus, in 22 of 22 sectors. The cut's tie group
  (elements with the cut's modulus exactly) is the cut's eigenvalue and its conjugate: 2 elements.
- A4. Margin: the smallest |ab − cut| / cut over the elements outside the tie group is at least 1e-13 (about 450 ulp) in every
  sector, so no other eigenvalue's inclusion depends on the last bit of any modulus routine. Fail: a sector below it.
- A5. σR = 16, m = 1/2, pilot against P = 340: the leading |μ| v_c of A and of B each within 1e-8 relative (R3 of I96-rpi5 has 9.1e-11
  and 1.4e-9; the threshold is a round number chosen with those in view), the cut equal at the four digits §7 prints (0.1128), and
  both files pass A3 and A4. The two windows' counts are reported, not required equal (different P).
- A6. The window columns of the 22 sectors are listed against §7's printed tables (the window tables' "eigenvalues in it (A / B)",
  the sector tables' "symmetric to"), parsed from `notes/warp/tanh_spectrum.md`, and against the two sector logs. Data: every
  difference is listed with the old and the new value. No threshold.

Cross-machine. The coordinator reruns `retab.py` on the Mac; `retab_rpi5.csv` holds only the machine-independent columns (counts,
the cut to four digits, the symmetry value to two digits), so the two files `diff` directly.

## Controls, each must fire

- C1. `tanh_spectrum.py --part=window --mutate=abscut` (the cut taken as `abs(z)` of one scalar): exit 1, `window_scalar` fails
  (P2's window of A is 10, not 12), `window_planted` passes (P1's moduli are exact, so the two paths agree on it).
- C2. `retab.py --mutate=abscut`: A3 fails. Predicted sectors, from the signs of `np.abs(array) − abs(scalar)` at the cut on this
  machine (`I96-rpi5/sector_numbers_output.txt`, R1b): σR = 8, m = 13/2 and 17/2; σR = 16, m = 1/2, 7/2, 11/2 and 15/2. In each the
  window of A is 2 below the count by position. The other 16 sectors pass.
- C3. `retab.py --mutate=nearcut` (an unmatched real value one ulp above the cut is added to A): A4 fails in 22 of 22.
- C4. `retab.py --mutate=notie` (the count by position stops counting the conjugate pair together): A3 fails in 22 of 22, the count
  by position 1 below the window.
- If a control does not fire where predicted, report it. The mutation is not changed.

Differences from §7 expected before the run (an expectation, not a criterion). The sector logs follow the rounding of the machine
that wrote them: the laptop (σR = 8) left the cut's pair out at m = 7/2, 13/2, 15/2, 17/2 (the Mac's negative signs, and the Mac
reproduces the log in all 132 values), dh610 (σR = 16) at m = 1/2, 7/2, 11/2, 15/2 (rpi5's, and rpi5 reproduces the log in 132 of
132). With the pair always in, A's window count should rise by 2 in exactly those 8 sectors (σR = 8: 24→26, 16→18, 16→18,
16→18; σR = 16: 20→22, 16→18, 16→18, 12→14), A's totals from 254 to 262 and from 186 to 194, B's counts and totals (284, 216)
not move, and the symmetry value change at least at σR = 8, m = 15/2 (3.4e-11 → 5.5e-11) and σR = 16, m = 15/2 (2.9e-11 →
4.0e-11).

Supplementary, not part of the acceptance. `I75-dh170` holds σR = 2 and 4 arrays (22 sectors), so the same recount is run on them
and compared with `notes/warp/tanh_spectrum_output.txt` (which feeds §4's symmetry sentence and §5's window totals 652 / 676 and
396 / 424). Data only.

## v_c of the B-spline checker

- V0. `I96-mac2/vc96.py` rerun here (mpmath, 30 digits) reproduces `vc96.txt` to the 15 digits it prints: σR = 2, 4, 8, 16 give
  3.7448997586788, 2.47097067490909, 1.56243374163835, 0.985029856014836.
- V1. New `v_c` in `tanh_spectrum_check.py`: Gauss–Legendre, 20 nodes per panel, panels split at r = 1 + j/σ for j = −6..6 (clipped
  at 0), plus the end panels [0, first split] and [1 + 6/σ, 1 + 14/σ]. Fixed before the run. |v_c − vc96| < 1e-9 at σR = 2, 4, 8
  and 16. Fail: any larger.
- V2. `--mutate=nosplit` restores one panel on [0, 15] with 400 nodes (the previous rule). Predicted: fails V1 at σR = 16, with
  v_c ≈ 0.9850202 (9.7e-6 low, from I96-mac2's review). At σR = 2, 4, 8 it is the previous values, reported as data.
- V3. What changes in `tanh_spectrum_check.py`'s printed outputs: the previous and the new v_c at the four σR. The report's
  `v_c sR=` check (σR = 2 and 4, against #75's printed values to 1e-5) is predicted to pass as before.

## Results, step 2: the window helper (code: `wip/i140-window-vc` at 5cdf71a)

Correction before any run: the text above had √137/40 = 0.292618; it is 0.2926175 and prints as 0.292617. The check compares
with `math.sqrt(137) / 40` to 1e-12, so it was never affected.

| check | verdict | numbers |
|---|---|---|
| A1 plant P1 | pass | cut 0.625, k 10, windows 12 / 12, by position 12, symmetry 0.292617 (`window_plant.log`) |
| A2 plant P2 | pass | pair 0.455509+0.374953i, `np.abs(array)` 0.5899815219915627 below `abs(scalar)` 0.5899815219915628: k 10, windows 12 / 12 |
| A3 | pass | window = position = exact modulus in 22 of 22; the cut's tie group is the eigenvalue and its conjugate in 22 of 22 |
| A4 | pass | smallest margin 2.2e-11 (σR = 8), 1.9e-12 (σR = 16, m = 5/2); limit 1e-13 |
| A5 | pass | pilot and P = 340: leading \|μ\|v_c differ by 9.1e-11 (A) and 1.4e-9 (B), cut 0.1128 in both, A window 22 and B 24 in both, pilot margin 1.7e-10 |
| A6 | listed | 8 of 22 sectors differ from §7 (below); §7's tables equal the two logs where they print the same column |

`retab_rpi5.txt` is the run (`retab.py --tag=rpi5`, exit 0, 1.6 s, 123 MB), `retab_rpi5.csv` its machine-independent columns.
`drive_part_tanh.py` runs `part_tanh` itself on the stored arrays (no solve; `ts.sector_task` returns the stored eigenvalues)
and compares the window table it prints with the csv: 22 of 22 equal (`drive_part_tanh.txt`), so the wiring of `window()` into
`part_tanh` is exercised.

Differences from §7 (old → new), all from `retab_rpi5.txt` A6. B's counts do not move in any sector.

| σR | m | A window | symmetry |
|---|---|---|---|
| 8 | 7/2 | 24 → 26 | |
| 8 | 13/2 | 16 → 18 | 2.5e-11 → 4.2e-11 |
| 8 | 15/2 | 16 → 18 | 3.4e-11 → 5.5e-11 |
| 8 | 17/2 | 16 → 18 | 4.6e-11 → 7.2e-11 |
| 16 | 1/2 | 20 → 22 | 5.3e-10 → 5.5e-10 |
| 16 | 7/2 | 16 → 18 | |
| 16 | 11/2 | 16 → 18 | 2.6e-11 → 3.4e-11 |
| 16 | 15/2 | 12 → 14 | 2.9e-11 → 4.0e-11 |

Totals: σR = 8 A 254 → 262 (B 284), σR = 16 A 186 → 194 (B 216). These are the eight sectors predicted before the run, with the
predicted +2 in each, the two predicted symmetry changes, and four more symmetry changes that "at least" allowed. The sectors
changed are the ones where `np.abs(array) − abs(scalar)` at the cut is negative on the machine that wrote the log
(`−` in the table of `retab_rpi5.txt` is this machine's sign; the laptop's and dh610's are inferred from their logs).

Controls.

| control | predicted | observed |
|---|---|---|
| C1 `tanh_spectrum.py --part=window --mutate=abscut` | exit 1, `window_scalar` fails (A window 10), `window_planted` passes | as predicted: exit 1, `window_scalar` fails with A window 10, `window_planted` passes (`window_plant_abscut.log`) |
| C2 `retab.py --mutate=abscut` | A3 fails in σR = 8 m = 13/2, 17/2 and σR = 16 m = 1/2, 7/2, 11/2, 15/2, window 2 below position | as predicted, exactly those six, window 16/16/20/16/16/12 against position 18/18/22/18/18/14 (`retab_rpi5_abscut.txt`, exit 1) |
| C3 `retab.py --mutate=nearcut` | A4 fails in 22 of 22 | as predicted (margins 1.3e-16 and 1.2e-16); A5 fails too (its pilot margin). Unpredicted: A3 also fails at σR = 16, m = 11/2: window 17 = position 17 but exact modulus 19 (`retab_rpi5_nearcut.txt`) |
| C4 `retab.py --mutate=notie` | A3 fails in 22 of 22, position 1 below the window | as predicted (`retab_rpi5_notie.txt`, exit 1) |
| `drive_part_tanh.py --mutate=abscut` | part_tanh prints the old values in the six C2 sectors | as predicted: 6 of 22 differ, and they are the logs' old values (`drive_part_tanh_abscut.txt`, exit 1) |

The unpredicted A3 failure under `nearcut` is the exact-modulus count seeing the array's rounding. At σR = 16, m = 11/2 the cut
pair's exact modulus is 1.04 ulp above its `np.abs(array)` value, so `np.abs(array)` here is not correctly rounded; the added real
value, one ulp above that array value, is at or below the pair's exact modulus, and the exact count puts the pair inside while the
array-modulus window leaves it out. (`abs(scalar)` is `hypot` here and equals the array value plus one ulp.) With the unmutated helper
the pair is inside the window by construction, and window, position and exact counts agree in all 22 sectors.

## Results, step 3: v_c (code: `wip/i140-window-vc` at 000c3a2, outputs at 93ed6d1)

| check | verdict | numbers |
|---|---|---|
| V0 `vc96.py` rerun | pass | `vc96_rerun_rpi5.txt` is identical to `I96-mac2/vc96.txt` (0.6 s) |
| V1 split v_c, 20 nodes, \|j\| <= 6, end at 1 + 14/σ | pass | difference from mpmath +8.9e-16, 0, +4.7e-15, +2.2e-16 at σR = 2, 4, 8, 16 (limit 1e-9) (`vc_split.log`, exit 0) |
| V2 `--mutate=nosplit` (one panel on [0, 15], 400 nodes) | as predicted | v_c(16) = 0.985020182373, 9.7e-6 low; `v_c sR=16` fails, exit 1 (`vc_nosplit.log`). At σR = 2, 4, 8 it passes at 2.6e-14, 2.5e-14, 3.6e-13: the previous rule was accurate up to σR = 8 |
| V3 what changes in the checker's output | | `--part=report --out=I94-win/eig` run with the previous script (main 87279bd) and the new one gives the same output line for line (`report_old_vs_new.diff` is empty): the `v_c sR=` check (σR = 2 and 4 against #75's printed 3.7449 and 2.470971, limit 1e-5) passes as before, the new values differing from the old by 2.7e-14 and 2.5e-14, below the six digits printed. σR = 8 and 16 appear only in `--part=solve`: the stored `vc`, the `v_c =` header and the ARPACK floor `--floor / v_c`. New − old is +3.6e-13 at σR = 8 and +9.7e-6 at σR = 16 (printed 0.985020 → 0.985030, and every \|μ\|v_c of a σR = 16 run is 9.8e-6 larger relative) |

Runs and exit codes (each stdout in this folder; `.exit` holds the code):

| file | command (from the worktree root) | exit |
|---|---|---|
| `window_plant.log` | `python notes/warp/tanh_spectrum.py --part=window` | 0 |
| `window_plant_abscut.log` | the same with `--mutate=abscut` | 1 (`window_scalar`) |
| `retab_rpi5.txt` (= `notes/warp/tanh_spectrum_windows_output.txt`) | `python -X utf8 ../negative-mass-raw/I140-rpi5/retab.py --tag=rpi5 --ts=notes/warp` | 0 |
| `retab_rpi5_abscut.txt`, `_nearcut`, `_notie` | the same with `--mutate=...` | 1, 1, 1 |
| `drive_part_tanh.txt`, `drive_part_tanh_abscut.txt` | `python -X utf8 ../negative-mass-raw/I140-rpi5/drive_part_tanh.py --ts=notes/warp [--mutate=abscut]` | 0, 1 |
| `vc_split.log` (= `notes/warp/tanh_spectrum_check_vc_output.txt`) | `python notes/warp/tanh_spectrum_check.py --part=vc` | 0 |
| `vc_nosplit.log` | the same with `--mutate=nosplit` | 1 (`v_c sR=16`) |
| `vc96_rerun_rpi5.txt` | `python ../negative-mass-raw/I96-mac2/vc96.py` | 0 |
| `report_old_v_c.log`, `report_new_v_c.log` | `tanh_spectrum_check.py --part=report --out=../negative-mass-raw/I94-win/eig` with the script of 87279bd and of 000c3a2 | 1, 1 (the same `own75` failures in both; these arrays are #94's first ones) |

Memory and time. Every run is one process on one thread under `nice -n 10`, each under 2 s of wall time and 125 MB resident
(`retab.py` 1.6 s, 123 MB; `vc96.py` 0.6 s, 21 MB). Nothing came near a limit, and nothing was stopped.

The earlier logs of `window_plant*.log` and `vc_split.log` had a header line naming an uncommitted tree. They were rerun from the
committed code (`000c3a2`) with the stdout unchanged, and the notes' two output files are those stdouts.

Cross-machine rerun on the Mac (the coordinator's): from the raw clone, `python -X utf8 I140-rpi5/retab.py --tag=mac
--ts=<worktree>/notes/warp`, then `diff I140-rpi5/retab_rpi5.csv I140-rpi5/retab_mac.csv`. The csv holds counts, the cut to four
digits and the symmetry value to two, so a difference is a machine dependence. `retab.py` runs the planted checks first and
then reads `I96-win/eig`, `I96-dh610/eig` and (supplementary) `I75-dh170`.

## Files

`retab.py` (re-tabulation, imports `tanh_spectrum.window`), `drive_part_tanh.py` (runs `part_tanh` on the stored arrays),
`retab_rpi5.csv` and the three mutated csv, the logs in the tables above, `report_old_vs_new.diff`, `vc96_rerun_rpi5.err` (its
`time -f` line).
