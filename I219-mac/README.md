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

Head `b6d7087` (23 commits on main 7b14116: the 4 of the PR rebased, 19 of this task). CI at the rebase `a12de84`: Build run
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
