# dev_00: the first development runs, before logs were kept

Two development runs were made at a terminal before `dev_01` to `dev_06` were put in files. Their output was seen but not
saved; this note records what they showed. Both were reproduced where noted. Neither is a run of record.

## 1. Underflow of the Taylor coefficients (the first `hp.rs`)

The first `hp.rs` expanded about x0 in h = x - x0 with 1/k and the shifted coefficients of N as plain constants. The planted
case P2 (q + p^2 = 0, start eta = 2, T = 13/10, g = 7/10) to 1e12 gave, in the relative error of F, F', F'' at each checkpoint:

| precision, mode | 200 | 1e3 | 1e4 | 1e6 | 1e9 | 1e12 |
|---|---|---|---|---|---|---|
| DD, project | 3e-32 | 2e-32 | 3e-32 | 3e-32 | 4e-32 | 1e20 to 9e25 (wrong) |
| DD, conserve | 1e-31 | 2e-31 | 4e-31 | 9e-31 | 2e-30 | 1e20 to 9e25 (wrong) |
| QD, project | 1e-64 | 7e-65 | 3e-65 | 2e20 to 2e26 (wrong), then NonFinite at x = 2.9e5 | | |
| QD, conserve | as QD project | | | | | |

A trace of the QD walk (`--trace`) ended at x = 292119 with `NonFinite`, the last good steps h = 2.5e4 at x = 2.7e5. The cause:
the Taylor coefficients about x0 scale like x0^-k, so at x0 = 3e5 and order 60 they are 1e-330, below the smallest double,
and for DD (order 30) at x0 = 1e12 they are 1e-360. The low parts of a multi-double underflow to zero or a subnormal. The fix
(in `hp.rs`, commit 880c1a9): the step variable is s = (x - x0)/L with L the power of two nearest the previous step, which
changes only the constants (1/k becomes L/k and the shifted coefficient e_j becomes e_j L^j, both exact scalings by a power of
two) and leaves c_k L^k of order one. After it P2 passes at roundoff to 1e12 in all four configurations (`dev_02`).

## 2. #167's baseline crate

The crate of #167 was built unchanged (1 min 4 s on the Pi, `cargo build --release -j 2`, 4 warnings of its own) and its
`forward` command run on F(0) in {1.5, 2, 3, 5}, F'(0) in {1, 10, 100}: all 12 plus sides LOGLOG with q/p^2 + 1 between -1.8e-4 and
-4.5e-2 at 200, in 1.6 s. `fwdstate 5 100 200` gave F = 59.54 (G is large for large F'(0); this sets the eta at which
the root series with K terms reaches 1e-10, and is why README W2 states its bar at eta >= 1e3), and `fwdstate 5 100 1e5` stopped at
`StepLimit` (4001 steps, the old plan's largest step is 10): the old walker cannot reach 1e12, which is why the new one has
an unbounded step and its own planner.
