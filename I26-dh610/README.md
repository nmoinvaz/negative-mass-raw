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
| `run_01_sym_closed_reduce` | `order4.py sym closed reduce` | `nm-i26-01` | 2:07.23, peak 67 MiB | 1 |
| `run_02_n4b` | `order4.py n4b` | `nm-i26-02` | 19:39.50, peak 56 MiB | 1 |
| `run_03_n4bg` | `order4.py n4bg` | `nm-i26-03` | 4:14.76, peak 57 MiB | 0 |
| `run_04_evals_remainder` | `order4.py evals remainder --w2raw=inputs_w2_growthD.txt` | `nm-i26-04` | 2:01.98, peak 71 MiB | 0 |
| `run_05_lc2` | `order4.py lc2` (after A4) | `nm-i26-05` | 0:40.50, peak 57 MiB | 0 |

Code of the first four runs: worktree commit 0ab15d6 (`run_00_code.txt`), `order4.py` sha256 d2455d5e04e4dc3e…; `run_05`: commit 4f08fd3, sha256 e0a9d1e96de4154f…. The earlier units were `nm-i26-dev02`, `-dev03`
(stopped), `-dev_04_evals`, `-dev_05_symclosed`, `-chainA` … `-chainG3`, `-dev16`.

## Amendments

### A1 (2026-11-26, after dev_02 to dev_05; the coordinator ruled on N3 and N4b by hc the same day)

- **N3 and N4b as written are NOT MET** and stay in the runs of record as written: `dev_02_closed` gave N3 25.8 digits (bar 30) and N4b
  22.0 digits (bar 25); N1, N2 and N4a passed (43.7, 44.9, 44.5 digits). The cause is the checks' own cancellation, not the closed
  forms: (h_2 − h_2(1))/sin²θ near the throat and u·K near π/2 lose digits at working precision 45 (N3) and 30 (N4b) with no guard
  digits. The scratch reading before this amendment, N3 with 30 guard digits, was 40.7 digits (`dev_06_diagN3`, the same script rerun
  with a log). So the closed forms (also used by N2, N4a and the planted run) are not at fault.
- **Added: N3g and N4bg**, the same checks with the same bars (30 and 25 digits) and the integrands evaluated with 30 guard digits
  (the quadratures keep their working precision 45 and 30). `dev_05_symclosed`: N3g 40.1 digits.
- The script is split in parts that run as separate processes: `sym`, `closed` (N1, N2, N3, N3g, N4a), `n4b`, `n4bg` (the nested
  quadratures, about 30 min and 65 min), `evals` with `remainder` (A, B, P, M, X, Q, R). The output of record is the concatenation
  of the four logs in the order `run_01` … `run_04` (see the run table).
- **Defect fixed after dev_03**: `PanelB`'s integration matrix used T₀ = 1 for x in its first column; B returned slope −19197 instead of
  −4π and Ω₀ = −1370 (`dev_03_evals.note`; A50 and A70 had finished, the run was stopped by me with `systemctl --user stop`, no exit
  code). Fixed before `dev_04_evals`. The 10-minute `closed` run launched in the terminal before dev_02 (piped to `tail`, no output
  kept) was stopped by me after its time per piece was measured; it is not a record.
- **Nominal development runs** `dev_04_evals` (11 of 11 pass, Ω₂ of A50, A70, B1, B2 = 74.36938672793331759538467029584661726673414341502…;
  A50–A70 77.6 digits, B1–B2 48.2, A70–B2 64.4; A70 against the closed form 80.7, capped by the 80-digit working precision of the
  comparison) and `dev_05_symclosed` (8 of 9: N3 as written fails). Reported after the fact: **the criteria were not changed by
  these runs**; only the additions above and the output formatting (digits capped at the working precision, the grid string, the
  extra report of the 60-digit remainders from `inputs_w2_growthD.txt`, not gated).
- The planted order-3 digits seen in `dev_04`: A50 80.3, A70 ≥ 80, B1 48.2, B2 64.7 (bar 30).

### A2 (2026-11-26, after dev_07 to dev_14): the reduction by hand, its criteria, the new controls and the controls' targets

**The reduction.** At Ω₀ = −4 ln 2 the closed forms need only ℓ = ln cos θ, u = tan θ, C = Cl₂(π − 2θ) and D₃ = Cl₃(π − 2θ) + (3/4)ζ(3):
L₂ = −2Ω₁ − 4Ω₀ℓ + 16ℓ² + 16uC, Y₃ = 4Ω₁ℓ − 4ℓ³ + 32ℓ² − 16Ω₀ℓ + 32uC − 16D₃ (no θ, no K, no T). With them the integrand of
G_k (E1 with E2, Ω_{k−1} → 0) is A(ℓ)/S + B(ℓ) + γC + δD₃, S = sin²θ, with A, B polynomials in ℓ (A(0) = 0) and
δ = −32 P′, γ = 64uP′ + 64uℓ, P = cot θ (ℓ − Ω₀). Then ∫δD₃ = 64∫CP (by parts, D₃′ = 2C, boundary terms vanish),
γ + 64P = 64(Ω₀ − 1)u, ∫₀^{π/2} tan θ Cl₂(π − 2θ)dθ = π³/12 (by parts, C′ = 2ℓ + 2 ln 2, J₁ and J₂), ∫ℓ^b/S = −bJ_{b−1}, and
J_n = ∫₀^{π/2} ℓ^n dθ from the Beta function. At k = 3 there is no C or D₃ at all (L₂ was eliminated by E2): G₃ = 0 gives
Ω₁ = 2π²/3 + 8 ln²2; at k = 4 the same steps give Ω₂ = 80ζ(3) − (8/3)π² ln 2 − (32/3) ln³2. Found in `dev_12_reduce1` … `reduce4`
(sympy scripts, logs kept) after dev_04. **Status: *derived* if H0 to H8 pass** (each step checked); it uses E1, E2 (N4a, N4b),
Ω₀ = −4 ln 2 (README.md, derived there) and nothing identified; it is not independent of A (same E1, E2), and B, which uses neither,
is the independent check of its value.

**Added criteria** (declared before the runs of record; bars 30 digits unless a residual 0):

| id | statement |
|---|---|
| H0 | the README forms of L₂ and Y₃ at Ω₀ = −4 ln 2 equal the forms above (sympy residual 0) |
| H1 | A/S + B + γC + δD₃ equals method A's integrand at θ = 0.2, 0.7, 1.1, 1.4, k = 3 and 4 (30 digits) |
| H2a, H2b | δ = −32 dP/dθ (sympy residual 0); ∫δD₃ dθ = 64∫C cot θ (ℓ − Ω₀)dθ by quadrature (30 digits) |
| H3 | γ + 64 cot θ (ℓ − Ω₀) − 64(Ω₀ − 1)u = 0 (sympy residual 0) |
| H4 | ∫₀^{π/2} tan θ Cl₂(π − 2θ)dθ = π³/12: by quadrature, and by parts (C′ = 2ℓ + 2 ln 2 to 30 digits, boundary term ℓC → 0, 2J₂ + 2 ln 2 J₁) |
| H5 | ∫ ℓ^b/S dθ = −bJ_{b−1}, b = 1 … 4, by quadrature (30 digits) |
| H6 | J_n (n ≤ 4) from the Beta function series (sympy) against quadrature (30 digits) |
| H7 | G₃ = 0 gives Ω₁ = 2π²/3 + 8 ln²2 and G₄(Ω₂ = 0)/(4π) gives 80ζ(3) − (8/3)π² ln 2 − (32/3) ln³2, with that Ω₁ (sympy, difference 0) |
| H8 | the derived G₃(0) and G₄(0) against method A's at 40 digits (30 digits) |

**Added controls** (mutated quantity): `wrong_Y3` (32Kθ → 16Kθ in the symbolic Y₃ of S1 and H0), `wrong_B` (B′ = h₃,u/(2u) in S3),
`wrong_P` (P = cot θ(ℓ + Ω₀) in H2, H3), `wrong_J3` (J₃ with 5ζ(3) in place of 6ζ(3)), `wrong_tanC` (π³/6 for π³/12). `wrong_Om0` and the
others apply to H7 as to A and B.

**Targets of the controls, computed** (nominal failures: N3 only; each list is the checks that fail beyond N3). The runs `dev_07_*`
for `wrong_h`, `wrong_Om0`, `T_const`, `K_sign`, `bad_exchange`, `coarse_B`, `short_tail` **crashed** in PSLQ (`ValueError: prec cannot be
less than 53`: the digits shared by A70 and B2 were below 16, and PSLQ was given exactly that precision), so Q1, Q2, R1, R2 were
not computed there. Fixed (PSLQ works at max(shared digits, 30)) and the seven controls rerun for `evals` and `remainder` as `dev_15_*`
(the `wrong_h` log has a space in its name, `dev_15_evals remainder_wrong_h`). The table uses `dev_07` for the other parts and `dev_15`
for the evaluations.

| control | fires | silent (computed) |
|---|---|---|
| `wrong_h` | E0, S2, N3g, N4a, P1, M1, M3, X1, X2, Q1, Q2, R1, R2, H1, H8 | S1, S3, N1, N2, P2, M2 |
| `wrong_Om0` | P1, M1, M3, X1, X2, Q1, Q2, R1, R2, H7, H8 (P3 passes: Ω₁ moved by 0.0276 in A50 and B1) | M2, P2 |
| `wrong_Om1` | X1, X2, Q1, Q2, R1, R2 | P1, P2, M1, M2, M3 (both methods take the same wrong input) |
| `T_const` | N1, N2, M3, X1, X2, Q1, Q2, R1, R2, H1, H8 | P1, P2, M1, M2 (T enters at k = 4 only) |
| `K_sign` | N1, N2, N3g, N4a, N4b, N4bg, M3, X1, X2, Q1, Q2, R1, R2, H1, H8 | P1, P2, M1, M2 (K enters at k = 4 only) |
| `bad_exchange` | P1, P2, M1, M3, X1, X2, Q1, Q2, R1, R2, H1, H8 (Ω₂ of A is 632098) | M2 |
| `coarse_B` | P1, P2, M2, M3, X2, Q2 | M1, X1, Q1, R1, R2 (A70 is untouched; Q2 fires because PSLQ gets only the shared 14 digits, below its tolerance) |
| `short_tail` | P1, P2, M3, X2, Q2 | M1, M2 (both grids share V = 6), X1, Q1, R1, R2 |
| `pslq_wrong_basis` | Q1, Q2 | |
| `wrong_Om2_series` | R1, R2 | X1, X2 |
| `wrong_J3` | H5, H6, H7, H8 | |
| `wrong_tanC` | H4, H7, H8 | |
| `wrong_Y3` | S1, H0 | |
| `wrong_B` | S3 | |
| `wrong_P` | H2a, H2b, H3 | |

N4b under `wrong_h` and N4bg under `T_const` and `wrong_h` were not run; N4b under `T_const` (`dev_08_T_const`) was still running when
this was written. `K_sign` fires N4b and N4bg, which is what a check needs to have a control. N3 as written has none (it fails nominally).

**Harness mistakes, not results.** `dev_14_sym_none` and `dev_14_reduce_none` exited 1 on an assertion (`--mutate=none` is not a
mutation); `dev_11_reduce_*` ran the `reduce` part of `dev_10_order4_wip.py` before `wrong_Y3`, `wrong_B`, `wrong_P` were added
(`dev_13_order4_wip.py` has them; both are scratch copies of what became `order4.py`, checked with `cmp` after the merge).

**The runs of record** (all parts of `order4.py`, separate processes, at most 4): `run_01` sym, closed, reduce; `run_02` n4b; `run_03` n4bg;
`run_04` evals, remainder (with `--w2raw`). Their logs, concatenated in that order, are `order4_output.txt`.

### A3 (2026-11-26, after dev_16, before the runs of record): the closed form of L₃

`dev_17_l3explore` and `dev_17_l3ansatz` (sympy; logs kept): with the forms of A2, dB/dθ = h₃,θ cot θ has no 1/u and no D₃ term,
b = −16(3 − 2c²)ℓ² − 32 ln 2 (5 − 2c²)ℓ + 32u(1 + c²)C − 64 ln²2 − 2Ω₁(1 + 2c²), c² = 1/(1 + u²); an ansatz finds its antiderivative
B(0) = 0, with Lc2(θ) = ∫₀^θ ln² cos φ dφ (a weight-3 log-cosine integral, expressible with Li₃ of 1 + e^{2iθ}; not written out here):

    B = −32(ℓ + ln 2)C + 16 S C + 32 Lc2 + 16 sin θ cos θ ℓ(ℓ + 2 ln 2) − 4Ω₁θ − 2Ω₁ sin θ cos θ,    L₃ = −2h₃ + 2uB.

**Added criteria:** S4 (sympy residual 0 for (R − 1)L₃′ − L₃/2 − h₃ with that B, derivation d/dθ with C′ = 2ℓ + 2 ln 2, D₃′ = 2C, Lc2′ = ℓ²)
and N5 (L₃ closed, Lc2 by quadrature, against −2h₃(1) + uC₃ by quadrature at θ = 0.4, 1.0, 1.4, Ω₂ = 0, 30 guard digits: 30 digits).
**Added control** `wrong_L3` (32 Lc2 → 16 Lc2): fires S4 and N5 (`dev_16_sym+closed_wrong_L3`). `dev_08_T_const` (N4b under `T_const`) was stopped by me
after 58 min with no result (`dev_08_T_const.note`); `K_sign` is the control of N4b and N4bg. `dev_16_order4_final.py` is `order4.py` as run for the
records (sha256 d2455d5e04e4dc3e…, same as the file committed on the branch at the time of the first run of record).

**Status words for the closed forms of Y₃ and L₃.** *checked symbolically* (S1, S4) and *numerical evidence* (N2, N5); Y₃ needs Cl₂, Cl₃, L₃ needs in
addition Lc2. Y₄ is not given in closed form (G₄ needs only L₃ through E1, E2).

### A4 (2026-11-26, after run_01 to run_04, before run_05): the log-cosine integral in polylogarithms

`run_01` to `run_04` finished (exit 1, 1, 0, 0; `run_02` N4b 22.0 digits NOT MET as written, `run_03` N4bg 27.5 digits met, `run_01` N3 25.8 NOT MET as written). While the nested
quadratures ran, the function left open in S4, Lc2(θ) = ∫₀^θ ln² cos φ dφ, was written with polylogarithms (`dev_18_lc2_probe.py`, from ln cos φ = ln(1 + t) − ln 2 − ½ ln t,
t = e^{2iφ}, dφ = dt/(2it), and the standard antiderivatives of ln²(1 + t)/t, ln(1 + t)/t, ln(1 + t) ln t/t):

    Lc2(θ) = (1/2i)[F(e^{2iθ}) − F(1)],   F(t) = ln t ln²(1 + t) − (2/3)ln³(1 + t) − 2 ln(1 + t)Li₂(1/(1 + t)) − 2Li₃(1/(1 + t))
                                              + ln²2 ln t + (ln t)³/12 + 2 ln 2 Li₂(−t) + ln t Li₂(−t) − Li₃(−t) + (ln 2/2)ln² t.

**Added criterion N6** (part `lc2`, not part of `run_01`): this Lc2 against its quadrature at θ = 0.3, 0.9, 1.4 (30 digits), and L₃ closed (S4's B with this Lc2) against −2h₃(1) + uC₃
by quadrature at the same points (30 digits, 30 guard digits in the integrand, quadrature at working precision 45). **Added control** `wrong_Lc2` (the sign of Li₃(−t) in F): fires N6
(`dev_18_lc2_wrong_Lc2`: −3.6 and 0.3 digits). An earlier scratch version of N6 ran its quadrature at 75 digits and failed at 2.4 digits: tanh-sinh nodes at θ ~ 1e-70 with integrand
cancellation ε/θ; the same cancellation as N3, N4b. Fixed by guarding the integrand only (as N3g, N4bg). `order4.py` after this amendment differs from `dev_16_order4_final.py` (the code of
`run_01` to `run_04`) by 47 added lines and 3 changed lines (the usage line, the mutation list, the default parts); `cmp` against `dev_18_order4_wip2.py`: identical.
