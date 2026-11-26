# I26-dh610: Ω₂ from the order-4 matching integral of Paper III's large-D expansion

Machine: dh610-fedora (Fedora, 20 cores, 62 GB), shared with choptuik-large-d's runs (10 to 15 cores); runner
negative-mass-dh610-i26 (Claude Code, Sonnet 5.5, account claude-me2). Issue: https://github.com/nmoinvaz/negative-mass/issues/26
Code: worktree `~/Source/negative-mass-i26`, branch `wip/i26-omega2` (from 514ac42, the head of #195's branch); script
`notes/wormhole_largeD/order4.py`, output `order4_output.txt`, note `omega2.md`. Pushes: `git push origin HEAD:refs/heads/wip/i26-omega2`.
Development runs `dev_NN_*` and runs of record `run_NN_*` keep stdout (`.log`), stderr (`.err`) and the exit code (`.rc`) beside
this file (`devrun.sh`, `runrec.sh`, copied from I195-dh610); reruns are numbered, nothing is overwritten. Amendments are numbered
and dated at the end. Status words as in AGENTS.md: a closed form reached by hand and checked at each step is *derived*; a step
checked by sympy is *checked symbolically*; agreement of an integral with a constant is *numerical evidence*; a PSLQ relation is an
*identification*. No sentence here claims novelty.

**Written after two prototypes.** `dev_00_protoA.*` and `dev_01_protoB.*` (rerun with logs after they had been run once in the
terminal) were run before this file. They gave Ω₂ = 74.36938672793331759538467029584661726673414|4557 (A, 50 digits) and
74.3693867279333175953846702958466218852 (B, N = 30, w = 0.6, V = 16, 1e-33 off the closed form), so the answer was seen before
the criteria below were written. The criteria were written from the issue and the task, not tuned to those numbers; every
bar below is a bar of the issue or of the task, or a digit count well below what the prototypes reached.

## Convention

As in README.md, matched.py, order3.py and #195: s = 2(D − 3), ε = 1/s, W²a² = s + Ω, Ω = Ω₀ + Ω₁ε + Ω₂ε² + …, R = r^s, l = ln R.
Ω₀ = −4 ln 2, Ω₁ = 2π²/3 + 8 ln²2 = 10.4233603787…, and #195's Ω₂ = 74.3693867279333175953847. In 1/(D − 3) the coefficient
of order k is Ω_k/2^k.

## The order equations

The master equation in R, ε (README.md, "Matched asymptotics"): Y_R = ε L r/R, (R − 1)L_R = (1 + εΩ) rY + L/(2R) +
(½ + ε)L(R − 1)/R − (½ + ε)Y(R − 1)/(Rr) − Y/(2rR), r = e^{εl}. Expanding in ε (sympy, `order4.py sym`, check E0) gives for k = 0 … 4

    dY_k/dl = F_{k−1},  F_{k−1} = Σ_{j=0}^{k−1} L_{k−1−j} l^j/j!                         (Y_0 = 1, Y_k(R = 1) = 0)
    (R − 1)L_k′ − L_k/2 = h_k,   h_k = (1 − 1/R)L_{k−1} + Σ_{j=0}^{k−1} Y_j c_{k−j} + Y_k/2
    c_1 = Ω₀ + 3l/2 − 1 + 1/R
    c_2 = Ω₀ l + Ω₁ + l²/4 + l − l/R
    c_3 = Ω₀ l²/2 + Ω₁ l + Ω₂ + l³/4 − l²/2 + l²/(2R)
    c_4 = Ω₀ l³/6 + Ω₁ l²/2 + Ω₂ l + Ω₃ + l⁴/48 + l³/6 − l³/(6R)

The solution analytic at the throat is L_k = −2h_k(1) + (R − 1)^{1/2}C_k(R), C_k = ∫₁^R (h_k − h_k(1))(R′ − 1)^{−3/2}dR′, with
h_k(1) = Ω_{k−1}, and the mode needs G_k = C_k(∞) = 0. G_k is affine in Ω_{k−2} with slope −4π (the order-3 slope was computed
as −12.5663706144 in README.md); so G_2 = 0 gives Ω₀, G_3 = 0 gives Ω₁, **G_4 = 0 gives Ω₂**.

Variable θ = arctan √(R − 1): R = sec²θ, l = −2 ln cos θ, u = tan θ, (R − 1)^{−3/2}dR = 2dθ/sin²θ, G_k = 2∫₀^{π/2}(h_k − h_k(1))/sin²θ dθ.

## Method A: closed forms in θ, and the matching integral reduced to one integral

Closed forms (the README's, with K, and a new one for Y₃): K(u) = 2θ ln 2 − Cl₂(π − 2θ), T(θ) = ∫₀^θ φ ln cos φ dφ =
(θ/2)Cl₂(π − 2θ) − ¼Cl₃(π − 2θ) − (3/16)ζ(3) − (ln 2)θ²/2, and, with u = tan θ,

    Y_1 = −l,  Y_2 = −2Ω₀ l − (3/2)l²,  L_0 = −1,  L_1 = −2Ω₀ − 2l,
    L_2 = −2Ω₁ + 2Ω₀ l + 4l² − 8Ω₀ uθ − 16uK,
    Y_3 = −2Ω₁ l + l³/2 + 8l² + 8Ω₀ l + 8Ω₀θ² − 16Ω₀ uθ − 32uK + 32Kθ + 64T.

The matching integral G_k needs L_{k−1} and Y_k, which are nested integrals. Two integrations by parts remove them (derived by
hand, checked in mpmath at 30 digits, N4; both assume G_{k−1} = 0, which the order below provides):

    (E1)  G_k = 4∫₀^{π/2}L_{k−1}dθ + 2∫₀^{π/2}Σ_{j=1}^{k−1}L_{k−1−j}l^j/j! dθ + 2∫₀^{π/2}(Σ_{j<k}Y_j c_{k−j} − Ω_{k−1})/sin²θ dθ
          (from sin²θ = 1 − 1/R and ∫Y_k/sin²θ dθ = 2∫F_{k−1}dθ),
    (E2)  ∫₀^{π/2}L_{k−1}dθ = 2∫₀^{π/2}h_{k−1} ln cos θ/sin²θ dθ    (from L = −2h + 2 tan θ ∫₀^θ h_φ cot φ dφ and G_{k−1} = 0).

So G_k is one integral of closed forms (Cl₂, Cl₃, elementary), for k = 2, 3, 4 by the same code, with Y_j (j ≤ k − 1) and L_j (j ≤ k − 2)
closed. Ω₀, Ω₁, Ω₂ are solved in turn from the affine G_k; the slope is evaluated and compared with −4π.
Quadrature: mpmath at working precision d + 20 guard digits, [0, 1] by Gauss–Legendre (`mp.quad(method="gauss-legendre")` on [0, ½],
[½, 1]), [1, π/2] by tanh-sinh in x = π/2 − θ (so cos θ = sin x, tan θ = cot x, Cl(π − 2θ) = Cl(2x): no cancellation near π/2).
mpmath's quad error estimate is an estimator, not a bound.

## Method B: the hierarchy from its definitions, no closed forms, no exchange

Variable v = √l (R = e^{v²}, smooth at the throat), panels of width w on [0, V], N Chebyshev nodes per panel, cumulative integrals
by the spectral integration matrix (mpmath matrices). For k = 0 … 4: Y_k = ∫₀^l F_{k−1}dl cumulatively from the left; h_k from the
table; the tail C_right(v) = ∫_v^V (h_k − h_k(1))R(R − 1)^{−3/2} 2v dv cumulatively from the right; L_k = −2h_k(1) − u C_right (this
is the analytic solution when G_k = 0, and avoids the u ~ e^{v²/2} amplification of a left-hand integral's error); G_k = C_right(0).
Ω₀, Ω₁, Ω₂ are found in turn from G_2, G_3, G_4 (affine in Ω_{k−2}). The truncation at V costs about e^{−V²/2}.
B uses none of K, T, Cl₂, Cl₃, (E1), (E2), and no input value of Ω₀ or Ω₁.

**The four evaluations of G_4 (declared before the runs of record).**

| name | method | working precision | grid or quadrature |
|---|---|---|---|
| A50 | A | 50 digits | as above |
| A70 | A | 70 digits | as above |
| B1 | B | 120 digits | N = 40, w = 1/2, V = 18 (36 panels) |
| B2 | B | 140 digits | N = 50, w = 2/5, V = 20 (50 panels) |

**What the evaluations share** (recorded as AGENTS.md asks): the table of c_m and h_k (one sympy expansion of the master equation,
check E0, and #195's E0 for the master equation itself), the analytic-at-throat condition, mpmath. A and B share no closed form, no
integration by parts, no grid. #195's fit (the full equation in a Rust crate, no matching) shares none of the matched machinery and
is the independent reference. Every difference between evaluations below is a spread over method, precision and grid choices: an
estimator range, **not a rigorous bound**. No result here is a rigorous enclosure.

## Criteria (each can fail; written before the runs of record)

"d digits" means a relative difference ≤ 10^−d.

| id | statement | bar |
|---|---|---|
| E0 | the table of h_k (k = 0 … 4) equals the ε-expansion of the master equation | sympy residual 0 |
| S1 | Y_1, Y_2, Y_3 closed forms satisfy dY_k/dl = F_{k−1} | sympy residual 0 |
| S2 | L_0, L_1, L_2 closed forms satisfy (R − 1)L_k′ − L_k/2 = h_k | sympy residual 0 |
| S3 | L_3 = −2h_3 + 2 tan θ B(θ), B′ = h_3,θ cot θ (the order-3 reduction of L₃ to one integral) satisfies (R − 1)L_3′ − L_3/2 = h_3 | sympy residual 0 |
| N1 | K and T closed forms against quadrature of their definitions, θ = 0.3, 0.8, 1.2, 1.5 | 30 digits |
| N2 | Y_3 closed form against ∫₀^l F_2 dl, same θ | 30 digits |
| N3 | L_2 closed form against −2h_2(1) + u C_2 by quadrature, same θ | 30 digits |
| N4 | (E2) at k − 1 = 2 (closed L_2) and at k − 1 = 3 (L_3 of S3 by nested quadrature, dps 30) | 30 digits for k − 1 = 2, 25 for 3 |
| P1 | planted: Ω₀ and Ω₁ of A50, A70, B1, B2 against −4 ln 2 and 2π²/3 + 8 ln²2 (the same code that gives Ω₂) | 30 digits each |
| P2 | the evaluated slope of G_k in Ω_{k−2} against −4π, k = 2, 3, 4, every evaluation | 30 digits |
| P3 | control `wrong_Om0` (Ω₀ + 1/100 in the orders ≥ 3) moves Ω₁ of A50 and B1 | |Ω₁ − closed| > 10⁻³ |
| M1 | G_4 of A50 against A70 (two precisions); Ω₂ | 20 digits |
| M2 | B1 against B2 (two grids); Ω₂ | 20 digits |
| M3 | A70 against B2 (two methods); also A50–B1, A50–B2, A70–B1 reported; Ω₂ | 20 digits (the issue's) |
| X1 | the Ω₂ of record (A70) against #195's fit 74.3693867279333175953847 | 5e-23 absolute (half a unit of its last digit); also against #195's 38-digit median |
| X2 | each evaluation's Ω₂ against 80ζ(3) − (8/3)π² ln 2 − (32/3) ln³2 | A70 40 digits, A50 40, B1 and B2 30 |
| Q1 | PSLQ (`mp.pslq`, tol 1e-18, maxcoeff 1000, maxsteps 10⁶; the relation also found at 10·tol) on {Ω₂, ζ(3), π² ln 2, ln³2}, Ω₂ of A70 at the digits it shares with B2 (≤ 60) | relation ±(3, −240, 8, 32); the perturbed basis (ζ(3) + 10⁻³) finds none |
| Q2 | PSLQ, tol 1e-30, maxcoeff 1000, on {Ω₂, ζ(3), π² ln 2, ln³2, π², ln² 2, ln 2, 1} | ±(3, −240, 8, 32, 0, 0, 0, 0); the perturbed basis finds none |
| R1 | remainder rem = W²a² − [s − 4 ln 2 + Ω₁/s + Ω₂/s²] against #195's W² at D = 200, 500, 1000, 2000 (`w2_output.txt`, the qd values printed there); the series uses the integral's Ω₁, Ω₂ | \|rem·s³ − Ω₃\| falls with D; rem·s³ within 1 % of Ω₃ = −652.84010757006 at D = 2000 |
| R2 | two-point extrapolation (s₂x₂ − s₁x₁)/(s₂ − s₁), x = rem·s³, from D = 1000, 2000 | within 0.05 of Ω₃ (set from #195's tabulated remainders −659.2, −656.0) |

Reported and not gated: rem·s³ at the 64 values of D of `w2_output.txt` and (rem·s³ − Ω₃)s against Ω₄ = −12794.5; the 60-digit qd
values at D = 200 … 2000 of raw I195-dh610/run_02; each term of the reduced G_4 and its identification (the reduction, if reached).

The criteria bars are for the runs of record; a criterion that fails is reported **not met**, and I do not change it; I ask the
coordinator first about any change of a grid, a precision, a tolerance or a criterion after a development run.

## Controls (`--mutate=NAME`)

Each check has a control that must make it fail. The mutated quantity is fixed here; **the targets of each control (the checks it
must fire) are computed in a development run and declared in an amendment before the runs of record.**

| name | mutated quantity |
|---|---|
| `wrong_h` | the sign of −l/R in c_2 (table, A and B alike) |
| `wrong_Om0` | Ω₀ → −4 ln 2 + 1/100 in the orders ≥ 3 (A and B) |
| `wrong_Om1` | Ω₁ → 2π²/3 + 8 ln²2 + 1/100 at order 4 (A and B) |
| `T_const` | T without its −(3/16)ζ(3) |
| `K_sign` | K = 2θ ln 2 + Cl₂(π − 2θ) |
| `bad_exchange` | the factor 8 in (E1)+(E2) written 4 |
| `coarse_B` | B with N = 10 |
| `short_tail` | B with V = 6 |
| `pslq_wrong_basis` | ζ(3) + 10⁻³ in the PSLQ bases |
| `wrong_Om2_series` | Ω₂ + 1/100 in the four-term series of R1, R2 |

## Runs

Production: `systemd-run --user --unit=nm-i26-<name> --working-directory=<dir> nice -n 10 …`, at most 4 processes, one thread each,
with `runrec.sh` (log, stderr, exit code, /usr/bin/time -v, load). Stop condition: any run not finished in 2 h of wall time is
stopped and reported with what finished. Memory is reported only. Units are recorded in the table below as they are started.

| run | what | unit | wall | exit |
|---|---|---|---|---|

## Amendments

(none yet)
