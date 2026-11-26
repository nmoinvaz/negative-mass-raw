# I168-mac: the coordinator's review of #168 (rerun of the default mode, independent check ind168)

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, mpmath 1.3.0, numpy 2.5.4
(`/Users/nathan/Source/negative-mass/.venv`), at nice 10 with at most 2 processes. Issue:
https://github.com/nmoinvaz/negative-mass/issues/168. Under review: branch `wip/i168-conical-attraction` at aff2d76, raw
`I168-rpi5` at cd80040. Stop condition: any single run not finished after 1 h of wall time is stopped (by its PID) and
reported. Written 2026-11-26 before the first run of `ind168.py`.

## Rerun of the runner's default mode

`python3 notes/warp/conical_attraction.py` from a worktree at aff2d76: the 21 checks, then the 27 controls.

## ind168.py: what it shares with #168

Shared: sympy and mpmath; the block entries of a conical shift, ρ²(P, Q, Z, Y, h) = (−(F′² + FF″), −ηw/2, −w/2, −(ηF′² +
Fw/2), η²F′²/2) with w = F′ + ηF″ (`det_classify.md` §6, C9b), and θ-variables F′ = pν, F″ = (q − p)ν², η = 1/ν
(`conical_limit.md` §1); and the objects under test, read from `conical_attraction.md`: the coefficients c₃, c₂, c₁, c₀,
the polynomial P(w) with κ, μ, c, M, the scalar equation (1), and the stated constants. Not shared: ind168 imports
nothing from the repository. Its D is its own (sympy's determinant of the block), and so are its exact interval
arithmetic (Fractions, branch and bound), its exponential bounds and its integrator.

## Criteria (each coded as worded; each can fail)

Box Ω: σ, b ∈ [0, 1/500], a ∈ [0, 1/1000], ω ∈ [−100, 100] (a superset of Lemma 1's hypotheses). "Proved on a box" means
ind168's interval arithmetic over exact Fractions, with bisection, establishes the inequality on every sub-box.

| id | criterion |
|---|---|
| K1 | 8 det(block) with the entries above, in (G, p, q, ν), equals c₃q³ + c₂q² + c₁q + c₀ with the note's c₃ = −2Gσκ, c₂ = −p(2G(G² − 1)σ² + pμ), c₁ = 4Gσc p⁴, c₀ = p⁴(c²p² − 4G²σ²), σ = ν², b = G²σ, exactly |
| K2 | that polynomial equals p⁶ P(q/p²) with ω = 2Gσ/p, a = Gσ and the note's P(w) = −2aκw³ − Mw² + 4acw + c² − ω², κ = 1 − b + σ, μ = 1 + 3σ − b + 2σ² − 6bσ, c = 1 + 2σ, M = μ + (b − σ)ω, exactly |
| K3 | with G′ = σr, r′ = 2r + s, s = (G²ê − r²)/(2G), y = r/G: y′ = y(4 − y)/2 − σy² + ê/2 and (ln G)′ = σy; and ê = y²(1 + 2aw) when s = σr²w; exactly |
| K4 | Lemma 1 on Ω: κ ∈ [0.998, 1.002], μ ≥ 0.99, c ∈ [1, 1.01], M ≥ 0.79; (A) 4M − 3κ > 0; (B) κ − 2M + 32a²(c² − c − ω²) < 0; (C) P(2) < 0, P(−2) < 0, P′(2) < 0; (D) c² + 16aκ + 8ac ≤ 1.05²; (E) on Ω with ω ∈ [−1/2, 1/2]: P(0), P(1/2), P(−1/2) > 0 |
| K5 | Lemma 2. (a) P(−x) = 0 ⟹ κ(1 − 2ax) = (κ − M) − 4ac/x − (ω² − c²)/x², exactly. (b) On f ∈ [0, 1], u ∈ [0, 1/500], σ = fu, b = (1 − f)u: (2f + 2f²u + 6f(1 − f)u + 16f(1 − f)u(c + c²))/κ ≤ 51/25, 2\|1 − 2f\|/κ ≤ 201/100, 64f(1 − f)u/κ ≤ 321/10000, and 321/10000 ≤ (181/50 − 201/100)/50 |
| K6 | Regime B: on Ω with \|y\| ≤ 1/50 and p = ay: \|b − σ + yμ/2\|/κ ≤ 121/10000, (2c/κ)a²y² ≤ (121/10000)², a²\|y\|\|c²y² − 4\|/(2κ) ≤ (121/10000)³, hence 3Θ ≤ (363/10000)\|p\| |
| K7 | The small branch: 4σ + 8a ≤ 16/1000 on Ω, so (ln\|ω\|)′ ≤ −2 + 16/1000 ≤ −1.984 |
| K8 | The huge branch, with g(y) = (4 − y)/2 − σy − u(αy + β)/2, α = 51/25, β = 181/50, σ, u ∈ [0, 1/500]: y·g(y) ≥ 1.4923y on [1/50, 1]; y·g(y) ≥ 0.1062 on [1, 15/4]; and with g⁺(y) = (4 − y)/2 − σy + u(αy + β)/2: g⁺(17/4) ≤ −0.1042 and −1/2 − σ + uα/2 < 0 (so g⁺ ≤ −0.1042 on [17/4, ∞)) |
| K9 | Theorem A's chain in exact rationals: c_e = α(9/2)² + β(9/2) ≤ 58; c_f ≥ c_e/2 + (9/2)², c_f = 50; ū = e^{9σ₀/2}u₀ ≤ 1.0046·10⁻³ for σ₀ ≤ u₀ ≤ 1/1000 (e^x ≤ 1/(1 − x)); B = 1/4 + 4c_fū ≤ 0.451 < 1/2; H = B/(7/2) ≤ 0.129; e^H ≤ 1.14 (Taylor bound with remainder, e^x ≤ Σ_{k≤4} x^k/k! + (x⁵/120)/(1 − x/6)) |
| K10 | Re-solve (numerical evidence): ind168's own RK4 in t = ln η on (G, p), h = 1/200, with q the most negative real root w of the cubic (the huge root, w ≤ −1/(4a)) at every stage, from G₀ = 1, ζ₀ = 1/4, u₀ = 1/1000 (σ₀ = 1/2000), to τ = 10: the huge root has w ≤ −1/(4a) at every step, (b) \|ζ\| ≤ 0.451e^{−7τ/4} and (c) \|ζ\| ≤ 1.14(\|ζ₀\| + 50ū τ)e^{−2τ} at every step, and \|y − 4\| ≤ 10⁻⁶ at τ = 10 |

Read and rederived by hand by the coordinator, not coded: Lemma 1's shape argument; Theorem A's Steps 1–4; Theorem B's
induction and identification; Lemma 3, Corollary 4 and Theorem C's case analysis.

## Mutations (`--mutate=NAME`; each must make ind168 exit non-zero with exactly these criteria failing)

| mutation | change | targets |
|---|---|---|
| `D-sign` | the block's Y entry with +F w/2 in place of −F w/2 | K1 |
| `P-omega` | P(w) with + ω² in place of − ω² | K2 |
| `red-sigma` | the claimed y′ with + σy² | K3 |
| `box-omega` | Ω with ω ∈ [−200, 200] in K4 | K4 |
| `ehat-alpha` | K5's first bound 2 in place of 51/25 | K5 |
| `regb-y` | K6 with \|y\| ≤ 1/5 | K6 |
| `cf-49` | K9 with c_f = 49 | K9 |
| `y-thr` | K8's first bound 3/2 y in place of 1.4923y | K8 |
| `small-root` | K10 starts on the root w ∈ (1/2, 2) in place of the huge root | K10 |

K7 has no mutation of its own: its content is one inequality between two exact numbers, checked as stated.

## Runs (filled in as they are done)
