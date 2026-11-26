# I166-rpi5: time-dependent additive shifts b = X(t, x) + R(t, ρ) at the one-sign stage (criteria, logs, controls)

Machine rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process, one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/166. Branch `wip/i166-one-sign-time`, worktree
`~/Source/negative-mass-i166` (main 6ae2047). Python `~/Source/negative-mass-venv314/bin/python` (3.14.10, sympy 1.14.0, mpmath
1.3.0). No Singular, no stored certificates: every check is exact sympy and runs on macOS. Written 2026-11-25, after the six
development probes below and before the first run of `notes/warp/one_sign_time.py` (which did not exist yet). Stop condition: a
single run not finished after 1 h of wall time is stopped and reported. Memory is logged (`/usr/bin/time -v`), never a stop
condition. Estimate 2 to 3 h.

## Question

#158 decided the static reductions and the planar and gauge time dependence. For a time-dependent shift b(t, x, ρ) with
Z = ½ b_xρ ≡ 0 on a box, b = X(t, x) + R(t, ρ). By #158's Dichotomy either R_ρ ≡ 0 on a sub-box (planar, decided in #158) or
h = ½ R_ρ² > 0 on a sub-box. There Lemma R with Z = 0 gives v₀ v₂ = 0: **branch A: v₀ = 0** and **branch B: v₂ = 0**. Decide both,
up to the gauge x → x + D(t) (b → b(t, x − D) − D′): the solution families with their parameters, or a proof that none exists.
For every family that passes the algebraic stage run closure (Lemma K): kernel of M = R − λg, integrability, L_X M. State which
pass, which fail, and whether any is localized in x.

## Reduction (stated before the runs of record; proved by hand in the note, re-checked by the script as listed below)

The block of #158 for b = X + R, with S = R_ρρ + R_ρ/ρ:

    P = X_tx − (X + R) X_xx − X_x²,   Q = −S/2,   Z = 0,   Y = −R_tρ/2 + X_x R_ρ,   h = R_ρ²/2.

**Lemma Z.** Let h > 0 and Z = 0. Then rank(R₃ − λη₃) = 1 for some real λ ≠ 0 iff, at the point, (A) Q = 0 and 2hP + Y² = 0
[v = (0, v₁, v₂), v₁² = 2h, v₂ = −Y/v₁, λ = h + v₂² = h − P], or (B) P < 0, Y = 0 and Q² + P(2h + P) = 0 [v = (v₀, v₁, 0),
v₀² = −P, v₁ = −Q/v₀, λ = h]. (Elimination ideals of Lemma R's equations at v₀ = 0 and at v₂ = 0.) The two conditions are
closed in the box, so on an open dense subset each point has a neighborhood where one holds throughout (Baire).

**Branch A.** Q = 0 gives R = C(t) ln ρ + d(t), C ≠ 0 (h > 0). Then ρ²(2hP + Y²) = C²P + (X_x C − C′/2)². Its ln ρ part is
−C³ X_xx, so X_xx = 0, X = c(t) x + e(t), and what is left is C²c′ − cCC′ + C′²/4 = 0, that is

    c′ = 2γ c − γ²,   γ = C′/(2C).

So b = c(t) x + C(t) ln ρ + d(t) (d absorbs e), with C(t) ≠ 0 any C¹ function and c = |C|(k₀ − K), K′ = γ²/|C|, k₀ ∈ ℝ. The
function d(t) is pure gauge (D′ + cD = d). c(t) and C(t) = ρ b_ρ are gauge invariant. λ = C²/(2ρ²) + (γ − c)² > 0, two
phantoms, and R_ab = λ(g_ab − ρ² dφ_a dφ_b) − α_a α_b with α = (C/ρ)(dx + b dt) + (γ − c) dρ. The static members are C′ = 0
(then c′ = 0, #158's u = c x + C ln ρ + d). A member with C′ ≠ 0 is **not** gauge-equivalent to any static one.

**Branch B.** v₂ = 0 gives Y = 0, so X_x R_ρ = R_tρ/2 with X_x a function of (t, x) and R_tρ/R_ρ of (t, ρ): X_x = κ(t), R_ρ = m(t) f(ρ),
m′ = 2κ m. With p = κ² − κ′ (= v₀² > 0 if v₀ ≠ 0) and g = (f′ + f/ρ)²/4 the equation of (B) is
m² g − p m² f² + p² = 0 for all (t, ρ). If f² is not constant it separates: p and p²/m² are constant, so m is constant, κ = 0,
p = 0, a contradiction. If f is constant, g = f²/(4ρ²) depends on ρ and f² does not, a contradiction. So **branch B has no
solution with v₀ ≠ 0 anywhere**: v₀ ≡ 0 and the solution lies in branch A, in the sub-family v₂ = γ − c = 0.

**Closure.** On branch A, M = −α ⊗ α − λρ² dφ ⊗ dφ has the kernel plane spanned by n = ∂_t − b∂_x and K₂ = (γ − c)∂_x − (C/ρ)∂_ρ,
and [n, K₂] − (C′/C) K₂ = r ∂_x with r = w′ + wc − 2γw − C²/ρ², w = γ − c, ∂_ρ r = 2C²/ρ³ ≠ 0. So the plane is not integrable
where C ≠ 0, and closure fails for every member.

Expected answer: the solution set is larger than the static family (C(t) free), closure fails on all of it, none is localized
in x. The issue's second alternative ("every solution is gauge-equivalent to the static family") is false: probes 1 and 2 show
time-dependent members passing the algebraic stage at exact points.

## Development probes (before this README; scripts and logs in `dev/`)

| probe | what | result |
|---|---|---|
| 1 | 4D coordinate Ricci + `same_sign_form` at 3 exact points: T1 = x/2 + e^{2t} ln ρ, T2 = (1/2 + e^{2t}/3) x + e^{2t} ln ρ, T3 = −tanh t x + e^{2t}(1 − tanh²t) ln ρ, and the ODE-violating T2 + x/5 | T1, T2, T3: root with inertia (0, 2), pattern MM at all points (one T3 draw had tanh t = 1, C = 0, an extra root λ = 1: the script redraws C = 0 points); ODE-violating: no root at 3 of 3 points |
| 2 | `closure2` on T1, T2, T3 and the static 3x/2 + 2 ln ρ + 1/5 | kernel dimension 2, not integrable, 1 to 4 s each |
| 3 | general symbolic: Ricci of c(t)x + C(t) ln ρ + d(t) minus [λ(g − ρ²dφ²) − α⊗α] with c′ → 2γc − γ²; block of X(t,x) + R(t,ρ) | the first is the zero matrix, with c′ → 2γc + γ² it is not (the printed `None` is `is_zero_matrix` undecided); the block matches the formulas above; 6 s |
| 4 | Lemma Z elimination ideals, branch B separation, `dsolve` calls | A: ⟨2hP + Y², Q⟩ and B: ⟨Y, Q² + P(2h+P)⟩ as claimed, ⟨Q, 2hP − Y²⟩ is not; separation: p₁ − p₂ and m₁² − m₂² in the saturated ideal, m₁ − m₂ not; `dsolve` of G′ = 2κG and R″ + R′/ρ = 0 fine. **The script died with a `PolynomialError`** (1/ρ in a generator) at the f-constant case; kept, fixed in probe 5 |
| 5 | the f-constant case with ι = 1/ρ as a generator; the sign-flipped E_B; `dsolve` of c′ = 2γc − γ² | the ideal with saturation by p m f₀ (ρ_a − ρ_b)(ι_a + ι_b) is not [1] (it lacked the factor ι_a + ι_b), see probe 6; `dsolve` of the c ODE returns an implicit integral relation, so the closed form is checked by substitution |
| 6 | forms and bracket for the general family; D′ + cD = d; the f-constant ideal with (ι_a + ι_b); `closure2` and 3 exact points on T4 = −x/t + t^{-2} ln ρ (v₂ = 0 member), P3 = 3x/2 + 2 ln ρ + tanh t, P4 = P1(t, x − tanh t) − (1 − tanh²t) | F − claim = 0, ∂_ρ(ρF/C) = −2C²/ρ³; bracket residual r as stated, ∂_ρ r = 2C²/ρ³; D = e^{−∫c}∫d e^{∫c} solves D′ + cD = d; the f-constant ideal is [1]; T4, P3, P4: root with inertia (0, 2), MM, kernel dimension 2, not integrable |

No criterion below was changed after seeing a failing check. The probes are not runs of the script.

## Planted and tested families (every one through the same function `run_family`)

Chain-rule symbols: En = e^{2t} (En′ = 2 En), Th = tanh t (Th′ = 1 − Th²), Ti = 1/t (Ti′ = −Ti²), Lg = ln ρ.

| name | b | role |
|---|---|---|
| P1 | 3x/2 + 2 ln ρ + 1/5 | planted static (#158's A1) |
| P2 | x + 3 ln ρ | planted static (#158's A2) |
| P3 | 3x/2 + 2 ln ρ + Th | gauge copy, d(t) = tanh t |
| P4 | 3(x − Th)/2 + 2 ln ρ + 1/5 − (1 − Th²) | gauge copy, b₁(t, x − D) − D′ with D = tanh t |
| T1 | x/2 + En ln ρ | new: C = e^{2t}, γ = 1, c = 1/2, γ − c = 1/2 |
| T2 | (1/2 + En/3) x + En ln ρ | new: γ = 1, c = 1/2 + e^{2t}/3 |
| T3 | −Th x + En (1 − Th²) ln ρ | new: γ = 1 − tanh t, c = −tanh t, γ − c = 1 |
| T4 | −Ti x + Ti² ln ρ | new, v₂ = 0 member: C = t⁻², γ = c = −1/t (branch B ∩ A) |
| F1 | 3x/2 + 2 ln ρ + 1/5 + x²/10 | planted failure (X_xx ≠ 0) |
| F2 | (1/2 + En/3 + 1/5) x + En ln ρ | planted failure (violates the c ODE) |
| A0 | x | integrable positive control of the closure code (C = 0, planar K = 1) |

Exact points: 3 per family, `random.seed(1660 + k)`, ρ = j/10 (j = 5..30), Lg, t, x ∈ `rq()`, En = a/b > 0, Th = j/9 (|j| ≤ 8), Ti = a/b
> 0; a draw with C = 0 at the point is redrawn.

## Criteria (each is coded exactly as worded; each can fail)

All criteria are exact (sympy rational arithmetic, no floating point decision). "Zero" means `simplify` returns 0. Names are the
script's check names. #158's code is imported read-only: `one_sign_classify.blocks` (the block from jets), `v_block`,
`rad_member`; `same_sign_scalars.same_sign_form`, `rank1_lams`, `closure2`, `simp_r`; `phantom_source.ricci`; `two_scalars.rq`.

| id | check | criterion |
|---|---|---|
| C1 | `block` | For b = X(t, x) + R(t, ρ), X and R undefined functions, the coordinate Ricci tensor (`ricci`) of ds² = −dt² + (dx + b dt)² + dρ² + ρ² dφ² in the frame (n, ∂_x, ∂_ρ, ∂_φ/ρ) minus [[P−h, Q, 0], [Q, −P−h, Y], [0, Y, h]] ⊕ 0 is zero, with P, Q, Y, h as in the Reduction; R₀₀ + R₁₁ + 2R₂₂ = 0; `blocks` of #158 on the jets of X + R returns (P, Q, 0, Y, h) of the Reduction; for R = r(t) the block is diag(P, −P, 0) |
| C2 | `gauge` | (a) for b̃ = b(t, x−D(t), ρ) − D′(t), the entries (P, Q, Y, h) of the Reduction for X̃ = X(t, x−D) − D′, R̃ = R, at (t, x, ρ), equal those of b at (t, x−D, ρ) (undefined X, R, D); (b) b = c x + C ln ρ + d gives b̃ = c x + C ln ρ + (d − cD − D′), and D = e^{−∫c} ∫ d e^{∫c} satisfies D′ + cD − d = 0 |
| C3 | `lemmaZ` | (a) the elimination ideal of {P + v₂², Q, Y + v₁v₂, 2h − v₁²} (v₀ = 0) in (P, Q, Y, h) (lex basis, v eliminated) equals ⟨Q, 2hP + Y²⟩; (b) that of {P + v₀², Q + v₀v₁, Y, 2h − v₀² − v₁²} (v₂ = 0) equals ⟨Y, Q² + P(2h+P)⟩ (equality: each generator of one basis reduces to 0 modulo the other); (c) through `rank1_lams`: 12 random blocks `v_block(0, v₁, v₂)` (v₁v₂ ≠ 0, small rationals) give exactly [(h + v₂², MM)], 12 `v_block(v₀, v₁, 0)` (v₀v₁ ≠ 0) give exactly [(h, MM)], 12 random (P, Q, 0, Y, h), h > 0, with neither 2hP + Y² = 0 = Q nor Y = 0 = Q² + P(2h+P), give [] |
| C4 | `rho_ode` | `dsolve` of R″ + R′/ρ = 0 (ρ > 0) returns C₁ + C₂ ln ρ (difference zero), and it satisfies the ODE |
| C5 | `branchA` | with X(t, x), C(t), d(t) undefined and R = C ln ρ + d: (i) Q = 0 and ρ²(2hP + Y²) = C²P + (X_x C − C′/2)²; (ii) as a polynomial in ℓ = ln ρ its ℓ-coefficient is −C³ X_xx and its ℓ⁰ part is C²(X_tx − (X + d)X_xx − X_x²) + (X_x C − C′/2)²; (iii) for X = c(t)x + e(t) it equals C²c′ − cCC′ + C′²/4 = C²(c′ − 2γc + γ²), γ = C′/(2C); (iv) on c′ = 2γc − γ²: h − P = C²/(2ρ²) + (γ − c)² equals h + v₂² with v₂ = −Y/v₁, v₁ = C/ρ |
| C6 | `c_ode` | with A(t) > 0, γ(t) undefined, A′ = 2γA, K′ = γ²/A and c = A (k₀ − K): c′ − 2γc + γ² = 0 (so c = |C|(k₀ − K) for any C ≠ 0); for C′ = 0 (γ = 0) c′ = 0; for T2: c = En(1/3 − K), K = −1/(2 En), equals 1/2 + En/3 |
| C7 | `t_ode` | `dsolve` of G′ = 2κ(t)G returns C₁ exp(2∫κ dt), and it satisfies the ODE |
| C8 | `branchB` | (i) X = κ(t)x + e(t), R_ρ = m(t) f(ρ): P = κ′ − κ², Q = −m(f′ + f/ρ)/2, h = m²f²/2, and Q² + P(2h + P) = m²g − p m²f² + p² with p = κ² − κ′, g = (f′ + f/ρ)²/4; (ii) E_B(p_j, m_j, F_i, g_i) = m_j²g_i − p_j m_j² F_i + p_j² = 0 for j = 1, 2 and i = a, b, with 1 − s p₁p₂m₁m₂(F_a − F_b): p₁ − p₂ and m₁² − m₂² reduce to 0 modulo the Gröbner basis; (iii) f = f₀ constant, g = f₀² ι²/4 at ι_a = 1/ρ_a, ι_b = 1/ρ_b (ρ_aι_a = 1 = ρ_bι_b), with 1 − s p m f₀ (ρ_a − ρ_b)(ι_a + ι_b): the Gröbner basis is [1] |
| C9 | `planted` | P1–P4 through `run_family`: (a) 4D coordinate Ricci; (b) at 3 exact points `same_sign_form` has a root equal to λ = C²/(2ρ²) + (γ − c)² (from b by the chain rule: C = ρ b_ρ, γ = C′/(2C), c = b_x) with inertia (0, 2) and pattern MM; (c) Q and 2hP + Y² from `blocks` on the jets of b are zero; (d) F1: no root with a pattern at 3 of 3 points and 2hP + Y² ≠ 0 |
| C10 | `family` | T1–T4 as C9 (a)–(c); C′ = d/dt(ρ b_ρ) ≠ 0 (not gauge-equivalent to a static member); c′ − (2γc − γ²) = 0 from the chain rule; for T4, γ − c = 0 and the root equals h; F2: no root with a pattern at 3 of 3 points and 2hP + Y² ≠ 0 |
| C11 | `identity` | b = c(t)x + C(t) ln ρ + d(t), c, C, d undefined: R_ab − [λ(g_ab − ρ² dφ_a dφ_b) − α_a α_b], α = (C/ρ)(dx + b dt) + (γ − c) dρ, λ = C²/(2ρ²) + (γ−c)², is the zero matrix after c′ → 2γc − γ²; with M = −α⊗α − λρ² dφ⊗dφ, M(n, ·) = 0 and M(K₂, ·) = 0 for K₂ = (γ − c)∂_x − (C/ρ)∂_ρ |
| C12 | `closure_general` | (a) [n, K₂] − (C′/C)K₂ has components (0, r, 0, 0), r = w′ + wc − 2γw − C²/ρ² (w = γ − c), and ∂_ρ r = 2C²/ρ³; (b) the coefficient F of dt∧dx∧dρ∧dφ in α ∧ dα ∧ dφ equals C³/ρ³ + (C/ρ)(−w′ + (2γ − c)w) and ∂_ρ(ρF/C) = −2C²/ρ³ (computed from the form components, independent of (a) apart from α) |
| C13 | `closure_points` | `closure2` of M = R − λg for P1, P3, P4, T1, T2, T3, T4 (λ as in C9): kernel dimension 2 and not integrable; positive control of the same call: A0: dimension 2, integrable, L_X M = 0, quotient flat |
| C14 | `localized` | b_xx = 0 and b_x = c(t) for the family; setting c = 0 in c′ = 2γc − γ² gives γ² = 0 (sympy `solve`), so C′ = 0; the gauge of C2(b) with c = 0 is D′ = d |

Controls are `--mutate=NAME`; each must exit non-zero with exactly its target checks failing (extra failures are reported,
not adjusted). A control that exits 0, or whose failing checks differ from its target list, is reported as silent or off
target. **Targets are declared in a dated amendment after a development run computes them** (the rule of this task);
until then only the names and the intended change are listed.

| control | intended change | intended check |
|---|---|---|
| `block-P` | P built without −X_x² | `block` |
| `gauge-drop` | b̃ without −D′(t) | `gauge` |
| `gauge-ode` | D′ − cD = d in place of D′ + cD = d | `gauge` |
| `lemmaZ-A` | claims ⟨Q, 2hP − Y²⟩ | `lemmaZ` |
| `lemmaZ-B` | claims ⟨Y, Q² − P(2h+P)⟩ | `lemmaZ` |
| `lemmaZ-blocks` | the B-blocks built with P = +v₀² | `lemmaZ` |
| `rho-dsolve` | solves R″ + 2R′/ρ = 0 and compares with C₁ + C₂ ln ρ | `rho_ode` |
| `A-P` | P built with X in place of X + R | `branchA` |
| `A-ode` | the claimed ODE expression with −C′²/4 | `branchA` |
| `c-ode` | K′ = −γ²/A | `c_ode` |
| `t-dsolve` | claims G = C₁ exp(∫κ) | `t_ode` |
| `B-claim` | claims m₁ − m₂ in the ideal | `branchB` |
| `B-const` | g = f₀²/4 (the 1/ρ² dropped) in the f-constant case | `branchB` |
| `plant-pert` | P1 replaced by F1 in the list that must be found | `planted` |
| `fam-ode` | T2 replaced by F2 in the list that must be found | `family` |
| `ident-ode` | c′ → 2γc + γ² | `identity` |
| `ident-alpha` | α with (c − γ) dρ | `identity` |
| `closure-bracket` | the commutator without the K₂(b) term | `closure_general` |
| `closure-form` | α without the b dt term | `closure_general` |
| `closure-C0` | two of the seven members replaced by A0 | `closure_points` |
| `loc-claim` | the ODE claimed as c′ = 2γc − γ²c | `localized` |

## Files and runs

`run_step.sh NAME command...` writes `logs/NAME.log`, `.rc` and `.time` (`/usr/bin/time -v`), refuses to overwrite a log, and runs
at nice 10. Long runs are launched with `systemd-run --user --unit=nm-i166-<step>`. Every log is kept; a rerun gets a new number.

## Amendments (dated; the criteria above stay as first written, these say what the code tests)

**A1 (2026-11-25, after dev runs `dev_1` to `dev_3` and the dev control batch `ctl_dev1_*`/`ctl_dev2_*`, before any run of record).**
No criterion above was changed. What the dev runs showed and what the code does:

- **`gauge-drop` was silent in the first dev control batch** (`ctl_dev1_gauge-drop.log`, exit 0, `gauge` passed). Cause: a bug in
  the check code, not in the criterion. `to_jets` replaced the function X(t, x) inside its own derivatives before replacing the
  derivatives, so every entry of C2(a) became 0 and `dev_1`, `dev_2` and the batch compared 0 = 0 (a vacuous pass). Found by the
  silent control. Fixed: derivatives are replaced first, and the script asserts that the compared P entries contain the jet
  symbol X_11 (a vacuous comparison now crashes). After the fix `dev_3` passes 14 of 14 and `gauge-drop` and `gauge-ode` fire on
  `gauge` (`ctl_dev2_gauge-drop`, `ctl_dev2_gauge-ode`). The other 20 controls fired in the first batch.
- **Control targets, declared now from those dev runs** (each control fails exactly one check and no other; the dev logs show which
  sub-criterion fails, e.g. `B-const` fails only (iii) of `branchB`, `B-claim` only (ii), `closure-bracket` only (a) and
  `closure-form` only (b) of `closure_general`). The targets equal the intended checks of the table above, so no prediction
  changed: `block-P`: `block`; `gauge-drop`, `gauge-ode`: `gauge`; `lemmaZ-A`, `lemmaZ-B`, `lemmaZ-blocks`: `lemmaZ`; `rho-dsolve`:
  `rho_ode`; `A-P`, `A-ode`: `branchA`; `c-ode`: `c_ode`; `t-dsolve`: `t_ode`; `B-claim`, `B-const`: `branchB`; `plant-pert`:
  `planted`; `fam-ode`: `family`; `ident-ode`, `ident-alpha`: `identity`; `closure-bracket`, `closure-form`: `closure_general`;
  `closure-C0`: `closure_points`; `loc-claim`: `localized`. Every check has at least one control.
- **Wording that the code tests as follows** (the README sentence was looser or longer than the code; the code is the criterion):
  (1) "All criteria are exact (no floating point decision)": `same_sign_form` takes the inertia of R − λg from 60-digit
  eigenvalues (as in #78 and #158); the minors, the roots λ and everything else are exact, and the matrices here are rational,
  so the inertia is a numerical computation on exact data. (2) C5(ii) as coded tests the ℓ-coefficient and the ℓ⁰ part and
  nothing about the degree (`dev_1` also tested "degree 1"; removed before `dev_2`, which is not a loosening: the identity (i)
  already fixes the whole expression). (3) C6 as coded also checks K′ = γ²/A for the T2 data (K = −1/(2 En)), which the
  sentence implies. (4) C14 as coded also checks that the gauge of C2(b) with c = 0 gives d̃ = d − D′ (added before `dev_2`; the
  README line was not coded in `dev_1`). (5) Lemma Z (B) is coded as the elimination ideal ⟨Y, Q² + P(2h + P)⟩ only; the
  inequalities P ≤ 0, 2h + P ≥ 0 (so that v₀ = √(−P), v₁ = √(2h + P) are real) are by hand in the note, and the note states
  (B) in its closed form with P ≤ 0.
- The probes `dev/probe_*` are not runs of the script. `dev_1`, `dev_2` (the vacuous `gauge`), `dev_3`, `ctl_dev1_*` and
  `ctl_dev2_*` are kept.

## Runs of record (2026-11-25; every log is kept, nothing overwritten; the `.rc`, `.time` (`/usr/bin/time -v`) files sit beside each log)

| step | command (from the worktree) | log | exit | wall | result |
|---|---|---|---|---|---|
| probes 1 to 6 | `dev/probe_N.py` | `dev/probe_N.log` | 0 (probe 4: 1, `PolynomialError`) | seconds | before the README, see the table above |
| dev 1 | `--no-controls` (script 7192041) | `logs/dev_1.log` | 0 | 19.7 s | 14 of 14, but `gauge` (a) compared 0 = 0 (A1) |
| dev control batch 1 | `run_controls.sh dev1` (systemd unit `nm-i166-ctldev1`, 21 controls, one process at a time) | `logs/ctl_dev1_*.log`, `ctl_dev1_batch.log` | 1 each, `gauge-drop` **0 (silent)** | about 3 min | 20 of 21 on target, `gauge-drop` silent (A1) |
| dev 2 | `--no-controls` after the edits to C5(ii) and C14 | `logs/dev_2.log` | 0 | 19.7 s | 14 of 14, `gauge` (a) still vacuous |
| fix | `to_jets` replaces derivatives before X; assertion that the compared entries contain X_11 (script 68819a4) | | | | |
| dev 3 | `--no-controls` | `logs/dev_3.log` | 0 | 19.7 s | 14 of 14, `gauge` (a) now non-vacuous |
| dev control batch 2 | `--mutate=gauge-drop`, `--mutate=gauge-ode` | `logs/ctl_dev2_*.log` | 1, 1 | 2 s, 3 s | both fire `gauge` |
| **final 1** | `run_final.sh 1` (systemd unit `nm-i166-final1`), default mode at 68819a4 | `logs/final_1.log` (= `notes/warp/one_sign_time_output.txt`), `.err` empty | 0 | 3:10.25 | 14 of 14 checks, 21 of 21 controls fire on their target, 77 MB peak |

The script is unchanged between `final_1` and the committed branch (`git diff 68819a4 HEAD -- notes/warp/one_sign_time.py` is empty);
the branch commit with the note and the output is 1df365a. No threshold, point set or criterion changed after a failing run of
record; the only failure of record is `gauge-drop` in dev control batch 1, a bug in the check code, fixed and rerun (A1).
