# I51: proposed text for notes/novelty/RESULTS.md and notes/novelty/search_log.md

Written 2026-11-24 for the coordinator, who edits the notes. Line numbers are those of RESULTS.md and search_log.md on main
at 639c931. Every quote is in `quotes.md` (found verbatim in the stored source by `make_quotes.py`). No verdict of the table
changes; the wording of the cells below changes. "Sec. IV.1" of DG08 is §IV A in the arXiv v2 and v3 (revtex4: Roman
sections, lettered subsections); the journal's numbering was not seen (CQG answers 403).

## RESULTS.md

```diff
@@ line 3
-Search run 2026-10-22. Raw log: `search_log.md` (same directory).
+Search run 2026-10-22; rerun 2026-11-24 for work posted 2026-10-21 to 2026-11-24 (#51, `negative-mass-raw/I51-rpi5`).
+Raw log: `search_log.md` (same directory).
@@ line 23, row A1: "(implicit)" is not accurate, the identity is stated; what is not stated is its use
-| A1 | Exact zero mode φ₀ = 1/ψ₀ of the intertwined operator Ĥ | **Partially known** (implicit) | Dotti–Gleiser 2008 (0809.3615) §IV.1: the intertwiner maps 1/ψ to a solution of Ĥ; it is the SUSY-QM zero mode "missing in the spectrum" |
+| A1 | Exact zero mode φ₀ = 1/ψ₀ of the intertwined operator Ĥ | **Partially known** | Dotti–Gleiser 2008 (0809.3615) §IV A (v2, v3; §III in v1): for any solution ψ of Hψ = ω₀²ψ, Ĥ(1/ψ) = ω₀²/ψ, and they set ψ̂⁽²⁾ := 1/ψ. Not applied to the Zerilli ψ₀ and its pole, no node discussed |
@@ lines 51-55
-   - Sec. IV.1, SUSY-QM remark: the partner solution "ψ^ωo(j=2) := 1/ψ_ωo(j=1)" satisfies Ĥ(1/ψ) = ω₀²/ψ. At ω₀ = 0 this is our φ₀. They note it is "missing in the spectrum" of Ĥ.
+   - §IV A (v1: §III): "we obtain Ĥ(1/ψ_{ω_o}^{(j=1)}) = ω_o²/ψ_{ω_o}^{(j=1)}. We will set ψ̂_{ω_o}^{(j=2)} := 1/ψ_{ω_o}^{(j=1)}" (TeX, quotes I1, I2). At ω₀ = 0 and ψ = ψ₀, the zero mode of Zerilli's Hamiltonian (ℓ = 2: ψ₀ = r(r³+3Mr²−6M³)/(8M⁴(3M+2r)), with a pole at r_s), this is our φ₀.
+   - v2 and v3 only: "In the supersymmetric quantum mechanics context, ω_o = 0 and ψ^{(j=1)} satisfies appropriate boundary conditions to make it an eigenfunction of H. ... H and Ĥ are isospectral, except for ω_o² = 0, which is missing in the spectrum of Ĥ." That is the case of a normalizable ψ; the Zerilli ψ₀ has a pole at r_s, so the remark is not about our φ₀.
    - They never use it to count modes. The count of exactly one unstable mode is "numerical evidence".
-   - They impose the boundary condition only at r = 0. Their artificial Robin condition at r = 10⁻⁴ is a numerical device.
+   - They impose the boundary condition only at r = 0: §V, "the spatial piece of the modified wave equation has a unique self adjoint extension, that naturally selects the boundary condition that is physically relevant". The numerics (§III) enforce Ψ̂ ≃ x^{3/2} "by imposing Robin type boundary conditions in the form 3Ψ̂ − ∂Ψ̂/∂r = 0 at r = 10⁻⁴", a numerical device.
+   - §V (Summary, identical in v2 and v3; v1's differs) contains no matter source, truncation, node, Sturm count, threshold or l-cap; the words star, fluid, Sturm, node, truncat, cap, threshold have 0 hits in all three versions.
@@ line 77, Paranjape 2025 (abstract and references read, chapter text behind the paywall)
-   - Paranjape 2025, "Puzzles with Negative Mass" (Springer proceedings, ISBN 9783031912665, pp. 167–173): calls dynamical stability of the smoothed star "possible", i.e. open.
+   - Paranjape 2025, "Puzzles with Negative Mass" (CRM Series in Mathematical Physics, Springer, doi 10.1007/978-3-031-91266-5_14, ISBN 9783031912665, pp. 167–173). Abstract: "It was shown [1–3] how to fill in a "negative mass star" so that the singularity is smoothed out, and the energy-momentum satisfies the dominant energy condition and can even gives rise to a dynamically stable configuration." [1–3] are Belletête–Paranjape 2013 (arXiv:1304.1566, no stability analysis of the bubble), Mbarek–Paranjape 2014 and Johnson et al. 2020, so the stability meant is presumably the radial thin-wall one of [3] (chapter text unread). The chapter cites none of Gleiser–Dotti, Dotti 2022, de Aguiar Alves et al. 2025. Its puzzles are repulsion against graviton exchange and the thermodynamics of a negative-mass gas. (The word "possible" in the earlier text of this note is not in the abstract.)
+   - Laguna 2026, "Singustars: Between Black Holes and Compact Stars", arXiv:2611.14482 (2026-11-10): TOV solutions with a negative point mass inside a fluid shell and a positive-mass Schwarzschild exterior. Radial modes and spherical evolutions only: "singustars with Γ = 2 are stable only for M ≲ 0.63 and C ≲ 0.25". "We analyze geodesics and nonradial perturbations of singustars in a forthcoming paper." Not a regular negative-mass star; A4 stands.
@@ line 29, row C2
-| C2 | ... | **Apparently new**, as a derivation and an application | Ivanov explicitly leaves the EIH treatment "for possible future work" |
+| C2 | ... | **Apparently new**, as a derivation and an application | Ivanov leaves the second-order Havas–Goldberg treatment "for a possible future work"; his abstract says the leading-order equations are equivalent to Havas–Goldberg's weak-field ones |
@@ lines 159-160
-   - His derivation comes from conservation of the four-momentum norm plus Fermi–Walker kinematics. He calls the μ²/D³ term "technically … post-Newtonian" and says an EIH / Havas–Goldberg treatment is "left for a possible future work".
+   - His derivation comes from conservation of the four-momentum norm plus Fermi–Walker kinematics. He calls the μ²/D³ term "technically … post-Newtonian" and, citing a handbook ([6], Landau–Lifshitz), says the post-Newtonian corrections "are either proportional to Δμ or ẏ". Abstract (v2): "when only leading terms in the ratio of a characteristic gravitational radius to the distance between the particles are retained our elementary analysis leads to equations of motion equivalent to those derived from relativistic weak-field equations of motion of Havas and Goldberg 1962". Discussion: the Einstein–Infeld–Hoffmann equations are named as a route for V ≪ c, and "a self-consistent relativistic treatment of the problem in the next to the weak field approximation must be based on the second-order formalism of Havas and Goldberg 1962. Such an approach is left for a possible future work."
@@ lines 108-111, 182, 214-220: Shirokov 2608.24577 has a v2
-   - The lone star survives to t = 1000 with a peak decay of 0.63 % per 100 time units. He says this is not asymptotic stability.
+   - v1 (2026-08-25): the lone star survives to t = 1000 with a peak decay of 0.63 % per 100 time units, "not asymptotic stability". v2 (2026-10-26; all simulations rerun, fourth-order time integration, corrected initial data, second author I. Nachevsky): peak amplitude changes by 0.11 % to t = 1000, "A star of negative ADM mass thus shows no sign of instability over the evolved time". Both keep the "first asymptotically flat bod(y/ies) of negative ADM mass evolved in numerical relativity" claim and list sideways stability as untested. Neither version cites Ivanov, Cao, Price or Havas–Goldberg. Numbers: #83.
-Shirokov's "mass ladder" flips at ratio 0.995 against a predicted 1.000. ...
+Shirokov's v1 "mass ladder" flips at ratio 0.995 against a predicted 1.000 (±0.03); the word "ladder" and the 0.995 are not in v2, which lists unequal-mass runs |M₋|/M₊ = 0.60, 0.80, 1.33 in its run table. Recheck in #83 before the footnote is kept.
@@ line 220, row E text: "arXiv shows only v1 (2026-08-25)" is out of date
-- No comments, replies or errata. arXiv shows only v1 (2026-08-25).
+- No comments, replies or errata as of 2026-11-24: INSPIRE still lists one citer (Shirokov & Nachevsky 2610.13206, a self-citation). arXiv shows v1 (2026-08-25) and v2 (2026-10-26).
@@ lines 228-243, Limits of this search
-- **arXiv full-text and listing API** (export.arxiv.org) was blocked by a permission timeout, so systematic arXiv abstract queries could not be run. ...
+- **arXiv listing API** (export.arxiv.org) was blocked by a permission timeout on 2026-10-22. On 2026-11-24 it answers 200 and was used for the rerun (#51); `lastUpdatedDate` is rewritten by the server to `submittedDate`, so revisions are read from `id_list` requests.
-- **Paywalled or not read:**
-  - Price 1993 (AJP 61, 216);
-  - Bonnor & Swaminarayan 1964;
-  - Bičák, Hoenselaers & Schmidt 1983;
-  - Cao 2012 full text (abstract only);
-  - Paranjape 2025 proceedings (abstract only);
-  - the full text of Dotti–Gleiser 2008 §V (ar5iv was truncated, so the conclusion section was not read).
+- **Paywalled or not read** (status 2026-11-24, #51):
+  - Price 1993 (AJP 61, 216, doi 10.1119/1.17293): not read. pubs.aip.org (article and PDF) and doi.org answer 403; OpenAlex and Semantic Scholar list no open copy; no INSPIRE record; no arXiv version; no open copy found by web search. Still taken to be a Newtonian pedagogical note, unverified.
+  - Bonnor & Swaminarayan 1964; Bičák, Hoenselaers & Schmidt 1983: see #17.
+  - Cao 2012 (IJMPD 21, 1250061): abstract (Crossref) and 30-entry reference list (INSPIRE) read; full text not read (worldscientific.com 403; no arXiv version: four arXiv API queries and INSPIRE show none).
+  - Paranjape 2025: abstract and 10 references read; chapter text behind the paywall, the `.pdf` URL returns the landing page; no arXiv version.
+  - Dotti–Gleiser 2008: all five sections read in v1, v2 and v3 from the e-print TeX (§V is the Summary).
@@ line 242
-- Results posted after about 2026-10-21 are not covered.
+- Work posted 2026-10-21 to 2026-11-24 was searched by the rerun of #51 (arXiv API and INSPIRE, 146 runs; web queries of this note, standard mode; `queries.md`): one record bears on a verdict (Laguna 2611.14482, A4); three known papers were revised (Shirokov 2608.24577 v2, Shirokov & Nachevsky 2610.13206 v2 text only, Caridi et al. 2603.13210 v2 accepted by PRD, D unchanged). Later work is not covered.
```

## search_log.md (append)

```diff
@@ end of file
+## Rerun 2026-11-24 (#51, raw `negative-mass-raw/I51-rpi5`; queries.md lists every query with its UTC time and count)
+- Window: arXiv submittedDate and INSPIRE `de` from 2026-10-21 to 2026-11-24. Control window 2026-01-01 to 2026-10-20 through the same code path plants known papers; controls C1 (planted positives), C2 (window edge), C3 (nonsense token = 0), C4 (Shirokov citers list 2610.13206) pass, `--mutate=window` and `--mutate=terms` fail as designed.
+- 39 arXiv queries (A01-A10, B01-B10, C01-C09, D01-D05, E01-E04, Z01) and 11 INSPIRE queries, each in both windows; INSPIRE `refersto:recid:` trails of 22 papers (all dates and new); `id_list` for 45 known arXiv ids (versions, last update).
+- New records in the window, over all queries: 5 distinct. Only 2611.14482 (Singustars) bears on a verdict (A4). The others are false matches (black-hole evaporation spectra, AdS3 entanglement wedges, quantum reference frames, top-quark mass).
+- Citation trails, citers now / new since 2026-10-21: GHI 62/1 (Singustars), GD06 59/0, DG08 21/0, Mbarek-Paranjape 26/0, Shirokov 1/0, Ivanov 3/0, Novikov+ 7/0, Cao 4/0, Paranjape chapter 0/0, Dotti 2022 6/0, de Aguiar Alves+ 4/0, Johnson+ 5/0, Cardoso-Cavaglia 35/0, Giveon+ 20/0, Bernal+ 1/0, Dzhunushaliev+ 0805.3211 56/1 and 1409.6978 44/1 (no bearing), Tamaki-Sakai 37/1 (2611.01826, G > 0 boson stars, no bearing), Bicak-Kofron 7/0, Trivedi-Loeb 3/0, Caridi+ 0/0, Shirokov-Nachevsky 2/1 (2610.29941, same authors).
+- Revised after 2026-10-21: Shirokov 2608.24577 v2 (2026-10-26), Shirokov & Nachevsky 2610.13206 v2 (2026-10-24), Caridi-Corelli-Pani 2603.13210 v2 (2026-11-06).
+- 34 web queries of RESULTS.md A-E (standard mode, `websearch/01-06.tsv`): nothing posted after 2026-10-21 beyond the above. Older items that surfaced and are not in the table: Emergence of Negative Mass in General Relativity (arXiv:2312.03800, phantom field plus monopole, no boson-star stability), Sakaguchi-Malomed soliton pairs (not gravity).
+- Tool facts: INSPIRE `A or B and de > d` binds as `A or (B and de > d)`: parenthesize. `abstracts.value:"x" and arxiv:<id>` ignores the first clause. arXiv `all:"a b"` matches the words loosely; `ti:` is strict.
```
