# I209-mac-review: the coordinator's review of #209 (rerun, independent check ind209)

Machine: macOS (the coordinator's Mac, Apple M5, arm64), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`:
mpmath 1.3.0, sympy 1.14.0), nice 10, at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/209.
Under review: branch `wip/i209-exchange-review` at 76db404 (code 886f764 and 023019f), raw `I209-rpi5` at b7c952b.
Written 2026-11-27 before the first run of `ind209.py` and before the rerun.

## Rerun

`exchange_review.py sym exact clausen exch grid ctlsum`, as the run of record `run_03`, from a detached worktree
`~/Source/negative-mass-r209` in `notes/wormhole_largeD`. The expectation: every verdict line equals `run_03`'s. mpmath
and sympy are pure Python at the same versions.

## ind209: E1, E2 and E3 on a hierarchy that shares no code with method B

#209 checks E1 to E3 numerically on method B's panel hierarchy (`PanelK`), the code #26 and #208 also used; this is its
recommended task 1. ind209 evaluates the same three identities, in `exchange_review.py`'s forms, on the coordinator's
own Taylor-jet hierarchy from the reviews of #26 and #208 (`I208-mac-review/ind208.py`):
- order 40 in v = √l, 70 digits, V = 17;
- C_k integrated from the throat outward, L_k = −2h_k(1) + s C_k;
- the order equations derived from #195's ℓ-system.

The θ-integrals are accumulated along v with dθ = (v/s) dv, sin²θ = 1 − 1/R and ℓ = ln cos θ = −v²/2. At v = 0 the
factors of v are divided out exactly. Ω₀ … Ω₃ are the closed forms.

The identities, as `exchange_review.py` states them (`e1_residual`, `e2_sides`, `e3_sides`):
- E1: G_k = 4∫L_{k−1}dθ + 2∫(F_{k−1} − L_{k−1})dθ + 2∫(Σ_{j<k}Y_j c_{k−j} − Ω_{k−1})/sin²θ dθ;
- E2: ∫L_m dθ = 2∫h_m ℓ/sin²θ dθ;
- E3: ∫Y_m[(ℓ − Ω₀)/sin²θ + 1]dθ = 2∫(ℓ − Ω₀)F_{m−1}dθ.

On this hierarchy L_m carries the growing solution s·G_m whenever G_m ≠ 0. The identities' hypothesis G_m = 0 can
therefore be tested here, which #209 reports it could not do on `PanelK` (its control `bnd_G` is silent there by
construction).

## Criteria (each coded as worded; each can fail)

"agree to d" means |a − b| / max(|a|, |b|, 1) ≤ 10^−d.

| id | criterion |
|---|---|
| K1 | E1 holds at k = 3, 4 and 5, its two sides agreeing to 30, in two settings: with the closed-form Ω's, where G_k = 0 and the three O(100) terms must cancel, and with Ω_{k−2} + 1/10, where G_k ≈ −0.4π ≠ 0 must be reproduced |
| K2 | E2 holds at m = 2, 3 and 4: its two sides agree to 30 |
| K3 | E3 holds at m = 2, 3 and 4: its two sides agree to 30 |
| K4 | The hypothesis matters. With Ω₀ → Ω₀ + 1e-3 in every order (so G₂ ≠ 0), E2 at m = 2 fails by more than 1e-6, on the same hierarchy truncated at the same V |

## Mutations (`--mutate=NAME`; each must make ind209 exit non-zero with exactly these criteria failing)

The targets are predicted from the code, not yet computed. A mutation that misses its targets is reported.

| mutation | change | targets |
|---|---|---|
| `e1-factor` | E1's first term with 2 in place of 4 | K1 |
| `e2-weight` | E2's weight ℓ → ℓ + ln 2 | K2 |
| `e3-Om0` | E3 with Ω₀ → 0 | K3 |
| `k4-off` | K4 run without the Ω₀ shift, so E2 holds | K4 |

## Amendments

**A1, 2026-11-27, after run 1.** Run 1 crashed at its start (NameError: `Rinv`): the copy from ind208 left out that
symbol's definition. The line is restored, and nothing else changes. Run 2 is the first run that computes anything.

## Runs (filled in as they are done)

| file | what |
|---|---|
