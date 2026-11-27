# I190-mac-review: the coordinator's review of #190 (rerun, independent check ind190)

Machine: macOS (the coordinator's Mac, Apple M5, arm64 NEON), Rust 1.94.0, Python 3.14.7
(`/Users/nathan/Source/negative-mass/.venv`), nice 10, at most 2 processes. Issue:
https://github.com/nmoinvaz/negative-mass/issues/190.

Under review:
- multishoot pull request #73 (`feat/implicit-taylor-r2` at eaf55a8, on main 70fea18), in a clone
  `~/Source/negative-mass-r190/multishoot`;
- the crate branch `wip/i190-implicit-taylor` at 550800c, in a worktree `~/Source/negative-mass-r190/nm`;
- raw `I190-rpi5` at 5f2ac0f.

Written 2026-11-27 before the first run of `ind190` and before the rerun.

## Rerun

1. `cargo test --release -j 2 --features mutate --lib --test implicit --test taylor --test taylor_order --test plane --
   --nocapture --test-threads=2` in the clone at eaf55a8, as the Pi's `run_36`. The same with `--features
   portable,mutate`, as `run_37`. The digest lines are compared with the Pi's: dd 92ec461781147d77, f64 b124d44e9758f1a1,
   qd 75902b0bf76ced2a, and the plane digests. This Mac is aarch64 NEON like the Pi, so equal digests are expected.
2. The crate at 550800c with `--features implicit_lib`, built on this Mac. Then
   `conical_offgrid.py --grid=ctl --no-controls --dump=DIR` (16 checks) and `conical_loglog.py` (20 checks, 17
   controls), compared with the Pi's baseline logs and dumps (`run_06`, `run_09`, `dump_base_ctl`) by the Pi's own
   `sys/compare_outputs.py`. The expectation: 16 of 16, 20 of 20 and 17 of 17, with every η*, class and kind equal to the
   baseline as printed.

## ind190: three planted implicit equations of the coordinator's choosing

A Rust binary (`harness/`, depending on the clone by path) drives `multishoot::implicit::Walker` on three equations
that are not in the PR's tests. Each A_g is a polynomial in x passed through `taylor_shift`.

- **E1, a fold:** N = y″² − 4(1 − x). The branch y″ = 2√(1 − x) from (y, y′, y″) = (0, 0, 2) at x = 0 has the closed
  form y = (8/15)(1 − x)^{5/2} + (4/3)x − 8/15. A0 = 2y″ vanishes at x = 1 with exponent ½. The walk targets x = 2 with
  a checkpoint at 0.9.
- **E2, two roots crossing:** N = (y″ − 2y)(y″ + y) = y″² − y y″ − 2y².
  - Branch P, from (1, √2, 2): y = e^{√2 x}, walked to x = 2.
  - Branch C, from (1, 0, −1): y = cos x. On it A0 = 2y″ − y = −3y vanishes at x = π/2, where the two roots meet. Walked
    to x = 3 with `Project`.
- **E3, three real roots:** N = (y″ − y′)(y″ + y′)(y″ − 2y′) = y″³ − 2y″²y′ − y″y′² + 2y′³.
  - Branch M, the middle root, from (1, 1, 1): y = eˣ, walked to x = 2.
  - Branch T, the top root, from (½, 1, 2): y = e^{2x}/2, walked to x = 2.

Lanes f64, dd and qd at the PR's own orders and tolerances (22, 42, 80 and 1e-14, 1e-30, 1e-62), with hmax 0.3.

## Criteria (each coded as worded; each can fail)

bar = 1e-9 (f64), 1e-25 (dd), 1e-56 (qd).

| id | criterion |
|---|---|
| K1 | In each lane, E2-P (`Project` and `Conserve`), E2-C (`Project`), E3-M (`Project` and `Conserve`) and E3-T (`Project`) end with `Stop::End`, and each has \|y − y_exact\| / \|y_exact\| ≤ bar at its end point |
| K2 | In each lane, E2-C reports exactly one crossing, located, with \|x − π/2\| ≤ bar |
| K3 | In each lane, E1 stops with `Tiny`, `Pivot` or `ZeroPivot` at x_stop, with 0 < 1 − x_stop ≤ 1e-3. At its checkpoint x = 0.9, \|y − y_exact\| / \|y_exact\| ≤ 1e3 · bar |

## Mutations (`--mutate=NAME`; each must make ind190 exit non-zero with exactly these criteria failing)

The targets are predicted from the code, not yet computed. A mutation that misses its targets is reported.

| mutation | change | targets |
|---|---|---|
| `wrong-root` | E3-M starts on the top root, (1, 1, 2), and is compared with eˣ | K1 |
| `cross-at` | K2's expected crossing is π/2 + 1e-3 | K2 |
| `fold-at` | K3's fold is taken at x = 0.99 | K3 |

## Runs (filled in as they are done)

| file | what |
|---|---|
| `ind190_run1.txt` | run 1: **exit 0, 3 of 3.** K1: all 18 walks reach `End`. The worst relative errors are 2.6e-16 (f64), 1.25e-32 (dd) and 4.0e-65 (qd), against bars of 1e-9, 1e-25 and 1e-56. K2: E2-C reports exactly one located crossing in each lane, at π/2 to 0 (f64), 1.2e-32 (dd) and 1.1e-64 (qd). K3: E1 stops `Tiny` within 3.4e-13 to 5.2e-13 of the fold at x = 1, and its checkpoint at 0.9 matches the closed form to 0 (f64), 2.8e-32 (dd) and 2.8e-65 (qd) |
| `ind190_run1_mut_*.txt` | `wrong-root` fails exactly K1 (relative error 2.76 in every lane). `cross-at` fails exactly K2. `fold-at` fails exactly K3 |
| `rerun_lib.sh`, `rerun_lib_default.log`, `rerun_lib_portable.log` | the library suite at eaf55a8: everything passes, default and `portable`. **The digests equal the Pi's** (dd 92ec461781147d77, f64 b124d44e9758f1a1, qd 75902b0bf76ced2a), on both backends |
| `rerun_crate.sh`, `rerun_build_on.log`, `rerun_on_offgrid_ctl.log`, `dump_on_ctl_mac/` | the crate at 550800c with `implicit_lib`: offgrid `ctl` passes 16 of 16, in 237 s at load 7 to 8. The Pi's comparator against its baseline (`run_06`, `dump_base_ctl`) finds **all 537 η* equal in the 10 printed digits** (largest relative difference 2.45e-15), and every class and kind equal. Its two flagged differences are the review's own: the `/usr/bin/time` lines of this wrapper, and one dump file named by a hash of its absolute path. That file's contents are identical apart from its first line, which holds the path |
| `rerun_on_loglog.log` | run 1 of loglog: **crashed** (FileNotFoundError). The review worktree sits one level deeper than the script's relative path `../../../negative-mass-raw` assumes. This is a defect of the review's setup, not of the code; it is kept as run 1. Fixed for run 2 by the symlink `~/Source/negative-mass-r190/negative-mass-raw` |
| `rerun_on_loglog_2.log`, `ctl_on_loglog_mac2/` | run 2 of loglog with `implicit_lib`: **20 of 20 checks, every control fired on its target only**, in 226 s. The Pi's comparator against its baseline `run_09` compares 124 lines; its one gated difference is the line count (124 against 143), which is this wrapper's `/usr/bin/time -l` output. No η*, class or kind differs |
| PR #73's CI (not run here) | **The CI fails**, on Ubuntu NEON, x86_64 AVX2 and Windows SSE2 and in coverage, in one test only: `tests/slaved.rs` `slaved_residual_returns_the_factorization_error` ("series_lus: order 53: singular or non-finite pivot at column 0 (NaN)"). That test is not part of #73, and **multishoot main at 70fea18 fails the same test in CI**: a defect already on main. The CI does not assert the implicit digests, so it says nothing about AVX2 bitwise equality |
| `ind190_run2_b6d7087.txt` | the same harness rebuilt against multishoot#73 after #219's rebase and review fixes (b6d7087): **3 of 3, every case line identical to run 1 at eaf55a8** |
