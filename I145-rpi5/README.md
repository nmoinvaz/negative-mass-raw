# I145-rpi5: the static (s = 0) even-parity equation and its master variable, from the linearized Einstein equations

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10, one thread.
Issue: https://github.com/nmoinvaz/negative-mass/issues/145
Worktree: `~/Source/negative-mass-i145`, branch `wip/i145-zerilli-static` (base main 9fba0b0).
Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0, mpmath 1.3.0). Exact rational-function algebra only; no floats.

Written 2026-11-23, before the new script was run. Check ids and control targets below are fixed before its first run. Anything added after
seeing data is listed at the end under "Added after the first run".

## What was read, and what is shared with #143

Read before writing: AGENTS.md; #145 and #143 (issue text and comments); `phase2/dg_proof/zerilli_derivation.md` (all, including the coordinator's
review); `negative-mass-raw/I143-mac/README.md` (criteria Y0-Y5 and the observation after them; **`ind143.py` itself not opened**); RESULTS.md §4.2, §4.6, §6;
#143's `zerilli_derivation_lib.py` and `zerilli_derivation.py` (both read in full; the library is **imported** by `zerilli_static.py`, the driver's structure and its
typed DG06 formulas are adapted from `zerilli_derivation.py`); DG06's TeX (below). Not opened: any other script of phase2.

| tag | source | read | used for |
|---|---|---|---|
| DG06 | Dotti, Gleiser, CQG 23 (2006) 5063, arXiv:gr-qc/0604021, TeX source re-fetched 2026-11-23 into `dg06_src/` (gunzip of the e-print, `nakedsingularity2.tex`) | eqs. (2)-(6), (9) read again; the formulas typed in #143's driver agree with them | ansatz (2), map (3)-(4), V (6), master variable (9) |
| RES | `phase2/dg_proof/RESULTS.md` §4.2 | V and f at M = -1 | comparison at M = -1 |
| #143 | `zerilli_derivation.md`, its flow, A, ψ = [r²K − (r−2M)H1/s]/(λr+3M) | typed as comparison targets in S.R1, S.R3 only | the s → 0 relation |
| RW, CPM | Regge-Wheeler potential V_RW = f(L/r² − 6M/r³) (given in the task); the Cunningham-Price-Moncrief combination Ψ = r h0' − 2 h0 as the static odd master variable | **not read**, recalled; (unverified) as a literature statement | planted odd target; its master variable is the one typed input of the planted case, as DG06 (9) is of the real one |
| Z70 | Zerilli's papers | not read (publisher HTTP 403 in #143) **(unverified)** | nothing |

Comparison target of E.5d (symbolic in r, l, M), λ = (l-1)(l+2)/2, f = 1 - 2M/r (it is the V of #143, not an input of the derivation):

  V_Z = 2 f [λ²(λ+1) r³ + 3λ² M r² + 9λ M² r + 9 M³] / (r³ (λ r + 3M)²)

## Setup

Coordinates (t, r, x = cos θ, φ); everything rational. P(x) = P_l(x) abstract with Legendre's equation, L = l(l+1) one symbol, M symbolic.
**Static:** no time dependence at all (the ansatz carries no e^{st}, the symbol s does not occur in any static equation). DG06's sign conventions as in #143:
g_tt = -f(1 - ε H0 P), g_tr = ε H1 P, g_rr = f⁻¹(1 + ε H2 P), angular r²(1 + ε K P) on the unit sphere; odd: g_tφ = ε h0 (1-x²)P', g_rφ = ε h1 (1-x²)P'.
First order in ε by #143's dual numbers (imported). The time-dependent e^{st} ansatz of #143 is rebuilt only for S.0 and S.R*.

## Checks (id : statement). A failed planted check (PL.*) ends the script with exit 2 before any real data; a failed real check exits 1.

| id | statement |
|---|---|
| PL.0a | dual inverse: g·g⁻¹ = 1 to first order for a generic symmetric h |
| PL.0b | static de Sitter has R_μν = (3/a²) g_μν, all components |
| PL.0c | R_μν[g_Schw(M)] = 0, M symbolic |
| PL.0d | the Legendre reduction equals the explicit derivatives of P_l, l = 2..6, orders 2, 3, 4 |
| PL.G | h = L_ξ g_Schw for a static even ξ (a P, b P, c (1-x²)P'/r²) and a static odd ξ (d P') gives δR_μν = 0, all 10 components |
| PL.X | the covariant route δR = ∇δΓ − ∇δΓ equals the dual-number route in every component for the static even ansatz, the static odd ansatz and the static even gauge h |
| PL.O.1 | static odd components have the expected angular form (x-independent coefficients times the structure); the other odd-sector components vanish |
| PL.O.2 | static odd reduction: δR_rφ is c(r) h1 alone with c ≠ 0 for L ≠ 2, so h1 = 0; δR_xφ contains h1 jets only (so it is implied); δR_tφ contains h0 jets only and is second order in h0 |
| PL.O.3 | **planted target:** Ψ = r h0' − 2 h0 (CPM) obeys Ψ,ₓₓ = V Ψ with the coefficient of Ψ,ₓ exactly 0 and V = f (l(l+1)/r² − 6M/r³) exactly, symbolic in r, l, M |
| PL.O.4 | the comparison routine reports a planted unequal pair as unequal |
| A.1 | P and xP' are independent for L ∉ {0, 2} (symbolic; rank 2 for l = 2..30; rank 1 at l = 1) |
| A.2 | the seven even components have the expected angular form (x-independent coefficients of P and xP' or P'), and the angular-tensor covariance identities hold |
| S.1 | none of the nine static even coefficient equations contains the symbol s |
| H.1 | **H1 sector, tr:** δR_tr is c_tr(r, M, L)·H1 with no other jet; c_tr is an explicit nonzero factor, so H1 = 0 wherever c_tr ≠ 0 |
| H.2 | **H1 sector, tx:** δR_tx contains H1 jets only, so it is implied by H1 = 0 |
| H.3 | **decoupling:** tt, rr, rx and the angular components contain no H1 jet |
| E.1 | the traceless angular equation is c₀ (H0 − H2), c₀ ≠ 0: H0 = H2 =: H (l ≥ 2 through A.1) |
| E.2 | δR_rx and δG_rr (= δR_rr/2 + δR_tt/(2f²) − (angular trace)/(2 f r²)) have no second derivative; they are solved for (K', H'); determinant of the coefficient matrix printed and factored; the flow F(K, H) is explicit |
| E.4 | completeness: δR_tt, δR_rr and the angular trace vanish **identically** on the flow of E.2 (if they instead reduce to a nonzero algebraic relation, that is reported as a result: the static solution space would be smaller than 2-dimensional) |
| E.5a | DG06 (9) with K' from the flow is ψ = p K + q H with p, q printed; the map (K, H) → (ψ, ψ,ₓ) has a nonzero determinant (printed) |
| E.5b | ψ,ₓₓ = a ψ + b ψ,ₓ from the flow (d/dx = f d/dr): b = 0 exactly |
| E.5d | a = V_Z exactly, symbolic in r, l, M (and again with L = l(l+1)) |
| E.5e | at M = -1, a equals RESULTS §4.2's V = 2f[λ²r²((λ+1)r-3) + 9(λr-1)]/(r³(λr-3)²), f = 1 + 2/r, λ = c/2, exactly |
| E.6a | converse: DG06 (3)-(4) at s = 0 (H1 = 0, K = Fψ + fψ', H0 = H2 = (f(hψ + rψ'))' − K) with ψ,ₓₓ = Vψ satisfies all seven radial equations (tt, tr, rr, tx, rx, trace, traceless), exactly |
| E.6b | (9) o (3) = identity on ψ (modulo the equation), and (3) o (9) = identity on (K, H) (modulo the flow): the two maps are inverse |
| S.0 | the static coefficient equations equal the s = 0 values of the nine e^{st} coefficient equations (same code, time-dependent ansatz), all components |
| S.R1 | with H1 = s h̃1, (δR_tr / s) at s = 0 is a nonzero multiple of K' + (r−3M)/(r(r−2M)) K − H/r − L h̃1/(2r²), the tr line of `zerilli_derivation.md` §3 at H1/s = h̃1 |
| S.R2 | define h̃1 from that equation (solved, not typed); then (δR_tx / s) at s = 0, i.e. (f h̃1)' − H − K, vanishes on the static flow: every static solution is the s → 0 limit of an e^{st} solution |
| S.R3 | with that h̃1, DG06 (9) of the static solution equals ψ = [r²K − (r−2M) h̃1]/(λr+3M), #143's map with H1/s → h̃1 |
| D.1 | every divisor met (the factors of the denominators of c_tr, c₀, the flow, p, q, a, V and of (9)) lies in {r, r−2M, L, L−2, λr+3M, M} |
| D.2 | λr + 3M = 0 at r = −3M/λ, positive iff M < 0; (λr+3M)²V there is (L−2)²(L+1)²/18 ≠ 0 (a genuine double pole); at M = −1 the zero is 6/c = r_s |
| D.3 | no step divides by s |
| D.4 | no step divides by L − 2 = 2λ; the steps that divide by L and by r − 2M are listed |
| D.5 | the determinants of E.2 and E.5a and c_tr are nonzero rational functions |

## Controls: each is `--mutate=NAME`; with `--failfast` the first FAIL id must equal the target; exit 2 at a planted id, exit 1 at a real one

| mutation | what it changes | target |
|---|---|---|
| `dual_inv` | dual inverse uses +ε g⁻¹ h g⁻¹ (#143's) | PL.0a |
| `ds_typo` | the expected de Sitter Ricci typed as (2/a²) g | PL.0b |
| `bg_nonvac` | background f = 1 − 2M/r + M²/r² (not a vacuum solution) | PL.0c |
| `leg_sign` | sign error in the Legendre reduction (#143's) | PL.0d |
| `drop_trace` | the first-order part of −∂_ν Γ^a_μa dropped from the dual-number Ricci (#143's); predicted visible because the static even gauge h has a nonzero trace | PL.G |
| `route2_drop` | route 2 drops the ∇_ν δΓ^a_μa term (#143's); run with `--skip=PL.G` | PL.X |
| `ang_norm_odd` | tφ component read without the factor 1/(1-x²) | PL.O.1 |
| `inj_rphi` | the static δR_rφ equation gets an extra h0 term | PL.O.2 |
| `rw_typo` | −6M/r³ → −3M/r³ in the typed V_RW | PL.O.3 |
| `fsign_ans` | wrong sign of M in f in the master-variable machinery and the tortoise factor (#143's) | PL.O.3 |
| `cpm_typo` | the typed Ψ = r h0' − 2 h0 becomes r h0' − 3 h0 | PL.O.3 |
| `cmp_blind` | the comparison routine evaluates at M = 0 only | PL.O.4 |
| `l1` | the independence check run at L = 2 | A.1 |
| `ang_norm` | xx component read without the factor 1-x² | A.2 |
| `s_leak` | an s K term added to the rx coefficient equation after A.2 | S.1 |
| `inj_tr` | a K term added to δR_tr after A.2 | H.1 |
| `inj_tx` | a K term added to δR_tx after A.2 | H.2 |
| `inj_h1` | an H1 term added to δR_rr after A.2 | H.3 |
| `ans_rr` | g_rr = f⁻¹ + ε H2 P in the ansatz (no 1/f on H2) | E.1 |
| `grr_drop` | the angular-trace term dropped from δG_rr, which should leave a second derivative (K'') in it | E.2 |
| `tt_drop_K` | the undifferentiated K term dropped from δR_tt after A.2 (a dropped term of the linearized tensor), after which δG_rr stays first order and the determinant is unchanged | E.4 |
| `psi_zero` | the master variable replaced by 0, so the (K, H) → (ψ, ψ,ₓ) determinant is 0 | E.5a |
| `mv_coef` | (λ+1) → λ in the second term r K/(λ+1) of (9) | E.5b |
| `fsign_mv` | r − 2M → r + 2M in the prefactor of (9) | E.5b |
| `mv_lam` | λr + 3M → λr + 2M in the prefactor of (9) | E.5b |
| `v_typo` | typed V_Z: 9λM²r → 9λMr | E.5d (E.5b passes) |
| `res_typo` | typed RESULTS V: 9(λr−1) → 9(λr−2) | E.5e |
| `dg3_typo` | DG06 (4) h(r): −3M² → −2M² | E.6a |
| `inv_typo` | the typed copy of (9) used in E.6b has (λ+1) → (λ+2) in the prefactor | E.6b |
| `dep_typo` | the e^{st} ansatz has g_tr = 2 ε H1 P e^{st} | S.0 |
| `tr_typo` | the typed tr line of #143 has L/(2r²) → L/(3r²) | S.R1 |
| `h1t_typo` | the solved h̃1 is multiplied by 3/2 | S.R2 |
| `sr_typo` | the typed #143 map has λr + 3M → λr + 2M | S.R3 |
| `div_set` | the stated divisor set typed with λr + 7M | D.1 |
| `d2_zero` | the zero of λr + 2M instead of λr + 3M | D.2 |
| `div_s` | s appended to the divisors met | D.3 |
| `div_l2` | L − 2 appended to the divisors met | D.4 |
| `d5_zero` | the determinant of E.2 replaced by 0 in the D.5 list | D.5 |

Controls after PL.G / PL.X run with `--skip=PL.G,PL.X` (those planted checks act before the mutation); the baseline runs everything. Unmutated: exit 0, no FAIL.
The prediction for `grr_drop` (E.2) rests on a structural argument (K'' enters δR_rr and the angular trace but not δR_tt); `tt_drop_K` (E.4) assumes the dropped term
does not change the determinant. If either target is missed it is reported as a MISS and the target is not changed.

## Process

Step 2: planted odd case and the H1 sector (exploratory run, `--part=odd` and `--part=h1`); step 3: even reductions; step 4: controls (one process, systemd unit `nm-i145-*`);
step 5: final run and final controls. Every stdout goes to a log in this folder. A run not finished in 1 h of wall time is stopped and reported. Nothing is stopped for memory;
peak rss is recorded with `/usr/bin/time -v`.

## Added after the first run

(empty)
