# I167-mac-review: the coordinator's review of #167 (rerun, independent check ind167)

The runner's raw folder for #167 is `I167-mac` (it ran on this Mac), so the review uses this folder name.

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, mpmath 1.3.0
(`/Users/nathan/Source/negative-mass/.venv`), Rust 1.94.0, at nice 10 with at most 2 processes. Issue:
https://github.com/nmoinvaz/negative-mass/issues/167. Under review: branch `wip/i167-conical-global` at 12f47dd, raw
`I167-mac` at 0134f16. Stop condition: any single run not finished after 1 h of wall time is stopped (by its PID) and
reported. Written 2026-11-26 before the first run of `ind167.py`.

## Rerun of the runner's default mode

`python3 notes/warp/conical_global.py --fresh` from a worktree at 12f47dd, after `cargo build --release -j 2` of the crate.

## ind167.py: what it shares with #167

Shared: sympy and mpmath; the block entries of a conical shift (`det_classify.md` §6, C9b) and D's formula (#65); the
claims under test. Not shared: ind167 imports nothing from the repository and does not use the crate. Its N is its own
(sympy's determinant of the block), and so are its root tracking and its integrator.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| L1 | 8 det(block) in (F, F′, F″, η) equals the note's a₃F″³ + a₂F″² + a₁F″ + a₀ (§1) exactly |
| L2 | N(F, F′, F″; 0) = 2F′²(F² − 1)(FF″ + F′²) and ∂N/∂F″ at η = 0 equals 2F′²F(F² − 1), exactly |
| L3 | With F = 1 + (2/5)η² + Bη⁴ + B₃η⁶: the lowest-order equations of N in η that contain B, then B₃, are linear and solved uniquely by B = −22/125 and B₃ = 998/10625; and with F = 1 + bη², the η⁴ coefficient of N is 64b³(5b − 2) |
| L4 | The small-F balance: the monomials F^iF′^jF″^k of N with i + j + k = 4 and j + 2k = 6 sum to −η²(η² + 1)F″²[(η² + 2)F′² + 2FF″]; every other monomial has i + j + k ≥ 4 and j + 2k ≤ 6, and is not of both i + j + k = 4 and j + 2k = 6. So under F ~ c(η − η*)^α, 0 < α < 1, that balance is the most singular, and it vanishes iff α(η*² + 4) = 2 |
| L5 | Re-solve (numerical evidence): ind167's own inward integration of N = 0 for (F_∞, C) = (1, 0), from the series through η⁻⁴ at η = 1000, on the root of the cubic nearest the series' F″, tracked by continuity, ends with F → 0 at η* within 1e-4 of 1.28193326312 |

## Mutations (`--mutate=NAME`; each must make ind167 exit non-zero with exactly these criteria failing)

| mutation | change | targets |
|---|---|---|
| `d-sign` | the block's Y entry with + F w/2 in place of − F w/2 | computed in a dev run of this mutation alone before run 1, then declared in an amendment; prediction L1, L3, L4 (not L2: at η = 0, Q = 0 and Y enters D only squared) |
| `eta0-coef` | L2 expects 3F′²(F² − 1)(FF″ + F′²) | L2 |
| `even-b` | L3 expects B = −21/125 | L3 |
| `balance-coef` | L4 expects (η² + 3) in place of (η² + 2) | L4 |
| `start-C` | L5 starts from C = 10 | L5 |

L5 integrates the unmutated N in every run, so `d-sign` acts on L1 to L4 only.

## Amendments

**A1 (2026-11-26, after the dev run `dev/dev1_d-sign.txt`, before run 1).** `d-sign` alone fails L1, L3, L4 and not L2,
as predicted; its declared targets are L1, L3, L4. In the same dev run L5 failed, and L5 uses the unmutated N: the walk
ends at η = 1.2815844 (F = 9.9e-5) against 1.28193326312, 3.5e-4 apart, outside the 1e-4 tolerance. So L5 as worded will
fail in run 1 as well; run 1 is run as committed, and the cause is examined after it.

**A2 (2026-11-26, after run 1, before run 2).** Run 1 fails L5 as worded, by a defect of the coordinator's design: η* =
1.2815843809 against 1.28193326312. An absolute error δF at η shifts the solution's C by about δF·η⁴, and `start-C`
measures dη*/dC ≈ −0.08 (C = 10 gives η* = 0.449). The 4-term series at η = 1000 is truncated at about 1e-15·η⁰, which
gives δC of a few 1e-3, enough for 3.5e-4 in η*. The diagnostic `dev/l5_start.py` (`dev/l5_start.log`) makes it worse
with a later start (η₀ = 1e4: 1.2800, 1e5: 1.0976), as the RK4 error at large η enters C the same way. Run 2's L5 starts at
η = 200 from ind167's own series through ν⁸ with logs, whose stages it solves from its own N (θ-form); the criterion and
tolerance are otherwise unchanged. Whether it passes is not known when this is written.

## Runs (filled in as they are done)

| file | what |
|---|---|
| `dev/dev1_d-sign.txt` | the dev run that set `d-sign`'s targets (A1) |
| `ind167_run1.txt`, `ind167_run1_mut_*.txt` | run 1: exit 1, 4 of 5; L5 failed by the coordinator's start data (A2): η* = 1.2815843809. Each mutation fired its target plus L5 |
| `dev/l5_start.py`, `dev/l5_start.log` | the start-point diagnostic behind A2 |
| `ind167_run2.txt` | run 2: exit 0, 5 of 5 criteria pass. L5: η* = 1.28193249506 against #167's 1.28193326312, 7.7e-7 apart. The own series through ν⁸ at (F_∞, C) = (1, 0) has a₆₀ = −70/27, a₆₁ = 112/9, a₆₂ = −128/3, equal to #159's table at that point (`conical_limit.md` §3), and a₈₀ = −439/108, a₈₁ = 478/9, a₈₂ = −512/3, a₈₃ = 256 |
| `ind167_run2_mut_*.txt` | the 5 mutations, each exit 1 with exactly its target failing; `start-C` gives η*(C = 10) = 0.449121206 |
