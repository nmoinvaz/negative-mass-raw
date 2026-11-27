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
