# I317-mac: corrected eps = 1e-2 reading (V3), frozen, then predicting #305's X1 to X3 (analysis of stored runs only)

Machine: the coordinator's Mac (Apple M5, macOS, shared). Issue: https://github.com/nmoinvaz/negative-mass/issues/317
Code: `notes/wormhole_evolution/settled_mass_blind.py` in nmoinvaz/negative-mass, branch `wip/i317-corrected-blind`
(`freeze` and `analyze`; `--part=dev|record`, `--mutate=`, `--baseline=`). No evolution runs: the stored runs of #266, #267, #283, #295 and #305 are read.

Stage 0 (this stub, before any analysis log): the folder layout.

- `dev/`: development runs. They read only the fifteen training members of #296 and B = 0, never #305's X1 to X3 and never #295's N1 to N3 (a guard in the script raises).
- `record/`: the runs of record, after the frozen file is committed and pushed.
- `frozen_v3.json`: the frozen coefficients (written by `freeze --part=record`, never overwritten).
- `scripts/`: drivers.

Stage 1 (method, bar, mutations and their development effects) follows below once the development runs are done.

## Stage 1: method, bar, checks, mutations (written before the frozen fit; development ran on training members only)

Date 2026-11-28. Code: `notes/wormhole_evolution/settled_mass_blind.py` (branch `wip/i317-corrected-blind`). Readings are #296's `settled_mass_eps.read` (#266's `member_at` on the pair's mean profile,
#267's `speed_at`), imported unchanged; the fit is #296's `fit_pred`, the subtraction is #296's `sub_ref` operation.

### What is asked (issue #317)

Freeze #296's V3: subtract B = 0's reading at eps = 1e-2 from r_th and rdot_th of every member, keep M_0 = 0.223086, refit the form y = M/r_th - M_0 = a g + b g^2 + c rdot_th over the fifteen training members
without delta = 1e-12 (14 points: B = 0.025, 0.05, 0.1, 0.125; delta = 1e-7, 1e-9, 1e-10, 1e-11; #283's W1-W3, C1-C3). Commit and push the coefficients. Then predict #305's X1 to X3 from their stored runs at eps = 1e-2.
**Acceptance (gating): each of X1, X2, X3 within 6e-5 of the frozen V3 prediction at eps = 1e-2, or the residuals are reported.** Bar 6e-5 from the issue; not moved.
Reported without gating: the same prediction with V1 (free intercept, eps = 1e-2), with V3 at eps = 1e-3, and with the unsubtracted refits at both eps (the latter at eps = 1e-3 is #305's P4 refitted without e12).

### Order (the freeze is code-enforced)

1. `freeze --part=record` reads B = 0 and the 14 training members at eps = 1e-3 and 1e-2 (a guard raises on X1-X3 and N1-N3), writes `frozen_v3.json` (five fits: V3 1e-2, V1 1e-2, V3 1e-3, fixed-M_0 refit at 1e-2 and 1e-3;
   B = 0's offsets; the sha256 of the inputs; the sha256 of the script) and never overwrites it. It is then committed and pushed with a README stage 2 that prints the coefficients.
2. `analyze --part=record` first checks (GIT) that `frozen_v3.json` is tracked, unmodified and contained in a pushed commit of this repository, recomputes the five fits (FRZ) and compares them with the frozen ones, then
   loads X1-X3 from `I305-mac/runs` (`settled_mass_route.load_point`, the declared (B, x_c, w) = (0.09112, 4.0, 1.5), (0.1695, 4.0, 1.5), (0.2044, 4.0, 1.5)), reads them at eps = 1e-3 and 1e-2 and predicts them from the frozen coefficients
   and B = 0's frozen offsets. N1-N3 (#295) are read as a control (not X; #296 already read them at 1e-2).
3. The record README stage 3 names the raw commit that holds the frozen file.

### Development partition

`--part=dev`: the fit is 11 of the 14 (held out: B = 0.05, C2, delta = 1e-10: one B, one route-C and one delta point, chosen by structure before any run), the prediction is the three held out. X1-X3 and N1-N3 are never read (guard).
`dev/frozen_dev.json` is committed and pushed (raw commit 8dcdaae9) before the dev analysis, so GIT runs on it. Baseline `dev/analyze_dev.1.log`, `.2.log` (the same apart from header and time): 19 checks (15 gating, 4 non-gating), 0 gating fail;
held-out residuals under the frozen V3 fit at eps = 1e-2: -2.41e-06, -1.28e-05, +9.25e-06 (bar 6e-5 is used in dev too: the baseline passes it; no dev bar was needed). The non-gating unsubtracted refit at eps = 1e-2 misses B = 0.05 by +8.83e-05.

### Checks (15 gating, 4 non-gating; the same ids in dev and record)

| id | what | can fail by |
|---|---|---|
| CFG | M_0 = B = 0's plateau to 1e-6, P4's constants = #295's, bar 6e-5, frozen file's part, training set, M_0, bar, X's declared (B, x_c, w) | `m0_shift`, `bar_shift`, `keep_e12` |
| GIT | frozen file tracked, unmodified, in a pushed commit | `git_untracked` |
| RUNS | every member reads at both eps, finite | `no_run` |
| RDX | the stored-run loader used for X (root and spec of the point) returns members bit for bit equal to #296's on points both read (dev: W2, C2; record: N1-N3) | `x_loader_h` |
| REP296 | t_dep, gamma_1, r_th, rdot_th at both eps and M equal #296's printed table, half a unit of the last digit (dev 135 numbers, record 162) | `eps_swap`, `dep_eps`, `rdot_nolapse`, `asym_sign` |
| FRZ | the five frozen fits equal the refit recomputed now to 1e-9; B = 0's offsets to 1e-12; the inputs' sha256 | `stale_frozen`, `b0_eps`, `no_subtract`, `sub_sign`, `keep_e12`, ... |
| REPV3 | #296's printed max |M - predicted| without e12 (fixed, V1, V3; T1 and, at the record, T2; eps 1e-3 and 1e-2) equal the recomputed, half a unit of the last digit (dev 6, record 12) | `no_subtract`, `sub_sign`, `coef_a`, `m0_shift`, ... |
| PARSE305 | #305's printed M - P4 (+9.00e-05, +2.13e-04, +1.98e-04) parse from its output | `parse_wrong` |
| REFX | at eps = 1e-3 frozen P4 (#295) misses X1-X3 by #305's printed residuals to half a unit of the last digit (dev stand-in: C2 against #283's printed M - P3, 1e-6) | `coef_a`, `m0_shift`, `dep_eps`, ... |
| PL1 | planted members that follow the form, offset by B = 0's second-order part, through make_fit + the frozen prediction with V3: residual <= 1e-12, coefficients to 1e-9 | `no_subtract`, `sub_sign`, `coef_a`, ... |
| PL2, PL3 | a x 1.05, c x 0.8 in the planted test members fires (6e-5) | `coef_a`, `coef_c` |
| PL4 | an offset 1.5 times B = 0's at the planted test members fires (6e-5): V3 is sensitive to a member dependence of the second-order part | `no_member_dep` |
| PL296 | #296's planted cases (PDEP2, PTD2, PFIT2) pass through the same readings at eps = 1e-2 (sets patched to this part's) | `dep_eps`, `rdot_nolapse`, `asym_sign`, `coef_a`, `coef_c`, `no_rscale`, `no_speed` |
| PX | **the frozen V3 fit at eps = 1e-2 predicts the test members within 6e-5** | `coef_a`, `coef_c`, `no_rscale`, `no_subtract`, `sub_sign`, `test_swap`, ... |
| PX-V1_1e-2, PX-V3_1e-3, PX-FIX_1e-2, PX-FIX_1e-3 | non-gating: V1 at 1e-2, V3 at 1e-3, the unsubtracted refits at 1e-2 and 1e-3 | |

Planted truth before real data: PL1-PL4 and PL296 run the fit, the subtraction and the prediction on planted members with a known answer before the real members are predicted; the pass criteria are in the table.
Independence: the prediction shares #296's readings and fit machinery by design (the issue asks for it); what the reproductions REP296, REPV3, REFX show is that this driver reaches #296's and #305's printed numbers through it.

### Mutations and their development effects (23; each newly fires exactly this set on the dev partition: first pass `dev/mut/*.1.log`, second pass `dev/mut/*.2.log` 23 of 23 MATCH)

| mutation | what it breaks | newly fires |
|---|---|---|
| `asym_sign` | odd part's sign flipped in the locus (#296's) | FRZ, PL296, PX, PX-FIX_1e-3, PX-V1_1e-2, PX-V3_1e-3, REFX, REP296 |
| `b0_eps` | V3 at eps = 1e-2 subtracts B = 0's reading at eps = 1e-3 | FRZ |
| `bar_shift` | bar 1e-4 in CFG | CFG |
| `coef_a` | a x 1.05 in every prediction (and #296's refit hook) | PL1, PL2, PL296, PX, PX-FIX_1e-3, PX-V1_1e-2, PX-V3_1e-3, REFX, REPV3 |
| `coef_c` | c x 0.8 in every prediction | PL1, PL296, PL3, PX, PX-FIX_1e-3, PX-V1_1e-2, PX-V3_1e-3, REFX, REPV3 |
| `dep_eps` | departure criterion x 10 (#296's) | FRZ, PL296, PX, PX-FIX_1e-3, PX-V1_1e-2, PX-V3_1e-3, REFX, REP296, REPV3 |
| `eps_swap` | members at eps = 1e-2 read at 1e-3 | FRZ, PX, PX-V1_1e-2, REP296, REPV3 |
| `git_untracked` | GIT looks at an untracked path | GIT |
| `keep_e12` | delta = 1e-12 kept in the fit | CFG, FRZ |
| `m0_shift` | M_0 = 0.223095 in the recomputed fits | CFG, FRZ, PL1, REFX, REPV3 |
| `no_member_dep` | PL4's member dependence removed (offset factor 1.0) | PL4 |
| `no_rscale` | prediction without the r_th' factor | PL1, PL296, PX, PX-FIX_1e-3, PX-V1_1e-2, PX-V3_1e-3, REFX, REPV3 |
| `no_run` | W1 at eps = 1e-2 treated as missing | RUNS |
| `no_speed` | fits without the rdot_th column | FRZ, PL1, PL296, REPV3 |
| `no_subtract` | V3's subtraction removed | FRZ, PL1, PX, REPV3 |
| `parse_wrong` | #305's printed residuals read from #296's output | PARSE305 |
| `rdot_nolapse` | speed without the lapse factor (#296's) | FRZ, PL296, REFX, REP296, REPV3 |
| `stale_frozen` | V3's frozen a + 1e-6 | FRZ |
| `sub_r_only` | only r_th - 1 subtracted | FRZ, PL1, PX, REPV3 |
| `sub_sign` | V3's subtraction with the wrong sign | FRZ, PL1, PX, REPV3 |
| `sub_v_only` | only rdot_th subtracted | FRZ, PL1, REPV3 |
| `test_swap` | the test members' M rotated by one | PL1, PX, PX-FIX_1e-3, PX-V1_1e-2, PX-V3_1e-3 |
| `x_loader_h` | the stored-run loader reads h = 0.01 | RDX |

`parse_wrong` and `no_member_dep` were added after the first dev pass (they cover PARSE305 and PL4, which no mutation fired); their effect was computed on their own `.1` runs, and all 23 `.2` runs use the final script.
`PX-FIX_1e-2` fails without a mutation in dev (+8.83e-05 at B = 0.05) and so cannot be newly fired. REFX's X branch (#305's printed residuals) has no dev run: its code path is exercised in dev only through the C2 stand-in; on the record the mutations are run again
and any difference from the dev sets is reported. At the record PX is expected to fail without a mutation if X is missed, and then no mutation can newly fire it.

### What I expect (written before the freeze)

#296: V3 without e12 predicts #295's N1-N3 to 2.12e-6 and #283's six to 2.13e-5 at eps = 1e-2. #305/#314: the frozen refit at eps = 1e-3 misses X1-X3 by +9.0e-5, +2.13e-4, +1.98e-4, none of the speed or member readings tried closes X2, X3,
and the miss is proportional to rdot_th along X (-0.080). I expect V3 at eps = 1e-2 to move X2 and X3 (their rdot_th at 1e-2 differs from 1e-3 by 40 % and 73 %) but have no basis for the direction; I would not be surprised if X1 passes and X2, X3 miss.
This is a prior, not a criterion.

### Limits of this stage

- The bar of 6e-5, the fit set (14 points), M_0, V3's definition and the order are fixed here and not changed after X is read.
- The eps = 1e-2 and 1e-3 members of the 14 and B = 0 are read in dev as well as at the freeze (they are training members); no X or N member is read before the freeze.
- Three more things are not controlled here: h other than 0.005, delta other than 1e-8, X's equality to B = 0's second-order part (PL4 shows the size of a 50 % member dependence: 1.4e-4).

## Stage 2: the frozen fit (written and committed before X1-X3 or N1-N3 were read by any code)

`freeze --part=record` (log `record/freeze_record.1.log`, exit 0, 6 s) read B = 0 and the 14 training members (B0.025, B0.05, B0.1, B0.125, e7, e9, e10, e11, W1, W2, W3, C1, C2, C3) at eps = 1e-3 and 1e-2, h = 0.005, and wrote
`frozen_v3.json` (this folder). Script `notes/wormhole_evolution/settled_mass_blind.py` at commit 8f63e0b of nmoinvaz/negative-mass (branch `wip/i317-corrected-blind`), sha256 `78f8454944a331e81d63a114d41ce5b6c3beb7c7305b597f6d26e2970d0332a8`;
inputs sha256 `0517bce5789750ad0aaaacf3275e7506dc1450936a1cbdc47419201fb11f2ded`. M_0 = 0.223086, bar = 6e-05.

**The gating fit is V3 at eps = 1e-2.** Form: y = M / r_th' - M_0 = a g + b g^2 + c rdot_th', with r_th' = r_th - dr and rdot_th' = rdot_th - dv, (dr, dv) = B = 0's (r_th - 1, rdot_th) at the same eps; prediction M = r_th' (M_0 + a g + b g^2 + c rdot_th').
Plain least squares over the 14 points, no weights. Frozen coefficients (12 digits; the file holds the full floats):

| fit | (a, b, c [, intercept]) | in-sample max | leave-one-out max | subtracted (dr, dv) |
|---|---|---|---|---|
| V3_1e-2 | +0.229606394834, +0.131548678788, +0.558734349701 | 2.047e-05 | 2.965e-05 | -1.411564e-04, -3.239682e-04 |
| V1_1e-2 | +0.229658178272, +0.131501001749, +0.558263902441, +0.000211848400 | 2.075e-05 | 3.041e-05 | none |
| V3_1e-3 | +0.228776413889, +0.297260530540, +0.749985718292 | 3.989e-05 | 6.284e-05 | -1.496053e-06, -3.260799e-06 |
| FIX_1e-2 | +0.236536612091, +0.099542208240, +0.467328462919 | 1.554e-04 | 1.638e-04 | none |
| FIX_1e-3 | +0.228897026074, +0.296149233172, +0.749665170223 | 3.956e-05 | 6.315e-05 | none |

Not X: nothing of #305's X1-X3 or #295's N1-N3 was read (the script raises). For reference only, and read before X: #295's frozen P4 (eps = 1e-3, e12 kept, fifteen points) is (0.2296318924, 0.2834170383, 0.7657657062); V3 at eps = 1e-3 without e12 is (0.2288, 0.2973, 0.7500);
V3 at eps = 1e-2 is (0.2296, 0.1315, 0.5587): the form's b and c differ by 2x and 0.75x between the two readings even after the subtraction. That was seen at the freeze and is not a criterion.

The raw commit that holds `frozen_v3.json` is named in stage 3 (a commit cannot name its own hash).

## Stage 3: the record (after the frozen file was committed and pushed)

The raw commit that holds `frozen_v3.json` and stage 2 above is **7a8a4e8c** (pushed before any code read X1-X3; GIT in every record log prints it: `last commit 7a8a4e8c8a1674b0316dd56dc10d98b2120405d8 2026-11-28T04:41:01-08:00`).
Script commits in nmoinvaz/negative-mass (branch `wip/i317-corrected-blind`): 8f63e0b (freeze and analysis, used for the freeze), 55fd959 and 010c9e7 (the post hoc command; `git diff 8f63e0b 010c9e7` adds 62 lines, deletes none).

- `record/analyze_record.1.log` (script 8f63e0b+55fd959), `.2.log` (55fd959), `.3.log` (010c9e7, the output of record): 19 checks, 15 gating; **PX fails**, the other 14 gating pass; the three logs are equal apart from header and time.
- Prediction of record, V3 at eps = 1e-2 (bar 6e-5): X1 +3.346e-05, X2 +7.317e-05, X3 +7.733e-05. Not gating: V1 1e-2 +3.359e-05, +7.285e-05, +7.722e-05; V3 1e-3 +7.774e-05, +1.769e-04, +1.439e-04; unsubtracted 1e-2 +6.956e-05, -1.168e-04, -1.020e-04; unsubtracted 1e-3 +7.886e-05, +1.756e-04, +1.432e-04.
- Control, not X: N1-N3 under the frozen V3 fit +7.3e-08, -2.12e-06, -1.79e-06.
- `record/post_hoc.1.log` (before the trajectory block), `.2.log` (final): post hoc, gates nothing.
- Mutations of record, `record/mut/*.1.log` (baseline `analyze_record.3.log`): 20 of 23 match their declared sets; `test_swap` and `x_loader_h` also newly fire REFX (its X branch has no dev run); `parse_wrong` fires PARSE305 and then raises KeyError 'X1' in REFX (log and `.err` kept).
- Figure: `record/graph.1.log`, `.2.log` (the first drew text past the right edge; the second is the figure in the note).
- Deviations from stage 1: none in the bar, fit set, M_0 or order. The prior written in stage 1 (X1 inside, X2 and X3 outside would not surprise me) matched the result.
