# I263-rpi5: Ω₅ from the order-7 matching integral of Paper III's large-D expansion

Machine: rpi5-ubuntu (Ubuntu, 4 cores, 8 GB, aarch64; Python 3.14.10 venv `negative-mass-venv314`, mpmath 1.3.0 with the pure-Python
backend, sympy 1.14.0), shared with other projects (at most 3 processes of mine, `nice -n 10`, `OMP_NUM_THREADS=1`; runs longer than a few
minutes are systemd user units `nm-i263-*`). Runner `negative-mass-rpi5-i263` (Claude Code, Sonnet 5.5, account claude-me2), started by the
coordinator over hc. Issue: https://github.com/nmoinvaz/negative-mass/issues/263 (milestone G5).
Code: worktree `~/Source/negative-mass-i263`, branch `wip/i263-omega5` from f0192c7 (`main`); script `notes/wormhole_largeD/order7.py` (it imports
`PanelB` from the unchanged `order4.py`), output `order7_output.txt`, note `omega5.md`. Pushes: `git push origin HEAD:refs/heads/wip/i263-omega5`.
Development runs `dev_NN_*` and runs of record `run_NN_*` keep stdout (`.log`), stderr (`.err`) and the exit code (`.rc`) beside this file
(`devrun.sh`, `runrec.sh`: `runrec.sh` also keeps `/usr/bin/time -v` and the machine's load); nothing is overwritten, reruns are numbered.
`dev_NN_order7_wip.py` is the code of the development runs of that number. Status words as in AGENTS.md: agreement of an integral or a series
with a constant is *numerical evidence*; a PSLQ relation is an *identification* (a *conjecture* until a by-hand reduction meets it); a step
checked by sympy is *checked symbolically*; a closed form reached by hand with each step checked is *derived*. No sentence here claims novelty.

## What was run before this file (disclosure)

| runs | what |
|---|---|
| `dev_01` | `order7.py sym cache`: E0 through k = 7 (sympy, residual 0), CACHE (cached chain = uncached chain, bit for bit, on a small grid) |
| `dev_02` … `dev_07` | `order7.py grid` on (40, 1/2, 18, 120), (60, 2/5, 24, 200), (60, 2/5, 24, 150), (100, 1/4, 30, 260), (60, 2/5, 24, 100), (60, 2/5, 24, 90): timing, digits against the closed forms of Ω₀ … Ω₄, the working precision needed |
| `dev_08`, `dev_09` | the same on (100, 1/4, 30, 165) and (100, 1/4, 30, 150) (the working precision ladder at N = 100) |
| `dev_10` | (170, 1/4, 38, 285): timing for the grids of record |
| `dev_11` … `dev_14` | `xsym` (sympy: P′ = g₄u, W′ = w₄′), `exch7` (E1 … E5 and the reduced form on the E-grid; `dev_12` had E123_7 relative to G₇, which is ≈ 0 at the root: fixed in `dev_14`), `reduce7` (RD1 and A7, `dev_13`) |
| scratch | the remainder checks on the 148-digit Ω₅ of `dev_05` (to set R6, R7, X3's bars), the decomposition of the integrand of G₇ in sympy |

**Seen before this file:**
- Ω₅ = 40860.455354525687312544064826003370427803937221541648542145851754614473138612946084795122442852581665254897136411397869…
  (`dev_02` … `dev_05`: equal to 48, 77 and 148 digits between the grids); the two-point extrapolation of #220 gave ≈ 40860.
- **The working digits.** At order 7 the cached chain loses about 12 digits to rounding: N = 100, w = 1/4 gives 148.5 digits of Ω₀ … Ω₄ at 165 and 260 working digits and 146.6 at 150
  (`dev_05`, `dev_08`, `dev_09`), N = 60, w = 2/5 gives 77.8 digits at 90, 100, 150 and 200. #220 used 1.6 times the digits it expected; the grids below use the expected digits plus about 20.
- **Timing** (3 processes): (100, 1/4, 30, 260) 245 s (panel setup 15 s), (100, 1/4, 30, 165) 180 s, (60, 2/5, 24, 200) 42 s; (170, 1/4, 38, 285) about 124 s per k-step of 8 integration units at the start (`dev_10`).
  #220's G1 took 35.7 min for the uncached chain (90 integration units); the cached chain has 48 units for k = 2 … 7.
- The derivatives of the generators and the weights of the steps E4 (at one level higher), E2W and E5 (below) hold on the E-grid to 44 to 50 digits (`dev_12`, `dev_14`: 12 of 12), the decomposition of the integrand of G₇ against the
  numeric integrand of closed forms to 45 digits (`dev_13`, RD1).
- The remainder with the 148-digit Ω₅ (`scratch_rem`): rem₆·s⁵ = 42708.4, 41781.5, 41220.7, 41044.2 at D = 1000, 2000, 5103, 10⁴ (the #220 table), Ω₆ ≈ 3.67·10⁶ (rem₇·s⁶ = 3684792, 3678586, 3674753, 3673534),
  the refit of #195's 64 values of W² gives Ω₅ to 7.5e-28 (K = 14) … 3.3e-25 (K = 44). The bars of R6, R7, X3 below are set knowing those numbers.

**Not seen:** the real Ω₅ on the grids of record; any PSLQ on the real Ω₅ (the development runs have no PSLQ); method A's value of Ω₅ (`dev_13` was still running when this was written).

## Convention

As in README.md, matched.py, order3.py … order6.py and #195: s = 2(D − 3), ε = 1/s, W²a² = s + Ω, Ω = Ω₀ + Ω₁ε + Ω₂ε² + Ω₃ε³ + Ω₄ε⁴ + Ω₅ε⁵ + …, R = r^s, l = ln R = −2 ln cos θ.
Ω₀ = −4 ln 2, Ω₁ = 2π²/3 + 8 ln²2, Ω₂ = 80ζ(3) − (8/3)π² ln 2 − (32/3) ln³2 (#26), Ω₃ = 22π⁴/45 + (16/3)π² ln²2 + (32/3) ln⁴2 − 320ζ(3) ln 2 − 384ζ(3) (#208, #209),
Ω₄ = −10432ζ(5) − 160π²ζ(3) + 640 ln²2 ζ(3) − (64/9)π² ln³2 − (88/45)π⁴ ln 2 − (128/15) ln⁵2 − (2432/45)π⁴ + 1536 ln 2 ζ(3) + 3072ζ(3) (#220). Ω₅ ≈ 4.086·10⁴ is an estimate (#220).
In 1/(D − 3) the coefficient of order k is Ω_k/2^k.

## The order equations at k = 7

#26's equations, unchanged, for k = 0 … 7:

    dY_k/dl = F_{k−1},  F_{k−1} = Σ_{j=0}^{k−1} L_{k−1−j} l^j/j!                     (Y_0 = 1, Y_k(R = 1) = 0)
    (R − 1)L_k′ − L_k/2 = h_k,   h_k = (1 − 1/R)L_{k−1} + Σ_{j=0}^{k−1} Y_j c_{k−j} + Y_k/2,   h_k(1) = Ω_{k−1}
    c_1 … c_6 as in `order6.py`
    c_7 = Ω₀ l⁶/720 + Ω₁ l⁵/120 + Ω₂ l⁴/24 + Ω₃ l³/6 + Ω₄ l²/2 + Ω₅ l + Ω₆ + l⁷/3360 − l⁶/720 + l⁶/(720R)                      (new)

c_7 is the coefficient of ε⁷ of (1 + εΩ)e^{εl} − (½ + ε)(1 − 1/R)e^{−εl} − e^{−εl}/(2R) (check E0, sympy, residual 0, through k = 7). The solution analytic at the throat is L_k = −2Ω_{k−1} + (R − 1)^{1/2}C_k,
C_k = ∫_1^R (h_k − Ω_{k−1})(R′ − 1)^{−3/2}dR′, and the mode needs G_k = C_k(∞) = 0. G_k is affine in Ω_{k−2} with slope −4π: G_2 = 0 gives Ω₀, … , G_6 = 0 gives Ω₄, **G_7 = 0 gives Ω₅** (Ω₆ drops out of G_7: it is
h_7(1), subtracted). Ω₀ … Ω₅ are solved in turn by one function (`omega_chain`) with no closed form of Y_k or L_k and no input value of Ω₀ … Ω₄: the planted orders k = 2 … 6 are the same path as the new k = 7.

## Method B at order 7, and the cached chain

As in I220-rpi5's README: variable v = √l (R = e^{v²}), panels of width w on [0, V], N Chebyshev nodes per panel, cumulative integrals by the spectral integration matrix (`PanelB` of order4.py, shared;
`PanelK` of order7.py replaces its sums by `mp.fdot` and caches l^j/j! and c_m on the nodes, which changes timing and the last rounding only). For each k: Y_k = ∫₀^l F_{k−1}dl from the left; h_k from the table; the tail
C_right(v) = ∫_v^V (h_k − h_k(1))R(R − 1)^{−3/2}2v dv from the right; L_k = −2h_k(1) − u C_right (u = √(R − 1)); G_k = C_right(0). Two evaluations of G_k (Ω_{k−2} = 0 and 1) give Ω_{k−2} and the slope.

**What is new in the chain.** Y_j, L_j (j ≤ k − 2) do not depend on Ω_{k−2}, so step k keeps the levels 0 … k − 2 of the earlier steps and computes Y_{k−1}, then, for each of the two trial values, L_{k−1}, Y_k and G_k, then
L_{k−1} at the root: 8 integration units per step, 48 for k = 2 … 7 (the uncached chain of #220 has 2(2k + 1) units at step k, 120 for k = 2 … 7). The operations and their order are those of the uncached chain;
**CACHE** compares the two chains on a small grid and requires equal Ω₀ … Ω₅ to the working digits minus 5. The root's residual |G_k(root)|/|slope| is also reported at every k (RES), which tests that the affine G_k has its root there.
For a mutation that changes an input of the lower levels (`wrong_Om0` … `wrong_Om4`) the chain is recomputed from level 0 (it must reach every level).

## Grids of record (declared before the runs of record)

The digits law of #208 and #220, digits ≈ N log₁₀(7.7/w), holds at order 7 (`dev_02` … `dev_09`: 48.7, 77.8, 148.5 digits for N = 40, 60, 100). The working digits are the expected digits plus about 20.

| name | N | w | V | working digits | panels | expected digits (N log₁₀(7.7/w)) | tail e^{−V²/2} V^{28} | expected wall |
|---|---|---|---|---|---|---|---|---|
| G1 | 285 | 1/4 | 48 | 445 | 192 | 424 | 10⁻⁴⁵³ | about 1.8 h (panel setup about 25 min of it) |
| G2 | 275 | 3/10 | 47 | 410 | 157 | 388 | 10⁻⁴³³ | about 1.2 h |

Also run and reported, not gated: B1 (60, 2/5, 24, 100), B2 (100, 1/4, 30, 170), B3 (170, 1/4, 38, 285). **The control grids** (`--cgrids`, used only for the controls of the grid-dependent mutations): C1 = (90, 1/4, 29, 160) (expected 134 digits),
C2 = (85, 3/10, 28, 150) (120), named G1 and G2 in a `--cgrids` run, with the same bars (100 digits) as the grids of record. The agreement of G1 and G2 on Ω₅ is an estimator range over grid and precision, **not a rigorous bound**; nothing here is a rigorous enclosure.

**What the evaluations share** (recorded as AGENTS.md asks): the table of c_m and h_k (one sympy expansion, E0, extended to k = 7), the analytic-at-throat condition, `PanelB` and mpmath. G1 and G2 share the code and differ in N, w, V and precision.
#195's 64 values of W² (the full equation in a Rust crate, no matching) share none of the matched machinery and are the independent reference for Ω₅ (X3); the closed forms of Ω₀ … Ω₄ (#26, #208, #209, #220) are the planted truth.

## Criteria (each can fail; written before the runs of record)

"d digits" means a relative difference ≤ 10^−d. The code is `order7.py` at commit 7d93fc3 of `wip/i263-omega5` (the code of the runs of record, unless a later commit is named in "Results of record").

| id | statement | bar |
|---|---|---|
| E0 | the table of h_k (k = 0 … 7) and dY_k/dl (k = 1 … 7) equals the ε-expansion of the master equation | sympy residual 0 |
| CACHE | the cached chain equals the uncached chain on (24, 1/2, 12, 60 digits): Ω₀ … Ω₅ | relative difference ≤ 10^−55 |
| PL0 … PL4 | planted: Ω₀ … Ω₄ of G1 and G2 against their closed forms, the same code path that gives Ω₅ | 100 digits each (the issue's bar) |
| PLW | the control `wrong_Om_i` moves Ω_{i+1} of G1 and G2 (evaluated only under those mutations; the control's own statement, not a check of the result) | change > 10⁻³ |
| SL | the evaluated slope of G_k in Ω_{k−2} against −4π, k = 2 … 7, G1 and G2 | 100 digits |
| RES | max over k = 2 … 7 of \|G_k at the chain's root\|/\|slope\| | 10⁻¹⁰⁰ |
| M5 | Ω₅ of G1 against G2 (two grids, two precisions) | 100 digits (the issue's) |
| RNG | Ω₅ of G1 and G2 between 4.0e4 and 4.2e4 | the issue's range |
| X3 | Ω₅ of G1 and G2 against the polynomial extrapolation in 1/s of #195's 64 values of W² (qd, 60 digits, D = 50 … 10⁴) with Ω₀ … Ω₄ fixed at the closed forms: y = (W² − [s + Ω₀ + … + Ω₄/s⁴])s⁵ = Ω₅ + Ω₆/s + …, the K points of largest s, K = 14, 18, 22, 26, 30, 36, 44 | 1e-22 on every window (an estimator range, not a bound; set knowing 7.5e-28 … 3.3e-25 on a development Ω₅) |
| R6 | two-point extrapolation (s₂x₂ − s₁x₁)/(s₂ − s₁) of rem₆·s⁵ from D = 5103, 10⁴ against the computed Ω₅ | relative 10⁻⁴ (an estimate) |
| R7 | the seven-term series (Ω₁ … Ω₅ of G2) against #195's W²: \|rem₇·s⁶(D = 10⁴) − rem₇·s⁶(D = 5103)\| (a wrong Ω₅ adds (error)·s, 10⁴ per unit) | 2500 (set knowing 1219) |
| E1_7, E2_6, E2_5, E2_4, E3_7, E123_7, E4_7, E2Wa, E2Wb, E5_7, G7R, LC2 | on the hierarchy of the E-grid (40, 1/2, 18, 100 digits, 36 panels; its own Ω₀ … Ω₅), at Ω₅ = its root, 0 and 1/2: E1 at k = 7; E2 at m = 6, 5, 4; E3 at m = 6; their sum E123 for G₇; E4 (the order-6 step that removes Y₄), now removing Y₅; E2Wa, E2Wb: E2 with a weight, removing L₄; E5, the new step that removes Y₄ (below); G7R, G₇ against the reduced form with no Y₄ … Y₆, L₄ … L₆; LC2, the nodes' ∫ℓ² against J₂ | 30 digits (relative to the largest term for E1_7, E123_7, G7R) |
| XS | sympy: P′ = g₄u, W′ = w₄′ with the generators' derivative rules, and w₅ equals order 6's w₄ | residual 0 |
| PQ1 … PQ9 | PSLQ tool checks of the bases Q1 … Q9 (below): the planted relation is recovered exactly and the perturbed basis on the planted target finds nothing | exact recovery; none |
| RD1, A7 | the decomposition of the reduced integrand into C^a D₃^b Lc2^c against the numeric integrand of closed forms at four points; method A: Ω₅ from G₇ by quadrature (40 digits, 150 guard digits) of that integrand at Ω₅ = 0, 1, and its slope against −4π | RD1 30 digits; A7 30 digits against G1, G2, slope 30 digits |

Reported and not gated: the digits of G1, G2 against B1, B2, B3; Ω₅ to the working digits of every grid; rem₆·s⁵, rem₇·s⁶ and Ω₆ ≈ 3.67·10⁶ at the D of #195's list; each PSLQ verdict on the real Ω₅ (a relation not found is a result, not a failed check).

## The steps of the reduction by hand (declared before the runs)

E1, E2, E3 are #209's (derived there for every k). At k = 7 (m = 6) they leave Y₀ … Y₅ and L₀ … L₅ in G₇ = 8∫H₆ℓ/S + 2∫(F₆ − L₆) + 2∫(S′₇ − Ω₆)/S − 4∫(ℓ − Ω₀)F₅ (check E123_7), H₆ = S L₅ + Σ_{j≤5}Y_j c_{6−j}, S′₇ = Σ_{j≤5}Y_j c_{7−j}.
**E4 extends to Y₅ unchanged** (declared before the run, as the task asks): the weight of Y₅ is w₅ = (8ℓc₁ + 2c₂ + 4Ω₀ℓ)/S = (2Ω₁ + 8Ω₀ℓ − 22ℓ²)/S − 12ℓ, the same as the weight of Y₄ at k = 6 (the pairs (c₁, c₂) and the E2-collapse of the top L are
the same at every k), so ∫Y₅w₅ = −2∫(22ℓ² − 8Ω₀ℓ − 2Ω₁ + 16uC)F₄, with F₄ = L₄ + L₃l + ½L₂l² + ⅙L₁l³ + (1/24)L₀l⁴ (check E4_7). L₅ is removed by the collapse of its weight to 4Ω₀ and E2 at m = 5 (8ℓ + 2l − 4(ℓ − Ω₀) = 4Ω₀).
**What is new at k = 7** is that L₄ and Y₄ stay:
- **E2W**, E2 with a weight g(θ): ∫L_m g dθ = −2∫P h_m/S, P′ = g tan θ, P(0) = 0 (from (L cot θ)′ = 2h/S; the boundary terms [L cot θ·P] vanish as in E2). The weight of L₄ is 12ℓ² (E2Wa: P = −4ℓ³), and after E4 it is
  g₄ = −32ℓ² + 16Ω₀ℓ + 4Ω₁ − 32uC, with P = 32ℓ³/3 − 8Ω₀ℓ² − 4Ω₁ℓ − 32(uC + ℓ² + 2 ln 2 ℓ − D₃/2) (E2Wb); D₃ = Cl₃(π − 2θ) + ¾ζ(3), D₃′ = 2C.
- **E5**, the Y₄ step: the weight of Y₄ is w₄′ = [8ℓc₂ + 2c₃ + 8Ω₀ℓc₁ − P]/S, with primitive W = −2Ω₂cot θ − a₁(ℓ cot θ + θ) − a₂(ℓ²cot θ + 2Lc1) − a₃(ℓ³cot θ + 3Lc2) + 32(−Cℓ + 2Lc2 + 2 ln 2 Lc1) + 16D₃ cot θ − 20Lc2 − 8Ω₀Lc1 + const, a₁ = 8Ω₁ + 8Ω₀² + 64 ln 2,
  a₂ = 32 − 28Ω₀, a₃ = −20/3, Lc1 = (C − 2 ln 2 θ)/2, Lc2 = ∫₀^θℓ², and the constant fixed by W(π/2) = 0. **The term Z = ∫C cot θ, which would be a new generator, cancels** between 32∫uC/S and −16∫D₃/S, so W is in the generators of order 6
  (the same kind of cancellation as at order 6, where the cot θ part of D₃'s primitive cancelled the 1/u part of the C coefficient). ∫Y₄w₄′ = −2∫W u F₃ (check E5_7, boundary terms O(θ) at 0 and O(x lⁿ) at π/2).
So **G₇ needs only Y₀ … Y₃ and L₀ … L₃** (closed forms of #26 and #208): G₇ = ∫₀^{π/2}Ĩ₇dθ. Its decomposition in the generators has the monomials 1, C, D₃, Lc2, C², CD₃, CLc2 (as at order 6) and the new D₃², D₃Lc2, Lc2² (RD1).
**The finite-part reduction to master integrals** (as order6.py's `reduce6`) is attempted after the runs and reported with how far it got; it is not gated here (it gets its own amendment with its checks and controls before it runs).

## PSLQ (declared before the run of record)

`mp.pslq(x, tol, maxcoeff = H, maxsteps = 10⁶)` on [Ω₅, constants…], Ω₅ of G2 rounded to d = min(340, ⌊digits G1 and G2 share⌋ − 32) digits (at least 30), constants at d digits. Tolerance τ = 10^−(d − 12). The residual |Σ cᵢxᵢ| is also computed from the integer
vector returned. Budget (n + 1)·log₁₀(2H + 1) + 1, n = the number of constants. A relation counts only if (i) it holds at τ, (ii) its budget with the declared H is below d, (iii) the basis with the first constant of non-zero coefficient shifted by √2·10⁻³ finds nothing, (iv)
the coefficient of Ω₅ is not zero, and (v) it holds at d + 20 digits (tolerance 10^−(d + 8)) on both G1 and G2 (the grids share at least d + 32). Otherwise "not found" or "found but does not count" is reported with the basis, d, τ and H. A relation that PSLQ alone suggests is a *conjecture* until a by-hand reduction meets it.

The monomials are ln 2^a (π²)^b ζ(3)^c ζ(5)^e of weight a + 2b + 3c + 5e (ln 2: 1, π²: 2, ζ(3): 3, ζ(5): 5, products add); the polylogarithm products are Li₄(½)·{1, ln 2, ln²2, π²}, Li₅(½)·{1, ln 2}, Li₆(½). **The task text names π²ζ(5) among the weight ≤ 6
constants; it has weight 7**, so it is in Q9 (weight ≤ 7: the 11 monomials of weight 7 are added), not in Q1 … Q8.

| basis | constants besides Ω₅ | n | H | budget |
|---|---|---|---|---|
| Q1 pure weight 6 | ln⁶2, π²ln⁴2, π⁴ln²2, π⁶, ζ(3)ln³2, π²ζ(3)ln 2, ζ(3)², ζ(5)ln 2 | 8 | 10¹² | 111.7 |
| Q2 pure weight 6 with the polylogarithms | Q1 and Li₄(½)ln²2, Li₄(½)π², Li₅(½)ln 2, Li₆(½) | 12 | 10¹² | 161.0 |
| Q3 weights 6, 5 | Q1 and the 6 monomials of weight 5 | 14 | 10¹¹ | 170.5 |
| Q4 weights 6 … 4 | Q3 and the 4 of weight 4 | 18 | 10¹⁰ | 196.7 |
| Q5 weights 6 … 3 (the weights Ω₄ has, shifted: Ω₄ had 5, 4, 3) | Q4 and the 3 of weight 3 | 21 | 10¹⁰ | 227.6 |
| Q6 weight ≤ 6 | Q5 and ln²2, π², ln 2, 1 | 25 | 10⁹ | 243.0 |
| Q7 weight ≤ 6 with all the polylogarithm products | Q6 and the 7 products | 32 | 10⁹ | 308.0 |
| Q8 weights 6 … 3 with the polylogarithm products | Q5 and the 7 products | 28 | 10⁹ | 270.7 |
| Q9 weight ≤ 7 | Q6 and the 11 monomials of weight 7 (ln⁷2, π²ln⁵2, π⁴ln³2, π⁶ln 2, ζ(3)ln⁴2, π²ζ(3)ln²2, π⁴ζ(3), ζ(3)²ln 2, ζ(5)ln²2, π²ζ(5), ζ(7)) | 36 | 10⁸ | 308.0 |

**Planted truth** (the tool's size check): the same call on x = (Σ cᵢbᵢ)/den, cᵢ integers of 3 to 4 digits and den ∈ {3, 5, 7, 9, 11, 13, 15, 21, 45} drawn once with `random.Random(seed)` (seeds 263001 … 263009 for Q1 … Q9), bᵢ the true constants of the basis:
the vector (den, −c₁ … −c_n) must be returned (up to sign), and the basis with b₂ + √2·10⁻³ must find nothing. Odd powers of π, Catalan's constant, β(4) and the weight-6 alternating sums beyond Li₆(½) (the space of alternating
sums of weight ≤ 6 has one more irreducible than Q7 holds) are not in any basis: **a "not found" is for these bases only**.

## Controls and what they break (targets are declared in amendment A1, after their development runs and before the controls of record)

Every check has a `--mutate=NAME` control. A control is **on target** when the set of checks that fire (FAIL) is exactly the declared set. Groups, each with its own nominal run:
(T1) grid-dependent mutations on the control grids: `wrong_h`, `wrong_c6`, `wrong_c7`, `wrong_Om0` … `wrong_Om4`, `coarse_B`, `short_tail`, `stale_cache` (parts evals values remainder, and `pslq --bases=Q1,Q3 --no-real`, with H lowered to
10^max(4, ⌊(d − 25)/(n + 1)⌋ − 1) because d is about 90 there);
(T2) post-processing mutations on the saved Ω's of record: `pslq_wrong_basis`, `pslq_wrong_target` (parts values pslq with `--no-real --bases=Q1,Q3,Q5 --pslq-cap=150`), `wrong_Om5_series` (Ω₅ + 10 in R6, R7), `wrong_closed4` (Ω₄'s closed form + 10⁻³: PL4);
(EX) `exch7`: `e1_sign`, `e2_weight`, `e3_factor`, `e4_g`, `e4_noC`, `e2w_g`, `e2w_P`, `e5_noD3`, `e5_const`, `wrong_h`, `wrong_c7`;
(RD) the controls of the finite-part reduction, with their amendment.

## Runs of record

On the grids of record, as separate processes (each started with `runrec.sh`, `nice -n 10`, `OMP_NUM_THREADS=1`, `systemd-run --user`):

| run | command (from `notes/wormhole_largeD`) | expected |
|---|---|---|
| `run_01` | `order7.py sym xsym cache exch7` | 15 checks, a few minutes |
| `run_02` | `order7.py evals --grids=G1 --save=G1.json` | about 1.8 h |
| `run_03` | `order7.py evals --grids=G2 --save=G2.json` | about 1.2 h |
| `run_04` | `order7.py evals --grids=B1,B2,B3 --save=B.json` | about 20 min |
| `run_05` | `order7.py values pslq remainder --load=G1.json,G2.json,B.json --w2raw=inputs_w2_growthD.txt` | PSLQ at d = 340 |
| `run_06` | `order7.py reduce7 --load=G1.json,G2.json,B.json` | RD1, A7 |

**Stop condition:** any single run not finished in 3 h of wall time is stopped and reported with what finished. Memory is reported only. If G1 or G2 stops, the other grid and B1 … B3 are reported and PSLQ runs at the digits they share.

## Amendments

**A1 (2026-11-27, 14:30, before the runs of record of `reduce7`, of the exchange controls and of PSLQ): the reduction by hand, its checks, the split of PSLQ, and the targets of the exchange controls.**

*What had been seen before this amendment* (disclosure; `dev_13` … `dev_20`, scratch in the issue's comment of 14:12):
- `dev_15` (`reduce7` on the code before RD5b and RD5c): RD1 … RD6 pass (6 of 6): the 37 integrations by parts leave I_final with no u, 1/u or new generator; G₇(Ω₅ = 0) = 513467.62545644651939787084471209 from them
  equals the quadrature of the integrand of closed forms to 39.1 digits; the masters of the closed form agree with 30-digit quadrature to 25.6 … 30.0 digits (RD5's bar is 25 for that reason); the two masters ⟨lt²C²⟩, ⟨lt³D₃⟩ were identified first
  by PSLQ at 55 digits (`scratch_prototypes/masters2.out`: ⟨lt²C²⟩/π = (3/4)ζ(3)² − (95/96)ζ(6), ⟨lt³D₃⟩/π = (9/16)ζ(3)² − (11/4)ζ(6)); ⟨lt³D₃⟩ was then also derived by hand (generating function of the Beta moments and two Euler sums).
- **The closed form of Ω₅ was in hand, and equal to a 148-digit development grid (`dev_05`) to 148.1 digits, before any PSLQ on the real Ω₅ ran.** The PSLQ of the runs of record confirms known integer coefficients; it is not a blind search. The bases Q1 … Q9 were declared before the reduction was coded.
- `dev_20_ex_*` (the exchange controls, 11 mutations): the targets below are what they fired; the two that did not fire as I first wrote them are results: `e2w_g` only reaches E2Wa (the hook is in E2Wa's left side; E2Wb's weight and P are built together),
  and `e5_const` is silent because the constant of W is zero: W(π/2) = 0 identically once Ω₀ = −4 ln 2 and Ω₁ = 2π²/3 + 8 ln²2 (the 64J₂ − 32πq² − 24πqΩ₀ − 4πΩ₀² − 4πΩ₁ of the limit cancels).

*The checks of the reduction* (`order7.py reduce7`, run `run_07_reduce7` on the grids of record; bars written after `dev_15`):

| id | statement | bar |
|---|---|---|
| RD1 | the integrand of G₇ after E1 … E5 as coefficients of C^a D₃^b Lc2^c, and again in lt = ln(2 cos θ), K₂ = ∫lt² (the masters' variables), against the numeric integrand of closed forms at θ = 0.2, 0.7, 1.1, 1.4 | 30 digits |
| RD2 | the 37 integrations by parts: I_start − Σ dF − I_final = 0 symbolically; the primitives of the D₃² and D₃ coefficients have residual 0; no u, 1/u left in I_final | exactly |
| RD3 | the 1/u part of the CD₃ coefficient after the D₃² step, the 1/u part of the C coefficient after the D₃ step, and K₃ other than in CK₃ all vanish; the slope of G₇ in Ω₅ is −4π | exactly |
| RD4 | the series (order 10) of lt, u, 1/u, C, D₃, K₂, K₃ at θ → π/2 and 0 (the finite-part kit) against the functions at x = θ = 10⁻³ | 1e-24 relative |
| RD5 | the 18 master integrals ⟨C^a D₃^b K₂^c θ^j lt^k⟩ against their closed forms, quadrature at 30 digits | 25 digits |
| RD5b | ⟨lt²C²⟩ and ⟨lt³D₃⟩ against their closed forms at 100 digits (found at 55) | 90 digits |
| RD5c | the Euler sums used (ΣH_n/n³, ΣH_n/n⁵, ΣH_n²/n⁴, ΣH_n^{(2)}/n², ΣH_n^{(2)}/n⁴, Σ(H_n^{(2)})²/n², ΣH_nH_n^{(2)}/n³) against their closed forms, and (π/4)Σs_m² against π(3ζ(3)²/4 − 95ζ(6)/96), Euler–Maclaurin at 40 digits | 30 digits |
| RD6 | G₇(Ω₅ = 0) = Σ B[F_i] + ∫I_final (quadrature at 45 digits) against the quadrature of the integrand of closed forms | 30 digits |
| A7 | method A: Ω₅ from the closed-form integrand at Ω₅ = 0, 1 (quadrature at 40 digits, 150 guard digits) against G1, G2, and its slope against −4π | 30 digits |
| RD7 | Ω₅ of the closed form of the reduction (boundary terms + masters) against G1, G2 | 100 digits |
| RD8 | the PSLQ relation of `run_06*` for Q6 equals 315 × the closed form's coefficients (the integer vector) | equal |

*Not derived by hand:* ⟨lt²C²⟩ (identified; by Parseval it is (π/4)Σs_m², an Euler-sum combination that RD5c checks numerically). The Euler sums are taken as known facts, checked numerically by RD5c; none is proved here.

*PSLQ is split over processes by basis* (same code, same bases, same d; each process loads `G1.json`, `G2.json`): `run_06a` Q1 … Q4, `run_06b` Q5, Q6, `run_06c` Q7, Q8, Q9 (parts `pslq --bases=…`); `run_05` is `values remainder`; `run_07` is `reduce7`.

*Targets of the exchange controls* (`declared_ex.json`; read from `dev_20_ex_*` and `dev_14_exch7`; a control is on target when the set of checks that fire is exactly the declared set):

| control | what it breaks | fires | silent |
|---|---|---|---|
| `e1_sign` | the sign of E1's second integral | E1_7, E123_7, G7R | E2_6 … E2_4, E3_7, E4_7, E2Wa, E2Wb, E5_7 |
| `e2_weight` | E2's weight ℓ as ℓ + ln 2 | E2_6, E2_5, E2_4, E123_7, G7R | E1_7, E3_7, E4_7, E2Wa, E2Wb, E5_7 |
| `e3_factor` | E3's 4 as 2 | E3_7, E123_7, G7R | E1_7, E2_x, E4_7, E2Wx, E5_7 |
| `e4_g` | E4's 22ℓ² as 20ℓ² | E4_7, E5_7, G7R | E2Wb: its weight and P are built from the same g |
| `e4_noC` | E4's 16uC dropped | E4_7, E5_7, G7R | E2Wb (same reason) |
| `e2w_g` | E2Wa's 12ℓ² as 10ℓ² on the left | E2Wa | everything else |
| `e2w_P` | P's D₃/2 dropped | E2Wb, E5_7, G7R | E4_7, E2Wa |
| `e5_noD3` | W's 16D₃ cot θ dropped | E5_7, G7R | E4_7, E2Wa, E2Wb |
| `e5_const` | W(π/2) not subtracted | none: **the constant is zero** | all |
| `wrong_h` | the sign of −l/R in c₂ (Ω₀ ≠ −4 ln 2 then) | E4_7, G7R | E1_7, E2_x, E3_7, E2Wx, E5_7: E4 is the only step that uses Ω₀ = −4 ln 2 |
| `wrong_c7` | the sign of l⁶/(720R) in c₇ | none: **E1 … E5 hold for any table** (E0 and the values see it) | all |

**A2 (2026-11-27, 16:20, after `run_02` … `run_04`, `run_06c`'s Q7, before the controls of record of the groups T1, EX, RD): what was seen, two discrepancies, and the targets of T1 and RD.**

*What had been seen before this amendment* (`run_01` … `run_04`, `dev_21` … `dev_24`):
- `run_01` (15 of 15), `run_02` (G1: N 285, 1 h 34 m 46 s, panel setup 8 m 22 s, peak 1.02 GB), `run_03` (G2: N 275, 1 h 4 m 52 s, panel setup 6 m 52 s, peak 0.79 GB), `run_04` (B1 … B3: 19 m 10 s): the grids' Ω₀ … Ω₅ are saved in `G1.json`, `G2.json`, `B.json`; I read them
  (Ω₅ = 40860.455354525687312544064826033704278039372215373284079454102667838994220332959565447528…, the same to the digits printed in both). `run_06c` printed `PQ7` and the real PSLQ of Q7: **found**, the relation of the derived closed form
  (315 Ω₅ − 1792 ln⁶2 − … = 0, no Li term), after which the controls below were run and the targets read.
- **Discrepancy 1: the cap of d.** The README above says d = min(340, ⌊digits shared⌋ − 32); the code (committed at 7d93fc3, before the README) has `PSLQ_DIGITS = 330`. The runs use 330 (the two grids share 382.7 digits, tolerance 1e-318, verification at 350 digits).
  Every budget is below 318 (Q7 307.9, Q9 308.1), so the criteria are unchanged; this is a typo of the README, not a change of the code.
- **Discrepancy 2: RD5c is its own part.** `reduce7` first held RD5c (the Euler sums by Euler–Maclaurin at 40 digits); `dev_23_rd_nominal` ran 28 minutes without finishing it and I stopped its unit (partial log `dev_23_rd_nominal_stopped.log`). RD5c is now the part `euler7` at 34 digits (bar 30), run as `run_08_euler7`, with its own controls.
  `reduce7` has RD1 … RD7, RD5b, LN2, RD8 and A7. The checks' statements are unchanged.
- **Two controls failed to run at first, and were fixed:** `dev_21_t1_wrong_Om0` … `wrong_Om4` died with `KeyError: 'resid2'` (the uncached chain, used by the wrong-input mutations, had no residuals), and `dev_21_t1_stale_cache` died with `KeyError: 2`.
  Both are fixed in `order7.py` (commit 4f6f020), and reran as `dev_21b_*`. The controls of record use the fixed code.
- **LN2** is a new check (not in A1): F(ε) = exp(4 ln 2 ε)(1 + Ω₀ε + … + Ω₅ε⁶) is free of ln 2 through ε⁶ (sympy). It was added to `reduce7` after the derived closed form was in hand; it fires under `rd_J5` and `rd_B`, which break the ln 2 structure.
- **Not seen yet:** the real PSLQ of Q1 … Q6, Q8, Q9; `run_05`; `run_07`; the T2 and `euler7` controls.

*Targets of the T1 controls* (`declared_t1.json`; read from `dev_21_t1_cnom` and `dev_21b_*`, on the control grids C1, C2 (`--cgrids`), parts `evals values remainder pslq --bases=Q1,Q3 --no-real`; PLW is silent in every `wrong_Om` control, not listed):

| control | fires | silent (declared results) |
|---|---|---|
| `wrong_h` | PL0 … PL4, RNG, R6, R7, X3 | SL, RES, M5 (both grids share the error), PQ1, PQ3 |
| `wrong_c6` | PL4, R6, R7, X3 | PL0 … PL3, SL, M5, RNG |
| `wrong_c7` | X3 | **R6, R7** (Ω₅ moves by less than their sensitivity), PL0 … PL4, SL, M5, RNG |
| `wrong_Om0` … `wrong_Om3` | PL(i+1) … PL4, R6, R7, X3 | PL0 … PLi, SL, M5 |
| `wrong_Om4` | X3 | **R6, R7** (+1/100 in Ω₄ moves Ω₅ by 0.027726 (PLW), below R6's bar), everything else |
| `coarse_B` | PL0 … PL4, SL, M5, PQ1, PQ3, R6, R7, X3 | RES, RNG; PQ1, PQ3 fire because PSLQ is given the few digits the coarse grids share |
| `short_tail` | PL0 … PL4, SL, R6, R7, X3 | **M5** (both grids share V), RES, RNG |
| `stale_cache` | PL2, PL3, PL4, RES, RNG, R6, R7, X3 | PL0, PL1, SL, M5 |

*Targets of the RD controls* (`declared_red.json`; `dev_24_rd_*` on `dev_cnom.json`; part `reduce7 --load=…`):

| control | what it breaks | fires | silent, and why |
|---|---|---|---|
| `rd_kit` | the sign of ln 2 in C's expansion at π/2 | RD4 | RD6, RD7: the finite parts of the C terms cancel in the sum, the closed form does not depend on it (as at order 6) |
| `rd_Dstep` | the sign of the P_{b−1} part of the primitive of the D₃ coefficient | RD2 | RD6, RD7: **a wrong primitive F is still an exact step I ← I − dF with const += B[F]**; only RD2's residual of the primitive sees it |
| `rd_J5` | J̃₅'s ζ(5) coefficient × 17/18 | RD5, RD7, LN2 | RD6 (the numeric integral does not use J̃₅) |
| `rd_master` | ⟨lt²C²⟩'s ζ(6) coefficient 95/96 as 94/96 | RD5, RD5b, RD7 | LN2 (A is free of ln 2) |
| `rd_B` | the sign of the boundary term of step CL | RD6, RD7, LN2 | RD5 |

**A3 (2026-11-27, 16:40, after `dev_24_euler_*` and `dev_25_t2_*`, before the T2 and `euler7` controls of record and the RD controls of record): the targets of T2 and of the Euler-sum controls.**
`run_05` (`values remainder`: PL0 … PL4, SL, RES, M5, RNG, R6, R7, X3 all pass, M5 382.7 digits), `run_06a` (Q1 … Q4: not found), `run_06b` (Q5, Q6: found) and Q7, Q8 of `run_06c` (found) were read before this amendment; the T2 controls had no target before `dev_25`.
The RD controls use the committed code be7b9cb (the only change since 2e70c66 is the constant of RD8, the relation of `run_06b`).

*Targets of the T2 controls* (`declared_t2.json`; `dev_25_t2_*` on `G1.json`, `G2.json`: parts `values pslq remainder --no-real --bases=Q1,Q3,Q5 --pslq-cap=150`; d = 150 and the budgets of the lowered H are below 125, so PQ5 passes in the nominal run; on the control grids `dev_22_t2_*` d = 88 and PQ5 failed in the nominal run for a budget above d, which is why these controls use the grids of record):

| control | what it breaks | fires | silent |
|---|---|---|---|
| `pslq_wrong_basis` | the first constant of every basis + √2·10⁻³ | PQ1, PQ3, PQ5 | everything else |
| `pslq_wrong_target` | the planted target × (1 + 10⁻²⁰) | PQ1, PQ3, PQ5 | everything else |
| `wrong_Om5_series` | Ω₅ + 10 in the series of R6, R7 | R6, R7 | everything else (X3 does not use the series) |
| `wrong_closed4` | Ω₄'s closed form + 10⁻³ | PL4, X3 | R6, R7 (they use the grids' Ω's) |

*Targets of the Euler-sum controls* (part `euler7`; `dev_24_euler_*`): nominal fires nothing; `rd_master` (the coefficient of ΣH_nH_n^{(2)}/n³ in the exact assembly, 101/48 as 100/48) fires RD5c (sympy residual ≠ 0).
`reduce7`'s `rd_master` (⟨lt²C²⟩'s ζ(6) coefficient) fires RD5, RD5b, RD7, as declared in A2.
