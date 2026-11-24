# I146-rpi5: Regge–Wheeler gauge is attainable (e^{st} and static), and #143's flow at r_s against DG06's Lemma 1

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10, one thread.
Issue: https://github.com/nmoinvaz/negative-mass/issues/146
Worktree: `~/Source/negative-mass-i146`, branch `wip/i146-gauge-rs` (base main debadbe).
Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0, mpmath 1.3.0). Exact rational-function algebra only; no floats.

Written 2026-11-23, before `zerilli_gauge_rs.py` was run. Check ids and control targets below are fixed before its first run. Anything
changed or added after seeing data is listed at the end under "Edited before the first run" and "Added after the first run".

## Exploratory algebra done before this README (not a result)

Three small throwaway scripts in the session scratchpad (not in the repository, not in this folder; they typed #143's and #145's printed flows as
inputs) were run to see what the r_s part looks like, before the checks below were written. What they showed, so that the checks are not pretended to be blind:

1. Through ψ_Z = ζ/(2λr − 3μ), DG06's (nv1) K equals (3)'s K; (nv1)'s H1 is (2/r) times (3)'s H1 (and is not dimensionless); (nv1)'s H2 has the opposite sign on its
   ζ term. (im) is (9) times (2λr − 3μ).
2. On #143's flow, ζ = (im)(K, K′, H) is 2r²K − 2(r−2M)H1/s (no H), ζ′ has no H either, and the 2×2 matrix T with (ζ, ζ′) = T (K, H1) has det 4r(λr+3M)/s;
   T(r_s) has rank 1 and its range lies on ζ′ = c* ζ with c* = λ²/(3M(2λ+3)) = −2λ²/(3μ(2λ+3)) = M/(r_s(r_s−2M)). DG06's (cz) as typed is ζ′ = +2λ²/(3μ(2λ+3)) ζ.
3. DG06's own (RW17) forces the same c* at r_s (the ODE's singular-point relation), and the corrected (nv1)'s numerators vanish at r_s iff ζ′ = c* ζ. The residue matrix
   of the (K, H1) flow at r_s has eigenvalues 0 and 1. The static flow (#145) gives the same c*.
4. The same relation at M = −1 is #138's L1.2: χ′/χ(r_s) = −1/(r_s(r_s+2)).

The checks R.1–R.11, R.S.1–R.S.2 were written after this, to confirm or refute 1–4 in the script itself (the flow is **re-derived** from the Einstein equations in the run, not typed).
The gauge part (G*, PL.E, PL.P) was written from a hand derivation of L_ξ g (below) and was not run.

## What was read, and what is shared with #143 and #145

Read before writing: AGENTS.md; #146's text; #143's and #145's notes `zerilli_derivation.md` and `zerilli_static.md` (all, including both coordinator reviews) and their
auto-memory handovers; #143's `zerilli_derivation_lib.py` (all) and the structure of `zerilli_derivation.py` and `zerilli_static.py`; `review_lemma_a.md` §5 (#138 L1) and
`review_lemma_a3.md` §6 (#142 L6.5, LL11, LL12); DG06's TeX (below). Issue search: `gh search issues` for "Regge-Wheeler gauge", "regularity r_s", "gauge attainable":
#143, #145 (assume the gauge, do not treat r_s), #108 (open, not on the subject), #3, #142. Nothing else bears on the task. #148 (open, not mine) is the general-l certificate: not done here.

**Shared code.** `zerilli_derivation_lib.py` of #143 is **imported unchanged** (harness, dual-number Ricci, covariant route, Legendre reduction, `ang_split`, `jetify`, `flow_sub`).
The driver `zerilli_gauge_rs.py` is new; the even-parity radial equations and the flow of §R are derived again in it with that library (same code path as #143's E.2), not typed.

| tag | source | read | used for |
|---|---|---|---|
| DG06 | Dotti, Gleiser, CQG 23 (2006) 5063, arXiv:gr-qc/0604021, TeX `dg06_src/nakedsingularity2.tex` (gunzip of the e-print, sha256 4da32b56…) | the section "A modified Regge-Wheeler-Zerilli formalism" (lines 255–360) and eqs. (RW2), (RW2a), (poten1), (RW3a) (lines 150–215) | (3)–(4) = RW2, RW2a; V = poten1; (9) = RW3a; (AppB1) line 267; (RW17) lines 270–284; (nv1) 287–300; (im) 303–310; Lemma 1 and (cz) 313–319; (AppB2) 337–350 |
| #143 | `zerilli_derivation_output.txt` lines E.2 | the printed flow (K′, H1′, H′), A | typed **comparison targets** of R.1 only |
| #145 | `zerilli_static.md` §1 | the static flow in (K, H) | typed comparison target of R.S.1 only |
| #138 | `review_lemma_a.md` §5, L1.2, L1.3 | χ′/χ(r_s) = −1/(r_s(r_s+2)), χ″(r_s) = 0 at M = −1, s = 0 | cross-reference only (R.11 reproduces its numbers; nothing depends on it) |
| RW57, Z70, MP05 | Regge–Wheeler (1957), Zerilli (1970), Martel–Poisson (2005) | **not read** | nothing; the gauge-invariant combinations the solve prints are standard, and I name no source for them *(unverified)* |

The published version of DG06 was not read: discrepancies below are discrepancies of this arXiv TeX file against the derivation, not of the journal text *(unverified)*.

## Definitions

Coordinates (t, r, x = cos θ, φ); unit sphere γ = dx²/(1−x²) + (1−x²)dφ²; L = l(l+1) is one symbol; λ = (L−2)/2; f = 1 − 2M/r; μ = −2M; r_s = −3M/λ = 3μ/(2λ);
P(x) = P_l(x) abstract with Legendre's equation; E = e^{st}, or E = 1 for the static case. M symbolic throughout, then M = −1.

**The seven functions of a general even (l, m = 0) perturbation** (conventions as DG06 (2), their signs; names are mine):

| name | component | definition |
|---|---|---|
| H0 | h_tt | f H0 P E |
| H1 | h_tr | H1 P E |
| H2 | h_rr | H2 P E / f |
| Jt | h_tx (= h_tθ up to dx = −sinθ dθ) | Jt P′(x) E |
| Jr | h_rx (= h_rθ) | Jr P′(x) E |
| K | trace part of h_ab | h_ab = r² E [K P γ_ab + G T_ab] |
| G | traceless angular part | T_ab = D_aD_bP + (L/2) P γ_ab, so (1−x²)T_xx = xP′ − (L/2)P and T_φφ/(1−x²) = −(xP′ − (L/2)P) |

Regge–Wheeler gauge: Jt = Jr = G = 0. (With my K the Regge–Wheeler paper's K_RW is K + (L/2)G; they agree in RW gauge.) The structure T(x) = xP′ − (L/2)P vanishes identically iff L ∈ {0, 2}.
**Gauge vector:** ξ^t = a P E, ξ^r = b P E, ξ_x = c P′ E (lower index; ξ^x = c(1−x²)P′E/r², as `xi_even` of #143, #145), ξ^φ = 0, with a, b, c functions of r.
h → h′ = h + L_ξ g (sign as the issue).

Hand derivation of the effect of ξ on the seven functions (to be reproduced by the code through `extract`, not typed into the solve):
ΔJt = −f a + s c, ΔJr = b/f + c′ − 2c/r, ΔG = 2c/r², ΔK = 2b/r − L c/r², ΔH0 = −(f′/f) b − 2 s a, ΔH1 = −f a′ + s b/f, ΔH2 = −(f′/f) b + 2 b′.
Solve (predicted): c = −r² G/2, b = −f (Jr − r² G′/2), a = (Jt − s r² G/2)/f. Divisors predicted: constants, r (from c = −r²G/2 and the ΔG row 2/r²), f = (r−2M)/r. **Not s, not L−2, not M.**
L−2 enters through the independence of the two angular structures: at L = 2 the traceless part of every h_ab is identically 0, G is not a function of h, and the three conditions reduce to two.

## Checks (id : statement). A failed planted check (PL.*) ends the script with exit 2 before any real data; a failed real check exits 1.

Part `planted` (exit 2):

| id | statement |
|---|---|
| PL.0a–d | #143's: dual inverse; Ricci of static de Sitter = (3/a²)g; vacuum Schwarzschild with M symbolic; Legendre reduction against P_l, l = 2..6 |
| PL.L | **the Lie derivative, two routes.** (L_ξ g)_{μν} from the partial-derivative form ξ^a∂_a g_{μν} + g_{aν}∂_μξ^a + g_{μa}∂_νξ^a equals ∇_μξ_ν + ∇_νξ_μ (ξ_ν = g_{νa}ξ^a, background Christoffels), all 10 components, for ξ = (aPE, bPE, c(1−x²)P′E/r², 0) with a, b, c arbitrary functions |
| PL.G | h = L_ξ g (partial form, even ξ with e^{st}) gives δR_μν = 0, all 10 components (#143's PL.G.even) |
| PL.X | the covariant route equals the dual-number route in every component of δR for the even RW ansatz with e^{st} (#143's PL.X.even) |
| PL.E | **extraction round trip.** Build h from the seven arbitrary functions, extract the seven functions from it (`extract`: Legendre reduction, coefficients of P, xP′, P′ read separately; the angular identities βxx + βφφ = 0 and αφφ − αxx = L βxx checked inside), get the same seven back, symbolic in L; with E = e^{st} and with E = 1 |
| PL.P | **planted pure gauge.** η = (ea P E, eb P E, ec(1−x²)P′E/r², 0) with ea, eb, ec arbitrary functions of r. (i) h = ∇η + ∇η (covariant route) goes through `extract` and the solver; the result is ξ = −η and all seven functions of h + L_ξ g are 0 (in particular the four RW functions). (ii) h = (H0, H1, H2, K arbitrary, Jt = Jr = G = 0) + L_η g: the solver returns ξ = −η and the transformed h equals the RW-gauge part exactly. With E = e^{st} and with E = 1 |

Part `gauge` (e^{st}, exit 1):

| id | statement |
|---|---|
| GA.1 | the structure function T_l = xP_l′ − (L/2)P_l: P and xP′ independent iff L ∉ {0, 2} (symbolic, as #143's A.1); T_l is a nonzero polynomial with leading coefficient −k_l l(l−1)/2 ≠ 0 for l = 2..30; T_1 ≡ T_0 ≡ 0 |
| GS.1 | for h with seven arbitrary functions the equations ΔJt = −Jt, ΔJr = −Jr, ΔG = −G, **read off from `extract(L_ξ g)`**, are solved for (a, b, c) exactly (symbolic L, M, s); substituting gives Jt′ = Jr′ = G′ = 0 identically; a, b, c and the four RW functions H0′, H1′, H2′, K′ are printed |
| GS.2 | the printed solution equals the closed forms of "Definitions" (typed there as comparison targets) exactly |
| GS.3 | **divisors.** Every denominator of (a, b, c) and of H0′, H1′, H2′, K′ (as rational functions of r, M, s, L times jets of the seven functions) lies in the vocabulary {s, r, r−2M, L, L−2, M}; the factors met are exactly {r, r−2M}; s, L−2 and M are not among them |
| GU.1 | **uniqueness.** For l = 2..8 (explicit Legendre polynomials P_l) the homogeneous problem (h = 0; require Jt′ = Jr′ = 0 and the traceless angular part of h′ ≡ 0 as a function of x) has only ξ = 0 |
| GU.2 | **the L = 2 failure.** At l = 1 (P = x): the traceless angular part of L_ξ g vanishes identically for every c; the family a = s c/f, b = −f(c′ − 2c/r), c arbitrary, gives Jt′ = Jr′ = 0 and no G condition. So the Regge–Wheeler conditions fix ξ for l ≥ 2 only |

Part `static` (no time dependence; exit 1):

| id | statement |
|---|---|
| GST.1 | with E = 1 (separate code path from the s → 0 value of the e^{st} equations): (a, b, c) = (Jt/f, −f(Jr − r²G′/2), −r²G/2), equal to GS.1's at s = 0 exactly; the solve is algebraic (no ODE in r, no integration constant), divisors {r, r−2M} |
| GST.2 | uniqueness for static ξ: for l = 2..8 the homogeneous static problem has only ξ = 0 |
| GST.3 | **residual freedom beyond static ξ.** ξ = t κ with κ = (αP, βP, γP′…): L_ξ g is t-independent iff L_κ g = 0, which for l ≥ 2 and M symbolic forces α = β = γ = 0 (no Killing vector with l ≥ 2). So no residual gauge freedom among time-independent perturbations either |

Part `rs` (exit 1). The flow is derived in the run: δR_tr, δR_tx, δR_rx of the e^{st} even RW ansatz give (K′, H1′, H′) (H0 = H2 = H from the traceless equation); δG_rr gives A = aK K + a1 H1 + aH H; the static flow is the s = 0 value (#145's S.0).

| id | statement |
|---|---|
| R.1 | the derived flow, det and A equal #143's printed ones (typed targets: K′, H1′, H′ rows, aK, a1, aH) exactly |
| R.2 | **r_s is a regular point of the flow.** Denominators of every entry of F and of a lie in {s, r, r−2M} (constants aside); at r_s = −3M/λ: s ≠ 0, r_s ≠ 0, r_s − 2M = −M(2λ+3)/λ ≠ 0; aH(r_s) = 0 |
| R.3 | **finite jets.** The Taylor coefficients u^{(k)}(r_s), k = 0..4, of any solution of the 3-dimensional flow are linear in (K, H1, H)(r_s) with finite coefficients (no pole at r_s). With the Cauchy theorem for analytic coefficients: every solution of the flow is analytic at r_s |
| R.4 | **the map to ζ.** ζ := (im)(K, K′, H2 = H) with K′ from the flow: its coefficient of H is 0, and ζ′ along the flow has coefficient 0 on H. With (ζ, ζ′)ᵀ = T (K, H1)ᵀ: det T = 4r(λr+3M)/s; T(r_s) has rank 1 (not 0); its second row equals c* times its first, with c* derived as T21/T11 at r_s, equal to λ²/(3M(2λ+3)) = M/(r_s(r_s−2M)). So **ζ′(r_s) = c* ζ(r_s) for every regular solution of the flow, whether or not A = 0** |
| R.5 | **DG06's (cz) as typed** ζ′(r_s) = +2λ²/(3μ(2λ+3)) ζ(r_s): the derived c* equals −(typed constant) exactly, symbolic in M and λ and at M = −1 (c* = −λ²/(3(2λ+3)); typed +); the typed condition restricted to the solution space S = {A = 0} is ζ(r_s) = 0, which is not vacuous (the functional ζ(r_s) is not zero on S(r_s)). This check **passes iff the discrepancy of sign is exactly as stated** |
| R.6 | the ODE for ζ on S (from the flow with H eliminated by A) equals DG06's (RW17), ∂_t² → s², exactly; and the singular-point relation of that ODE at r_s (residue relation) is ζ′ = c* ζ |
| R.7 | **(nv1) against the flow and against (3)–(4).** The map (K, H1) = T⁻¹(ζ, ζ′) derived from the flow, and H on S in terms of (ζ, ζ′): typed (nv1) K equals the derived K; typed (nv1) H1 = (2/r) × the derived H1; typed H2 with ζ″ replaced through the ODE of R.6 differs from the derived H by exactly the sign of its ζ term. The same three relations hold against DG06 (3)–(4) composed with ψ = ζ/(2λr−3μ) (off-shell, symbolic in a free ζ). The corrected (nv1) (H1 denominator 2(r+μ)(2λr−3μ); H2's ζ term sign flipped) equals the derived map. This check **passes iff the relations are exactly as stated** |
| R.8 | (im) = (9)·(2λr − 3μ) exactly, and (9)∘(3) = identity on a free ψ (off-shell) |
| R.9 | **Lemma 1 mechanics on the corrected (nv1).** Numerators n_K = r²(2λr−3μ)K, n_1 at r_s are nonzero multiples of (ζ′ − c*ζ); the double-pole numerator N2 of H2 satisfies N2(r_s) ∝ (ζ′ − c*ζ), N2′(r_s) = −(L−2)/(2M) N2(r_s), and the coefficient of ζ″(r_s) in N2′(r_s) is 0. So (K, H1, H2) is smooth at r_s iff ζ is smooth and ζ′(r_s) = c* ζ(r_s): Lemma 1 holds with c* and not with the typed sign |
| R.10 | **apparent singularity of the 2-dimensional flow.** The residue matrix of the (K, H1) flow (H eliminated by A) at r_s has eigenvalues exactly {0, 1}; the compatibility condition of the resonance (no logarithm) holds identically; hence every solution of the 2-dimensional flow is analytic at r_s (consistent with R.3) |
| R.11 | **M = −1 and l = 2, 3, 4 (exact numbers).** r_s = 3/λ = 6/c with c = (l+2)(l−1) (#143's, typed 6/c); aH(r_s) = 0; T(r_s) rank 1; c* = −λ²/(3(2λ+3)) = −1/(r_s(r_s+2)) (#138 L1.2); typed (cz) constant = −c*; ζ″(r_s)/ζ(r_s) on S is −9s²/(L+1)² |
| R.S.1 | the static flow (K, H) derived from δR_rx and δG_rr at s = 0 with H1 = 0 (δR_tr = L H1/(2r²)) equals #145's printed one (typed target) exactly |
| R.S.2 | **static.** The static flow has denominators in {M, r, r−2M}; r_s is a regular point; ζ = (im)(K, K′, H) with the static flow, (ζ, ζ′) = T_s (K, H): det T_s = −8r²(λr+3M)²/(L M) (a double zero at r_s), T_s(r_s) has rank 1 with its second row equal to c* (the **same** c* as R.4) times its first. So (cz*) holds for every static solution; the typed (cz) holds only on ζ(r_s) = 0 |

What each statement does not claim: R.4 is about solutions of the flow, a linear ODE system with analytic coefficients: regular means C^∞ (= real analytic, the coefficients being rational).
It does not say that ψ or V are regular at r_s (they are not: λr+3M divides). R.9 concerns smoothness of (K, H1, H2) as functions of a free smooth ζ.

## Controls: each is `--mutate=NAME`; with `--failfast` the first FAIL id must equal the target; exit 2 at a planted id, exit 1 at a real one

Controls after PL.G / PL.X run with `--skip=PL.G,PL.X` (those planted checks act before the mutation); the baseline runs everything.

| mutation | what it changes | target |
|---|---|---|
| `dual_inv` | dual inverse uses +ε g⁻¹ h g⁻¹ (#143's) | PL.0a |
| `ds_typo` | the expected de Sitter Ricci typed as (2/a²) g | PL.0b |
| `bg_nonvac` | background f = 1 − 2M/r + M²/r² | PL.0c |
| `leg_sign` | sign error in the Legendre reduction | PL.0d |
| `lie_drop` | the partial-derivative route drops g_{μa}∂_νξ^a | PL.L |
| `drop_trace` | the first-order part of −∂_νΓ^a_μa dropped from the dual-number Ricci (#143's); the even gauge h has a nonzero trace, so it is visible | PL.G |
| `route2_drop` | route 2 drops the ∇_νδΓ^a_μa term; with `--skip=PL.G` | PL.X |
| `ext_G` | G read from the xx coefficient of xP′ without the average, as βxx − βφφ (twice G) | PL.E |
| `solve_sign` | the solved c = +r²G/2 | PL.P |
| `solve_drop_s` | the solved a without the s c term | PL.P |
| `l2_struct` | GA.1 is run with l = 1 in its range | GA.1 |
| `gs_a` | after PL.P: the solved a used in GS.1 is replaced by Jt/f (drops s c) | GS.1 |
| `hand_typo` | the typed closed form of K′ has (L/2)G → (L/4)G | GS.2 |
| `gdiv_set` | the vocabulary of GS.3 typed without r−2M | GS.3 |
| `gdiv_s` | s appended to the divisors met in GS.3 | GS.3 |
| `l2` | GU.1 is run with l = 1 in its range (the solve at L = 2 has a one-function family) | GU.1 |
| `fam_typo` | GU.2's typed family has a = 2sc/f | GU.2 |
| `st_Edep` | the "static" ansatz of GST.1 carries e^{st} | GST.1 |
| `st_l2` | GST.2 is run with l = 1 in its range | GST.2 |
| `kill_dropG` | GST.3 drops the ΔG equation | GST.3 |
| `flow_typo` | the typed K′ coefficient (r−3M) → (r−2M) in R.1's target | R.1 |
| `rs_typo` | r_s typed as −3M/(λ+1) | R.2 |
| `pole_inject` | after R.2: a term 1/(λr+3M) added to the coefficient of H in K′ (a flow with ψ's pole) | R.3 |
| `flow_h` | after R.3: the coefficient of H in K′ scaled by 1/2 | R.4 |
| `cz_coef` | the typed (cz) constant has 2λ² → 3λ² | R.5 |
| `cz_sign` | the typed (cz) has the sign of the derived condition | R.5 |
| `rw17_typo` | typed (RW17): 6λμr → 5λμr in the ζ′ coefficient | R.6 |
| `nv1_h1` | typed (nv1) H1 given the corrected denominator | R.7 |
| `nv1_h2` | typed (nv1) H2 given the corrected sign | R.7 |
| `im_coef` | (λ+1) → λ in the typed (im) | R.8 |
| `n2_sign` | N2 built with the typed sign of the ζ term | R.9 |
| `log_inject` | after R.9: the next Laurent coefficient of the (K, H1) flow perturbed (a logarithm) | R.10 |
| `rs6c_typo` | r_s at M = −1 typed 3/c instead of 6/c | R.11 |
| `sflow_typo` | #145's typed static K′ coefficient λ/M → 2λ/M in R.S.1's target | R.S.1 |
| `sflow_h` | after R.S.1: the coefficient of H in the static K′ scaled by 1/2 | R.S.2 |

Predictions that rest on structure rather than on a single line: `drop_trace` fires at PL.G only if the dropped term is not zero for the even gauge h (it is not: the trace is nonzero);
`gs_a` and `pole_inject` are applied after the checks that would otherwise catch them; `flow_h` makes ζ′ depend on H (the H cancellation 2r·H − 2r·H in ζ′ fails).
If a target is missed it is reported as a MISS and the target is not changed.

## Process

Step 1 this README; step 2 planted case and e^{st} gauge solve (`--part=planted`, `--part=gauge`), post and revise the ETA; step 3 static gauge and r_s (`--part=static`, `--part=rs`), post;
step 4 controls (one process, systemd user unit `nm-i146-*`); step 5 final run `zerilli_gauge_rs_output.txt` and final controls. Every stdout goes to a log in this folder.
A run not finished in 1 h of wall time is stopped and reported. Nothing is stopped for memory; peak rss is recorded with `/usr/bin/time -v`.

## Edited before the first run of `zerilli_gauge_rs.py`

The first runs were development runs (`dev1.log` planted part, `dev2.log` through the static part, `dev3.log` through R.S.2; all with `--skip=PL.G,PL.X`).
`dev2` had one FAIL, GS.3, a bug in my check and not in the criterion: the expected divisor set was compared as the string `r - 2*M`, which sympy prints as `-2*M + r`.
The divisors it found were exactly {r, r−2M}. The comparison now uses `str(r - 2*M)`; the criterion (the divisors met are exactly {r, r−2M}) is unchanged. `dev3` then had 0 FAIL.
Nothing else was changed in a criterion or a control target after these runs.

## Added after the first run

Written after `dev1`–`dev4`, `step2`, `step3` and the first controls run (`controls.log`: baseline and 35 pairs, 36 OK, 0 MISS, 726 s; the script then had 32 PASS), and before the
final run and the final controls run. No criterion or control target above was changed. Two checks and two mutations were added, and one bug of mine fixed:

- **PL.R** (planted, exit 2): the Laurent / resonance routine of R.10 (`laurent_test`) on three planted flows with known answers: R = diag(0,1) with F1 = 0 (analytic, sympy's `dsolve` of u′ = u/x
  has no logarithm), R = diag(0,1) with the coupling u₂′ = u₂/x + u₁ (`dsolve` returns a logarithm), and a residue with eigenvalues {0, 2}. Mutation `nolog_blind` (the routine ignores the next
  Laurent coefficient) → PL.R. Added because R.10's routine had no planted case in the list above; R.10 calls the same routine.
- **R.12**: M = −1, l = 2, explicit smooth ζ: with ζ′(r_s) = c* ζ(r_s) the corrected (nv1) gives (K, H1, H2) with no pole at r_s; ζ = 1 and a ζ with the typed (cz) constant give poles in all three.
  Mutation `ex_typed` (the conforming ζ is built with the typed constant) → R.12. Added to have a concrete counterexample for the typed sign.
- `laurent_test` raised an IndexError on the eigenvalue-{0,2} planted flow (no resonance, no left null vector); it now returns (False, False) there.

## Results (written after the final controls run)

| file | what | result |
|---|---|---|
| `dev1.log` … `dev4.log` | development runs of the planted part, through the static part, through R.S.2, and the final script with `--skip=PL.G,PL.X` | `dev2` had the GS.3 string-comparison FAIL (my check bug, see above); `dev1`, `dev3`, `dev4` 0 FAIL |
| `step2.log` | `--part=gauge`, nothing skipped | 16 PASS, 0 FAIL, exit 0, 105 s |
| `step3.log` | `--part=all` on the script before PL.R and R.12 | 32 PASS, 0 FAIL, exit 0, 123 s, rss 104 MB |
| `controls.log`, `controls_logs/` | first controls run (baseline and 35 pairs) | 36 OK, 0 MISS, 726 s |
| `final.log` | `--part=all`, nothing skipped = `phase2/dg_proof/zerilli_gauge_rs_output.txt` | 34 PASS, 0 FAIL, exit 0, 124 s (PL.G about 88 s), rss 104 MB |
| `controls_final.log`, `controls_final_logs/` | final controls (baseline and 37 pairs) = `zerilli_gauge_rs_controls_output.txt` | 38 OK, 0 MISS, 762 s, rss 119 MB |

Every target in the control table above was hit; the two added mutations (`nolog_blind`, `ex_typed`) were on target in their first run. The predictions resting on structure all held.
`DG06` TeX: `dg06_src/` (copied from `I145-rpi5/dg06_src`, sha256 of `nakedsingularity2.tex` 4da32b56…). Launchers: `run_step.sh`, `run_controls.sh` (systemd user units `nm-i146-*`).
