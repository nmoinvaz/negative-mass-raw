# I151-rpi5: linear e-folding time of the asymmetric Ellis family at m/a = 1/2, against [GGS09a] Table I and [SN26] (#151)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, `nice -n 10`,
`OMP_NUM_THREADS=1`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/151
Worktree: `~/Source/negative-mass-i151`, branch `wip/i151-ellis-efold` (base main cde03d9). Code `notes/ellis_efold.py`, stdout
`notes/ellis_efold_output.txt`, note `notes/ellis_efold.md`. Python `~/Source/negative-mass-venv314/bin/python` (3.14.10, numpy
2.5.4, scipy 1.18.1, mpmath 1.3.0, sympy 1.14.0).

This README was written before the first run of the solver. Nothing in it was changed after a result was seen except where a
section is headed "Amendments".

## 1. Sources read (full TeX, in this folder)

| paper | arXiv version | file here | sha256 |
|---|---|---|---|
| [GGS09a] González, Guzmán, Sarbach, CQG 26, 015010 (2009) | 0806.0608 v2 (19 Nov 2008) | `src_ggs09a/phantom_lin.tex` (+ `.bbl`, `TimeScale.eps`, e-print) and `pdf/ggs09a_0806.0608.pdf` (12 pp) | tex `eaea3332…c10`, pdf `9bff9921…f75` |
| [SN26] Shirokov, Nachevsky, arXiv:2610.13206 | v2 (24 Oct 2026) | `src_sn26/research.tex`, `numbers.tex`, `research.bbl`, `00README.json` and `pdf/sn26_2610.13206.pdf` (23 pp) | research.tex `0ff0739f…d4d`, numbers.tex `1468824e…e0a`, pdf `5c1d7abd…21b` |

Only the files quoted are committed. [SN26]'s e-print (10 MB, with 12 videos) is not. Its sha256 is
`94e07907…7124`; [GGS09a]'s e-print is `294238b8…a86316c` (full values: `sha256sum` of the files named here, `curl -sL
https://arxiv.org/e-print/<id>`). Page numbers below are the arXiv PDF's. Equation numbers are the PDF's printed numbers. Both
papers are data. Neither addresses text to an AI agent.

## 2. Normalizations (formulas and sources)

**[GGS09a]** (b, γ₀, γ₁ constants of the family; t, x coordinates; K ≡ their κΦ₁² = −2(1+γ₁²)).
- Metric, Eq. (13), p. 3, with Eqs. (11)–(12): g = −e^{2γ₁ arctan(x/b)+2γ₀} dt² + e^{−2γ₁ arctan(x/b)−2γ₀}[dx² + (x²+b²) dΩ²].
- Parameters, p. 3–4: B := b e^{−γ₀}, γ₁ ≥ 0. Areal radius r = B √(1+(x/b)²) e^{−γ₁ arctan(x/b)}, minimum at x_throat = γ₁ b, with
  r_throat = B √(1+γ₁²) e^{−γ₁ arctan γ₁} (p. 4). ADM masses m_{+∞} = B γ₁ e^{−γ₁π/2}, m_{−∞} = −B γ₁ e^{+γ₁π/2} (p. 4). The
  p. 10 formula writes r_throat = b √(1+γ₁²) e^{−γ₁ arctan γ₁}: with the rescaling to b = 1, γ₀ = 0 used in §III B (p. 6) the two
  agree (B = b = 1); for b ≠ B the p. 4 form (with B) is the one used here.
- Rescaled units (p. 6): b = 1, γ₀ = 0, so g = −e^{2γ₁ arctan x} dt² + e^{−2γ₁ arctan x}[dx² + (1+x²)dΩ²]; ∂ := e^{2γ₁ arctan x}∂_x = ∂_ρ,
  ρ(x) = ∫₀ˣ e^{−2γ₁ arctan y} dy (p. 7).
- Master equation, Eq. (30) p. 6: χ_tt − ∂²χ + W(x)χ = 0, W = −V + 2(∂Ψ₀/Ψ₀)² (below Eq. (30)), W printed in Eq. (32) p. 7 with F = 1 +
  γ₁(1+γ₁ x) arctan x/(1+γ₁²). Unstable mode χ = e^{βt} χ₀(x), H χ₀ = −β² χ₀, H = −∂_ρ² + W (p. 7, §III C).
- **Time scale, p. 10:** τ = e^{γ₁ arctan γ₁} t is the **proper time at the throat** (with γ₀ = 0), and
  T := τ_unstable / r_throat = e^{2γ₁ arctan γ₁} / (√(1+γ₁²) β) = 1/(√(1+γ₁²) β̄), β̄ = e^{−2γ₁ arctan γ₁} β. Table I (p. 10) lists T
  for γ₁ = 0 … 10; T(0) = 0.846, T(0.5) = 0.758, T(∞) → 0.590.
- At γ₁ = 0, r_throat = b = 1 and T = 1/β.

**[Torii–Shinkai 2013, via notes/critical_ghost.md §1.1 and one_mode.py N4]**: ω²a² = −1.397 at n = 4 (the repo records 1.39705243 in
`notes/wormhole_largeD/one_mode.py`, N4); a = throat radius. At γ₁ = 0 this is β² with r_throat = 1: 1/√1.397 = 0.846 = T(0). The
paper [TS13] itself is not re-read here.

**[SN26]** (a throat scale, m mass parameter; t evolution time; isotropic r; G = c = 1; units of m).
- Eq. (2), p. 2: X = (r − a²/4r)/a, Ω = 1 + a²/4r², u = (m/a)(arctan X − π/2). Eq. (3), p. 2: α = e^u, γ_ij = e^{−2u} Ω² δ_ij, φ = C arctan X.
  Setting ρ_E = r − a²/4r (dρ_E = Ω dr; ρ_E² + a² = r²Ω²), g = −e^{2u} dt² + e^{−2u}[dρ_E² + (ρ_E²+a²) dΩ²].
- Throat, p. 2: minimal surface at X = m/a; R⋆ ≡ R_min = e^{−u(r_t)} √(a²+m²) = √(a²+m²) exp[(m/a) arctan(a/m)]; fiducial a = 2, m = 1:
  R⋆ = √5 e^{(1/2) arctan 2} = 3.8895. M_ADM = m (p. 2, "Here a is the throat scale and m the ADM mass").
- Time, §IV B p. 7: T ≡ τ α_th / R⋆ with α_th = e^{u(r_t)} = 0.575 the static lapse at the throat and τ the e-folding time in the evolution time t
  (α → 1 at X → +∞, so t is the proper time of the far (+) end). "Our drainhole is the γ₁ = m/a = 0.5 member of the static family of
  [GGS09a] (their metric with b = a, γ₀ = −πγ₁/2), for which their linear analysis gives T = 0.758. We solved the linearised field
  equations of this solution ourselves, with their regularised master equation and, independently, in the gauge δφ = 0; both give
  T = 0.7584, i.e. τ_lin = 5.13 M." Measured: τ = 5.12 (level 3), 5.23 (level 4), T = 0.76, 0.77, agreement 0.2 % and 1.9 %
  (`numbers.tex`: clmTauLevelThree, clmTauLevelFour, clmProperEfoldThree/Four, clmGgsAgreement/Four, clmLinT, clmLinTau).
  The code of their linear solver (`linear_mode.py`) is not in the arXiv source. Not read.

**The map (to be checked symbolically, U1).** ρ_E = a x, so [SN26] = [GGS09a] with b = a, γ₁ = m/a, γ₀ = −πγ₁/2, B = a e^{πγ₁/2}. Then
(i) m_{+∞} = Bγ₁e^{−γ₁π/2} = a γ₁ = m; (ii) r_throat = B√(1+γ₁²) e^{−γ₁ arctan γ₁} = R⋆ (using arctan γ₁ = π/2 − arctan(1/γ₁));
(iii) lapse at the throat e^{γ₁ arctan γ₁ + γ₀} = α_th; (iv) t_SN = a e^{πγ₁} T_GGS-time, i.e. an e-folding time τ_SN = a e^{πγ₁}/β in the
[SN26] time t; (v) τ_SN α_th / R⋆ = e^{2γ₁ arctan γ₁}/(√(1+γ₁²) β) = [GGS09a]'s T. So [SN26]'s T and [GGS09a]'s T are the same quantity
(proper time at the throat over areal throat radius). Numbers: at a = 2, m = 1, γ₁ = 1/2 the printed 5.13 · 0.575 / 3.8895 = 0.7584.

## 3. What is computed

β(γ₁), the largest root of −χ_ρρ + Wχ = −β²χ (decaying at both ends), and T(γ₁) as above, at γ₁ = 0 (control) and γ₁ = 1/2, and a
table at the 16 values of the first row of [GGS09a] Table I (γ₁ = 0, 0.1, …, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0; the second row, γ₁ ≥ 2.5, is not computed: x(ρ) ~ ρ e^{πγ₁}
reaches 10¹³ at γ₁ = 10 and the printed W loses all digits there).

- **Method A (shooting).** `scipy.integrate.solve_ivp` (DOP853, rtol 1e-13, atol 1e-16) on the system for (χ, P = χ_ρ, x) in the
  variable ρ (x_ρ = e^{2γ₁ arctan x}), from ρ = ±L (L = 30) to ρ = 0. At large |ρ| W → 2/ρ² (p. 7: W = e^{±2πγ₁}[2x⁻² + …], ρ/x → e^{∓πγ₁}),
  whose decaying solution is e^{−β|ρ|}(1 + 1/(β|ρ|)); the start is χ = 1 and P/χ = −g at ρ = +L, +g at ρ = −L, with
  g = β + (1/(β L²))/(1 + 1/(β L)). An error in the start decays inward, because the wanted solution grows inward. W = **printed
  Eq. (32)**. Match at ρ = 0 by the normalized Wronskian; scan β ∈ [0.05, √(−min W)] on 60 points for sign changes (their count is
  checked), `brentq` (xtol 1e-14, rtol 1e-14) on the bracket of the largest β.
- **Method B (matrix).** Uniform grid in ρ on [−L, L], sixth-order central differences for −d²/dρ², Dirichlet ends, h = L/1500, the lowest
  eigenvalue by `scipy.linalg.eig_banded`. x(ρ_i) from x_ρ = e^{2γ₁ arctan x}, x(0) = 0 (`solve_ivp` DOP853, rtol 1e-13, evaluated on
  the grid). W = **derived**: −V + 2(∂Ψ₀/Ψ₀)² computed with sympy from V (static form, p. 5) and Ψ₀ (Eq. (28)), lambdified. B shares with A: the
  background (Eqs. (11)–(14)), V, Ψ₀ and ρ(x); it shares no code for W, no integrator, no root finder, no discretization.
- **Method C (gauge δΦ = 0, no W).** The linearized Einstein–ghost equations for δd, δa, δc with δΦ = 0, derived here with sympy from the
  metric ansatz of Eq. (3) p. 2 (Ricci tensor, no use of [GGS09a]'s linearized equations), reduced to one second-order ODE for C = δc:
  e^{4d}[C'' + 2(d'+c')C'] − β²C − (2 e^{2(d−c)}/c')(C' − d'C) = 0 (expected form, to be confirmed by the derivation, check L1), singular at the
  throat c' = 0 with exponents 0 and 3. Decaying solutions from x = ±X (C ≈ e^{−βρ}, X with ρ = ±30) are continued across the throat on a
  semicircle of radius r in the complex x plane (r < b√(1+γ₁²), the distance to the singular points ±i) and matched by the determinant of
  (C, C'). The upper and lower semicircles must give the same roots (trivial monodromy). C shares with A and B only the background
  functions c, d of Eqs. (11)–(12). It shares nothing of W, V, Ψ₀.
- Answer reported: T from method A (the printed W), error bar = the largest spread over A's tolerance and domain variations
  (rtol 1e-13 → 1e-11, L = 30 → 40), B's h (L/1500 → L/3000) and L, C's r and X, and the three methods. That is a spread over
  discretization and solver choices at fixed physics, not a rigorous enclosure; the root-finder tolerance is 1e-14.

## 4. Checks, criteria, tolerances (fixed before the first run)

β̃ ≡ β in [GGS09a] units (b = 1, γ₀ = 0). "rel" is |x − y|/|y|.

| id | check | pass criterion |
|---|---|---|
| U1 | the map of §2 (sympy, a, m, γ₁ symbolic): (i)–(v), plus the metric of [SN26] Eq. (3) equals [GGS09a] Eq. (13) under the map, plus the printed numbers | each identity simplifies to 0; R⋆(2,1) within 6e-5 of 3.8895, α_th within 6e-4 of 0.575, 5.13·α_th/R⋆ within 1.5e-3 of 0.7584 |
| U2 | the code's T(β, γ₁) = e^{2γ₁ arctan γ₁}/(√(1+γ₁²) β) equals [SN26]'s definition τ_SN α_th/R⋆ with τ_SN = a e^{πγ₁}/β, α_th, R⋆ from [SN26]'s closed forms (a = 1, m = γ₁; 6 values of γ₁ in [0.05, 3], β = 1.7) | rel < 1e-13 |
| S1 | background (Eqs. (11)–(14)) solves R_μν = κ∂_μΦ∂_νΦ, □Φ = 0 (sympy Ricci tensor of the metric) | all components 0 identically in x, γ₁ |
| W1 | printed W (Eq. (32)) = −V + 2(∂Ψ₀/Ψ₀)² (mpmath 30 digits, 8 values of x in [−6, 9] × γ₁ ∈ {0, 0.5, 2}); γ₁ = 0 gives −3/(1+x²)²; W(γ₁) at the throat equals the printed closed form (p. 7); x²W → 2e^{±2πγ₁} at \|x\| = 10⁶ | rel < 1e-12; rel < 1e-14; rel < 1e-12; rel < 1e-4 |
| L1 | the ODE of method C follows from the linearized equations (sympy); and the reconstructed (δc, δa, δd) from a local solution of that ODE satisfy all five linearized equations (tt, tx, xx, θθ, scalar) at 6 points (mpmath odefun, 30 digits) | residuals < 1e-15 |
| P-A | planted, method A, through the same code path: W_pl(x) = −ℓ(ℓ+1) sech²(ρ(x)) with ρ(x) = ∫₀ˣ e^{−2γ₁ arctan y} dy by quadrature, ℓ ∈ {0.9, 1.6}, γ₁ ∈ {0, 0.5, 1.0}; exact β = ℓ (ground state); bound states β = ℓ − n > 0, so 1 for ℓ = 0.9 and 2 (β = 1.6, 0.6) for ℓ = 1.6 | β rel < 1e-9; sign-change count = number of bound states |
| P-B | the same with method B | β rel < 1e-8; count of negative eigenvalues = number of bound states |
| P-C | planted, method C: manufactured solution C* = e^{d(x)} exp(−(x−x_t)²/2) (C*' − d'C* vanishes at the throat) of the ODE with source S = L[C*], integrated from x_t + r to x_t − r on the upper and the lower semicircle, γ₁ ∈ {0, 0.5, 1.0}, β = 1.3 | (C, C') at the end rel < 1e-8 on both paths |
| G0 | control γ₁ = 0, A and B | T ∈ [0.8455, 0.8465] (rounds to 0.846); β² ∈ [1.3965, 1.3975] (−1.397); β² rel to 1.39705243 < 1e-6; β² rel to the eigenvalue of the repo's D = 4 potential U = −3/r⁴ with r² = 1 + l² (one_mode.py S3, retyped here, solved by A) < 1e-9 |
| G1 | A vs B | β rel < 1e-7 at γ₁ ∈ {0, 0.5, 1.0} |
| G2 | A vs C | β rel < 1e-6 at γ₁ ∈ {0, 0.5, 1.0}; upper vs lower semicircle β rel < 1e-9 |
| G3 | **the acceptance test**: T(γ₁ = 1/2) against [SN26]'s linear 0.7584 | \|T/0.7584 − 1\| ≤ 0.002 → agree. If not: the difference is reported with the normalizations of §2, and nothing is changed |
| G4 | T(0.5) against [GGS09a] Table I 0.758 | \|T − 0.758\| ≤ 0.0006 |
| G5 | the 16 values against Table I: γ₁ = 0, 0.1, …, 1.0 → 0.846, 0.841, 0.826, 0.805, 0.782, 0.758, 0.737, 0.718, 0.701, 0.687, 0.675; γ₁ = 1.2, 1.4, 1.6, 1.8, 2.0 → 0.656, 0.642, 0.631, 0.624, 0.618 | each \|T − table\| ≤ 0.001 |
| G6 | [SN26]'s ledger: T₃ = 5.12 α_th/R⋆ and T₄ = 5.23 α_th/R⋆ (α_th, R⋆ from the closed forms) against my T | 100·(T₃/T − 1) ∈ [−0.25, −0.15] % (they print 0.2 %), 100·(T₄/T − 1) ∈ [1.85, 1.95] % (they print 1.9 %) |
| G7 | exactly one negative eigenvalue (B) and one root of the matching function in the scan (A) | at γ₁ ∈ {0, 0.5, 1.0, 2.0}: count 1; B's next eigenvalue ≥ 0 |
| D1 | spread of β (A: rtol, L; B: h, L; C: r, X) | max relative spread < 1e-7 (this is the error bar of the answer) |

Status words for the note: the identities U1, S1, W1, L1 are *checked symbolically* (or to 30 digits); β and T are *numerical evidence*
(three methods, spread D1); nothing is *proved*.

## 5. Control targets and predictions (`--mutate=NAME`; each run executes every check; exit 1 if any check fails)

A control is silent on its target if the named check does not fail. Silence is a result and is reported, and a target list is not
edited after a run. Predictions:

| mutation | what it changes | must fail (target) | predicted not to fail |
|---|---|---|---|
| `potential` | W → W + 0.1/(1+x²)² in both A and B (planted, W1 and C code untouched) | **G0** (γ₁ = 0 control), G2, G3, G4, G5, G6 | U1, U2, S1, W1, L1, P-A, P-B, P-C, G1, G7, D1 |
| `printedW` | the −4γ₁/(1+x²)·F_x/F term of the printed W (A only) gets 3γ₁ | W1, G1 (γ₁ = 0.5, 1.0), G2, G3, G4, G5 | G0 (the term is ∝ γ₁), P-A, P-B, U1, U2 |
| `matrix` | B's sixth-order stencil: the centre weight −49/18 becomes −2.7 | P-B, G1, G0 (B's value) | P-A, U1, U2, W1 (G2 compares A and C: passes) |
| `planted` | the planted exact answer β = ℓ replaced by β = 1.01 ℓ | P-A, P-B | G0, G1, G2, G3 |
| `xmap` | A's equation becomes x_ρ = e^{−2γ₁ arctan x} (sign flipped) | P-A at γ₁ ≠ 0, G1, G2, G3, G4, G5 | G0 (γ₁ = 0), P-B, U1, U2 |
| `units` | γ₀ = +πγ₁/2 in the map of §2 | U1 | everything numerical |
| `tfactor` | the code's T drops the factor e^{2γ₁ arctan γ₁} | U2, G3, G4, G5, G6 | G0 (γ₁ = 0), G1, G2, P-A, P-B, P-C, U1 |
| `count` | G7 uses W + a second well −2 sech²(ρ − 8) | G7 | everything else |
| `domain` | A and B use L = 4 instead of 30 | D1, G0 (the 1e-6 test), G1 | U1, U2, S1, W1, L1, P-C (P-A, P-B use the same L and may fail) |
| `deltaphi` | the 2 in 2e^{2(d−c)}/c' of method C's ODE becomes 1 | L1, G2 | G0, G1, G3, P-A, P-B (P-C is self-consistent) |
| `cpath` | method C's semicircle radius → 0 (through the singular point) | P-C, G2 | G0, G1, G3 |
| `background` | κΦ₁² = −2(1+γ₁²) replaced by −2(1+2γ₁²) in S1 | S1 | all others |

If a prediction is wrong (a control does not fire, or fires on something not predicted), that is reported in the note and on the
issue as it is, with the log of the run.

## 6. Run plan

1. Step 1 (this README): committed and pushed to negative-mass-raw before the script is run.
2. Step 2: the script's γ₁ = 0 part alone (`--gamma=0`), A and B, logged here (`run1_gamma0.log`); posted with a revised ETA.
3. Step 3: γ₁ = 1/2 and the other checks, then the mutations (one run each, `mut_<name>.log`), logs numbered if rerun.
4. Step 4: the final run, stdout to `notes/ellis_efold_output.txt` and a copy here.
Every stdout goes to a log in this folder. Logs are never overwritten; reruns are `…_run2.log`. One process, one thread, `nice -n 10`; a
run that exceeds 1 h wall time is stopped and what finished is reported. Memory is reported only. Systemd units (`nm-i151-<step>`) for
any run over a few minutes, exit code in `<step>.rc`.

## 7. Amendments

(none yet)
