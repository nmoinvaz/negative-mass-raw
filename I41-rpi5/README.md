# I41-rpi5: the settled black-hole mass at the Ellis threshold (D = 4, family S)

Machine rpi5-ubuntu (Raspberry Pi 5, 4 cores, 8 GB, aarch64), Python 3.14.10, numpy 2.5.4, scipy, numba 0.68.1, one thread per process, `nice -n 10`, at most 3 processes.
Issue https://github.com/nmoinvaz/negative-mass/issues/41 ("Reconcile the Ellis threshold masses 0.30 a and 0.22 a"). Worktree `negative-mass-i41`, branch
`wip/i41-threshold-masses`, from main at 2a712f5. Code: `notes/wormhole_evolution/settled_mass.py`, which imports #39's `dn.py` and #40's `threshold.py` unchanged.
This README is written before the runs of record. It states each check, its bar, and the mutation that must fire it. Status words as in AGENTS.md: every mass here is
*numerical evidence*. No sentence claims novelty.

## Question and plan

[SH02] reports a threshold black-hole mass M → 0.30 a and [GGS09b] m_AH ≈ 0.22 (r_AH 0.51 → 0.45), both in units of the initial throat radius a. #40 measured the
Misner–Sharp mass at the first trapped cell (0.494 a, r ≈ 0.99 a), a formation value in a grid that stretches. This issue:

- **A.** What each of [SH02], [GGS09b], [ST17] calls the threshold black-hole mass: definition (section and equation), unit, time of reading, conversion to one unit. Read from arXiv
  (PDF; TeX source for [GGS09b] and [ST17]); hashes in `papers.sha256`, fetch log in `papers.fetch.log`; the files are kept outside the repository.
- **B.** The settled mass in this code: D = 4, family S of #40 (symmetric ghost pulse, Gaussian in φ, centre 3, width 0.5, mirrored with parity −1 onto the other ray), at
  p*ₕ − δ on the collapse side, δ = 1e-6 and 1e-8, followed past the first trapped cell, M_AH(t) recorded until it settles or the declared limit.
- **C.** The comparison with 0.30 a and 0.22 a.

## What is built (not in #39 or #40)

A uniform grid cannot follow the horizon. On it e^{−f} grows exponentially along the horizon (pilot at h = 0.02, δ = 1e-8, no excision: e^{−f} = 1.0 at the first trapped
cell, 4.1 at x⁺ = 12.95, 12 at 13.45, 38 at 14.2; `dev/pilot1.log`), the horizon is a layer of width about r e^{f} in x⁻, and the cell update loses it (#39's F_cut = 25 excises it).
`settled_mass.py` keeps the horizon on the grid with a chain of levels:

- level 0 is #39's uniform square grid (h, h), evolved by the same arithmetic (`row_step2` with h₊ = h₋ is `dn.row_step`; check PL3);
- level k ≥ 1 is a box that starts on the column x⁺ = v_k, has Nc cells of width h/2^k in x⁻ centred on the horizon, and runs to the end of x⁺. Its lower ray is the row of level
  k − 1 at the box's lower edge, its left ray the column of level k − 1 at v_k interpolated (cubic, 4 points) to the finer nodes. Characteristic evolution has no dependence on
  later x⁻ or x⁺, so each level is exact in its domain of dependence;
- level k + 1 starts at the first column where e^{−f} on the horizon reaches F_{k+1} = F₁ 2^k, so e^{−f} h₋ is the same at the end of every level;
- the horizon is the zero of r₊ (+ to − along x⁻, with r₋ < −tol) in each cell column, linearly interpolated between cell centres; there M_AH = r^{n−1}/2 (the cell formula
  r^{n−1}(1 + 2e^f r₊r₋)/2 is interpolated alongside and equals it to the truncation error);
- the series starts at the first trapped cell of #40's definition (r₊, r₋ < −1e-2), excision as #39 (r_cut = 0.05; no e^{−f} cut).

## Declared parameters

| quantity | value |
|---|---|
| dimension, family | D = 4 (n = 2), S, 8πG = 1, a = 1 |
| h | 0.02, 0.01, 0.005 (the three of #40, the declared triple) and 0.0025 (a fourth member, giving the finer triple 0.01, 0.005, 0.0025) |
| δ | 1e-6 and 1e-8, p = p*ₕ − δ (collapse side); p*ₕ re-bisected on this machine to hi − lo ≤ 1e-14 (`runs/pstar_h*.json`) |
| chain | F₁ = 1.5, K = 20 (levels 1 to 20); level 1 is W₁ = 2.4 wide in x⁻ and each box has Nc = 2W₁/h cells (240, 480, 960, 1920), width h/2^k at level k |
| **declared stretching limit** | **e^{−f} on the horizon ≤ F_max = F₁ 2^K = 1 572 864** (the series ends at the last column below it). The horizon is then resolved to ρ = e^{−f}h₋/(2r) ≈ F₁h/2r (0.03 at h = 0.02) |
| rectangle | rows: first trapped row + 3 + Nc h/4; columns: first trapped column + 12 |
| trapped tolerance, r_cut | 1e-2 (#40), 0.05 (#39) |

## Planted cases (exact solutions through the same chain, written down before the runs of record)

- **P1**, D = 4 Schwarzschild, r_h = 0.6 (M = 0.3), in coordinates where the horizon is x⁻ = 5 and e^{−f} on it is e^{2(x⁺−3)} (an Eddington-type x⁺ and a Kruskal-type x⁻: the
  stretching of the real run). Closed form by Lambert W. M_AH must be 0.3 at every column up to the limit.
- **P2**, the exact ghost solution r² = a(p² + m²) − pm, f = 0, a = 3/4 (derive.py D5), through two forced zoom levels (x⁺ = 3.0 and 3.08, to 3.12). Its contour r₊ = 0 is
  m = 2ap (a moving line; r₋ > 0 there, so the finder runs without the trapped condition); r on it is known.

## Checks, bars, and the mutations that must fire

| id | check | bar |
|---|---|---|
| PL1 | P1: M recovered, second order, limit reached | max \|M − 0.3\| ≤ 1e-4 at h = 0.005; orders of the max error between the four h in [1.75, 2.25]; every run ends at F ≥ F_max/2 |
| PL2 | P2: r on the moving contour | max error ≤ 5e-5 at h = 0.005; orders in [1.75, 2.25] |
| PL3 | level 0 against `dn.evolve` (numba) on the same data (h = 0.02, δ = 1e-6) | nodes and dead flags bit-identical; same first trapped cell |
| AN | chain (h = 0.02, δ = 1e-6) against a zoom-free uniform anisotropic grid (h, h/32) at its own p*_AN − δ (`runs/pstar_an_h0.02_Q32.json`), where e^{−f} < 40 | max \|ΔM\| ≤ 3e-4 |
| RC1 | p*ₕ on this machine | hi − lo ≤ 1e-14 and, where #40 has it, within 1e-11 of #40's (dh610-fedora) |
| RC2 | fates at p*ₕ ∓ δ (all h, both δ); first trapped cell and its time at δ = 1e-8 against #40's | collapse and expansion; cell equal; \|T − T₄₀\| ≤ √2 h |
| RC3 | M_AH at the first trapped cell against #40's M_hor at p*ₕ − 1e-8 | ≤ 2e-3 |
| RC4 | first law on the horizon: ΔM = ∫(r²/2) e^f r₋ φ₊² dx⁺ from the first trapped cell to e^{−f} = 20 | relative ≤ 2e-2 |
| RC5 | every run ends at the declared limit (status "limit", F_max/2 ≤ F_end < F_max), ≥ Nc/8 cells from the box edges, no gaps | all |
| RC6 | second order of M_AH(x⁺): max \|M_h − M_h/2\| over three windows of x⁺ − x⁺_f ([0, 1.5], [1.5, 3], [3, end]), cubic splines, both δ, h = 0.02, 0.01, 0.005 | observed order in [1.5, 2.5] |
| RC6b | the same for h = 0.01, 0.005, 0.0025 | observed order in [1.5, 2.5] |
| RC7 | the settled value does not depend on δ | plateau means over the last 1.0 of x⁺ at δ = 1e-6, 1e-8 differ by ≤ 1e-4, every h |
| RC8 | M_AH has settled at the limit | plateau mean over the last 1.0 differs from that of the previous 1.0 by ≤ 1e-4, and the mean horizon flux over the last 0.5 is ≤ 1e-5, every run |

The acceptance of the issue, "M_AH(t) converges at second order at three h up to the declared limit and its settled value is reported with what the error bar is", is RC5, RC6, RC8
and the report below; PL1 to PL3, AN and RC1 to RC4 are the controls under it. RC6's band is wider than #39's [1.75, 2.25] because the development runs at the declared parameters gave
orders 1.6 to 2.4 over these windows (noise of order 1e-5 at the level switches); P1 and P2, which have exact answers, keep #39's band. RC7 and RC8 use plateau means, not the value at the
last column: at h = 0.02 the end value has a jitter of 1.5e-4 from the level sawtooth (found in development, raw `dev/analyze_dev3.log`, which failed both with the end value). A failed
check is reported as not met.

## What is reported without a bar

- M_AH(x⁺), r_AH, e^{−f}, t = (x⁺ + x⁻)/√2 on the horizon, for each h and δ (`settled_mass_output.txt`).
- The late-time value: M at the limit, plateau means over the last 1.0 and 0.5, their range, the change between the last two windows, the mean horizon flux. **Four error bars, never
  mixed**: *resolution* (differences between h, Richardson), *window* (plateau means and ranges), *δ* (1e-6 against 1e-8), and the *limit* (what the flux at the limit could still remove: the
  flux integrated forward is not extrapolated; the flux at the limit is reported).
- h = 0.0025 as a fourth member; M at the limit against the distance from threshold (`settled_mass.py scan`, family S, δ from 1e-8 to 1e-1, h = 0.01); [SH02]'s Table I data through the same chain
  (`settled_mass.py sh02`, h = 0.01, 0.005): E0, x⁻_H and M against their printed values, and the e^{−f} at which our M_AH equals their M.

## Mutations (targets computed in development before they were declared; dev logs in `dev/mut/`)

Predictions written before the development mutation runs finished, then the fired set in the development run (the runs of record repeat them and must give the same set).

| mutation | what it breaks | predicted | fired in development = declared |
|---|---|---|---|
| `mass_exponent` | M = r^n/2 instead of r^{n−1}/2 | PL1, RC3, RC4 | PL1, RC3, RC4 |
| `finder_sign` | finder looks for the − to + crossing of r₊ | PL1, PL2, AN, RC2 to RC8 | AN, PL1, PL2, RC2 to RC8 |
| `hm_swap` | the kernel uses h₊ for h₋ | PL1, PL2, AN, others unknown | AN, PL1, PL2, RC4, RC5, RC6, RC6b, RC7, RC8 |
| `interp_shift` | left-ray cubic evaluated at 1/4 of a cell, not 1/2 | PL1, PL2, others unknown | AN, PL1, PL2, RC6, RC6b, RC7, RC8 |
| `flux_sign` | sign of the first-law integrand | RC4 | RC4 |
| `time_unit` | t = x⁺ + x⁻ (no 1/√2) | RC2 | RC2 |
| `no_zoom` | K = 0 | PL1, RC5, RC8, others unknown | PL1, RC5, RC6, RC6b, RC7, RC8 |
| `short_limit` | K = 12 in the real runs (F_max = 6144) | RC5, RC8 | RC5, RC8 |
| `pstar_off` | p*ₕ + 2e-8, so the collapse side is lost | RC2 to RC8 | RC2 to RC8 |
| `theta_coef` | #39's sphere-term coefficient | PL1, PL2, AN, RC2 to RC8 | AN, PL1, PL2, PL3, RC2 to RC8 (PL3 by its exception: the data's fates change) |
| `rcut_off` | the chain's r_cut × 1.5 (level 0 differs only in the interior) | PL3 | PL3 |
| `an_nodes` | the AN grid's left-ray nodes 1 % off | AN | AN |
| `i40_shift` | #40's p*ₕ + 1e-10 | RC1 | RC1 |
| `col_shift` | x⁺ of a record at the left edge of the cell, not its centre | PL2, RC6, RC6b | PL2, RC6, RC6b |
| `delta_swap` | the δ = 1e-6 runs replaced by δ = 3e-2 | RC7 | RC7 |

Two controls were wrong at first and are reported: `delta_swap` with δ = 1e-3 was silent (M at the limit is flat in δ to 1e-3, as the scan shows; `dev/mut_first/mut_delta_swap.log`), replaced by δ = 3e-2
before any run of record; the first `finder_sign`, `theta_coef` runs stopped on an uncaught exception in the AN check and in the kernel-identity check (`dev/mut_first/`), fixed by catching it and
recording the check as failed. The development mutation runs used `devraw` (the same jobs and the same p*ₕ as the runs of record, run before the criteria were frozen); the runs of record repeat them.

## Development runs (before the runs of record)

`dev/`: the pilot of the uniform grid without excision, planted P1 at four h and Nc = 120, 240, 480, P2 at four h, the real runs at F₁ = 4, 2, 1.5 and Nc = 120 to 960, then
the chain at the declared parameters (`analyze_dev1.log` to `analyze_dev4.log`), the supplementary scan and SH02 runs, and the scripts (`dev/scripts/`, copied from the scratchpad; they
import `settled_mass.py` as it was then).

## Changes made during development (all before the runs of record)

- F₁ 4 → 2 → 1.5: at h = 0.02 the series had a sawtooth of up to 5e-4 at the level boundaries (error growing as ρ² within a level, ρ = e^{−f}h₋/2r); at F₁ = 1.5 the series moves by at most
  1.5e-6 between Nc = 480 and 960 at h = 0.005. F₁ = 1.0 loses the horizon at level 1 (r₋ at the throat is about −0.02, near the trapped-cell tolerance 1e-2): not used.
- Nc: 120 → 480 → the box width fixed in x⁻ (W₁ = 2.4, Nc = 2W₁/h). At Nc = 120 the planted P1 error at the finest h grew with the level (7.4e-6 at level 0 to 1.6e-5 at level 10): the row
  at the box's lower edge, which seeds the next level, was only Nc/4 cells deep. At Nc = 480 and h = 0.0025 the box (0.6 wide) was narrower than the horizon's motion in level 1 (0.24 in x⁻) and the
  run stopped ("horizon too close to the edge"); with W₁ fixed all four h run.
- K: 12 → 20. At F_max = 6144 the horizon flux had not died (φ₊ on the horizon changes sign near x⁺ − x⁺_f = 4.75 and a second, smaller infall of ghost field starts, flux up to 4e-4 at 5.75);
  the first draft of RC8 fitted an exponential to it, which is wrong (`dev/analyze_dev2.log`). At K = 20 the flux falls below 1e-6 by x⁺ − x⁺_f ≈ 8.5. dxp 10 → 12.
- The AN control first used the same amplitude as the chain on the anisotropic grid: that grid has its own discrete threshold (p*_AN = −1.4e-4 against +4.75e-5), so no trapped cell formed.
  It now bisects p*_AN (`pstar_an`) and compares at p*_AN − δ. The first bisection stopped at the row limit ("static through X", hi − lo = 2.9e-8); the rows were extended (hi − lo = 2.7e-10).
- RC7 and RC8 moved from the value at the last column to plateau means (above).
- P1 horizon x⁻ = 1 → 5 (the box needs Nc h/4 rows of level 0 on each side); P2's first windows (zoom at 3.0 and 3.15, end 3.25) lost the contour at h = 0.0025, now 3.0, 3.08, 3.12.
  P1 uses r₋ < 0 as the trapped condition (tol = 0); the real runs use #40's 1e-2.
- `track` got an end reason; the chain got first-trapped-cell detection inside the row sweep, equal to `dn.events_from_grid`'s collapse event (PL3).
- p*ₕ is bisected on this machine for the four h (units `nm-i41-pstar*`); it matches #40's (dh610-fedora) to 9e-15, −4.6e-14, −3.1e-15 at the first three h.
- Mistakes: `settled_mass.py` was edited (appended to) while the first bisection units were running (they had already loaded it and `pstar` was untouched); the first launcher script named
  the run folders `h_d1e-6` (empty shell variable, and the analysis expects `h0.02_d1e-06`), caught before any analysis; the `sh02` E0 was first computed on a ray shorter than x⁺ = 20
  (E at x⁺ = 18.6 for three rows) and the Gaussian first placed at x⁺ = 3 instead of the printed l = 3; both corrected before use.

## Runs of record

Code: `settled_mass.py` at 4706c38 for the jobs, the first analysis and the 15 mutated analyses; 16a04d2 adds three reports (the M_AH table to the limit, the F* columns of `sh02`, the command
`sh02_uniform`) and changes no check; the second analysis, `sh02` and `sh02_uniform` were run at 16a04d2. All runs: systemd user units, `nice -n 10`, one thread, at most 3 at once.

| what | unit | command or script | wall time | exit |
|---|---|---|---|---|
| p*ₕ, four h (18, 18, 18, 23 runs) | `nm-i41-pstar0.0025`, `pstar0.005`, `pstar-fast` | `settled_mass.py pstar --h=H` | 627 s, 140 s, 48 s, 14 s | 0 |
| p*_AN, h = 0.02, Q = 32 | `nm-i41-pstaran2` (dev folder, copied to `runs/`) | `settled_mass.py pstar_an` | 79 s | 0 |
| jobs, h = 0.02, 0.01, 0.005, 0.0025 at δ = 1e-6 and 1e-8 | `nm-i41-rec-jobs-a`, `-b` | `launch_jobs.sh` | 3 s to 102 s each, peak rss 1.79 GB (h = 0.0025, δ = 1e-8) | 0 (8 of 8) |
| analysis of record (13 checks) | `nm-i41-rec-analyze` (4706c38), `nm-i41-rec2-analyze` (16a04d2) | `settled_mass.py analyze --raw=...` | 30 s, 43 s | 0, 0 |
| 15 mutated analyses | `nm-i41-rec-mut-a`, `-b`, `-c` | `launch_mut.sh` | about 5 min each | 1 each (a check fires), fired set = declared set in 15 of 15 |
| M at the limit against δ (family S, h = 0.01) | `nm-i41-rec-scan` | `settled_mass.py scan` | 66 s | 0 |
| SH02 Table I through the chain, h = 0.01, 0.005 | `nm-i41-rec-scan` (first), `nm-i41-rec2-sh02` (with F*) | `settled_mass.py sh02` | 40 s, 105 s | 0 |
| SH02 data on a uniform grid of 9600 cells | `nm-i41-rec2-uniform` | `settled_mass.py sh02_uniform` | about 6 min, peak about 2 GB | 0 |

Result: 13 of 13 checks pass; M_AH settles at 0.22308 a (r_AH = 0.44617 a) to e^{−f} = 1.57e6 on the horizon; see `settled_mass_output.txt` in the repository and `analyze_record.log` here
(`analyze_record_1.log` is the first analysis, at 4706c38). Mistakes of the runs of record: the shell that moved the old `sh02` logs aside used an empty variable in one name, so
`runs/sh02_h_1.log` (renamed `sh02_h0.005_1.log`) holds only the first h = 0.005 stdout and the first h = 0.01 stdout was overwritten (its numbers are in `sh02_h0.01.json`, which the rerun rewrote with the
same E0, x_H and M and the added F*).
