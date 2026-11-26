# I195-dh610: high-precision W²(D) of the Ellis wormhole at large D, and the fit of Ω₁ and Ω₂

Machine: dh610-fedora (Fedora, 20 cores, 62 GB), shared with choptuik-large-d's runs (12 to 15 cores); runner
negative-mass-dh610-i195 (Claude Code, Sonnet 5.5, account claude-me2). Issue: https://github.com/nmoinvaz/negative-mass/issues/195
Code: worktree `~/Source/negative-mass-i195`, branch `wip/i195-w2-largeD` (from main 900c574); crate
`notes/wormhole_largeD/w2_crate/`. Pushes: `git push origin HEAD:refs/heads/wip/i195-w2-largeD`.
Written before the first run (`dev_*`, `run_*`). Development runs `dev_NN_*` and runs of record `run_NN_*` keep stdout
(`.log`), stderr (`.err`) and the exit code (`.rc`) beside this file; reruns are numbered, nothing is overwritten.
Amendments are numbered and dated at the end. A number that came from a development run says so. Status words as in
AGENTS.md; a PSLQ relation is an *identification*, the fitted Ω₁ and Ω₂ are *numerical evidence*.

## Convention (a discrepancy in the task text, reported)

The issue writes the series as `Ω₁/(D−3) + Ω₂/(D−3)² + …` and also asks for Ω₁ = 2π²/3 + 8 ln²2. Those disagree: the
repository's Ω_k (README.md, order3.py, matched.py) are the coefficients of ε^k with **ε = 1/s = 1/(2(D−3))**,
W²a² = s + Ω₀ + Ω₁ε + Ω₂ε² + …, Ω₀ = −4 ln 2, Ω₁ = 10.4233603788 = 2π²/3 + 8 ln²2, and #26's "73/(2(D−3))²" is
Ω₂ ≈ 73. In 1/(D−3) the coefficient of order k is Ω_k/2^k (so the third term is (π²/3 + 4 ln²2)/(D−3), as in
README.md's "Result"). **This run uses the repository's Ω_k.** The coordinator decides if the issue's wording changes.

    g(D) := W²a² − 2(D−3) + 4 ln 2 = Ω₁ ε + Ω₂ ε² + Ω₃ ε³ + …,   ε = 1/(2(D−3)).

## Method

**The equation.** E2 of `master.py` (n = D−2, a = 1, background r′² = F = 1 − r^{−2(n−1)}). Variable
ℓ = s ln r, s = 2(n−1) = 2(D−3), so r = e^{εℓ}, F = 1 − e^{−ℓ}; w := dY/d ln r = Y_ℓ/ε; W² = s + Ω. Then, exactly,

    Y_ℓ = ε w
    F w_ℓ = A Y + B w
    A = (1 + εΩ) e^{2εℓ} − (½ + ε) F − ½ e^{−ℓ},    B = (½ + 2ε) F + ½ e^{−ℓ}

It is `modes_r.py`'s system (Y_r = L, F r L_r = …) and `matched.py`'s R-form with R = e^ℓ, written with w = rL so that
only e^{2εℓ} appears (no 1/r). The transcription is checked symbolically from E2 itself (check E0 below).
- **Throat (ℓ = 0, F = 0).** Regular singular point, exponents 0 and ½ in ℓ (0 and 3 in proper distance). The even mode
  (Y(0) = 1) is the analytic one: w₀ = −(1 + 2εΩ), and for m ≥ 1
  (m − ½) w_m = A₀ Y_m + Σ_{j=1}^m (A_j Y_{m−j} + B_j w_{m−j}) − Σ_{j=1}^{m−1} φ_j (m−j) w_{m−j},  Y_m = ε w_{m−1}/m,
  φ_j = (−1)^j/(j+1)!, with A_j, B_j the Taylor coefficients of A, B at 0. The series converges for |ℓ| < 2π (zeros of F
  at ℓ = 2πik); it is summed at ℓ₀ = 1.
- **Far end.** For r ≫ 1 the two solutions grow like r (decaying, the mode) and rⁿ, and the separation of their
  exponents in ℓ is at least ½: σ(ℓ) = √(¼ + 4ε(1 + εΩ)e^{2εℓ}). The linear system is integrated **inward** from ℓ_∞ to
  ℓ₀ from the arbitrary vector (Y, w) = (1, 1), which the flow contracts onto the decaying solution, the other component
  falling like e^{−∫σ}. No Bessel function and no truncation of F is used. ℓ_∞ is the first ℓ ≥ ℓ₀ (on a 0.25 grid)
  with ∫_{ℓ₀}^{ℓ_∞} σ dℓ ≥ T, T = ln(10^{d}) + 12 for d = 17, 33, 65, 130 digits in f64, dd, qd, od (T = 51, 88, 162,
  311), σ evaluated at the starting Ω.
- **Eigenvalue.** M(Ω) = Y_in w_ser − w_in Y_ser at ℓ₀ (the 2 × 2 determinant of the two ends' vectors, zero at the
  mode); Newton on Ω with the exact derivative, carried as dual parts (Ẏ, ẇ) of the same recursion (A depends on Ω
  linearly). Start: growth.csv's value for D ≤ 30, else the three-term series plus 73/s². Iterate until
  |ΔΩ| < 10^{−d_lane}·|Ω| twice in a row; a different start (±0.5 in Ω) must reach the same root (check S4).
- **Taylor stepping.** Order K and tolerance `tol` per lane; the step is the largest h with |c_k|h^k ≤ tol·|state|∞ for
  k = K−1 and K (multishoot's `plan_path` rule), steps shortened to land on ℓ₀. Reciprocals 1/k are formed in the lane
  (#193's lesson; control `recip_f64` rounds them from f64).

| lane | digits | order K | tol | series order at ℓ₀ | T | stated digits d_lane (planted) |
|---|---|---|---|---|---|---|
| f64 | 16 | 24 | 1e-17 | 20 | 51 | 11 |
| dd | 32 | 48 | 1e-33 | 46 | 88 | 27 |
| qd | 64 | 96 | 1e-65 | 90 | 162 | 56 |
| od | 128 | 180 | 1e-130 | 170 | 311 | 110 |

**Library use.** The crate depends on multishoot 4.2.0, multisolver 0.2.2 and multidouble (the pin of
`taylor_polar/Cargo.toml`: main ba0ad101ce76 by `[patch.crates-io]`). The primary solver is the crate's own lane-generic
Taylor stepper (f64, dd, qd, od behind one trait, as #186's), because multishoot's `Equations` takes constants in
double-double (#193) and has no f64 lane. multisolver's Newton and multishoot's `Shooting` are tried as a second method
(method B: nodes at ℓ = 1, 20, 60, 150, … with the far condition p = 1 at ℓ_∞, the throat series as the left end, the
eigenvalue as the global, written with lane-arithmetic constants and polynomial fields P = e^{2εℓ}, E = e^{−ℓ}). Method B
is an extra: its agreement or its failure is reported in the note, and no criterion below depends on it.

## What is computed, and the checks (each can fail; each has a control)

Digits are agreements between independent computations, not error bounds; an error bar says what it is.

**Equation.**
- **E0** symbolic: E2 of `master.py` with the background relations, written in ℓ, equals the system above (residual 0).
- **M1** scipy `master.py` (E2 in proper distance) at D = 5, 6, 7, 8 agrees with this crate's qd value to 2e-3 (its
  stated accuracy, "about 10⁻³ at D ≤ 10" in README.md). Coarse; only catches a wrong equation.

**Planted eigenproblem, through the same code** (the same stepper, series start, inward flow, determinant and Newton, only
the coefficient generator A is replaced): A_pl = ε(Ω − Ω*) e^{2εℓ} + s κ [F(E + κE²) + B E] with E = e^{−ℓ}, κ = 3/4,
Ω* = 5/2. At Ω = Ω* it has the exact solution Y* = exp(−κ(1 − e^{−ℓ})) (analytic at the throat, Y*(0) = 1; the other
solution grows like e^{(½+2ε)ℓ}), so the eigenvalue is exactly Ω*. D = 5, 50, 1000, 10⁴ (ε = 1/4 … 5e-5).
- **S1** the throat series at Ω*, summed at ℓ₀, against (Y*, w*)(ℓ₀): relative error ≤ 10^{−d_lane}.
- **S2** the inward flow from the exact (Y*, w*)(ℓ_∞) to ℓ₀ against (Y*, w*)(ℓ₀): ≤ 10^{−d_lane} (stepper alone).
- **S3** the contraction: the flow from (1, 1) at ℓ_∞ reaches (Y*, w*)(ℓ₀) in direction to 10^{−d_lane}.
- **S4** Newton from Ω* + 0.3 and from Ω* − 0.4 gives |Ω − Ω*| ≤ 10^{−d_lane}·|Ω*| in each lane (f64, dd, qd, od)
  at each of the four D.
- **S5** the contraction's own bound: the eigenvalue from a shorter ℓ_∞ (T′ = T/2 + 20, in dd, qd, od) satisfies
  |Ω(T′) − Ω*| ≤ 100·e^{−T′}·|Ω*| + 10^{−d_lane}·|Ω*|, and the control `short_contraction` (T/4) violates it.

**Reproduction.**
- **G1** growth.csv: every row (D = 4 … 11, 20, 30, 50, 100, 200, 500, 1000, 2000), qd lane, |W²a² − csv| ≤ 5e-13
  (half a unit of the printed 12th decimal). Reported per row; a row that fails is reported with its difference.
  The `modes_r.py` rows of growth.csv are known to move by 4e-10 … 5e-6 under changes of its numerical parameters
  (`logs_modes_r.txt`), so failures there are expected and are a result, not an error to remove.
- **L1** lane agreement, D list below: |W²_qd − W²_od| ≤ 1e-30·W² at every D. The digit count printed for each D is
  −log10 of that relative difference.

**D list of record** (64 values, D_j = round(50·200^{j/63}), j = 0 … 63, all distinct):
50, 54, 59, 64, 70, 76, 83, 90, 98, 107, 116, 126, 137, 149, 162, 177, 192, 209, 227, 247, 269, 292, 318, 346, 376,
409, 445, 484, 527, 573, 623, 678, 737, 802, 873, 949, 1032, 1123, 1221, 1329, 1445, 1572, 1710, 1860, 2023, 2201,
2394, 2604, 2832, 3081, 3351, 3645, 3965, 4313, 4691, 5103, 5550, 6037, 6567, 7143, 7770, 8452, 9193, 10000.

**Fit.** Data: the qd values of the D list, g_j = W²_j − 2(D_j − 3) + 4 ln 2 (ln 2 to 70 digits). Model M1:
g/ε = Σ_{k=1}^{K} Ω_k ε^{k−1}, least squares by QR in mpmath at 300 digits, unweighted in g/ε (a relative weight on the
leading term). Cells: K ∈ {10, 12, 14, 16, 18, 20, 24} × window D ≥ D_lo, D_lo ∈ {50, 100, 200, 500}, a cell kept when
it has at least K + 4 points. **Gate:** a cell is admitted when its largest relative residual max_j |res_j|/|g_j| is at
most 100·max(δ_data, 1e-60), where δ_data = max_j |W²_qd − W²_od|/|g_j| over the D list (the lanes' disagreement,
step 3). **Headline** Ω_k = the median over admitted cells, **error bar** = (max − min) over admitted cells: a spread
over fit choices, an estimator range, not a bound. If M1 admits no cell, model M2 is tried:
g/ε = Σ_{k=1}^{K} Ω_k ε^{k−1} + Σ_{k=3}^{K} Λ_k ε^{k−1} ln ε, K ∈ {8, 10, 12, 14}, same windows and gate; the logs, if
needed, are a finding.
- **F1** planted fit: synthetic g from Ω_k = A (k+1)! c^k (A, c from Ω₁ = 10.4233603787385, Ω₂ = 73; the series
  truncated at its smallest term) on the D list, relative noise 1e-40 (uniform, fixed seed): ≥ 3 admitted cells,
  |Ω₁ − truth| ≤ 1e-15, |Ω₂ − truth| ≤ 1e-16·|Ω₂|, and the truth inside the cells' range for both.
- **F2** planted fit with a model error: F1's data plus 0.5 ε³ ln ε (relative to g/ε: 0.5 ε² ln ε): M1 admits no cell,
  M2 admits at least one cell and recovers the planted Ω₂ to 1e-10·|Ω₂|.
- **F3** the fit of record, on the qd values. **Ω₁:** admitted cells exist, the range ≤ 1e-12, and
  |Ω₁ − (2π²/3 + 8 ln²2)| ≤ 1e-12 and ≤ 3 × range (else the mismatch is reported). **Ω₂:** the range ≤ 1e-16·|Ω₂|
  (16 significant digits); the digits reached are reported whether or not this holds.

**PSLQ** (mpmath, `mp.pslq(..., tol=τ, maxcoeff=H, maxsteps=10⁶)`, precision 60 digits, the input the fit's headline).
A relation is called found only if its coefficient vector is a multiple of the expected one (Ω₁) or has max |coeff| ≤ H,
holds at τ and at 10τ, the **budget** n·log10(2H + 1) + 1 < −log10(τ/|Ω|) is met (else *inconclusive*, never *found*),
and the perturbed-basis control fails.
- **P1** Ω₁ in {Ω₁, π², ln²2}, τ = 1e-11, H = 100: expected 3Ω₁ − 2π² − 24 ln²2 = 0, i.e. (3, −2, −24).
  Control P1c: ln²2 replaced by ln²2 + 1e-3: no relation with |coeff| ≤ 100 at τ.
- **P2** Ω₂ in the weight-3 basis {Ω₂, ζ(3), π² ln 2, ln³ 2}, τ = 1e-13, H = 1000 (budget 13.2 digits against 14.9).
  Control P2c: ζ(3) replaced by ζ(3) + 1e-3.
- **P3** Ω₂ in {Ω₂, ζ(3), π² ln 2, ln³ 2, π², ln² 2, ln 2, 1}, τ = 10 × F3's range of Ω₂, H = 100 (budget
  8·log10 201 + 1 = 19.4 digits: *inconclusive* unless the fit has more). Control P3c as P2c.
- A relation that is not found is reported as not found.

## Controls (`--mutate=NAME` of the crate or the driver)

Each check has one; its **targets** (the checks it must fail) are computed in a development run and entered in
Amendment A1 before the first run of record. Declared names: `wrong_eps` (ε off by 1e-6 relative in A), `wrong_B` (the ½e^{−ℓ} term
of B dropped), `wrong_A_sign` (the ½e^{−ℓ} term of A with the wrong sign), `recip_f64` (1/k constants rounded from f64),
`short_series` (series order halved), `short_contraction` (T/4), `step_loose` (tol 1e-10 in every lane), `wrong_planted`
(κ off by 1e-3 in A_pl only), `fit_wrong_eps` (ε = 1/(D−3) in the fit), `fit_drop_term` (K−4 terms), `pslq_wrong_basis`
(P1c, P2c, P3c), `csv_shift` (growth.csv's D=4 value + 1e-9).

## Runs

Every run longer than a few minutes is a systemd user unit `nm-i195-<name>`, `nice -n 10`, at most 4 threads in total;
a run not finished in 2 h is stopped and reported with what finished. Memory is reported only (`/usr/bin/time -v`).
Timings are reported with the machine, load and thread count.

## Amendments

**A1, 2026-11-26 (development runs dev_00, dev_03 to dev_09): the planted construction.** Before this, `dev_00` (synthetic
data only, no real data) showed that a 64-point fit of data good to 1e-60 reaches Ω₂ to about 1e-29 for D_lo ≥ 500; the
targets above were set from it. The first planted system (Y* = exp(−κ(1 − e^{−ℓ})), κ = 3/4, with the Ω term weighted
by e^{2εℓ}) was wrong as a test, not as a method:
- S1 failed in every lane (series error 1e-6 f64, 2e-18 dd, 2e-41 qd at the declared series orders, `dev_03_*`). The
  recursion is right: its coefficients equal Y*'s Taylor coefficients to 1e-63 (`dev_09`), but Y*'s own coefficients fall
  only by about 0.35 per order (c₆₀ = 6e-25), so the orders chosen for the real problem (radius 2π) cannot sum it.
- S3 failed at small D (−4.9 in dd at D = 5): the planted system has no e^{2εℓ} term at Ω*, so the contraction rule
  σ(ℓ) = √(¼ + 4ε(1 + εΩ)e^{2εℓ}) of the real system overstates its contraction.
- the e^{2εℓ} weight on the Ω term makes the Newton iterates off Ω* overflow at small D.
- `dev_03_planted_od` was stopped by me after 3.5 min (exit 143); its log is empty.

**New construction** (code: `sys.rs`): Y* = 1/(1 + κF), κ = min(ε, 10⁻³) (radius of convergence at the throat
ln(1 + 1/κ) ≥ 6.9 > 2π, and w*(0) = −sκ = O(1) as in the real mode), A_pl = ε(Ω − Ω*) + sκ u [F(1 + 2κu) + B] with
u = E/(1 + κF) (the Ω term is a constant shift), ℓ_∞ from σ = ½ (the planted system's own exponent gap). Ω* = 5/2 as
before. **The thresholds of S1 to S5, the D values, lanes, orders and tolerances are unchanged.** With it (`dev_06`,
D = 5, 50, 1000, 10⁴; log10 of the relative error): S1, S2, S3 meet the stated digits in f64 (−14.7 or better), dd (−30.9
or better) and qd (−63 or better). Three declared criteria do not hold, and are reported to the coordinator, not changed:
- **S4 at large D.** The noise floor of Ω grows like s = 2(D−3): Ω relative error, D = 1000 and 10⁴: f64 −10.6, −9.0
  (stated 11); dd −26.8, −25.2 (stated 27); qd −59.1, −57.5 (stated 56, met). Expressed against W² (= s + Ω) instead of Ω
  these are f64 3e-14 and 1e-13, dd 2e-30 and 8e-30, qd 4e-62: all within the stated digits.
- **S4 second start (Ω* − 0.4) at D = 5** converges to another root (relative error 0.2, 60 iterations, in every lane;
  Ω* − 0.1 and Ω* − 0.3 do the same, `dev_07`); at D = 6, 8, 20 it reaches Ω*. From above (+0.1, +0.2, +0.3) it reaches
  Ω* at every D tried.
- **S5** (the contraction bound 100 e^{−T′} + 10^{−d}) holds at D = 5, 50 and fails at D = 1000 and 10⁴ in qd (−39.2, −37.2
  against −41.9): the contraction's error in Ω is amplified by about s² (the other solution's w is s times its Y).
