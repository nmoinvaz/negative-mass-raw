# I315-mac: Ω₇ from the order-9 matching integral of Paper III's large-D expansion, and the ln 2 factor of F at ε⁸

Machine: the coordinator's Mac (Apple M5, 10 cores, 32 GB, macOS; Python 3.14.7 in `~/Source/negative-mass/.venv`, mpmath 1.3.0 with the pure-Python backend, sympy 1.14.0), shared with other agents and loaded
(at most 2 processes of mine, `nice -n 10`, `OMP_NUM_THREADS=1`; runs longer than a few minutes are started with `nohup` and `devrun.sh` / `runrec.sh`). Runner `negative-mass-mac-i315` (Claude Code, Sonnet 5.5, account claude-me2),
started by the coordinator over hc. Issue: https://github.com/nmoinvaz/negative-mass/issues/315.
Code: worktree `~/Source/negative-mass-i315`, branch `wip/i315-omega7` from 7fde1e0 (`main`); script `notes/wormhole_largeD/order9.py` (it **imports** `order8.py`, which imports `PanelB` from the unchanged `order4.py`; `order9.py` replaces
`order8.cc` by a table that adds c₉, and `order8.closed_omegas` by the closed forms of Ω₀ … Ω₆), output `order9_output.txt`, note `omega7.md`. Pushes: `git push origin HEAD:refs/heads/wip/i315-omega7`.
Development runs `dev_NN_*` and runs of record `run_NN_*` keep stdout (`.log`), stderr (`.err`) and the exit code (`.rc`) beside this file (`devrun.sh`; `runrec.sh` also keeps `/usr/bin/time -l` and the machine's load); nothing is overwritten,
reruns are numbered, runs I stopped are renamed `*.stopped.*`. Status words as in AGENTS.md: agreement of an integral or a series with a constant is *numerical evidence*; a PSLQ relation is an *identification* (a *conjecture* until a by-hand reduction
meets it); a step checked by sympy is *checked symbolically*; a closed form reached by hand with each step checked is *derived*; Ω₇ is *computed*. **No by-hand reduction of G₉ is attempted** (#316 is the by-hand reduction of G₈, not mine), so nothing here is *derived* at order 9.
No sentence here claims novelty.

## What was run before this file (disclosure)

| runs | what |
|---|---|
| terminal runs, **not logged** (my mistake: they ran before `devrun.sh` was in use) | `order9.py grid --grid=30,1/2,12,60` (the chain runs to k = 9: Ω₇ = 25545344.605…); `order9.py sym struct cache` (E0 through k = 9, CACHE, LN2, TR6, LN2b all pass); `order9.py zv` at 60 and 560 digits: at 60 digits ZV4 failed because H = 1e12 does not fit 50 digits (a mis-sized test, not a result); at 560 digits ZV1, ZV2, ZV2b, ZV4 failed at 1e-436: **mpmath's `zeta(s, a)` is good to about 290 digits at a = 2001** (checked against a direct sum: 5e-33 relative at s = 200), so `mzv2` now sums the Hurwitz values by its own asymptotic series (`hz`); the second run at 560 digits passes all five; these three are repeated as `dev_06` and `run_01` |
| `dev_01_pilot_grid_120` | the pilot: `order9.py grid --grid=120,1/4,34,200` (N = 120, w = 1/4, V = 34, 200 digits, 136 panels): **137 s** (panel setup 7 s; 14 … 23 s per k = 2 … 9), one process |
| `dev_02_planted_pslq_F` | `order9.py pslq` with `--load=dev_planted_f8.json --pslq-cap=480` on F1 … F7, F7m: PF1 … PF7 pass (planted relations recovered, perturbed bases find nothing), the real PSLQ of the **planted** f₈ finds the planted relation in F6, F7 (not in F1 … F5; not in F7m, as the planted ζ(5,3) coefficient is not zero), 120 s |
| `dev_03_planted_pslq_X1X2` | the same on X1, X2 at cap 480 (X1: PX1 passes and the planted f₈ is found in 7 min; X2 was still running when this file was written) |
| `dev_03_…stopped`, `dev_04_…stopped` | the first starts of dev_03 and dev_04, **stopped by me after 11 s**: with dev_02 still running they made three processes of mine (the limit is two); `dev_04_planted_pslq_XF_nr.stopped_a.*` is the restart of XF (planted only, `--no-real`, cap 480), stopped by me after 22 min inside its first PSLQ call (51 constants), to free the second process; no result |
| `dev_05_remainder_pilot_N120` | `order9.py remainder` on the printed Ω₁ … Ω₇ of the pilot (`dev_pilot_N120_values.json`, a wrapper of the log's numbers): to set the bars of R8, R9, X5 below |

**Seen before this file:**
- **Ω₇ ≈ 25545344.60539842986474372299543836025230506839973816817720289984585922…** (the pilot's 177 digits; N = 30 gives 25545344.605398429863…); #282's two-point estimate was 25545476. Ω₆ of the pilot equals #282's (3672259.16259439048965785936962062657…).
- **Digits.** The law digits ≈ N log₁₀(7.7/w) holds at order 9: Ω₀ … Ω₆ against their closed forms 177.2 … 179.0 digits (expected 178.6), the slopes of G_k against −4π 178.9 digits, |G_k at the root|/|slope| ≤ 1.95e-186.
- **Timing.** 137 s for the pilot (one process, the Mac loaded: load average 3 … 4). With P·N² × (working digits factor) the grids below are expected at about 2.4 h each (2 processes), the projection is in the issue before the runs.
- **The remainder on that Ω₇** (`dev_05`): rem₈·s⁷ → Ω₇ by the two-point extrapolation from D = 5103, 10⁴ gives 25545476.0, relative difference 5.16e-6 from the pilot's Ω₇; rem₉·s⁸ → Ω₈ ≈ −1.094e9 (negative; |rem₉·s⁸(10⁴) − rem₉·s⁸(5103)| = 1.29e6);
  the refit of #195's 64 values of W² with Ω₀ … Ω₆ fixed gives Ω₇ to 1.6e-19 (K = 14), 1.1e-18, 4.2e-18, 1.1e-17, 2.0e-17, 3.7e-17, 5.8e-17 (K = 44). **The bars of R8, R9 and X5 below are set knowing these numbers.**
- ζ(5,3) = 0.03770767298484754401130478229365991482… (`dev_06`, repeated in `run_01`).
- The planted f₈ of `dev_planted_f8.json` (13 integers up to 9e8 over 14175, `dev_planted_f8_coefficients.json`) is invented and stands in for the real f₈ in every PSLQ tool check.

**Not seen:** any PSLQ of the real f₈ (the bases below are declared first); Ω₇ on the grids of record; the controls' behavior on any target.

## Convention

As in README.md, matched.py, order3.py … order8.py and #195: s = 2(D − 3), ε = 1/s, W²a² = s + Ω, Ω = Ω₀ + Ω₁ε + Ω₂ε² + … , R = r^s, l = ln R = −2 ln cos θ.
Ω₀ … Ω₅ are the closed forms of #26, #208, #220, #263 (`order8.closed_omegas`), Ω₆ the closed form identified in #282 (`order9.om6_closed`: f₇ of its PSLQ relation, minus the exact lower terms; it equals #282's computed Ω₆ to 400 digits).
These seven are the planted truth; Ω₆ is also compared with #282's computed value (`inputs_I282_G1.json`, `inputs_I282_G2.json`, copied from `I282-rpi5/G1.json`, `G2.json`; 430.8 digits between them).

**F.** F(ε) = e^{4 ln 2 ε}(1 + Ω₀ε + Ω₁ε² + …) = 1 + f₂ε² + f₃ε³ + … ; f₈ = Ω₇ + Σ_{j=0}^{6}Ω_j(4 ln 2)^{7−j}/(7−j)! + (4 ln 2)⁸/8!, with Ω₀ … Ω₆ exact (closed forms). W²a² = s 2^{−4/s}F(1/s).
The question of the issue: is f₈ free of ln 2, i.e. a rational combination of ln 2-free monomials of π², ζ(3), ζ(5), ζ(7) **and ζ(5,3)**? (f₂ … f₆ are checked symbolically in #263 and here (LN2); f₇ is identified in #282 and checked here against the printed Ω₆ (LN2b).)
The weight-8 Euler sums are four: π⁸, π²ζ(3)², ζ(3)ζ(5) and the double zeta value ζ(5,3) = Σ_{n>m≥1} n⁻⁵m⁻³ (Zagier's dimension 4); a basis without ζ(5,3) is for the three monomials only (F7m).

## The order equations at k = 9

#26's equations, unchanged, for k = 0 … 9 (see `order8.py`), with c₁ … c₈ as in `order8.py` and the new

    c_9 = Ω₀l⁸/40320 + Ω₁l⁷/5040 + Ω₂l⁶/720 + Ω₃l⁵/120 + Ω₄l⁴/24 + Ω₅l³/6 + Ω₆l²/2 + Ω₇l + Ω₈ + l⁹/241920 − l⁸/40320 + l⁸/(40320R)                      (new)

c₉ is the coefficient of ε⁹ of (1 + εΩ)e^{εl} − (½ + ε)(1 − 1/R)e^{−εl} − e^{−εl}/(2R) (check E0, sympy, residual 0, through k = 9). G_k = C_k(∞) is affine in Ω_{k−2} with slope −4π: G₂ = 0 gives Ω₀, … , G₈ = 0 gives Ω₆, **G₉ = 0 gives Ω₇** (Ω₈ drops out of G₉: it is h₉(1), subtracted).
Ω₀ … Ω₇ are solved in turn by `order8.omega_chain` (the cached chain: 8 integration units per step, 64 for k = 2 … 9; the uncached chain has 2(2k + 1) per step, 192) with no closed form of Y_k or L_k and no input value of Ω₀ … Ω₆.
For the mutations that change an input of the lower levels (`wrong_Om0` … `wrong_Om6`) the chain is recomputed from level 0.

## Grids of record (declared before the runs of record)

Method B as in I282-rpi5's README: v = √l (R = e^{v²}), panels of width w on [0, V], N Chebyshev nodes per panel, cumulative integrals by the spectral integration matrix (`PanelB`, `PanelK`).

| name | N | w | V | working digits | panels | expected digits (N log₁₀(7.7/w)) | tail e^{−V²/2}V³⁶ | expected wall |
|---|---|---|---|---|---|---|---|---|
| G1 | 405 | 1/4 | 57 | 625 | 228 | 602.9 | 10⁻⁶⁴²·³ | 2.4 h (panel setup 13 min of it) |
| G2 | 428 | 3/10 | 57 | 625 | 190 | 603.2 | 10⁻⁶⁴²·³ | 2.3 h |

N is larger than the issue's 330 because the Mac is faster than the issue's rpi5 estimate (the pilot: 137 s): the grids give about 596 digits, so that PSLQ can run at d = 560 digits and the bases X2, X3, XF can hold heights up to 10¹⁴, 10¹², 10⁹ (below).
Also run and reported, not gated: B1 (60, 2/5, 26, 100), B2 (100, 1/4, 32, 170), B3 (170, 1/4, 40, 285) (expected digits 77.1, 148.9, 253.1).
**The control grids** (`--cgrids`, used only for the controls of the grid-dependent mutations): C1 = (90, 1/4, 32, 160) (expected 134.0 digits), C2 = (85, 3/10, 31, 150) (119.8), named G1 and G2 in a `--cgrids` run, with the same bars (100 digits) as the grids of record.
The agreement of G1 and G2 on Ω₇ is an estimator range over grid and precision, **not a rigorous bound**; nothing here is a rigorous enclosure.
**What the evaluations share:** the table of c_m and h_k (one sympy expansion, E0, extended to k = 9), the analytic-at-throat condition, `PanelB`, `PanelK`, the cached chain and mpmath. G1 and G2 share the code and differ in N, w, V and precision.
#195's 64 values of W² (the full equation in a Rust crate, no matching) share none of the matched machinery and are the independent reference for Ω₇ (X5); the closed forms of Ω₀ … Ω₅ and #282's Ω₆ are the planted truth.

## Criteria (each can fail; written before the runs of record)

"d digits" means a relative difference ≤ 10^−d. The code is `order9.py` at commit 957c9a8 of `wip/i315-omega7` (the code of the runs of record, unless a later commit is named in "Results of record").

| id | statement | bar |
|---|---|---|
| E0 | the table of h_k (k = 0 … 9) and dY_k/dl (k = 1 … 9) equals the ε-expansion of the master equation | sympy residual 0 |
| CACHE | the cached chain equals the uncached chain on (24, 1/2, 12, 60 digits): Ω₀ … Ω₇ | relative difference ≤ 10⁻⁵⁵ |
| LN2 | F = e^{4 ln 2 ε}(1 + Ω₀ε + … + Ω₅ε⁶) from the closed forms of Ω₀ … Ω₅: f₀ = 1, f₁ = 0 and d f_n/d ln 2 = 0 for n = 2 … 6 | sympy residual 0 |
| TR6 | Ω₆ as printed in omega6.md (24 terms) equals Ω₆ from the f₇ relation of #282 by exact algebra (a transcription check) | difference 0 |
| LN2b | f₇ from the printed Ω₆ has d f₇/d ln 2 = 0 and equals the f₇ of #282's relation | sympy 0 |
| ZV1, ZV2, ZV2b | ζ(5,3) + ζ(3,5) = ζ(3)ζ(5) − ζ(8); 6ζ(5,3) + 15ζ(6,2) + 30ζ(7,1) + 3ζ(4,4) = ζ(8) (shuffle minus stuffle); ζ(2,6) + ζ(6,2) = ζ(2)ζ(6) − ζ(8); at 560 digits, `mzv2` by an exact head n ≤ 2000 and an asymptotic tail | residual ≤ 10⁻⁵⁵⁵ |
| ZV3 | ζ(5,3) against `mp.nsum` at 30 digits | 20 digits |
| ZV4 | PSLQ at 550 digits, H = 10¹²: no relation among π⁸, π²ζ(3)², ζ(3)ζ(5), ζ(5,3); a relation with nonzero ζ(6,2) and zero π²ζ(3)² coefficient among those four and ζ(6,2) | as stated |
| PL0 … PL5 | planted: Ω₀ … Ω₅ of G1 and G2 against their closed forms, the same code path that gives Ω₇ | 100 digits each (the issue's bar) |
| PL6 | planted: Ω₆ of G1 and G2 against #282's computed Ω₆ (its G1, `inputs_I282_G1.json`) | 100 digits (the issue's bar) |
| PL6c | Ω₆ of G1 and G2 against the identified closed form | 100 digits |
| PLW | the control `wrong_Om_i` moves Ω_{i+1} of G1 and G2 (evaluated only under those mutations; the control's own statement) | change > 10⁻³ |
| SL | the evaluated slope of G_k in Ω_{k−2} against −4π, k = 2 … 9, G1 and G2 | 100 digits |
| RES | max over k = 2 … 9 of \|G_k at the chain's root\|/\|slope\| | 10⁻¹⁰⁰ |
| M7 | Ω₇ of G1 against G2 (two grids, two precisions) | 100 digits (the issue's) |
| RNG | Ω₇ of G1 and G2 between 2.4e7 and 2.7e7 (#282's estimate 2.55e7) | the range |
| X5 | Ω₇ of G1 and G2 against the polynomial extrapolation in 1/s of #195's 64 values of W² (qd, 60 digits, D = 50 … 10⁴) with Ω₀ … Ω₆ fixed at the closed forms: y = (W² − [s + Ω₀ + … + Ω₆/s⁶])s⁷ = Ω₇ + Ω₈/s + …, the K points of largest s, K = 14, 18, 22, 26, 30, 36, 44 | 1e-14 on every window (an estimator range, not a bound; set knowing 1.6e-19 … 5.8e-17 on a 177-digit Ω₇) |
| R8 | two-point extrapolation (s₂x₂ − s₁x₁)/(s₂ − s₁) of rem₈·s⁷ from D = 5103, 10⁴ against the computed Ω₇ | relative 1e-4 (an estimate; set knowing 5.16e-6) |
| R9 | the series through Ω₇ (of G2) against #195's W²: \|rem₉·s⁸(D = 10⁴) − rem₉·s⁸(D = 5103)\| (a wrong Ω₇ adds (error)·s, 2e4 per unit) | 5e6 (set knowing 1.29e6) |
| TBL | the table of bases below equals the code's `PSLQ_BASES` | exact |
| PF1 … PF7, PF7m, PX1 … PX3, PXF | PSLQ tool checks of the twelve bases below: the planted relation is recovered exactly and the perturbed basis on the planted target finds nothing | exact recovery; none |
| ID7 | Ω₇ from the relation PSLQ found in F7 (f₈ = −Σcᵢbᵢ/c₀, Ω₇ = f₈ − the exact ln 2 terms with Ω₆ printed), evaluated at 600 digits, against G1 and G2 | 520 digits |
| ZL | F7 found a relation, and every relation found in a basis with ln 2 (X1, X2, X3, XF) has zero coefficients on every ln 2 monomial | exact |

**ID7 and ZL are the structure's verdict and can fail**: if no relation of f₈ is found in the ln 2-free basis F7 they fail, and that is a result (*not found* in that basis), not a defect to repair.
Reported and not gated: the digits of G1, G2 against B1 … B3; Ω₇ to the working digits of every grid; rem₈·s⁷ and rem₉·s⁸ at the D of #195's list; each PSLQ verdict on the real f₈ (a relation not found is a result, not a failed check); Ω₇ by weight when a relation is found;
the coefficient of ζ(5,3) in f₈ and the height of the integer vector.

## PSLQ (declared before the run of record)

`mp.pslq(x, tol, maxcoeff = H, maxsteps = 4·10⁶)` on [f₈, constants…], f₈ computed from Ω₇ of G2 and the exact Ω₀ … Ω₆, rounded to d = min(560, ⌊digits G1 and G2 share on Ω₇⌋ − 32) digits, constants at d digits (ζ(5,3) by `mzv2`, ZV1 … ZV4).
Tolerance τ = 10^−(d − 30) (the slack is 30, not #282's 12: the terms cᵢbᵢ of a relation of height 10¹² are of size 10¹⁶ and their rounding is 10^−(d − 16), which a slack of 12 would not cover).
Budget (n + 1)·log₁₀(2H + 1) + 1, n = the number of constants. A relation counts only if (i) it holds at τ, (ii) **its budget plus the slack 30 is below d** (stricter than #282's "budget below d"), (iii) the basis with the first constant of non-zero coefficient shifted by √2·10⁻³ finds nothing,
(iv) the coefficient of f₈ is not zero, and (v) it holds at d + 20 digits (tolerance 10^−(d − 10)) on both G1 and G2. Otherwise "not found" or "found but does not count" is reported with the basis, d, τ and H.
**The bases (declared before any PSLQ of the real f₈).** The ln 2-free monomials of weight ≤ 8 (π²: 2, ζ(3): 3, ζ(5): 5, ζ(7): 7, ζ(5,3): 8, products add): π⁸, π²ζ(3)², ζ(3)ζ(5), ζ(5,3) (weight 8), π⁴ζ(3), π²ζ(5), ζ(7) (7), π⁶, ζ(3)² (6), π²ζ(3), ζ(5) (5), π⁴ (4), ζ(3) (3), π² (2), 1 (0): 15 constants.
They span the Euler sums of weight ≤ 8 (Zagier's dimensions 1, 0, 1, 1, 1, 2, 2, 3, 4; independence is conjectural). The bases with ln 2 are ln^j 2 times the ln 2-free monomials of weight ≤ 8 − j (ζ(5,3) enters only at j = 0).
**The table below is the output of `order9.py table`; TBL compares it with the code, so that no H is typed from memory (#282's A2, A3).**

<!-- table -->

| basis | constants besides f8 | n | H | budget | budget + slack |
|---|---|---|---|---|---|
| F1 | the 4 monomials of weight 8 | 4 | 1e16 | 82.5 | 112.5 |
| F2 | F1 and the 3 of weight 7 | 7 | 1e16 | 131.4 | 161.4 |
| F3 | F2 and the 2 of weight 6 | 9 | 1e16 | 164.0 | 194.0 |
| F4 | F3 and the 2 of weight 5 | 11 | 1e16 | 196.6 | 226.6 |
| F5 | F4 and pi^4 | 12 | 1e16 | 212.9 | 242.9 |
| F6 | F5 and zeta(3) | 13 | 1e16 | 229.2 | 259.2 |
| F7 | F6 and pi^2, 1 (the ln 2-free basis, weight <= 8) | 15 | 1e16 | 261.8 | 291.8 |
| F7m | F7 without zeta(5,3) | 14 | 1e16 | 245.5 | 275.5 |
| X1 | F7 and ln 2 x the 11 monomials of weight <= 7 | 26 | 1e15 | 414.1 | 444.1 |
| X2 | X1 and ln^2 2 x the 8 of weight <= 6 | 34 | 1e14 | 501.5 | 531.5 |
| X3 | X2 and ln^3 2 x the 6 of weight <= 5 | 40 | 1e12 | 505.3 | 535.3 |
| XF | X3 and ln^4 2 x 4, ln^5 2 x 3, ln^6 2 x 2, ln^7 2, ln^8 2 (the full basis, weight <= 8) | 51 | 1e9 | 484.7 | 514.7 |

<!-- /table -->

(`n` is the number of constants besides f₈; a `PF`/`PX` line of a log prints n + 1, the length of the vector.)
The capacity of d = 560 digits is what fixes H: X2 holds heights up to 10¹⁴, X3 up to 10¹², XF up to 10⁹; **#282's f₇ relation has height 2.76e9 and its weight-8 successor is expected larger** (the integer vector of f₂ … f₇ grew by 28, 49, 120 per order).
**What a relation's height does to a basis:** a basis whose H is below the height of the relation cannot find it, so its "not found" is for that H only (the caveat of #282's XF at 10⁸); a basis with ln 2 can find the F7 relation only if H is above its height, and the check is then that the coefficients on the ln 2 monomials are zero.
**Run order and one rule, declared now:** F1 … F7, F7m, then X1, X2; X3 and XF are started after F7, and if F7 found a relation of height above the basis's H the run of that basis is not made and is reported as "not run: height h above H" (its result would be the capacity caveat above, as in #282's run_06c);
the planted-relation and perturbed-basis checks PX3, PXF are made in any case. If F7 finds nothing, every basis is run, since then the ln 2 bases are the only place a relation can be.

**Planted truth** (the tool's size check): the same call on x = (Σ cᵢbᵢ)/den, cᵢ integers of 3 to 4 digits and den ∈ {3, 5, 7, 9, 11, 13, 15, 21, 45} drawn once with `random.Random(seed)` (seeds 315001 … 315006 for F1 … F6, 315007 for F7, 315008, 315009, 315010 for X1, X2, X3, 315011 for F7m, 315012 for XF),
bᵢ the true constants of the basis: the vector (den, −c₁ … −c_n) must be returned (up to sign), and the basis with b₂ + √2·10⁻³ must find nothing. (At the small d of a control run H is lowered to 10^max(4, ⌊(d − 35)/(n + 1)⌋ − 1).)
**What a result means.** If F7 finds a relation that counts, **F is free of ln 2 at ε⁸ and the relation is an *identification*** (PSLQ, at d digits, a *conjecture* until a by-hand reduction meets it; none is attempted); Ω₇ then follows by exact algebra (ID7).
If F7 finds nothing, the ln 2-free question has the answer *not found in F7* (at H = 10¹⁶, d = 560); X1 … XF then say whether a relation with ln 2 exists in their span, and a relation found there with a nonzero coefficient on a ln 2 monomial is the answer *F has ln 2 at ε⁸*.
If F7 finds a relation and F7m does not, **ζ(5,3) enters f₈** (its coefficient is reported); if F7m finds the same relation, its ζ(5,3) coefficient is zero. A "not found" is for these bases only: odd powers of π, Catalan's constant, Li₄(½) and its products, Li₅(½), Li₆(½), Li₇(½), Li₈(½) and the alternating sums of weight ≥ 6 beyond the ln 2 monomials are in no basis.

## Controls and what they break (targets are declared in amendments, after their development runs and before the controls of record)

Every check has a `--mutate=NAME` control. A control is **on target** when the set of checks that fire (FAIL) is exactly the declared set. Groups, each with its own nominal run:
(CHK) `sym struct cache`: `wrong_h`, `wrong_c6`, `wrong_c7`, `wrong_c8`, `wrong_c9` (E0), `stale_cache` (CACHE), `ln2_struct` (LN2, LN2b);
(ZVC) `zv`: `zeta53_wrong` (ζ(5,3) · (1 + 10⁻³⁰));
(T1) grid-dependent mutations on the control grids: `wrong_h`, `wrong_c6`, `wrong_c7`, `wrong_c8`, `wrong_c9`, `wrong_Om0` … `wrong_Om6`, `coarse_B`, `short_tail`, `stale_cache` (parts `evals values remainder`, and `pslq --bases=F1,F3 --no-real`, with H lowered because d is about 90 there);
(T2) post-processing mutations on the saved Ω's of record: `pslq_wrong_basis`, `pslq_wrong_target` (parts `values pslq` with `--no-real --bases=F1,F3,F5 --pslq-cap=200`), `wrong_Om7_series` (Ω₇ + 10⁶ in R8, R9), `wrong_closed5` (Ω₅'s closed form + 10⁻³), `wrong_closed6` (Ω₆'s closed form + 10⁻³: PL6c, X5), `zeta53_wrong` (the real PSLQ: F7 finds nothing);
(T2b) the same two PSLQ mutations on F2, F4, F6, F7, F7m, X1, X2, X3 (`--pslq-cap=300`); XF has its own controls (T2bxf);
(ST) the structure verdict: `pslq --bases=F7 --pslq-cap=300 --save-rel=…` then `closed7 --rel=…` on the planted f₈ (`dev_planted_f8.json`) and on the saved Ω's of record: `ln2_leak` (f₈ + 1000 ln 2 ζ(7): F7 finds nothing, ID7 and ZL fire), `f8_rel` (a coefficient of the relation off by one: ID7), `ln2_zl` (a nonzero ln 2 coefficient put in: ZL).

## Runs of record

On the grids of record, as separate processes (each started with `runrec.sh`, `nice -n 10`, `OMP_NUM_THREADS=1`, `nohup`):

| run | command (from `notes/wormhole_largeD`, `PY` = `~/Source/negative-mass/.venv/bin/python`) | expected |
|---|---|---|
| `run_01` | `$PY -I order9.py sym struct cache zv table --check=$RAW/README.md` | 13 checks, 20 s |
| `run_02` | `$PY -I order9.py evals --grids=G1 --save=$RAW/G1.json` | about 2.4 h |
| `run_03` | `$PY -I order9.py evals --grids=G2 --save=$RAW/G2.json` | about 2.3 h |
| `run_04` | `$PY -I order9.py evals --grids=B1,B2,B3 --save=$RAW/B.json` | about 15 min |
| `run_05` | `$PY -I order9.py values remainder --load=$RAW/G1.json,$RAW/G2.json,$RAW/B.json --ref282=$RAW/inputs_I282_G1.json,$RAW/inputs_I282_G2.json --w2raw=$RAW/inputs_w2_growthD.txt` | PL0 … PL6, PL6c, SL, RES, M7, RNG, R8, R9, X5 |
| `run_06a` | `$PY -I order9.py pslq --bases=F1,F2,F3,F4,F5,F6,F7,F7m --save-rel=$RAW/rel_a.json --load=$RAW/G1.json,$RAW/G2.json` | PSLQ at d = 560 |
| `run_06b` | `… pslq --bases=X1 --save-rel=rel_b.json` | |
| `run_06c` | `… pslq --bases=X2 --save-rel=rel_c.json` | |
| `run_06d` | `… pslq --bases=X3 --save-rel=rel_d.json` | by the rule above |
| `run_06e` | `… pslq --bases=XF --save-rel=rel_e.json` | by the rule above |
| `run_07` | `$PY -I order9.py closed7 --rel=rel_a.json,rel_b.json,rel_c.json,rel_d.json,rel_e.json --load=…` | ID7, ZL, Ω₇ by weight |

(`$RAW` is `~/Source/negative-mass-raw/I315-mac`.)
**Stop condition:** a grid or a PSLQ run not finished in 6 h of wall time is stopped and reported with what finished. Memory is reported only. If G1 or G2 stops, the other grid and B1 … B3 are reported and PSLQ runs at the digits they share.

## Amendments

**A1 (2026-11-28, 03:40 PST, after the first k-step of G1 and G2, before any other run of record; criteria unchanged):** three corrections of this file.
- **Run count of `run_01`.** The table says 13 checks and 20 s; the run has **11 checks** (E0, CACHE, LN2, TR6, LN2b, ZV1, ZV2, ZV2b, ZV3, ZV4, TBL) and took 7 s; `run_01` passed 11 of 11 (`run_01_sym_struct_cache_zv_table.log`). The disclosure's "`dev_06` and `run_01`" is `run_01` alone: `dev_06` was never made.
- **The wall projection was wrong.** The README and the issue said about 2.4 h per grid. The first k-step of G1 and of G2 took **1612 s each** (panel setup about 15 min before it), 1.7 times the projection (it scaled the pilot's time by P·N² and a factor 3 for the 625-digit arithmetic; the factor is larger).
  Projected now: about 4.4 h per grid, ending near 07:20 PST (started 02:51 PST), above the 4 h line of the task and below the 6 h stop. Reported to the coordinator and on the issue at 03:35; **the coordinator answered "continue with the grids as they are"** (hc, 03:37; a restart at N = 355 would save about 50 min and lose the X2/X3 capacity, so none was made) **and "run the PSLQ stage as declared, X3 and XF included unless the declared rule skips them"**.
- **Machine load at the start of the grids:** load average 3.8 (`run_02_evals_G1.env`), two processes of mine, nice 10.
