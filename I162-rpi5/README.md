# I162-rpi5: logs of notes/warp/bessel_closure.py (closure fails on every open set for the Bessel shift family)

Machine rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process, one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/162. Branch `wip/i162-bessel-closure`, worktree
`~/Source/negative-mass-i162` (main c7a7882). Python `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0,
mpmath 1.3.0). Written 2026-11-24, before the first run of record. Stop condition: a single run not finished after 1 h of
wall time is stopped and reported. Memory is reported, never a stop condition.

## Question

#80 (`det_classify.md` section 3): u = c x + g(rho) has D = det R3 = 0 with g'' + g'/rho = eps (g'^2 + 2 c^2) exactly where
g' != 0; the solutions are g = -eps ln(alpha J0(sqrt2 c rho) + beta Y0(sqrt2 c rho)) + d. There R = a a - b b with
a = (g' d rho + 2 c th1)/sqrt2, b = W nu/sqrt2, W = sqrt(g'^2 + 2 c^2), th0 = dt, th1 = dx + u dt, th2 = d rho,
nu = th0 + eps th1. Closure failed at 6 exact jets (c, g') = (2, 1), (6, 17), (0, 1/2) only. Does it fail on every open set
for every member with c != 0? For c = 0 the family is #65's b(rho), where nu ^ d nu = b' dx ^ d rho ^ dt is the Frobenius
argument.

## What was explored before this README (not of record)

Hand derivations and four scratch scripts in the scratchpad (kept here as `scratch_explore1.py` ... `scratch_explore5.py`
with their stdout, `scratch_proto1.py`; no run of record), then a first scratch run of the draft script in the scratchpad
(`scratch_draft_baseline.log`, and one run of each control, `scratch_draft_ctl_*.log`), made to compute what each control
does before declaring it. The draft script is the script of record unchanged unless an amendment below says so. They gave:

1. By hand: R(xi, xi) = k(xi) m(xi) with k = a + b, m = a - b, so k and m are fixed by R up to k -> lam k, m -> m/lam and
   a swap (unique factorization of a quadratic form). Closure (some chi with e^chi k and e^-chi m closed, #65 stage 2)
   gives dk = -d chi ^ k and dm = d chi ^ m, so k ^ dk = 0 and m ^ dm = 0 (necessary, not sufficient).
2. By hand: d th0 = 0, d th1 = c th1 ^ th0 + g' th2 ^ th0, d th2 = 0. For k~ = alpha th0 + beta th1 + gamma th2 with alpha,
   beta, gamma functions of rho: k~ ^ dk~ = (beta alpha' - alpha beta' + g' beta^2 - c beta gamma) th0 ^ th1 ^ th2.
   For k~ = sqrt2 (a + b) (alpha = W, beta = 2c + eps W, gamma = g') and m~ = sqrt2 (a - b) (alpha = -W, beta = 2c - eps W):
   O_k = 2 c W' + g'(2c + eps W)(c + eps W), O_m = -2 c W' + g'(2c - eps W)(c - eps W). With W W' = g' g'' and the ODE:
   O_k = g'(g'^2 + 4c^2 + 5 c eps W - 2 c g'/(rho W)), O_m = g'(g'^2 + 4c^2 - 5 c eps W + 2 c g'/(rho W)).
   The W' terms cancel in the sum: O_k + O_m = 2 g'(g'^2 + 4 c^2), with no ODE.
3. Scratch sympy (`scratch_explore1.py`, `_explore5.py`): coordinate k ^ dk equals these forms; at 8 exact jets
   (including (c, g', rho) = (-2, 1, 4/39) with O_k = 0 and (2, 1, 4/39) with O_m = 0, eps = +1) `two_scalars.closure`
   returns 'no chi' exactly where (O_k, O_m) != (0, 0) and 'omega closed' (pointwise, so not decisive) at g' = 0.
4. Scratch sympy (`scratch_explore3.py`, `scratch_proto1.py`): O_k = 0 with g' != 0 means H = 0, H = (W/g') O_k (a function
   of (G = g', r = 1/rho)); the flow is (G, r)' = (eps W^2 - G r, -r^2). Eliminating r through H = 0 in L_V H gives
   N(G, c) = -(G^2 + 2 c^2) P(G, c) for k and m and eps = +-1, P = G^12 - 21 c^2 G^10 - 78 c^4 G^8 + 720 c^6 G^6 +
   5936 c^8 G^4 + 13056 c^10 G^2 + 8704 c^12 (monic), whose real roots at c = 1 are G = +-2.9388, +-4.7402. So a member
   can touch {O_k = 0} or {O_m = 0} only at isolated values of G.
5. Scratch sympy (`scratch_explore4.py`): the four planted pairs below behave as predicted; for u = c x + d the pair
   (c th1, c th0) has O = 0 and `two_scalars.closure` returns 'omega = d chi needed but d omega != 0' with
   omega = (-c(c x + d), -c, 0, 0), (d omega)_tx = c^2.

Everything below was fixed after this exploration and is not changed after the first run of record, except by a dated
amendment written before the run it concerns.

## Notation and imports

Coordinates (t, x, rho, phi). G = g', W = sqrt(G^2 + 2 c^2), r = 1/rho. k~ = sqrt2 k, m~ = sqrt2 m (scaling does not matter to
closure). O is the coefficient of dt ^ dx ^ d rho in k~ ^ dk~ (the d phi components vanish, asserted in the code).
Imported, read-only: `two_scalars.closure` and `two_scalars.dform` (the closure test and the exterior derivative of #65,
reviewed in #79; so the `points`, `planted` and `planar` checks are not independent of #65's closure code, and the checks that
call only `O_of` are independent of it). Own code: the Ricci tensor, the coframe, the ODE reduction, the Frobenius
coefficient. Not imported: `det_classify`, `phantom_source`. Output of the script is stdout only; each run is logged in this
folder, reruns are numbered.

## Checks (each is a `check(name, ok, detail)`; the script exits 1 if any fails)

**C1 `frame`.** (a) For symbolic g(rho), c, with the ODE substituted for g'' and g''' (eps = +1 and -1): the 4 x 4 matrix
R_{mu nu} (own Ricci code, metric -dt^2 + (dx + u dt)^2 + d rho^2 + rho^2 d phi^2, u = c x + g) minus
[(sqrt2 a)(sqrt2 a)^T/2 - (g'^2 + 2c^2)/2 nu nu^T], nu = th0 + eps th1, simplifies to 0 in every entry. (b) For both
eps, the squares of the three 2 x 2 minors of the matrix with rows (0, 2c, g') and (1, eps, 0) sum to 2 (g'^2 + 2c^2), which
is positive for c != 0 (then a ^ b != 0).

**C2 `frobenius`.** For eps = +-1 and for k~, m~ built from the symbolic g: (a) with no ODE, the coordinate coefficient O of
k~ ^ dk~ minus (beta alpha' - alpha beta' + g' beta^2 - c beta gamma), alpha = s W, beta = 2c + s eps W, gamma = g', s = +1 for
k~ and -1 for m~, simplifies to 0; (b) with the ODE substituted, O minus g'(g'^2 + 4c^2 + s(5 c eps W - 2 c g' (1/rho)/W))
simplifies to 0.

**C3 `sum`.** (a) For eps = +-1, with no ODE, O_k + O_m - 2 g'(g'^2 + 4 c^2) simplifies to 0. (b) The discriminant of
G^2 + 4c^2 in G is -16 c^2. (c) The real roots of G (G^2 + 4 c0^2) are [0] for c0 in {1/2, -3, 7}.

**C4 `isolated`.** (a) For eps = +-1 and c in {1/2, -3, 7, 1}: g'' from the ODE at g' = 0 equals 2 eps c^2, which is nonzero.
(b) Planted: g = 1 (a constant) satisfies the ODE residual g'' + g'/rho - eps (g'^2 + 2c^2) = 0 at c = 0 for both eps, and
does not at c in {1/2, -3}.

**C5 `each`.** For eps = +-1 and both k~ (s = +1), m~ (s = -1): (a) H := (G^2 + 4c^2) W + s (5 c eps (G^2 + 2c^2) - 2 c G r)
equals (W/G) O_closed(G, W, r) modulo W^2 - (G^2 + 2c^2) (exact polynomial remainder); (b) with G' = eps W^2 - G r, r' = -r^2,
W' = G G'/W, solve H = 0 for r, substitute in L_V H, take the numerator, split by parity in W as p0 + p1 W with W^2 = G^2 + 2c^2
and N = p0^2 - p1^2 (G^2 + 2c^2); then N = -(G^2 + 2c^2) P(G, c), P as printed in item 4 of the exploration, in all four cases,
and P is monic of degree 12 in G (so N is not the zero polynomial); (c) numerically at (G, c) = (3/2, 1) with 60 digits the
numerator before the parity split equals p0 + p1 W to within 1e-40 (a polynomial identity evaluated in sympy at 60 digits;
the rounding error is about 1e-58, so the threshold can be met). The real roots of P at c = 1 are printed as an observation
(not a criterion).

**C6 `points`.** At the ten jets (c, G, rho0) = (2, 1, 5/7), (6, 17, 5/7), (0, 1/2, 5/7) [#80's], (-2, 1, 4/39), (2, 1, 4/39),
(1, 1, 5/7), (3, 7/2, 2/3), (-6, 7, 3/11), (1, 0, 5/7), (-3, 0, 1/2), both eps (20 points), at x0 = 1/3, t0 = 1/10: (a) the
coordinate O_k, O_m, with the ODE substituted and the jet put in, equal the closed forms exactly; (b) with a, b the pair of
C1, `two_scalars.closure` returns not-ok with a reason starting 'no chi' at exactly those points where (O_k, O_m) != (0, 0)
(at the four jets with G = 0 it returns ok, pointwise and not decisive, since the equation d omega = 0 is evaluated at one
point; the criterion only requires that it does not report 'no chi' there).

**C7 `bessel`.** Five members (c, eps) = (1/2, +1), (3/2, -1), (-2, +1), (1, -1), (5/2, +1) with psi = alpha J0(sqrt2 |c| rho) +
beta Y0(sqrt2 |c| rho), alpha = n/3, beta = -m/5 from `random.seed(162)`, n in 1..9 and m in 1..9, g = -eps ln psi, no ODE
substituted anywhere: the coordinate O_k, O_m from the explicit expression, evaluated by mpmath at 80 digits at x0 in
{1/3, -5/7} and rho in {3/7, 5/7, 9/7, 13/7, 17/7, 23/7} (points with |psi| < 1/1000 skipped), against the closed forms with
the numerical g', W: (a) max difference < 1e-50; (b) max |O_k + O_m - 2 g'(g'^2 + 4c^2)| < 1e-50; (c) at least 40 points are
tested. Threshold: the quantities are of order 1 to 1e3, mpmath evaluates J0, Y0 and their derivatives by series/asymptotics to
full working precision (no quadrature), so the expected error is about 1e-70, far under 1e-50. Observation (not a criterion):
the numbers of sign changes of g', O_k, O_m on a grid of 260 points in 0.3 < rho < 8.95.

**C8 `planted`.** Through the same functions (`O_of`, `two_scalars.closure`): P1 the closed pair (a, b) = (d rho, dt): O = (0, 0),
closure ok, omega = 0. P2 k = e^-chi d(t + x), m = e^chi d(t - x + rho^2/2), chi = c x + g(rho) symbolic, a = (k + m)/2,
b = (k - m)/2: O = (0, 0), closure ok, omega = d chi = (0, c, g', 0). P3 (a, b) = (dt, x d rho): O_k = 1, O_m = -1 and closure
returns not-ok with 'no chi'. P4 k = dt, m = (1 + t rho) d rho: O = (0, 0) and closure returns not-ok with reason starting
'omega = d chi needed' (the Frobenius test is blind to it). Pass iff all four.

**C9 `c0`.** At c = 0 (u = g(rho), W = sgn(g') g' for sgn = +-1), for eps = +-1: O_k = O_m = g'^3 for both sgn; and for
nu = (1 + eps g) dt + eps dx, the coefficient of (d rho + nu) ^ d(d rho + nu) and of (d rho - nu) ^ d(d rho - nu) is g'
(#65: nu_+- ^ d nu_+- = b' dx ^ d rho ^ dt).

**C10 `planar`.** For u = c x + d (g' = 0, outside the ODE, the planar case of #80): (a) R = c^2 (th1 th1 - th0 th0) exactly
(own Ricci); (b) with a = c th1, b = c th0: O_k = O_m = 0, `two_scalars.closure` returns not-ok with a reason starting
'omega = d chi needed', and (d omega)_{tx} = c^2.

## Controls (`--mutate=NAME`; target in advance; each must exit non-zero with the target check failing)

The target of each control was named when the mutation was written (the `MUTATIONS` table of the script) and then checked in a
scratch run of the draft script (`scratch_draft_ctl_*.log`, one run per control, one process, nice 10) before this README was
committed: **each of the 13 exited 1 with exactly its target check failing and the other nine checks passing** (column
"scratch"). The scratch baseline `scratch_draft_baseline.log` exited 0 with 10 checks passed in 101 s.

| name | change | target | scratch |
|---|---|---|---|
| `frame-nu` | nu = th0 - eps th1 in b | `frame` | fired, 100 s |
| `frob-struct` | drops the c th1 ^ th0 term of d th1 (the term c beta gamma) in the coframe formula | `frobenius` | fired, 100 s |
| `frob-ode` | reduces on the ODE with -eps in place of eps | `frobenius` | fired, 100 s |
| `sum-factor` | expects 2 g'(g'^2 + 2c^2) | `sum` | fired, 99 s |
| `isolated-c0` | samples the step g'' = 2 eps c^2 at c = 0 | `isolated` | fired, 100 s |
| `each-w2` | W^2 = G^2 + c^2 in the elimination | `each` | fired, 100 s |
| `each-friction` | drops -G r in G' of the Lie derivative | `each` | fired, 100 s |
| `points-closed` | replaces (a, b) at every jet by the closed pair (d rho, dt) | `points` | fired, 64 s |
| `bessel-freq` | J0(c rho), Y0(c rho) in place of J0(sqrt2 c rho), Y0(sqrt2 c rho) | `bessel` | fired, 86 s |
| `plant-pass` | the boosted planted m multiplied by the non-integrable (dt - dx + x d rho) | `planted` | fired, 101 s |
| `plant-fail` | (dt, x d rho) replaced by the closed (dt, rho d rho) | `planted` | fired, 100 s |
| `c0-sign` | expects -g'^3 | `c0` | fired, 100 s |
| `planar-closed` | (c th1, c th0) replaced by the closed (c dx, c dt) | `planar` | fired, 100 s |

Extras (other checks failing under a control) are reported, not hidden. A control that crashes or hangs before its target
runs is reported as silent. The controls that make the obstruction vanish are `points-closed` and `planar-closed` (a closed
pair has O = 0 and closure ok).

## Logs

`run_*` logs are stdout of the script; `ctl_*` logs one control each. Failed, stopped and silent runs are kept and numbered.

## Plan for the runs of record

`run_final.run1.log`: `python3 notes/warp/bessel_closure.py --no-controls` (checks only, expected about 2 min, exit 0 if all
ten pass). Then `run_final.run2.log`: the full run with `--logdir=final_mut` (the checks, then each control as a subprocess;
about 25 min); the final `notes/warp/bessel_closure_output.txt` is the stdout of that full run. Peak memory from
`/usr/bin/time -v`. Each as a systemd user unit `nm-i162-<step>` with the exit code in a `.rc` file.

## Runs of record

Script of record: commit ba9a31d of `wip/i162-bessel-closure` (`notes/warp/bessel_closure.py`, sha256 c770c0fb...; identical to the
draft that ran in scratch). Note and output: 115fc31.

| log | command | exit | wall | peak RSS | result |
|---|---|---|---|---|---|
| `run_final.run1.log` | `bessel_closure.py --no-controls` | 0 | 100 s | 71 MB | 10 of 10 checks pass |
| `run_final.run2.log` | `bessel_closure.py --logdir=final_mut` (checks, then 13 controls) | 0 | 22 min 43 s | 72 MB | 10 of 10 pass; 13 of 13 controls FIRED on target only |

`final_mut/mut_<name>.log` is each control's own stdout. `notes/warp/bessel_closure_output.txt` is `run_final.run2.log`. Both runs
were one process, nice 10, as systemd user units `nm-i162-run1` and `nm-i162-run2`; the `.time` files hold `/usr/bin/time -v`.

Results against the criteria above: nothing failed, no control was silent or off target, no threshold was touched. Largest
residuals: `bessel` 1.77e-74 and 4.03e-76 at 80 digits (thresholds 1e-50). Observations printed (not criteria): the real roots of P at
c = 1, and the sign-change counts along the five members. The four jets with g' = 0 return 'omega closed' from
`two_scalars.closure` (pointwise, not decisive); the criterion only required that it not report 'no chi' there.

Disagreement with the issue text, reported: the issue asks for an expression "nonzero on the ODE for all (c != 0, g', rho, eps)".
O_k + O_m = 2 g'(g'^2 + 4 c^2) is nonzero for all g' != 0 but vanishes at g' = 0, where g'' = 2 eps c^2 makes the zeros isolated
on every member; each of O_k, O_m alone also vanishes on a hypersurface of the jets (exact jet (-2, 1, 4/39, +1) has O_k = 0).

The scratch exploration scripts were run twice: once interactively (output seen, not saved), once more to save the `scratch_*.log`
files here, with unchanged code.

## Amendments

(none)
