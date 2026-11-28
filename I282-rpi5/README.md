# I282-rpi5: Ω₆ from the order-8 matching integral of Paper III's large-D expansion, and the ln 2 factor of F at ε⁷

Machine: rpi5-ubuntu (Ubuntu, 4 cores, 8 GB, aarch64; Python 3.14.10 venv `negative-mass-venv314`, mpmath 1.3.0 with the pure-Python backend, sympy 1.14.0), shared with other projects
(at most 3 processes of mine, `nice -n 10`, `OMP_NUM_THREADS=1`; runs longer than a few minutes are systemd user units `nm-i282-*`). Runner `negative-mass-rpi5-i282` (Claude Code, Sonnet 5.5,
account claude-me2), started by the coordinator over hc. Issue: https://github.com/nmoinvaz/negative-mass/issues/282 (milestone G5).
Code: worktree `~/Source/negative-mass-i282`, branch `wip/i282-omega6` from ee43442 (`main`); script `notes/wormhole_largeD/order8.py` (it imports `PanelB` from the unchanged `order4.py`),
output `order8_output.txt`, note `omega6.md`. Pushes: `git push origin HEAD:refs/heads/wip/i282-omega6`.
Development runs `dev_NN_*` and runs of record `run_NN_*` keep stdout (`.log`), stderr (`.err`) and the exit code (`.rc`) beside this file (`devrun.sh`; `runrec.sh` also keeps `/usr/bin/time -v`
and the machine's load); nothing is overwritten, reruns are numbered. `dev_01_order8_wip.py` is the code of `dev_01`. Status words as in AGENTS.md: agreement of an integral or a series with a
constant is *numerical evidence*; a PSLQ relation is an *identification* (a *conjecture* until a by-hand reduction meets it); a step checked by sympy is *checked symbolically*; a closed form
reached by hand with each step checked is *derived*. **No by-hand reduction of G₈ is attempted** (the issue does not require it), so nothing here is *derived* at order 8: Ω₆'s value is *computed*
and its closed form, if PSLQ finds one, is *identified*. No sentence here claims novelty.

## What was run before this file (disclosure)

| runs | what |
|---|---|
| `dev_01` | `order8.py sym struct cache`: E0 through k = 8 (sympy, residual 0), LN2 (F's f₂ … f₆ free of ln 2 from the closed forms of Ω₀ … Ω₅, residual 0), CACHE (cached chain = uncached chain, 60 digits equal, bit for bit) |
| `dev_02`, `dev_03`, `dev_05`, `dev_06` | `order8.py grid` on (60, 2/5, 24, 120), (100, 1/4, 30, 200), (100, 1/4, 30, 165), (100, 1/4, 30, 150): digits of Ω₀ … Ω₅ against the closed forms, the working precision needed |
| `dev_04` | the same on (170, 1/4, 38, 285): timing |
| `dev_07` | `order8.py remainder` on the 148-digit Ω₆ of `dev_03` (to set the bars of R7, R8, X4) |
| `dev_08` | `order8.py pslq --no-real --pslq-cap=200` on `dev_03`'s Ω₆: the tool checks (planted relation, perturbed basis) of the bases below; **no PSLQ of the real f₇** |

**Seen before this file:**
- **Ω₆ ≈ 3672259.1625943904896578593696206265702762366840…** (`dev_03`, N = 100, which agrees with the N = 60 grid of `dev_02` to 78.1 digits; the digits of N = 100 are 148). It is in the issue's range 3.5e6 … 3.9e6 (#195's W² gave about 3.7e6).
- **Digits.** The law digits ≈ N log₁₀(7.7/w) holds at order 8: Ω₀ … Ω₅ come out at 77.0 … 77.8 (N = 60), 148.1 … 148.8 (N = 100), 250.0 … 251.0 (N = 170) digits. Rounding loss: at N = 100, 165 working digits give Ω₅, Ω₆ equal to the 200-digit run to 162.4 and 158.9 digits
  (the discretization is 148), and 150 working digits give 145.6 and 144.8. The working digits of the grids below are the expected digits plus about 18.
- **Timing** (`dev_04`, one process while two others ran): (170, 1/4, 38, 285) 1055 s in all (panel setup 74 s), 127 … 141 s for k = 2 … 7 and 181 s for k = 8. The cached chain has 56 integration units for k = 2 … 8 (48 for k = 2 … 7 at order 7).
- **The remainder on that Ω₆** (`dev_07`): two-point rem₇·s⁶ from D = 5103, 10⁴ gives 3672264.5 (relative 1.47e-6 from the computed Ω₆); |rem₈·s⁷(10⁴) − rem₈·s⁷(5103)| = 52722 (rem₈·s⁷ → Ω₇ ≈ 2.55e7, an estimate);
  the refit of #195's 64 values of W² with Ω₀ … Ω₅ fixed gives Ω₆ to 1.1e-23 (K = 14), 8.0e-23, 3.1e-22, 7.9e-22, 1.5e-21, 2.8e-21, 4.4e-21 (K = 44). **The bars of R7, R8 and X4 below are set knowing these numbers.**
- F's coefficients from the closed forms (`dev_01`): f₂ = 2π²/3, f₃ = 80ζ(3), f₄ = 22π⁴/45 − 384ζ(3), f₅ = −2432π⁴/45 − 160π²ζ(3) + 3072ζ(3) − 10432ζ(5), f₆ = −38812π⁶/315 + 39424π⁴/45 − 256π²ζ(3)/3 + 3200ζ(3)² − 36864ζ(3) + 74240ζ(5).
  Their weights are 2; 3; 4, 3; 5, 4, 3; 6, 5, 4, 3: nothing of weight 2, 1, 0 beyond f₂, and no ζ(7) yet. The integer vector of f₆ has entries up to 2.3e7 after clearing the denominator 315.

**Not seen:** any PSLQ of the real f₇ (the bases below were declared first); Ω₆ on the grids of record; the controls' behavior on any target but the ones in `dev_01`.

## Convention

As in README.md, matched.py, order3.py … order7.py and #195: s = 2(D − 3), ε = 1/s, W²a² = s + Ω, Ω = Ω₀ + Ω₁ε + Ω₂ε² + … , R = r^s, l = ln R = −2 ln cos θ.
Ω₀ = −4 ln 2, Ω₁ = 2π²/3 + 8 ln²2, Ω₂ = 80ζ(3) − (8/3)π² ln 2 − (32/3) ln³2, Ω₃ = 22π⁴/45 + (16/3)π² ln²2 + (32/3) ln⁴2 − 320ζ(3) ln 2 − 384ζ(3), Ω₄ (#220),
Ω₅ = (256/45)ln⁶2 + (64/9)π²ln⁴2 − (2560/3)ζ(3)ln³2 + (176/45)π⁴ln²2 − 3072ζ(3)ln²2 + 640π²ζ(3)ln 2 + (9728/45)π⁴ln 2 − 12288ζ(3)ln 2 + 41728ζ(5)ln 2 − (38812/315)π⁶ + 3200ζ(3)² − (256/3)π²ζ(3) + 74240ζ(5) + (39424/45)π⁴ − 36864ζ(3) (#263; derived there, with E2W and E5 under review in #264).
These six are the planted truth. In 1/(D − 3) the coefficient of order k is Ω_k/2^k.

**F.** F(ε) = e^{4 ln 2 ε}(1 + Ω₀ε + Ω₁ε² + …) = 1 + f₂ε² + f₃ε³ + …; f₇ = Ω₆ + Σ_{j=0}^{5}Ω_j(4 ln 2)^{6−j}/(6−j)! + (4 ln 2)^7/7!, with Ω₀ … Ω₅ exact (their closed forms). W²a² = s 2^{−4/s}F(1/s).
The question of the issue: is f₇ free of ln 2, i.e. a rational combination of ln 2-free monomials of π², ζ(3), ζ(5), ζ(7)?

## The order equations at k = 8

#26's equations, unchanged, for k = 0 … 8:

    dY_k/dl = F_{k−1},  F_{k−1} = Σ_{j=0}^{k−1} L_{k−1−j} l^j/j!                     (Y_0 = 1, Y_k(R = 1) = 0)
    (R − 1)L_k′ − L_k/2 = h_k,   h_k = (1 − 1/R)L_{k−1} + Σ_{j=0}^{k−1} Y_j c_{k−j} + Y_k/2,   h_k(1) = Ω_{k−1}
    c_1 … c_7 as in `order7.py`
    c_8 = Ω₀ l⁷/5040 + Ω₁ l⁶/720 + Ω₂ l⁵/120 + Ω₃ l⁴/24 + Ω₄ l³/6 + Ω₅ l²/2 + Ω₆ l + Ω₇ + l⁸/80640 + l⁷/5040 − l⁷/(5040R)                      (new)

c_8 is the coefficient of ε⁸ of (1 + εΩ)e^{εl} − (½ + ε)(1 − 1/R)e^{−εl} − e^{−εl}/(2R) (check E0, sympy, residual 0, through k = 8, `dev_01`). G_k = C_k(∞) is affine in Ω_{k−2} with slope −4π: G_2 = 0 gives Ω₀, … , G_7 = 0 gives Ω₅, **G_8 = 0 gives Ω₆**
(Ω₇ drops out of G_8: it is h_8(1), subtracted). Ω₀ … Ω₆ are solved in turn by one function (`omega_chain`) with no closed form of Y_k or L_k and no input value of Ω₀ … Ω₅.

## Method B at order 8, and the cached chain

As in I263-rpi5's README: variable v = √l (R = e^{v²}), panels of width w on [0, V], N Chebyshev nodes per panel, cumulative integrals by the spectral integration matrix (`PanelB` of order4.py, shared; `PanelK` replaces its sums by `mp.fdot` and caches l^j/j! and c_m).
Y_j, L_j (j ≤ k − 2) do not depend on Ω_{k−2}, so step k keeps the levels 0 … k − 2 of the earlier steps: 8 integration units per step, 56 for k = 2 … 8 (the uncached chain has 2(2k + 1) per step, 154). The operations and their order are those of the uncached chain;
**CACHE** compares the two chains on a small grid. For the mutations that change an input of the lower levels (`wrong_Om0` … `wrong_Om5`) the chain is recomputed from level 0 (it must reach every level).

## Grids of record (declared before the runs of record)

| name | N | w | V | working digits | panels | expected digits (N log₁₀(7.7/w)) | tail e^{−V²/2}V³² | expected wall |
|---|---|---|---|---|---|---|---|---|
| G1 | 300 | 1/4 | 50 | 465 | 200 | 446.6 | 10⁻⁴⁸⁸·⁵ | 2.5 h (panel setup about 15 min of it) |
| G2 | 310 | 3/10 | 49 | 455 | 164 | 436.9 | 10⁻⁴⁶⁷·³ | 2.3 h |

The grids are larger than #263's (N = 285 and 275) so that PSLQ can run at d = 390 digits (the budget of the full basis XF is 382). Also run and reported, not gated: B1 (60, 2/5, 26, 100), B2 (100, 1/4, 32, 170), B3 (170, 1/4, 40, 285) (expected digits 77.1, 148.9, 253.1).
**The control grids** (`--cgrids`, used only for the controls of the grid-dependent mutations): C1 = (90, 1/4, 32, 160) (expected 134 digits), C2 = (85, 3/10, 31, 150) (120), named G1 and G2 in a `--cgrids` run, with the same bars (100 digits) as the grids of record.
The agreement of G1 and G2 on Ω₆ is an estimator range over grid and precision, **not a rigorous bound**; nothing here is a rigorous enclosure.
**What the evaluations share:** the table of c_m and h_k (one sympy expansion, E0, extended to k = 8), the analytic-at-throat condition, `PanelB` and mpmath. G1 and G2 share the code and differ in N, w, V and precision.
#195's 64 values of W² (the full equation in a Rust crate, no matching) share none of the matched machinery and are the independent reference for Ω₆ (X4); the closed forms of Ω₀ … Ω₅ are the planted truth.

## Criteria (each can fail; written before the runs of record)

"d digits" means a relative difference ≤ 10^−d. The code is `order8.py` at commit 0ac9b7e of `wip/i282-omega6` (the code of the runs of record, unless a later commit is named in "Results of record").

| id | statement | bar |
|---|---|---|
| E0 | the table of h_k (k = 0 … 8) and dY_k/dl (k = 1 … 8) equals the ε-expansion of the master equation | sympy residual 0 |
| CACHE | the cached chain equals the uncached chain on (24, 1/2, 12, 60 digits): Ω₀ … Ω₆ | relative difference ≤ 10^−55 |
| LN2 | F = e^{4 ln 2 ε}(1 + Ω₀ε + … + Ω₅ε⁶) from the closed forms of Ω₀ … Ω₅: f₀ = 1, f₁ = 0 and d f_n/d ln 2 = 0 for n = 2 … 6 | sympy residual 0 |
| PL0 … PL5 | planted: Ω₀ … Ω₅ of G1 and G2 against their closed forms, the same code path that gives Ω₆ | 100 digits each (the issue's bar) |
| PLW | the control `wrong_Om_i` moves Ω_{i+1} of G1 and G2 (evaluated only under those mutations; the control's own statement) | change > 10⁻³ |
| SL | the evaluated slope of G_k in Ω_{k−2} against −4π, k = 2 … 8, G1 and G2 | 100 digits |
| RES | max over k = 2 … 8 of \|G_k at the chain's root\|/\|slope\| | 10⁻¹⁰⁰ |
| M6 | Ω₆ of G1 against G2 (two grids, two precisions) | 100 digits (the issue's) |
| RNG | Ω₆ of G1 and G2 between 3.5e6 and 3.9e6 | the issue's range |
| X4 | Ω₆ of G1 and G2 against the polynomial extrapolation in 1/s of #195's 64 values of W² (qd, 60 digits, D = 50 … 10⁴) with Ω₀ … Ω₅ fixed at the closed forms: y = (W² − [s + Ω₀ + … + Ω₅/s⁵])s⁶ = Ω₆ + Ω₇/s + …, the K points of largest s, K = 14, 18, 22, 26, 30, 36, 44 | 1e-18 on every window (an estimator range, not a bound; set knowing 1.1e-23 … 4.4e-21 on a 148-digit Ω₆) |
| R7 | two-point extrapolation (s₂x₂ − s₁x₁)/(s₂ − s₁) of rem₇·s⁶ from D = 5103, 10⁴ against the computed Ω₆ | relative 5e-5 (an estimate; set knowing 1.47e-6) |
| R8 | the series through Ω₆ (of G2) against #195's W²: \|rem₈·s⁷(D = 10⁴) − rem₈·s⁷(D = 5103)\| (a wrong Ω₆ adds (error)·s, 2e4 per unit) | 1e5 (set knowing 52722) |
| PF1 … PF6, PX1 … PX3, PXF | PSLQ tool checks of the ten bases below: the planted relation is recovered exactly and the perturbed basis on the planted target finds nothing | exact recovery; none |
| ID6 | Ω₆ from the relation PSLQ found in F6 (f₇ = −Σcᵢbᵢ/c₀, Ω₆ = f₇ − the exact ln 2 terms), evaluated at 400 digits, against G1 and G2 | 380 digits |
| ZL | F6 found a relation, and every relation found in a basis with ln 2 (X1, X2, X3, XF) has zero coefficients on every ln 2 monomial | exact |

**ID6 and ZL are the structure's verdict and can fail**: if no relation of f₇ is found in the ln 2-free basis F6 they fail, and that is a result (*not found* in that basis), not a defect to repair.
Reported and not gated: the digits of G1, G2 against B1 … B3; Ω₆ to the working digits of every grid; rem₇·s⁶ and rem₈·s⁷ at the D of #195's list; each PSLQ verdict on the real f₇ (a relation not found is a result, not a failed check);
Ω₆ by weight when a relation is found.

## PSLQ (declared before the run of record)

`mp.pslq(x, tol, maxcoeff = H, maxsteps = 10⁶)` on [f₇, constants…], f₇ computed from Ω₆ of G2 and the exact Ω₀ … Ω₅, rounded to d = min(390, ⌊digits G1 and G2 share⌋ − 32) digits, constants at d digits. Tolerance τ = 10^−(d − 12).
Budget (n + 1)·log₁₀(2H + 1) + 1, n = the number of constants. A relation counts only if (i) it holds at τ, (ii) its budget with the declared H is below d, (iii) the basis with the first constant of non-zero coefficient shifted by √2·10⁻³ finds nothing,
(iv) the coefficient of f₇ is not zero, and (v) it holds at d + 20 digits (tolerance 10^−(d + 8)) on both G1 and G2. Otherwise "not found" or "found but does not count" is reported with the basis, d, τ and H.
**The bases (declared before any PSLQ of the real f₇).** The ln 2-free monomials of weight ≤ 7 (π²: 2, ζ(3): 3, ζ(5): 5, ζ(7): 7, products add): π⁴ζ(3), π²ζ(5), ζ(7) (weight 7), π⁶, ζ(3)² (6), π²ζ(3), ζ(5) (5), π⁴ (4), ζ(3) (3), π² (2), 1 (0): 11 constants.
They span the non-alternating Euler sums of weight ≤ 7 (Zagier's dimensions 1, 0, 1, 1, 1, 2, 2, 3; independence is conjectural). The bases with ln 2 are ln^j 2 times the ln 2-free monomials of weight ≤ 7 − j.

| basis | constants besides f₇ | n | H | budget |
|---|---|---|---|---|
| F1 | the 3 monomials of weight 7 | 3 | 10¹⁶ | 66.2 |
| F2 | F1 and the 2 of weight 6 | 5 | 10¹⁶ | 98.8 |
| F3 | F2 and the 2 of weight 5 | 7 | 10¹⁶ | 131.4 |
| F4 | F3 and π⁴ | 8 | 10¹⁶ | 147.7 |
| F5 | F4 and ζ(3) | 9 | 10¹⁶ | 164.0 |
| **F6** (the ln 2-free basis, weight ≤ 7) | F5 and π², 1 | 11 | 10¹⁶ | 196.6 |
| X1 (ln 2 once) | F6 and ln 2 × the 8 ln 2-free monomials of weight ≤ 6 | 19 | 10¹⁴ | 287.0 |
| X2 | X1 and ln²2 × the 6 of weight ≤ 5 | 25 | 10¹³ | 346.8 |
| X3 | X2 and ln³2 × the 4 of weight ≤ 4 | 29 | 10¹² | 370.0 |
| **XF** (the full basis with ln 2, weight ≤ 7) | X3 and ln⁴2 × 3, ln⁵2 × 2, ln⁶2, ln⁷2 | 36 | 10¹⁰ | 382.1 |

**Planted truth** (the tool's size check): the same call on x = (Σ cᵢbᵢ)/den, cᵢ integers of 3 to 4 digits and den ∈ {3, 5, 7, 9, 11, 13, 15, 21, 45} drawn once with `random.Random(seed)` (seeds 282001 … 282010 for F1 … F6, X1, X2, X3, XF, in that order),
bᵢ the true constants of the basis: the vector (den, −c₁ … −c_n) must be returned (up to sign), and the basis with b₂ + √2·10⁻³ must find nothing.
**What a result means.** If F6 finds a relation that counts, **F is free of ln 2 at ε⁷ and the relation is an *identification*** (PSLQ, at d digits, a *conjecture* until a by-hand reduction meets it; none is attempted); Ω₆ then follows by exact algebra (ID6).
If F6 finds nothing, the ln 2-free question has the answer *not found in F6* (at H = 10¹⁶, d = 390); X1 … XF then say whether a relation with ln 2 exists in their span, and a relation found there with a nonzero coefficient on a ln 2 monomial is the answer *F has ln 2 at ε⁷*.
**XF can only find a relation of height up to about 10^(d/(n + 1))**: if the integer vector of F6's relation is larger than XF's H, XF's "not found" is for that H only and is reported with the height. A "not found" is for these bases only: odd powers of π, Catalan's constant, Li₄(½) and its products, and the weight-6 and 7 alternating sums beyond them are in no basis.

## Controls and what they break (targets are declared in amendment A1, after their development runs and before the controls of record)

Every check has a `--mutate=NAME` control. A control is **on target** when the set of checks that fire (FAIL) is exactly the declared set. Groups, each with its own nominal run:
(CHK) `sym struct cache`: `wrong_h`, `wrong_c6`, `wrong_c7`, `wrong_c8` (E0), `stale_cache` (CACHE), `ln2_struct` (LN2: a stray ln 2 ζ(3) in Ω₃);
(T1) grid-dependent mutations on the control grids: `wrong_h`, `wrong_c6`, `wrong_c7`, `wrong_c8`, `wrong_Om0` … `wrong_Om5`, `coarse_B`, `short_tail`, `stale_cache` (parts `evals values remainder`, and `pslq --bases=F1,F3 --no-real`, with H lowered to 10^max(4, ⌊(d − 25)/(n + 1)⌋ − 1) because d is about 90 there);
(T2) post-processing mutations on the saved Ω's of record: `pslq_wrong_basis`, `pslq_wrong_target` (parts `values pslq` with `--no-real --bases=F1,F3,F5 --pslq-cap=150`), `wrong_Om6_series` (Ω₆ + 1000 in R7, R8), `wrong_closed5` (Ω₅'s closed form + 10⁻³: PL5, X4);
(T2b) the same two PSLQ mutations on F2, F4, F6, X1, X2, X3, XF (`--pslq-cap=250`);
(ST) the structure verdict: `pslq --bases=F6 --pslq-cap=250 --save-rel=…` then `closed6 --rel=…` on the saved Ω's: `ln2_leak` (f₇ + 1000 ln 2 ζ(3)²: F6 finds nothing, ID6 and ZL fire), `f7_rel` (a coefficient of the relation off by one: ID6), `ln2_zl` (a nonzero ln 2 coefficient put in: ZL).

## Runs of record

On the grids of record, as separate processes (each started with `runrec.sh`, `nice -n 10`, `OMP_NUM_THREADS=1`, `systemd-run --user`):

| run | command (from `notes/wormhole_largeD`) | expected |
|---|---|---|
| `run_01` | `order8.py sym struct cache` | 3 checks, 15 s |
| `run_02` | `order8.py evals --grids=G1 --save=G1.json` | about 2.5 h |
| `run_03` | `order8.py evals --grids=G2 --save=G2.json` | about 2.3 h |
| `run_04` | `order8.py evals --grids=B1,B2,B3 --save=B.json` | about 25 min |
| `run_05` | `order8.py values remainder --load=G1.json,G2.json,B.json --w2raw=inputs_w2_growthD.txt` | PL0 … PL5, SL, RES, M6, RNG, R7, R8, X4 |
| `run_06a` | `order8.py pslq --bases=F1,F2,F3,F4,F5,F6,X1 --save-rel=rel_a.json --load=…` | PSLQ at d = 390 |
| `run_06b` | `order8.py pslq --bases=X2,X3 --save-rel=rel_b.json --load=…` | |
| `run_06c` | `order8.py pslq --bases=XF --save-rel=rel_c.json --load=…` | |
| `run_07` | `order8.py closed6 --rel=rel_a.json,rel_b.json,rel_c.json --load=…` | ID6, ZL, Ω₆ by weight |

**Stop condition:** any single run not finished in 4 h of wall time is stopped and reported with what finished. Memory is reported only. If G1 or G2 stops, the other grid and B1 … B3 are reported and PSLQ runs at the digits they share.

## Amendments

**A1 (2026-11-27, 22:55, after `run_01` … `run_05` and `run_06a`, before the controls of record and `run_06b`, `run_06c`): what was seen, and the targets of CHK, T1 and T2.**

*What had been seen before this amendment* (disclosure; the logs are in this folder):
- `run_01` (3 of 3: CACHE, E0, LN2), `run_02` (G1, 2 h 14 m 06 s, panel setup 598 s, peak 1.21 GB), `run_03` (G2, 1 h 55 m 27 s, panel setup 644 s, peak 1.04 GB), `run_04` (B1, B2, B3, 22 m 59 s, peak 0.49 GB; it ran beside G1's last k-step) and `run_05` (13 of 13 pass).
  **Ω₆ = 3672259.16259439048965785936962062657027623668409099035239492678148238…** (G1; G2 agrees to 430.8 digits, |difference| 6.39e-425). PL0 … PL5: G1 439.6 … 440.2 digits, G2 429.7 … 430.8 (bar 100); X4 is the same 1.1e-23 … 4.4e-21 as the development run.
- `run_06a` (PF1 … PF6, PX1: 7 of 7 pass; the real PSLQ): **F1, F2, F3, F4 find nothing; F5, F6 and X1 find one relation**, with zeros on π², 1 and on every ln 2 monomial of X1
  (the integer vector of F5 has height 2.76e9; budget 164.0 for F5, 196.6 for F6, 247.0 for X1, all below d = 390; it holds at 410 digits on G1 and G2 to 4.0e-401, bar 1e-398; the perturbed bases find nothing). The vector is in `run_06a_pslq_F1_F6_X1.log`.
- **Done outside the declared list, in this order:** `dev_08` was stopped by me after 13 minutes inside PXF at cap 200 (`dev_08_pslq_planted.stopped`; PF1 … PX3 had passed); `dev_13_planted_f7` is the end-to-end test of `pslq` and `closed6` on a planted f₇
  (`dev_planted_f7.json`: an invented ln 2-free combination of the 11 monomials, its Ω₆ built from it and the exact Ω₀ … Ω₅ at 450 digits): F6 returns the planted integer vector exactly, ID6 and ZL pass; `dev_15_values_G1G2` ran `values remainder` on G1, G2 before `run_05`
  (the same numbers); `dev_16_closed6_rel_a` ran `closed6` on `rel_a.json` (ID6 and ZL pass, the closed form of Ω₆; `run_07` repeats it with all relation files).
- **Deviation 1: `run_06a` … `run_06c` load `G1.json,G2.json` only** (the table above has `--load=…`); B.json is not needed by PSLQ and did not exist yet when `run_06a` started.
- **Deviation 2:** the controls ran in a frozen copy of the code (`frozen_0ac9b7e` in the session scratchpad, a byte-for-byte copy of `order8.py`, `order4.py` and `w2_output.txt` at 0ac9b7e) during development, so that edits could not reach a queued job; the controls of record run from the checkout.

*Targets of the CHK controls* (`declared_chk.json`; read from `dev_09_chk_*`; part `sym struct cache`): a control is on target when exactly these checks fire.

| control | fires |
|---|---|
| `nominal` | nothing |
| `wrong_h` | E0 |
| `wrong_c6` | E0 |
| `wrong_c7` | E0 |
| `wrong_c8` | E0 |
| `stale_cache` | CACHE |
| `ln2_struct` | LN2 |

*Targets of the T1 controls* (`declared_t1.json`; read from `dev_10_t1_*` on the control grids C1, C2 (`--cgrids`), parts `evals values remainder pslq --bases=F1,F3 --no-real`; PLW is silent in every `wrong_Om` control, i.e. the wrong input moved Ω_{i+1}):

| control | fires |
|---|---|
| `cnom` | nothing |
| `wrong_h` | PL0, PL1, PL2, PL3, PL4, PL5, RNG, R7, R8, X4 |
| `wrong_c6` | PL4, PL5, R7, R8, X4 |
| `wrong_c7` | PL5, R7, R8, X4 |
| `wrong_c8` | X4 |
| `wrong_Om0` | PL1, PL2, PL3, PL4, PL5, R7, R8, X4 |
| `wrong_Om1` | PL2, PL3, PL4, PL5, R7, R8, X4 |
| `wrong_Om2` | PL3, PL4, PL5, R7, R8, X4 |
| `wrong_Om3` | PL4, PL5, R7, R8, X4 |
| `wrong_Om4` | PL5, R7, R8, X4 |
| `wrong_Om5` | X4 |
| `coarse_B` | PL0, PL1, PL2, PL3, PL4, PL5, SL, M6, PF3, R7, R8, X4 |
| `short_tail` | PL0, PL1, PL2, PL3, PL4, PL5, SL, R7, R8, X4 |
| `stale_cache` | PL2, PL3, PL4, PL5, RES, R7, R8, X4 |

Declared silences that are results: `wrong_c8` fires only X4 (the change in Ω₆ is below R7's and R8's sensitivity); `wrong_Om5` fires only X4 for the same reason (+0.01 in Ω₅ moves Ω₆ by less than R7, R8 can see); `wrong_c7`, `wrong_Om4` do not fire PL4 (Ω₄ does not depend on them);
M6 stays silent in every control but `coarse_B` (both grids share the error); RES fires only in `stale_cache`.

*Targets of the T2 controls* (`declared_t2.json`; read from `dev_11_t2_*` on `dev_N170_285.json`, a wrapper of `dev_04`'s printed values, parts `values pslq remainder --no-real --bases=F1,F3,F5 --pslq-cap=150`; the controls of record use `G1.json`, `G2.json` at the same cap):

| control | fires |
|---|---|
| `nominal` | nothing |
| `pslq_wrong_basis` | PF1, PF3, PF5 |
| `pslq_wrong_target` | PF1, PF3, PF5 |
| `wrong_Om6_series` | R7, R8 |
| `wrong_closed5` | PL5, X4 |

*Not yet read (their targets come in A2, before their controls of record):* T2b (`dev_12_t2b_*`, `dev_12_t2bxf_*`), the structure group ST (`dev_14_st_*` on `dev_planted_f7.json`).
