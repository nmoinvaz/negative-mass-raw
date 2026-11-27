# I224-rpi5: junction algebra of the S-brane of [BHR21] and the Schwarzschild–de Sitter gluing, plan, criteria, reading log

Machine rpi5-ubuntu (4 cores, aarch64), one process at a time, `nice -n 10`. Issue: https://github.com/nmoinvaz/negative-mass/issues/224
(source: `notes/baby_universes.md` §4, T4, from #211). Code branch `wip/i224-junction` of negative-mass, files
`notes/baby_universes_junction.py`, `notes/baby_universes_junction_output.txt`, `notes/baby_universes_junction.md`.

This README is written and committed before the run of record. Section 7 lists the development runs that came first, and
section 8 (runs of record) is appended after the run.

## 1. What is derived, in this order

Signature (−+++), G_μν = κ T_μν, κ = 8πG; the physical statements do not depend on it ([BHR21] uses (+−−−)).

1. The junction condition for a spacelike hypersurface: from the singular part of G^μ_ν of the kinked metric
   ds² = −dτ² + A(τ)² dx² + B(τ)² dΩ² (J1, no Israel formula used), and as the Israel formula (J2).
2. Schwarzschild interior at r = r₀ (past) → (i) a homogeneous anisotropic cosmology ds² = −dτ² + a² dx² + b² dΩ², (ii) de Sitter in
   its R × S² slicing a = sinh(Hτ)/H, b = cosh(Hτ)/H (τ > 0, the expanding wedge).
3. [BHR21] (4)–(5) against the derived matching (P1, P2, P3).
4. The shell stress and its NEC and WEC status, for the isotropic S-brane (each sign of the tension) and for the general
   shell (E1, E2, D3 … D6b).
5. [FMM90]: its text was not reachable (section 6); the Schwarzschild–de Sitter matching is derived from the geometry alone.

## 2. Printed equations to compare ([BHR21], arXiv:2105.07166 v1, read on the rendered page 6)

- (1) `S = ∫ d⁴x [ √(−det g) ( ½ R + L_M ) − δ(r − r₀) √(−det q) S ]`, "where g is the determinant of the space-time metric, R is the
  usual Ricci scalar, q is the determinant of the induced metric on the S-brane hypersurface, L_M is the matter Lagrangian, S is
  the tension of the S-brane, and r = r₀ is the location of the S-brane (recall that inside the horizon the coordinate r is
  time-like, and r = 0 is the location of the Schwarzschild singularity)".
- (2) `ds² = f(r) dt² − (1/f(r)) dr² − r² dΩ²`, f = 1 − r_s/r. (3) `ds² = dt² − a(t)² dx² − b(t)² dΩ²`.
- (4) `ȧ/a + √g f′/(2f) = S`.
- (5) `ḃ/b + √g/r₀ = S`.
  "where a prime denotes the derivative with respect to r, and all quantities are evaluated on the matching surface. As is evident,
  a positive S-brane tension is required in order to get expansion to the future of the S-brane."
- Also: the S-brane "carries positive tension but vanishing energy density. This object violates the usual energy conditions";
  its stress tensor is "a positive tension (i.e. negative pressure) and vanishing energy density"; "for a sufficiently large
  S-brane tension the universe to the future of the S-brane is an expanding cosmology". The details are deferred to arXiv:2103.02842
  (not read).
- The text extraction of the paper lost the layout of (4)–(5); they were read from a 130 dpi rendering of page 6 of the PDF
  (sha256 of paper.pdf `48fbbc67…e3a2`, the #211 paper cache). The symbol g in (4)–(5) is the symbol the text calls the determinant
  of the space-time metric; (4)–(5) do not define it otherwise.

## 3. By-hand values (derived before the code was written; typed into the checks as reference values)

Notation: F = r_s/r₀ − 1 > 0 inside the horizon (F = −f(r₀)); K^i_j = ½ h^{ik} L_n h_kj with the future-directed unit normal; [X] = X₊ − X₋
(+ the future side); s = jump of each K^i_j in the isotropic case.

- **H1** [K^i_j] − δ^i_j [K] = κ S^i_j. For S^i_j = diag(p_x, p_θ, p_θ): κ p_x = −2[K^θ], κ p_θ = −([K^x] + [K^θ]); S^n_n = 0 (G^τ_τ has no
  second derivative of A, B). An S-brane of tension σ: p_x = p_θ = −σ, [K^i_j] = κσ/2 for every i.
- **H2** Black-hole interior, n^r = −√F: K^x_x(−) = r_s/(2 r₀² √F) = (F+1)/(2 r₀ √F) > 0, K^θ_θ(−) = −√F/r₀ < 0; Hamiltonian constraint
  R₃ + K² − K^i_j K^j_i = 0 with R₃ = 2/r₀².
- **H3** (4) and (5) are K^x(+) − K^x(−) = s and K^θ(+) − K^θ(−) = s with √g := √(−f(r₀)) = √F. With the action (1) at κ = 1 the derived
  right-hand side is S/2.
- **H4** Thresholds on s for the future rates: ȧ/a > 0 iff s > −(F+1)/(2 r₀ √F) (negative); ḃ/b > 0 iff s > √F/r₀ (positive); volume
  iff s > (3F−1)/(6 r₀ √F), positive iff r₀ < 3 r_s/4. In σ = 2s/κ: ḃ/b > 0 iff σ > 2√F/(κ r₀).
- **H5** S-brane: T_μν k^μ k^ν = −σ for every null k = (1, e); T_μν u^μ u^ν = −σ γ² |v|². General shell (S^n_n = 0): NEC ⇔ WEC ⇔
  p_x, p_θ ≥ 0. [K^θ] = −κ p_x/2, so a shell that satisfies the NEC cannot raise ḃ/b.
- **H6** de Sitter wedge: with c = H r₀ = cosh(Hτ₀), t = sinh(Hτ₀) = √(c²−1): K^x = c²/(r₀ t), K^θ = t/r₀; K^x K^θ = H².
- **H7** Schwarzschild → de Sitter shell: κ r₀ p_x = −2(t + √F) < 0; κ r₀ p_θ = −[(2t²+1)/t + (F−1)/(2√F)]; p_θ can be ≥ 0 only if
  F < (3 − 2√2)² = 17 − 12√2 ≈ 0.0294; K^x K^θ = −(F+1)/(2 r₀²) < 0 on the Schwarzschild side, so no shell-free matching exists; the
  isotropic S-brane exists iff t = 2√F/(3F+1), with s = 3√F (F+1)/(r₀ (3F+1)) > 0.
- **H8** [ρ] = −S^i_j K̄^j_i (Gauss–Codazzi); with isotropic s: κ ρ₊ = s (2K₋ + 3s), K₋ = (1−3F)/(2 r₀ √F), and 2K₋ + 3√F/r₀ = 1/(r₀ √F).

## 4. Checks, criteria and what each shares

Every pass criterion is an exact sympy identity or sign (no tolerance). The script exits 1 if a check fails. A check that fails on
real data is reported, never loosened.

| id | check | criterion | shares with |
|---|---|---|---|
| S0a | Einstein routine: Schwarzschild G^μ_ν = 0 | zero matrix | – |
| S0b | de Sitter R × S² slicing solves G^μ_ν = −3H² δ | zero residual | routine |
| S0a′ | flat FRW: G^τ_τ = −3H², G^i_j = −(2ä/a + H²) | zero residual (sign anchor of the routine) | routine |
| J1b | G^τ_τ has no A″, B″; G^μ_ν linear in them | symbolic | routine |
| J1 | singular part of G^i_j (∫A″ dτ = [A′]) = Israel formula | equal as expressions | routine; K^x = A′/A |
| J2a | K(−) at r = r₀ from ½ L_n g, future normal | equals H2 | none of J1 |
| J2b | K from L_n g equals K from ∇n (Schwarzschild, de Sitter) | equal | – |
| J2c | normal is unit timelike | g(n,n) = −1 | – |
| S0c | Schwarzschild interior as KS cosmology (A = √F, B = r, ṙ = −√F): vacuum equations, and its K equals J2a | zero residual, equal K | metric function f only |
| S0d | Hamiltonian constraint on the Schwarzschild side | ρ = 0 | K of J2a |
| P0a | planted: flat FRW H₁ → H₂ through the junction code | p_s = −2[H]/κ, σ = 2[H]/κ, [ρ] = 3(H₂²−H₁²)/κ (Raychaudhuri, Friedmann) | israel_S only |
| P0b | planted: Schwarzschild(F₁) → Schwarzschild(F₂) at one r₀ | S·K̄ = 0 identically; F₂ = F₁ gives S = 0 | J2a K, israel_S |
| P1 | printed (4), (5) with g := −f(r₀) equal the derived jumps | zero difference | J2a K |
| P2 | dimensions of √g in (4), (5) | exponent 0 for g := −f(r₀), 2 for g read as the determinant | – |
| P3 | S-brane of action (1) at κ = 1: [K^i_j] = σ/2 | exactly 1/2 (the printed RHS is 2×; reported as a finding) | israel_S |
| X1, X2 | thresholds of H4 in s, and their signs | equal to H4 | J2a K |
| X3 | the same in σ, through tension → pressure → jump | equal to H4 | israel_S |
| E1 | isotropic shell: NEC, WEC for σ = +1, 0, −1 | violated, saturated, satisfied | – |
| E2 | general shell: NEC form, [K^θ] = −κ p_x/2, no raising of ḃ/b | identities, sign | israel_S |
| D2 | de Sitter K at b = r₀ from the closed form | equals H6 | – |
| D2b | de Sitter in static form f₂ = 1 − H²r² (r > 1/H), K(+) by the code of J2a | G^μ_ν = −3H² δ and K equal to D2 | routine, J2a code |
| D3 | shell stress Schwarzschild → de Sitter | equals H7; p_x < 0 | israel_S |
| D3b | p_θ sign threshold | the two identities behind 17 − 12√2 | – |
| D4 | no shell-free matching | products of H7 | – |
| D5 | isotropic S-brane into de Sitter | equals H7; H r₀ < 2/√3 with the maximum at F = 1/3 (the derivative of 4F/(1+3F)² is 4(1−3F)/(1+3F)³) | – |
| D6 | Hamiltonian constraint on the de Sitter side, and [ρ] = −S·K̄ | zero residual | israel_S, K |
| D6b | post-brane density of the isotropic S-brane | κρ₊ = s(2K₋+3s), from the + side and from −S·K̄ | israel_S, K |

J1 and J2 are independent routes to the junction condition (the singular part of the Einstein tensor of a kinked metric, and the
Israel formula); they share the metric ansatz and the Einstein routine, which S0a, S0b, S0a′ test on known solutions. S0c and J2a are
two computations of K(−) (a Kantowski–Sachs rewrite of the Schwarzschild interior, and a Lie derivative in Schwarzschild coordinates).

## 5. Mutations and their declared targets

Targets are the checks that must fire. They were computed in the development runs `dev/dev2_mut_*.txt` and, for `ds_orientation` and D2b, `dev/dev3_mut_*.txt` (section 7) before being
declared here and in `MUTATIONS` of the script; `--mutate=all` reruns each and compares. A check that is silent under a mutation is
not a failure of the mutation; the targets are what is required.

| mutation | what it changes | targets that must fire |
|---|---|---|
| `jump_sign` | [K] = K₋ − K₊ in `israel_S` (the sign of the jump of K) | J1 P0a P3 X3 E2 D3 D6 D6b |
| `trace_term` | the −δ^i_j [K] term of the Israel formula dropped | J1 P0a P0b P3 X3 E2 D3 D6 D6b |
| `tension_sign` | p = +σ for the S-brane | P0a P3 X3 E1 |
| `orientation` | Schwarzschild normal n^r = +√F (white-hole interior) | J2a S0c P1 X1 X2 X3 E2 D3 D5 |
| `lapse` | Schwarzschild normal n^r = −F | J2c J2a S0c S0d P0b P1 X1 X2 X3 D3 D4 D5 D6b |
| `printed_g` | g of (4), (5) read as −det g_μν | P1 P2 |
| `ds_swap` | de Sitter a, b exchanged (a = cosh/H, b = sinh/H) | S0b D2 |
| `ds_orientation` | de Sitter static form with n^r = −√(−f₂) | D2b |

Predicted silences (seen in the development runs): `jump_sign` leaves P1, X1, X2, E1, D4, D5 silent (they do not go through the sign of the
jump); `orientation` leaves D6 silent (the constraint is quadratic in K). The acceptance mutation of the issue is `jump_sign`.

## 6. Reading log

| source | read | not read |
|---|---|---|
| [BHR21] arXiv:2105.07166 v1 | all of it again (9 pages with references) from the #211 paper cache; eqs (1)–(5) on the rendered page | arXiv:2103.02842, the companion with the details |
| [FMM90], PRD 41, 383 | INSPIRE and OSTI abstracts only; `reading/fmm90_attempts.txt` lists every attempt | the text (KEK scan KEKSCAN 2000-33-351 = ICTP IC/88/91, rejected by the server; publisher HTTP 403 in #211) |
| [Isr66] Israel, Nuovo Cim. B 44S10, 1 (1966), Erratum B 48, 463 (1967) | INSPIRE record 50008 (title, journal, both DOIs 10.1007/BF02710419 and 10.1007/BF02712210 match [BHR21]'s reference [8]) | the paper |

What the [FMM90] abstract says (OSTI and INSPIRE agree, `reading/osti_6852005_abstract.txt`): the interior is studied "on the assumption that some limiting
curvature exists"; "the Schwarzschild metric inside the black hole can be attached to the de Sitter one at some spacelike junction
surface which may represent a short transition layer"; "the method of massive thin shells by Israel is used to obtain the characteristics
of this layer"; "instead of the singularity the closed world can be formed inside the black hole"; the property "may also be valid in a more
general case provided the gravitation theory is asymptotically free and the limiting curvature exists"; the fate of the evaporating black
hole is "briefly discussed". What it does not say: the layer's stress, any energy condition, the parameters of the matching.

Issue search (negative-mass, `gh search issues`, terms S-brane, limiting curvature, junction, Israel, thin shell, Kantowski): only #211 and
#212 (and this issue) match. #211: the reading that ranked these proposals. #212: its README is the model for recording a printed
equation that disagrees with a derivation.

## 7. Development runs (before this README was committed, and the third before its update)

The script was run in development: `dev/dev_run1.txt` (26 checks, all pass, the script before X3 existed), `dev/dev_run2.txt` (27 checks),
`dev/dev1_mut_*.txt` (mutations, before X3), `dev/dev2_mut_*.txt` (mutations, the script of dev run 2). They were produced by the
script as it stood, uncommitted, in the worktree; the committed script differs from dev run 2 only by the removal of an unused
helper and the MUTATIONS table now holding the declared targets. Not run: a thick-shell (regularized layer) integration of the
Kantowski–Sachs equations.

Runs 1 and 2 of the committed script (27 checks, section 8) met every declared target. Before the run of record the script got three
additions (the D5 extremum, the check D2b and the mutation `ds_orientation`, which the note's wording needs); `dev/dev3_run.txt` and
`dev/dev3_mut_*.txt` are the development run of that script (28 checks pass; `ds_orientation` fires D2b alone, the other seven
mutations fire what they fired before). The target of `ds_orientation` (D2b) is declared in section 5 in the commit that holds
this paragraph, before the run of record, run 3.
