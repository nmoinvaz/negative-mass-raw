# I219-mac: rebase multishoot#73 onto main and answer its CodeRabbit review

Machine: the coordinator's Mac (Apple M5, arm64, macOS), shared with other sessions: at most 2 processes, nice 10.
rustc/cargo 1.94.0. Issue: https://github.com/nmoinvaz/negative-mass/issues/219. PR:
https://github.com/nmoinvaz/multishoot/pull/73 (branch `feat/implicit-taylor-r2`, head eaf55a8 on main 70fea18). Clone:
`~/Source/negative-mass-i190-libs/multishoot`. Written 2026-11-26 before the first run, after reading multishoot's CLAUDE.md,
`src/implicit.rs`, `tests/implicit.rs`, #190's closing comment and the 20 review threads.

Not merged, no release; the maintainer merges by rebase. Pushes to the PR branch only, the first with
`--force-with-lease`.

## Plan

1. Digests at the current head eaf55a8, before the rebase: `cargo test --release -j 2 --features mutate --test implicit --
   --nocapture --test-threads=2` (log `pre_eaf55a8_*.log`). Expected: dd 92ec461781147d77, f64 b124d44e9758f1a1, qd
   75902b0bf76ced2a.
2. Rebase onto origin/main (7b14116), fmt, clippy (`mutate`, `portable,mutate`, none), the full suite with `mutate` and with
   `portable,mutate`, digests compared with step 1. Push with `--force-with-lease`, wait for CI, post on #219.
3. The threads, the six majors first (below), then the fourteen minors. Each real defect: a test that fails without the fix,
   a control under `--features mutate` that makes the test fail (run once, log kept), one commit. Not-real threads: a
   one-sentence reason. Suite and digests after each batch. Every digest change is reported with the fix that caused it.
4. CI green on every job, every thread answered, closing comment on #219, handover.

## Pass criteria, written before the first run

| id | criterion |
|---|---|
| P1 | The rebase is conflict free or each conflict keeps both sides' intent; the three digests after it equal those at eaf55a8 on the default build and on `portable` |
| P2 | Each fixed thread has a test that fails when its control is on (log shows the failure) and passes when it is off |
| P3 | No existing test is edited to make it pass; where a test's assertion changes by intent (threads 4, 5, 6) that is said in its commit |
| P4 | fmt, clippy (`mutate`; `portable,mutate`; none) clean; the suite passes with `mutate` and `portable,mutate`; CI green on every job |
| P5 | A fix that moves a digest says which and why; a fix that must not move one (the guards, the diagnostics) leaves them equal |

## The six majors

| # | thread | line | claim | first check |
|---|---|---|---|---|
| 1 | `l^j` rounded to f64 underflows | `src/implicit.rs:499` | `lps[j] = l^j` underflows at `l = 2^-600`, j = 2, so `y''_2` of `N = y'' - 2^1000 x^2` is 0, not 2^-200 | reproduce with the f64 walker; scale by the exponent in pieces |
| 2 | `advance` on a stale series | `:1070` | `form`, `advance`, `advance` gives `[0.5, 1, 1]` for y'' = 1, not `[2, 2, 1]` | reproduce; a `ready` flag cleared by `advance`, `set_y` and a failed `form` |
| 3 | no crossing check on the last accepted step | `:1113` | one step -1 to 1 on N = y''^2 - x^2 reports no crossing | reproduce; check the end point's A0 sign without projecting |
| 4 | step-sum passes on a non-finite error | `tests/implicit.rs:701` | `f64::max` drops NaN | test that feeds a NaN coefficient |
| 5 | step-sum passes on a wrong stop | `:705` | `path_steps` returns a prefix without the stop | return the stop; require it and the samples |
| 6 | coefficient observation mixed into a gated check | `:789` | `coeffs` is `recorded = true`, so its header's criterion cannot fail | split: a gated criterion on the supported contract, the observation labelled as one |

## Logs

Every command's output goes to a log here, numbered when rerun; logs are never overwritten. `pre_*` is before the rebase,
`post_*` after it, `fixN_*` after each fix, `ctl_*` the control runs, `ci_*` the CI runs.

## Results (2026-11-27)

Head `b6d7087` (24 commits on main 7b14116: the 4 of the PR rebased, 20 of this task). CI at the rebase `a12de84`: Build run
45949911354 and Lint run 45949911352, every job green. CI at `02691af`: Build run 45952318413, Lint run 45952318357, every job
green (Windows included). CI at `b6d7087` (docs only): Build run 45953693108, Lint run 45953693119.

### Digests (`cargo test --release --features mutate --test implicit -- --nocapture`)

| digest | eaf55a8 (before the rebase) | a12de84 (rebased) | b6d7087 |
|---|---|---|---|
| `digest dd` | 92ec461781147d77 | 92ec461781147d77 | 92ec461781147d77 |
| `digest f64` | b124d44e9758f1a1 | b124d44e9758f1a1 | b124d44e9758f1a1 |
| `digest qd` | 75902b0bf76ced2a | 75902b0bf76ced2a | 75902b0bf76ced2a |
| `digest-full dd, f64, qd` | (did not exist) | | 13ac06786e54ccb1, 50775575530f4fa9, b37fa8d9cb20094f |
| `digest od`, `digest-full od` | (did not exist) | | c542a935a4215b82, 801e3f57cd16e9b1 |

Equal on aarch64 NEON (default build), `--features portable`, with and without `mutate`, and, through the pinned constants
in the tests, on every CI job (SSE2, portable, AVX2 with `-C target-feature=+avx2,+fma`, ARM64 NEON, macOS NEON, MSVC).
No fix moved a planted digest or a printed planted value: `planted_compare.txt` (167 lines before, 0 changed, 27 new
lines of the new checks). The only digests that differ are the new ones of thread 20 (`digest-full`, `digest od`).

### Threads and commits

| # | thread | verdict | commit | test | control (feature `mutate` unless said) | log of the control's firing |
|---|---|---|---|---|---|---|
| 1 | README:96 `\|A0\|` | fixed (the thread was deleted by CodeRabbit before the reply) | e7a3df3 | the row has 3 pipes | none (docs) | |
| 2 | README:107 Project | fixed | e7a3df3 | docs | none | |
| 3 | src:222 `taylor_shift` empty | fixed | 97ab1ff | `shift_edges` | `EmptyShift` | fix10_shift_mutate.log |
| 4 | src:499 `l^j` (major) | fixed | b52b50e | `underflow` (f64) | `PlainScale` | fix1_underflow_mutate.log |
| 5 | src:550 reciprocal | fixed | 9d0b921 | `reciprocal` (f64) | `PlainReciprocal` | fix11_recip_mutate.log |
| 6 | src:924 repeated crossing | fixed | b6630a0 | `repeat_form` | `RepeatCrossing` | fix3_repeat_mutate.log |
| 7 | src:995 rho | fixed | 2b05b94 | `rho_scale` (f64) | `PlainRho` | fix12_rho_mutate.log |
| 8 | src:1070 stale series (major) | fixed | 6547399 | `stale` | `StaleSeries` | fix2_stale_mutate_2.log |
| 9 | src:1107 duplicate checkpoints | fixed | 682eb5a | `dup_checkpoints` | `NoDedup` | fix8_dedup_mutate.log |
| 10 | src:1113 last step (major) | fixed | e25569b | `last_crossing` | `NoEndCrossing` | fix4_end_mutate.log |
| 11 | src:1145 zero only for Pivot | fixed | b68b9de | `zero_only_pivot` | `KeepZero` | fix9_zero_mutate.log |
| 12 | tests:342 non-finite crossing | fixed | 0fe9e37 | `crossings`, `closed_form` | `NanPos`, `NanState` (test-side) | fix13_nanpos_mutate.log, ctl_old_fix13_*.log |
| 13 | tests:461 planner control | fixed | 5675c3a | `planner` | `FlipBit` (test-side) | fix14_planner_mutate.log |
| 14 | tests:701 NaN step sum (major) | fixed | 24933e4 | `step_sum` | `NanCoeff` (test-side) | fix5_nan_stepsum_mutate.log, ctl_old_fix5_*.log |
| 15 | tests:705 wrong stop (major) | fixed | 26ff096 | `step_sum` | `Cut(0)`, `Cut(3)` (test-side) | fix6_cut_mutate.log, ctl_old_fix6_cut.log |
| 16 | tests:789 coeffs (major) | fixed | 7897d40 | `coeffs` (gated) | `BadCoeff` (test-side), `SkipOrder(3)` | fix7_coeffs_ctl_mutate.log |
| 17 | tests:911 NaN lane | fixed | 6a2fdfd | `lanes` | `NanLane` (test-side) | fix15_lanes_mutate.log, ctl_old_fix15_lanes.log |
| 18 | tests:923 lane control | fixed | 6a2fdfd | `lanes` | `LanePerturb`, `NanLane` | fix15_lanes_mutate.log |
| 19 | tests:937 AVX2 | fixed: the digests are pinned, the AVX2 job passes them | 02691af | `digest_*` | `digest_pinned_fails_on_a_flip`, a wrong constant (ctl_old_fix17_pinned_wrong.log) | ci_avx2_02691af_2.log |
| 20 | tests:949 checkpoints, OD | fixed | 15b83c4 | `digest_od`, `digests` | `digest_sees_a_checkpoint` | fix16_digest_mutate.log, ctl_old_fix16_digest.log |
| 21 | README:98 (new, 2nd review) crossings list | fixed in the docs; the detection is not changed | b6d7087 | docs | none | |
| 22 | README:102 (new, 2nd review) multiplicity | fixed | b6d7087 | docs | none | |

`ctl_old_*` logs: the pre-fix text put back for one run, the control's test fails (it "did not fire" on the old code).
`ctl_old_fix7_coeffs.log` is a run of `misc_f64` with `coeffs` ungated: it passes, as the old arrangement did, and shows nothing
more. Also not a result: `ci_avx2_02691af.log` is the "run is still in progress" message of a log fetch, kept; the log is
`ci_avx2_02691af_2.log`.

### Also changed

- `070f302`: 6 `needless_range_loop` sites that clippy 1.94.0 flags on this Mac and CI's clippy does not.
- API: `Stop::NotFormed` (new variant), `Scalar::is_finite` (new required method), `ImplicitControl` variants and
  `taylor_shift_with` under `mutate`.
- Behaviour: `Walker::advance` refuses a stale series; `run` also checks the end of the last accepted step; `WalkOut::zero`
  is `None` unless the stop is `Pivot`; the digest tests assert pinned constants.

## Round 2 (second request on #219, 2026-11-27)

Head after round 1: b6d7087. Head now: 5513db7 (21 new commits on the branch, all plain pushes, no rebase). Not merged, no
release. Reopened four threads that CodeRabbit had not accepted, requested full reviews (`@coderabbitai review`) at 07:12,
08:20, 08:51, 09:24 and 09:51 UTC, and answered what each review found. After 09:24 the coordinator's stopping rule applied:
fix every major finding with a test and a control, fix minor ones where the fix is small and tested, otherwise answer in one
sentence and leave the thread, and request exactly one more full review if a major finding needed a code change (09:51).

### Digests before and after (`digest`, `digest-full`, as printed by the `digest_*` tests)

| lane | before (b6d7087) | after (5513db7) |
|---|---|---|
| f64 | b124d44e9758f1a1, 50775575530f4fa9 | unchanged |
| dd | 92ec461781147d77, 13ac06786e54ccb1 | unchanged |
| qd | 75902b0bf76ced2a, b37fa8d9cb20094f | unchanged |
| od | c542a935a4215b82, 801e3f57cd16e9b1 | 10f1b89a823ad3c3, 1d9549c94134d037 |

od changed on purpose: eight parts per value (`parts` had four), then the K-A step-sum series (full 21d526b7c72a4319), then
the planned step lengths (full 1d9549c94134d037). Logs: `r2_digest_first_run_2.log` (the first od values),
`r2_od_pinned_all_mutate.log`, `r2_new_findings_b_all_mutate.log`. Identical on the default and `portable` builds
(`r2_final_*_portable_mutate.log`) and on CI's AVX2 job (`r2_ci_avx2_*.log`, `digest_od ... ok`).

### Findings by review

| review of | new | fixed | answered, not changed |
|---|---|---|---|
| reopened threads (b6d7087) | 4 | 4 (one answered with the run output) | 0 |
| f1bc2ec | 8 | 8 (3 docs) | 0 |
| 20a77cc | 7 | 7 (1 docs) | 0 |
| 3d6dd53 | 9 | 9 (1 docs) | 0 |
| e3fdc90 | 3 | 3 | 0 |
| 1fa9869 | 4 | 3 | 1 |
| total | 35 | 34 | 1 |

Follow-up replies by CodeRabbit on threads already fixed: 7. Fixed 2 (src:1045 end crossing as a preview; src:1111 a sign
change just beyond a tangent zero), answered with runs 2 (tests:846, tests:949: the matrix of runs), answered not changed 3
(src:1144 and src:1173: the quotient a0 / a1 itself overflows; src:1111: a root 2.0078125 within a hundredth of a half-bracket
of the tangent zero). 52 threads on the PR at the end, 51 resolved, 1 open (src:1260).

### Each finding

| review | finding | outcome | commit | check | control |
|---|---|---|---|---|---|
| reopened | README:107 `Project` wording | fixed (twice) | 5f0d240, ae24d37 | docs | none |
| reopened | tests:461 last-bit control run | answered with the run | | `controls_without_hooks` | `r2_final_*_controls_without_hooks.log` |
| reopened | tests:949 digest | fixed, answered with runs | f1bc2ec, 7b14a17 | `digest_od`, `digest_od_sees_the_lower_parts` | `Poke::EndLower`, `SumLast`, `SumStep`; `r2_ctl_old_od_*.log`, `r2_ctl_old_nohash_h.log` |
| reopened | README:102 crossing wording | fixed | 6cc2c94 | docs | none |
| f1bc2ec | README:98, README:116, src:16 | fixed in the docs | ae24d37 | docs | none |
| f1bc2ec | src:259 `taylor_shift` about 0 | fixed | af79e35 | `shift_zero_point` | `NanCoeff` (test-side); `r2_ctl_old_shift_zero.log` |
| f1bc2ec | src:1045 non-finite end pivot | fixed; end crossing a preview | 6707ef9, 20a77cc | `end_pole`, `end_preview` | `NoFiniteEnd`, `RecordEnd`; `r2_ctl_old_end_pole.log` |
| f1bc2ec | src:1117 linear pivot slope squared | fixed | 1a03636 | `linear_pivot` | `PlainRho`; `r2_ctl_old_linear_pivot.log` |
| f1bc2ec | tests:846 step lengths in the digest | fixed | 7b14a17 | `digest_od_sees_the_lower_parts` | `Poke::SumStep`; `r2_ctl_old_nohash_h.log` |
| f1bc2ec | tests:1077 lanes one at a time | fixed | 332d95c | `lanes_controls` | `r2_ctl_old_lane_v_only.log`, `r2_ctl_old_lane_u_only.log` |
| 20a77cc | README:113 `Conserve` outcomes | fixed in the docs | 3d6dd53 | docs | none |
| 20a77cc | src:1031 sign compared and stored | fixed | f1c0812 | `two_samples` | `LastSign`; `r2_round3_tests_on_old_src.log` |
| 20a77cc | src:1112 located without a closed bracket | fixed | 6eb4b78 | `located_far` | `OpenBracket`; `r2_round3_located_far_on_old_src.log` |
| 20a77cc | src:1144 small quadratic coefficient | fixed | 265fdc7 | `quad_small_coeff` | `ScaledQuad` |
| 20a77cc | src:1159 infinite coordinate | fixed | 265fdc7 | `overflow_coordinate` | `NoFiniteZero` |
| 20a77cc | tests:1690, tests:1762 controls | fixed | 8336338, 265fdc7 | `shift_zero_point`, `linear_pivot` | `NanCoeff`, `PlainRho` |
| 3d6dd53 | src:1018 location from the last formed state | fixed in the docs | e3fdc90 | docs | none |
| 3d6dd53 | src:1109 midpoint overflow | fixed | 68f404a | `midpoint_overflow` | `SumMidpoint` |
| 3d6dd53 | src:1111 zero midpoint | fixed, then probes closer | 68f404a, 63671f0 | `tangent_midpoint`, `tangent_near_root` | `ZeroMid` |
| 3d6dd53 | src:1173 fallback overflow | fixed | 45af622 | `rho_fallback_overflow` | `DoubleFirst` |
| 3d6dd53 | src:1189 numerator overflow | fixed | 45af622 | `zero_numerator_overflow` | `ProductFirst` |
| 3d6dd53 | tests:1687, 1791, 1843, 1897 | fixed | e3fdc90, 45af622, 68f404a | the checks named | `NanCoeff`, `ScaledQuad`, `OpenBracket`, `WrongStep` |
| e3fdc90 | src:1170 backward bracket (major) | fixed | 63671f0 | `backward_crossing` | `BackwardBracket`; `r2_round5_tests_on_old_src.log` |
| e3fdc90 | src:1245 numerator underflow | fixed | 1fa9869 | `zero_numerator_underflow` | `ProductFirst` |
| e3fdc90 | src:1250 `s l` overflow | fixed | 1fa9869 | `coordinate_overflow` | `ProductX` |
| 1fa9869 | src:1260 scale after the displacement rounds | answered: out of scope, a follow-up | | | |
| 1fa9869 | tests:1941, 2032, 2190 | fixed | 5513db7 | `backward_crossing`, `coordinate_overflow` | `NanPos` (test-side) |

### Runs and CI

Local, at 5513db7 (this Mac, aarch64 NEON, 2 threads, nice 10): the implicit suite with `mutate` (34 tests) and with
`portable,mutate` (34 tests), `controls_without_hooks`, `cargo fmt --check`, clippy in `mutate`, `portable,mutate` and no
features, `RUSTDOCFLAGS="-D warnings" cargo doc`: all exit 0 (`r2_round6_*.log`, `r2_final_5513db7_*.log`). 81 control cells
fire. CI at 5513db7: Build run 45980245585 (SSE2, portable, AVX2, NEON, macOS NEON, MSVC, MSRV, mutation controls, Coverage)
and Lint run 45980245696 (Rustfmt, Clippy x3, Docs) all success (`r2_ci_avx2_5513db7_done.log`;
`r2_ci_avx2_5513db7.log` is the 82-byte "still in progress" fetch, kept).

### Also changed

- API: `ImplicitControl` (feature `mutate`) has 12 new variants: `RecordEnd`, `ScaledQuad`, `NoFiniteZero`, `DoubleFirst`,
  `ProductFirst`, `ProductX`, `OpenBracket`, `ZeroMid`, `SumMidpoint`, `BackwardBracket`, `LastSign`, `NoFiniteEnd`.
  `PlainRho` is now the unscaled formula with no linear shortcut.
- Behaviour: the crossing at the end of a `run` is in the result and not recorded in the walker (a resuming `form` records it);
  a crossing is compared with the first `form`'s sign at each start; `located` needs a closed bracket; `WalkOut::zero` is
  `None` where `beta` is not positive or the coordinate is not finite; a zero midpoint of a wide bracket is resolved by the
  signs near it.
