# I208-dh610: Ω₃ from the order-5 matching integral of Paper III's large-D expansion

Machine: dh610-fedora (Fedora, 20 cores, 62 GB), shared with choptuik-large-d's runs (10 to 15 cores); runner
negative-mass-dh610-i208 (Claude Code, Sonnet 5.5, account claude-me2). Issue: https://github.com/nmoinvaz/negative-mass/issues/208
Code: worktree `~/Source/negative-mass-i208`, branch `wip/i208-omega3` (from 5b53626, the head of #26's branch); script
`notes/wormhole_largeD/order5.py` (it imports `PanelB` from the unchanged `order4.py`), output `order5_output.txt`, note `omega3.md`.
Pushes: `git push origin HEAD:refs/heads/wip/i208-omega3`. Development runs `dev_NN_*` and runs of record `run_NN_*` keep stdout
(`.log`), stderr (`.err`) and the exit code (`.rc`) beside this file (`devrun.sh`, `runrec.sh`, copied from I26-dh610); reruns are
numbered, nothing is overwritten. Amendments are numbered and dated at the end. Status words as in AGENTS.md: agreement of an integral
with a constant is *numerical evidence*; a PSLQ relation is an *identification*; a closed form reached by hand with each step checked is
*derived*; a step checked by sympy is *checked symbolically*. No sentence here claims novelty.

## What was run before this file (disclosure)

Development runs, in order (every log is kept beside this file; nothing was overwritten):

| runs | what |
|---|---|
| `dev_00` | `order5.py sym`: E0 at k = 5 (residual 0) |
| `dev_01` … `dev_05`, `dev_07`, `dev_08` | one grid each through the chain k = 2 … 5 (`order5.py grid --grid=N,w,V,dps`), no gate; `dev_06_compare`, `dev_09_compare` compare them |
| `dev_09_nominal` | all parts of the first full version of `order5.py` with `--no-real` (the PSLQ part runs its planted and perturbed controls and skips the real target); its remainder part crashed (`KeyError: 1000`: the 64-value list of `w2_output.txt` has no D = 1000 or 2000); fixed by reading the 60-digit qd values of #195's `run_02` for D = 200 … 2000, as #26 did (`inputs_w2_growthD.txt`, copied from I26-dh610, which holds the RESULT lines of I195-dh610/run_02_w2_qd_growth.log) |
| `dev_10` … `dev_12` | controls `wrong_h`, `wrong_c5`, `wrong_Om0`, same parts (same remainder crash); `dev_13` the remainder of the nominal values by `--load`; `dev_18` … `dev_20` the remainders of those three by `--load` |
| `dev_14` … `dev_17` | controls `wrong_Om1`, `wrong_Om2`, `coarse_B`, `short_tail`, all parts |
| `dev_21`, `dev_22` | controls `pslq_wrong_basis`, `wrong_Om3_series` by `--load` of `dev_09_nominal.json` |
| `dev_23` | the real-target branch of the PSLQ part on **synthetic targets with a known answer** (a member of P2 and ζ(5)/π; no real Ω₃). It found a defect in my control: the perturbed basis shifted a constant by 10⁻³, a rational, and P2 contains 1, so the true relation scaled by 1000 was found; changed to √2·10⁻³ (irrational), `dev_25_real_branch` rerun (member found in P2 only, perturbed basis nothing, ζ(5)/π nowhere); `dev_26`, `dev_27` rerun the PSLQ controls with that code. A guard was added in the same change: a relation counts only if Ω₃'s coefficient is not zero |
| `dev_NN_order5_wip.py` | the code of each development run, 00, 02, 09, 13, 24, 25; `dev_25_order5_wip.py` is the code of the runs of record |

**Seen before this file:** Ω₃ of every development grid (the best, N = 90, agrees with #195's 40-digit median to 3.8e-38); the digits of every grid
against the closed forms of Ω₀, Ω₁, Ω₂; the remainders rem·s⁴ at D = 1000, 2000, 5103, 10⁴ (`dev_13`: |rem·s⁴ − Ω₄| = 21.4, 10.5, 4.04, 2.05; #26's table
of rem·s³ with #195's Ω₃, which this Ω₃ equals to 4e-38, has the same numbers). **Not seen:** any PSLQ on the real Ω₃ (the only earlier one is
#195's `dev_25_pslq_omega3`, 35 digits, nothing found in the pure weight-4 basis). The bars below are the issue's or the task's, or digits well below
what the development grids reached; the bars of R3 and R4 were set knowing that order of magnitude (declared as such), and are not tuned to it: R3 asks
for falling and 0.05 % where the numbers are 0.016 %, R4 for 0.1 where the number is 0.018.

## Convention

As in README.md, matched.py, order3.py, order4.py and #195: s = 2(D − 3), ε = 1/s, W²a² = s + Ω, Ω = Ω₀ + Ω₁ε + Ω₂ε² + Ω₃ε³ + …, R = r^s,
l = ln R. Ω₀ = −4 ln 2, Ω₁ = 2π²/3 + 8 ln²2, Ω₂ = 80ζ(3) − (8/3)π² ln 2 − (32/3) ln³2 (#26), Ω₃ = −652.84010757006… (#195's fit, a
fit). In 1/(D − 3) the coefficient of order k is Ω_k/2^k.

## The order equations at k = 5

#26's equations (`omega2.md`), unchanged, for k = 0 … 5:

    dY_k/dl = F_{k−1},  F_{k−1} = Σ_{j=0}^{k−1} L_{k−1−j} l^j/j!                     (Y_0 = 1, Y_k(R = 1) = 0)
    (R − 1)L_k′ − L_k/2 = h_k,   h_k = (1 − 1/R)L_{k−1} + Σ_{j=0}^{k−1} Y_j c_{k−j} + Y_k/2,   h_k(1) = Ω_{k−1}
    c_1 … c_4 as in I26-dh610/README.md
    c_5 = Ω₀ l⁴/24 + Ω₁ l³/6 + Ω₂ l²/2 + Ω₃ l + Ω₄ + l⁵/80 − l⁴/24 + l⁴/(24R)                         (new)

c_5 is the coefficient of ε⁵ of (1 + εΩ)e^{εl} − (½ + ε)(1 − 1/R)e^{−εl} − e^{−εl}/(2R), the same expression whose lower coefficients are c_1 … c_4.
The solution analytic at the throat is L_k = −2Ω_{k−1} + (R − 1)^{1/2}C_k, C_k = ∫₁^R (h_k − Ω_{k−1})(R′ − 1)^{−3/2}dR′, and the mode needs
G_k = C_k(∞) = 0. G_k is affine in Ω_{k−2} with slope −4π: G_2 = 0 gives Ω₀, G_3 = 0 Ω₁, G_4 = 0 Ω₂, **G_5 = 0 gives Ω₃** (Ω₄ drops out of
G_5: it is h_5(1), subtracted). Ω₀ … Ω₃ are solved in turn by one function (`omega_chain`) with no closed form of Y_k or L_k and no input value
of Ω₀ … Ω₂: planted orders k = 3, 4 are the same path as the new k = 5.

## Method B at order k

Variable v = √l (R = e^{v²}), panels of width w on [0, V], N Chebyshev nodes per panel, cumulative integrals by the spectral integration matrix
(mpmath matrices; `PanelB` of order4.py, shared, with its T₀ defect of #26 fixed there). For each k: Y_k = ∫₀^l F_{k−1}dl from the left; h_k from the table;
the tail C_right(v) = ∫_v^V (h_k − h_k(1))R(R − 1)^{−3/2}2v dv from the right; L_k = −2h_k(1) − u C_right (u = √(R − 1)); G_k = C_right(0).
The truncation at V costs about e^{−V²/2} times a power of V. Two evaluations of G_k (Ω_{k−2} = 0 and 1) give Ω_{k−2} and the slope.

**Cancellation, measured** (`dev_03`, `dev_04`: N = 60, w = 2/5, V = 24 at 200 and at 240 working digits; `dev_06_compare.log`): the two precisions agree on
Ω₀, Ω₁, Ω₂, Ω₃ to 198.5, 198.6, 200.5, 198.7 digits, so rounding costs about 1.5 digits at every order including k = 5; the extra order adds
nothing measurable. The error of a grid is its discretization (`dev_01` … `dev_08`, digits of Ω₀/Ω₁/Ω₂ against the closed forms):

| grid (N, w, V, working digits) | digits | Ω₃ against the next finer grid |
|---|---|---|
| 40, 1/2, 18, 120 (B1 of #26) | 48.7 / 48.2 / 48.2 | 48.9 |
| 50, 2/5, 20, 140 (B2 of #26) | 65.2 / 64.7 / 64.4 | 64.4 |
| 60, 2/5, 24, 200 and 240 | 77.8 / 77.2 / 77.0 | 77.0 |
| 70, 1/3, 26, 240 | 95.9 / 95.4 / 95.3 | 96.0 |
| 80, 3/10, 28, 180 | 113.0 / 112.4 / 112.2 | 112.2 |
| 90, 1/4, 30, 240 | 133.8 / 133.3 / 133.2 | |

**The grids of record (declared before the runs of record):**

| name | N | w | V | working digits | panels | expected digits (from the table above) |
|---|---|---|---|---|---|---|
| B3 | 80 | 3/10 | 28 | 180 | 94 | 112 |
| B4 | 90 | 1/4 | 30 | 240 | 120 | 133 |

Also run and reported, not gated: B1 (40, 1/2, 18, 120) and B2 (50, 2/5, 20, 140), the grids of #26. Working digits are the expected
digits plus 60 or more, against a measured rounding loss of 1.5. The agreement of B3 and B4 on Ω₃ is an estimator range over grid and
precision, **not a rigorous bound**; nothing here is a rigorous enclosure.

**What the evaluations share** (recorded as AGENTS.md asks): the table of c_m and h_k (one sympy expansion, E0, extended to k = 5), the
analytic-at-throat condition, `PanelB` and mpmath. B3 and B4 share the code and differ in N, w, V and precision. #195's fit (the full equation
in a Rust crate, no matching) shares none of the matched machinery and is the independent reference for Ω₃; the closed forms of Ω₀, Ω₁, Ω₂
(derived in #26) are the planted truth.

## Criteria (each can fail; written before the runs of record)

"d digits" means a relative difference ≤ 10^−d.

| id | statement | bar |
|---|---|---|
| E0 | the table of h_k (k = 0 … 5) and dY_k/dl (k = 1 … 5) equals the ε-expansion of the master equation | sympy residual 0 |
| PL0, PL1, PL2 | planted: Ω₀, Ω₁, Ω₂ of B3 and B4 against −4 ln 2, 2π²/3 + 8 ln²2 and 80ζ(3) − (8/3)π² ln 2 − (32/3) ln³2, the same code path that gives Ω₃ | 40 digits each (the issue's bar for Ω₁, Ω₂) |
| PL3 | control `wrong_Om0` moves Ω₁ and `wrong_Om1` moves Ω₂ of B3 and B4 (evaluated only under those mutations) | change > 10⁻³ |
| SL | the evaluated slope of G_k in Ω_{k−2} against −4π, k = 2 … 5, B3 and B4 | 40 digits |
| M3 | Ω₃ of B3 against B4 (two grids, two precisions) | 30 digits (the issue's) |
| X1 | |Ω₃ − (−652.8401075700561254352393037996)| ≤ 1e-30, B3 and B4, #195's fit **as the issue words it** | 1e-30 |
| X1b | amendment A1: the same bar against #195's 40-digit median −652.8401075700561254352393037996473610805 | 1e-30 |
| Q1, Q2, Q3 | PSLQ tool checks of P1, P2, P3 (below): the planted relation is recovered exactly and the perturbed basis on the planted target finds nothing | exact recovery; none |
| R3 | five-term series s − 4 ln 2 + Ω₁/s + Ω₂/s² + Ω₃/s³ (Ω₁, Ω₂, Ω₃ of B4) against #195's qd W² at D = 1000, 2000, 5103, 10⁴ (the values of the 64-D list of `w2_output.txt`): x = rem·s⁴; |x − Ω₄| falls with D at the four D, and at D = 10⁴ it is below 0.05 % of |Ω₄|, Ω₄ = −12794.499860023 (#195's fit, `w2_output.txt`) | falling; 0.05 % |
| R4 | two-point extrapolation (s₂x₂ − s₁x₁)/(s₂ − s₁) from D = 5103 and 10⁴ | within 0.1 of Ω₄ |
| RD0 … RD8, A5 | **added by amendment A3 after `run_03`**: the reduction of G₅ by hand (parts `reduce5`, `a5`, run_04), below | residual 0, or 30 digits (RD6 25) |
| X3 | **added by amendment A2 after `run_02`**: Ω₃ of B3 and B4 against the closed form of the P2 relation found there, 22π⁴/45 + 16π² ln²2/3 + 32 ln⁴2/3 − 320ζ(3) ln 2 − 384ζ(3) (part `closedform`, run_03) | 100 digits |

Reported and not gated: the digits of B3, B4 against B1, B2, and of B1 against B2; Ω₃ to 110 digits of every grid; rem·s⁴ and
(rem·s⁴ − Ω₄)s at the 64 values of D (the second tends to Ω₅); each PSLQ verdict on the real Ω₃.

**X1 as worded cannot be met** (found in `dev_05`, reported to the coordinator, ruling 2026-11-26): the issue's string has 28 decimals and is #195's median
truncated, so every Ω₃ that equals the median differs from it by 4.7e-29 > 1e-30. X1 stays in the runs of record as worded and is **NOT MET**, a
defect of the criterion's wording; X1b (A1) is the criterion that tests the agreement.

## PSLQ (declared before the run of record)

`mp.pslq(x, tol, maxcoeff = H, maxsteps = 10⁶)` on [Ω₃, constants…], Ω₃ of B4 rounded to d = min(110, ⌊digits B3 and B4 share⌋) digits (at least
30), constants at d digits. Tolerance τ = 10^−(d − 12). `mp.pslq`'s tolerance applies to the vector normalized by its norm; the residual
|Σ cᵢxᵢ| is also computed from the integer vector returned. Budget n·log10(2H + 1) + 1, n = the number of elements of the vector.

| basis | constants besides Ω₃ | n | H | budget |
|---|---|---|---|---|
| P1 pure weight 4 | π⁴, π² ln²2, ln⁴2, ζ(3) ln 2, Li₄(½) | 6 | 10⁹ | 56.8 |
| P2 weight ≤ 4 | P1 and ζ(3), π² ln 2, ln³2, π², ln²2, ln 2, 1 | 13 | 10⁶ | 83.0 |
| P3 weight 4, extended | P1 and π ζ(3), π³ ln 2, π ln³2, π²G, β(4), G ln²2, πG ln 2 (G = Catalan, β(4) = Σ(−1)ⁿ/(2n + 1)⁴) | 13 | 10⁶ | 83.0 |

**Why these** (P3). The integrand of G_5 is built from ℓ = ln cos θ, u = tan θ, Cl₂(π − 2θ), Cl₃(π − 2θ), the Li₂, Li₃ of #26's L₃ and, through Y₄, their
integrals, over θ ∈ [0, π/2]. All arguments are π − 2θ or e^{2iθ}, taken at θ = 0 and π/2 only, so the Fourier sums that arise have only the sign (−1)^k
and carry alternating Euler sums (P1, P2 are their weight-4 space: ln 2 · 1, π², ln²2, ζ(3), …, Li₄(½)): **Clausen values at π/2 (G, β(4), π²G) are not
expected** and enter P3 only because the issue names them. The other new constants are the products with an odd power of π, π ζ(3), π³ ln 2, π ln³2,
that appear if G_5 has a weight-5 part without the factor π, which divided by the slope 4π is weight 4 with one π (G_4 had none: G_4 ∝ π throughout). A
relation counts only if (i) it holds at τ, (ii) its budget with the declared H is below d, and (iii) the basis with the first constant of non-zero coefficient
shifted by √2·10⁻³ finds nothing; and the coefficient of Ω₃ is not zero. Otherwise "not found" is reported with the basis, d, τ and H.

**Planted truth** (the tool's size check): the same call on x = (Σ cᵢbᵢ)/den, where cᵢ are integers of 3 to 4 digits drawn once with `random.Random(seed)`
and bᵢ the true constants of the basis: the vector (den, −c₁ … −c_m) must be returned (up to sign), and the basis with b₂ + √2·10⁻³ must find nothing (√2·10⁻³ is outside the rational span of every basis; 10⁻³ is not, since P2 contains 1).

| basis | seed | den | cᵢ |
|---|---|---|---|
| P1 | 208001 | 3 | −5293, −9775, −3564, 3369, 6056 |
| P2 | 208002 | 21 | 6710, 4667, −7444, 6041, −5799, −7340, −4164, 7518, −7530, 8437, −5037, −556 |
| P3 | 208003 | 11 | 3030, 6924, 348, 9390, 5683, 837, 1456, 7077, −9825, 2140, 5615, 1807 |

## Controls (`--mutate=NAME`)

| name | mutated quantity |
|---|---|
| `wrong_h` | the sign of −l/R in c₂ (the table, every order) |
| `wrong_c5` | the sign of l⁴/(24R) in c₅ |
| `wrong_Om0` | Ω₀ → −4 ln 2 + 1/100 in the orders k ≥ 3 |
| `wrong_Om1` | Ω₁ → 2π²/3 + 8 ln²2 + 1/100 in the orders k ≥ 4 |
| `wrong_Om2` | Ω₂ → closed form + 1/100 at order 5 |
| `coarse_B` | N = 10 on every grid |
| `short_tail` | V = 6 on every grid |
| `pslq_wrong_basis` | π⁴ + √2·10⁻³ in the basis given to PSLQ (the planted target is built from the true π⁴) |
| `wrong_Om3_series` | Ω₃ + 1/100 in the five-term series of R3, R4 |
| `wrong_closed` | 23π⁴ in place of 22π⁴ in X3 (A2) |
| `wrong_E3` | the factor 4 of E3 written 2 (A3) |
| `wrong_AD` | the F₂ term of A_D with coefficient 352 + 32 (A3) |
| `wrong_C2` | ∫C² = π⁵/180 in place of π⁵/360 (A3) |
| `wrong_reg` | J₂ in place of J₁ in the regularized u(Lc2, θ) integral (A3) |
| `wrong_J4` | J₄ + πζ(3)/8 (A3) |

**Targets, computed in the development runs `dev_09` … `dev_27` before being declared** (nominal: every check passes except X1, which fails as worded; the lists are the
checks that fail beyond X1; `PL3` is evaluated only under `wrong_Om0`, `wrong_Om1`).

| control | fires | silent |
|---|---|---|
| `wrong_h` | E0, PL0, PL1, PL2, X1b, R3, R4 | SL, M3, Q1 … Q3 |
| `wrong_c5` | E0, X1b, R3, R4 (Ω₃ moves by 0.0243) | PL0 … PL2, SL, M3, Q1 … Q3 (c₅ enters only at k = 5 and both grids share it) |
| `wrong_Om0` | PL1, PL2, X1b, R3, R4 (PL3 passes: Ω₁ moves by 0.027626) | E0, PL0, SL, M3, Q1 … Q3 |
| `wrong_Om1` | PL2, X1b, R3, R4 (PL3 passes: Ω₂ moves by 0.027726) | E0, PL0, PL1, SL, M3, Q1 … Q3 |
| `wrong_Om2` | X1b, R3, R4 | E0, PL0 … PL2, SL, M3, Q1 … Q3 (both grids take the same wrong input) |
| `coarse_B` | PL0 … PL2, SL, M3, X1b, Q1 … Q3 | E0, R3, R4 (Q fires because the grids share 15 digits, so PSLQ runs at 30) |
| `short_tail` | PL0 … PL2, SL, X1b, R3, R4 | E0, M3, Q1 … Q3 (both grids truncate at V = 6 and agree with each other) |
| `pslq_wrong_basis` | Q1, Q2, Q3 | all others |
| `wrong_Om3_series` | R3, R4 | all others |
| `wrong_closed` (A2) | X3 (the part `closedform` has no other check): `dev_31`, 2.5 digits against the bar 100 | |
| `wrong_E3` (A3) | RD1, RD3, RD4, RD6, RD8, A5 | RD0, RD2, RD5, RD7 (RD2 compares two builds that both carry the factor) |
| `wrong_AD` (A3) | RD3, RD4 | the others (RD8 uses the coefficients of the C terms as printed, which RD4 checks) |
| `wrong_C2` (A3) | RD5, RD8, A5 | the others |
| `wrong_reg` (A3) | RD6, RD8, A5 | the others |
| `wrong_J4` (A3) | RD5, RD7, RD8, A5 | RD6 (it uses J₁, J₂, J₃ only) |

X1 has no control (it fails nominally, a defect of its wording); X1b is the check that every value-changing control fires.

## Runs

Production: `systemd-run --user --unit=nm-i208-<name> --working-directory=<dir> nice -n 10 …` with `runrec.sh` (log, stderr, exit code,
/usr/bin/time -v, load), at most 4 processes, one thread each. Stop condition: any run not finished in 2 h of wall time is stopped and reported with
what finished. Memory is reported only. The development runs used the units `nm-i208-dev…`.

| run | what | unit | wall | exit |
|---|---|---|---|---|
| `run_01_sym` | `order5.py sym` | `nm-i208-01` | 0:01.88, peak 58 MiB | 0 |
| `run_02_evals_pslq_remainder` | `order5.py evals pslq remainder --save=run_02_evals.json --w2raw=inputs_w2_growthD.txt` (the real PSLQ is on) | `nm-i208-02` | 11:06.23, peak 130 MiB | 1 (X1 as worded) |
| `run_03_closedform` | `order5.py closedform --load=run_02_evals.json` (A2) | foreground | 0:00.56, peak 53 MiB | 0 |
| `run_04_reduce5_a5` | `order5.py reduce5 a5 --load=run_02_evals.json` (A3) | `nm-i208-04` | 3:14.73, peak 64 MiB | 0 |

Code of `run_01`, `run_02`: worktree commit 57710d3, `order5.py` sha256 2cd0cbea… (`run_00_code.txt`); `run_03`: the commit after amendment A2, which adds `closed_omega3`, `check_closedform`,
the control `wrong_closed` and the `closedform` hook (23 lines added, 3 changed: the usage line, the mutation list, the `--load` condition; `dev_30_order5_wip.py`). Commands run from
`notes/wormhole_largeD`. `order5_output.txt` is the concatenation of the four logs in order.

## Amendments

### A1 (2026-11-26, after dev_05 and dev_09; the coordinator ruled by hc the same day)

**X1** is the issue's criterion as worded, |Ω₃ − (−652.8401075700561254352393037996)| ≤ 1e-30. Found in `dev_05`: that string has 28 decimals and is #195's median
−652.8401075700561254352393037996473610805 truncated, so every Ω₃ equal to the median differs from it by 4.7e-29. The coordinator ruled: X1 stays as worded and **NOT MET**
(a defect of the criterion's wording, reported as such); **X1b** is added with the same bar, 1e-30, against the 40-digit median (raw I195-dh610/dev_25_pslq_omega3.log
line 1; the fit's range is 2.74e-35). X1b was added after the development runs; Ω₃ of the development grids is 3.8e-38 from the median.

### A2 (2026-11-26, after run_02): the PSLQ relation, and its check X3

`run_02` (11 of 12 checks met, X1 as worded not) found, with the real Ω₃ and the declared P2 (tolerance 1e-98, H = 10⁶, d = 110): the relation (45, −22, −240, −480, 14400, 0, 17280, 0, 0, 0, 0, 0, 0)
on (Ω₃, π⁴, π² ln²2, ln⁴2, ζ(3) ln 2, Li₄(½), ζ(3), π² ln 2, ln³2, π², ln²2, ln 2, 1), residual 2.73e-107, largest coefficient 17280 (its own budget 13·log10(34561) + 1 = 60 against
the declared 82.9 < 110), the perturbed basis finds nothing: it counts under the rules above. P1 and P3 found nothing. So Ω₃ = 22π⁴/45 + 16π² ln²2/3 + 32 ln⁴2/3 − 320ζ(3) ln 2 − 384ζ(3)
(status: *identification*). The relation contains ζ(3) alone, weight 3, with Li₄(½) absent; that is why P1 (pure weight 4) found nothing at #195's 35 digits or here.

**Added after seeing this**, declared before its run: criterion **X3** (table above, bar 100 digits on B3 and B4, whose errors are 112 and 133 digits; B1 and B2 reported) and its control `wrong_closed`
(targets computed in `dev_30`, `dev_31`: nominal 112.2/133.4/48.9/64.4 digits, mutated 2.5). A development probe before it (`dev_29_closedform_probe`) gave the same digits. No bar of an earlier criterion was changed.

### A3 (2026-11-26, after run_03): the reduction of G₅ by hand, method A at order 5, and their checks

**What was found** (development scripts, logs kept: `dev_28_a5` with `dev_32`, `dev_33` the numerical method A; `dev_34_reduce5_explore`, `dev_35_reduce5_assemble` the sympy reduction): the exchange identities
E1 and E2 of #26 turn G₅ into one integral of closed forms, but the integrand holds Y₄, which has no closed form. **E3** removes it: Y₄ enters only through (4ℓ + 2c₁)Y₄/S = 2P′Y₄, with c₁ = Ω₀ − 3ℓ − S and
P = cot θ (ℓ − Ω₀), P′ = (Ω₀ − ℓ − S)/S, so ∫2P′Y₄ dθ = −2∫P Y₄′ dθ = −4∫(ℓ − Ω₀)F₃ dθ (Y₄′ = 2 tan θ F₃, the boundary terms PY₄ vanish: Y₄ ~ θ² at 0 and ~ ℓ⁴ at π/2, P ~ 1/θ and ~ x ln x).
The integrand then needs only Y₀ … Y₃ and L₀ … L₃, all closed in #26 (L₃ through Lc2 and the polylogarithms of omega2.md). At Ω₀ = −4 ln 2 it is rest + cC·C + cD·D₃ + cL·Lc2 with
cL = −1024 q u (q = ln 2); cD = 32(6ℓ − 8q) + 32(11ℓ² + 8qℓ − Ω₁)/S has an antiderivative A_D (ℓ, cot θ, θ, K), with A_D(π/2) = 0 and D₃(0) = 0, so ∫cD D₃ = −2∫A_D C; then
cC − 2A_D (K = 2qθ − C) = u(64(16q² + 8q + Ω₁) + 128(8q − 3)ℓ − 512ℓ²) + 512 C, with the cot θ and θ terms cancelling exactly. What remains: ∫uℓⁿC = (2J_{n+2} + 2qJ_{n+1})/(n + 1), ∫C² = π⁵/360
(Parseval), the regularized ∫u[−1024q(Lc2 − J₂) + 128 qΩ₁(θ − π/2)] = −1024qJ₃ + 128qΩ₁J₁ (the divergent constants cancel: −1024qJ₂ + 64π qΩ₁ = 0), and the log-cosine moments J_n (n ≤ 4) and ∫ℓᵇ/S = −bJ_{b−1}.
Assembled in sympy, G₅ = 4π(Ω₃ᶜ − Ω₃) with Ω₃ᶜ the closed form of A2: **the PSLQ identification becomes a derivation if RD0 … RD8 pass.**

**Criteria** (bars written after `dev_37`, whose values were 42 to 45 digits; the bars are below them):

| id | statement | bar |
|---|---|---|
| RD0 | c₁ = Ω₀ − 3ℓ − S and (4ℓ + 2c₁)/S = 2P′ (sympy) | residual 0 |
| RD1 | E3 at j = 3 (closed Y₃, F₂): ∫2P′Y₃ = −4∫(ℓ − Ω₀)F₂ | 30 digits |
| RD2 | the decomposition rest + cC C + cD D₃ + cL Lc2 (sympy) against method A's integrand with Y₄ removed, θ = 0.2, 0.7, 1.1, 1.4 | 30 digits |
| RD3 | A_D′ = cD (sympy), A_D(π/2) = 0, and ∫cD D₃ = −2∫A_D C (quadrature) | residual 0; 30 digits |
| RD4 | cC − 2A_D = u P(ℓ) + 512 C with P as above (sympy) | residual 0 |
| RD5 | ∫uℓⁿC for n = 0, 1, 2 and ∫C² = π⁵/360 (quadrature) | 30 digits |
| RD6 | the divergence cancels (sympy), and the regularized integral by quadrature | residual 0; 25 digits |
| RD7 | ∫ℓᵇ/S = −bJ_{b−1}, b ≤ 5, and J_n (n ≤ 4) from the Beta function against quadrature | 30 digits |
| RD8 | the assembly: G₅ = 0 gives Ω₃ = 22π⁴/45 + 16π² ln²2/3 + 32 ln⁴2/3 − 320ζ(3) ln 2 − 384ζ(3), and the slope is −4π (sympy) | difference 0 |
| A5 | method A at order 5, 40 digits, G₅ by quadrature of the Y₄-free integrand with the closed forms of order4.py (30 + 80 guard digits): slope against −4π, Ω₃ against the closed form, against B4 and against the derived G₅(0) | 30 digits each |

Quadrature as in #26 (Gauss–Legendre on [0, 1], tanh-sinh in π/2 − θ beyond; the angle is recomputed from x at the guarded precision, because u ~ 1/x multiplies terms in θ). **Status:** *derived* if RD0 … RD8 pass, with the facts
it takes: E1, E2 (#26: N4a, N4bg), E3 (RD1, and the boundary argument above), the closed forms Y₃, L₃ (#26), Ω₀, Ω₁, Ω₂ (#26), Parseval for ∫C², the Beta-function moments. It is not independent of A5 (same E1 to E3);
**B is the independent check** (A5 against B4, and the identification found by PSLQ on B's value). Targets of the controls (table above) were computed in `dev_39` … `dev_43`.

**Runs of record, summary** (`order5_output.txt`): 24 checks, 23 met, X1 (as worded) not met. The note is `omega3.md`; `assemble_output.py` writes the output file from the four logs.
