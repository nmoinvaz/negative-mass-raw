# I143-rpi5: derivation of the static even-parity (Zerilli) potential for M < 0 from the linearized Einstein equations

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10, one thread.
Issue: https://github.com/nmoinvaz/negative-mass/issues/143
Worktree: `~/Source/negative-mass-i143`, branch `wip/i143-zerilli-derivation` (base main ff23585).
Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0, mpmath 1.3.0). Exact rational-function algebra only; no floats anywhere.

Written 2026-11-23, before any check was run. Check ids and control targets below are fixed before the first run. Anything added after
seeing data is listed at the end under "Added after the first run".

## Independence

Written from the issue, RESULTS.md §4.2 (the V to compare with) and DG06's TeX (eqs. (1)-(9)). No script of phase2 and no output of #8 or #142
was opened. The only formulas typed from outside are the ones named in the next table, each used as a target of a comparison and never as an
input of the derivation, except the definition of the master variable (DG06 eq. (9)), which is the one typed input of the reduction.
Everything else (the linearized tensor, the radial equations, the algebraic relation, the first-order system, the ODE of the master variable and
its potential V) comes out of the metric.

| tag | source | read | used for |
|---|---|---|---|
| DG06 | Dotti, Gleiser, Class. Quantum Grav. 23 (2006) 5063, arXiv:gr-qc/0604021, TeX source (`nakedsingularity2.tex`) | eqs. (1)-(9) | metric ansatz (2), map ψ_Z → (K, H1, H2) (3)-(4), V (6), r* (8), master variable (9) |
| RES | `phase2/dg_proof/RESULTS.md` §4.2 | the V and f at M = -1 | comparison at M = -1 |
| Z70 | Zerilli, PRL 24 (1970) 737; PRD 2 (1970) 2141 | publisher page: HTTP 403 (checked 2026-11-23 at doi.org, link.aps.org and journals.aps.org) | **(unverified)**: not read; the potential's published form is taken from DG06 (6), as in #142 |

The Zerilli form used as the comparison target (symbolic in r, l, M), with λ = (l-1)(l+2)/2 and f = 1 - 2M/r:

  V_Z = 2 f [λ²(λ+1) r³ + 3λ² M r² + 9λ M² r + 9 M³] / (r³ (λ r + 3M)²)

It is not an input of the derivation.

## Setup of the derivation

Coordinates (t, r, x = cos θ, φ). Then the unit sphere is dx²/(1-x²) + (1-x²) dφ², everything is rational in (r, x, M, s, l), and no trigonometric
simplification is needed. P(x) = P_l(x) is an abstract function obeying Legendre's equation (1-x²)P'' - 2xP' + L P = 0, L = l(l+1) symbolic; derivatives of
order ≥ 2 are removed with it. Time dependence e^{st}, axisymmetric (m = 0), Regge-Wheeler gauge, DG06's sign conventions:

  g_tt = -f (1 - ε H0 P e^{st}), g_tr = ε H1 P e^{st}, g_rr = f⁻¹ (1 + ε H2 P e^{st}), angular part r² (1 + ε K P e^{st}) (unit sphere).

First order in ε is carried by a dual-number class (a0 + ε a1, ε² = 0), so the inverse metric, the Christoffel symbols and the Ricci tensor are
built from the definitions with the first order exact by construction. Odd parity: g_tφ = ε h0 e^{st} (1-x²) P', g_rφ = ε h1 e^{st} (1-x²) P'.

## Checks (id : statement : what a failure means)

Planted checks run first; a failed planted check ends the script with exit 2 before any real data. A real failed check exits 1.

| id | statement |
|---|---|
| PL.0a | the dual inverse satisfies g·g⁻¹ = 1 exactly (first order), for a generic symmetric h |
| PL.0b | planted known Ricci: static de Sitter ds² = -(1 - r²/a²)dt² + dr²/(1 - r²/a²) + r²dΩ², R_μν = (3/a²) g_μν, all components exactly |
| PL.0c | background vacuum: R_μν[g_Schw(M)] = 0 exactly, M symbolic |
| PL.0d | the Legendre reduction on P_l(x) explicit, l = 2..6: the reduced expression for P'', P''', P'''' equals the true derivative |
| PL.G | pure gauge: h = L_ξ g_Schw for an even ξ (three free functions of r, times e^{st} P) and an odd ξ (one function) gives δR_μν = 0, all 10 components, M, l, s symbolic |
| PL.X | independent route: δR_μν = ∇_a δΓ^a_μν − ∇_ν δΓ^a_μa with δΓ from covariant derivatives of h (shares with the dual-number route only the background Γ and h) equals the dual-number δR_μν, all components, for the even ansatz, the odd ansatz and the gauge h |
| PL.O.1 | odd parity: every δR component has the expected angular form (an r-function times an angular structure; x-independence of the coefficients) |
| PL.O.2 | the odd equations reduce: h0 is solved from δR_xφ (divisor named), and then δR_tφ and δR_rφ are implied by one second-order ODE of Ψ = f h1/r |
| PL.O.3 | **planted target:** Ψ,ₓₓ = (V_RW + s²)Ψ with the coefficient of Ψ,ₓ exactly 0 and V_RW = f (l(l+1)/r² − 6M/r³) exactly, symbolic in r, l, M |
| PL.O.4 | the comparison routine reports a planted unequal pair as unequal |
| A.1 | P and xP' are linearly independent for L ∉ {0, 2} (symbolic: P = A x^c in the Legendre equation forces c(c-1) = 0 and L = c(c+1)); rank 2 of the coefficient matrices for l = 2..30; rank 1 at l = 1 |
| A.2 | every even δR component has the expected angular form: coefficients of P and of xP' are x-independent times the structure, for all 7 components |
| E.1 | the traceless angular equation equals c₀ (H0 − H2) with c₀ ≠ 0 an explicit factor: H0 = H2 (l ≥ 2) |
| E.2 | δR_tr, δR_tx, δR_rx (first order, no second derivatives) solve for K', H1', H' (determinant of the coefficient matrix printed and factored); δG_rr after these substitutions has no derivative left: an algebraic relation A(H, H1, K) = 0 |
| E.3 | consistency: d/dr of A along the first-order flow is κ(r) A exactly |
| E.4 | completeness: every remaining radial equation (tt, angular trace, second-order forms, all 9 coefficient equations of the 7 components) is exactly 0 on the surface A = 0 along the flow |
| E.5a | the master variable of DG06 (9), ψ = r(r-2M)/((λ+1)(λr+3M)) (H2 − r K') + r K/(λ+1), reduces to ψ = p K + q H1 on the surface; p, q printed |
| E.5b | ψ,ₓₓ = a ψ + b ψ,ₓ derived from the flow (x tortoise, d/dx = f d/dr): b = 0 exactly |
| E.5c | a − s² does not depend on s (∂/∂s = 0), and equals the derived V |
| E.5d | derived V = V_Z exactly, symbolic in r, l, M (and in λ) |
| E.5e | at M = -1: derived V = V of RESULTS §4.2, 2f[λ²r²((λ+1)r-3) + 9(λr-1)]/(r³(λr-3)²), f = 1 + 2/r, λ = c/2, exactly |
| E.6a | converse: DG06 (3)-(4) with e^{st} substituted, ψ,ₓₓ = (V+s²)ψ imposed, satisfies all radial equations exactly |
| E.6b | (9) applied to the output of (3) returns ψ exactly |
| D.* | divisions: the denominators met in E.1-E.5 are listed with the step; each stated factor is verified symbolically (D.1 λr+3M, D.2 s, D.3 f and r-2M, D.4 l ≥ 2, D.5 the det of E.2/E.5a); at M = -1, λr+3M = 0 at r = 3/λ = 6/c = r_s of dg_proof, and r_s is positive only for M < 0 |

## Controls: each is `--mutate=NAME`; the first FAIL id must equal the target below (run with `--failfast`)

| mutation | what it changes | target (first FAIL id) |
|---|---|---|
| `fsign_bg` | f = 1 + 2M/r in the background metric (wrong sign of M in f) | PL.0c (exit 2); PL.0b still passes |
| `fsign_mv` | wrong sign of M in the factor r-2M of the master variable (9) (r+2M) | E.5b |
| `mv_coef` | (λ+1) → λ in the master variable's second term r K/(λ+1) | E.5b |
| `drop_trace` | the first-order part of −∂_ν Γ^a_μa is dropped from the dual-number Ricci (the background part is kept) | PL.G (exit 2); PL.0c, PL.O.* still pass (the trace of the odd h is 0) |
| `v_typo` | one coefficient of the typed V_Z changed (9λM²r → 9λMr) | E.5d (E.5b, E.5c still pass) |
| `rw_typo` | −6M/r³ → −3M/r³ in the typed V_RW | PL.O.3 (exit 2) |
| `l1` | the angular independence check run at L = 2 (l = 1) | A.1 |
| `dual_inv` | the dual inverse uses +ε g⁻¹ h g⁻¹ | PL.0a (exit 2) |
| `leg_sign` | sign error in the Legendre reduction (+L P) | PL.0d (exit 2) |
| `route2_drop` | route 2 drops the ∇_ν δΓ^a_μa term | PL.X (exit 2) |
| `res_typo` | one coefficient of RESULTS' V typed wrongly (9(λr−1) → 9(λr−2)) | E.5e |
| `dg3_typo` | DG06 (4): h(r) with −3M² → −2M² | E.6a |
| `skip_s` | the algebraic relation A, once derived, has its H1 coefficient scaled by 2 | E.3 |

Unmutated: exit 0, no FAIL. Planted: PL.0a..PL.O.4. Real: A.1..D.*.

## Process

Step 2 (linearized tensor, planted odd case) and step 3 (even parity) are exploratory runs first (logs here), the finals follow in step 5.
Every stdout goes to a log in this folder. Any single run longer than 1 h of wall time is stopped and reported.

## Added after the first run

(nothing yet)
