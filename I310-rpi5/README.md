# I310-rpi5: criteria, development runs and runs of record for #310, κ r_S c₁ = −c/π at all 20 black universes of #212

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared), runner `negative-mass-rpi5-i310`, worktree `~/Source/negative-mass-i310` on `wip/i310-c1-all`, at most 3 processes, nice 10, one thread each.
Issue: https://github.com/nmoinvaz/negative-mass/issues/310. Script: `notes/black_universe/static_c1_all.py`, which imports `static_c1_members.py` (#301) and through it `horizon_sector.py`, `full_slice.py`, `linear.py`, all read only.
Python: `~/Source/negative-mass-venv314/bin/python` (3.14.10; numpy 2.5.4, scipy 1.18.1, numba 0.68.1, mpmath 1.3.0, sympy 1.14.0). Written before the runs of record (`runs/`); the development runs are in `dev/` (`d1_*`, `d2_*`, `d3_*`).

## Question

#301 proved κ r_S c₁ = K/2 = −c/π for the exact family r = √L R, F = A + 1/L − 1 (#269) at every Ellis member, and ran it at c = −1, −1.5, −0.3 and on Schwarzschild. This issue: run T1 and T2 of
`static_c1_members.py` (mpmath) at all 20 black universes of #212 (c = −10, −3, −2, −1.5, −1.1, −1.01, −1.001, −1.0001, −1, −0.9999, −0.999, −0.99, −0.95, −0.9, −0.7, −0.5, −0.3, −0.2, −0.1, −0.01) and T4 (the exact
mode through the slice code) at five of them, with ρ_h > 1 among them. Conventions as in #301: G = c = 1, r_S = R(ρ_h), κ = A′(ρ_h)/2 for the Killing field with A → 1, c₁ = δr(S) per unit δL, M the Misner–Sharp mass at infinity.

## Method

All checks are the checks of #301, run one member at a time (ids `T1[c]` …), plus the following new code, all in `static_c1_all.py`:

1. **Members.** `Ellis2` is `static_c1_members.Ellis` with the horizon scan widened from |ρ| ≤ 6 to |ρ| ≤ 30 (c = −0.01 has ρ_h = −7.0022).
2. **T1** (`static_c1_members.check_T1`, one member): ρ_h, κ, r_S of the double-precision class against mpmath (40 digits); c₁ = R_h/2 + R′_h/(2κ) against d_L[√L R(ρ_h(L))] (120 digits); dM_ADM = d_L lim m_L against −c/π;
   κ r_S c₁ (double constants) against dM_ADM. Bar 1e-12 on each.
3. **T1x** (new): κ r_S c₁ = −c/π and K(horizon) = κ R_h² + ρ_h = −2c/π from the closed forms alone at 40 digits (no double constant, no finite difference). Bar 1e-12 (the numbers are ~1e-39).
4. **T2** (the recipe of `check_T2`, one member, printing |ratio − 1| from the 120-digit value instead of its float rounding): dM = κ_ξ dA/(8π) at L = 0.5, 0.9, 1, 1.5, 2, 4, κ_ξ = √L A′(ρ_h(L))/2, A = 4π L R(ρ_h(L))², M the Misner–Sharp limit at ρ = 1e20;
   M_MS against K L^{3/2}/3. Bar 1e-12.
5. **T5** (new): with r_S := 1, κ c₁ misses dM_ADM by 1 − 1/r_S at every c ≠ −1 (the check requires miss > 1e-12 and |miss − (1 − 1/r_S)| ≤ 1e-9·(1 − 1/r_S) + 1e-13) and holds to 1e-12 at c = −1.
6. **Chart** (new): `hs.KChart` anchors Π = 1 at ρ_c = 1, which is inside the horizon at c = −3 and −10 (`lin.Chart` raises "the corner must lie in the static region"), and its lnE table ends at ρ_hi = ρ_c + 1.25 p_max/√2 + 3 with p_max = 2 ln(pi_max)/√2 + 8, independent of κ. At small κ
   the table ends before Π = 1e12 (c = −10: ρ(Π = 1e12) = 104.1, table to 49.8; c = −0.01: 89.5, table to 38.6), and `_solve_delta` then returns the extrapolated cubic without an error. `KChartRc` (subclass of `hs.KChart`) takes the anchor ρ_c = ρ_h + 1 and
   pi_max = max(1e12, e^{(ρ_h − ρ_c + ln(1e12)/(2κ) + 12 − 10.1)/1.25}) so that the table reaches Π = 1e12 at every κ (ρ_hi = 134.7 at c = −10, 103.6 at c = −0.01). The anchor is a gauge: Π → λΠ, and E = A/(2κ²Π), ρ_Π = A/(2κΠ) are independent of it.
   `fs.Bg` is built without calling `hs.KChart` (`Bg.__new__`, then kc, par, tab, kappa).
7. **C0** (new): ρ(Π) of the chart against mpmath, from ln Π(ρ) = ln(δ/δ_c) + ∫_{ρ_c}^{ρ}(2κ/A − 1/(r − ρ_h)) dr (Π(ρ_c) = 1, 40 digits, Newton in ρ started at the chart's value), at Π = 1e-4, 1e-2, 0.25, 1, 4, 25, 1e3, 1e6, 1e8, 1e10, 1e12;
   relative in ρ − ρ_h. Bar 1e-9.
8. **T3** (`check_T3`, one member): ρ-form p, q, a, a(0) = −r_S, Θ and dm in ρ against the s-form, closed-form tail, conservation. Bar 1e-8. Not run at c = −10: its closed-form tail probes ρ = 3, inside the horizon (ρ_h = 4.197).
9. **T4** (`check_T4`, one member): the exact mode through the slice code at 9–14 values 0.05 ≤ s ≤ 1e5 and the 7 cut extensions read at ρ = 1e8. **Bars of #301, unchanged:** 1e-9 on c₁(S) against d_L r_S, on Θ_gen + r_S c₁ and c₁ = −Θ_gen/r_S
   (relative to r_S c₁) and on dm of the slice code against d_L m at fixed Π; 1e-6 on κ r_S c₁ against dM_ADM, and on the cut extensions against κ r_S c₁ and against dM_ADM.
10. **T7** (`check_T7`, one member, secondary): the exact mode (amplitude 2e-3) as ray data through the Kruskal solver in the same chart, h = 0.005, 0.0025, 0.00125, 0.000625, Richardson of the last two. Bars of #301: error/scale at the finest step ≤ 5e-2 with the last two
    ratios 4.0 ± 0.3; c₁ of the horizon fit, δr(S), Θ_gen(s) = −r_S c₁ at 8 values of s, δM of the three cuts against the exact value and against κ r_S c₁, all ≤ 1e-6 relative; |c₂| ≤ 1e-6 c₁.
11. **X** (extension, not in the issue): C0, T3 and T4 at the other 15 members. **C1** (anchor independence): C0 and T4 at c = −1.5 with ρ_c = 3 (#301 used ρ_c = 1; the default here is ρ_h + 1 = 1.34).
12. **`derive`**: S0 (sympy: A = 1 + c f(ρ) solves R²A″ = 2(A − 1) for symbolic c) and T0 (per member: A′ > 0 on [−30, 30], A(−30) < 0 < A(30), A(ρ_h) ≤ 1e-14: one simple horizon).

What the checks share (recorded, AGENTS.md): T1, T1x, T2, T5 and C0 read mpmath from A(ρ) alone (the closed form of #212) and share with each other only the family definition A(ρ), r = √L R, F = A + 1/L − 1 (#269); S0 checks that A solves the ODE
that the family needs. T4, T3 and T7 share the slice code of #258/#259 (Θ_gen, dm), the exact mode of #301 and the chart; their reference values (c₁, dM_ADM) are the mpmath numbers of T1. The chart is checked by C0 against code that shares
only A(ρ) with it.

## The five members of T4 and why

| c | ρ_h | κ | r_S | anchor ρ_c | why |
|---|---|---|---|---|---|
| −10 | 4.197082 | 0.116522 | 4.314568 | 5.197 | ρ_h > 1, smallest κ on the c < −1 side, largest r_S ≠ 1 of the c < −1 side; T3 not run |
| −3 | 1.118725 | 0.351374 | 1.500515 | 2.119 | ρ_h > 1, nearest to the throat from outside |
| −0.5 | −0.524073 | 0.660873 | 1.129005 | 0.476 | c > −1, mid |
| −0.1 | −2.024885 | 0.409506 | 2.258353 | −1.025 | c > −1, r_S = 2.26 |
| −0.01 | −7.002156 | 0.140086 | 7.073202 | −6.002 | c > −1, smallest |c|, smallest κ on that side, c₁ = 3.2e-3 a difference of two terms of size 3.5 |

The other 15 members (X) run the same T4. The issue's two conditions hold: ρ_h > 1 at c = −10 and −3; c > −1 at c = −0.5, −0.1 and −0.01.

## Criteria (declared before the runs of record)

| issue acceptance | checks | bar |
|---|---|---|
| κ r_S c₁ = −c/π at all 20 | `T1[c]` (6 quantities, double constants against mpmath) and `T1x[c]` (closed forms, 40 digits), c at the 20 members | 1e-12 |
| dM = κ_ξ dA/(8π) at all 20 | `T2[c]`, six L per member, and M_MS against K L^{3/2}/3 | 1e-12 |
| Θ_gen + r_S c₁ ≤ 1e-9 at five | `T4[c]` at c = −10, −3, −0.5, −0.1, −0.01 (all of its bars as listed in Method 9) | 1e-9 (1e-6 on the identity and the cuts, as in #301) |
| `rs_one` fails at every c ≠ −1 | `T5[c]`: r_S := 1 misses by 1 − 1/r_S at the 19 members, holds at c = −1; and `--mutate=rs_one` fires `T1[c]` and `T1x[c]` at the 19 members and none at c = −1 (declared set below) | miss > 1e-12 |
| each check has a `--mutate=` with a computed effect | the 19 mutations below (17 of `check`, 2 of `derive`); fired sets equal the declared ones | exact equality of sets |

Secondary, reported and held to the bars of Method, not part of the issue's acceptance: C0 (chart), T3, T7 (the step ladder is the default for every member, see below), X, C1, S0, T0.

A failed check is reported with its number and cause. No bar is changed after data. T1 at c = −0.01 is marginal in double precision (see d1: 6.0e-13 of 1e-12); it is reported as measured, and `T1x` is the check of the identity at 40 digits.

## Mutations (declared effects, computed in development run d3 before the runs of record)

`static_c1_all.py check|derive --mutate=NAME`, each a change of the code under test; every check is in scope. The fired sets are in `dev/d3_<name>.log` (derive ones `dev/d3_derive_<name>.log`) and are the `DECLARED` dictionary of the script;
`static_c1_all.py mutations DIR PREFIX` compares stored logs with it (DIR/PREFIX<name>.log; 20 of 20 equal on d3, the unmutated run `base` included). The run of record must reproduce them.

| mutation | change | declared fired set | computed effect (d3) |
|---|---|---|---|
| `base` | none | none | 146 of 146 checks pass (183 s) |
| `s_ode` | `derive`: RHS of the ODE with the wrong sign | S0 | residual ≠ 0 |
| `a_flip` | `derive`: K → −K in A | T0 at the 20 | min A′ = −2.4 at c = −0.1 (ρ = 6.0), −2.4e-1 at c = −0.01 |
| `rs_one` | r_S := 1 in κ r_S c₁ (scm) | T1, T1x at the 19 with c ≠ −1; T4 at 15 of the 20 and C1; T7 at the five | κ r_S c₁ vs dM 7.7e-1 (c = −10), 3.1e-9 (c = −1.0001), 8.6e-1 (c = −0.01); T4/T7 cuts 7.7e-1, 8.6e-1, 3.3 |
| `ctl_true` | T5's wrong arm uses the true r_S | T5 at the 19 | the arm holds (5.1e-14 at c = −10; T5 needs it to fail) |
| `c1_noshift` | c₁ without R′_h/(2κ) | T1, T1x at the 19 | relative 6.6e-1 (c = −10), 1.2e-4 (c = −1.0001) |
| `kappa_off` | κ → 1.01 κ in the comparisons | T1, T1x, T5 at the 20; T4 at the 20 and C1; T7 at the five | 1.0e-2 at every member |
| `cpi_off` | −c/π replaced by −c/3.14159 (T1x only) | T1x at the 20 | 8.4e-7 |
| `law_norm` | κ_ξ without √L | T2 at the 20 | ratio 1.4142 at L = 0.5, 0.5 at L = 4 |
| `law_mass` | M ∝ L² for L^{3/2} | T2 at the 20 | M_MS vs closed form 6.2e-1 (c = −10) |
| `th_noF` | no μ s r_Π δF term in Θ_gen | T4 at the 20 and C1; T7 at the five | all fire |
| `th_nophi` | no c δφ term | same set | all fire (also at c = −0.01) |
| `dm_noT` | no −R R′ y_x term in δm | same set | all fire |
| `jump_off` | no jump of δr′ at the cut | same set | all fire |
| `mode_khat` | κ̂ = 0 in the exact mode | same set | all fire |
| `mode_dF0` | δF = 0 in the exact mode | same set | all fire |
| `th_asign` | sign of a | T4 at the 20 and C1; T7 at the five; T3 at the 19 (all but c = −10) | all fire |
| `xform_p` | p without A R′/R | same set as `th_asign` | all fire |
| `xform_q` | sign of q | same set as `th_asign` | all fire |
| `chart_short` | the table of `hs.KChart` (pi_max = 1e12) instead of `KChartRc`'s | C0 and T4 at c = −10 and −0.01, T3 at c = −0.01 | ρ(1e12) = 49.8 for 104.1 (c = −10), 38.6 for 89.5 (c = −0.01), Θ_gen + r_S c₁ 8.7e5 at c = −10; silent at the other 18 |

Blind spots kept: `rs_one` does not fire T4 at c = −1.001, −1.0001, −0.9999, −0.999 (r_S − 1 < 1e-6, below T4's identity bar of #301; T1 and T1x catch it at 3e-9 … 3e-7); `rs_one` does not fire T5 (its wrong arm sets r_S := 1 itself); T4's Θ_gen + r_S c₁
is blind to `rs_one` (it uses the member's r_S through a(0) = −r_S of the chart); `chart_short` is silent at the 18 members whose table is long enough at pi_max = 1e12 (κ ≥ 0.35: c = −3 and the rest), as it should be; T7 does not fire on `chart_short` (its solver data lie at Π ≤ 6).

## Changes made between the first development run and the runs of record

- **Anchor.** d1 anchored Π = 1 at max(1, ρ_h + 1) (ρ_c = 1 for ρ_h < 0, as #301). T7 then failed at c = −0.1 (pointwise error/scale 7.49e-2 at h = 6.25e-4, bar 5e-2; c₁ fit 8.6e-6, bar 1e-6) and at c = −0.01 (error 7.1e+2, c₁ fit 0.71, ratio 4.00 at every halving):
  e^{−F} at S is large when the anchor sits far outside the horizon (S at ρ = −7, anchor at 1), as #301 saw at c = −0.3 (10.9), and the second-order error constant scales with it. Logs `dev/d1_t7_a.log`, `dev/d1_t7_b.log`, `dev/d1_t7_c-3.log`.
  d2 and d3 anchor at ρ_h + 1 at every member (e^{−F}(S) = O(1)); the step ladder of #301 (0.005 … 0.000625) then suffices at all five, so no member runs with a finer h. T7 error/scale at h = 0.000625: 2.73e-8 (c = −10), 3.73e-6 (−3), 4.34e-5 (−0.5), 1.71e-6 (−0.1), 2.13e-8 (−0.01), ratios 4.00.
  T4 is chart-independent (C1: c = −1.5 with ρ_c = 3, 1.34 and, in #301, 1). The bars of the issue and of T7 were not touched.
- **T3** is not run at c = −10 (first run `dev/d1_five.log`: ValueError, probe ρ = 3 inside the horizon).
- **T2** prints |ratio − 1| from the 120-digit value; #301's version prints the float-rounded value (0.0).
- **T4 has no step h** (the mode is closed form in Π); the h ladder belongs to T7.
- Mutation chains use absolute paths (`run_mut.sh`); the d3 chains started on the first launch.

## Development runs

| run | what | result |
|---|---|---|
| d1 | C0, T3, T4 at the five (anchor max(1, ρ_h + 1)); T1, T1x, T5 at 20; T2 at 3, then 20; X, C1; T7 at the five | all pass but T7 at c = −0.1, −0.01 (above); T1[−0.01] 6.0e-13 |
| d2 | C0, T3, T4, T7 at the five, anchor ρ_h + 1 | 19 of 19 pass |
| d3 | the unmutated default run, 17 mutations of `check`, 3 runs of `derive` | base 146 of 146; fired sets equal the declared ones (20 of 20) |

T4 costs about 1 s per member (T3 + T4), T7 about 30 s per member, the unmutated run 183 s on one process. The d3 `check` runs used the working file before the `derive`, `DECLARED` and `mutations` additions (committed as b54e1f5 with them);
the check code is the same, and the runs of record are compared with `dev/d3_base.log` line by line apart from timings.

## Result (runs of record, code commit b54e1f5, `runs/`)

`check` 146 of 146 (184 s, exit 0, `runs/r_base.log`), `derive` 21 of 21 (3 s, exit 0, `runs/r_derive_base.log`), `table` exit 0 (`runs/table.log`), every `.err` empty. The 17 mutations of `check` (`runs/r_<name>.log`) and the 2 of `derive`
(`runs/r_derive_<name>.log`) exit 1 and fire the declared sets: `static_c1_all.py mutations runs r_` gives 20 of 20 equal, the unmutated run included. The unmutated run of record equals `dev/d3_base.log` line by line apart from timings
(`diff` on the check lines). Launched as three transient systemd units (`nm-i310-rec1` … `rec3`), nice 10, one thread each, about 30 min wall; peak memory 0.55 GB (one T7 member, `dev/d4_mem_T7.err`).

| criterion | result |
|---|---|
| κ r_S c₁ = −c/π to 1e-12 at all 20 | T1x ≤ 7.4e-35 (c = −0.01); T1 ≤ 1.7e-15 at 19, 6.0e-13 at c = −0.01 (bar 1e-12); all 20 pass |
| dM = κ_ξ dA/(8π) to 1e-12 at all 20 | T2 \|ratio − 1\| ≤ 1.6e-18 (c = −0.01), 1.6e-21 (c = −10); M_MS against K L^{3/2}/3 the same |
| Θ_gen + r_S c₁ ≤ 1e-9 at the five | 1.5e-10 (c = −10), 7.6e-12 (−3), 1.1e-12 (−0.5), 4.5e-12 (−0.1), 1.2e-10 (−0.01); the other 15 ≤ 1.1e-11; cut extensions ≤ 6.7e-12 |
| `rs_one` fails at every c ≠ −1 | T5: miss = 1 − 1/r_S at 19 of 19 (3.084e-9 at c = −0.9999 … 0.859 at c = −0.01), holds at c = −1; `--mutate=rs_one` fires T1 and T1x at the 19 and neither at c = −1; T4 at 15 members and C1 |
| each check has a `--mutate=` | 20 of 20 fired sets equal the declared ones |
| secondary | C0 ≤ 2.5e-10 (21 charts); T3 19 of 19 (worst 5.1e-9 of 1e-8, coefficient a at c = −0.01); T7 5 of 5 at the ladder 0.005 … 0.000625 (error/scale at the finest step 2.7e-8 … 4.3e-5, ratios 4.00, every other bar ≤ 8.4e-9); C1 2.6e-12; S0 residual 0; T0 20 of 20 |

Nothing failed in the runs of record. Items that differ from the text of #301 or the task are listed in the note (`notes/black_universe/static_c1_all.md`, Sec. 7): the stock chart cannot be built at ρ_h ≥ 1 and its table is too short at small κ; T4 has no step h; the finer h that #301 needed at c = −0.3 is
an effect of the anchor at ρ = 1 (shown at c = −0.1, −0.01).
