# I283-mac: family G's settled mass on a second route to its member (normal pulse's width, centre), D = 4, δ = 1e-8: #41's chain, #225's member, #267's throat speed, P2 and P3 tested blind

Machine: the coordinator's Mac (Apple M5, macOS, shared and heavily loaded), Python 3.14.7, numpy 2.5.4, scipy 1.18.1, numba 0.68.1, one thread per process (`NUMBA_NUM_THREADS=1`), `nice -n 10`, at most 2 processes.
Runner negative-mass-mac-i283 on the claude-me2 account. Issue https://github.com/nmoinvaz/negative-mass/issues/283 ("Test G's settled mass on a second route to its member, blind"). Worktree
`~/Source/negative-mass-i283`, branch `wip/i283-second-route` from main (92bf50a). Code: `notes/wormhole_evolution/settled_mass_route.py`, a thin driver that imports #266's `settled_mass_b.py` and #267's
`settled_mass_member.py` (which import #41's `settled_mass.py`, #253's `settled_mass_g.py`, #40's `threshold.py`, #225's `throat_locus.py`, #39's `dn.py` and #255's `throat_drift.py`), all unchanged. It replaces
`threshold.family` in its own process by `route_family` (family G with the normal pulse's own centre and width). This README is written after the development runs (`dev/`) and before any run of record (`runs/`).
Status words as in AGENTS.md: every mass and every member parameter here is *numerical evidence*. No sentence claims novelty.

## Question and plan

#253 to #267: family G's settled mass at D = 4 rises with the member the data leave. #266 varies the normal amplitude B at δ = 1e-8: M/r_th − M₀ = a γ₁ + b γ₁² (a, b) = (0.2027, 0.8534) (**P2**) to 6e-6 over
four B. #267 varies δ at B = 0.1 and finds that P2 misses by up to 9e-4; a post hoc fit over nine points with the throat's speed ṙ_th = dr_th/dτ at departure as a third parameter,
M/r_th − M₀ = a γ₁ + b γ₁² + c ṙ_th, (a, b, c) = (0.2300, 0.2724, 0.7835) (**P3**), describes them to 4.3e-5. B moves γ₁, r_th, the tuned ghost amplitude and the remnants of the pulses together, and δ moves the member
along one curve in time. This issue changes the normal pulse in another way: its width (route W) or its centre (route C) at tuned amplitude B, so that γ₁ ≈ 0.012, 0.048, 0.075 are reached with r_th and ṙ_th different
from family B's, and tests P2 and P3 with their coefficients fixed by the issue, on points they were not fitted on. Six points, each at h = 0.01 and 0.005, p*ₕ bisected, #41's chain at p*ₕ − 1e-8, the pair
p*ₕ ∓ 1e-8, the member at departure and ṙ_th exactly as #266 and #267 read them.

## Declared parameters (the chain is #41's, unchanged; none of this is changed after a run of record)

| quantity | value |
|---|---|
| dimension, family, units | D = 4 (n = 2); family G of #40 with its ghost pulse (field 0, centre 3, width 0.5, amplitude A tuned) unchanged and the normal pulse (field 1, same ray) with its own amplitude B, centre x_c, width w; 8πG = 1, a = 1 the throat radius of the initial static wormhole; t = (x⁺ + x⁻)/√2 |
| the routes | **W**: x_c = 3.0, w = 1.0 (family B has w = 0.5). **C**: x_c = 4.0, w = 0.5 (family B has x_c = 3.0). B tuned per route and target (table below) |
| p*ₕ | bisected for each point and h: `threshold.bisect` on `threshold.point` (X = 28), hi − lo ≤ 1e-14, p*ₕ = (lo + hi)/2. Bracket: the six points start from the bracket scan's (the first two amplitudes of the development set's `points.jsonl`: a factor 2 wide), so the runs of record take the development set's bisection path and equal it bit for bit; the reproduction point starts from #266's (0.005, 0.03) |
| δ | A = p*ₕ − 1e-8 for the chain, the pair A = p*ₕ ∓ 1e-8 |
| chain | #41's through #253's `run_real_g`: F₁ = 1.5, K = 20, W₁ = 2.4, r_cut = 0.05, trap tol 1e-2, dxp = 12, dm = 3, limit e^{−f} ≤ F_max = 1 572 864 on the horizon; settled mass = plateau mean of M_AH over the last 1.0 of x⁺ (`summary_g`, key `plat1`), M = r_AH/2 |
| member, departure | #266's: `member_at` at ε = 1e-3 (the first t ≥ 6 at which the unstable mode's part \|r_min(p*ₕ + δ) − r_min(p*ₕ − δ)\|/2 reaches ε of the mean throat radius; #225's `slice_masses` and `fit_asym` on the pair's mean profile; r_th, s_th linearly interpolated in t; γ₁ = s_th/√(1 − s_th²)) |
| throat speed | #267's `speed_at`: dr_th/dτ of the pair's mean (r_th, τ of the locus), #255's local slope `rdot_local` (half window 0.5 in τ), interpolated to t_dep |
| **P2** | M_pred = r_th (M₀ + a γ₁ + b γ₁²), h = 0.005: M₀ = 0.223086, (a, b) = (0.2027, 0.8534), the digits of `settled_mass_member_output.txt`, "h = 0.005: #266's relation". h = 0.01 (post hoc): M₀ = 0.223095, (a, b) = (0.2029, 0.8502), same place |
| **P3** | M_pred = r_th (M₀ + a γ₁ + b γ₁² + c ṙ_th), h = 0.005, M₀ = 0.223086, (a, b, c) = (0.2300, 0.2724, 0.7835), `settled_mass_member_output.txt`, "fit over these 9 points" (the third line). Not refitted on the new points |
| the family-B reference | #266's stored runs (read only) at the same h: B = 0, 0.025, 0.05, 0.1, 0.125, the member at ε = 1e-3 and ṙ_th through the same code (`settled_mass_member.load266`) |

Readings of the issue that are mine, stated so the coordinator can overrule them:

- "p*ₕ by bisection": #40's, hi − lo ≤ 1e-14 as in #266 and #267. With the rule of BR below, a stop by "static through X" at hi − lo ≤ 2e-14 passes.
- "SEP: the new member's r_th or ṙ_th differs from family B's (interpolated at the same γ₁) by more than five times its own h difference": family B is interpolated in γ₁ over its five points (B = 0 … 0.125)
  by a piecewise-linear and by a PCHIP curve and the smaller of the two differences is used; the "h difference" is |x(h = 0.01) − x(h = 0.005)| of the same quantity of the new member; informative when γ₁
  lies inside family B's range (0 to 0.07545) and the r_th test or the ṙ_th test holds. A point that fails is "not informative" and is left out of P2 and P3.
- "the member at departure at the two h agrees to 1e-4 relative in γ₁, r_th": relative differences h = 0.01 against 0.005; "2e-5 absolute in ṙ_th": the same.
- "the reproduction of #266's B = 0.1 point to 1e-6 in M and the member": the point (B, x_c, w) = (0.1, 3.0, 0.5) through this driver, h = 0.005 gating (h = 0.01 post hoc): |ΔM| ≤ 1e-6 and |Δγ₁|, |Δr_th|, |Δṙ_th| ≤ 1e-6 (absolute), and p*ₕ to 1e-13 (#267's P266).
- "within 6e-5": |M − M_pred| for the plateau at h = 0.005; the bar is #266's and #267's.

## The routes and the six targets (development at h = 0.02, `dev/`)

Each route's parameter was chosen in development by the rule: among the candidates of that route that stall at all three γ₁, the one with the largest minimum over the three γ₁ of |ṙ_th − family B's at the same γ₁| (the speed is what P2 and P3 differ in). The rule uses r_th and ṙ_th only; P2 and P3 were not evaluated on the tuning points (one hand estimate of both at the (3.0, 0.7) point with B = 0.1209 was made from its printed numbers while the scan was running; it did not enter the rule) and the first full evaluation is the analysis of `runs_b` below.
Family B at h = 0.02: γ₁ = 0, 0.00293, 0.01184, 0.04831, 0.07544; r_th = 1, 0.99945, 0.99836, 1.00287, 1.01587; ṙ_th = −3.6e-6, −9.7e-5, −3.0e-4, +6.4e-5, +1.59e-3 (`dev/devsep_h0.02.txt`).

| candidate (x_c, w) | stall at all three γ₁ | ṙ_th − family B's at γ₁ = 0.012, 0.048, 0.075 | r_th − family B's | rule |
|---|---|---|---|---|
| (3.0, 1.0) | yes (B up to 0.19) | −2.0e-4, −7.3e-4, −1.07e-3 | −3.4e-3, −1.4e-2, −2.2e-2 | **route W** (min 2.0e-4) |
| (3.0, 0.7) | yes | −6.5e-5, −2.3e-4, −3.1e-4 | −1.3e-3, −5.2e-3, −8.1e-3 | |
| (3.0, 0.35) | yes | +2.8e-5, +1.1e-4, +1.5e-4 | +7.9e-4, +3.2e-3, +5.0e-3 | |
| (4.0, 0.5) | yes | −8.8e-5, −3.5e-4, −5.6e-4 | +1.3e-3, +3.5e-3, +3.8e-3 | **route C** (min 8.8e-5) |
| (3.5, 0.5) | yes | −4.3e-5, −1.7e-4, −2.5e-4 | +6.3e-4, +1.8e-3, +2.3e-3 | |
| (2.5, 0.5) | **no**: no stall at γ₁ = 0.075 (B = 0.151: "horizon lost" at x⁺ = 2.49) | +3.1e-5, +1.1e-4 | −7.7e-4, −3.4e-3 | |
| (2.0, 0.5) | no stall (B = 0.1: horizon lost at x⁺ = 2.47) | | | |

The six points (B tuned by a secant iteration in (ln B, ln γ₁) at h = 0.02 to within 0.4 % of the target; the development values at h = 0.02 are printed, the runs of record are at 0.01 and 0.005):

| point | target γ₁ | B | x_c | w | γ₁ (h = 0.02) | r_th | ṙ_th | M (plateau) | p*₀.₀₂ |
|---|---|---|---|---|---|---|---|---|---|
| W1 | 0.012 | 0.07905 | 3.0 | 1.0 | 0.01200 | 0.99496 | −5.05e-4 | 0.224425 | 0.005342294 |
| W2 | 0.048 | 0.1543 | 3.0 | 1.0 | 0.04797 | 0.98917 | −6.67e-4 | 0.231799 | 0.02023382 |
| W3 | 0.075 | 0.1909 | 3.0 | 1.0 | 0.07500 | 0.99362 | +4.95e-4 | 0.240838 | 0.03107103 |
| C1 | 0.012 | 0.0393 | 4.0 | 0.5 | 0.01199 | 0.99962 | −3.89e-4 | 0.225573 | 0.0008024925 |
| C2 | 0.048 | 0.07726 | 4.0 | 0.5 | 0.04801 | 1.00632 | −2.93e-4 | 0.236068 | 0.003020778 |
| C3 | 0.075 | 0.09576 | 4.0 | 0.5 | 0.07484 | 1.01937 | +9.93e-4 | 0.247333 | 0.004825716 |

The targets are inside family B's γ₁ range (0.00294 to 0.07545) and within 0.8 % of its nodes at B = 0.05, 0.1, 0.125 (0.01184, 0.04832, 0.07545 at h = 0.005; the interpolation error is then ≤ 2e-4 in r_th, 3e-5 in ṙ_th).

## What the development runs found (`dev/`, before this README)

| run | what | result |
|---|---|---|
| tuning | 18 points at h = 0.02 (`dev/logs/tune_*`), 8 candidates | table above; the plumbing reproduces #266's B = 0.1, h = 0.02 point (p*, M, member, ṙ_th) bit for bit through `route_family` |
| `runs_a` | the six points and (0.1, 3.0, 0.5), h = 0.01 and 0.005, bracket scan, whole job 32 to 92 s each | all stall (T gains 3.8 to 4.9 per side); γ₁ at h = 0.005 within 0.22 % of target; every chain ends at e^{−f} = 1.55e6 to 1.57e6 |
| `runs_a2` | (0.1, 3.0, 0.5) from #266's bracket (0.005, 0.03) | p*ₕ, M, member, ṙ_th equal #266's bit for bit at both h. With the bracket scan's path (`runs_a`) p*₀.₀₀₅ differs from #266's by 1.7e-15 and M by 1.5e-6 (the roundoff realization of the chain, #253's 6.6e-6 at h = 0.005), so REP fails there: **the reproduction point starts from #266's bracket** |
| `runs_b` | the dev set the analysis and the mutations were run on: the six points of `runs_a`, REP of `runs_a2` | the analysis (`ana_dev3.log`, exit 1): 32 checks, 3 gating fail: **HST (W1: γ₁ differs between the two h by 1.1e-4, bar 1e-4), P2, P3 (W3: +7.1e-5, bar 6e-5)**, and post hoc P2-ph |
| P2, P3 on the new members, h = 0.005 | M − predicted: P2: −1.4e-4, −5.0e-4, −7.5e-4, −6.5e-5, −2.7e-4, −4.6e-4 (W1, W2, W3, C1, C2, C3); P3: +1.4e-5, +4.7e-5, +7.1e-5, −3.8e-6, −1.4e-5, −2.2e-5 | P2 fails at every point and by 12 times the bar at W3 (all six negative); P3 holds at five points and misses W3 by 1.1e-5, **inside the roundoff scatter of the plateau (6.6e-6 at h = 0.005, #253)**. The runs of record are the development set's bisection path, so they reproduce these numbers; the residuals are not changed by this README |
| post hoc, seen in dev | a refit of the two forms over the four B and the six new points | P2's form: (0.197, 0.857), residual 4.0e-4, leave-one-out up to 6.0e-4. P3's form: (0.2269, 0.3294, 0.7096), residual 3.9e-5, leave-one-out up to 6.6e-5. Reported in the output as post hoc descriptions |
| SEP | all six informative | r_th and ṙ_th both separate by at least 1e3 times their h differences (r_th: 1.3e-3 to 2.2e-2 against ≤ 3.7e-6, ≥ 6e3 times; ṙ_th: 8.6e-5 to 1.07e-3 against ≤ 8.2e-7, ≥ 1e3 times) |
| HST | 7 points | γ₁ 1.1e-4 (W1), 5.1e-5, 4.5e-5, 1.5e-5, 1.1e-5, 9.2e-6, 2.2e-5; r_th ≤ 3.7e-6; ṙ_th ≤ 8.2e-7 |
| RH | \|plat(0.01) − plat(0.005)\| | 6.1e-6 to 1.4e-5 |
| the normal field's flux | share of the first law's flux to F = 20 | 2.6e-9 to 4.5e-8 of dM: RC4 cannot see the normal field (mutation `normal_drop` fires nothing; declared as a blind spot) |

Changes made to my own checks after the development data and before this README (the issue's four acceptance bars are untouched):

1. **BR.** C3 at h = 0.01 ends its bisection by "static through X" at hi − lo = 1.2e-14 (one step short of 1e-14; the lifetime at p*ₕ ± 6e-15 is past the rectangle). The first rule (stopped = None and hi − lo ≤ 1e-14) failed there. The declared rule accepts a stop by "static through X" at hi − lo ≤ 2e-14 (p*ₕ uncertain by 6e-15, 6e-7 of δ, below the roundoff of M). This relaxes BR; it does not touch P2, P3, HST, SEP or REP.
2. **REP's bracket**, above.
3. `fam_b` sorts family B by γ₁ (a mutated asymmetry sign reversed the order and the PCHIP stopped: the mutation `asym_sign` crashed once, `dev/mut_a/aborted_asym_sign.*` kept).

## Checks, bars, and what gates

Gating: the six points at h = 0.01 and 0.005 (REP: h = 0.005). Post hoc, gates nothing (`-ph`): REP at h = 0.01, P2 at h = 0.01. A failed check is reported as not met; nothing here is changed after a run of record.

| id | check | bar |
|---|---|---|
| CFG | `settled_mass.CRIT` equal #41's declared chain; X = 28; ghost pulse (3.0, 0.5); the (B, x_c, w) stored in each run's pstar and chain summaries equal the declared | equal |
| FAM0 | `route_family` with the default normal pulse equals `threshold.family("G", A)` at three A | equal |
| RUNS | every (point, h) has its pstar, chain, member output and reads without error | all |
| BR | bracket ends are collapse and expansion, the replayed bisection equals lo and hi, hi − lo ≤ 1e-14, or stopped by "static through X" at hi − lo ≤ 2e-14, h as its float repr | as stated |
| STL | each point stalls: fates collapse at p*ₕ − 1e-6, −1e-8 and expansion at +1e-6, +1e-8, and T gains ≥ 2.0 per side from 1e-6 to 1e-8 | 2.0 |
| EVT | the chain's first trapped cell equals the pair's collapse-side one; fates −1, +1 at p*ₕ ∓ 1e-8 | equal |
| RC5, RC4, RC8 | the chain ends at 0.5 F_max ≤ F_end < F_max, horizon ≥ Nc/8 from the edges; first law to F = 20; M_AH settled (plateau change ≤ 1e-4, flux ≤ 1e-5) | 0.5 F_max; 2e-2; 1e-4, 1e-5 |
| RH | \|plat(0.01) − plat(0.005)\| | 5e-5 |
| TGT | γ₁ at departure (h = 0.005) within 3 % of the target | 3 % |
| **HST** | member at departure at the two h: γ₁, r_th to 1e-4 relative, ṙ_th to 2e-5 absolute (the issue's) | 1e-4, 2e-5 |
| FITQ | the member's fit of M(r) on the two sides has an rms residual ≤ 1e-4 at the slices within 0.5 of t_dep | 1e-4 |
| **SEP** | each point informative, as read above | 5 × the h difference |
| **P2**, **P3** | \|M − M_pred\| ≤ 6e-5 for every informative point, h = 0.005 (the issue's) | 6e-5 |
| P2-ph | P2 at h = 0.01 with P2's (a, b) at that h | 6e-5 |
| **REP** | (0.1, 3.0, 0.5) reproduces #266's B = 0.1 at h = 0.005 (REP-ph at 0.01): p*ₕ to 1e-13, M and (γ₁, r_th, ṙ_th) to 1e-6 | 1e-13, 1e-6 |
| PMEM | planted static members of γ₁ = 0, 0.012, 0.048, 0.075 as profile slices through the extraction, h = 0.01, 0.005 | γ₁ 1e-5, r_th 1e-6, m± 1e-4 |
| PDEP | planted growing pair through `departure_time` | 2e-5 |
| PTD | planted pairs (odd part, trajectory of the measured size, rows every 0.5 in t from exact static members, τ = 0.97 t) through `member_at` and `speed_at`: t_dep, γ₁, r_th and ṙ_th at departure against the known values | 2e-5, 1e-5, 5e-5, 5e-6 (observed 7.2e-6, 4.8e-10, 2.1e-5, 1.4e-6) |
| PPRED | planted data that follow P2 (P3) exactly pass P2 (P3) at 1e-12 and fire P3 (P2) | 6e-5 (observed mismatch 1.3e-3) |
| PSEP | planted points at known separations from a planted family B through the separation test: informative or not as planted (5 cases) | as planted |

Error bars of M and of the member (kept separate, not mixed): the h difference \|plat(0.01) − plat(0.005)\| (RH, observed 6e-6 to 1.4e-5 in dev); the roundoff-realization scatter of the plateau, #253's 6.6e-6 at
h = 0.005 and 2.5e-5 at 0.01 (quoted, not remeasured; the supplement below measures a second realization of the six points); the member's h difference (HST). The bar 6e-5 is about twice the sum of the first two.

Supplement (post hoc, gates nothing): **RN**, the six points at h = 0.005 again, p*ₕ bisected from the bracket (0.98 p*, 1.02 p*) of the development p*ₕ: the same p*ₕ to a few 1e-15 and a different ulp-noise realization of the chain; the output prints the differences in M, the member and the
residuals of P2 and P3 (`analyze --rn=DIR`). It measures the scatter that W3's margin (1.1e-5) is to be set against; it does not replace the runs of record.

## Mutations (each `--mutate=NAME`; effect computed on the development set `runs_b` before being declared)

The mutation's declared set is the checks it newly fails; HST, P2, P3 and P2-ph already fail on the development set without a mutation (`--baseline=` reads them from the unmutated log), so no mutation can newly fire them: their ability to fail is shown by those failures, their ability to pass by the other points
(HST: six of seven points; P3: five of six) and by PPRED. 26 mutations; computed in 10 to 74 s each on the development set (`dev/mut_a/`).

| mutation | what it does | newly fires (declared) |
|---|---|---|
| crit_dm | `settled_mass.CRIT["dm"] = 2.0` | CFG |
| spec_w | the declared w × 1.1 | CFG |
| w_scale | the normal pulse's width × 1.1 in `set_route` (the chain is rerun from the stored p*ₕ: the fates at p*ₕ ∓ 1e-8 are lost) | FAM0, REP, REP-ph, RH, RUNS, RUNS-ph, SEP, TGT |
| xc_offset | the normal pulse's centre + 0.1 (chain rerun) | the same eight |
| no_run | the first point's member output treated as missing | RH, RUNS, SEP, TGT |
| bisect_early | the bracket replayed after 30 steps | BR, BR-ph |
| stl_flat | the lifetimes at 1e-6 and 1e-8 taken equal | STL, STL-ph |
| evt_side | the pair's expansion-side event in place of the collapse-side one | EVT, EVT-ph |
| short_limit | K = 12 (chain rerun) | RC5, RC5-ph, RC8, RC8-ph, REP, REP-ph |
| no_settle | the series truncated 3.0 before its end | RC5, RC5-ph, RC8, RC8-ph, REP, REP-ph |
| flux_sign | the horizon flux with the wrong sign | RC4, RC4-ph |
| mass_exponent | M = r^n/2 (chain rerun) | RC4, RC4-ph, REP, REP-ph |
| normal_drop | the normal field dropped from the flux | **nothing** (blind spot: the normal field is 1e-8 of the flux) |
| rh_swap | the plateau at h = 0.005 of the next point | RH |
| tgt_scale | the targets × 1.1 | TGT |
| eps_h | ε × 100 at h = 0.005 only | FITQ, PTD, SEP (HST fails already; no informative point is left, so P2 and P3 are skipped) |
| fitq_scale | the fit rms × 10 | FITQ |
| sep_self | family B replaced by the new member's own values | SEP |
| sep_k | the factor 5 → 0.005 in `sep_test` | PSEP |
| coef_a | a × 1.05 in the predictions | PPRED |
| coef_c | c × 0.8 | PPRED |
| no_rscale | the prediction without the r_th factor | PPRED |
| rep_off | the reproduction compared with #266's B = 0.125 | REP, REP-ph |
| asym_sign | #225's `fit_asym` with the sides swapped | PMEM, PTD, TGT |
| dep_eps | ε × 10 in `departure_time` | FITQ, PDEP, PTD |
| rdot_nolapse | τ = t in the speed | PTD |

For P2 and P3 the coefficient mutations (coef_a, coef_c, no_rscale) newly fail only the planted test: on the new members both already fail or sit at the bar.

## Run procedure (the runs of record)

`scripts/make_jobs.py` writes `jobs_rec.txt` (14 lines "B XC W H LO HI"); `scripts/run_jobs.sh RAW/runs jobs_rec.txt LANE 2` (two lanes, nice 10, `NUMBA_NUM_THREADS=1`) runs `scripts/run_one.sh` (pstar, chain, member; logs never overwritten, reruns numbered);
`python settled_mass_route.py analyze --raw=RAW [--rn=RAW/runs_rn]`; `scripts/run_muts.sh RAW RAW/mut LANE 2 RAW/analyze_record.log` (the unmutated log is the baseline). Stop condition: a single run not finished in 2 h of wall time is stopped and reported (dev: 32 to 92 s).

## Changes made after this README

(none yet)
