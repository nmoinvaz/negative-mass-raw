# proposal.md: proposed rewrite of the rotating-wormhole entries of `notes/critical_ghost.md`

Diff against `notes/critical_ghost.md` at main 1305816. Reading task: the note is the coordinator's and is not edited here.
Every sentence below carries the quote ids (`quotes.md`) that support it, in braces. `check_quotes.py` checks that the ids exist,
that every number and every double-quoted string in a sentence occurs in a cited quote, and that the diff text equals the
sentences. CALC1 is `jovera_check.py` (a recompute from the exact solution of arXiv:2610.38659, not a quote).

Tags proposed for the two new references: [BGKKKN26] = arXiv:2610.38659, [SN26b] = arXiv:2610.29941 ([SN26] is already
arXiv:2610.13206). The first row's cell is long because each sentence is one claim; sentences 6–11 may move to a remark below
the table. The 4D result is a nonlinear evolution, so it is proposed for §1.2 "Recent", not for the §1.1 table.

## Sentences

### Row R1 table

- R1.1 For J > 0 there are two unstable modes: the static wormhole's mode and a second one that descends from its non-normalizable zero mode. {D12, D23, A02}
- R1.2 The two modes merge at a critical \|J\|/A of 0.10063 for symmetric wormholes in [DFKKR13] and of 0.100628 in [BGKKKN26]. {D14, D15, A03, A26}
- R1.3 [DFKKR13] also gives 0.1381 for a non-symmetric family (\|a₋∞\| = 1), where the instability persists to faster rotation. {D16, D19}
- R1.4 [DFKKR13] found no further unstable mode beyond the merger "within the type of modes investigated". {D17}
- R1.5 [DFKKR13] concluded that rotation "may stabilize wormholes" if "no new unstable modes of a different type appear". {D18}
- R1.6 The abstract of [DFKKR13] is stronger: the unstable mode of the static wormhole "vanishes when the angular momentum exceeds some critical value". {D01}
- R1.7 [BGKKKN26] continues the pair past the merger as ω± = ±ω_R + iω_I with ω_I > 0, an oscillatory instability. {A04, A33, A36}
- R1.8 [BGKKKN26] calls the earlier apparent loss of the instability "not stabilization". {A04}
- R1.9 [BGKKKN26] says the real-eigenvalue calculation of [DFKKR13] "correctly located the merger" but could not follow the modes past it. {A34}
- R1.10 Past the merger the dimensionless growth rate ω_I A^{1/3} falls to order 10⁻⁶. {A37}
- R1.11 The data are consistent with ω_I ∼ (\|J\|/A − 0.5)⁶ toward the extremal Myers–Perry limit at \|J\|/A = 0.5. {A39}
- R1.12 [BGKKKN26] treats linear perturbations in the cohomogeneity-one gravitational sector and concludes that the symmetric rotating wormholes are linearly unstable there. {A43, A19}
- R1.13 [BGKKKN26] analyzes the reflection-symmetric family only, on an exact background. {A01, A45}
- R1.14 Both papers treat equal angular momenta, J₁ = J₂ = J, as cohomogeneity-one problems. {D02, A07, A12}
- R1.15 \|J\|/A is the angular momentum over the throat area A = A(0), in units with 4πG = 1 (recomputed here from the exact solution; neither paper states G). {A14, A16, D06, D07, CALC1}

### Row R2 bullets

- R2.1 At 81% of the extremal angular momentum (model D90) the throat's areal radius shows no growing departure through t = 150, about 28 e-folding times of the static instability, at three resolutions. {S02, S25, S31}
- R2.2 Two other rapidly rotating models, D75 and D80, show no growth over their shorter reliable intervals. {S26, S31}
- R2.3 The authors call this "evidence of prolonged radial stability" under the numerical perturbations present. {S31}
- R2.4 They add that the evolutions "bound growth only over that span" and that a slower mode could still emerge later. {S32}
- R2.5 The runs start from axisymmetric data, so only axisymmetric growth is bounded. {S33}
- R2.6 Only the drainhole family (C = 1) was evolved. {S33, S10}
- R2.7 At lower spin, rotation slows the collapse: the e-fold time of the throat's areal radius rises from 5.4 (static) to 13.3 at 24% of the extremal angular momentum. {S34, S17}
- R2.8 The collapse rate extrapolates to zero at 32% of the extremal angular momentum, against 33% from second-order perturbation theory. {S34}
- R2.9 The 32% is an extrapolation of a fit, not a measured endpoint. {S35}
- R2.10 The models at 28.8% and 33% of the extremal angular momentum expand instead, and the direction of departure depends on the effective perturbation. {S41, S02}
- R2.11 The authors say this establishes growth in those simulations "without identifying a second eigenmode". {S36}
- R2.12 The perturbative mode crossings concern C ≤ 0.2 whereas the evolutions use C = 1, so the evolutions do not test the conjectured merger at the same parameters. {S37}
- R2.13 The e-fold time τ is a fit of the nonlinear areal radius, whereas the perturbative value belongs to a linear mode in Killing time. {S38}
- R2.14 The authors state that a perturbative method cannot decide which continuation rotation takes in four dimensions. {S06}
- R2.15 The angular momentum is quoted as a percentage of its extremal value A/8π, with A the throat area and G = c = 1. {S13, S11}

## Diff

```diff
--- a/notes/critical_ghost.md  (§1.1 table)
+++ b/notes/critical_ghost.md
-| Rotating 5D Ellis wormholes | The unstable mode disappears above a critical angular momentum. A later study reports that the two imaginary frequencies merge at \|J\|/A = 0.100628 and continue as an oscillatory instability, "not stabilization" (arXiv:2610.38659, abstract only read, #50) | [DFKKR13] |
+| Rotating 5D Ellis wormholes, equal angular momenta (J₁ = J₂) | For J > 0 there are two unstable modes: the static wormhole's mode and a second one that descends from its non-normalizable zero mode. The two modes merge at a critical \|J\|/A of 0.10063 for symmetric wormholes in [DFKKR13] and of 0.100628 in [BGKKKN26]. [DFKKR13] also gives 0.1381 for a non-symmetric family (\|a₋∞\| = 1), where the instability persists to faster rotation. [DFKKR13] found no further unstable mode beyond the merger "within the type of modes investigated". [DFKKR13] concluded that rotation "may stabilize wormholes" if "no new unstable modes of a different type appear". The abstract of [DFKKR13] is stronger: the unstable mode of the static wormhole "vanishes when the angular momentum exceeds some critical value". [BGKKKN26] continues the pair past the merger as ω± = ±ω_R + iω_I with ω_I > 0, an oscillatory instability. [BGKKKN26] calls the earlier apparent loss of the instability "not stabilization". [BGKKKN26] says the real-eigenvalue calculation of [DFKKR13] "correctly located the merger" but could not follow the modes past it. Past the merger the dimensionless growth rate ω_I A^{1/3} falls to order 10⁻⁶. The data are consistent with ω_I ∼ (\|J\|/A − 0.5)⁶ toward the extremal Myers–Perry limit at \|J\|/A = 0.5. [BGKKKN26] treats linear perturbations in the cohomogeneity-one gravitational sector and concludes that the symmetric rotating wormholes are linearly unstable there. [BGKKKN26] analyzes the reflection-symmetric family only, on an exact background. Both papers treat equal angular momenta, J₁ = J₂ = J, as cohomogeneity-one problems. \|J\|/A is the angular momentum over the throat area A = A(0), in units with 4πG = 1 (recomputed here from the exact solution; neither paper states G). | [DFKKR13], [BGKKKN26] |
```

```diff
--- a/notes/critical_ghost.md  (§1.2, "Recent", after the [SN26] bullets)
+++ b/notes/critical_ghost.md
     - horizon radius at formation 3.88 and 3.81 against R⋆ = 3.89 M.
+  - [SN26b] (4D, 3+1 numerical relativity, rotating Ellis–Bronnikov drainhole family with C = 1; v2, 6 Nov 2026):
+    - At 81% of the extremal angular momentum (model D90) the throat's areal radius shows no growing departure
+      through t = 150, about 28 e-folding times of the static instability, at three resolutions.
+    - Two other rapidly rotating models, D75 and D80, show no growth over their shorter reliable intervals.
+    - The authors call this "evidence of prolonged radial stability" under the numerical perturbations present.
+    - They add that the evolutions "bound growth only over that span" and that a slower mode could still emerge
+      later.
+    - The runs start from axisymmetric data, so only axisymmetric growth is bounded.
+    - Only the drainhole family (C = 1) was evolved.
+    - At lower spin, rotation slows the collapse: the e-fold time of the throat's areal radius rises from 5.4
+      (static) to 13.3 at 24% of the extremal angular momentum.
+    - The collapse rate extrapolates to zero at 32% of the extremal angular momentum, against 33% from
+      second-order perturbation theory.
+    - The 32% is an extrapolation of a fit, not a measured endpoint.
+    - The models at 28.8% and 33% of the extremal angular momentum expand instead, and the direction of departure
+      depends on the effective perturbation.
+    - The authors say this establishes growth in those simulations "without identifying a second eigenmode".
+    - The perturbative mode crossings concern C ≤ 0.2 whereas the evolutions use C = 1, so the evolutions do not
+      test the conjectured merger at the same parameters.
+    - The e-fold time τ is a fit of the nonlinear areal radius, whereas the perturbative value belongs to a linear
+      mode in Killing time.
+    - The authors state that a perturbative method cannot decide which continuation rotation takes in four
+      dimensions.
+    - The angular momentum is quoted as a percentage of its extremal value A/8π, with A the throat area and G = c
+      = 1.
```

```diff
--- a/notes/critical_ghost.md  (References)
+++ b/notes/critical_ghost.md
 - [DFKKR13] V. Dzhunushaliev, V. Folomeev, B. Kleihaus, J. Kunz, E. Radu, "Rotating wormholes in five dimensions",
   arXiv:1309.2448 (PRD 88, 124028 (2013)).
+- [BGKKKN26] J. L. Blázquez-Salcedo, L. M. González-Romero, F. S. Khoo, B. Kleihaus, J. Kunz, P. Navarro Moreno, "Exact
+  rotating wormholes in five dimensions and their exceptional-point instability", arXiv:2610.38659 (v1, 28 Oct 2026; no
+  journal reference on the arXiv page).
...
   gravitational waves", arXiv:2610.13206 (v2, 24 Oct 2026; no journal reference on the arXiv page).
+- [SN26b] N. M. Shirokov, I. Nachevsky, "Rotation slows the instability of Ellis-Bronnikov wormholes", arXiv:2610.29941 (v2,
+  6 Nov 2026; no journal reference on the arXiv page).
```

```diff
--- a/notes/critical_ghost.md  (§6, "Not read")
+++ b/notes/critical_ghost.md
   - [MGM26] (quoted from choptuik-large-d);
   - the citers of [SH02] other than those opened (title and abstract only).
+  - the slow-rotation and charged-wormhole papers that [BGKKKN26] and [SN26b] cite for the 4D and charged cases (Azad et al.,
+    arXiv:2301.05243 and 2403.08387; Blázquez-Salcedo et al., arXiv:2510.11406 and 2607.18399; ids from [BGKKKN26]'s TeX
+    comments, *(unverified)*): their results appear here only as [BGKKKN26] and [SN26b] state them.
```

The first-claim sentence of the old row ("The unstable mode disappears above a critical angular momentum") is kept as
[DFKKR13]'s own statement (R1.6) with its hedge (R1.4, R1.5). The tail "abstract only read, #50" is dropped: all three papers
were read in full (#152).

## What the papers do not settle

Each item says what is missing. None of these is in the proposed row.

1. **Whether [DFKKR13] searched only real ω².** The words "real-eigenvalue" are [BGKKKN26]'s (A04, A34). [DFKKR13] writes that for unstable modes "−Ω² is positive" (D10) and fixes Ω² by an auxiliary ODE (D11), which is consistent with a real search, but it never says so. The proposal therefore attributes "real-eigenvalue" to [BGKKKN26].
2. **Past the merger for non-symmetric 5D wormholes.** [DFKKR13] gives 0.1381 for |a₋∞| = 1 (D16); [BGKKKN26] analyzes the symmetric family only (A01, A09). No quote says the pair continues as an oscillatory instability there.
3. **Other sectors in 5D.** Both papers restrict to the cohomogeneity-one gravitational sector (A19, A43, D17). Whether other modes appear is open; [DFKKR13]'s own caveat is "if no new unstable modes of a different type appear" (D18). It is also not settled whether [DFKKR13]'s argument that H_φ = 0 for unstable modes (D09, D10, which uses −Ω² > 0) carries over to a complex pair; [BGKKKN26] sets the scalar and angular-velocity perturbations aside by gauge choice (A19).
4. **Time evolution in 5D.** [DFKKR13] names it as future work (D21). Neither 5D paper has one; no other 5D evolution was searched for here.
5. **4D: merger or complex pair.** [SN26b] says a perturbative method cannot decide (S06), and that its evolutions at C = 1 do not test the C ≤ 0.2 crossings (S37). So 4D has no critical J for the modes, only an extrapolated zero of the collapse rate (32%, S34, S35).
6. **4D: what "no growth through t = 150" excludes.** It excludes growth with an e-fold time much shorter than 150 in axisymmetric, drainhole (C = 1), 81% data (S02, S25, S32, S33). It does not exclude a slow mode, a nonaxisymmetric ergoregion instability (S33), or a pair like the 5D one. The 5D paper's growth rate past the merger is of order 10⁻⁶ in units of A^(−1/3) (A37); whether the 4D rate is similar is not in either paper. This comparison is mine, not a quote.
7. **4D: no perturbation at D90.** Perturbations of both signs were added only at D21 (S22). The abstract speaks of "no growing departure" under discretization error alone (S02, S21).
8. **4D: version change.** v1 wrote "From 58% upward we find no evidence of instability over the evolved times" (V01) and that the result "addresses the four-dimensional stability question left open" (V02), and said the expansions were consistent with a second mode "rather than with the instability ending in a mode merger" (V03). v2 does not contain these sentences (checked by `check_quotes.py`). The proposal cites v2 only. [BGKKKN26] cites 2610.29941 without a version (A06).
9. **Units of |J|/A.** Neither 5D paper states G. G = 1/(4π) reproduces every printed value (`jovera_run1.log`); G = 1 does not. This is a recompute, not a quote, and R1.15 says so.
10. **Not carried into the note.** [BGKKKN26]'s statement of priority ("To the best of our knowledge, the present case provides the first explicit identification …") is a novelty claim; AGENTS.md requires reading the closest prior work before repeating one, so it is not repeated. The charged-wormhole paper it compares with was not read.
