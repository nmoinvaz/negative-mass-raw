# I266-mac: the settled mass of family G against the normal amplitude B (D = 4), #41's chain, with #225's static member at departure

Machine: the coordinator's Mac (Apple M5, 10 cores, macOS, shared and heavily loaded), Python 3.14.7, numpy 2.5.4, scipy 1.18.1, numba 0.68.1, one thread per process (`NUMBA_NUM_THREADS=1`),
`nice -n 10`, at most 2 processes. Runner negative-mass-mac-i266 on the claude-me2 account. Issue https://github.com/nmoinvaz/negative-mass/issues/266 ("Measure family G's settled
mass against the normal amplitude B"). Worktree `~/Source/negative-mass-i266`, branch `wip/i266-mass-vs-B`, from main at 817181d. Code: `notes/wormhole_evolution/settled_mass_b.py`, a thin driver that
imports #41's `settled_mass.py`, #253's `settled_mass_g.py`, #40's `threshold.py`, #225's `throat_locus.py` and #39's `dn.py` unchanged. This README is written after the development runs
(`dev/`) and before any run of record (`runs/`); nothing above the line "Changes made after this README" is changed after the first run of record. Status words as in AGENTS.md: every mass
and every member parameter here is *numerical evidence*. No sentence claims novelty.

## Question and plan

Family S settles at M_AH = 0.22309 a (#41). Family G of #40 (a ghost pulse A = p*ₕ − δ plus a fixed normal pulse B = 0.1 on the same ray) settles at 0.2355 a at δ = 1e-8 (#253), and its
near-critical state is the static member r_th = 1.0028 a, γ₁ = 0.048 (#225). That the settled mass follows that member is a conjecture. This issue runs #41's chain for G at B = 0, 0.025, 0.05,
0.1, 0.2 and for family O, each with its own bisected p*ₕ, measures the member (r_th, γ₁) at departure for each by #225's method, and sets M(B) against them.

## Declared parameters (the chain is #41's, unchanged; none of this is changed after a development run without a ruling)

| quantity | value |
|---|---|
| dimension, units | D = 4 (n = 2), 8πG = 1, a = 1 the throat radius of the initial static wormhole; t = (x⁺ + x⁻)/√2 |
| members | O (one-sided ghost pulse, `threshold.family("O", A)`), G with the normal amplitude B = 0, 0.025, 0.05, 0.1, 0.2 (`threshold.CRIT["G_B"]` set to B; ghost pulse A on field 0 and normal pulse B on field 1, both on the + ray, centre 3, width 0.5). **Added by this note:** G with B = 0.125 (supplementary; the stall persists to B = 0.15, dev03) |
| h | 0.01 and 0.005 (the issue's) and 0.02 (added, so that the order can be read from three h); the h passed is the float of the literal `0.02`, `0.01`, `0.005` of #40's job logs |
| p*ₕ | bisected for each member and each h: `threshold.bisect` on `threshold.point` (rectangle X = 28, #40's), stop at hi − lo ≤ 1e-14, p*ₕ = (lo + hi)/2. Brackets (lo collapse, hi expansion, checked at run time): O, G(B = 0), G(0.025): (−0.01, 0.01); G(0.05): (0, 0.02); G(0.1): (0.005, 0.03) = #40's; G(0.125): (0.01, 0.05); G(0.2): (0.03, 0.1) |
| δ | 1e-8, A = p*ₕ − δ (collapse side); p*ₕ + δ must expand |
| chain | #41's: F₁ = 1.5, K = 20, W₁ = 2.4, r_cut = 0.05, trap tol 1e-2, dxp = 12, dm = 3; limit e^{−f} ≤ F_max = F₁ 2^K = 1 572 864 on the horizon; first trapped cell of #40 |
| settled mass | plateau mean of M_AH over the last 1.0 of x⁺, as #253; M = r_AH/2 |
| member pair | the pair A = p*ₕ ∓ 1e-8 through `throat_locus.sweep` (`dn.row_step` unchanged, triangle t ≤ 34, profile slices every 0.5 in t from 3); its collapse side is the run of record's amplitude |
| departure | t_dep(ε): first t ≥ 6 at which the unstable mode's part \|r_min(p*ₕ + δ) − r_min(p*ₕ − δ)\|/2 reaches ε of the tuned (mean) throat radius; primary **ε = 1e-3**, alternative ε = 1e-2 |
| member at departure | #225's `slice_masses` and `fit_asym` (radii 1.25, 1.5, 2, 3, 4 r_th) on the pair's **mean** profile (r, f, r₊, r₋ averaged node by node: the unstable mode is odd in the pair), r_th the mean of the two locus minima; s_th linearly interpolated in t between the two slices that bracket t_dep; γ₁ = s_th/√(1 − s_th²) (`throat_locus.member_report`). #225's own reading (the collapse side alone) is printed beside it |

Readings of the issue that are mine, stated so the coordinator can overrule them:

- "bisect to 1e-14 relative, as #40": #40's rule is hi − lo ≤ 1e-14 (absolute); I use it. The brackets reached are 6e-15 to 9e-15, which is 1e-9 (B = 0) to 1e-13 (B = 0.2) of p*ₕ, 1e-6 of δ.
  A bracket that is 1e-14 of p*ₕ itself is below the roundoff floor of the fate (about 1e-12, #40).
- "second order" needs three h; h = 0.02 is added to the issue's two. The two finest h, 0.01 and 0.005, are the issue's pair.
- "γ₁ and r_th measured at departure": the issue gives no definition of departure; the one above is mine. The numbers at ε = 1e-2 are reported too.

## What the development runs found (dev/, before this README)

| run | what | result |
|---|---|---|
| dev00, dev01 | fates against A at B = 0 … 0.2 (h = 0.02) | p*ₕ ≈ 1e-3, 4e-3, 1.5e-2, 6.8e-2 at B = 0.025, 0.05, 0.1, 0.2; brackets above straddle |
| dev02 | B = 0.2 near p*ₕ (h = 0.02) | **no stall**: collapse at T = 5.30 for every A in [0.0682, 0.0683054], expansion at T = 12.2 for every A in [0.068306, …]; T does not grow as p* is approached (a prompt threshold) |
| dev03 | T(p*ₕ ∓ 10^−e) against B (h = 0.02) | B = 0.1, 0.125, 0.15: T gains 4.1, 4.2, 4.5 per side from e = 6 to 8 (stall); B = 0.175, 0.2: no gain (prompt) |
| pipeline at B = 0.2 | the chain | stops at level 0, "horizon lost" at x⁺ = 4.53, e^{−f} = 0.77 (< 1), after 28 columns; the first trapped cell has r = 1.11 a, M = 0.556 a: a direct collapse, not a horizon that grows out of a stall |
| pipeline at B = 0.15 | bisection, chain | the rectangle X = 28 ends the bisection at hi − lo = 9e-14 ("static through X"); the chain ends by "columns exhausted" at e^{−f} = 9.3e5 to 9.6e5 (dxp = 12 is #41's declared value). Not run for the record; a recommended task |
| dev04 | planted static member as profile slice, h = 0.02, 0.01, 0.005, γ₁ = 0 … 0.3 | γ₁ to 3e-6, r_th to 1e-6 (first version: 3e-4 to 2e-3 from a coarse table: fixed before this README) |
| dev05 | the static Ellis wormhole as data (A = 0, B = 0) | not static on the grid: collapses at T = 7.6, 8.8, 10.0 (h = 0.02, 0.01, 0.005); `run_real_g` refuses it (fates −1, −1) |
| dev (analysis) | the 21 checks on 21 development runs (h = 0.02, 0.01, 0.005 for all seven members) | all pass, after PO was scoped to the stalling members (B = 0.2: order 2.52, a prompt threshold) |

The first development launch of the member stage was stopped (my own processes, by PID) because the stored rows lacked the radii the analysis refits with; its logs are in `dev/aborted/`.

## Checks, bars, and the mutations that must fire

A failed check is reported as not met; nothing here is changed after a run of record. "Stalling members": O, G(B = 0, 0.025, 0.05, 0.1, 0.125). B = 0.2 is a prompt threshold: BR, STL and EVT apply to it; the chain, its checks and the member checks do not (its chain status is reported). Bars of the checks that repeat #253's are #253's.

| id | check | bar |
|---|---|---|
| CFG | `settled_mass.CRIT` equal #41's declared chain; X = 28 for G and O; `threshold.CRIT["G_B"]` = 0.1 at import | equal |
| PMEM | planted: exact static ghost wormholes of known γ₁ = 0, 0.00293, 0.0483, 0.0755, 0.3 (GGS09a's closed forms: r_th, s_th, end masses m₊, m₋) as profile slices of the sweep (t = 13, h = 0.01, 0.005), through `slice_masses`, `fit_asym`, the parabolic throat minimum and `asym_masses` | γ₁ ≤ 1e-5, r_th ≤ 1e-6, m± ≤ 1e-4 (observed 1e-6, 1e-8, 2e-6) |
| PDEP | planted growing pair (odd part q₀ e^{λt}) through `departure_time` at ε = 1e-3, 1e-2, 1e-1 | \|t_dep − exact\| ≤ 2e-5 (observed 6e-6: the linear interpolation of an exponential) |
| PREL | planted relation M/r_th = M₀ + aγ₁ + bγ₁² through the leave-one-out test | every held-out point ≤ 6e-5 |
| BR | bracket ends are collapse and expansion; replay of the bisection equals lo, hi; hi − lo ≤ 1e-14; not stopped by "static through X"; h_arg is the repr of the float | all 21 jobs |
| P40 | B = 0.1: p*ₕ on this machine equals #40's `D4_G_h*` (dh610); the h of its job.log equals the h passed | ≤ 1e-10 (observed 5e-14) |
| GO | G with B = 0 and O: same p*ₕ bit for bit and same first trapped cell, every h | equal |
| PO | p*ₕ second order at h = 0.02, 0.01, 0.005, every stalling member | observed order in [1.75, 2.25] (#40's band) |
| STL | T(p*ₕ ∓ 1e-8) − T(p*ₕ ∓ 1e-6) ≥ 2.0 on both sides (stall; expected 3.9) or not (prompt); equals the declared class: stall for O and B ≤ 0.125, prompt for B = 0.2 | every h |
| EVT | chain's first trapped cell = the pair's collapse-side event (same amplitude); fates collapse at p*ₕ − δ, expansion at +δ; B = 0.1 equals #40's `stall.json` | equal |
| RC4 | first law on the horizon, both fields (ghost + normal, #253's `flux_integral_g`), to e^{−f} = 20 | relative ≤ 2e-2 |
| RC5 | every run of a stalling member ends at the declared limit (status "limit", F_max/2 ≤ F_end < F_max), ≥ Nc/8 cells from the box edges, no gaps | all 18 |
| RC6 | M_AH(x⁺) second order at h = 0.02, 0.01, 0.005, windows x⁺ − x⁺_f in [0, 1.5], [1.5, 3], [3, end] | observed order in [1.5, 2.5] (#253's) |
| RC8 | settled: plateau mean over the last 1.0 differs from the previous 1.0 by ≤ 1e-4, horizon flux (both fields) over the last 0.5 ≤ 1e-5 | every run |
| RH | the settled value at two h: \|plat(0.01) − plat(0.005)\| | ≤ 5e-5 (observed ≤ 1.5e-5) |
| RB0 | **B = 0 (G with a zero normal pulse, and O) reproduces S's 0.22309** at h = 0.02, 0.01, 0.005 | ≤ 6e-4 (the issue's) |
| RB10 | B = 0.1 reproduces #253's plateau means (I253-rpi5, δ = 1e-8) at every h | ≤ 1e-4 (observed 1.5e-5) |
| MB0 | B = 0 (G, O): the member at departure is the symmetric one | \|γ₁\| ≤ 2e-5, \|r_th − 1\| ≤ 1e-4 (observed 2e-7, 3e-6) |
| C225 | B = 0.1: r_th and s_th of the pair's mean at t = 12, 13, 14 equal #225's printed table | r_th ≤ 3e-4, s_th ≤ 1e-4 (observed 1.2e-4, 3e-5; #225 prints four digits) |
| HST | the member at departure at the two finest h agree, every stalling member | γ₁ ≤ 5e-5, r_th ≤ 1e-4 (observed 1e-7) |
| REL | M/r_th − M₀ = aγ₁ + bγ₁² (M₀ = B = 0's plateau at h = 0.005), leave one out over B = 0.025, 0.05, 0.1, 0.125 at h = 0.005, γ₁ and r_th at ε = 1e-3 | every held-out point ≤ 6e-5 |

REL is not a blind test: its form (the r_th scaling, the quadratic in γ₁) was chosen after the development runs at h = 0.02 and 0.01 (all seven members); the runs of record at h = 0.005 reproduce
the same members and so test its stability and not its form. It is also a relation along a one-parameter family in B: it does not separate the dependence on γ₁ from that on r_th, and is
no test of the conjecture that M follows the member. The note says so.

Mutation targets (each computed in the development runs `dev/mut_a/` on the development set before being declared here; `analyze --mutate=NAME`; the declared set is exactly the checks that fire):

| mutation | what it breaks | checks that fire (declared) |
|---|---|---|
| `crit_dm` | dm = 2.0 in the chain constants | CFG |
| `bisect_early` | the bracket after 30 bisection steps in place of the last | BR |
| `pstar_h_swap` | #40's p*ₕ of the next h | P40 |
| `go_h` | O at the next h against G(B = 0) | GO |
| `pstar_h1` | p*ₕ scaled by h₁/h (a first-order seed) | PO |
| `stl_flat` | the lifetimes at 1e-6 and 1e-8 taken equal | STL |
| `evt_side` | the pair's expansion-side event in place of the collapse-side one | EVT |
| `flux_sign` | the horizon flux with the wrong sign | RC4 |
| `short_limit` | K = 12: the chain stops at e^{−f} = 6144 | RB10, RC5, RC8 |
| `no_zoom` | K = 0: a uniform grid, no zoom levels | RB0, RB10, RC4, RC5, RC6, RC8, REL, RH |
| `mass_exponent` | M = rⁿ/2 in place of rⁿ⁻¹/2 | RB0, RB10, RC4, REL |
| `family_B` | B = 0.11 in place of 0.1 (the chain refuses: fates at p*ₕ ∓ δ) | EVT, RB10, RC5, RC6, RC8, REL, RH |
| `b_offset` | B = 0.05 in place of 0 (the chain refuses) | EVT, RB0, RB10, RC5, RC6, RC8, REL, RH |
| `h_plat` | the plateau at h = 0.02 in place of 0.005 in RH | RH |
| `rth_collapse_side` | r_th of the collapse side alone in place of the pair's mean | MB0, REL |
| `asym_sign` | #225's `fit_asym` with the two sides swapped | C225, PMEM |
| `dep_eps` | ε × 10 in `departure_time` | MB0, PDEP, REL |
| `eps_h` | ε × 100 at the finest h only | HST, MB0, REL |
| `rel_perm` | M of the members rolled by one in REL and PREL | PREL, REL |

## The planted member, and the chain started from one

- *Through the extraction (PMEM, above):* an exact static ghost wormhole of known γ₁, r_th and end masses, as the node values of a slice, through #225's member code. Known: γ₁, r_th, m±. Recovered to 1e-6.
- *Through the chain: cannot be done.* A static member has no trapped surface, so the chain has no first trapped cell and no horizon to follow (dev05: the static Ellis wormhole as data is not even static on the grid;
  it collapses at T = 7.6 to 10.0 because of the truncation error, and `run_real_g` refuses it). The chain starts at a horizon that the member's unstable mode forms; the settled mass of that
  horizon is the unknown, and no planted member has a known one. The planted truths of the chain are #41's PL1 (exact Schwarzschild) and PL2 (exact ghost solution), run through the same code in
  #253 and not repeated here; RB0 and RB10 repeat the chain's reproduction of S (0.22309) and of #253 (0.2355).
- A member as characteristic data (the asymmetric static wormhole as the initial rays) is #254's, not built here.

## Not run, and why

- B = 0.15 (stall, but dxp = 12 ends the chain at e^{−f} ≈ 9e5 and X = 28 ends the bisection): dev logs only. B = 0.175 and above: no stall (dev03).
- #41's AN control and h = 0.0025: not asked; the chain is #253's and its controls are RB0, RB10, RC4 to RC8.
- The δ dependence of M(B): #253 has it at B = 0.1 (+5.7e-4 from 1e-6 to 1e-8); #267 has it against the member.
- The noise runs of #253: its scatter (6.6e-6 at h = 0.005, 2.5e-5 at h = 0.01) is quoted, not remeasured.

## How to run

```
cd ~/Source/negative-mass-i266/notes/wormhole_evolution          # numba and the venv: ~/Source/negative-mass/.venv/bin/python
scripts/run_jobs.sh ROOT jobs.txt LANE NLANES                    # in this folder: pstar, chain, member for each line "FAM B H" of jobs.txt (O has B "-")
python settled_mass_b.py analyze --raw=ROOT [--mutate=NAME]      # ROOT/runs/<tag>/h<h>/{pstar,chain,member}
```

Layout: `runs/<tag>/h<h>/{pstar/{points.jsonl,summary.json}, chain/{series.npz,summary.json}, member/{member.json,locus.npz}, logs/}`, `mut/` (the analyses with a mutation), `dev/`, `scripts/`.

## Changes made after this README

### Amendment A1 (2026-11-27, coordinator's ruling by hc; made before any run of record was analysed)

The runs of record (`runs/`) are unchanged by it. The ruling: B = 0.2 is run as declared and reported as not applicable (a finding about G, not a failed check); B = 0.125 and h = 0.02 are supplementary,
labelled post hoc, and gate nothing; the note says where between B = 0.15 and 0.2 the stall disappears, if the runs bracket it.

- **Checks split.** Every check that covers B = 0.125 or h = 0.02 is split in two. The gated check covers the issue's members (O and G at B = 0, 0.025, 0.05, 0.1, 0.2) at the issue's two h (0.01, 0.005);
  the same check with the suffix `-ph` covers the rest, is printed as POST HOC, and does not set the exit code. Same bars. PO and RC6 read an order and need three h, so they exist only as `PO-ph`
  and `RC6-ph`; the gated "two h" statement is RH. REL is gated over B = 0.025, 0.05, 0.1 (bar unchanged, 6e-5) and `REL-ph` over B = 0.025, 0.05, 0.1, 0.125.
- **Known before the amendment was written:** on the development set REL over three B misses its bar (7.9e-5 against 6e-5: each held-out point is predicted from two others, and B = 0.1 is an
  extrapolation from B = 0.025 and 0.05), and `REL-ph` over four B passes (5.5e-6). The bar is not moved; REL is expected to be reported as not met.
- **New, post hoc, gating nothing:** `settled_mass_b.py stallscan --h=H --B=B1,B2,... --out=DIR` (p*ₕ to 1e-12 and the lifetime at p*ₕ ∓ 1e-6, ∓ 1e-8) for B = 0.15, 0.155, …, 0.175 at h = 0.02 and 0.01,
  to bracket where the stall ends; printed by `analyze`.
- **Mutation targets recomputed** on the development set with the amended analysis: the table above is replaced by the one below (dev logs `dev/mut_b/`). Code at aee454e.

| mutation | checks that fire (declared, amended) |
|---|---|
| `crit_dm` | CFG, REL |
| `bisect_early` | BR, BR-ph, REL |
| `pstar_h_swap` | P40, P40-ph, REL |
| `go_h` | GO, GO-ph, REL |
| `pstar_h1` | PO-ph, REL |
| `stl_flat` | REL, STL, STL-ph |
| `evt_side` | EVT, EVT-ph, REL |
| `flux_sign` | RC4, RC4-ph, REL |
| `short_limit` | RB10, RB10-ph, RC5, RC5-ph, RC8, RC8-ph |
| `no_zoom` | RB0, RB0-ph, RB10, RB10-ph, RC4, RC4-ph, RC5, RC5-ph, RC6-ph, RC8, RC8-ph, REL, REL-ph, RH, RH-ph |
| `mass_exponent` | RB0, RB0-ph, RB10, RB10-ph, RC4, RC4-ph, REL-ph |
| `family_B` | EVT, EVT-ph, RB10, RB10-ph, RC5, RC5-ph, RC6-ph, REL, RH |
| `b_offset` | EVT, EVT-ph, RB0, RB0-ph, RB10, RB10-ph, RC5, RC5-ph, RC6-ph, REL, RH, RH-ph |
| `h_plat` | REL, RH |
| `rth_collapse_side` | MB0, MB0-ph, REL, REL-ph |
| `asym_sign` | C225, PMEM, REL |
| `dep_eps` | MB0, MB0-ph, PDEP, REL, REL-ph |
| `eps_h` | HST, HST-ph, MB0, REL, REL-ph |
| `rel_perm` | PREL, REL, REL-ph |

REL fails without a mutation (above), so it is in every set where a mutation leaves it failing; the sets are exactly what fired on the development set.

### After A1: changes to reports only (no check, bar or mutation target changed)

- `stallscan`: its first launch stopped on an argument-parsing slip (logs in `logs/aborted/`), fixed and rerun; the scan reaches B = 0.15 to 0.175 at h = 0.02 and 0.01, B = 0.16 to 0.175 and (extra, `runs/stallscan_extra`) B = 0.15, 0.155 at h = 0.005.
  The report merges the files per h.
- Reports added to `analyze`: the member's end masses m± (`asym_masses`), and the relation REL with the member read at ε = 1e-2 (a guard was added to that line after the mutation `eps_h` stopped in it on the records: `mut/eps_h.log`
  crashed, `mut/eps_h.2.log` matches; the first record analysis `analyze_record.log` predates both reports, `analyze_record.2.log` is the output of record).
- Results of the runs of record: 37 checks (17 post hoc), all pass except the gating REL (7.9e-5 against 6e-5, expected from A1); 19 of 19 mutations fire exactly their declared sets.
- Figure: `plot_settled_mass_b.py` with the vendored `data_graphs.py` (the arriba graph-data skill's, unchanged) writes `settled_mass_b.svg`.
