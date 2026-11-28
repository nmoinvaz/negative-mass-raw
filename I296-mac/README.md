# I296-mac: G's settled mass read against the member at departure eps = 1e-2 as well as 1e-3 (stored runs of #266, #267, #283, #295; no new run)

Machine: the coordinator's Mac (Apple M5, macOS, shared; at most 2 processes, nice 10, `NUMBA_NUM_THREADS=1`). Issue: https://github.com/nmoinvaz/negative-mass/issues/296
(from #283's recommended task 2 and #295's recommended task 3). Worktree `~/Source/negative-mass-i296`, branch `wip/i296-departure-eps`; code
`notes/wormhole_evolution/settled_mass_eps.py` at **dc9d00a** (a thin driver over #295's `settled_mass_route3.py`, which imports #283's, #266's and #267's drivers unchanged).
Python `~/Source/negative-mass/.venv/bin/python`. Stored inputs, read only: negative-mass-raw `I266-mac`, `I267-mac`, `I283-mac`, `I295-mac`, and the printed outputs of the four notes.

This README is written in stages. **Stage 1 (this text) is committed before any of #283's six or #295's three members is read at eps = 1e-2** (its commit is named in the issue post "criteria declared").
Stage 2 (the analysis of record, its logs and the mutations of record) is added after it.

## What had been read before this README, and what not

- Training points (#266's B = 0, 0.025, 0.05, 0.1, 0.125 and #267's delta = 1e-7, 1e-9 .. 1e-12) were read at eps = 1e-3 and at eps = 1e-2 in development (`dev/`).
- The test points (#283's W1-W3, C1-C3 and #295's N1-N3) were read at eps = 1e-3 only (their stored numbers are in the earlier notes), by the code's own guard: the development partition raises
  if a test point is asked for at any other eps (`--part=dev`; the logs `dev/analyze_dev.*.log` show 19 points at 1e-3 and 10 at 1e-2).
- One look before the code was written (not a member): the stored `t_dep` at eps = 1e-3, 1e-2, 1e-1 and the last row time of each test point's `member.json`, to see that the stored rows reach eps = 1e-2
  (they do: the rows run to t_dep(1e-1) + 1). No gamma_1, r_th, rdot_th or M of a test point at eps = 1e-2 had been computed.
- What development showed on the training points (this motivated the variants below; it is *not* the test):
  - B = 0, the symmetric member (r_th = 1, static, rdot_th = 0): at eps = 1e-3 r_th = 0.999999, rdot_th = -3.3e-6; at eps = 1e-2 **r_th = 0.999859 and rdot_th = -3.24e-4.**
    So the pair-mean's reading at eps = 1e-2 carries a second-order part of the unstable mode (about -1.4 eps^2 in r_th, and its growth rate 2 lambda in rdot_th) that the symmetric member shows alone.
  - The same moment read from two pairs (delta = 10^-e at eps = 1e-2 and 10^-(e+1) at 1e-3) differs by -1.4e-4 in r_th (e7 vs B0.1: 1.002742 vs 1.002878), the same contamination.
  - The form refitted at eps = 1e-2 over six of the nine training points predicts the three held out (B0.05, e9, e11) to +6.7e-5, -1.2e-4, -1.3e-4, and over eight predicts e10 to -7.1e-5; the same
    partitions at eps = 1e-3 give -9.0e-6, -2.9e-5, -2.3e-5 and -2.2e-5. In sample the fits are 3.2e-4 and 3.5e-4 at eps = 1e-2 against 3.1e-5 and 3.8e-5 at 1e-3.
- **Expectation, written before the data:** T1 and T2 below fail at fixed M_0, and the three variants V1-V3 do not rescue them, because the form does not even describe the training members at eps = 1e-2 at 6e-5.
  The tests are run as declared whatever the data say; no bar moves.

## The tests (gating), declared

Common: h = 0.005, delta = 1e-8, D = 4. Member = (gamma_1, r_th, rdot_th) at departure, read by #266's `member_at` on the pair's mean profile at the first t where |odd|/r_tuned = eps, and #267's `speed_at`
(the code of `settled_mass_route.read_point`; eps is the only change). M = the plateau of M_AH over the last 1.0 of x+ (`summary_g(...)['plat1']`). The form is P3's: y = M / r_th - M_0 = a gamma_1 + b gamma_1^2 + c rdot_th
with M_0 = 0.223086 (the coordinator's ruling; B = 0's plateau 0.2230862), plain least squares, no intercept, no weights. Prediction M_pred = r_th (M_0 + a gamma_1 + b gamma_1^2 + c rdot_th). Bar 6e-5 (the issue's), on |M - M_pred|.

| test | fit at eps = 1e-2 over | predicts at eps = 1e-2 | passes iff |
|---|---|---|---|
| **T1** | the nine of #267: B = 0.025, 0.05, 0.1, 0.125 (#266) and delta = 1e-7, 1e-9, 1e-10, 1e-11, 1e-12 at B = 0.1 (#267) | #283's six: W1, W2, W3 (normal pulse w = 1.0, centre 3), C1, C2, C3 (centre 4.0, w = 0.5) | max over the six of \|M - M_pred\| <= 6e-5 |
| **T2** | the fifteen: the nine and #283's six | #295's three: N1, N2, N3 (w = 0.75, centre 3.5) | max over the three <= 6e-5 |

(The point delta = 1e-8 at B = 0.1 is #266's B = 0.1 and is in the nine as B0.1; there is no separate e8.) A failure is reported with the residuals; it is not a failed check to fix.

## Reproduction at eps = 1e-3 (gating; the issue's third acceptance)

Same code, eps = 1e-3, against the printed numbers of the earlier notes (parsed from their output files at run time): **E3S** the six's M and M - P3 (P3 = #267's rounded (0.2300, 0.2724, 0.7835)) equal #283's to 1e-6;
**E3F** the fifteen-point refit (a, b, c) equals #295's frozen (0.2296318924, 0.2834170383, 0.7657657062) and its printed recomputation to 1e-6; **E3N** the three's M and M - P4 equal #295's to 1e-6;
**E3P** the nine-point refit equals #267's printed (0.2300, 0.2724, 0.7835) to the half unit of its last digit and its nine leave-one-out errors (predicted - measured, in y, the printed order) to 1e-6
(the sign convention was found in development: #267 prints A k . co - y k).

## Other gating controls

CFG (constants, sets, M_0 = B = 0's plateau to 1e-6 at h = 0.005 and 0.01, P4's constants equal the brief's); RUNS (every point reads at both eps, finite); MEM (t_dep(1e-2) - t_dep(1e-3) in [1.9, 2.2], the mode's growth
ln 10 / lambda; observed on the nine training points and B0: 1.948 to 2.065); E2B (eps = 1e-3 and 1e-2 members of the training points equal the printed t_dep, r_th, gamma_1 of #266 and #267 to the half unit of the last digit: 60 numbers);
PDEP2 (planted growing pair, crossing of 1e-2, bar 2e-5); PTD2 (planted pairs through `member_at` and `speed_at` at eps = 1e-2, bars: t_dep 2e-5, gamma_1 1e-5, r_th 5e-5 as #283, **rdot_th 1e-5**: #283's 5e-6
was written for eps = 1e-3; the planted error at eps = 1e-2 is 8.1e-6 (`dev/analyze_dev.1.log`, the first development run, which failed this bar), the estimator's slope over +-0.5 in tau on a trajectory two units later; in M that is 0.77 x 8.1e-6 = 6e-6, a tenth of the bar;
the bar is for planted data only and was set in development, before any test point was read); PFIT2 (planted data that follow the form exactly pass T1 and T2's code at 1e-12; with a x 1.05 or c x 0.8 in the test points they fire at 6e-5:
development 5.5e-4 and 1.3e-4).

## Post hoc variants, declared now (gate nothing; all are reported next to T1 and T2, whatever they show)

The variants answer whether a T1 or T2 failure is the form's or the reading's. They were suggested by B = 0's reading above. Each reuses the same fit code; `-V1`, `-V2`, `-V3`, `-h` are registered post hoc checks (6e-5, per set).

- **V2**: M_0 read at the same eps, M_0(eps) = B = 0's plateau / B = 0's r_th at eps (0.223118 at 1e-2).
- **V3**: B = 0's reading at the same eps subtracted: r_th' = r_th - (r_th(B=0) - 1), rdot_th' = rdot_th - rdot_th(B=0); M_0 = 0.223086.
- **V1**: a free intercept (four parameters).
- **-h**: T1 and T2 at h = 0.01 (M_0 = 0.223095, the refit at h = 0.01, members read at h = 0.01 and eps = 1e-2).
- printed only: the eps = 1e-3 constants (P3 on the six, P4 on the three, P4 on the nine and six) applied to the eps = 1e-2 members without a refit; the fifteen's and eighteen's in-sample and leave-one-out errors at both eps;
  the same-moment pairs (delta = 10^-e at 1e-2 against 10^-(e+1) at 1e-3) and B = 0's r_th - 1; leverage of the test points in the training design; the tests T1 and T2 at eps = 2e-3, 5e-3, 1e-2, 2e-2, 5e-2 with the four M_0 choices.

## The development partition, its bars, and the mutations

`--part=dev` fits and holds out *training* points only: T1 fits (B0.025, B0.1, B0.125, e7, e10, e12) and holds out (B0.05, e9, e11); T2 fits the other eight and holds out e10; the T-type checks use the development bar
**3e-4** because they do not pass 6e-5 there (above); every other bar is the record's. 21 checks (13 gating, 8 post hoc) pass in development (`dev/analyze_dev.4.log`, equal to `.3`).

Mutations (12, each runnable: `--mutate=NAME --baseline=LOG`). Effects computed in development (`dev/mut/NAME.log`, first set; the second set `NAME.1.log` is the same code with the declared sets and says MATCH for all 12). The effects on the record are those declared minus any check
that already fails without a mutation (a check failing at baseline cannot be newly fired; its ability to fail is shown by PFIT2's planted data and by these development effects).

| mutation | what it breaks | newly fires (development) |
|---|---|---|
| `asym_sign` | the asymmetry's sign in #225's fit (every gamma_1 flipped) | E2B, E3F, E3N, E3P, E3S, PTD2 |
| `coef_a` | a x 1.05 in the prediction | E3N, E3S, PFIT2, T1, T2 and all eight post hoc checks |
| `coef_c` | c x 0.8 in the prediction | E3N, E3S, PFIT2 (at the dev bar 3e-4 the three held-out points move 1e-4: T1, T2 do not fire; PFIT2 shows it fires at 6e-5) |
| `dep_eps` | the departure threshold x 10 (every reading) | E2B, E3F, E3N, E3P, E3S, PDEP2, PTD2 |
| `drop_point` | e12 left out of every fit | E3F, E3P |
| `eps_swap` | the eps = 1e-2 reading returns the eps = 1e-3 one | E2B, MEM |
| `loo_off` | in-sample error in place of leave-one-out | E3P |
| `m0_shift` | M_0 = 0.223095 | CFG, E3F, E3N, E3P, E3S |
| `no_rscale` | prediction without the r_th factor | E3N, E3S, PFIT2, T1, T2 and all eight post hoc checks |
| `no_run` | W1 and e9 treated as missing | RUNS |
| `no_speed` | the form without rdot_th | E3F, E3P, PFIT2 |
| `rdot_nolapse` | the speed per unit t in place of tau | E3F, E3N, E3P, E3S, PTD2 |

## Plan and files

1. `analyze --part=record` (about a minute) -> `record/analyze_record.log`; reruns are numbered, no log is overwritten. 2. `scripts/run_muts.sh record record/mut BASELOG` (12 mutations, one lane).
3. Note `notes/wormhole_evolution/settled_mass_eps.md` with the script's output `settled_mass_eps_output.txt` (the record's log), the answer, the error-bar table, proposed text for `settled_mass_route3.md`, `critical_ghost.md` section 1.3 and Paper V (not applied).
Files here: `README.md`, `dev/` (development logs, `mut/`), `scripts/run_muts.sh`, and stage 2's `record/`.

## Stage 2: the analysis of record (added after Stage 1 was committed at 21b10fba; nothing above was edited)

- **Record 1** (`record/analyze_record.log`, code dc9d00a, 14 s, exit 1): 21 checks, 2 gating checks fail: **T1** (max |M - M_pred| 1.29e-4; W1 +4.80e-5, W2 -1.28e-4, W3 -1.97e-5, C1 +4.67e-5, C2 -1.29e-4, C3 -3.20e-5)
  and **T2** (9.34e-5; N1 +6.67e-5, N2 -9.34e-5, N3 +1.24e-5). The other 11 gating checks pass (CFG, RUNS, PDEP2, PTD2, PFIT2, MEM, E2B, E3S, E3F, E3N, E3P); six of the eight post hoc checks fail (T1-V1, T1-V2, T1-V3, T1-h, T2-V2, T2-h),
  T2-V1 and T2-V3 pass (4.2e-5, 3.7e-5).
- **Addendum, after Record 1 and before any mutation of record:** `post_hoc2` was added (code 97a41f4; printed only, gates nothing, the gating checks and T1, T2 unchanged): the fits' own errors under the four readings,
  T1 and T2 without e12 (and without e11, e12), and B = 0's reading against eps with its eps^2 scaling. It was added because Record 1's in-sample table has e12 at +374e-6 (the delta = 1e-12 pair at the pair's roundoff floor, whose
  same-moment partner differs in t_dep by 0.026) and because B = 0's contamination looked like eps^2. **Record 2** (`record/analyze_record.2.log`, code 97a41f4, exit 1) equals Record 1 in every line above `== Post hoc 2`
  (checked with diff) and is the output of record, copied to `notes/wormhole_evolution/settled_mass_eps_output.txt`.
- **Mutations of record** (`record/mut/NAME.log`, baseline = Record 2, `scripts/run_muts.sh record record/mut record/analyze_record.2.log`): 12 run, all exit codes as printed in each log.
  **9 of 12 newly fire exactly their declared set** (asym_sign, coef_a, drop_point, eps_swap, loo_off, m0_shift, no_rscale, no_run, rdot_nolapse). **3 of 12 (coef_c, dep_eps, no_speed) fire their declared set and also the two post hoc checks T2-V1
  and T2-V3** (DIFFERENT, exit 1): those two pass on the record at the bar 6e-5 (margins 1.8e-5 and 2.3e-5), but the development bar was 3e-4 where the mutations' shifts (about 1e-4) did not reach it. The declared sets were not edited.
  T1 and T2 fail without a mutation, so no mutation can newly fire them on the record; that they can fail is shown by these failures, by PFIT2's planted data (fires at 5.5e-4 and 1.3e-4 for a x 1.05 and c x 0.8) and by development (coef_a and no_rscale fire them at the dev bar).
- Reruns are numbered; no log is overwritten. Raw commit of Stage 2 is named in the issue's closing comment.

## Stage 3: the note and the figure

- Branch `wip/i296-departure-eps` at **d46fa83**: `notes/wormhole_evolution/settled_mass_eps.md`, `settled_mass_eps_output.txt` (= `record/analyze_record.2.log`, byte for byte), `settled_mass_eps.svg`; the script is unchanged since 97a41f4.
- `scripts/settled_mass_eps_graph.py` draws the figure from the stored runs through the script's own functions (`record/graph.log` the first drawing, `record/graph.1.log` the final: only the footnote's warning text differs).
  Rerun: `NUMBA_NUM_THREADS=1 python scripts/settled_mass_eps_graph.py` (about 15 s), writes `notes/wormhole_evolution/settled_mass_eps.svg` in the worktree.
- Nothing in Stage 1 or 2 was edited. The note reports: T1 and T2 not met; the eps = 1e-3 reproduction met; 3 of 12 record mutations fire two extra post hoc checks.
