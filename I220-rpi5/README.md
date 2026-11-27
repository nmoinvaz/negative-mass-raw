# I220-rpi5: Ω₄ from the order-6 matching integral of Paper III's large-D expansion

Machine: rpi5-ubuntu (Ubuntu, 4 cores, 8 GB, aarch64; Python 3.14.10 venv `negative-mass-venv314`, mpmath 1.3.0 with the pure-Python
backend, sympy 1.14.0), shared with choptuik-large-d (at most 3 processes of mine, `nice -n 10`, `OMP_NUM_THREADS=1`; runs longer than a few
minutes are systemd user units `nm-i220-*`; units are in `units.txt`). Runner `negative-mass-rpi5-i220` (Claude Code, Sonnet 5.5, account
claude-me2), started by the coordinator over hc. Issue: https://github.com/nmoinvaz/negative-mass/issues/220 (milestone G5).
Code: worktree `~/Source/negative-mass-i220`, branch `wip/i220-omega4` from 79ba70d (`main`); script `notes/wormhole_largeD/order6.py` (it
imports `PanelB` from the unchanged `order4.py`), output `order6_output.txt`, note `omega4.md`. Pushes: `git push origin
HEAD:refs/heads/wip/i220-omega4`. Development runs `dev_NN_*` and runs of record `run_NN_*` keep stdout (`.log`), stderr (`.err`) and the
exit code (`.rc`) beside this file (`devrun.sh`, `runrec.sh`: `runrec.sh` also keeps `/usr/bin/time -v` and the machine's load); nothing is
overwritten, reruns are numbered. `dev_NN_order6_wip.py` is the code of the development runs of that number. Status words as in AGENTS.md:
agreement of an integral or a series with a constant is *numerical evidence*; a PSLQ relation is an *identification* (a *conjecture* until a
by-hand reduction meets it); a step checked by sympy is *checked symbolically*; a closed form reached by hand with each step checked is
*derived*. No sentence here claims novelty.

## What was run before this file (disclosure)

| runs | what |
|---|---|
| `dev_01` … `dev_03` | `order6.py grid --grid=N,w,V,dps` (first version, chain k = 2 … 6, no gate): (40, 1/2, 18, 120), (100, 1/4, 30, 260), (60, 2/5, 24, 200) |
| `dev_04` … `dev_06` | the first version of the full parts on the control grids: nominal, `wrong_c6`, `wrong_Om2` (`--no-real`). Their PSLQ runs of P2 and P3 used H = 10⁸ and 10⁷ at d = 113, whose budgets (150, 154) exceed d: the planted checks Q2, Q3 failed on the nominal run too (a chance relation in the perturbed basis). The control grids now use H = 10⁵ and 10⁴ (below) |
| `dev_07` … `dev_09` | the same on the next version: `dev_07` nominal (14 of 14) and `wrong_h` (stopped, partial log), `dev_08` `wrong_Om0` and `wrong_Om1` (stopped, partial log), `dev_09` `wrong_Om3`, `coarse_B`, `short_tail`. I stopped units `nm-i220-wA`, `wB`, `wX` myself when the code changed under their queued jobs |
| `dev_10`, `dev_11` | `order6.py exch6` (E1, E2, E3, E4 at k = 6 on the hierarchy: 6 of 6, 44 digits) and its first mutations (`e1_sign`, `e2_weight`, `e3_factor`; the rest stopped as above) |
| `dev_12` | the control matrix of the code of record on the control grids (`dev_12_order6_wip.py`; nominal 15 of 15, nine mutations) |
| `dev_13_exch_*` | `exch6` nominal and its seven mutations |
| `dev_14_load_*`, `dev_15_load_*` | the four controls of the post-processing on `dev_12_cnom.json`; `wrong_Om4_series` shifted Ω₄ by 1/100 in `dev_14` and was **silent on every check**, so it is declared with the shift 1 (`dev_15`) |
| scratch | `dev_refit_prototype.py`/`.log`: the extrapolation behind X2 on the control grid's Ω₄ (run once, before X2 was coded) |

**Seen before this file:** Ω₄ = −12794.49986002319463279201242038108593384471984131637817405690244443567494146446… on the grids (40, 1/2, 18, 120),
(60, 2/5, 24, 200), (100, 1/4, 30, 260), equal to #195's printed fit −12794.499860023 to 1.9463e-10, which is inside half a unit of its last digit
(5e-10: that is how X1's bar is read from the fit's printing, not from this difference); the grid ladder (48.7, 77.8, 148.8 digits of Ω₀ …
Ω₃ against the closed forms: the law digits ≈ N log₁₀(7.7/w) of #208 holds at order 6); the remainders of the six-term series rem·s⁵ =
42708.4, 41781.5, 41220.7, 41044.2 at D = 1000, 2000, 5103, 10⁴ (bars R5, R6 below are set knowing that order of magnitude, and are not
tuned to it); the polynomial extrapolation of #195's 64 values of W² to Ω₄ (Ω₀ … Ω₃ fixed at the closed forms): 5e-32 to 2e-29 from the
control grid's Ω₄ (windows K = 14 … 44; X2's bar 1e-25 is set knowing that); E1 … E4 and the reduced form hold to 44 digits on the E-grid.
**Not seen:** any PSLQ on the real Ω₄ (the development runs have `--no-real`; the real PSLQ is first run in the runs of record).

## Convention

As in README.md, matched.py, order3.py … order5.py and #195: s = 2(D − 3), ε = 1/s, W²a² = s + Ω, Ω = Ω₀ + Ω₁ε + Ω₂ε² + Ω₃ε³ + Ω₄ε⁴ + …,
R = r^s, l = ln R = −2 ln cos θ. Ω₀ = −4 ln 2, Ω₁ = 2π²/3 + 8 ln²2, Ω₂ = 80ζ(3) − (8/3)π² ln 2 − (32/3) ln³2 (#26), Ω₃ = 22π⁴/45 +
(16/3)π² ln²2 + (32/3) ln⁴2 − 320ζ(3) ln 2 − 384ζ(3) (#208, #209). Ω₄ = −12794.49986002 is #195's fit. In 1/(D − 3) the coefficient of
order k is Ω_k/2^k.

## The order equations at k = 6

#26's equations, unchanged, for k = 0 … 6:

    dY_k/dl = F_{k−1},  F_{k−1} = Σ_{j=0}^{k−1} L_{k−1−j} l^j/j!                     (Y_0 = 1, Y_k(R = 1) = 0)
    (R − 1)L_k′ − L_k/2 = h_k,   h_k = (1 − 1/R)L_{k−1} + Σ_{j=0}^{k−1} Y_j c_{k−j} + Y_k/2,   h_k(1) = Ω_{k−1}
    c_1 … c_5 as in `order5.py`
    c_6 = Ω₀ l⁵/120 + Ω₁ l⁴/24 + Ω₂ l³/6 + Ω₃ l²/2 + Ω₄ l + Ω₅ + l⁶/1440 + l⁵/120 − l⁵/(120R)                         (new)

c_6 is the coefficient of ε⁶ of (1 + εΩ)e^{εl} − (½ + ε)(1 − 1/R)e^{−εl} − e^{−εl}/(2R), the expression whose lower coefficients are c_1 … c_5
(check E0, sympy, residual 0, through k = 6). The solution analytic at the throat is L_k = −2Ω_{k−1} + (R − 1)^{1/2}C_k, C_k = ∫_1^R (h_k −
Ω_{k−1})(R′ − 1)^{−3/2}dR′, and the mode needs G_k = C_k(∞) = 0. G_k is affine in Ω_{k−2} with slope −4π: G_2 = 0 gives Ω₀, … , G_5 = 0 gives
Ω₃, **G_6 = 0 gives Ω₄** (Ω₅ drops out of G_6: it is h_6(1), subtracted). Ω₀ … Ω₄ are solved in turn by one function (`omega_chain`) with no closed
form of Y_k or L_k and no input value of Ω₀ … Ω₃: the planted orders k = 3 … 5 are the same path as the new k = 6.

## Method B at order k

As in I208-dh610's README: variable v = √l (R = e^{v²}), panels of width w on [0, V], N Chebyshev nodes per panel, cumulative integrals by
the spectral integration matrix (`PanelB` of order4.py, shared; `PanelK` of order6.py replaces its two sums by `mp.fdot` and caches l^j/j! and
c_m on the nodes, which changes timing and the last rounding only). For each k: Y_k = ∫₀^l F_{k−1}dl from the left; h_k from the table; the tail
C_right(v) = ∫_v^V (h_k − h_k(1))R(R − 1)^{−3/2}2v dv from the right; L_k = −2h_k(1) − u C_right (u = √(R − 1)); G_k = C_right(0). The truncation at V
costs about e^{−V²/2} times a power of V. Two evaluations of G_k (Ω_{k−2} = 0 and 1) give Ω_{k−2} and the slope.

**Timing, measured** (`dev_01`, `dev_02`, `dev_03`; this machine, one process at nice 10, three running): (40, 1/2, 18, 120) 14 s, (60, 2/5, 24, 200)
62 s, (100, 1/4, 30, 260) 366 s, of which k = 6 takes 100 s; the control grids (84, 1/4, 28, 200), (80, 3/10, 28, 190) 218 s and 166 s. Digits of
Ω₀ … Ω₃ against the closed forms and of Ω₄ between grids: 48 (N = 40), 77 (N = 60), 148 (N = 100): digits ≈ N log₁₀(7.7/w) at every order, k = 6
included. Estimated from that law: G1 ≈ 36 min, G2 ≈ 20 min.

**The grids of record (declared before the runs of record):**

| name | N | w | V | working digits | panels | expected digits (N log₁₀(7.7/w)) | tail e^{−V²/2} V^24 |
|---|---|---|---|---|---|---|---|
| G1 | 170 | 1/4 | 38 | 400 | 152 | 253 | 10⁻²⁷⁵ |
| G2 | 150 | 3/10 | 36 | 360 | 120 | 211 | 10⁻²⁴⁴ |

Also run and reported, not gated: B1 (40, 1/2, 18, 120), B2 (60, 2/5, 24, 200), B3 (100, 1/4, 30, 260). **The control grids** (`--cgrids`, used
only for the controls of the grid-dependent mutations): C1 = (84, 1/4, 28, 200) (expected 125 digits) and C2 = (80, 3/10, 28, 190) (113), named
G1 and G2 in a `--cgrids` run, with the same bars as the grids of record (they are met with 12 to 25 digits to spare). The agreement of G1 and G2 on Ω₄
is an estimator range over grid and precision, **not a rigorous bound**; nothing here is a rigorous enclosure.

**What the evaluations share** (recorded as AGENTS.md asks): the table of c_m and h_k (one sympy expansion, E0, extended to k = 6), the analytic-at-throat
condition, `PanelB` and mpmath. G1 and G2 share the code and differ in N, w, V and precision. #195's fit (the full equation in a Rust crate, no
matching) shares none of the matched machinery and is the independent reference for Ω₄; the closed forms of Ω₀ … Ω₃ (derived in #26, #208, #209)
are the planted truth.

## Criteria (each can fail; written before the runs of record)

"d digits" means a relative difference ≤ 10^−d. The code is `order6.py` at commit e7f8c10 of `wip/i220-omega4`.

| id | statement | bar |
|---|---|---|
| E0 | the table of h_k (k = 0 … 6) and dY_k/dl (k = 1 … 6) equals the ε-expansion of the master equation | sympy residual 0 |
| PL0 … PL3 | planted: Ω₀ … Ω₃ of G1 and G2 against −4 ln 2, 2π²/3 + 8 ln²2, 80ζ(3) − (8/3)π² ln 2 − (32/3) ln³2 and 22π⁴/45 + (16/3)π² ln²2 + (32/3) ln⁴2 − 320ζ(3) ln 2 − 384ζ(3), the same code path that gives Ω₄ | 100 digits each (the issue's bar) |
| PLW | the control `wrong_Om_i` moves Ω_{i+1} of G1 and G2 (evaluated only under those mutations; the control's own statement, not a check of the result) | change > 10⁻³ |
| SL | the evaluated slope of G_k in Ω_{k−2} against −4π, k = 2 … 6, G1 and G2 | 100 digits |
| M4 | Ω₄ of G1 against G2 (two grids, two precisions) | 100 digits (the issue's) |
| X1 | |Ω₄ − (−12794.499860023)| ≤ 5e-10, G1 and G2: #195's fit, which prints 14 digits (`w2_output.txt`; the range over its six cells is 1.5e-30) | half a unit of its last digit |
| X2 | Ω₄ of G1 and G2 against the polynomial extrapolation in 1/s of #195's 64 values of W² (qd, 60 digits, D = 50 … 10⁴) with Ω₀ … Ω₃ fixed at the closed forms: y = (W² − [s + Ω₀ + Ω₁/s + Ω₂/s² + Ω₃/s³])s⁴ = Ω₄ + Ω₅/s + …, the K points of largest s, K = 14, 18, 22, 26, 30, 36, 44 | 1e-25 on every window (an estimator range, not a bound) |
| E1_6, E2_5, E2_4, E3_6, E4_6, G6R | on the hierarchy of the E-grid (36, 1/2, 16, 80 digits, 32 panels; its own Ω₀ … Ω₄), at Ω₄ = its root, 0 and 1/2: E1 at k = 6; E2 at m = 5, 4; E3 at m = 5; E4, the new step that removes Y₄ (below); G6R, G_6 against the reduced form with no Y₄, Y₅, L₄, L₅ | 30 digits (relative to the largest term for E1_6, G6R) |
| Q1 … Q4 | PSLQ tool checks of P1 … P4 (below): the planted relation is recovered exactly and the perturbed basis on the planted target finds nothing | exact recovery; none |
| R5 | the six-term series s − 4 ln 2 + Ω₁/s + … + Ω₄/s⁴ (Ω₁ … Ω₄ of G2) against #195's qd W² at D = 1000, 2000, 5103, 10⁴: x = rem·s⁵ falls with D and |x(10⁴) − x(5103)| ≤ 500 | falling; 500 |
| R6 | two-point extrapolation (s₂x₂ − s₁x₁)/(s₂ − s₁) from D = 5103, 10⁴, which estimates Ω₅ | between 4.0e4 and 4.2e4 |
| RD…, A6 | **to be added by an amendment before their runs**: the reduction of G₆ by hand | |

Reported and not gated: the digits of G1, G2 against B1, B2, B3; Ω₄ to the working digits of every grid; rem·s⁵ at the 64 values of D (it tends
to Ω₅); each PSLQ verdict on the real Ω₄ (a relation not found is a result, not a failed check).

**What E4 is** (a new step, checked here on the hierarchy before it is used by hand). After E1, E2 and E3, Y₄ remains in G₆ through
Y₄·w₄ with w₄ = (2Ω₁ + 8Ω₀ℓ − 22ℓ²)/sin²θ − 12ℓ, ℓ = ln cos θ (from 8ℓc₁/S in H₅, 2c₂/S in S₆ and the 4Ω₀ℓ/S that remains of 4Ω₀∫L₄ = 8Ω₀∫h₄ℓ/S,
since the L₄ terms of G₆ combine to 4Ω₀∫L₄). With Ω₀ = −4 ln 2, W₄ = cot θ (22ℓ² − 8Ω₀ℓ − 2Ω₁) + 16 Cl₂(π − 2θ) satisfies W₄′ = w₄, and
∫Y₄w₄ dθ = −2∫(22ℓ² − 8Ω₀ℓ − 2Ω₁ + 16 tan θ Cl₂(π − 2θ))F₃ dθ, F₃ = L₃ + L₂l + ½L₁l² + ⅙L₀l³ (by parts, dY₄/dθ = 2 tan θ F₃, W₄ tan θ = …; boundary
terms O(θ) at 0 and O(x l⁶) at π/2). So G₆ needs only Y₀ … Y₃ and L₀ … L₃, which are closed forms of #26 and #208.

## PSLQ (declared before the run of record)

`mp.pslq(x, tol, maxcoeff = H, maxsteps = 10⁶)` on [Ω₄, constants…], Ω₄ of G2 rounded to d = min(200, ⌊digits G1 and G2 share⌋) digits (at least
30), constants at d digits. Tolerance τ = 10^−(d − 12). The residual |Σ cᵢxᵢ| is also computed from the integer vector returned. Budget
(n + 1)·log10(2H + 1) + 1, n = the number of constants. A relation counts only if (i) it holds at τ, (ii) its budget with the declared H is below
d, (iii) the basis with the first constant of non-zero coefficient shifted by √2·10⁻³ finds nothing, and (iv) the coefficient of Ω₄ is not zero.
Otherwise "not found" or "found but does not count" is reported with the basis, d, τ and H. A relation that PSLQ alone suggests is a
*conjecture* until the by-hand reduction meets it.

| basis | constants besides Ω₄ | n | H | budget |
|---|---|---|---|---|
| P1 pure weight 5 | π⁴ ln 2, π² ln³2, ln⁵2, π²ζ(3), ζ(3) ln²2, ζ(5) | 6 | 10⁹ | 66.1 |
| P2 weight ≤ 5 | P1 and π⁴, π² ln²2, ln⁴2, ζ(3) ln 2 (weight 4), ζ(3), π² ln 2, ln³2 (3), π², ln²2 (2), ln 2, 1 | 17 | 10⁸ | 150.4 |
| P3 weight ≤ 5 with the polylogarithms at ½ | P2 and Li₄(½), Li₄(½) ln 2, Li₅(½) | 20 | 10⁷ | 154.3 |
| P4 pure weight 5 with them | P1 and Li₄(½) ln 2, Li₅(½) | 8 | 10⁹ | 84.7 |

**Why these.** Ω₀ … Ω₃ lie in the weight ≤ k + 1 span of {ln 2, π², ζ(3)} with products adding (Ω₃ has one weight-3 term). G₆ = 4π(Ω₄ᶜ − Ω₄) is built from the
moments J_n = ∫₀^{π/2} lnⁿ cos θ dθ (n ≤ 6: ζ(5) enters through J₅), Clausen integrals of Cl₂, Cl₃ at π − 2θ and the Li₂, Li₃ of #26's L₃; P2 is the
weight ≤ 5 span of ln 2, π², ζ(3), ζ(5) (the weights up to 5 that the earlier orders show). P3 and P4 add the products with Li₄(½), Li₅(½), which are not
reducible to those four and which the Fourier sums of the Clausen terms (sign (−1)^k) can in principle produce. Odd powers of π, Catalan's constant and β(4) are
not included: Ω₃ had none, and G₆ ∝ π throughout.

**Planted truth** (the tool's size check): the same call on x = (Σ cᵢbᵢ)/den, cᵢ integers of 3 to 4 digits and den ∈ {3, 5, 7, 9, 11, 13, 15, 21, 45} drawn once
with `random.Random(seed)` (seeds 220001 … 220004 for P1 … P4), bᵢ the true constants of the basis: the vector (den, −c₁ … −c_n) must be returned (up to sign), and the basis with
b₂ + √2·10⁻³ must find nothing (√2·10⁻³ is outside the rational span of every basis; a rational shift is not, since P2 contains 1).

## Controls and their declared targets

Every check has a `--mutate=NAME` control. **Targets were computed in the development runs `dev_12` … `dev_15` before this file** (`declared_t1.json`, `declared_t2.json`,
`declared_ex.json`; `ctl_summary.py PREFIX --declared FILE` compares a set of control logs with them). A control is **on target** when the set of checks that fire (FAIL) is exactly the declared set.
Three groups, each with its own nominal run: (T1) grid-dependent mutations on the control grids, all parts with `--no-real`; (T2) post-processing mutations on the nominal run's saved
Ω's (`--load`, parts values, pslq, remainder, `--no-real`; the control grids use H = 10⁵ and 10⁴ for P2 and P3 so that the budgets stay below d ≈ 113); (EX) `exch6`.

| control | what it breaks | fires | declared silent, and silent |
|---|---|---|---|
| T1 `wrong_h` | the sign of −l/R in c₂ | E0, PL0, PL1, PL2, PL3, X1, R5, R6, X2 | SL (the slope is not in c₂'s l/R term), M4 (both grids share it), Q1 … Q4 |
| T1 `wrong_c6` | the sign of l⁵/(120R) in c₆ | E0, X1, X2 | PL0 … PL3, SL, M4, Q1 … Q4, **R5, R6**: Ω₄ moves by 0.0152, below R5's and R6's sensitivity (about 0.03 to 0.05) |
| T1 `wrong_Om0` | Ω₀ + 1/100 in the orders ≥ 3 | PL1, PL2, PL3, X1, R5, R6, X2 | PL0, SL, M4 (both grids take the same wrong input), Q1 … Q4 |
| T1 `wrong_Om1` | Ω₁ + 1/100 in the orders ≥ 4 | PL2, PL3, X1, R5, R6, X2 | PL0, PL1, SL, M4, Q1 … Q4 |
| T1 `wrong_Om2` | Ω₂ + 1/100 in the orders ≥ 5 | PL3, X1, R5, R6, X2 | PL0 … PL2, SL, M4, Q1 … Q4 |
| T1 `wrong_Om3` | Ω₃ + 1/100 in k = 6 | X1, X2 | PL0 … PL3, SL, M4, Q1 … Q4, **R5, R6** (Ω₄ moves by 0.0277) |
| T1 `coarse_B` | N = 10 | PL0 … PL3, SL, M4, Q1 … Q4, R5, R6, X2 | E0, **X1**: the grid's error (1e-11) is below X1's 5e-10; Q1 … Q4 fire because PSLQ is given the 15 digits the grids share |
| T1 `short_tail` | V = 6 | PL0 … PL3, SL, X1, R5, R6, X2 | E0, **M4** (both grids share V), Q1 … Q4 |
| T2 `pslq_wrong_basis` | the first constant of every basis + √2·10⁻³ | Q1 … Q4 | everything else |
| T2 `pslq_wrong_target` | the planted target × (1 + 10⁻²⁰) | Q1 … Q4 | everything else |
| T2 `wrong_Om4_series` | Ω₄ + 1 in the series of R5, R6 | R5, R6 | everything else (at + 1/100 it fires nothing: `dev_14`) |
| T2 `wrong_closed3` | Ω₃'s closed form + 10⁻³ | PL3, X2 | PL0 … PL2, SL, M4, X1, Q1 … Q4, R5, R6 |
| EX `e1_sign` | the sign of E1's second integral | E1_6, G6R | E2_5, E2_4, E3_6, E4_6 |
| EX `e2_weight` | E2's weight ℓ as ℓ + ln 2 | E2_5, E2_4, G6R | E1_6, E3_6, E4_6 |
| EX `e3_factor` | E3's 4 as 2 | E3_6, G6R | E1_6, E2_5, E2_4, E4_6 |
| EX `e4_g` | E4's 22ℓ² as 20ℓ² | E4_6, G6R | E1_6, E2_5, E2_4, E3_6 |
| EX `e4_noC` | E4's 16 u C dropped | E4_6, G6R | E1_6, E2_5, E2_4, E3_6 |
| EX `wrong_h` | c₂'s sign (the hierarchy then has Ω₀ ≠ −4 ln 2) | E4_6, G6R | E1_6, E2_5, E2_4, E3_6 |
| EX `wrong_c6` | c₆'s sign | none | **all six**: E1 … E4 are by-parts identities that hold for any table; E0 sees c₆ |

Silences that are results: R5 and R6 do not see an error in Ω₄ of 0.03 (they bound it to about 0.05); X1 does not see a coarse grid (X1's bar is that of the fit's 14 digits); M4 does
not see a wrong input or a short tail that both grids share; `wrong_c6` is seen by E0 and, on the values, by X1 and X2 only.

## What the runs of record are

On the grids of record, as separate processes (each started with `runrec.sh`, `nice -n 10`, `OMP_NUM_THREADS=1`, `systemd-run --user`):

| run | command (from `notes/wormhole_largeD`) | expected |
|---|---|---|
| `run_01` | `order6.py sym exch6` | 7 checks, minutes |
| `run_02` | `order6.py evals --grids=G1 --save=G1.json` | about 36 min |
| `run_03` | `order6.py evals --grids=G2 --save=G2.json` | about 20 min |
| `run_04` | `order6.py evals --grids=B1,B2,B3 --save=B.json` | about 8 min |
| `run_05` | `order6.py values pslq remainder --load=G1.json,G2.json,B.json --w2raw=inputs_w2_growthD.txt` | PSLQ at d = 200: minutes |

Then the controls of record (`ctl_t1_*`, `ctl_t2_*`, `ctl_ex_*`, the same lists as `dev_12`, `dev_14`/`dev_15` and `dev_13_exch`) against the declared targets. **Stop condition:** any
single run not finished in 2 h of wall time is stopped and reported with what finished. Memory is reported only. The reduction of G₆ by hand, its checks and its amendment follow the runs.

## Amendments

**A1 (2026-11-27, after `run_05`, before `run_06`): the reduction of G₆ by hand, its checks and their controls.** The task asks for the reduction "as far as it goes".
It went all the way, so the checks of the reduction are declared here, before their run `run_06`.

*What had been seen before this amendment* (disclosure; the files are `dev_16` … `dev_23`, `run_02` … `run_05`):
- `run_05` (code e7f8c10): PSLQ found in P2 and in P3 the relation [−45, −88, −320, −384, −7200, 28800, −469440, −2432, 0, 0, 69120, 138240, 0 …] (residual 6.4e-196,
  tolerance 1e-188, d = 200, budget 150.4 and 154.3 below d, the perturbed basis finds nothing): 45Ω₄ = −88π⁴ ln 2 − 320π² ln³2 − 384 ln⁵2 − 7200π²ζ(3) + 28800 ζ(3) ln²2
  − 469440 ζ(5) − 2432π⁴ + 69120 ζ(3) ln 2 + 138240 ζ(3); zero coefficients on π² ln²2, ln⁴2, every constant of weight ≤ 2, Li₄(½), Li₄(½) ln 2 and Li₅(½). P1 and P4 found nothing.
  All 17 checks of `run_01` … `run_05` pass (`run_05` exit 0).
- The reduction below gave the same closed form (`dev_16`, 08:45, **before `run_05` ran**: the PSLQ run is a confirmation of integer coefficients that were already known, not a blind
  search; the bases P1 … P4 were declared before the reduction was coded). `dev_16` read RD0 … RD7 on G2's saved values: 8 of 8.
- The mutation runs `dev_17` … `dev_23`. `dev_21` was stopped when RD8 was found to compare with the wrong sign (the check read the vector of the relation, not the closed form's
  coefficients); `dev_22` is the matrix of the final code (`dev_22_order6_wip.py`, with `rd_kit2` changed afterwards: `dev_23`). Two controls I first wrote were silent where I expected them to fire, and
  each is a result: `rd_kit` (the sign of ln 2 in C's expansion at π/2) fires only RD4, because the finite part of u θ C and of u C Lc2 move together and cancel in the sum (8J₂ = πΩ₁/2);
  my first `rd_kit2` (D₃(π/2) = 3ζ(3)/2) is silent on everything but RD4 because the D₃ coefficient integrates to zero, so D₃(π/2) multiplies zero. `rd_kit2` is now J₂ ×1.01 in Lc2(π/2).

*The code:* `order6.py` at commit 7acb933 (= the code of `run_01` … `run_05`, e7f8c10, and the part `reduce6`, checks RD0 … RD8, mutations `rd_*`). *The run:* `run_06_reduce6`:
`order6.py reduce6 --load=G1.json,G2.json,B.json` (sympy, mpmath 40 digits, about 3 min).

| id | statement | bar |
|---|---|---|
| RD0 | the derivative rules ℓ′ = −u, u′ = 1 + u², C′ = 2ℓ + 2 ln 2, D₃′ = 2C, Lc2′ = ℓ² against numerical derivatives at θ = 0.7 | 1e-30 |
| RD1 | the decomposition of the integrand of G₆ (after E1 … E4, from the closed forms of Y₀ … Y₃, L₀ … L₃ as generators; sympy) into coefficients of C^a D₃^b Lc2^c against the numeric integrand of closed forms (the `order4.py` closed forms and `order5.py`'s L₃) at θ = 0.2, 0.7, 1.1, 1.4 | 30 digits |
| RD2 | the by-parts identities of the reduction, 12 of them, as sympy residuals: M1, M2, M3 (their coefficients and derivatives), the primitive A of the D₃ coefficient, the u θ C and u θ (ℓ + q) identities, the Lc2 step, the u θ ℓ^b step | residual 0 |
| RD3 | the slope of G₆ in Ω₄ is −4π; the 1/u terms of the C coefficient cancel after the D₃ step; J₆ (and so ζ(3)²) drops out | exactly |
| RD4 | the asymptotic series (order 9) of ℓ, u, 1/u, C, D₃, Lc2 at θ → π/2 and θ → 0 (the finite-part kit) against the functions at x = π/2 − θ = 10⁻³ and θ = 10⁻³ | 1e-24 relative |
| RD5 | the master integrals against their closed forms, quadrature at 40 digits: ∫C², ∫ℓC², ∫θC, ∫ℓ²D₃, ∫C Lc2, ∫u ℓ^b C (b ≤ 3), J_n (n ≤ 6) | 30 digits |
| RD6 | method A at order 6: G₆ by quadrature (40 digits) of the numeric integrand of closed forms, Ω₄ from the affine G₆ at Ω₄ = 0, 1, against the derived closed form; and its slope against −4π | 30 digits |
| RD7 | the derived closed form against Ω₄ of G1 and G2 (B1 … B3 reported) | 100 digits |
| RD8 | the integer relation of `run_05` equals −45 followed by 45 × the derived closed form's coefficients on P2's constants, and every term of the closed form is a constant of P2 | equal |

The closed form is derived by `reduce6` from the integrand, not typed in; RD8 compares it with the vector PSLQ returned.

*Declared targets of the controls* (`declared_red.json`; read from `dev_22` and `dev_23`; a control is on target when the set of checks that fire is exactly the declared set):

| control | what it breaks | fires | silent, and why |
|---|---|---|---|
| `rd_w4` | E4's 22ℓ² as 20ℓ² in the symbolic integrand | RD1, RD6, RD7, RD8 | RD0, RD2 … RD5 (the numeric integrand has its own 22) |
| `rd_M1` | M1's constant 4096 as 4095 | RD2, RD6, RD7, RD8 | RD1, RD3 … RD5 |
| `rd_M3` | M3's boundary term sign | RD6, RD7, RD8 | RD2: the identity is a sympy residual, the boundary term is not |
| `rd_master` | ∫ℓ²D₃'s 5ζ(5) as 4ζ(5) | RD5, RD6, RD7, RD8 | RD1 … RD4 |
| `rd_J5` | J₅'s ζ(5) coefficient 1080 as 1000 | RD5, RD6, RD7, RD8 | RD1 … RD4 |
| `rd_Dstep` | the sign of the P_{b−1} part of F_b in the primitive A | RD2, RD6, RD7, RD8 | RD1, RD3 … RD5 |
| `rd_kit` | the sign of ln 2 in C(x) at π/2 | RD4 | RD6 … RD8: the closed form does not depend on it (finite parts cancel in the sum) |
| `rd_kit2` | Lc2(π/2) = 1.01 J₂ | RD4, RD6, RD7, RD8 | RD1 … RD3, RD5 |

The controls of record are `ctl_red_*` (these eight and the nominal run `ctl_red_nominal`), run with the final code, on `G2.json`.
