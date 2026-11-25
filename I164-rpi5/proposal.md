# proposal.md: proposed text for `notes/critical_ghost.md` from the slow-rotation and charged-wormhole papers (#164)

Diff against `notes/critical_ghost.md` at main dffa582 (stored as `src/critical_ghost_dffa582.md`, sha256 in
`sha256sums.txt`). Reading task: the note is the coordinator's and is not edited here. The diff block is derived from the
sentences below by `make_diff.py` (anchors are line numbers of the stored copy) and applied with `patch --dry-run` by
`check_quotes.py` (C9). Every sentence carries the ids of the records of `quotes.md` that support it, in braces.
`check_quotes.py` checks that the ids exist, that every number and every double-quoted string of a sentence occurs in a
cited record, that the diff text equals the sentences, and that a sentence tagged {KEEP} is existing text of the base note.
`CALC1` is `recompute_jc.py` (a recompute from the printed tables, not a quote; numbers cited to it are its `VALUE` lines).

Tags proposed for the four new references: [ABKK23] = arXiv:2301.05243, [ABKK24] = arXiv:2403.08387 (Azad, Blázquez-Salcedo,
Khoo, Kunz), [BGKKN25] = arXiv:2510.11406, [BGKKN26] = arXiv:2607.18399 (Blázquez-Salcedo, González-Romero, Khoo, Kunz,
Navarro Moreno). [BGKKN2x] differs from [BGKKKN26] (the 5D paper) by one letter; a rename costs nothing here.

Placement. The 4D slow-rotation result is a linear perturbation result, so it is a new row of the §1.1 table, after the 5D
row (R1). The charged row gets the supercritical result (R5). The two numbers [SN26b] takes from [ABKK23], [ABKK24] get
their own bullets in the §1.2 [SN26b] block (R2, R3). The "Not read" entry is replaced by what is still unread (R4).

## Sentences

### Row R1 table
anchor: after 98 | | Rotating 5D Ellis wormholes
col1: Slowly rotating 4D Ellis–Bronnikov wormholes, radial-led modes to second order in J
col3: [ABKK23], [ABKK24], [BGKKN25], [BGKKN26], [BGKKKN26]
- R1.1 The mode has no first-order correction in J: the numerical first-order term is "compatible with zero", below 10⁻⁷. {L20, M22}
- R1.2 For every C studied, from C = 0 to C = 1.4, the second-order correction to the frequency is positive, so the static mode becomes less unstable with J. {L06, M01, M08, M09, M18}
- R1.3 In the quadratic approximation the mode reaches zero at a critical J_c, with J_c/A about 50 % or less of the limiting value for the C studied. {L07, L08, M07}
- R1.4 J/A is the angular momentum over the throat area A, and its limiting value is that of the extremal Kerr black hole, J/A → 1/(8π) ≈ 0.0397. {L04, L05, M07}
- R1.5 A second unstable mode arises from a zero mode of the static wormhole and becomes more unstable with J, through a negative second-order coefficient. {L11, L12, L15, M11, M13}
- R1.6 The two modes cross at J/A about 0.013, "slightly above 30 %" of the limiting value, for C = 0, 0.05, 0.1 and 0.2. {L13, L14, M14, M15}
- R1.7 The second-mode coefficients are tabulated for those four values of C. {L15, M13}
- R1.8 The authors do not continue the modes past the crossing, because it "is indicating a deficiency of the applied quadratic approximation". {L16, M17}
- R1.9 They conjecture that the two modes "merge and disappear" near the critical value, as in five dimensions. {L17, M16}
- R1.10 [ABKK23] concludes that "the radial instability will disappear at even smaller values of the angular momentum, around 30 %" of the limiting value, so that "for sufficiently rapid rotation the wormholes will be stable". {L18}
- R1.11 [ABKK24] says the true critical angular momentum "is slightly smaller than the angular momentum, where the two perturbatively obtained branches of unstable radial modes cross", and that checking this "will need more sophisticated methods than perturbation theory". {M19, M20}
- R1.12 [ABKK24] also expects the second-order results to be "excellent approximations for most of the range J/A < J_c/A", by analogy with Kerr and Kerr–Newman black holes, where they are excellent "up to 50-60 %" of the extremal bound. {M10}
- R1.13 [BGKKN25] draws the analogy to charge: the slowly rotating wormholes "have two radially unstable modes", and the extrapolated slow-rotation result "showed that the two modes merged around 1/3 of the maximum value of the scaled angular momentum". {H18}
- R1.14 [BGKKN25] reports that for supercritical charged wormholes the two unstable modes merge and continue with equal imaginary parts and opposite real parts, and it says the fate of the rotating modes "can only be confirmed by a non-perturbative study in the future". {H01, H14, H22}
- R1.15 [BGKKN25] adds that "one might be tempted to conjecture that the radial instability disappears at the critical value", but that "this is not the case" for the charged wormholes. {H11, H12}
- R1.16 [BGKKN26] conjectures, by analogy, that the radial instability of 4-dimensional rotating wormholes "will therefore be relaxed for fast rotation as well", and says the fate of the instability at fast rotation "should be clarified". {N09, N10}
- R1.17 [BGKKKN26] says the charged-wormhole merger "can now be recognized as the same characteristic spectral mechanism" as its exceptional point. {A10, G01}

### Row R5 table
anchor: replace 94-94 | | Charged (Maxwell + ghost) wormholes
col1: Charged (Maxwell + ghost) wormholes, 4-parameter family
col3: [GGS09c], [BGKKN25], [BGKKN26]
- R5.1 One growing mode, proven for sub-critical and critical members; numerical evidence for super-critical. {KEEP}
- R5.2 For supercritical members, [BGKKN25] finds two purely imaginary unstable radial modes at small mass, one of which emerges from a zero mode. {H11}
- R5.3 The two modes merge at a critical mass and charge and continue with equal imaginary parts and opposite real parts. {H11, H14}
- R5.4 The imaginary part tends to zero as the extremal Reissner–Nordström limit is approached, and the instability timescale can then be arbitrarily large. {H16, H17, H20, N07}
- R5.5 [BGKKN25] calls the supercritical wormholes short of that limit "not yet fully radially stable". {H17}
- R5.6 For critical and subcritical members [BGKKN26] finds a single unstable radial mode, and for subcritical ones the instability "does not seem to completely vanish as long as M/r_T<1". {N05, N08}

### Row R2 bullets
anchor: after 151 |       endpoint;
- R2.1 [SN26b] sets that 32 % beside "the zero of their second-order rate for this family (33 % on this axis)", the family being C = 1 in the notation of [ABKK23], [ABKK24]. {X02, X07}
- R2.2 A percentage of 33 is printed in none of [ABKK23], [ABKK24], [BGKKN25] and [BGKKN26]. {N13, N14, N16}
- R2.3 Recomputed from the coefficients printed in [ABKK23], [ABKK24], the crossing of the two modes is 32.6 to 33.0 % of 1/(8π) for C = 0, 0.05, 0.1 and 0.2, consistent with the "around 1/3" that [BGKKN25] gives for the merger. {CALC1, H18}
- R2.4 The zero of the main-mode rate at C = 1, recomputed the same way with the throat area printed in [ABKK23], is 41.9 % of 1/(8π), or 53.3 % with the minimal-surface area; the first reproduces Fig. 6 of [ABKK24]. {CALC1, L19, M04}
- R2.5 So 33 % equals the recomputed crossing at C = 0.2 to the digit shown, and not the C = 1 zero obtained this way. {CALC1, X02}
- R2.6 [ABKK23] prints the area only for the static wormhole and says A is "obtained in second order", and [ABKK24] prints no formula for A. {L04, L19, N19}

### Row R3 bullets
anchor: after 158 |       and the perturbative τ
- R3.1 The second-mode crossings of [ABKK23], [ABKK24] are drawn for C = 0, 0.05, 0.1 and 0.2, and the evolutions of [SN26b] "use C=1". {X03, L14, M14}
- R3.2 [SN26b] reads [ABKK23], [ABKK24] as giving "a positive O(J²) correction for every asymmetry" and a second mode for "nearly symmetric wormholes". {S04}
- R3.3 [ABKK23] says "for every value of C we have studied" and [ABKK24] tabulates C = 0 to 1.4; [ABKK24] says the second mode starts from a zero mode "independent of C"; the words "nearly symmetric" occur in neither. {L06, M09, M12, N17}
- R3.4 [SN26b] writes that the authors "conjecture that the modes merge beyond the reliable range of the quadratic approximation and the instability disappears". {S05}
- R3.5 The phrase "reliable range" is not in the sources, which attribute the crossing to "a deficiency of the applied quadratic approximation" and to "a deficiency of the current perturbative approach". {L16, M17, N20}
- R3.6 [SN26b] writes that in the charged analogue the merged modes "continue as a complex pair (oscillating growth)", and that the growth rate "reaches zero only in the extremal limit". {S06}
- R3.7 [BGKKN25] and [BGKKN26] give equal imaginary parts and opposite real parts for the pair, and neither uses the words "oscillating growth" or "oscillatory instability". {H14, N06, H26, N12}
- R3.8 No charged-wormhole paper says the growth rate reaches zero "only" in the extremal limit; what they say is in the charged row. {N15}

### Row R4 entry
anchor: replace 530-532 |   - the slow-rotation and charged-wormhole papers
- R4.1 The radial spectrum of the supercritical charged wormholes in [GGS09c], to compare with the two unstable modes that [BGKKN25] finds there. {H11}
- R4.2 The quadrupole-perturbation paper of the same group, which [SN26b] says "derives the equations for quadrupole perturbations". {X06}
- R4.3 The study of rapidly rotating wormholes that [BGKKN26] cites for "did not show any instabilities". {N09}

## Diff

<!-- diff:begin -->
```diff
--- a/notes/critical_ghost.md
+++ b/notes/critical_ghost.md
@@ -91,11 +91,12 @@
 |---|---|---|
 | Static spherically symmetric wormholes of a massless ghost scalar, the full 2-parameter family (throat radius, product of the asymptotic masses) | **Exactly one** exponentially growing mode: proven for γ₁ ≠ 0, where the operator is factorized with the zero mode 1/Ψ₀ and a nodal argument gives exactly one bound state; for γ₁ = 0 that zero mode is not normalizable, a Rayleigh–Ritz bound gives a bound state and uniqueness is asserted by continuity (the symmetric case is proved in every D in `wormhole_largeD/one_mode.md`). Time scale T = τ/r_throat, τ the proper time at the throat, T = e^{2γ₁ arctan γ₁}/(√(1+γ₁²) β) in the units b = 1, γ₀ = 0: 0.846 (γ₁ = 0), 0.758 (1/2), 0.675 (1), 0.618 (2), 0.608 (2.5), 0.594 (5), 0.5897 (10) → 0.58835 (γ₁ → ∞). Both rows of Table I are reproduced at 32 values to their 3 digits (`ellis_efold.md`, #151, #163). The limit is 1/β̂ = 0.588351 from [GGS09a]'s own limit equation, solved from the TeX ([GGS09a] print 0.588); the table's 0.590 is T at γ₁ ≈ 8–10 rounded, and T falls like γ₁⁻² to 0.58835 (numerical evidence) | [GGS09a] |
 | Same, in n = 4…11, 20, 50, 100 spacetime dimensions | One negative ω² in every n. ω²a² = −1.397, −2.985, −4.687, −8.290, −12.044 (n = 4, 5, 6, 8, 10); −31.6, −91.3, −191.3 (n = 20, 50, 100). Faster in higher n | [TS13] |
-| Charged (Maxwell + ghost) wormholes, 4-parameter family | One growing mode, proven for sub-critical and critical members; numerical evidence for super-critical | [GGS09c] |
+| Charged (Maxwell + ghost) wormholes, 4-parameter family | One growing mode, proven for sub-critical and critical members; numerical evidence for super-critical. For supercritical members, [BGKKN25] finds two purely imaginary unstable radial modes at small mass, one of which emerges from a zero mode. The two modes merge at a critical mass and charge and continue with equal imaginary parts and opposite real parts. The imaginary part tends to zero as the extremal Reissner–Nordström limit is approached, and the instability timescale can then be arbitrarily large. [BGKKN25] calls the supercritical wormholes short of that limit "not yet fully radially stable". For critical and subcritical members [BGKKN26] finds a single unstable radial mode, and for subcritical ones the instability "does not seem to completely vanish as long as M/r_T<1". | [GGS09c], [BGKKN25], [BGKKN26] |
 | Ghost scalar with a potential: Ellis–Bronnikov and an AdS wormhole | Ellis–Bronnikov: a unique bound state; the asymmetric case also has a zero-energy mode growing linearly in t (a move along the family). AdS wormhole: exactly one unstable mode | [CPS20] |
 | All static V = 0 scalar-vacuum solutions, both signs | All unstable under spherical perturbations: Fisher (normal; solutions for *every* ω² < 0), anti-Fisher branches A, B and wormhole branch C. Branch A tends to Schwarzschild and its instability fades there | [BFZ11] |
 | Phantom with a specific potential (M-AdS wormholes, "black universes") | Unstable, except black universes whose horizon sits at the area minimum | [BKZ12] |
 | Rotating 5D Ellis wormholes, equal angular momenta J₁ = J₂ | Rotation adds a second unstable mode, the descendant of the static wormhole's non-normalizable zero mode [BGKKKN26]. The two merge at \|J\|/A = 0.10063 for symmetric wormholes and at 0.1381 for a non-symmetric family (\|a₋∞\| = 1) [DFKKR13]. [DFKKR13] found no unstable mode beyond the merger "within the type of modes investigated" and concluded that rotation "may stabilize wormholes" if "no new unstable modes of a different type appear"; its abstract says the static mode "vanishes when the angular momentum exceeds some critical value". [BGKKKN26] (exact background, symmetric family only, cohomogeneity-one gravitational sector) puts the merger at 0.100628 and follows the pair past it as ω± = ±ω_R + iω_I, ω_I > 0: an oscillatory instability, "not stabilization". It says [DFKKR13] "correctly located the merger" but could not follow the modes past it. ω_I A^{1/3} falls to order 10⁻⁶ toward the extremal Myers–Perry limit \|J\|/A = 0.5, consistent with ω_I ∼ (\|J\|/A − 0.5)⁶, and the symmetric wormholes are linearly unstable in that sector. A is the throat area; the printed \|J\|/A need 4πG = 1, which neither paper states (recomputed from the exact solution, #152) | [DFKKR13], [BGKKKN26] |
+| Slowly rotating 4D Ellis–Bronnikov wormholes, radial-led modes to second order in J | The mode has no first-order correction in J: the numerical first-order term is "compatible with zero", below 10⁻⁷. For every C studied, from C = 0 to C = 1.4, the second-order correction to the frequency is positive, so the static mode becomes less unstable with J. In the quadratic approximation the mode reaches zero at a critical J_c, with J_c/A about 50 % or less of the limiting value for the C studied. J/A is the angular momentum over the throat area A, and its limiting value is that of the extremal Kerr black hole, J/A → 1/(8π) ≈ 0.0397. A second unstable mode arises from a zero mode of the static wormhole and becomes more unstable with J, through a negative second-order coefficient. The two modes cross at J/A about 0.013, "slightly above 30 %" of the limiting value, for C = 0, 0.05, 0.1 and 0.2. The second-mode coefficients are tabulated for those four values of C. The authors do not continue the modes past the crossing, because it "is indicating a deficiency of the applied quadratic approximation". They conjecture that the two modes "merge and disappear" near the critical value, as in five dimensions. [ABKK23] concludes that "the radial instability will disappear at even smaller values of the angular momentum, around 30 %" of the limiting value, so that "for sufficiently rapid rotation the wormholes will be stable". [ABKK24] says the true critical angular momentum "is slightly smaller than the angular momentum, where the two perturbatively obtained branches of unstable radial modes cross", and that checking this "will need more sophisticated methods than perturbation theory". [ABKK24] also expects the second-order results to be "excellent approximations for most of the range J/A < J_c/A", by analogy with Kerr and Kerr–Newman black holes, where they are excellent "up to 50-60 %" of the extremal bound. [BGKKN25] draws the analogy to charge: the slowly rotating wormholes "have two radially unstable modes", and the extrapolated slow-rotation result "showed that the two modes merged around 1/3 of the maximum value of the scaled angular momentum". [BGKKN25] reports that for supercritical charged wormholes the two unstable modes merge and continue with equal imaginary parts and opposite real parts, and it says the fate of the rotating modes "can only be confirmed by a non-perturbative study in the future". [BGKKN25] adds that "one might be tempted to conjecture that the radial instability disappears at the critical value", but that "this is not the case" for the charged wormholes. [BGKKN26] conjectures, by analogy, that the radial instability of 4-dimensional rotating wormholes "will therefore be relaxed for fast rotation as well", and says the fate of the instability at fast rotation "should be clarified". [BGKKKN26] says the charged-wormhole merger "can now be recognized as the same characteristic spectral mechanism" as its exceptional point. | [ABKK23], [ABKK24], [BGKKN25], [BGKKN26], [BGKKKN26] |
 | Neutron star with a wormhole core (ghost with quartic coupling) | Linearly unstable | [DFKK13] |
 
 Two remarks.
@@ -149,6 +150,16 @@
     - rotation slows the collapse: the areal radius's e-fold time rises from 5.4 (static) to 13.3 at 24 %; the fitted rate
       extrapolates to zero at 32 %, against 33 % from second-order perturbation theory, an extrapolation and not a measured
       endpoint;
+    - [SN26b] sets that 32 % beside "the zero of their second-order rate for this family (33 % on this axis)", the
+      family being C = 1 in the notation of [ABKK23], [ABKK24].
+    - A percentage of 33 is printed in none of [ABKK23], [ABKK24], [BGKKN25] and [BGKKN26].
+    - Recomputed from the coefficients printed in [ABKK23], [ABKK24], the crossing of the two modes is 32.6 to 33.0 % of
+      1/(8π) for C = 0, 0.05, 0.1 and 0.2, consistent with the "around 1/3" that [BGKKN25] gives for the merger.
+    - The zero of the main-mode rate at C = 1, recomputed the same way with the throat area printed in [ABKK23], is
+      41.9 % of 1/(8π), or 53.3 % with the minimal-surface area; the first reproduces Fig. 6 of [ABKK24].
+    - So 33 % equals the recomputed crossing at C = 0.2 to the digit shown, and not the C = 1 zero obtained this way.
+    - [ABKK23] prints the area only for the static wormhole and says A is "obtained in second order", and [ABKK24]
+      prints no formula for A.
     - the 28.8 % and 33 % models expand instead; the direction depends on the effective perturbation, and the authors say this
       shows growth "without identifying a second eigenmode";
     - at 81 % (D90) no growing departure through t = 150, about 28 static e-folding times, at three resolutions; D75 and D80
@@ -156,6 +167,22 @@
       perturbations present, and say the runs "bound growth only over that span";
     - only axisymmetric data and only C = 1 were evolved; the perturbative mode crossings they compare with concern C ≤ 0.2,
       and the perturbative τ is a linear mode in Killing time while theirs is a fit of the nonlinear areal radius;
+    - The second-mode crossings of [ABKK23], [ABKK24] are drawn for C = 0, 0.05, 0.1 and 0.2, and the evolutions of
+      [SN26b] "use C=1".
+    - [SN26b] reads [ABKK23], [ABKK24] as giving "a positive O(J²) correction for every asymmetry" and a second mode for
+      "nearly symmetric wormholes".
+    - [ABKK23] says "for every value of C we have studied" and [ABKK24] tabulates C = 0 to 1.4; [ABKK24] says the second
+      mode starts from a zero mode "independent of C"; the words "nearly symmetric" occur in neither.
+    - [SN26b] writes that the authors "conjecture that the modes merge beyond the reliable range of the quadratic
+      approximation and the instability disappears".
+    - The phrase "reliable range" is not in the sources, which attribute the crossing to "a deficiency of the applied
+      quadratic approximation" and to "a deficiency of the current perturbative approach".
+    - [SN26b] writes that in the charged analogue the merged modes "continue as a complex pair (oscillating growth)",
+      and that the growth rate "reaches zero only in the extremal limit".
+    - [BGKKN25] and [BGKKN26] give equal imaginary parts and opposite real parts for the pair, and neither uses the
+      words "oscillating growth" or "oscillatory instability".
+    - No charged-wormhole paper says the growth rate reaches zero "only" in the extremal limit; what they say is in the
+      charged row.
     - v1 (21 Oct 2026) said "no evidence of instability"; v2 drops it (#152);
     - *Added by the coordinator:* the paper also notes that above about 29 % the throat's equator lies inside an ergoregion,
       and that horizonless rotating objects with an ergoregion are generically subject to a slow nonaxisymmetric instability,
@@ -527,9 +554,11 @@
   - the GMG96 perturbation section (only its abstract and the LRR summary);
   - [MGM26] (quoted from choptuik-large-d);
   - the citers of [SH02] other than those opened (title and abstract only).
-  - the slow-rotation and charged-wormhole papers that [BGKKKN26] and [SN26b] cite for the 4D and charged cases (Azad et
-    al., arXiv:2301.05243 and 2403.08387; Blázquez-Salcedo et al., arXiv:2510.11406 and 2607.18399; ids from [BGKKKN26]'s
-    TeX comments, *(unverified)*): their results appear here only as [BGKKKN26] and [SN26b] state them.
+  - The radial spectrum of the supercritical charged wormholes in [GGS09c], to compare with the two unstable modes that
+    [BGKKN25] finds there.
+  - The quadrupole-perturbation paper of the same group, which [SN26b] says "derives the equations for quadrupole
+    perturbations".
+  - The study of rapidly rotating wormholes that [BGKKN26] cites for "did not show any instabilities".
 - **Citers of [SH02]:** INSPIRE record 586606 had 222 citing records on 2026-11-24. All titles and 34 abstracts were read,
   and 11 papers were opened (#50; negative-mass-raw `I50-rpi5/quotes.md`, item 5). Only [SN26] calls the wormhole
   threshold a "type-I critical solution".
```
<!-- diff:end -->

References (bibliographic data, verified by `verify_ids.py` (C0) against the arXiv abs pages and INSPIRE; not covered by C3, C5, C6).
After [BGKKKN26] and [SN26b] in the References list:

```diff
--- a/notes/critical_ghost.md  (References)
+++ b/notes/critical_ghost.md
+- [ABKK23] B. Azad, J. L. Blázquez-Salcedo, F. S. Khoo, J. Kunz, "Are slowly rotating Ellis-Bronnikov wormholes stable?",
+  arXiv:2301.05243 (v2, 23 Nov 2023; PLB 848, 138349 (2024), journal reference from INSPIRE).
+- [ABKK24] B. Azad, J. L. Blázquez-Salcedo, F. S. Khoo, J. Kunz, "Radial perturbations of Ellis-Bronnikov wormholes in slow
+  rotation up to second order", arXiv:2403.08387 (v1, 13 Mar 2024; PRD 109, 124051 (2024)).
+- [BGKKN25] J. L. Blázquez-Salcedo, L. M. González-Romero, F. S. Khoo, J. Kunz, P. Navarro Moreno, "Radial perturbations of
+  charged wormholes" (v1 title "Charged wormholes can be long-lived"), arXiv:2510.11406 (v2, 13 Mar 2026; PLB 875, 140335 (2026)).
+- [BGKKN26] the same five authors, "Nonradial perturbations of static charged wormholes", arXiv:2607.18399 (v2, 8 Oct 2026;
+  PRD 114, 084019 (2026)).
```

## Answers to the four questions (ids are those of `quotes.md`)

1. **S04.** In the slow-rotation papers, in other words, with one added qualifier. Static mode: "for every value of $C$ we
   have studied, the second order correction to the mode is positive" (L06, [ABKK23] Sec. 5, both versions), "for all values
   of the asymmetry parameter of the wormholes considered" (M18, [ABKK24] Sec. VI); C = 0 to 1.4 in Table I (M09); no linear
   term (L20, M22). Second mode: "a zero mode of the static wormholes changes into a second unstable radial mode" (L11);
   "independent of $C$, this second unstable mode starts from a zero mode in the static limit" (M12). Not in the sources:
   "nearly symmetric" (N17). The second-mode coefficients and curves are for C = 0, 0.05, 0.1, 0.2 (L15, L14, M13, M14), so
   "nearly symmetric" is [SN26b]'s reading of the range shown, not a restriction the authors state.
2. **S05.** Yes, in [ABKK23] Sec. 5 and 6 and [ABKK24] Sec. I, V, VI, in words that include "disappear": "both unstable
   modes will change much more rapidly, approach each other, merge and disappear" (L17); "the radial instability will
   disappear at even smaller values of the angular momentum, around $30\%$ of the limiting value" (L18); "we expect that the two
   branches merge at some special value $J_s/A$ of the angular momentum $J/A$ and disappear" (M16); "Consequently these rotating wormholes then no longer feature a radial
   instability for $J/A > J_s/A$" (M16). It is a conjecture: "we only conjecture here" (M19), "will need more
   sophisticated methods than perturbation theory" (M20). The merged modes are those of the main and the second unstable
   mode. "Beyond the reliable range of the quadratic approximation" is [SN26b]'s phrase; the sources say the crossing "is
   indicating a deficiency of the applied quadratic approximation" (L16, M17) and also that second order "should be
   excellent" for "most of the range J/A < J_c/A" (M10), with J_c/A about 50 % or less (M07). They do not reconcile the
   crossing at about 30 % (L13, M15) with that range.
3. **S06 and A10.** In [BGKKN25] (Results, Conclusions) and [BGKKN26] (Sec. 5.4.3, 6), for the radial sector of supercritical
   charged wormholes: two purely imaginary unstable modes merge and "two modes that possess the same imaginary part
   but opposite real parts" (H14, H01, N06, N08); this is A10's sentence. "Complex pair" is [SN26b]'s paraphrase of
   that; "oscillating growth" is in neither paper (N12, H26). The imaginary part "tends very fast to zero" toward the
   extremal limit (H07, H16, N07); "only" is in neither paper (N15). Nearest: "while not yet fully radially stable" (H17),
   "the instability does not seem to completely vanish as long as $M/r_T<1$" (N05, subcritical members). Both papers
   conjecture the analogue for rotation, [BGKKN25] with the fate "can only be confirmed by a non-perturbative study" (H22),
   [BGKKN26] that the 4D instability "will therefore be relaxed for fast rotation" (N09). The nonradial paper [BGKKN26]
   contains a radial subsection per class (5.2.3, 5.3.3, 5.4.3), so the claim is in both.
4. **33 % and C <= 0.2.** Neither number is a quotation: "33 %" is printed in none of the four papers (N13, N14, N16).
   The C <= 0.2 is the range of the second-mode tables and captions (L15, L14, M13, M14), which [SN26b] reads in X03.
   Printed: the crossing "around $J/A\approx0.013$, slightly above $30\%$ of the limiting value" (L13, M15), and "around
   $1/3$" in [BGKKN25] (H18). Normalization: J is read off at infinity (M05) with $w\to 2J/r^3$, i.e. G = 1 (CALC1, P5; neither
   paper states G, N18); A is the throat area, "obtained in second order" (L04) but printed only for the static wormhole
   (L19), at r = 0, which for C != 0 is not the minimal surface (M04, M23, CALC1 P6); the limit J/A -> 1/(8 pi) is extremal
   Kerr (L05, M07). Recompute: the crossing is 32.6 to 33.0 % of 1/(8 pi) for C <= 0.2, and the zero of the C = 1 main-mode
   rate is 41.9 % (53.3 % with the minimal-surface area); the 41.9 % reproduces Fig. 6 of [ABKK24]. So [SN26b]'s 33 % equals
   the crossing at C = 0.2 and is not the C = 1 zero that [SN26b] says it is, unless [SN26b] converted with an area the
   sources do not print.

## What the papers do not settle

- Which area [SN26b] used for "33 % on this axis". [ABKK23], [ABKK24] do not print A to second order (N19, L19). The recompute
  gives 41.9 % or 53.3 % for the C = 1 zero and 33.0 % for the C = 0.2 crossing.
- Whether the merger of the two 4D modes lies inside the range where second order is reliable: L16, M17 against M10.
- The second mode for C > 0.2: no value is printed (L15, M13).
- Whether the nonperturbative 4D modes merge and disappear ([ABKK23], [ABKK24]) or continue as a pair with opposite real
  parts ([BGKKN25], [BGKKN26] by analogy): no 4D calculation beyond second order is in the four papers (N10, H22, M20).
- What [GGS09c] found for supercritical members (not read): the note's charged row says one growing mode there.
- The figure readings behind CALC1 P2 are by eye (about 0.00005); the formula J_c/A with the r = 0 area reproduces them
  within 0.0001 at C = 0, 1.0, 1.4, which the minimal-surface area does not.

## Not carried into the proposed text

- Priority statements: [BGKKN25] v2 "This bifurcation is a novel result that has not been observed in" [GGS09c] (H15; v1 says
  "see also"), [BGKKKN26]'s "first explicit identification" (I152), [ABKK23]'s "first evidence" (not quoted).
- The v1 wording of [BGKKN25] ("become effectively stabilized", H24; "long-lived", H23), which v2 drops.
- The nonradial polar instability of static massive Ellis wormholes for M/r_T above about 0.3 (N01, N11): it concerns
  nonradial modes, so the note's statement of one unstable mode (radial) stands, but the note does not mention it.
- The printed exponent of [BGKKN25] Eq. (6), omega_I ∝ (1 - M/r_T)^-3.1, diverges at M/r_T = 1; its own text and Fig. 2
  inset use tau_0, and [BGKKN26] prints omega_I ~ (1 - M/r_T)^3.1 (N04) and tau ~ (1 - M/r_T)^-3.1 (N05) (H09, H10).
