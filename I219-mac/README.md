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
