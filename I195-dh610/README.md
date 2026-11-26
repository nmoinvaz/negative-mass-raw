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

**A2, 2026-11-26 (the coordinator's rulings on dev_06 to dev_22; development runs dev_10 to dev_24; written before any run
of record; code at commit 5ad351a of branch `wip/i195-w2-largeD`).** The coordinator confirmed the convention (the issue body
is corrected) and accepted A1. The rulings:

*Planted checks, as ruled.*
- **S4 stays as worded** (|Ω − Ω*| ≤ 10^−d_lane |Ω*|, both starts, each lane, each D). It is reported NOT MET where it fails.
  Development (dev_24): 14 of 24 cases; not met in f64 and dd at D = 1000 and 10⁴, and for the start Ω* − 0.4 at D = 5 in
  f64, dd and qd. The fit uses qd, where S4 as worded is met at every case but that D = 5 start.
- **S4w, added after dev_06 by the coordinator's ruling:** |W² − W²*| ≤ 10^−d_lane · W²* with W²* = s + Ω*, both starts,
  each lane, each D. A-priori reason: Ω enters A only through εΩ, so the condition number of Ω is about 1/ε = s, and a
  precision of 10^−d in W² is a precision of s·10^−d in Ω. Development: 21 of 24, failing only at the D = 5 start below Ω*.
- **S4's start Ω* − 0.4 at D = 5 stays as declared and is reported NOT MET.** What it reaches (dev_10 to dev_13, planted, D = 5):
  it reaches no root in dd and qd. Newton walks down the positive, flat M(Ω) (M and M′ both near 0.5 to 9 in units of the
  vectors' size) by about 0.09 per step: after 60 iterations Ω = −1.2616 in dd (|M| = 10^−0.9 of the vectors' size) and
  −0.2100 in qd (10^−0.3). In f64 it stops at Ω = −1.5041 (|M| = 10^−16, "converged"). The scan of M (dev_12, dev_13) shows
  why: M > 0 on (−1.5, 2.5) with its one zero at Ω*, and for Ω below −1.5 M oscillates with a zero every 0.025 to 0.05 while
  the node count of Y rises from 0 (Ω ≥ −1.5) to 2, 3, … 7 at −1.525, −1.55, … −1.8 and 22 at −4. Those zeros are the planted
  system's further eigenvalues, with nodes in their eigenfunctions; f64's Ω = −1.5041 lies between the node counts 2 (at
  −1.525) and 0 (at −1.5), so it is one of them (the counter reads Y at the flow's step ends, so it can skip a node). At
  D = 6 the same start also fails (Ω = −3.509 in dd and f64); it reaches Ω* at D = 8 and 11 (f64, dev_11) (erratum A2.1: A2 first said D = 6, 8, 20,
  which was wrong for D = 6 at the −0.4 start; D = 6 reached Ω* from −0.1, dev_07). If the real problem's start rule (±0.5 in Ω, check R4 below) can reach
  another root at D ≤ 11, the note says so.
- **S5 stays as worded** and is reported NOT MET where it fails: dev_24 6 of 12, failing in f64, dd and qd at D = 1000 and 10⁴.
- **S5s, added after dev_06 by the coordinator's ruling:** the same test with the bound 100·s²·e^−T′ + 10^−d_lane in place of
  100·e^−T′ + 10^−d_lane (dd, qd, od). Reason: one factor s from Ω's conditioning (as S4w) and one from the other solution,
  whose w = s dY/dℓ is of order s·Y, so its w/Y ratio is s times the decaying one's. The bound uses the declared T (a control that shortens
  T does not shorten the bound). Development: 8 of 8 in dd and qd (dev_24); od at D = 50 and 10⁴ (dev_08): −77.2 and −69.5
  against −70.7 and −66.0.
- **`short_contraction` (T/4) and S5s.** It violates S5s in 7 of the 8 dd and qd cases (dd D = 50, 1000, 10⁴; qd D = 5, 50,
  1000, 10⁴) and is **silent at dd D = 5**: −27.33 against −27.0 (dev_19, dev_20; T/8 would fire there, −22.56). The
  coordinator ruled: keep T/4, declare the 7 cells as the S5s target (`CASE_TARGETS` in the driver), report dd D = 5 as silent.

*Added checks.*
- **R4** (the "±0.5" sentence of the README's Eigenvalue paragraph made a check): Newton on the real system from the start
  shifted by −0.5 and by +0.5, qd, at D = 4 … 11, 50, 1000, must reach the same root as the unshifted start to 1e-50
  (relative, digits shared by the two W² strings). Reports where a shifted start goes if it does not.
- **O2** (not in the README's list; the bar was written in the driver before its first run, dev_14): the throat series at
  l = 1 for the real system with Ω = Ω₀ + Ω₁ε + Ω₂ε² against the closed forms Y₀ + εY₁ + ε²Y₂ of README.md (Y₁ = −l, Y₂ =
  −2Ω₀ l − (3/2) l²), qd, D = 1000 and 10⁴: |difference| ≤ 100 ε³. Development: −9.85 ε³ and −9.76 ε³.
- **G1** is unchanged (±5e-13 per row, reported per row, expected to fail). Added, as reported comparison and not a gate (ruling
  1): for each row D = 20 … 2000 the csv value, `logs_modes_r.txt`'s tighter run (X 50, ρ₀/10, rtol 1e-13; not rerun) and the
  crate's, and the fraction of the csv-to-crate gap the tighter run closes. Development: 0 of 16 rows within 5e-13; the tighter
  run moves toward the crate's value at all 8 rows, by 0.42 (D = 20) to 0.84 (D = 2000) of the gap. The comparator passes the
  crate's own values printed to 12 decimals (so the failures are the csv's).
- **F3 stays as declared; F3k, added after dev_21 by the coordinator's ruling and after seeing the residuals plateau at
  K ≥ 20:** M1's grid with K = 28 and 32 added (K ∈ {10, 12, 14, 16, 18, 20, 24, 28, 32}); the gate, windows, K + 4 rule, tolerances,
  headline rule (median and range over admitted cells) and the criteria are F3's. F3 and F3k are reported side by side and the
  headline Ω₁ and Ω₂ (and the PSLQ inputs) come from F3k. **The grid of F3k was extended after a development run.**
  Development (dev_22, with the lanes' measured disagreement δ_data = 2.97e-54, gate 2.97e-52): F3 admits one cell (D_lo 500,
  K 24, residual 2.9e-54), so its range is 0 and its clause "|Ω₁ − closed form| ≤ 3 × range" cannot hold: F3 is NOT MET, a defect
  of the criterion's wording and not of the data, the difference from 2π²/3 + 8 ln²2 being 5.1e-49. F3k admits 6 cells; its
  Ω₁ − closed form is 8.0e-50 against a range of 1.7e-45, and Ω₂'s range is 3.2e-40 (41 digits).
- **PSLQ (P1, P2, P3) exactly as declared.** Development (dev_22): P1 finds (3, −2, −24) (residual 2.4e-49); P2 finds
  (3, −240, 8, 32) (residual 2.7e-44; budget 14.2 digits needed against the 14.9 the declared τ gives, and 40 digits in the
  fit); P3 at its declared H = 100 does not find the same relation (its coefficient 240 exceeds H). An identification.

*Controls: targets computed in development runs* (a target is a check that passes without the control and fails with it;
"n/N" is the cases of the check that meet it; dev_24 for the baseline row, dev_19 for the others; F3k, P1, P2, P3 in dev_23):

| control | E0 | S1 | S2 | S3 | S4 | S4w | S5 | S5s | O2 | M1 | F1 | F2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| none (baseline, dev_24) | PASS | 12/12 | 12/12 | 12/12 | 14/24 | 21/24 | 6/12 | 8/8 | PASS | PASS | PASS | PASS |
| `wrong_eps` | PASS | 12/12 | 12/12 | 12/12 | 14/24 | 21/24 | 6/12 | 8/8 | PASS | PASS | PASS | PASS |
| `wrong_B` | FAIL | 0/12 | 0/12 | 0/12 | 0/24 | 0/24 | 0/12 | 0/8 | FAIL | FAIL | PASS | PASS |
| `wrong_A_sign` | FAIL | 12/12 | 12/12 | 12/12 | 14/24 | 21/24 | 6/12 | 8/8 | FAIL | FAIL | PASS | PASS |
| `recip_f64` | PASS | 4/12 | 4/12 | 4/12 | 3/24 | 7/24 | 2/12 | 0/8 | PASS | PASS | PASS | PASS |
| `short_series` | PASS | 0/12 | 12/12 | 12/12 | 0/24 | 0/24 | 0/12 | 1/8 | PASS | PASS | PASS | PASS |
| `short_contraction` | PASS | 12/12 | 12/12 | 0/12 | 2/24 | 2/24 | 2/12 | 1/8 | PASS | PASS | PASS | PASS |
| `step_loose` | PASS | 12/12 | 4/12 | 4/12 | 1/24 | 3/24 | 1/12 | 0/8 | PASS | PASS | PASS | PASS |
| `wrong_planted` | PASS | 0/12 | 0/12 | 0/12 | 16/24 | 21/24 | 6/12 | 8/8 | PASS | PASS | PASS | PASS |
| `fit_wrong_eps` | PASS | 12/12 | 12/12 | 12/12 | 14/24 | 21/24 | 6/12 | 8/8 | PASS | PASS | FAIL | FAIL |
| `fit_drop_term` | PASS | 12/12 | 12/12 | 12/12 | 14/24 | 21/24 | 6/12 | 8/8 | PASS | PASS | FAIL | FAIL |

| control | F3k (dev_23) | P1 | P2 | declared targets |
|---|---|---|---|---|
| `wrong_eps` | FAIL (no cell admitted) | - | - | F3k only: the planted system's Ω term is zero at Ω*, so S1 to S3 and O2 do not see ε in A |
| `wrong_B` | FAIL | - | - | E0, S1, S2, S3, S5s, O2, M1, F3k |
| `wrong_A_sign` | FAIL | - | - | E0, O2, M1, F3k (the planted A replaces the real one, so S1 to S3 are blind to it) |
| `recip_f64` | FAIL | - | - | S1, S2, S3, S5s, F3k |
| `short_series` | FAIL | - | - | S1, S5s, F3k |
| `short_contraction` | FAIL | - | - | S3, S5s (the 7 cells), F3k |
| `step_loose` | FAIL | - | - | S2, S3, S5s, F3k |
| `wrong_planted` | not run | - | - | S1, S2, S3 |
| `fit_wrong_eps` | FAIL (Ω₁ = 20.85) | FAIL | still finds a relation, 4× scaled | F1, F2, F3k, P1 |
| `fit_drop_term` | **silent**: 3 of 6 cells still admitted | passes | passes | F1, F2 (F3k's silence is a result: dropping 4 terms leaves the K = 28 and 32 cells enough) |
| `pslq_wrong_basis` | passes | FAIL | flips from found to not found (status unchanged) | P1 (P2's flip reported; P3 not found with or without it) |

`csv_shift` is dropped: G1 fails on 16 of 16 rows of the unmodified csv, so it cannot be shown to fail again; the comparator's
self-test above replaces it. S4, S4w, S5 and F3 are not targets of any control, because they fail without one by the rulings.

*Code since the README's description* (commit 5ad351a): `scan` (M(Ω) on a grid), `--shift` (R4), a node counter, the planted
S4 diagnostics (`S4om`, `S4M`, `S4nodes`, `S4btrace`), the declared T in S5's bound, and a `kt_ms` field that prints
multishoot's `Plan::optimal_kt` at the lane's tolerance (dd: 45 against the crate's order 48) as a cross-check of the order.
multishoot's and multisolver's other code is not called by the crate (see the note).

## Runs of record (2026-11-26, dh610-fedora, 20 cores shared with choptuik-large-d)

Written after A2 was committed (raw 91537ed). Crate at commit 5ad351a (binary built from it, `cargo build --release -j 2`), driver
as named. Each single-thread process under `nice -n 10`; at most 4 processes at once (the planted od runs and od D-list parts ran
together with load average 9 to 14 from other users' work); memory reported only (`/usr/bin/time -v`, `.time` files). The
exit codes of 1 are the driver's: it exits 1 when a check fails, and S4, S4w, S5, F3, G1 and R4 do (see the note).

| run | what | start | load average (1, 5, 15 min) | wall | peak RSS (MiB) | exit |
|---|---|---|---|---|---|---|
| `run_01_planted_dd` | planted, dd | 14:16:13 | 13.80, 14.27, 13.25 | 0:03.00 | 3.5 | 0 |
| `run_01_planted_f64` | planted S1-S5, f64, D = 5, 50, 1000, 10^4 | 14:16:13 | 13.80, 14.27, 13.25 | 0:00.02 | 3.6 | 0 |
| `run_01_planted_od_D1000_10000` | planted, od, D = 1000, 10^4 (unit nm-i195-run01-od-D1000-10000) | 14:16:13 | 13.80, 14.27, 13.25 | 20:38.05 | 3.6 | 0 |
| `run_01_planted_od_D5_50` | planted, od, D = 5, 50 (unit nm-i195-run01-od-D5-50) | 14:16:13 | 13.80, 14.27, 13.25 | 27:10.08 | 3.4 | 0 |
| `run_01_planted_qd` | planted, qd | 14:16:16 | 13.80, 14.27, 13.25 | 1:19.71 | 3.5 | 0 |
| `run_02_w2_qd_growth` | W2 in qd at growth.csv's 16 D | 14:17:36 | 12.61, 13.89, 13.21 | 0:08.43 | 3.5 | 0 |
| `run_03_w2_qd_Dlist` | W2 in qd at the 64 D of the list (unit nm-i195-run01-qd-quick, as run_01 f64 to qd, run_02) | 14:17:45 | 12.36, 13.80, 13.18 | 0:50.36 | 3.5 | 0 |
| `run_04_w2_od_Dlist_p0` | W2 in od, D list index 0 mod 3 (unit nm-i195-run04-od-p0) | 14:16:13 | 13.80, 14.27, 13.25 | 16:51.51 | 3.4 | 0 |
| `run_04_w2_od_Dlist_p1` | od, index 1 mod 3 (unit nm-i195-run04-od-p1) | 14:18:42 | 12.69, 13.64, 13.16 | 18:35.77 | 3.3 | 0 |
| `run_04_w2_od_Dlist_p2` | od, index 2 mod 3 (unit nm-i195-run04-od-p2) | 14:33:12 | 9.18, 11.94, 13.34 | 23:18.55 | 3.6 | 0 |
| `run_05_driver_final` | the driver, code f620c48's predecessor 5ad351a (unit nm-i195-run05-driver) | 14:56:42 | 18.19, 18.43, 17.31 | 1:24.23 | 117.4 | 1 |
| `run_06_driver_final` | the driver, code f620c48 (unit nm-i195-run06-driver); same verdicts and numbers as run_05 | 14:58:52 | 19.69, 18.93, 17.65 | 1:37.83 | 116.6 | 1 |
| `run_07_driver_final` | the driver, code 69a9b96, with the Omega3, Omega4 and four-term remainder report: same verdicts as run_05 and run_06 (foreground, 74 s) | 15:00:50 | 18.54, 18.94, 17.82 | 1:14.04 | 116.5 | 1 |
| `run_08_driver_final` | the driver, code 4f022ee with the planted cases' digits table: **the output of record** (foreground) | 15:03:25 | 17.03, 17.76, 17.52 | 1:17.67 | 117.4 | 1 |

Cpu seconds inside the crate (sum of the `secs` fields): the qd D list 50.4 s (2106 Taylor steps, 1087 retries), the od D list
3525.8 s (2717 steps, 611 retries). `dev_25_pslq_omega3.*` is a development try, not a record: Omega3 = -652.8401075700561254352393037996
(range 2.7e-35 over the 6 cells) is not found in the pure weight-4 basis {pi^4, pi^2 ln^2 2, ln^4 2, zeta(3) ln 2, Li4(1/2)} at H = 10000 and
tau 1e-25 to 1e-33; the 13-element relation at weights <= 4 is spurious (its budget needs more digits than the fit has).
