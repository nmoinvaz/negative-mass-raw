# I184-mac: the coordinator's review of #184 (rerun of the default mode, independent check ind184)

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, mpmath 1.3.0, Rust 1.94.0, at nice 10 with at
most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/184. Under review: branch
`wip/i184-conical-loglog` at ed774f7, raw `I184-rpi5` at b707b72. Stop condition: 1 h per run. Written 2026-11-26 before
the first run of `ind184.py`.

## Rerun

`python3 notes/warp/conical_loglog.py --nobuild` from a worktree at ed774f7 after `cargo build --release -j 2` of the
crate (`rerun_build.log`, `rerun_default_1.log`).

## ind184.py: what it shares with #184

Shared: sympy, mpmath, the block entries of a conical shift and D's formula (as in I167-mac-review/ind167.py), the claims
under test. Not shared: ind184 imports nothing from the repository and does not use the crate; its N (determinant of the
block, in θ-variables), its exact interval arithmetic (Fractions, branch and bound) and its integrator are its own.

Notation (conical_loglog.md §3): N(G, p, q, σ) = A₀ + σA₁ + σ²A₂, u = 1 + |G|, D = {0 < p ≤ 1/4, σu³ ≤ p²/5}, q = −p² + w.
On D write s = 1/u ∈ (0, 1], G = θ(1 − s)/s (θ = ±1), q = p²(ω − 1), and σ = κ p² s³/5 with κ ∈ [0, 1]. Every quantity
below is then a polynomial in (s, ω, p, κ), checked by the code, and the box is s ∈ [0, 1], ω ∈ [−1/2, 1/2], p ∈ [0, 1/4],
κ ∈ [0, 1].

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| Q1 | Lemma 1 by exact interval arithmetic, for θ = +1 and θ = −1 on the box: (a) N/p⁶ < 0 at ω = −1/2; (b) N/p⁶ > 0 at ω = 1/2; (c) (∂N/∂q)/p⁴ > 0 for ω ∈ [−1/2, 1/2]; (d) \|R\|/(σu²p⁶) ≤ 30 with R = σA₁ + σ²A₂, so that the root has \|w\| ≤ \|R\|/(1.5p⁴) ≤ 20σu²p² |
| Q2 | With q = −p² + σe + O(σ²), the σ¹ coefficient of N vanishes iff e = −p²(G − 1)²/2, from ind184's own N |
| Q3 | Re-solve (numerical evidence): ind184's own RK4 in t = ln η (mpmath, 30 digits, h = 1/50), on the root of N in [−3p²/2, −p²/2], from (G, p) = (3, 1/10) at η = 10⁴ to η = 10¹². At every step: the state is in D, q/p² ∈ [−5/4, −3/4], and G(t) − G(t₁) ≥ (4/5) ln(1 + 5p₁(t − t₁)/4) (Theorem 1, items 1 and 2) |

Read and rederived by hand by the coordinator, not coded: Lemma 1's term bounds (26u²p⁶, 30u²p⁴, 15u³p⁴, 35u³p³ and
\|R\| < 0.37p⁶), Theorem 1's forward invariance ((ln r)′ ≤ −2 + 5.5p ≤ −0.625) and items 1 to 3.

## Mutations (`--mutate=NAME`; each must make ind184 exit non-zero with exactly these criteria failing)

| mutation | change | targets |
|---|---|---|
| `q1-sign` | Q1 (a) claims N/p⁶ > 0 at ω = −1/2 | Q1 |
| `q2-coef` | Q2 expects e = −p²(G − 1)²/4 | Q2 |
| `q3-start` | Q3 starts at (G, p) = (3, 1/2), outside D | Q3 |

## Runs (filled in as they are done)
