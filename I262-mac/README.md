# I262-mac: the c = −1 black universe's growing mode in closed form, and the slope dW/dc through c = −1

Machine: the coordinator's Mac (Apple M5, macOS, shared with other agents), `~/Source/negative-mass/.venv/bin/python` (numpy 2.5.4, scipy 1.18.1, sympy 1.14.0,
mpmath 1.3.0), `nice -n 10`, one thread per process, at most two processes. Code: `notes/black_universe/cminus1_mode.py` in worktree `~/Source/negative-mass-i262`,
branch `wip/i262-cminus1-mode` on main 818e14f; #212's `stability.py` is imported, not modified. Issue: https://github.com/nmoinvaz/negative-mass/issues/262
(depends on #248, #212). Written 2026-11-27 before the runs of record. Every development log is in `dev/` (scripts `dev*.py`, logs `dev*.log`; the mutation
development runs are `dev/runs_dev/dev15_*`).

## Question

#212's master equation for Y = δR (gauge δφ = 0), time dependence e^{Wt}, member c of the family (b = 1, K = −2c/π = 3m):

```
Y'' = (2/ρ − A'/A) Y' + (1/R⁴ − A'/(AρR²) − 2/(AR²) + W²/A²) Y,     A = 1 + cR² + K(ρ + R² arctan ρ),   R² = 1 + ρ²,   x = ∫dρ/A.
```

At c = −1 (K = κ = 2/π), W = κ: (1) is there a closed form for Y_ref, the solution with Y ∼ ρ^{1/2} (#248 D7: no logarithm, g₂ = π²/128 + 5/12 for g₁ = 0)? (2) What is
d(W/κ)/dc at c = −1, where #212's rates give W/κ − 1 ≈ 0.31(c + 1)?

## What development found, in the order it happened (this is not a search over the declared classes)

1. `dev01*`: the Frobenius series exact in K. For W = wK the exponents are 1 ∓ w/2 and g₁(w) = −w/(4K) is analytic through w = 1. At w = 1 g₁ is the free
   resonance coefficient (the ρ^{3/2} solution Y_b may be added): g₂ = (40K² + 24K g₁ + 3)/(96K²). g₁ = 0 gives #248's π²/128 + 5/12. Y_nat denotes
   g₁ = −1/(4K) = −π/8 (the continuation in w, g₂ = 5/12 − π²/128). `dev02`–`dev05`: a 40–50 digit Taylor-step integrator of the equation, the three solutions to ρ = 100,
   and β* = −Y_nat/Y_b → −0.19991708252087078 (the admixture, Y_∞ = Y_nat + β* Y_b decays at +∞).
2. `dev06`, `dev13`: #212's W(c) at c = −1 ± {1e-2, 3e-3, 1e-3, 3e-4, 1e-4} (R1 and R2). Fit W/κ − 1 = s₁(c+1) + s₂(c+1)²: s₁ = 0.314038 (R2), third order 0.314029.
   **Noticed numerically**: s₁ ≈ −(π/2)β*. It was derived afterwards (item 6).
3. `dev07`, run as an **obstruction test** (is the formal series of Y = e^{±κx}ρΣc_nρ^{−n} at ρ = +∞ convergent?), before any closed form was known: the e^{+κx} series
   came out as 1, 0, 1/2, 0, −1/8, 0, 1/16, … , the expansion of √(1 + ρ²) = R. The e^{−κx} series diverges (|c_{n+1}/c_n| ≈ 0.8n). This is how the closed form
   Y_ref = R e^{κx} was found. `dev08`: sympy: the residual of Y = R e^{Wx} is ∝ (πW + 2c), so zero at W = −2c/π = K for **every** c. `dev09`: against the ODE integration on
   ρ ∈ [−40, 40], 4e-42; mutants 5e-4 to 3.
4. `dev10`: the first-order monodromy of the equation about (c, W) = (−1, κ), by residues at ρ = 0, exact in π: J_aa = iπ κ̇/κ = −J_bb, J_ba = 0, J_ab = −iπ².
   `dev11`: I₀ = ∫₀^∞ 2Kρ² e^{−2κx}/(AR²) dρ = 1.0149036099284088921…; β* = π/4 − 1/I₀ agrees with the shooting value to 5.7e-41.
5. Resulting formulas: d(W/κ)/dc = J_ab β*/(2πi) = −(π/2)β* = π/(2I₀) − π²/8 = 0.3140290188873360539…, dW/dc = 1/I₀ − 2/π = 0.3486954735507377474…
6. No PSLQ was run on any of these numbers before the basis below was declared.

## Declared before the runs of record

### Ansatz class (acceptance 1)

𝒦 = { Y = e^{kκx} A^s F : k ∈ ℤ, s ∈ ½ℤ, F ∈ ℂ(ρ, R, arctan ρ) } (rational functions of ρ, R = √(1+ρ²) and T = arctan ρ; A is linear in T, so A^s with s ∈ ℤ is included in F).
It contains the issue's example (polynomials in ρ times powers of R, times T to degree ≤ 2, times e^{±κx}, times A^s). Classification, not search: every member of 𝒦 has, at
ρ → +∞ on the real axis, an expansion e^{kκx} ρ^p Σ c_n ρ^{−n}, convergent for large ρ (ρ, R, T = π/2 − arctan(1/ρ) and A = 1 − 4/(3πρ) + … are analytic in 1/ρ). The
equation has exactly two formal solutions at +∞, e^{±κx} ρ Σ c_n^± ρ^{−n} (p = 1, unique up to scale; N3). A solution in 𝒦 is therefore a multiple of one of them, and
is in 𝒦 only if its series converges: k = +1 gives Φ = R (N3), k = −1 diverges (N3). So 𝒦 ∩ {solutions} = ℂ·R e^{κx}, if N3 passes. The convergence claim for k = −1 is a ratio test
at n = 100: *numerical evidence*. The solution decaying at +∞ and the one with Y ∼ ρ^{3/2} are quadratures of Y_ref (Y_b = Y_ref ∫₀^ρ 2Kρ'²e^{−2κx}/(AR²)dρ'), not members of 𝒦.

### Criteria (each can fail; bars in the script's check texts)

| id | what | bar |
|---|---|---|
| S1 | Y = R^{pw}e^{Wx} in the Y equation for symbolic c: residual ∝ (πW + 2c), zero at W = K | exact (sympy) |
| S2 | c = 0: Y_K = R equals the variation of the throat radius b in the gauge δφ = 0 | exact |
| S3 | J (above), exact entries from residues, series to order 8 | exact |
| S4 | the line J predicts for the ingoing solution at W = K(c) is Y_ref (v_b/v_a = π/4) | exact |
| N0 | the equation as coded equals #212's `coef_x` at 6 points | 1e-12 |
| N1 | closed form against the Frobenius series (g₁ = π/8, 90 terms, 60 digits) at ρ = ±0.01, ±0.05, ±0.1 | 1e-30 |
| N2 | closed form against the integration of the master equation at W = κ on ρ = ±0.3 … ±40 (45 digits) | 1e-20 |
| N3 | formal series at +∞: e^{+κx} one equals R's (120 terms, 300 digits); e^{−κx} one diverges (ratio/n at n = 100 within 5% of π/4) | 1e-40; 5% |
| N4 | β* by shooting (ρ = 100) against π/4 − 1/I₀ by quadrature | 1e-30 |
| N5 | derived d(W/κ)/dc against the fit of W/κ − 1 = s₁ε + s₂ε² to #212's R2 rates at c = −1 ± 1e-2, 1e-3, 1e-4 | 1e-3 |
| N6 | 1/I₀ − 2/π against the central difference of #212's W at c = −1 ± 1e-4 | 1e-4 |
| N7 | PSLQ recovers a planted number and returns none for a control (both bases) | exact relation |
| N8 | planted: synthetic W/κ − 1 = s₁ε + s₂ε² + s₃ε³ with noise 1e-10 through the same fit recovers s₁ | 1e-3 |

A failed criterion is reported as not met. No bar is changed after seeing data.

### Mutations (effects computed in development, `dev/runs_dev/dev15_*`, before they were declared)

| name | what is changed | fires | effect in development (`dev/runs_dev/dev15_*`) |
|---|---|---|---|
| `sym_pw` | S1 with Y = R^{1.01} e^{Wx} | S1 | the residual at W = K is a nonzero function of ρ and c |
| `sym_gauge` | S2 with the gauge factor ρR/2 instead of ρR/√2 | S2 | Y = (√2ρ² + 2)/(2R), not R |
| `j_sign` | B₁ → −B₁ (the perturbing operator) | S3, S4, N5 | J_ab = +iπ²; S4 predicts v_b/v_a = −π/4 against π/4; derived slope −0.314029 against the fit +0.314038 (relative difference 2.0) |
| `j_g1` | J in the basis Y_a with g₁ = 0 | S3 | J_ba = iπ²(16 − π²)/64 ≠ 0, J_aa = −iπ; J_ab is unchanged, so S4 and N5 do not fire |
| `eq_P` | the sign of A′/A in P (the equation of N0 and the integrator) | N0, N2, N4 | N0 1.9; N2 1.0; N4 7.8 (relative differences) |
| `cf_R2` | R² → 1 + 1.01ρ² in the closed form | N1, N2 | N1 4.95e-5; N2 4.98e-3 |
| `cf_k` | e^{1.01κx} in the closed form | N1, N2 | N1 2.3e-2; N2 0.30 |
| `cf_xsign` | e^{−κx} in the closed form | N1, N2 | N1 99.8; N2 3.2 |
| `inf_P` | the sign of the 2εK/A term of the formal series at +∞ | N3 | the e^{+κx} series differs from R's by 5.9e182 at order 120 |
| `beta_g1` | shooting started from Y_a with g₁ = 0 | N4 | relative difference to the quadrature value 1.96 |
| `s_g1` | the slope formula with β* in the g₁ = 0 basis | N5 | derived 0.930879 against the fit 0.314038 (2.0) |
| `s_kappa` | dκ/dc dropped (d(W)/dc/κ instead of d(W/κ)/dc) | N5 | derived 0.547730 (0.74) |
| `dwdc_K` | dW/dc = 1/I₀ without −2/π | N6 | 0.985315 against the central difference 0.348695 (1.8) |
| `pslq_plant` | the planted number shifted by 1e-20 | N7 | no relation at tolerance 1e-33 (planted: None) |
| `fit_eps` | ε → −ε in the least-squares fit | N5, N8 | fitted slope −0.31404, relative difference 2.0 in both |

The declared fired sets are the "fires" column; the run of record of a mutation is `derive` for `sym_pw`, `sym_gauge`; `check` for `eq_P`, `cf_R2`, `cf_k`, `cf_xsign`, `inf_P`, `beta_g1`, `s_g1`,
`s_kappa`, `dwdc_K`, `pslq_plant`, `fit_eps`; and both for `j_sign`, `j_g1` (the fired set is the union). The development runs reproduced these sets; the `j_g1` set was first declared
in the script as {S3, S4, N5} and corrected to {S3} after its development run (J_ab does not depend on g₁), before this README.

### PSLQ (declared before the run on the real numbers)

50 digits, tolerance 1e-33, max coefficient 1000. Targets: τ = 1/I₀ = dW/dc + 2/π and s = d(W/κ)/dc. Bases (each with the target as the first entry):
B1 = {1, π, π², π³, 1/π, 1/π²}; B2 = {1, π, π², 1/π, ln 2, ln π, Catalan G, γ}. A relation counts as an identification only if every coefficient is at most 1000 in absolute
value and the residual is below the tolerance; it would still be *numerical evidence* until substituted and checked. Planted (3/2 − 5π/3 + 2π² in B1) and control (e^{1/3} + √2, both bases) are in N7.
There is no reason to expect τ to be in either span: I₀ is an integral of the Kruskal function ρ(Π).

### Runs

`cminus1_mode.py derive` (about 1 min), `check` (about 3 min), `table` (about 3 min), and the mutation runs above (15 mutations); one process each, nice 10, at most two at a time, logs
in `runs/`. A single run not finished in 2 h of wall time is stopped and reported. Memory is only reported. The output of record, `notes/black_universe/cminus1_mode_output.txt`, is
`derive`, `check`, `table`, `mutations` of these runs, in that order.

## Runs of record (2026-11-27, after the criteria commit be43bc1c)

Code `cminus1_mode.py` at 2f0eea2, the commit made after the development runs. The script was edited while the development mutation runs went on (N8 and `fit_eps` added, the `j_g1` set
corrected, two lines added to `table`), so the early development runs did not contain N8; the runs of record are the first runs of the committed script. `runs/run_all.sh`: two workers, nice 10, one process each. Exit codes: `derive` 0, `check` 0,
`table` 0; every mutation run 1 (its declared checks fail). No run was stopped; none was rerun.

| run | result |
|---|---|
| `derive` (51 s) | 4 of 4 pass: S1 (residual ∝ πW + 2c, zero at W = K), S2, S3 (J exact), S4 (the ingoing line at W = K(c) is Y_ref) |
| `check` (128 s) | 9 of 9 pass: N0 3.2e-15, N1 5.9e-61, N2 4.3e-42, N3 1.9e-122 and ratio/n 0.797, N4 1.1e-41, N5 2.9e-5 (second order) and 2.7e-8 (third), N6 2.7e-8, N7, N8 |
| `table` | I₀ = 1.0149036099284089, β* = −0.19991708252087078, dW/dc = 0.34869547355073775, d(W/κ)/dc = 0.31402901888733605; fits R2 s₁ = 0.31403797 (second order), 0.31402903 (third); PSLQ: no relation for 1/I₀ or the slope in B1 or B2 |
| `mut_<name>` (15) | fired sets equal the declared ones, 15 of 15 (`cminus1_mode.py mutations runs mut_`) |

Criteria met: S1–S4, N0–N8 all pass; the mutations fire as declared; no bar changed. Not met: the slope and I₀ are not identified in closed form (PSLQ found none in the declared bases).
The output of record is `notes/black_universe/cminus1_mode_output.txt` (commit 43d0d08), assembled from `runs/`.
