# I206-mac-review: the coordinator's review of #206 (multisolver PR #28)

Machine: macOS (the coordinator's Mac, Apple M5, aarch64 NEON), Rust 1.94.0, nice 10, `-j 2`. Issue:
https://github.com/nmoinvaz/negative-mass/issues/206. Under review: multisolver PR #28 at 21b9829 (c5b5ea7, 21b9829 on main
63d6e4d), raw `I206-mac` at 035fc85, note branch `wip/i206-locate` at b1633d8.

## What was checked

| check | result |
|---|---|
| PR state | MERGEABLE; every CI check SUCCESS (15) |
| `cargo test --release --test locate` at 21b9829, in the runner's clone (`rerun_test_locate.log`) | 9 passed, 0 failed, 4 ignored, 24.5 s, the runner's numbers |
| the fingerprint disagreement the runner reports | confirmed: multisolver main 63d6e4d `tests/locate.rs:739` asserts `0xf3a1_3cba_157d_2e3c`; `notes/warp/singularity_locator.md` lines 52 and 160 quote 0xa5113e9ccb6776c8 |
| scope | the PR's two commits touch `locate`'s grid and its tests; the negative-mass branch adds only `singularity_locator_206.md` |

No independent locator was written for this review: the PR changes a default grid and adds tests whose expected values are
the runner's runs, and CI reproduces them on five targets. The unmet criteria (D6 in f64, one confidently wrong weak result)
are recorded by assertions in the tests themselves.
