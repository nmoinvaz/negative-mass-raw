# I208-mac-review: the coordinator's review of #208 (rerun, independent check ind208)

Machine: macOS (the coordinator's Mac, Apple M5, arm64), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`:
mpmath 1.3.0 with the python backend, sympy 1.14.0), nice 10, at most 2 processes. Issue:
https://github.com/nmoinvaz/negative-mass/issues/208. Under review: branch `wip/i208-omega3` at fd15081, raw
`I208-dh610` at ace0b32. Written 2026-11-27 before the first run of `ind208.py` and before the rerun.

## Rerun

`rerun.sh`, from a detached worktree `~/Source/negative-mass-r208` at fd15081, in `notes/wormhole_largeD`, in one chain
of one process. It runs the four runs of record of `I208-dh610` (their `.env` files):
- `order5.py sym`;
- `order5.py evals pslq remainder --save=<here>/rerun_run_02_evals.json --w2raw=<I208-dh610/inputs_w2_growthD.txt>`;
- `order5.py closedform --load=<that json>`;
- `order5.py reduce5 a5 --load=<that json>`.

The expectation, written now: every PASS and FAIL line has the same verdict and the same printed numbers as dh610's
logs, except timings. Both machines run mpmath and sympy as pure Python, at the same versions, as #26's rerun did.

## ind208: ind26 carried to order 5

`ind208.py` is `I26-mac-review/ind26.py` with kmax = 5. ind26 is the coordinator's own code, reviewed in #26.
- It derives the order equations again from #195's ℓ-system.
- It integrates them by its own Taylor stepper in v = √l, with C_k from the throat outward.
- It shares with #208 only mpmath, sympy and README.md's matching conditions.

The settings are those of ind26 run 1: jets of order 40, 70 working digits, steps of 1/8 below v = 3 and 1/(2v₀)
beyond, and truncation at V = 17. Ω₃ comes from G₅ = 0, after Ω₀, Ω₁ and Ω₂ from G₂, G₃ and G₄.

## Criteria (each coded as worded; each can fail)

Ω₃* denotes #208's closed form, 22π⁴/45 + (16/3)π² ln²2 + (32/3) ln⁴2 − 320ζ(3) ln 2 − 384ζ(3).

| id | criterion |
|---|---|
| K1 | For k = 0 … 5, the ε^k coefficient of the L equation and of Y_l = εw, from the ℓ-system, equals `order5.py`'s h_k and dY_k/dl, through its `hk`, `cc` and `Fsum`: sympy residual 0 |
| K2 | Ω₀, Ω₁ and Ω₂ are within 1e-35, 1e-33 and 1e-30 of their closed forms. Ω₃ is within 1e-30 of Ω₃*, and within 1e-30 of #195's 40-digit median −652.8401075700561254352393037996473610805 |
| K3 | The slopes dG_k/dΩ_{k−2} at k = 2 … 5 are −4π, to 1e-30 relative. G₅(Ω₃ = 0)/(4π) equals Ω₃* to 1e-30 relative, with Ω₀ … Ω₂ K2's own |

## Mutations (`--mutate=NAME`; each must make ind208 exit non-zero with exactly these criteria failing)

The targets are predicted from the code, not yet computed. A mutation that misses its targets is reported.

| mutation | change | targets |
|---|---|---|
| `k1-B` | the ℓ-system's B uses (½ + ε)F in place of (½ + 2ε)F, in K1 and K2 alike | K1, K2, K3 |
| `short-V` | K2 truncates at V = 9 | K2, K3 |
| `drop-z3` | Ω₃* without its −384ζ(3) term, the one term of weight 3 | K2, K3 |

## Runs (filled in as they are done)

| file | what |
|---|---|
