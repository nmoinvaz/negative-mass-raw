# I148-rpi5: certificate of the Zerilli reduction's forward direction for every l, without dividing by M or s (#148)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10, one thread.
Issue: https://github.com/nmoinvaz/negative-mass/issues/148
Worktree: `~/Source/negative-mass-i148`, branch `wip/i148-zerilli-certificate` (base main fd95d71).
Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0, mpmath 1.3.0).

Written 2026-11-23, before the first run of `zerilli_certificate.py`. Criteria, the planted case, control names and targets below are
fixed here. Anything added after seeing data is listed at the end under "Added after the first run".

Before this README I built the seven even and the three odd radial equations interactively with #143's library (a scratch
script outside the repository) and read them, to know which jets they contain and how they are normalized. I solved for no
certificate and ran no check. I did not open `ind143.py`, `ind145.py` or `ind146.py`.

## What is built

- **Equations.** The radial equations are the coefficients of the angular structures in the first-order Ricci tensor δR_ab of
  g_Schw(M) + ε h, h in Regge–Wheeler gauge (axisymmetric, e^{st}, P(x), x = cos θ), made with #143's library
  `zerilli_derivation_lib.py`, imported unchanged: dual-number Ricci, Legendre reduction `leg_red` (P″ removed, L = l(l+1) one
  symbol), `coef_eqs`. Even, H0, H1, H2, K all kept, seven equations: tt (P), tr (P), rr (P), tx (P′), rx (P′), trace
  = xx(P) + pp(P), traceless = xx(xP′) = (H0 − H2)/2. Odd: tφ (P′), rφ (P′), xφ (xP′; its P coefficient is −(L/2) times that).
  Each equation is used with the normalization #143's SPEC gives it (covariant components δR_ab, sphere factor of the angular
  component removed). The certificate's denominators depend on that normalization: rescaling an equation by a function of r
  rescales its coefficients. The normalization is part of the claim and is stated in the note.
- **Targets.** Even: Z = ψ,ₓₓ − (V + s²)ψ with ψ = r(r−2M)/((λ+1)(λr+3M)) (H2 − r K′) + r K/(λ+1) (DG06 (9)),
  d/dx = f d/dr, f = 1 − 2M/r, λ = (L−2)/2, V = 2f[λ²(λ+1)r³ + 3λ²M r² + 9λM² r + 9M³]/(r³(λr + 3M)²) (the issue's text, typed
  in the script, not taken from #143's scripts). Odd (planted): Z = Ψ,ₓₓ − (V_RW + s²)Ψ, Ψ = f h1/r, V_RW = f(L/r² − 6M/r³).
- **Certificate.** Z = Σ_{i,k} c_ik D^k E_i, D = d/dr on jets, k = 0, 1, 2, c_ik in F = Q(r, M, s, L). Finding it is a linear
  system over F: unknowns c_ik, one row per jet monomial (H0_n, H1_n, H2_n, K_n). Solved by Gauss–Jordan elimination in the
  rational function field of `sympy.polys.fields`, a particular solution with the free unknowns 0.
  Column order O1: k ascending; within k: traceless, tx, tr, rx, tt, rr, trace.
  The certificate is not unique (the equations satisfy Bianchi identities), so its denominators depend on the solution.
  Procedure if the first solution's denominators fail E.den, fixed now: reversed order within k; k descending; permutations with
  seeds 1 to 20. Every attempt and its denominators are reported. A solution that passes E.den is a certificate, because
  E.id verifies it by a path that does not use the solver. If no certificate exists with k ≤ 2, k ≤ 3 is tried and reported.
  The pilot is `--L=6` (the same script with L = 6 substituted before the solve).
- **Independence of E.id from the solve.** E.id recomputes D^k E_i with sympy's `diff` on expressions in Function(r)
  (the solver differentiates linear forms on jets), types Z from the sympy formulas for ψ and V, and compares in the
  rational function field with exact canonical forms. It also evaluates the identity at 3 random rational points of (r, M, s, L).

## Criteria, each can fail

Planted checks exit 2 at once. Real checks are counted, exit 1 at the end. Ids in order of the run.

| id | check | pass condition |
|---|---|---|
| PL.0c | background | Ricci of g_Schw(M) is 0, M symbolic (as #143 PL.0c) |
| PL.0d | Legendre reduction | `leg_red` of P⁽ⁿ⁾, n = 2, 3, 4, equals the explicit derivative of P_l for l = 2..6 (as #143 PL.0d) |
| PL.D.1 | planted self-test of the denominator classifier | the classifier gives these verdicts on constructed denominators. Even rule, pass: r²((L−2)r+6M)²; r L (L+1); r³((L−2)r+6M)(L−5). Even rule, fail: r(r−2M); s r; M r; (L−2) r; (L−6) r (root L = 6, l = 2); (L−12) r (l = 3). Odd rule, pass: r²(r−2M); fail: s r. 11 cases in all |
| PL.O.1 | odd forms | each odd component has its expected angular form (`coef_eqs` ok) and xφ(P) + (L/2) xφ(xP′) = 0 |
| PL.O.2 | odd span test | the linear system for Z_odd has a solution (k ≤ 2) |
| PL.O.3 | odd identity | E.id for the odd certificate: exact in F and at 3 random points |
| PL.O.4 | odd denominators | every irreducible denominator factor is r, r − 2M, or a polynomial in L alone (rule below). Prediction: pass |
| A.1 | P and xP′ independent | for L not in {0, 2} (as #143 A.1; each angular coefficient is its own equation) |
| E.1 | even forms | all seven components have the expected angular form; xx(xP′) + pp(xP′) = 0 and pp(P) − xx(P) − L xx(xP′) = 0; traceless = (H0 − H2)/2 |
| S.explicit | explicit l | for l = 2, 3, 4 δR_ab computed with the explicit P_l (no Legendre reduction, no coefficient extraction) equals the reconstruction from the coefficient forms at L = l(l+1), all 7 nonzero components, exact |
| E.cert | even span test | the system for Z has a solution with k ≤ 2, L symbolic |
| E.id | even identity | exact in F by the independent path, and at 3 random rational points |
| E.den | even denominators | every irreducible factor of every c_ik's denominator is r, (L−2)r + 6M, or a polynomial in L alone (rule below); the list of factors and their highest exponents is printed |
| E.L | specialization | for L = 6, 12, 20 (l = 2, 3, 4): Z retyped from λ = (l−1)(l+2)/2 (not by substituting L), certificate and equations at L = l(l+1), identity exact in Q(r, M, s) for every jet; no denominator of a c_ik vanishes identically at that L |
| E.M0 | M = 0 | V at M = 0 equals L/r² exactly; Z retyped with f = 1 and V = L/r²; c_ik at M = 0 finite, identity exact with the equations at M = 0 |
| E.S0 | s = 0 | Z retyped as ψ,ₓₓ − Vψ; c_ik at s = 0 finite, identity exact with the equations at s = 0 (the static equation) |

**Denominator rule (E.den, PL.O.4).** Write each c_ik in lowest terms n/d and factor d over Q. A factor is allowed if it is r, or
(even) (L−2)r + 6M = 2(λr + 3M), or (odd) r − 2M, or a polynomial in L alone. A polynomial in L alone is allowed only if it is
not L − 2 and has no rational root l(l+1) with l an integer ≥ 2. Anything else fails: s, M, r − 2M (even), L − 2, an L-only factor with
such a root, and any factor that mixes the variables otherwise. The issue's wording ("no M, no s, no L − 2") is met by this rule and
is stricter than it, since r − 2M contains M. Not a criterion, a prediction: the coordinator's certificates at l = 2, 3, 4 have
denominators r²(λr + 3M)² up to a constant, so the highest exponents are expected to be 2 and 2.

**What is not checked here:** the converse (#143 E.6), the existence of Regge–Wheeler gauge (#146), r = r_s itself, and the
independence of the seven equations beyond A.1. The three checks above those are #143's, #145's and #146's.

## Controls

Each is `--mutate=NAME`; the run must exit with the stated code and the first FAIL id equal to the target. Names common with
#143's library: `leg_sign`, `l1` (the lib's `mut()` reads `--mutate=`). Written before the first run.

| name | what it changes | target (first FAIL) | exit |
|---|---|---|---|
| leg_sign | Legendre reduction P″ = (2xP′ + LP)/(1−x²) (lib) | PL.0d | 2 |
| den_allow_M | the classifier's allowed set also contains M | PL.D.1 | 2 |
| odd_v | V_RW typed with −5M/r³ in place of −6M/r³ | PL.O.2 | 2 |
| odd_psi | Ψ typed as h1/r in place of f h1/r | PL.O.2 | 2 |
| odd_cert | one coefficient of the odd certificate changed by +r after the solve | PL.O.3 | 2 |
| odd_den | the odd target replaced by the xφ equation scaled to leading coefficient 1 in h0 (needs 1/s) | PL.O.4 | 2 |
| l1 | A.1 evaluated at L = 2 | A.1 | 1 |
| expl_norm | S.explicit reconstructs the xx and pp components without the factor 1/(1−x²) resp. (1−x²) | S.explicit | 1 |
| v_coef | V typed with 8λM²r in place of 9λM²r | E.cert | 1 |
| psi_coef | (9) typed with r K/λ in place of r K/(λ+1) | E.cert | 1 |
| v_s2 | Z typed as ψ,ₓₓ − Vψ (no s²) | E.cert | 1 |
| drop_traceless | the traceless equation removed from the span | E.cert | 1 |
| flow_target | Z replaced by the K′ form of #143's flow, K′ + (r−3M)/(r(r−2M)) K − L H1/(2s r²) − H2/r: in the span only with 1/s | E.den | 1 |
| cert_coef | one coefficient of the even certificate changed by +r after the solve | E.id | 1 |
| l_spec | the retyped Z of E.L uses λ = (l−1)(l+1)/2 | E.L | 1 |
| m0_v | V at M = 0 typed as (L+2)/r² in E.M0 | E.M0 | 1 |
| s0_s1 | the static target typed as ψ,ₓₓ − (V+1)ψ | E.S0 | 1 |

An exploratory family, not part of the required set: `drop_tt`, `drop_tr`, `drop_rr`, `drop_tx`, `drop_rx`, `drop_trace`
(one equation removed). Predicted first FAIL: E.cert if the equation is needed over F, E.den if it is replaceable only through a
Bianchi identity that divides by s (the t-component of the linearized Bianchi identity relates s·E_tt to D E_tr and E_tx). I do not know
which of the two fires for which equation. A drop that exits 0 is an equation the certificate does not need, reported as that, not as a
missed control.

`drop_traceless` is predicted to fire at E.cert with confidence: only the traceless equation gives H0 = H2, and the target has
no H0.

## Runs and limits

1. Step 2: `--part=planted` (PL.*), then the odd certificate, then the pilot `--L=6 --part=even`. Post.
2. Step 3: even certificate with L symbolic, E.den, E.L, E.M0, E.S0. Post.
3. Step 4: `zerilli_certificate_controls.py` (baseline + the pairs above). Step 5: final run, stdout to `phase2/dg_proof/zerilli_certificate_output.txt`.
- One process at a time, nice 10, `OMP_NUM_THREADS=1`, systemd user units `nm-i148-*`, exit codes in `*.rc`.
- A run that has not finished in 1 h of wall time is stopped and what finished is reported. Memory is reported, never a stop condition.
- A failed check is a result. Thresholds are not changed after seeing data.

## Added after the first run

2026-11-23, steps 2 and 3. Nothing below changes a criterion, a threshold or a control target.
- PL.D.1 has 11 cases (3 even pass, 6 even fail, 1 odd pass, 1 odd fail), not 10 as the row said before; the script has the 11.
- First pilot run (`step2_pilot_L6_stopped_in_kdescending.log`, stopped by me after 3 min 21 s): the classifier compared the factor of
  the denominators with the symbolic L while the run had L = 6, so the O1 solution was called "NOT allowed" although its denominators were r^2 and
  (2r+3M)^2. The attempt `k-descending` (D^2 E columns first) ran over 2 minutes without a result, which O1 needs 1.3 s for.
  The classifier now takes the L of the solve (`classify_den(..., Lp)`). The first run is kept as that log. The search procedure beyond O1 was not
  needed in either run (O1 passed), so the question whether `k-descending` finishes is open and unimportant here.
- The solver returned zero coefficients for pivot columns solved to 0; they are now left out of the listing (cosmetic, `step2_odd` was rerun for it).
- `--part=even` also runs the planted checks and builds the odd equations (the script runs them before the even part); `--part=planted` stops after PL.D.1.
- Controls `flow_target` and `odd_den` run with `--attempts=1`: every equation has coefficients polynomial in s and these targets have 1/s, so no
  s-free certificate exists and the further attempts cannot pass.

Step 2 and 3 results are in `step2_odd.log`, `step2_pilot_L6.log` and `step3_even.log` (exit codes in the `.rc` files, wall seconds in `.time`, peak rss in `.rss`).
The certificates are in `cert_L6.json` and `cert_Lsym.json`.

Written after step 3 and before any control run: the certificate found with the column order O1 uses the equations traceless, tr, tt, rr and
trace (k = 0 for all, k = 1 for tt and rr) and not tx or rx. Predictions for the exploratory `drop_*` family, from that and not from a run of
the dropped variants: `drop_tx` and `drop_rx` exit 0 (not needed). For `drop_tt`, `drop_tr`, `drop_rr`, `drop_trace` I do not know which equation
another certificate can replace; each is accepted as exit 0 (not needed), or exit 1 at E.cert, or exit 1 at E.den; any other first FAIL is reported as unexpected.
The required controls are the 17 rows of the table above; the exploratory ones are reported separately and do not count toward them.
Controls runner: `zerilli_certificate_controls.py` (baseline `--part=all` unmutated, then `--mutate=NAME --failfast` with the args the table lists:
`--part=planted` for `leg_sign` and `den_allow_M`, `--part=odd` for the odd rows, `--part=even` for the even rows).

2026-11-23, step 4, written after control part 1 and before part 2.
- Part 1 (`controls_part1.log`, per-run logs in `controls_part1_logs/`, runner started with the whole list): baseline exit 0 with 16 PASS; 16 of the 17 required pairs
  exit as listed with the first FAIL at the pre-registered target. The 12th pair, `drop_traceless` at symbolic L, had not finished after 13 min 59 s
  (rss 157 MB, no output); I stopped that one run by its PID, so it is logged as `exit -15 ... MISS`. This is not a result about the control: the elimination
  for an inconsistent system in four variables was slow (`v_coef` 89 s, `psi_coef` 264 s, `drop_traceless` > 839 s). The batch went on. After `s0_s1` I stopped
  the batch (the exploratory family had just started at symbolic L, where the same slowness is expected); the runner printed no closing summary.
- The runner `zerilli_certificate_controls.py` got options `--only`, `--no-baseline`, `--extra`, `--cap` after part 1 started (the running process had already read the file).
- Part 2: `drop_traceless` and the six `drop_*` of the exploratory family at `--L=6` (the pilot's substitution, L = 6 before the solve, so 3 variables), cap 900 s per run.
  The target of `drop_traceless` is unchanged (E.cert, exit 1); the exploratory acceptance rule is unchanged (exit 0, or exit 1 at E.cert or E.den); a run past the cap is reported as stopped.
  A result at L = 6 is a statement at L = 6: no solution at L = 6 does not by itself show there is none at symbolic L, and a solution at L = 6 does not show one at symbolic L.
- Part 3 (after the final run): `drop_traceless` at symbolic L alone, cap 3000 s.

2026-11-23, step 4, written after control part 2 and before any further run.
- **Correction of the part-1 bullet.** I wrote that `drop_traceless` at symbolic L was slow because the inconsistent elimination swelled. That is wrong. Its stopped log
  (`controls_part1_logs/drop_traceless.log`) shows the attempts: O1 found a solution in 4.5 s, reversed-within-k in 1.4 s, both with "denominators NOT allowed", and `k-descending`
  took 451 s, also NOT allowed; I stopped the run in the search over the remaining column orders, not in a solve. So without the traceless equation **E.cert passes and E.den fails**.
  The pre-registered target of `drop_traceless` (E.cert, "with confidence") was wrong: it is a MISS. Reason (a reading, to be checked by the run below): the x-component of the
  linearized Bianchi identity gives the traceless equation from the other equations with a division by L − 2.
- **Part 2** (`controls_part2.log`, at `--L=6`, cap 900 s): `drop_traceless` exit 0 (certificate exists, denominators allowed: L − 2 is the number 4 at L = 6, so E.den cannot see it);
  `drop_tt`, `drop_tr`, `drop_rr`, `drop_tx`, `drop_rx` exit 0 (not needed at L = 6; for `drop_tt` the O1 solution had a forbidden denominator and the second column order passed);
  `drop_trace` exit 1 at E.1: **name collision**. `drop_trace` is also a mutation of #143's library (it drops the first-order part of a Ricci term), so `--mutate=drop_trace`
  switched on that one, not mine. Not a result about the trace equation. The equation drop for trace is renamed `dropeq_trace`; the other names stay.
- **New pre-registered controls** (written before they are run; added to the runner):
  `drop_second` = the three second-order equations tt, rr and trace removed from the span, `--L=6`: target E.cert, exit 1, with confidence: the first-order equations
  traceless, tr, tx, rx leave a 3-dimensional solution space (K, H1, H) on which Z does not vanish (Z is a multiple of the algebraic relation A of #143 E.2 on the flow), so Z is not in their span at any L.
  `drop_traceless` with `--attempts=2`, symbolic L: the pre-registered target E.cert stays and will be reported as a MISS if E.den fires; the expectation after part 1 is: exit 1, first FAIL E.den,
  with a forbidden denominator factor L − 2. The final control run is a single complete run of the runner on the final code, so that the controls output is one coherent file;
  its exploratory family (drop_tt, drop_tr, drop_rr, drop_tx, drop_rx, dropeq_trace) runs at `--L=6`, acceptance rule as before.

