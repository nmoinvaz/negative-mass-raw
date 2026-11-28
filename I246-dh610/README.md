# I246-dh610: the settled black-hole mass at D = 5 and 6 (families S and G), #41's apparent-horizon chain, and a planted Tangherlini

Machine dh610-fedora (Fedora, i7-12700, 20 threads shared with choptuik-large-d, 62 GB), Python 3.14.10, numpy 2.5.4, scipy 1.18.1, numba 0.68.1, one thread per process, `nice -n 10`, at most 4
processes, runs longer than a few minutes as systemd user units `nm-i246-*`. Memory is reported, never a stop condition; any single run over 3 h of wall time is stopped and reported (`timeout 10800`).
Issue https://github.com/nmoinvaz/negative-mass/issues/246 ("The settled threshold mass at D = 5 and 6 (#41)"), with #253's addition (family G at D = 5 and 6). Worktree `negative-mass-i246`, branch
`wip/i246-settled-mass-d56`, from main at 1f3a548. Code: `notes/wormhole_evolution/settled_mass_d56.py`, a thin driver that imports #41's `settled_mass.py`, #253's `settled_mass_g.py`, #40's `threshold.py`
and #39's `dn.py` unchanged. This README is written before any run of record (the first commit of this folder after the development runs); the mutation targets in the last section were computed in
development runs and are declared with it. Nothing declared here is changed after the first run of record without a ruling over hc. Status words as in AGENTS.md: every mass here is *numerical
evidence*. No sentence claims novelty. Units: a = 1 (throat radius of the initial static wormhole), 8πG = 1, D = n + 2, M = r^(n−1)(1 + 2e^f r₊r₋)/2, which on the apparent horizon (r₊ = 0) is r^(n−1)/2.

## Question and plan

#41 followed the Misner–Sharp mass on the apparent horizon of the symmetric ghost-pulse family S at D = 4 and found it settles at 0.22308 a, 9.4 time units after formation (e^{−f} = 1.57e6 on the
horizon); #253 found family G (ghost pulse tuned to p*ₕ plus a fixed normal pulse B = 0.1 on the same ray) settles 0.0125 a higher and depends on δ. [ST17] give a threshold mass at n = 5, 6 (their
Table I). This task runs #41's chain at D = 5, 6 (n = 3, 4) for S and G at #40's three h per D, with M = r^(n−1)/2 on the horizon, and a planted exact Tangherlini through the same chain.
Acceptance (the issue's, each can fail): the planted mass is recovered at second order; M_AH(x⁺) converges at second order at three h up to a declared limit; the settled values are compared with
[ST17]'s rows in one unit with the conversion shown; G against S per D with the δ dependence. The coordinator added (hc, 2026-11-27): report whether M_AH's convergence reaches #226's constraint-roundoff
floor (D = 6 at the finest h).

## Declared parameters

| quantity | value |
|---|---|
| dimension, families | D = 5, 6 (n = 3, 4); S and G of #40 (`threshold.family`: S = symmetric ghost pulse; G = ghost pulse A on field 0 plus normal pulse B = 0.1 on field 1, both on the + ray, centre 3, width 0.5, one-sided) |
| h | D = 5: 0.0070710678118654745, 0.0035355339059327372, 0.0017677669529663686. D = 6: 0.005, 0.0025, 0.00125. These are the strings of #40's job.log and equal `threshold.CRIT["H"]` bit for bit (checked in RC1) |
| p*ₕ | (lo + hi)/2 of #40's `D<D>_<fam>_h*/summary.json` (negative-mass-raw `I40-dh610`, last commit 99423f6e), hashes in `runs/pstar_D*_k*.json`; not bisected again. **One exception:** #40 has no run of G at D = 6, h = 0.00125 (about 4 h); it was bisected here (below) |
| δ | 1e-6 and 1e-8, A = p*ₕ − δ (collapse side); the expansion side p*ₕ + δ must expand. At δ = 1e-8 the amplitude is bit for bit #40's stall run (`stall_e` = 8) |
| chain | #41's: F₁ = 1.5, W₁ = 2.4 (level 1 is W₁ wide in x⁻, each box Nc = 2W₁/h cells rounded to a multiple of 4, width h/2^k at level k), r_cut = 0.05, trapped tolerance 1e-2, first trapped cell of #40 as the start, dm = 3. **Changed from #41 (see below): K = 28, dxp = 14** |
| **limits** | **Primary: e^{−f} on the horizon ≤ F₁ 2^28 = 402 653 184 (K = 28).** #41's 1 572 864 (K = 20) is read from the same series, cut at its last column with e^{−f} < 1 572 864 (a bit-identical prefix, check PFX), and every limit check is made at both. The quoted settled value is the K = 28 plateau |
| rectangle X | #40's: S 18 (D = 5), 15 (D = 6); G 22 (D = 5), 28 (D = 6). Rows: first trapped row + 3 + Nc h/4; columns: first trapped column + 14 |
| settled value | M_settled := plateau mean of M_AH over the last 1.0 of x⁺ (#41's `settled_summary` `plat1`), finest h, δ = 1e-8 |

p*ₕ used (D = 5: S 2.884790369034818e-4, 7.209092301764032e-5, 1.8020931233877496e-5; G 1.1233007374976298e-2, 1.0819117823594411e-2, 1.0715683256832448e-2; D = 6: S 1.1155147989984474e-3,
2.778388367505614e-4, 6.939553437860014e-5; G 1.2657678967584046e-2, 1.108797761415474e-2, 1.069693394962485e-2). Brackets hi − lo are 9.1e-15 (S) and 5.7e-15 (G), except D = 5, G, h = 0.00707 (2.9e-12, #40's bisection
ended on "static through X").

### The bisection of p*ₕ for G at D = 6, h = 0.00125 (the one input not from #40; the coordinator's ruling, hc 2026-11-27)

`scripts/bisect_pstar.py`: #40's own `threshold.bisect` and `threshold.point` unchanged, #40's bracket (0.005, 0.03) for G, X = 28.0, tolerance 1e-14, h = 0.00125 as `threshold.CRIT["H"][4][2]`; bisection
only (no series, no stall run). Machine dh610-fedora, code commit f8722437 (threshold.py, dn.py, checks.py unmodified), started 2026-11-27 18:39:21, 44 runs, 2569 s wall, one thread. Result in
`runs/pstar_D6_G_k2.json`, points in `runs/pstar_D6_G_k2.points.jsonl`, log `runs/logs/bisect_pstar_D6_G_k2.log`: lo = 0.010696933949622008, hi = 0.010696933949627691 (hi − lo = 5.7e-15), p*ₕ = 0.01069693394962485.
The three p*ₕ of G at D = 6 (0.012657679, 0.011087978, 0.010696934) have differences 1.5699e-3 and 3.911e-4, ratio 4.014. This overlaps #228 (G at D = 6 at its third resolution): the value is stored so that #228 can reuse it.
#40 has no stall run (event cell, M_hor) for this h, so RC2 and RC3 do not apply to k = 2 of G at D = 6.

## Changes made during development (before this declaration)

1. **Limit.** #41's e^{−f} = 1.57e6 was the plan (the coordinator approved it). The development runs (`dev/d04/analyze_2.log`, `dev/d06`, `dev/d07`) showed #41's RC8 (settled) fails at it: D = 6 S plateau change 4.0e-4 and
   flux 6.3e-5, D = 5 S flux 1.5e-5, against bars 1e-4 and 1e-5. The reason: the x⁺ span from formation to the limit shrinks with D (D = 4: 9.4; D = 5 S 6.1, G 8.1; D = 6 S 4.6, G 8.5; stretching rates d ln e^{−f}/dx⁺ 2.7, 1.9, 3.6, 1.8), so
   the last 1.0 still holds the decay tail. M_end itself is the same at K = 20, 24, 28 to ≤ 1.3e-5 (`dev/d06`), and the series are bit-identical prefixes. The coordinator ruled (hc): run everything at K = 28 (e^{−f} = 4.0e8, dxp = 14),
   evaluate RC5, RC6, RC8 at both limits, quote the K = 28 plateau, report the 1.57e6 reading and its RC8 verdict beside it as it comes out (RC8a is expected to fail and is reported as such).
2. **RC7 at the finest h only** (coordinator's ruling). At D = 6 S the δ-difference falls with h (3.9e-4, 9.3e-5, 2.4e-5, observed orders 2.05, 1.94): truncation at the coarse h. The three values and orders are printed.
3. **RNR** is posed differently from #253's (which failed): the dose at which the noise must respond is 2^20 × 2^−52, not 64 × 2^−52 (#253's dose scan: the scatter did not respond to 64×, and was 80× larger at 2^−32); the bar is 10×.
4. **Bracket bar** 1e-11 (RC1), because #40's G at D = 5, h = 0.00707 ended at 2.9e-12; every δ is at least 1e3 times that.
5. Two slips in development, kept in `dev/`: the first noise queue passed the 2^20 dose as `%g` (1.04858e+06, not 1048576.0) and was stopped and moved to `dev/_d05_aborted_noise_dose_format`; the first analysis (`dev/d04/analyze_1.log`)
   looked for run folders named `1e-06` while the lane script writes `1e-6`.
6. The planted cases' (λ, kp) were set from the development series (settled r_AH and late d ln e^{−f}/dx⁺ of the real S and G runs, rounded); their bars are 15 times the observed errors (below).

## What the driver adds to #41's code

- `run_real_d`: #253's `run_real_g` with n and the family as arguments (`threshold.family`, `threshold.point` with #40's rectangle, `settled_mass.chain`, first trapped cell as start). `settled_mass.track` is #253's wrapper (the normal field's φ₊ on the horizon).
- General n: the first law along the horizon, dM/dx⁺ = (r^n/n) e^f r₋ (φ₀₊² − φ₁₊²) (ghost with the sign of #41's `flux_integral`, normal field opposite; FLX tests it on planted series).
- `tang_exact`: the exact Tangherlini (n = 3, 4; r_h = λ, M = λ^(n−1)/2) in closed form (tortoise coordinate; Y(r) = −UV in elementary functions), in the gauge x⁻ = x_h + λU, V = κ e^{kp(x⁺−xs)}/(λ kp) so that the horizon is
  x⁻ = x_h and e^{−f} on it is e^{kp(x⁺−xs)} (the stretching of the real runs); D = 4 is #41's `schw_exact`. It shares no code with `dn.kruskal_exact`, against which it is checked (PT0).
- The conversion to [ST17]'s unit and the report tables.

## Checks, bars, and what is declared

A failed check is reported as not met. The bars are #41's and #253's where those existed.

| id | check | bar |
|---|---|---|
| CFG | `CRITD` equals the declared chain; #40's X of S and G at D = 5, 6 equal the declared | equal |
| FLX | the general-n horizon flux on planted series (ghost only, normal only, equal), n = 3, 4 | 1e-12 |
| PT0 | the closed-form Tangherlini against `dn.kruskal_exact` (r and f) at 400 points with r in [0.4, 5.9]; on the planted horizon r = λ and e^{−f} = e^{kp(x⁺−xs)} | 1e-9 |
| PT1-⟨D⟩⟨S\|G⟩ | exact Tangherlini through the chain at h = 2h₁, h₁, h₂, h₃ of #40's set, K = 28: max \|M − λ^(n−1)/2\| at h₃, observed order at the three halvings, status "limit", F reached ≥ F_max/2. Cases (λ, kp, x_h): D = 5 S-like (0.54, 2.7, 5), G-like (0.73, 1.9, 5); D = 6 S-like (0.60, 3.6, 5), G-like (1.19, 1.75, 5) | error ≤ 3e-4 M_exact; orders in [1.75, 2.25] |
| CONV | E = (D − 2) V_{D−2} M (κ² = 1, V the unit-ball volumes π, 4π/3, π²/2): the static throat (M = 1/2) gives [ST17]'s E_f/a₀ = 3.14, 6.28, 9.87 | 0.005 |
| A4P | the printed A₄ = π²/Ω⁴ gives E_throat = 2π² = 19.74 at n = 6, twice the table's 9.87 | ratio 2 ± 0.01 |
| CMPT | the G-against-S verdict function on planted offsets | half the bar "equal", three times "differs" |
| PL1–PL3 | #41's planted Schwarzschild, Roberts and level-0 identity at D = 4 through this driver | printed lines equal #41's output of record |
| L0ID-⟨D⟩⟨fam⟩ | level 0 of the chain (no zoom) equals `dn.evolve` bit for bit (nodes, dead flags, first trapped cell), k = 0, δ = 1e-6 | equal |
| PFX | runs to K = 20 and K = 24 (D = 5, 6 × S, G, k = 0, δ = 1e-8, same dxp) equal the K = 28 series cut at their limit bit for bit (M, x⁺, x⁻, r, e^{−f}); M_end at the three limits is printed | equal |
| RC1-⟨D⟩⟨fam⟩ | p*ₕ: hi − lo, h as the job takes it (equal to `threshold.CRIT["H"]` and #40's job.log), fate(p*ₕ ∓ 1e-10) = collapse/expansion on this machine, all three h | hi − lo ≤ 1e-11 |
| RC2 | fates at p*ₕ ∓ δ (all h, both δ); first trapped cell and its time at δ = 1e-8 against #40's `stall.json` (where #40 has the job) | cell equal; \|T − T₄₀\| ≤ √2 h |
| RC3 | M_AH at the first trapped cell against #40's M_hor at p*ₕ − 1e-8 | ≤ 2e-3 |
| RC4 | first law on the horizon, both fields, first trapped cell to e^{−f} = 20 | relative ≤ 2e-2 |
| RC5 | every run ends at the limit (status "limit", F_max/2 ≤ F_end < F_max), ≥ Nc/8 cells from the box edges, no gaps; at K = 28 and, as RC5a, at 1 572 864 | all six runs |
| RC6 | second order of M_AH(x⁺): max \|M_h − M_h/2\| over windows of x⁺ − x⁺_f [0, 1.5], [1.5, 3], [3, end], cubic splines, both δ, three h; at K = 28 and, as RC6a, at 1 572 864 | observed order in [1.5, 2.5] |
| RC8 | M_AH has settled at the limit: plateau mean over the last 1.0 differs from the previous 1.0 by ≤ 1e-4 and the mean horizon flux (both fields) over the last 0.5 is ≤ 1e-5, every run; at K = 28 and, as RC8a, at 1 572 864 | as stated |
| RC7-⟨D⟩S | the settled value of S does not depend on δ: plateau means at δ = 1e-6, 1e-8 differ at the finest h (the three values and orders are printed) | ≤ 1e-4 |
| DEP-⟨D⟩G | the δ dependence of G, plateau(1e-8) − plateau(1e-6), is the same at the two finest h to 10 % (a property of the solution, not of the resolution), or both are ≤ 1e-4 | as stated |
| TRK-⟨D⟩G | the wrapper's recomputed φ₊ of the ghost equals `settled_mass.track`'s, and the normal field's φ₊ on the horizon is nonzero | relative 1e-12 |
| RN0-⟨D⟩⟨fam⟩ | the noise-0 run reproduces the run of record bit for bit | bit-identical |
| RNR-⟨D⟩⟨fam⟩ | the scatter responds to a large noise: nonzero at 2⁻⁵², and at 2²⁰ × 2⁻⁵² at least 10 times that, every window and h | as stated |

IDs are suffixed by D and family (`RC6-5S` is D = 5, S). Expected (not predicted for the others): RC8a fails at every case (development: D = 5 S flux 1.5e-5, D = 6 S 6.3e-5, D = 5 G 1.2e-5, D = 6 G 5e-5 to 7e-5); it is reported, not loosened.
All other checks pass in development.

## The comparisons (declared before the runs; reported, not pass/fail except where a check is named)

- **G against S per D**, finest h, δ = 1e-8: M_G and M_S are plateau means. Error bar of M_G, three kinds kept separate and summed linearly as #253 did: h (finest pair), δ (|plat(1e-6) − plat(1e-8)|, a physical dependence,
  not an error), machine to machine 2e-5 (#41's review at D = 4, not remeasured). Verdict "equals" iff |M_G − M_S| ≤ the sum, else "differs"; Richardson values (second order, three h) and G/S printed. The δ dependence is
  printed at the three h with observed orders (DEP). G's formation value (first trapped cell) and the drift of #255 are reported beside it, not tested.
- **[ST17]** (arXiv:1706.02070 read from the TeX source; the PDF and source hashes equal #41's `papers.sha256`): Table I GR rows, E_f/a₀ = 3.14, 6.28, 9.87 for n = 4, 5, 6, "evaluated at x⁺ = 5", their (2.47)
  E_n = (n−2)A_{n−2}/(2κ²Ω){k + 2e^f ϑ₊ϑ₋/(n−2)²} with Ω = 1/r, κ² = 1 (α_GR = 1, α_GB = 0). Conversion: E = c_D M with c_D = (D−2)V_{D−2}, M = r^{D−3}(1 − (∇r)²)/2, V_2 = π, V_3 = 4π/3, V_4 = π²/2 (the unit-ball
  volumes, which are what the printed A₂, A₃, A₅ are; the printed A₄ = π² is twice V_4). Table: formation (first trapped cell) and settled M of S and G, E = c_D M, E/E_throat = 2M, against [ST17]'s E_f and E_f/E_throat.
- **Roundoff floor** (#226 at D = 5, 6): ulp-noise runs, relative noise u·ξ·2⁻⁵² (ξ uniform in (−1, 1)) on every node of both rays (`dn` rays, `add_noise` of #253), h = the two finest per D, δ = 1e-8, K = 28, runs (u, seed):
  (0, 1), (1, 1), (1, 2), (1, 3), (64, 1), (2²⁰, 1). Report: max |M_noisy − M| over the three windows against the h-difference E between that h and its coarser neighbour, ratio ≥ 1 "reached", 0.1 to 1 "approached", < 0.1 "not reached"
  (as #253). What it measures: the scatter between roundoff realizations of the run, not a calibrated roundoff response (#253's RNR failure); it is the same kind of number as #41's machine-to-machine 2e-5.

## Run plan (commands)

From `notes/wormhole_evolution/` of the worktree: `python3 settled_mass_d56.py pstar --n=N --fam=F --k=K --out=RAW/runs` (K = 0, 1, 2 coarse to fine; G at D = 6 has k = 2 from `scripts/bisect_pstar.py`);
`python3 settled_mass_d56.py job --n=N --fam=F --k=K --delta=D --out=RAW/runs/<tag> --pstar=RAW/runs [--K=K --noise=U --seed=S]`, queued by `scripts/lane2.sh` (four lanes at most; never overwrites: an existing folder is moved to
`*_aborted_<time>`; each job under `timeout 10800`); `python3 settled_mass_d56.py analyze --raw=RAW > settled_mass_d56_output.txt` (from the notes directory); mutated analyses by `scripts/mutlane.sh`.
Run folders: `runs/D<D>_<fam>_k<k>_d<δ>` (the 24 runs), `..._K20`, `..._K24` (PFX), `..._rn_u<u>_s<seed>` (noise). Every `job.log` is kept.

## Mutations (computed in development, `dev/mut/`; the case column is the `--cases=` of the mutated analysis)

MUTATIONS_PLACEHOLDER
