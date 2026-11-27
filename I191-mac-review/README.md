# I191-mac-review: the coordinator's review of #191 (rerun, independent check ind191)

Machine: macOS (the coordinator's Mac, Apple M5, arm64), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`:
mpmath 1.3.0), Rust 1.94.0, nice 10, at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/191.
Under review: multisolver pull request #26 (`feat/locate-singularity` at 0db3966), branch
`wip/i191-singularity-locator` at 71ebf1c, raw `I191-rpi5` at d19334b. Written 2026-11-27 before the first run of
`ind191.py`.

## Rerun

`cargo test --release --test locate -- --nocapture` in a clone `~/Source/negative-mass-r191/multisolver` at 0db3966
(`rerun_test_locate.log`). The suite prints a fingerprint of the locator's results on every cell. The runner reports
0xa5113e9ccb6776c8 on aarch64 NEON (the Pi), with `portable`, and in the PR's x86 CI. This Mac is a fourth build.

## ind191: three planted series of the coordinator's choosing

A Rust harness (`harness/`, depending on the clone by path) reads a series' coefficients as decimal strings, rounds
them to the lane, calls `locate(&c, &Opts::default())`, and prints the result. `ind191.py` makes the coefficients in
mpmath at 150 digits from closed forms, then compares. None of the three is a case of the suite:
- **L1**, a logarithm: f = −ln(1 − x/s*) with s* = 1.7, so c_0 = 0 and c_k = 1/(k s*^k). Expected kind Real, s = 1.7,
  α = 0. This is the log end #203 needs to recognize.
- **L2**, a branch point dressed by an entire function: f = cosh(x)·(1 − x/s*)^{−3/2} with s* = −2.3, by the Cauchy
  product. Expected Real, s = −2.3, α = −3/2.
- **L3**, a complex pair with a fractional exponent: f = (1 + x²/4)^{−1/3}. Expected Pair, s = 2i (re 0, im 2),
  α = −1/3.

Lanes f64, dd and qd at K = 30, 60 and 120 (the suite's orders per lane): nine cells.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | In each of the nine cells the kind is the expected one (Real, Real, Pair) |
| K2 | In each of the nine cells the bars cover the truth: \|s − s*\| ≤ `bar` and \|α − α*\| ≤ `alpha_bar` |

## Mutations (`--mutate=NAME`; each must make ind191 exit non-zero with exactly these criteria failing)

| mutation | change | targets |
|---|---|---|
| `wrong-s` | the reference s* of L2 is −2.3·(1 + 1e-2) | K2 |
| `pair-as-real` | L3's expected kind is Real | K1 |

## Runs (filled in as they are done)

| file | what |
|---|---|
