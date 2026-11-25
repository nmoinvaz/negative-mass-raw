# I163-rpi5: Ellis e-folding time, second row of [GGS09a] Table I (γ₁ = 2.5 … 10) and the large-γ₁ limit equation (#163)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, `nice -n 10`,
`OMP_NUM_THREADS=1`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/163
Worktree: `~/Source/negative-mass-i163`, branch `wip/i163-ellis-second-row` (base main 2455a0d). Code `notes/ellis_efold.py`, stdout
`notes/ellis_efold_output.txt`, note `notes/ellis_efold.md`. Python `~/Source/negative-mass-venv314/bin/python` (3.14.10, numpy 2.5.4,
scipy 1.18.1, mpmath 1.3.0, sympy 1.14.0).

This README was written before the first run of the new code (`--section=new`). Nothing in it is changed after a result is seen except
under "Amendments" at the end, which lists each change with the reason and the log that caused it.

## 0. What was run before this README (all logged here; none computes an eigenvalue of the second row or of the limit equation)

| log | what | result |
|---|---|---|
| `baseline_first_row_main2455a0d.log` (+ `.py`, `.rc`) | #151's **unmodified** `method_A(g, W_A, L=30, lam=lam_of(g))` at the 16 first-row γ₁, from the worktree at main 2455a0d | β_A to 17 digits; exit 0; these are the "#151 values" for R1 |
| `legacy_Lspread_L45.log`, `legacy_Lspread_L60.log`, `legacy_Lspread_report.txt` | the same call with L = 45 and 60 (domain-truncation spread of #151's path) | β changes by ≤ 2.0e-13 at every γ₁ ≤ 1.8 and by **6.3e-6 at γ₁ = 2.0** (L = 30 → 45; 45 → 60 changes nothing). #151's γ₁ = 2.0 value (T = 0.6178881) is truncated; the converged T is 0.6178919. D1 of #151 tested γ₁ = 0 and 0.5 only |
| `prefeas_throat_position.py/.log` | ρ̃_throat = λ ρ(γ₁) = ∫₀^{γ₁} e^{2γ₁(arctan γ₁ − arctan y)} dy, the throat position in #151's variable ρ̃ = λρ (λ = e^{2γ₁ arctan γ₁}, origin x = 0), whose domain is ρ̃ ∈ [−30, 30] | γ₁ = 1: 2.2; 2.0: 23.8; **2.5: 84.8**; 3: 321; 4: 5.2e3; 6: 1.8e6; 8: 7.1e8; 10: 3.0e11 |
| `prefeas_conditioning.py/.log` | the bracket of the printed Eq. (32) in double, and the same with the first two terms combined, against 60-digit mpmath, at x = 10 … 1e12, γ₁ = 2.5 and 10 | **both are accurate to 8e-16 or better at every x up to 1e12** |

Two facts follow, and they change how the far-field problem of the issue is handled.

1. **The printed W does not lose digits at large x.** The cancellation of −3/q and 3(x−γ₁)²/q² is against the term 2(F_x/F)² ≈ 2/x² of the
   same size, so the sum keeps full relative accuracy (`prefeas_conditioning.log`). The issue's and #151's remark ("the printed W loses all digits
   there") does not hold for the bracket in double precision.
2. **The reason #151's code cannot be run at γ₁ ≥ 2.5 is the position of the throat, not W.** The domain ρ̃ ∈ [−30, 30] is centred at x = 0.
   The wavefunction lives around the throat, at ρ̃ = 84.8 (γ₁ = 2.5) … 3e11 (γ₁ = 10). At γ₁ = 2.0 the throat is at 23.8, 6 units from the
   right end, which is why #151's γ₁ = 2.0 value is truncated at 6e-6.

## 1. Sources read

Everything is read from the TeX of [GGS09a] (`../I151-rpi5/src_ggs09a/phantom_lin.tex`, arXiv:0806.0608 v2, sha256 `eaea3332…c10`, as in #151).
Not fetched again.

- Table I, both rows: lines 955–985 (second row lines 970–981: 0.608 0.602 0.599 0.597 0.595 0.594 0.593 0.592 0.592 0.591 0.591 0.590
  0.590 0.590 0.590 0.590 at γ₁ = 2.5, 3.0, … , 10.0).
- Sec. IV (time scale), lines 863–952: Eq. (DiffEq) in x with a(x) = e^{2γ₁[arctan x − arctan γ₁]}, β̄ = e^{−2γ₁ arctan γ₁} β,
  W̄ = a²[bracket of Eq. (32)], T = 1/(√(1+γ₁²) β̄); shooting from large x; "the time scale converges to a value of 0.590 r_throat".
- Large-γ₁ subsection, lines 1001–1079: z = x/γ₁, â(z) = e^{2γ₁[arctan(γ₁ z) − arctan γ₁]}, β̂ = γ₁ β̄, Ŵ(z) = γ₁² W̄(γ₁ z) (lines 1021–1031).
  **Eq. (DiffEqLargeGamma)**, the PDF's (43):

  −(e^{2(1−1/z)} ∂_z)² χ + e^{4(1−1/z)} [2 z⁻² − 10 z⁻³ + 3 z⁻⁴] χ = −β̂² χ,  z > 0.

  **Eq. (ZeroModeLargeGamma)**: the zero mode (2/π)(z−1)/z² e^{1−z⁻¹}, "it can be checked that it solves (43) with β̂ = 0"; it has one zero, so
  one bound state. "A numerical shooting procedure … starts at some large value of z, where χ ≈ e^{−β̂ρ̂}, ρ̂(z) = ∫₁ᶻ e^{−2(1−ζ⁻¹)} dζ, **yields
  1/β̂ = 0.588**." Then T = 1/(√(1+γ₁²) β̄) = 1/β̂ in the limit (their words). The table's large-γ₁ value is 0.590.
- By hand from the TeX, as a check of the reader and not of the code: the five terms of Ŵ tend to −3/z² + 3(z−1)²/z⁴ + 2/z² − 4/z³ + 0 =
  2/z² − 10/z³ + 3/z⁴, and the prefactor â² tends to e^{4(1−1/z)}. Checked numerically below (N3b).

## 2. The far-field handling and the new coordinates

**New variable.** u = (ρ̃ − ρ̃_throat)/sc, sc = max(1, γ₁), i.e. dx/du = sc · a(x), x(0) = γ₁ (the throat). The equation becomes
−χ_uu + sc² W̄(x(u)) χ = −b² χ with b = sc β̄ (= β̂ for γ₁ ≥ 1). Then T = sc/(√(1+γ₁²) b), and in #151's units β = λ b/sc. The
mode is O(1) wide in u at every γ₁ (the limit equation's variable ρ̂ is this u at γ₁ → ∞). Domain u ∈ [−L′, L′], L′ = 20. At the ends x(−L′), x(+L′)
reach ≈ 0.2 γ₁ … e^{2γ₁ arctan(1/γ₁)} sc L′ ≤ 7.4 · 20 · γ₁, i.e. at most ≈ 1.2e3 at γ₁ = 10 and 2.4e4 at γ₁ = 160, nowhere near 1e12.
a(x) is evaluated as exp(2γ₁ atan2(x − γ₁, 1 + γ₁x)) (no cancellation next to the throat). λ is never formed in the new path.

**Far-field form.** Beyond x_sw = 2 max(1, γ₁) the code evaluates the bracket with the first two terms combined,
−3/q + 3(x−γ₁)²/q² = 3(γ₁² − 1 − 2γ₁x)/q² (exact algebra, q = 1 + x²). By §0 this is **not needed for accuracy**; it is kept as the
far-field form so that the large-x part of W is code that the second row's numbers depend on and that a control can break (the issue asks for
that control). That it changes nothing is checked by R3 (A with the far-field form against A with the printed bracket only) and N1a/N2.
At the far end the start is χ′ = −b χ (the free decaying solution), at the near end +b χ; the neglected 2/r² tail and the wrong
left tail change the start by an amount that the wanted solution dwarfs after e^{−2b(L′ − well width)} ≲ 1e-15; D1b measures it (L′ → L′ + 8).
The legacy path (domain centred at x = 0) is **not touched**; it produces the first row exactly as in #151 (R1).

**Methods** (the new path, γ₁ > 0 as well as the first row):

| method | what it solves | shares with the others |
|---|---|---|
| A, shooting | −χ_uu + sc² W̄ χ = −b² χ, W̄ = a² × printed bracket, DOP853 rtol 1e-13, inward from ±L′ to u = 0, normalized Wronskian, 40-point scan at rtol 1e-9 then `brentq` | the background x(u) |
| B, matrix | the same operator, sixth-order differences on h = 2L′/N, N = 4000, W̄ = e^{−4γ₁ arctan γ₁} (−V + 2(∂Ψ₀/Ψ₀)²) derived with sympy and evaluated at 40 digits | the background x(u) |
| C, gauge δΦ = 0 | the ODE of #151 for C = δc, rewritten with β²e^{−4γ₁ arctan x} = (b/sc)²/a(x)²; decaying solutions from x(±L′) continued across the throat on semicircles in the complex x plane, radius 0.5 min(√(1+γ₁²), γ₁ − x(−L′)); no W | the background functions only |
| LE-A, LE-B | A and B above on the limit equation: dz/du = e^{2(1−1/z)}, z(0) = 1, potential e^{4(1−1/z)}[2z⁻² − 10z⁻³ + 3z⁻⁴] | each other: the map z(u) and Ŵ |
| LE-C, finite volume | the limit equation on a uniform grid in t = ln z ∈ [ln 0.15, ln 150], −(pχ_t)_t + (zŴ/â)χ = −β̂²(z/â)χ, p = â/z, N = 8000 and 16000, Richardson in h² on the eigenvalue | Ŵ only |

The error bar of a reported T is the largest relative spread of b in D1b (A: rtol 1e-13 → 1e-11 and L′ → L′ + 8; B: N 4000 → 8000 and
L′ + 8; C: semicircle radius 0.5 → 0.3 and 0.7, L′ + 8) at γ₁ = 2.5, 5, 10, times T. It is a spread over discretization and solver choices at
fixed physics, not a rigorous enclosure; the root-finder tolerance is 1e-14. The same bar is quoted for the other γ₁ of the row (assumption,
said so in the note). The limit equation's error bar is the spread among LE-A, LE-B and LE-C.

## 3. Checks, criteria, tolerances (fixed before the first run)

"rel" is |x − y|/|y|. β′ ≡ b. The script codes each line as worded; a check that fails exits non-zero. #151's 46 checks and their criteria
are unchanged (`../I151-rpi5/README.md` §4); R1 is added to them.

| id | check | pass criterion |
|---|---|---|
| R1 | the legacy path of the extended script (domain centred at x = 0, L = 30) against #151's β_A at the 16 first-row γ₁ (`baseline_first_row_main2455a0d.log`, constants `FIRST_ROW_BETA`) | rel ≤ 1e-9 at all 16 |
| N1a | W̄ in the far-field form (double) against W̄ from the derived W (60 digits), γ₁ ∈ {2.5, 10}, x = 10, 1e2, 1e3, 1e4, 1e6, 1e8, 1e10, 1e12; points with \|W̄\| < 1e-3 of the sum of the absolute values of its terms are skipped and counted | rel ≤ 1e-12 |
| N1b | the printed bracket × a² (double) against the derived W̄ (40 digits) at 8 points of each of the 32 centred domains (x(−L′), x(+L′), u = ±10, ±2, ±0.5), same skip rule | rel ≤ 1e-12 |
| N2 | far-field bracket − printed bracket, symbolic in x, γ₁ | simplifies to 0 |
| N3a | [GGS09a]'s Ŵ(z) (lines 1021–1031, retyped, mpmath 50 digits) against γ₁² W̄(γ₁ z) of the code's bracket, γ₁ ∈ {2.5, 10, 100}, z ∈ {0.4, 1, 2, 5} | rel ≤ 1e-12 |
| N3b | Ŵ(z; γ₁) against the printed limit potential e^{4(1−1/z)}[2z⁻² − 10z⁻³ + 3z⁻⁴], z ∈ {0.4, 0.8, 1, 1.5, 3, 8}, max rel diff at γ₁ = 1e2, 1e3, 1e4, 1e5, 1e6 | each decade falls by at least 5; the last ≤ 1e-3 |
| LE0 | the zero mode (z−1)/z² e^{1−1/z} solves the printed Eq. (43) with β̂ = 0 | symbolic residual 0 |
| U3 | T of the new path, sc/(√(1+γ₁²) b), against `T_of(λ b/sc, γ₁)`, γ₁ ∈ {0.5, 2.5, 10}, b = 1.7 | rel ≤ 1e-13 |
| P-A2, P-B2 | **planted**, through the new geometry: W_pl = −ℓ(ℓ+1) sech²(u(x)), u(x) by Gauss–Legendre quadrature (independent of the ODE for x(u)), ℓ ∈ {0.9, 1.6}, γ₁ ∈ {2.5, 5, 10}; exact b = ℓ, bound states ℓ − n > 0 | A: rel < 1e-9 and 1 resp. 2 roots; B: rel < 1e-8 and 1 resp. 2 negative eigenvalues |
| P-C2 | planted for C: manufactured solution C* = e^{γ₁ arctan x} e^{−(x−γ₁)²/2} of the rescaled ODE with source, carried across the throat on both semicircles, γ₁ ∈ {2.5, 5, 10}, b/sc = 1.3 | (C, C′) rel < 1e-8 |
| P-LA, P-LB, P-LC | planted in the limit-equation geometry (z(u), ρ̂(z) by quadrature), same ℓ; exact β̂ = ℓ | A rel < 1e-9; B rel < 1e-8; finite volume (Richardson) rel < 1e-6; counts as above |
| R2 | **the first row through the new path**, 16 values: β = λ b/sc against #151's β_A | rel ≤ 1e-9 against the converged L = 60 values (`FIRST_ROW_BETA_L60`) at all 16, and against the as-run L = 30 values (`FIRST_ROW_BETA`) at γ₁ ≤ 1.8. At γ₁ = 2.0 the as-run value is truncated (§0), so its difference (expected 6.3e-6) is reported, not tested |
| R3 | A with the far-field form against A with the printed bracket only, γ₁ ∈ {0.5, 2, 2.5, 10} | rel ≤ 1e-10 |
| G5b | **the second row**: T(γ₁) = sc/(√(1+γ₁²) b) at the 16 values against Table I's second row | each \|T − printed\| ≤ 0.001 (the issue's criterion; the differences are reported) |
| G1b | A against B (derived W), the 16 second-row values and γ₁ ∈ {0.5, 1, 2} | rel ≤ 1e-7 |
| G2b | A against C (no W), γ₁ ∈ {2.5, 4, 6, 8, 10}; upper against lower semicircle | rel ≤ 1e-6; rel ≤ 1e-9 |
| G7b | exactly one root in A's scan and one negative eigenvalue in B (the next ≥ 0), γ₁ ∈ {2.5, 5, 10} | count 1 |
| D1b | spread of b (see §2), γ₁ ∈ {2.5, 5, 10} | max relative spread < 1e-7 |
| LE3 | the limit equation: A, B, finite volume | A against B rel < 1e-8; A against finite volume rel < 1e-6 |
| LE4 | the limit equation has one bound state: one root in A's scan, one negative eigenvalue in B and in the finite volume | count 1 |
| LE5 | **the issue's limit criterion**: 1/β̂ (from A) against the table's large-γ₁ value 0.590, and against the paper's own 1/β̂ = 0.588 | (a) \|1/β̂ − 0.590\| ≤ 0.001; (b) \|1/β̂ − 0.588\| < 0.0005 (rounds to it). If (a) or (b) fails the gap is reported with both numbers; nothing is reworded |
| LE6 | the finite-γ₁ problem tends to the limit equation: b = β̂_{γ₁} at γ₁ = 10, 20, 40, 80, 160 (A) against the limit's β̂ | the gap shrinks by a factor ≥ 1.5 at each doubling, and the last is ≤ 0.3 % of β̂ |

Not checks (diagnostics, printed and reported): N0 (the throat position and the x range of every centred domain, per γ₁), DIAG N1 (the printed
bracket's error at x up to 1e12), DIAG L0 (the legacy path at γ₁ = 2.5 and 3.0: how many roots it finds, expected none), the first-row
differences row by row, the Richardson extrapolation of T(γ₁) in 1/γ₁ from 80 and 160, T(γ₁) at 10 … 160.

What can be met (checked before the run, not by running the new code): sixth order at h = 0.01 gave 1e-12 in #151 at h = 0.02, so P-B2 (1e-8)
and G1b (1e-7) have margin; A's start error is e^{−2b(L′ − width)} ≲ 1e-15; the finite volume is second order with h = ln 1000/8000 = 8.6e-4,
h² ≈ 7e-7 times a modest constant, Richardson takes it to O(h⁴) ≈ 5e-13, so 1e-6 has margin. If a planted problem shows a method cannot meet
its tolerance, that goes under "Amendments" with the log, before any real-data check is read.

## 4. Controls (`--mutate=NAME`; each run executes every check of its section; exit 1 if any check fails)

A control is silent on its target if a named check does not fail, and a target that never ran counts as silent. Silence is a result and is
reported; a target list is not edited after a run. "must fail" is the prediction; every new check not listed for a mutation is predicted to pass.

| mutation | what it changes | must fail (target) | section |
|---|---|---|---|
| `potential` | W + 0.1/(1+x²)² in the legacy A and B | G0 G2 G3 G4 G5 G6 **R1** | all |
| `printedW` | the −4γ₁/(1+x²) F_x/F term gets 3γ₁, in the legacy and the new bracket | W1 G1 G2 G3 G4 G5 R1 **N1a N1b N3a R2 G5b G1b G2b** | all |
| `matrix` | B's centre weight −49/18 → −2.7 (legacy B, B2, LE-B) | P-B G1 G0 **P-B2 G1b P-LB LE3** | all |
| `planted` | exact β = ℓ → 1.01 ℓ | P-A P-B **P-A2 P-B2 P-LA P-LB P-LC** | all |
| `xmap` | the sign in the legacy A's x(ρ) | P-A G1 G2 G3 G4 G5 **R1** | all |
| `units` | γ₀ = +πγ₁/2 in the [SN26] map | U1 | all |
| `tfactor` | `T_of` drops e^{2γ₁ arctan γ₁} | U2 G3 G4 G5 G6 **U3** | all |
| `count` | a second well in the G7, G7b and LE4 geometries | G7 **G7b LE4** | all |
| `domain` | legacy L = 4; the new path L′ = 2 | D1 G0 G1 **D1b G5b R2 P-A2 P-B2 G1b LE3** | all |
| `deltaphi` | the 2 in method C's ODE becomes 1 (legacy C and C2) | L1 G2 **G2b** | all |
| `cpath` | method C's semicircle radius → 0 (legacy C and C2) | P-C G2 **P-C2 G2b** | all |
| `background` | κΦ₁² = −2(1+2γ₁²) in S1 | S1 | all |
| `largex` | far-field bracket: 3(γ₁² − 1 − 2γ₁x) → 3(γ₁² − 1 − γ₁x), used for x > 2 max(1, γ₁) | **N1a N2 R2 R3 G5b G1b G2b** | new |
| `centre` | the new path's origin x₀ = γ₁ → 0 (the legacy origin) | **G5b G1b G7b D1b** | new |
| `scale` | T of the new path without sc | **U3 G5b** | new |
| `lelimit` | the −10 of the limit potential → −9 | **LE0 N3b LE6** | new |
| `lefv` | finite-volume mass weight z/â → z | **LE3 P-LC** | new |

Bold entries are new targets. Runs of the 12 old mutations use the whole script (old and new section), the five new ones `--section=new`
(their targets are all new checks). The issue's required control is `largex`: it breaks the far-field form of W, which the new rows depend on
for x > x_sw; N1a, N2, R3 and the rows fire on it, R1, N1b, N3, P-* and the limit-equation checks are predicted to pass. `centre` shows the
issue's real obstruction: with #151's origin the rows fail. Not every check has a mutation that fires it: the diagnostics above are not checks.

## 5. Run plan

1. Step 1 (this README): committed and pushed to negative-mass-raw before the new code runs. The code is on the wip branch at the commit named in §6.
2. Step 2: `--section=new` (`run1_new.log`): far-field and first-row checks (N1a … R3), planted, then the rows. Post the far-field handling, the
   first row (R2, R3) and a revised ETA.
3. Step 3: the second row, the limit equation (same log). Post.
4. Step 4: the 17 mutations, one run each (`mut_<name>.log`, `.rc`, `.time`), logs numbered if rerun.
5. Step 5: the final run, stdout to `notes/ellis_efold_output.txt` and a copy here (`final_output.txt`); the note extended.

Every stdout goes to a log in this folder; logs are never overwritten, reruns are `…_run2.log`. One process, one thread, `nice -n 10`;
runs over a few minutes are `systemd-run --user --unit=nm-i163-<step>` with the exit code in `<step>.rc`. A run that exceeds 1 h wall time is
stopped and what finished is reported. Memory is reported only.

## 6. Code state at the README

`notes/ellis_efold.py` on `wip/i163-ellis-second-row`, extended (the legacy path, its constants and the 46 old checks are unchanged apart
from `LEG`, R1 and the extended `MUTATIONS` table). The commit is named in the first post.

## Amendments

1. **run1 (`run1_new.log`, rc 1) crashed in its first check, N1a**, with a ZeroDivisionError of the derived W at γ₁ = 10, x = 10: that sample point of §3 is
   exactly the throat, where the derived W is 0/0 (removable; #151's B had the same at γ₁ = 0). A code defect of the check, not a failed
   criterion. Fix: `derived_wbar_mp` uses #151's symmetric average (x ± 1e-8) when |x − γ₁| < 1e-14. The sample points, the 60 digits and the
   1e-12 are unchanged. Log kept; the rerun is `run2_new.log`.
2. **run2 (`run2_new.log`, rc 1, 3 min 55 s): P-C2 fails at γ₁ = 5.0 (9.3e-8, criterion 1e-8) and 10.0 (4.8e6); LE5(a) fails (criterion ≤ 0.001, value
   −0.00165).** Nothing in either criterion is changed. LE5(a) is the issue's acceptance reported as it is (§ results). For P-C2 the cause was computed
   (`diag_pc2_growth.py/.log`): the manufactured test integrates along an arc on which the unwanted homogeneous solution grows by 1.7e2, 3.4e4, 1.4e9 at
   γ₁ = 2.5, 5, 10 (b/sc = 1.3), so the test amplifies its own 1e-12 integration error; the real use of method C integrates in the stable
   direction and agrees with A to 1.5e-12 (G2b). The coordinator is asked how to treat P-C2 (hc message, answer recorded below).
3. The diagnostic "Richardson in 1/γ₁ from 80 and 160" of §3's list printed T_inf = 0.588341, but the gaps of LE6 fall by 4 per doubling
   (order 2), not 2. The diagnostic now also prints the measured order and the extrapolation with it. A diagnostic, not a check; no criterion involved.
4. **Coordinator's ruling on P-C2 (hc, 2026-11-24).** (i) P-C2 stays exactly as registered and stays FAILED in the output (γ₁ = 5.0, 10.0), with the diagnosis of
   amendment 2. (ii) Not replaced, and no new radius or b/sc picked by its growth factor. (iii) **P-C2b** is added, written here before its first run: the manufactured
   solution is carried through exactly the path, radius and direction method C uses for its real roots at each γ₁, with the same 1e-8. (iv) The controls `cpath` and
   `deltaphi` then target P-C2b; their effect on it is computed (standalone runs `pc2b_mut_<name>.log`) before the target lists are declared. (v) The note states the
   γ₁ = 2.0 point plainly.

   **P-C2b, as it will be coded** (`check_planted_C2b`; the same function `C2_det` runs the real roots and the planted test, with an optional source and one extra state):
   - γ₁ ∈ {2.5, 4, 6, 8, 10} (the set of G2b); b = the root of A at that γ₁ (from the same run), bt = b/sc. L′ = 20, semicircle radius, rtol 1e-12, DOP853, upper and
     lower semicircle, right start at x(+L′) and left start at x(−L′): exactly G2b's geometry (`C2_geometry`).
   - Right solution (decaying to the right, growing inward, as the real one): C_R* = exp(−bt s) h(x)/h(x_R), s = ∫_{x_R}^{x} dy/a(y) carried as a third state variable by
     the integrator itself (so that along the real segment and the arc the source follows the path), h = exp(κ w tanh((x − γ₁)/w)), κ = bt + γ₁/(1+γ₁²) (so that
     C′ − γ₁C/(1+x²) = 0 at the throat: C* is regular there), w = √(1+γ₁²). Left solution: C_L* = exp(+bt s_L), s_L = ∫_{x_L}^{x} dy/a. Both are integrated with the
     source S = C*″ − R_true(C*, C*′), R_true the ODE of L1 retyped in the test (k = 2), so the test is independent of `odeC2_rhs` (and a mutation of the latter fires it).
   - Path: right real segment x(+L′) → x_t + r, then the arc to x_t − r (both sides), left real segment x(−L′) → x_t − r.
   - Exact end values: s by real-axis quadrature (`scipy.integrate.quad`, epsrel 1e-13; the integrand is analytic in the disc of the arc, so the path does not matter).
   - Pass: for each γ₁, both semicircles and the left segment, ‖(C, C′) − exact‖/‖exact‖ < 1e-8. An exception is a failure. If P-C2b fails, that is a result.
   - Why this form: the unwanted homogeneous solution grows along the arc as in the real computation (amendment 2), but C* grows with it, so the relative error is not
     amplified; that is a property of the real direction, not a tuned parameter. The growth is not used to pick anything.
   - Predictions: `cpath` (r = 0, the integration reaches the singular throat) and `deltaphi` (the integrated ODE has the coefficient 1, the source the coefficient 2) fire it.
     P-C2 leaves the target list of `cpath` (it fails unmutated and cannot fire); P-C2b joins `cpath` and `deltaphi`.
5. The mutation queue `nm-i163-mut1` was stopped by me after 6 min, in its first run (`mut_largex_run1_stopped.*`, no `.rc`), so that all mutation logs come from the
   script that contains P-C2b. The mutation runs restart as `…_run2` after P-C2b has run once.
6. **P-C2b, first run (`pc2b_run1.log`, standalone `--only=P-C2b`, exit 0): passes at all five γ₁, worst 1.4e-11** (right + arc 2.5e-12 … 5.0e-12, left segment
   1.1e-11 … 1.4e-11; the criterion is 1e-8). Its effect under the two controls, computed before they were declared (`pc2b_mut_cpath.log`, `pc2b_mut_deltaphi.log`):
   `cpath` fires at all five γ₁ (the integration reaches the singular throat: non-finite right-hand side), `deltaphi` fires at all five (worst rel error 33 … 55).
   So the declared targets stand: `cpath` → P-C, G2, **P-C2b**, G2b (P-C2 removed: it fails unmutated and cannot fire); `deltaphi` → L1, G2, G2b, **P-C2b**.
   Note for the note: the real-path radius is r = min(0.5 √(1+γ₁²), 0.5 (γ₁ − x(−L′))), e.g. 3.83 at γ₁ = 10 against 5.02 in P-C2, so P-C2 was not
   the real path in the radius either.
7. The mutation runs are named `mut_<name>` (not `…_run2`, since the stopped first run was renamed `mut_largex_run1_stopped`); the final unmutated run is `final`.
8. **The 17 mutation runs (queue 2, `final` and `mut_*`, script commit 93f17c4) found three controls that did not fire on their whole target list.** Reported as they are;
   the first logs are kept.
   - `centre`: stopped by the 1 h cap (rc 124, `mut_centre.log`). The mutation sets x₀ = 0 also in the planted problems, and there the integration is extremely slow at
     γ₁ ≥ 5 (the planted P-A2 also fails there, 5.8e-9 and 3.2e-9 at γ₁ = 5). Its targets G5b, G1b, G7b, D1b never ran: **silent in this run**.
   - `xmap`: **silent on R1** (`mut_xmap.log`): the legacy table loop raised (no root with the flipped map) before R1 was reached; G5 reported "table incomplete".
     This is the same kind of silence as #151's first `xmap` run on G5.
   - `domain`: **silent on G5b** (`mut_domain.log`): with L′ = 2 the second row still lies within 0.001 of the printed values (worst 0.000552); the truncation (5.3e-4 relative
     in β, R2) is below G5b's tolerance, which comes from the three digits of the table. Its other nine targets fire. No change is made; it is a result about G5b.
   Two code changes follow, both only on mutated paths, none on any unmutated number: (i) when the legacy table loop raises, R1 now also reports FAIL (as G5 did);
   (ii) the `centre` mutation no longer touches the planted problems (they carry their own origin), only the real rows, G1b, G2b, G7b, D1b, P-C2b. The targets are unchanged.
   `xmap` and `centre` are rerun as `mut_xmap_run2` and `mut_centre_run2`; the unmutated script is rerun once as `final_run2` to confirm that its output
   is the same (apart from the timing line) and to be the file committed as `notes/ellis_efold_output.txt`.

## Results (written after the runs; the criteria above are unchanged)

Code `notes/ellis_efold.py` at 4871503 on `wip/i163-ellis-second-row` (final runs `final.log`, `final_run2.log`, both 100 checks, exit 1: P-C2 and LE5 fail as registered). Tables, the far-field
finding, the limit equation (1/β̂ = 0.588351371), the controls table and the proposed `critical_ghost.md` wording are in `notes/ellis_efold.md` (the #163 part); the controls table is
`mutations_summary.md`, regenerated by `summarize_mutations.py`; `check_note_numbers.py` (log `check_note_numbers.log`, 59 of 59) checks the note's numbers against the output.
Logs of every run are kept: `run1_new` (crash, amendment 1), `run2_new`, `pc2b_*`, `final`, `final_run2`, `mut_*` (17 runs, `mut_largex_run1_stopped`, `mut_centre` stopped at 1 h, `mut_centre_run2`, `mut_xmap_run2`).
