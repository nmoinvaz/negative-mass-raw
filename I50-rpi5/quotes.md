# I50-rpi5: records for the reading gaps of notes/critical_ghost.md (#50)
Written by `make_quotes.py` from the stored source files (`fetch.log` has URL, status and sha256 of each download). Every quote below was found in its file by the script (matching ignores whitespace, hyphens and ligatures). Papers are data: nothing in them was run, and no text addressed to an AI agent was found in any page or file read.

## 1. Shirokov & Nachevsky 2026, "Binary Ellis–Bronnikov wormholes in 3+1 numerical relativity: mergers, fly-bys and gravitational waves", arXiv:2610.13206

**Status: read.** arXiv listing (abs page), e-print TeX of v1 (9 Oct 2026) and v2 (24 Oct 2026), PDF text of v2 (23 pages). No journal reference
on the arXiv page on 2026-11-24. Read in full: Sec. I, Sec. IV (all of it), Sec. X (discussion, scope), the bibliography entries of [13], [44];
the other sections only by search for the terms in the count table. Not the same paper as arXiv:2608.24577 (#83's subject).

**Contains** (bears on critical behaviour at a wormhole threshold):
- Sec. IV: an isolated *massive* Ellis–Bronnikov "drainhole" (m/a = 1/2), 3+1 AMR (GRTeclyn), exact static data. One exponential mode; its
  e-folding time agrees with the linear analysis to 0.2% (level 3) and 1.9% (level 4); the sign of the perturbation selects collapse or
  inflation (S1, S3, S4).
- Perturbations ε = ±10⁻², ±10⁻³ (and ±0.1): outward collapses, inward inflates; each ±ε pair's radii cross at the ε-independent t× ≃ 13.0;
  horizon times t = 11 (ε = +10⁻²) and t = 25 (+10⁻³) (S5, S6).
- Lifetime law t ≈ τ ln(1/ε) with the cost of a decade 11–12 M ≃ τ ln 10, from the two amplitudes (S8, S9).
- Sec. IV H, "Type-I criticality": the static throat is "consistent with a type-I critical solution"; "Two perturbation amplitudes show both
  type-I signatures but do not establish the scaling"; mass gap: horizons at R = 3.88 and 3.81, near R⋆ (S10, S11). v1 worded the
  first as "consistent with both type-I signatures" (S12).
- Inflation branch: neck grows with HR₀ = 1.22, 6% below the linear mode's 1.30; cites Ha ≈ 1.1 for the massless throat of [SH02] (S7).
- Sec. IV E: says [Shi26a]'s "bounce and horizon shedding are artifacts of the halving" of the phantom stress-energy (S13, S14).

**Does not contain:**
- A bisection to a critical amplitude, a fit of lifetime against ln|p − p*|, or an exponent with an error: "bisect" and "fine-tun" do not occur
  (count table). The lifetime law rests on two amplitudes (+10⁻², +10⁻³); the ±pairs only test the symmetry of the branching.
- A comparison with [SH02]'s 0.60 or with the finite masses 0.30 a [SH02] and 0.22 a [GGS09b]: it gives horizon radii at formation
  (3.88, 3.81 against R⋆ = 3.89 M) for its own throat only.
- Normal-matter pulses (no ε family of normal pulses), other throat compactness, or the massless throat; Sec. X C says the results hold "for one
  phantom-scalar model, equal masses, a single throat compactness and no spin" (S2).
- A statement that the second collapse window of [GGS09b] (ε_c ≈ −0.05) exists or not (ε = −0.1 re-expands then collapses, Sec. IV C, but that
  is one run).

**Flags for the note:**
- S13 against `critical_ghost.md` §1.2's description of [Shi26a]: its collapse run used the phantom stress-energy halved (S_support = 0.5, H4, H5);
  the note does not say so, and [S&N] calls the bounce an artifact of that halving.
- S4: the linear time T = 0.758 at γ₁ = m/a = 0.5 lies between the 0.846 (massless symmetric) and 0.590 (large asymmetry) of [GGS09a] in §1.1 of the
  note; whether T is normalized the same way as [GGS09a]'s τ/r_throat was not checked.

**Quotes** (id, source file, line in that file, section or equation):

- **S1** `abs_2610_13206/abs.html` line n/a, abstract (v2). sha256 `2938dd1643bde234`

  > An isolated throat is unstable: depending on the sign of a small perturbation, it collapses to a black hole or inflates, at the rate that linear perturbation theory predicts to within 1.9%.

- **S2** `abs_2610_13206/abs.html` line n/a, abstract (v2). sha256 `2938dd1643bde234`

  > The results hold for one phantom-scalar model, equal masses, a single throat compactness and no spin.

- **S3** `pdf_sn_v2/paper_flow.txt` line 1224, Sec. IV B. sha256 `55982283fed1a60c`

  > The measured e-folding time agrees with it to 0.2% at level 3 and 1.9% at level 4; larger departures grow more slowly. The initial perturbation is truncation error, and its sign flips with resolution: level 3 collapses and level 4 inflates.

- **S4** `pdf_sn_v2/paper_flow.txt` line 1219, Sec. IV B. sha256 `55982283fed1a60c`

  > for which their linear analysis gives T = 0.758 [18]. We solved the linearised field equations of this solution ourselves, with their regularised master equation and, independently, in the gauge δϕ = 0; both give T = 0.7584, i.e. τlin = 5.13 M .

- **S5** `pdf_sn_v2/paper_flow.txt` line 1358, Sec. IV C. sha256 `55982283fed1a60c`

  > At ε = ±10−2 and ±10−3 an outward perturbation (ε > 0) always collapses and an inward one always inflates. The radii of each ±ε pair cross at the ε-independent t× ≃ 13.0.

- **S6** `pdf_sn_v2/paper_flow.txt` line 1363, Sec. IV C. sha256 `55982283fed1a60c`

  > The amplitude also sets the collapse time: horizons form at t = 11 (ε = +10−2 ) and t = 25 (+10−3 ), against t ≤ 61 for the unperturbed throat

- **S7** `pdf_sn_v2/paper_flow.txt` line 1730, Sec. IV F. sha256 `55982283fed1a60c`

  > Until t ≈ 40 the neck grows exponentially in its own proper time at a rate H, with HR0 = 1.22 (locally 1.0–1.3), where R0 = 3.81 is the perturbed neck’s initial radius. This is 6% below our linear mode’s 1.30, which the local rate reaches. Spherical evolutions find the same proper-time exponential: Ha ≈ 1.1 for the massless throat [13]

- **S8** `pdf_sn_v2/paper_flow.txt` line 1751, Sec. IV G. sha256 `55982283fed1a60c`

  > A static throat survives for about τ ln(1/ε), so its lifetime grows only logarithmically as the perturbation ε shrinks.

- **S9** `pdf_sn_v2/paper_flow.txt` line 1754, Sec. IV G. sha256 `55982283fed1a60c`

  > The delay at equal horizon radius (Sec. IV C) puts the cost of each decade in ε at 11–12 M ≃ τ ln 10.

- **S10** `pdf_sn_v2/paper_flow.txt` line 1770, Sec. IV H. sha256 `55982283fed1a60c`

  > In the language of critical collapse the static throat is consistent with a type-I critical solution [80]: a static solution with a single unstable mode (Sec. IV B) on the threshold between two end states. Here these are collapse and inflation, where the standard problem has collapse and dispersal. Two perturbation amplitudes show both type-I signatures but do not establish the scaling.

- **S11** `pdf_sn_v2/paper_flow.txt` line 1844, Sec. IV H. sha256 `55982283fed1a60c`

  > The ε = +10−2 and +10−3 horizons form at R = 3.88 and 3.81, both close to the throat’s own R⋆ : a tenfold smaller perturbation leaves the black hole’s mass at formation almost unchanged, where type-II scaling would shrink it as a power of ε. Shinkai and Hayward found evidence for critical solutions with a definite black-hole mass in spherical evolutions of the massless throat [13]; here the critical solution is the static throat itself.

- **S12** `src_sn_v1/x/research.tex` line 439, Sec. IV H (v1). sha256 `b061bfdb2c20b2b9`

  > The measurements above are consistent with both type-I signatures, though two amplitudes do not establish the scaling.

- **S13** `pdf_sn_v2/paper_flow.txt` line 1395, Sec. IV E. sha256 `55982283fed1a60c`

  > Ref. [44] evolved the massless throat with the phantom’s stress-energy halved; its bounce and horizon shedding are artifacts of the halving and do not occur here.

- **S14** `src_sn_v2/x/research.tex` line 991, bibliography. sha256 `0ff0739f4c5f8cce`

  > \newblock ``Wormhole dynamics: nonlinear collapse and gravitational-wave emission,''
  > \newblock arXiv:2604.00071 [gr-qc] (2026).

## 2. Clough–Dietrich–Khan 2024, "What no one has seen before: gravitational waveforms from warp drive collapse", arXiv:2406.02466 (Results section)

**Status: read.** arXiv listing (v1 4 Jun 2024, v2 24 Jul 2024; no journal reference listed), e-print TeX of v2, PDF text. DOI
10.33232/001c.121868 resolves (HTTP 200 landing page, `doi_cdk/`); the journal text was not read separately. Read in full: Sec. I, Sec. III
(Results: A gravitational waves, B matter fluxes), Sec. IV (discussion), Sec. II E (setup).

**Contains:**
- A negative-energy stiff-fluid warp bubble released from rest; velocities v = 0.1–0.2 (higher speeds up to 0.5 are said to evolve stably, but "good quality results require very high resolutions") (C5).
- A gravitational-wave burst and a matter flux that alternates in sign; the remnant "is not a black hole" and "appears to settle down into a
  stable remnant" (C1, C2, C3).
- The question whether NEC-violating matter can settle to a mass below zero (C4).

**Does not contain:**
- Any threshold, fine-tuning, bisection, exponent, lifetime or critical solution (count table: "threshold" 0, "bisect" 0, "fine-tun" 0,
  "lifetime" 0; "critical" 1 hit, a reference to critical-collapse gauge practice in Sec. II).
- A two-ended geometry (the word "wormhole" occurs once, in the introduction's list of exotic spacetimes) or a black-hole outcome in any run: the
  parameter scanned (v) gives the same kind of outcome throughout, so there is no boundary between outcomes in this paper.
- A conclusion that bears on the wormhole threshold. The introduction (C6) says in general terms that the fluid and deformations "disperse or
  collapse into a central point"; no run is reported of the second kind. The authors caution the waveforms are model-specific (C7).

So `critical_ghost.md` §3's description (a zero-ADM-mass warp bubble that disperses, stable remnant, no black hole) is confirmed by the results
section; the "not read" caveat there can be dropped.

**Quotes** (id, source file, line in that file, section or equation):

- **C1** `src_cdk_v2/x/main.tex` line 232, Sec. III A (Results, Gravitational waves). sha256 `4b4e749930054606`

  > However, since the remnant is not a black hole, there is no characteristic black hole ringdown in the signal, and there is evidence of a longer lower frequency tail, particularly for higher velocities.

- **C2** `src_cdk_v2/x/main.tex` line 257, Sec. III B (Results, Matter fluxes). sha256 `4b4e749930054606`

  > We see that whilst the gravitational-wave flux is strictly positive as expected, the matter flux alternates in sign, with waves of positive and negative energy leaving the volume.

- **C3** `src_cdk_v2/x/main.tex` line 263, Sec. III B. sha256 `4b4e749930054606`

  > The evolution does appear to settle down into a stable remnant, that could be described as a ``star'' of the warp fluid - it is a configuration of the fluid that appears to balance the gravitational forces and fluid pressures.

- **C4** `src_cdk_v2/x/main.tex` line 259, Sec. III B. sha256 `4b4e749930054606`

  > It would be interesting to study whether this is a generic effect, such that spacetimes with NEC-violating matter cannot dynamically settle into a state with a mass below zero.

- **C5** `src_cdk_v2/x/main.tex` line 223, Sec. II E (Numerical setup). sha256 `4b4e749930054606`

  > The velocity of the warp ship is varied between 0.1 and 0.2.

- **C6** `src_cdk_v2/x/main.tex` line 61, Sec. I. sha256 `4b4e749930054606`

  > it will quickly evolve away from that state and, in most cases, the warp fluid and spacetime deformations will disperse or collapse into a central point.

- **C7** `src_cdk_v2/x/main.tex` line 288, Sec. IV (Discussion). sha256 `4b4e749930054606`

  > We caution that the waveforms obtained are likely to be highly specific to the model employed

## 3. Nakonieczna–Rogatko–Moderski 2012, "Dynamical collapse of charged scalar field in phantom gravity", arXiv:1209.1203 (figures)

**Status: read, figures included.** arXiv listing (one version, 6 Sep 2012), e-print TeX, 18 figure files, PDF text. Figures 9a and 11b were
opened as images. Journal: PRD 86, 044043 (arXiv listing); not read separately.

**Contains:**
- All 18 figures are causal diagrams: Fig. 1 two Penrose diagrams (dynamical Schwarzschild, Reissner–Nordström); Figs. 2–18 "lines of constant r"
  in the (v, u)-plane with the apparent horizons r,v = 0 and r,u = 0 drawn (N1, N9). In Figs. 9a and 11b (read from a plot) there are two r,v = 0 curves and one r,u = 0 curve below the point where the line r = 0 ends.
- The "dynamical wormhole" label is a horizon-structure reading ("two branches of r,v = 0 apparent horizon and an apparent horizon r,u = 0
  inside them", with the calculation ending at positive r, N4, N6); the conclusions describe it as black-hole formation that gains phantom
  dilaton field, which then "provides a formation of the wormhole structure" (N7).
- Outcome sequences along one amplitude (Sec. IV D and the summary table, N3–N5, N8): with the normal charged scalar at φ̃ₛ = 0.6, α = −1, raising the
  phantom-dilaton amplitude φ̃ₖ gives a singular spacetime with a "dynamical wormhole" structure up to 0.15, a naked singularity above 0.2, and
  a non-singular spacetime from about 0.25; with φ̃ₖ = 0.1 raising φ̃ₛ takes non-singular to wormhole (N8: "WH → NS → ns", "ns → WH").
- Pure phantom dilaton: every amplitude non-singular (N2); this is the base of the note's "phantom field always disperses".

**Does not contain:**
- A curve of any quantity (mass, horizon radius, lifetime, throat area) against amplitude, a fit, an exponent or a critical solution: the
  figures show 2–3 amplitudes each (captions), 0.05–0.1 apart, and the transitions are only bracketed by those samples (0.15 / 0.2 / 0.25
  for the wormhole → naked singularity → non-singular sequence). No bisection. "critical" occurs once (the introduction, on another paper's treatment of critical phenomena in classical collapse); "threshold", "fine-tun", "scaling" do not
  occur (count table).
- A statement that a throat persists: the structure is read from apparent horizons on a grid that ends at positive r (N6).

So the note's wording "they report transitions such as singular/non-singular near dilaton amplitude 0.2–0.25, but no critical solution or exponent"
(§2.2) matches the figures and text; the more precise statement is the ordered sequence WH → NS → ns in φ̃ₖ (α = −1, φ̃ₛ = 0.6), bracketed
between 0.15, 0.2 and 0.25. A follow-up (Nakonieczna et al. 2015, arXiv:1508.02657, a citer of [SH02]) was also opened: no threshold analysis either (H7).

**Quotes** (id, source file, line in that file, section or equation):

- **N1** `pdf_nrm_v1/paper_flow.txt` line 833, Sec. IV (Results). sha256 `514b3b622b9076be`

  > The results of the numerical computations are depicted on Penrose diagrams, i.e., we plot lines of constant r (u, v) in the (v, u)-plane.

- **N2** `pdf_nrm_v1/paper_flow.txt` line 891, Sec. IV B (Einstein-phantom dilaton). sha256 `514b3b622b9076be`

  > for every considered dilaton field amplitude the emerging spacetime is non-singular, that is black holes do not form.

- **N3** `pdf_nrm_v1/paper_flow.txt` line 1008, Sec. IV D (Einstein-Maxwell-phantom dilaton). sha256 `514b3b622b9076be`

  > For values of amplitudes not exceeding 0.15 there are two branches of r,v = 0 horizon.

- **N4** `pdf_nrm_v1/paper_flow.txt` line 1016, Sec. IV D. sha256 `514b3b622b9076be`

  > may be interpreted as a dynamical wormhole [24]. On the other hand, for greater values of the parameter p̃k (larger than 0.2) the two branches of the horizon r,v = 0 form a loop with two ends coinciding with ending points of singular part of line r = 0.

- **N5** `pdf_nrm_v1/paper_flow.txt` line 1020, Sec. IV D. sha256 `514b3b622b9076be`

  > For even bigger values of amplitudes of dilaton field, from approximately p̃k = 0.25, the spacetime is non-singular with no visible horizons.

- **N6** `pdf_nrm_v1/paper_flow.txt` line 1013, Sec. IV D. sha256 `514b3b622b9076be`

  > The structure of an area beyond the horizon r,u = 0 is impossible to interpret fully and clearly, because calculations cannot be carried out until r = 0 and they end at some positive value of r.

- **N7** `pdf_nrm_v1/paper_flow.txt` line 1217, Sec. V (Conclusions). sha256 `514b3b622b9076be`

  > In fact one has a formation of the black hole which gains phantom dilaton field which violates null energy condition. This phenomenon provides a formation of the wormhole structure.

- **N8** `src_nrm_v1/x/pphstargatePDF.tex` line 1238, Table III, row EM\bar D, alpha = -1. sha256 `ba035bef9d4912b1`

  > $ns\rightarrow ns^\ast$ & $WH\rightarrow NS\rightarrow ns$ & $ns\rightarrow WH$

- **N9** `src_nrm_v1/x/pphstargatePDF.tex` line 1536, Figs. 2-18 captions. sha256 `ba035bef9d4912b1`

  > Lines of constant $r$ in $(vu)$-plane for $EM\overline{D}$ evolution with a varying dilaton field amplitude.

## 4. Kain 2026, "Dynamical wormholes", arXiv:2602.18231, references 22–29

**Status: read** (arXiv listing: v1 only, 20 Feb 2026; CQG 43, 045014 (2026) per the arXiv page; e-print TeX and PDF text). The bibliography was in the
TeX file; refs. 22–29 are the eight papers cited for "dynamically evolved by a number of groups using various numerical methods" (K1). The
earlier note said they could not be retrieved.

| ref | paper (as printed by Kain, K3–K6) | identifier verified | read | bears on a wormhole threshold |
|---|---|---|---|---|
| 22 | González–Guzmán–Sarbach, "Instability … II. Nonlinear evolution", CQG 26, 015011 (2009) | arXiv:0806.1370; INSPIRE 787653 | in the note | in the note (§1.2) |
| 23 | Doroshkevich–Hansen–Novikov–Shatskiy, "Passage of radiation through wormholes", IJMPD 18, 1665 (2009) | arXiv:0812.0702; INSPIRE 804234 | in the note | in the note (§1.2) |
| 24 | Shinkai–Torii, "Wormhole Dynamics", J. Phys. Conf. Ser. 574, 012056 (2015) | no arXiv id; INSPIRE 1340924; DOI 10.1088/1742-6596/574/1/012056 (open access PDF, 12 pages, `doi_jpcs_pdf/`) | yes, in full by search and the summary | partly: one sentence (K7) |
| 25 | Shinkai–Torii, "Nonlinear Dynamics in the Einstein–Gauss–Bonnet gravity", PRD 96, 044009 (2017) | arXiv:1706.02070; INSPIRE 1603086 | in the note; abstract re-read (INSPIRE) | in the note (§1.2, "critically formed minimum mass") |
| 26 | Novikov–Novikov, "Collapse of a Wormhole and its Transformation into Black Holes", JETP 129, 495 (2019) | no arXiv id; INSPIRE 1771985; DOI 10.1134/S1063776119100248 (Springer, HTTP 200 landing page; `.../pdf` URL returns the same HTML, no full text) | **abstract only** (K8); full text unavailable (paywall) | not from the abstract |
| 27 | Novikov–Novikov–Repin, "Disintegration and expansion of wormholes", PRD 102, 124073 (2020) | arXiv:2012.13788; INSPIRE 1838405 | yes, full text searched | no (K9: expansion dynamics, no threshold or scaling) |
| 28 | Calhoun–Fay–Kain, "Matter traveling through a wormhole", PRD 106, 104054 (2022) | arXiv:2210.04905; INSPIRE 2164089 | yes, full text searched | no scaling; same dichotomy for massless symmetric and massive asymmetric throats (K10) |
| 29 | Xu–Chew–Yeom, "Dynamics of Bronnikov–Ellis wormhole with double-null simulation", JCAP 08, 012 (2025) | arXiv:2503.07610; INSPIRE 2898811 | yes, full text searched | qualitatively: collapse faster with a larger pulse, slower with a larger mass (K11); fine-tuned two-pulse collisions delay but do not cure (K12, K13); no scaling law |

**Contains (Kain 2026 itself, for completeness):** the same expansion/collapse dichotomy for the Ellis–Bronnikov and the quantum corrected Schwarzschild
wormholes (K15); "as the strength of the perturbation is reduced, the system maintains the static configuration longer before eventually evolving
away" for N = 100, 200, 400 points per unit (K14), i.e. the lifetime grows as the perturbation (discretization error) shrinks, with no number;
"qualitatively similar" results for other initial data (K2).

**Does not contain:** a threshold amplitude, bisection, fit or exponent; "critical", "threshold", "fine-tun", "scaling" do not occur as physics
(count table; the two hits of "scaling" are a coordinate-scaling symmetry). None of refs. 22–29 beyond 22, 23, 24, 25 studies critical behaviour.
New relative to the note: refs. 24 (a sentence), 27, 28, 29; ref. 26's full text could not be read.

**Quotes** (id, source file, line in that file, section or equation):

- **K1** `pdf_kain_v1/paper_flow.txt` line 113, Sec. I. sha256 `d1fde15c4a835c2f`

  > The study of dynamically evolved wormholes was initiated by Shinkai and Hayward when they dynamically evolved the Ellis-Bronnikov wormhole [21], which has since been dynamically evolved by a number of groups using various numerical methods [22–29].

- **K2** `src_kain_v1/x/manuscript.tex` line 1150, Sec. IV E (quantum corrected Schwarzschild, dynamical evolution). sha256 `b49e8161307cae9b`

  > We have studied dynamical evolutions with different initial data which also lead to collapse. This includes using different static solutions and different parameters for the pulse. We found the results to be qualitatively similar.

- **K14** `src_kain_v1/x/manuscript.tex` line 663, Sec. III D (Ellis-Bronnikov, dynamical evolution). sha256 `b49e8161307cae9b`

  > We find that as the strength of the perturbation is reduced, the system maintains the static configuration longer before eventually evolving away.

- **K15** `src_kain_v1/x/manuscript.tex` line 1179, Sec. V (Comparison and conclusion). sha256 `b49e8161307cae9b`

  > As far as we are aware, the Ellis-Bronnikov wormhole and the quantum corrected Schwarzschild black hole are the only two charge free wormhole systems that have been dynamically evolved and which exhibit expansion or collapse.

- **K3** `pdf_kain_v1/paper_flow.txt` line 4415, refs. 22-23. sha256 `d1fde15c4a835c2f`

  > [22] J. A. González, F. S. Guzmán, and O. Sarbach, Instability of wormholes supported by a ghost scalar field. II. Nonlinear evolution, Class. Quant. Grav. 26, 015011 (2009), arXiv:0806.1370 [gr-qc]. [23] A. Doroshkevich, J. Hansen, I. Novikov, and A. Shatskiy, Passage of radiation through wormholes, Int. J. Mod. Phys. D 18, 1665 (2009), arXiv:0812.0702 [gr-qc].

- **K4** `pdf_kain_v1/paper_flow.txt` line 4420, refs. 24-25. sha256 `d1fde15c4a835c2f`

  > [24] H.-a. Shinkai and T. Torii, Wormhole Dynamics, J. Phys. Conf. Ser. 574, 012056 (2015). [25] H.-A. Shinkai and T. Torii, Nonlinear Dynamics in the Einstein-Gauss-Bonnet gravity, Phys. Rev. D 96, 044009 (2017), arXiv:1706.02070 [gr-qc].

- **K5** `pdf_kain_v1/paper_flow.txt` line 4423, refs. 26-27. sha256 `d1fde15c4a835c2f`

  > [26] I. D. Novikov and D. I. Novikov, Collapse of a Wormhole and its Transformation into Black Holes, J. Exp. Theor. Phys. 129, 495 (2019). [27] I. D. Novikov, D. I. Novikov, and S. V. Repin, Disintegration and expansion of wormholes, Phys. Rev. D 102, 124073 (2020), arXiv:2012.13788 [gr-qc].

- **K6** `pdf_kain_v1/paper_flow.txt` line 4427, refs. 28-29. sha256 `d1fde15c4a835c2f`

  > [28] K. Calhoun, B. Fay, and B. Kain, Matter traveling through a wormhole, Phys. Rev. D 106, 104054 (2022), arXiv:2210.04905 [gr-qc]. [29] A. Xu, X. Y. Chew, and D.-h. Yeom, Dynamics of Bronnikov-Ellis wormhole with double-null simulation, JCAP 08, 012, arXiv:2503.07610 [gr-qc].

- **K7** `doi_jpcs_pdf/paper_flow.txt` line 961, Sec. 4 (Conclusions and Discussions). sha256 `5dc071270214093e`

  > In [7], for small perturbations, an existence of critical solution is suggested. The similar behaviors are also observed in our investigations, which will be reported elsewhere.

- **K8** `doi_org_10_1134_S1063776119100248/page.html` line n/a, abstract (publisher landing page). sha256 `dbacc511c8a2aaf2`

  > Based on Khalatnikov’s ideas, we consider the physical processes that arise in the collapse of wormholes of different types.

- **K9** `cit_2012_13788/paper_flow.txt` line 14, abstract. sha256 `320ae10586988b79`

  > We consider the process of catastrophic expansion of a spacelike wormhole after a violation of its equilibrium state.

- **K10** `cit_2210_04905/paper_flow.txt` line 8, abstract. sha256 `3b2fdafc0bdb70e4`

  > We confirm that, for the massless symmetric wormhole, a pulse of regular scalar field causes the wormhole throat to collapse and form an apparent horizon, while a pulse of ghost scalar field can cause the wormhole throat to expand.

- **K11** `cit_2503_07610/paper_flow.txt` line 30, abstract. sha256 `fa73aec6a5886c6f`

  > The process of two scenarios can be accelerated by increasing the amplitude of pulses but can be delayed by increasing the wormhole’s mass.

- **K12** `cit_2503_07610/paper_flow.txt` line 1309, body text, pulse collisions (before Fig. 7). sha256 `fa73aec6a5886c6f`

  > Specifically, can fine-tuned collisions stabilize the throat, delaying or preventing horizon formation and maintaining traversability?

- **K13** `cit_2503_07610/paper_flow.txt` line 1525, body text, after Fig. 8. sha256 `fa73aec6a5886c6f`

  > hybrid pulse interactions can reduce but do not cure the instability, offering only limited extensions to the wormhole’s lifetime.

## 5. Papers citing Shinkai–Hayward 2002 [SH02] (INSPIRE citation list, by title and abstract; those bearing on a threshold opened)

**Status: read.** INSPIRE API, `refersto:recid:586606` (SH02's INSPIRE record), fetched 2026-11-24: **222 citing records**, one page, saved in
`inspire_sh02/page1.json` (sha256 in `fetch.log`); table with flags in `citers_out/citers.tsv` (`citers.py`). 169 have an arXiv id, 219 an abstract.
(A first query with `refersto:arxiv:gr-qc/0205041` matched 142134 records and was discarded; `fetch.log` has a note.) All 222 titles were read; full abstracts
of 34 records chosen from the titles, and for the 27 records whose abstract matches critical / threshold / fine-tun / scaling / exponent / Choptuik / type I / universal the text around each match (`citers_abs.py`); 11 papers were opened (marked "opened").

Of the 222, 206 mention a wormhole or throat in title or abstract; the rest are lensing, shadow, thin-shell, modified-gravity or static-construction
papers. Papers that evolve an Ellis-type throat nonlinearly or discuss its fate are listed; none of the others bears on a threshold.

| arXiv / INSPIRE id | paper | read | bears on a wormhole threshold |
|---|---|---|---|
| gr-qc/0306051 | Hayward 2003, "Recent progress in wormhole dynamics" | opened | restates [SH02]: collapse time −0.60 ln E₀, minimal black-hole mass 0.30 a, H = 1.1/a; "suggests critical black-hole and inflationary-universe solutions" (H1, H2); nothing measured |
| 0806.1370, 0812.0702, 1706.02070 | [GGS09b], [DHNS09], [ST17] | note | in the note |
| gr-qc/0212106, gr-qc/0406113, gr-qc/0406080 | Koyama; Hayward–Koyama (exact impulsive radiation) | abstract | no (exact constructions) |
| 0903.5438 | Hayward 2009, "Wormhole dynamics in spherical symmetry" | abstract | no (theory, laws for mouths; reviews conversion with black holes) |
| INSPIRE 1340924 | Shinkai–Torii 2015, JPCS 574, 012056 | opened (ref. 24) | one sentence (K7) |
| INSPIRE 1365436 | Shinkai 2015, "Wormhole in higher-dimensional space-time" (proceedings) | abstract | same content as ref. 24; no new number |
| INSPIRE 1771985 | Novikov–Novikov 2019 | abstract (landing page) | not from the abstract (K8) |
| 2012.13788 | Novikov–Novikov–Repin 2020 | opened | no |
| 2210.04905 | Calhoun–Fay–Kain 2022 | opened | no scaling |
| 2503.07610 | Xu–Chew–Yeom 2025 | opened | qualitative amplitude and mass dependence only |
| 2507.00109 | Kain 2025, quantum corrected Schwarzschild | opened | vacuum expands, "even a small amount of classical matter" collapses (H3): a threshold at zero classical matter, no scaling |
| 2602.18231 | Kain 2026 | opened | item 4 |
| 2604.00071 | Shirokov 2026 [Shi26a] | opened | collapse needs S_support = 0.5, unperturbed run expands (H4, H5) |
| 2610.13206 | Shirokov–Nachevsky 2026 | opened | item 1: the only paper that uses the words "type-I critical solution" for the wormhole threshold |
| 2610.29941 | Shirokov–Nachevsky 2026, "Rotation slows the instability of Ellis–Bronnikov wormholes" | opened | spin, not amplitude, as the parameter: slower collapse, no growth through t = 150 at the fastest spin; at intermediate spins the direction of departure "depending on the effective perturbation" (H6) |
| 1508.02657 | Nakonieczna et al. 2015 (follow-up to [NRM12]) | opened | no threshold analysis; a mass parameter "controlled the formation of a Cauchy horizon or wormhole throats" (H7) |
| 1001.1202 | Sarbach 2010 (exotic dust + magnetic field) | abstract | no: shell-crossing instability of a different model |
| 0907.1936 | Novikova et al. 2009 | abstract | no (singularity near collapse of a wormhole) |
| 2104.11134 | Yang 2021, trapping horizons of an evolving charged wormhole / black bounce | abstract | no (analytic conversion events) |
| 2611.00541 | Guvendi 2026, scalarization thresholds on a fixed Ellis wormhole | abstract | no: "threshold" is a coupling for linear growth of a probe field; "numerical evolutions are consistent with saturation" (H9) |
| 2610.38659 | Blázquez-Salcedo et al. 2026, rotating 5D Ellis–Bronnikov | abstract | qualifies the note's §1.1 row on [DFKKR13]: the loss of the radial instability "is therefore not stabilization, but a transition to an oscillatory instability" (H8) |
| 2510.11406, 2607.18399, 1309.2448, 1710.01884, 1606.04356 | linear stability and rotating studies | abstract | no |

**Contains:** no citer other than [SH02]-family papers measures a lifetime or mass against perturbation size at a wormhole threshold. The statements that bear:
[SH02] itself (in the note), its restatements (H1, H2, K7), [GGS09b]/[ST17] (in the note), [S&N]'s two-amplitude type-I reading (S10, S11), and the qualitative
amplitude/mass dependence in Xu et al. (K11).

**Does not contain:** a bisection, a fitted exponent, a comparison of the lifetime exponent with 1/λ₀ in print, or a resolution of 0.30 a against 0.22 a.
Not opened: the other citers listed only by title and abstract above; the full text of Novikov–Novikov 2019 and of the INSPIRE records with no arXiv id and
no open-access page.

**Quotes** (id, source file, line in that file, section or equation):

- **H1** `cit_gr-qc_0306051/paper_flow.txt` line 350, body text, summary of SH02. sha256 `d0fefcb10649cf92`

  > Unexpected critical behaviour was also discovered: the initial energy determines the collapse time x − x0 = −0.60 ln E0 and there appears to be a minimal black-hole mass M = 0.30a or Hubble constant H = 1.1/a as perturbations tend to zero, for both exotic and normal field perturbations. All this is unexplained.

- **H2** `cit_gr-qc_0306051/paper_flow.txt` line 377, conclusions (bullet list). sha256 `d0fefcb10649cf92`

  > Numerically discovered critical behaviour suggests critical black-hole and inflationary-universe solutions.

- **H3** `cit_2507_00109/paper_flow.txt` line 11, abstract. sha256 `2a621855d6399ca6`

  > In vacuum, the wormhole expands, but in the presence of even a small amount of classical matter, the wormhole collapses, forming a horizon and evolving to an evaporating black hole.

- **H4** `cit_2604_00071/paper_flow.txt` line 12, abstract. sha256 `d9e86ecccffd0a5d`

  > To force a clean collapse while breaking spherical symmetry, we reduce the phantom stress-energy support to Ssupport = 0.5 and add a quadrupolar scalar-field perturbation

- **H5** `cit_2604_00071/paper_flow.txt` line 309, Sec. II (initial data and perturbation). sha256 `d9e86ecccffd0a5d`

  > This halves the repulsive support, forcing the wormhole into the compressive branch.

- **H6** `cit_2610_29941/paper_flow.txt` line 17, abstract. sha256 `50df6da12829a11f`

  > At intermediate spins some throats expand, with the direction of departure depending on the effective perturbation.

- **H7** `cit_1508_02657/paper_flow.txt` line 33, abstract. sha256 `e346b8f6ecfaffa5`

  > The square of mass parameter of the dark matter scalar field potential controlled the formation of a Cauchy horizon or wormhole throats in the spacetime.

- **H8** `inspire_sh02/page1.json` line n/a, INSPIRE abstract of 2610.38659. sha256 `3c83f9cbf2badd87`

  > the apparent loss of the radial instability found in the original real-eigenvalue treatment is therefore not stabilization, but a transition to an oscillatory instability.

- **H9** `inspire_sh02/page1.json` line n/a, INSPIRE abstract of 2611.00541. sha256 `3c83f9cbf2badd87`

  > Numerical evolutions are consistent with saturation on the nodeless branch.

## 6. The Frolov map (§2.4(e)): Roberts' (C₁, C₂) to the parameter p of [Fro97]

**Result: the map exists and is p = −C₁C₂ for C₂ > 0.** Coordinates: U = √C₂ u, V = v/√C₂ (so that du dv and uv are unchanged, C₂u² → U² and C₁v² → C₁C₂V²).
Scalar: Φ_F = 2√π φ_M + const with the lower sign of [Mae09]'s "±" (the check finds exactly one sign that works). Equivalently, [Fro97]'s family is [Mae09]'s family with C₂ = 1 and C₁ = −p.
Checked with `frolov_map.py` (sympy and mpmath): 23 checks PASS, 4.1 s, peak rss 62 MB; ten mutations (seven wrong maps or signs, three typos in the script's own inputs) each exit 1 (README has the table of what fired).

What the sources print (verbatim in the quotes below): [Fro97] F1–F11; [Mae09] M1–M9; Brady 1994 B1–B6 (new: read from gr-qc/9402023, one version).
- The same metric: `−2 du dv` with R² = u² − uv − p v² ([Fro97], Σ = 0) and R² = −uv + C₁v² + C₂u² ([Mae09]); Brady's eq. (8) is r² = αv² + βu² − uv, i.e.
  (α, β) = (C₁, C₂) read off textually, and his β = 1 is [Fro97]'s normalization, so Brady's α = C₁ = −p ([Fro97] says his own sign of p is opposite to Brady's, F5).
- Sectors under the map: p > 0 ⟺ C₁ < 0 ⟺ black hole; p = 0 ⟺ C₁ = 0 the critical member (Brady's α_crit = 0, B3; [Fro97]'s F6); −1/4 < p < 0 ⟺ 0 < C₁ < 1/(4C₂)
  dispersal; p = −1/4 ⟺ 4C₁C₂ = 1 flat space (B4, M5); p < −1/4 ⟺ 4C₁C₂ > 1 the ghost members (M6). These are the placements already in `critical_ghost.md` §2.4(e) and
  `bh_to_wormhole.md` §2; the check M4 and Brady's B3 confirm them from two further sources.
- The marginally trapped line: [Fro97]'s R,V = 0 (F10) maps to u = 2C₁v, the θ_v = 0 line of `bh_to_wormhole.md` §2 (check M5); the Misner–Sharp masses agree (F9, M3; check M6).
- The scalar: Φ_F real for p > −1/4 (checks N1, N2), purely imaginary for p < −1/4 (N3), as [Mae09] states for 4C₁C₂ > 1 (M6). [Fro97] writes Φ with √(1+4p), real for p ≥ −1/4, and says only "for p<0 the field disperses" (F5); the ghost range is the same metric formula with an imaginary Φ, which
  [Fro97] does not discuss ("ghost", "phantom", "wormhole" do not occur in it).
- The k = 0 mode of [Fro97] is the family direction (F12), so the critical solution he perturbs is p = 0, the C₁ = 0 member; his spectrum 1/2 < Re k < 1 and
  β = 1 against the in-family 1/2 of Brady (B6) and others (F13, F14) are statements about that member: `critical_ghost.md` §2.4(e)'s last bullet is consistent with the text.

**Limits (stated, not hidden):**
- C₂ > 0 is needed for the real rescaling (the note's convention, `bh_to_wormhole.md` §2). C₂ < 0 gives a negative u² coefficient, which [Fro97]'s form (u² − uv − pv²) cannot take; the family's
  u ↔ v symmetry (C₁ ↔ C₂) covers C₁ > 0 with C₂ ≤ 0, and the region with both negative is a different part of the Roberts spacetime, not checked.
- [Fro97]'s region is u < 0 < v (F11); the numeric sign tests (N1–N5) use a point in it. [Mae09]'s wormhole-forming construction uses C₁, C₂ > 0 with 4C₁C₂ > 1 (M8), where R² is positive for all (u, v);
  the map there is an identity of metric and field (M1–M3 are identities in u, v and t), but [Fro97]'s perturbation analysis concerns only the p = 0 member.
- Roberts 1989 (GRG 21, 907) was not read. Brady 1994 was read in its arXiv version (gr-qc/9402023, CQG 11, 1255); the journal text was not.
- The formulas in `frolov_map.py` were typed by hand from the quoted TeX; `make_quotes.py` checks only that the quotes are in the files, not that the typing matches them. Brady's formulas are not in the script (textual comparison only).

**Quotes** (id, source file, line in that file, section or equation):

- **F1** `src_fro_v1/x/paper.tex` line 122, [Fro97] eq. (metric). sha256 `8bae2d4a768cc22d`

  > dS^2 = - 2e^{2\Sigma}\, du dv + R^2\, d\Omega^2,

- **F2** `src_fro_v1/x/paper.tex` line 174, [Fro97] eq. (ss_soln). sha256 `8bae2d4a768cc22d`

  > R &=& \sqrt{u^2 - uv - pv^2},

- **F3** `src_fro_v1/x/paper.tex` line 175, [Fro97] eq. (ss_soln). sha256 `8bae2d4a768cc22d`

  > \Phi &=& \frac{1}{2} \ln
  >     \left[-\frac{2pv + u(1 - \sqrt{1+4p})}{2pv + u(1 + \sqrt{1+4p})}\right] +
  >     \varphi(p).

- **F4** `src_fro_v1/x/paper.tex` line 184, [Fro97] eq. (const_phi). sha256 `8bae2d4a768cc22d`

  > - \frac{1}{2} \ln \left[\frac{\sqrt{1+4p}-1}{\sqrt{1+4p}+1}\right] =

- **F5** `src_fro_v1/x/paper.tex` line 187, [Fro97] Sec. II. sha256 `8bae2d4a768cc22d`

  > For values $p>0$ of control parameter, a black hole is formed; for
  > $p<0$ the field disperses, and the spacetime is flat again in region
  > $u>0$. (Our choice of sign of $p$ is opposite to the one in
  > \cite{Brady:94}.

- **F6** `src_fro_v1/x/paper.tex` line 168, [Fro97] eq. (crit). sha256 `8bae2d4a768cc22d`

  > R_0 &=& \sqrt{u^2 - uv},

- **F7** `src_fro_v1/x/paper.tex` line 132, [Fro97] eq. (es:3)-(es:7). sha256 `8bae2d4a768cc22d`

  > (R^2)_{,uv} + e^{2\Sigma} = 0,

- **F8** `src_fro_v1/x/paper.tex` line 139, [Fro97] eq. (es:5), (es:6). sha256 `8bae2d4a768cc22d`

  > R_{,vv} - 2\Sigma_{,v}R_{,v} + R (\Phi_{,v})^2 = 0,

- **F9** `src_fro_v1/x/paper.tex` line 201, [Fro97] eq. (mass). sha256 `8bae2d4a768cc22d`

  > 1 - \frac{2M}{R} = 2 g^{uv} R_{,u}R_{,v}.

- **F10** `src_fro_v1/x/paper.tex` line 196, [Fro97] eq. (ah). sha256 `8bae2d4a768cc22d`

  > A(u,v) = u^{;\mu}_{\ \ ;\mu} = R_{,v}.

- **F11** `src_fro_v1/x/paper.tex` line 228, [Fro97] Sec. III. sha256 `8bae2d4a768cc22d`

  > The signs are chosen to make the arguments of the logarithm positive in
  > the region of interest ($v>0$, $u<0$), where the field evolution occurs.

- **F12** `src_fro_v1/x/paper.tex` line 364, [Fro97] Sec. IV. sha256 `8bae2d4a768cc22d`

  > Clearly, the self-similar mode has eigenvalue $k=0$

- **F13** `src_fro_v1/x/paper.tex` line 576, [Fro97] Sec. V. sha256 `8bae2d4a768cc22d`

  > The eigenvalues $k$ approach $\sup \Re k = 1$, which corresponds to the
  > mass-scaling exponent $\beta=1$. This is different from the exponent
  > $\beta=1/2$ found in

- **F14** `src_fro_v1/x/paper.tex` line 567, [Fro97] Sec. V. sha256 `8bae2d4a768cc22d`

  > \frac{1}{2} < \Re k < 1,

- **B1** `src_brady/x/9402023.tex` line 155, [Bra94] eq. (8). sha256 `c222d2e6324cff6f`

  > r^2 &=& \alpha v^2 + \beta u^2 - uv \; , \label{eqn:8}

- **B2** `src_brady/x/9402023.tex` line 186, [Bra94] Sec. 2. sha256 `c222d2e6324cff6f`

  > In order to discuss the problem of collapse we can set $\beta = 1$ without loss
  > of generality.

- **B3** `src_brady/x/9402023.tex` line 193, [Bra94] Sec. 2. sha256 `c222d2e6324cff6f`

  > these are subcritical ($0<\alpha < 1/4$), critical ($\alpha = 0$) and
  > supercritical ($\alpha <0$).

- **B4** `src_brady/x/9402023.tex` line 197, [Bra94] Sec. 2. sha256 `c222d2e6324cff6f`

  > Moreover notice when $\alpha = 1/4$ the solution is simply flat
  > space.

- **B5** `src_brady/x/9402023.tex` line 177, [Bra94] eq. (mass1). sha256 `c222d2e6324cff6f`

  > m(u,v) =  -uv(1-4\alpha\beta)/4r

- **B6** `src_brady/x/9402023.tex` line 51, [Bra94] abstract. sha256 `c222d2e6324cff6f`

  > for near critical evolution
  > $M \simeq |\alpha-\alpha_{\rm crit}|^{1/2}$.

- **M1** `src_mae_v2/x/Wormholeformation.tex` line 184, [Mae09] eq. (roberts1). sha256 `54773cec4be574af`

  > ds^2=-2dudv+(-uv+C_1v^2+C_2u^2)d\Omega^2, \label{roberts1}

- **M2** `src_mae_v2/x/Wormholeformation.tex` line 190, [Mae09] eq. (roberts2). sha256 `54773cec4be574af`

  > \phi=\phi_0\pm \frac{1}{2\sqrt{\pi}}{\rm arctanh}\biggl(\frac{1-2C_1(v/u)}{\sqrt{1-4C_1C_2}}\biggl) \label{roberts2}

- **M3** `src_mae_v2/x/Wormholeformation.tex` line 199, [Mae09] eq. (roberts-mass). sha256 `54773cec4be574af`

  > m_{\rm MS}=-\frac{(1-4C_1C_2)uv}{4\sqrt{-uv+C_1v^2+C_2u^2}}. \label{roberts-mass}

- **M4** `src_mae_v2/x/Wormholeformation.tex` line 157, [Mae09] eq. (beq). sha256 `54773cec4be574af`

  > {\ma R}^{\mu}_{~~\nu}=8\pi \epsilon \phi^{,\mu}\phi_{,\nu}, \label{beq}

- **M5** `src_mae_v2/x/Wormholeformation.tex` line 187, [Mae09] Sec. II. sha256 `54773cec4be574af`

  > For $C_1C_2=1/4$, it is the Minkowski spacetime.

- **M6** `src_mae_v2/x/Wormholeformation.tex` line 224, [Mae09] Sec. II. sha256 `54773cec4be574af`

  > Therefore, the scalar field is purely imaginary corresponding to a ghost scalar field for $C_1C_2>1/4$.

- **M7** `src_mae_v2/x/Wormholeformation.tex` line 232, [Mae09] Sec. II. sha256 `54773cec4be574af`

  > On the other hand, the solution with $C_1=0$ was obtained by Brady in 1994

- **M8** `src_mae_v2/x/Wormholeformation.tex` line 319, [Mae09] Sec. III. sha256 `54773cec4be574af`

  > two Roberts spacetimes with the same nonzero $C_2$ but different $C_1$ can be attached in a regular manner at $v=0$.

- **M9** `src_mae_v2/x/Wormholeformation.tex` line 231, [Mae09] Sec. II. sha256 `54773cec4be574af`

  > we can set $|C_1|=1$ without loss of generality by the coordinate transformations ${\bar v}:=\sqrt{|C_1|}v$ and ${\bar u}:=u/\sqrt{|C_1|}$

## Term counts used in the "does not contain" lists

Case-insensitive counts in the whole text of the source (hyphen optional where written with one); `black hole` and `wormhole` counts include the bibliography.

| source | critical | threshold | fine-tun | bisect | scaling | exponent | lifetime | unstable mode | throat | wormhole | Choptuik | black hole |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Shirokov & Nachevsky v2 (PDF text) | 10 | 3 | 0 | 0 | 5 | 16 | 8 | 4 | 230 | 58 | 1 | 41 |
| Clough et al. v2 (TeX) | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 4 |
| Nakonieczna et al. v1 (PDF text) | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 11 | 0 | 45 |
| Kain 2026 v1 (PDF text) | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 35 | 268 | 0 | 66 |
