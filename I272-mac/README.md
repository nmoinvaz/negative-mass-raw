# I272-mac: the linear spectrum of the symmetric Ellis wormhole beyond its unstable mode, D = 5 and D = 4 (#272)

Machine: the coordinator's Mac (Apple M5), nice 10, at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/272
(branch `wip/i272-ellis-spectrum`, driver `notes/wormhole_evolution/ellis_spectrum.py`, note `ellis_spectrum.md`). Written before the runs of
record; the development runs (`dev/`) came first and are named where they set a bar.

## What is computed

The linear spherically symmetric perturbations of the symmetric Ellis wormhole (throat radius 1, n = D - 2), in #195's gauge delta phi = 0,
`h = diag(-e^{2nu}, e^{2lam})`, `r = r0 + eps Y(t, l)`. Four parts, one script, `python3 ellis_spectrum.py run [--only=planted,zero,spectrum,time] [--mutate=NAME]`.

1. **The time-dependent linear system** (`zero`). Re-derived in sympy without the factor e^{Wt}: E1tt, E1tl, E1ll, E2, S. With
   `L = Y'/r0' + g(l)` (from E1tl) and `N = L - nY/r0 + c(t)` (from S) the system reduces to `Y_tt = D Y - 2(n-1) g / r0`, with
   `D Y = Y'' - p Y' + q Y` (E2 of `master.py`), and E1tt, E1ll constrain only g. Tested as exact solutions of all five equations
   (n = 2, 3, sympy residual 0): the scale mode `Y1 = r0` (L = 1), its secular partner `t Y1`, the asymmetry mode `Y2 = r0 int r0'^2 r0^{n-2}`
   and `t Y2`, `t^2/2 Y1 + Y^(1)` with `D Y^(1) = Y1`, and the translation mode `r0^n r0'` (needs g != 0). `t` times the translation mode must fail.
   Asymptotics of `Y^(1)` (unbounded) and the order of the pole of the resolvent at W = 0 (log-derivative mismatch Delta(W), real small W).
2. **Poles of the resolvent**, i.e. the modes beyond the unstable one (`spectrum`), by two eigen-solvers that share only the equation:
   (a) shooting: Frobenius series at the throat, the outgoing solution integrated inward along a ray l = l_m + s e^{i theta} from far, zeros of the
   analytic Wronskian M(W) counted by the argument principle on boxes of the W-plane and polished by secant; (b) Chebyshev collocation of E2 on
   a complex-scaled contour (parity-reduced, Dirichlet at the ends), isolated eigenvalues taken as those present at three rotation angles.
3. **Time domain** (`time`): E2 as `Y_tt = D Y` on a staggered grid with parity at l = 0, RK4, the unstable mode projected out each step with its
   discrete left and right eigenvectors. Data: `sigma_0 = Y_t(0, l)` Gaussians (centers 3, 6, 1.5, widths 0.5, 1), `Y(0, l) = 0`. Observable `Y(t, 0)`, the throat radius
   perturbation. Series are the Richardson combination of h = 0.01 and 0.005 (second order, measured at h = 0.02, 0.01, 0.005).
4. **The comparison** with #255's kappa = 0.495 +- 0.01 (D = 5), 0.244 (D = 4), with #267's decay of the mass excess (0.649 to 0.669 per decade of delta,
   Delta tau = 0.975 x 2.00 per decade: rate 0.205 to 0.222 per proper time), and with #255's table of rdot_inf and E_net.

## Planted cases (same code path, answer known, before the real runs)

| case | known answer | solver |
|---|---|---|
| Poeschl-Teller `V0 sech^2(alpha l)`, V0 = 2.5, alpha = 1: W = -i omega, omega = +-sqrt(V0 - alpha^2/4) - i alpha (n + 1/2), n = 0, 1, 2 (even, odd, even) | exact | shooting, argument principle, collocation |
| unstable W^2 at D = 5, 4 | #195's crate (quad-double), `w2_crate w2 --lane=qd --D=5 --W2=2.985` and `--D=4 --W2=1.397` | shooting, collocation, the time-domain operator |
| `Y1 = r0` and `t Y1` | exact solutions | sympy residuals |
| `Y^(1)` asymptotics | `Z/l^3 -> 1/2` at D = 4, `(1/2) ln l` growth at D = 5 (variation of parameters at the resonance) | ODE |

## Criteria (declared; every one can fail)

Planted and checks of the machinery:

| check | claim | bar |
|---|---|---|
| PT1 | shooting finds the three Poeschl-Teller overtones | worst `|W - exact|` <= 1e-8 |
| PT2 | argument principle on boxes: windings 1 at the three roots, 0 in three empty boxes | `|w - want|` < 0.05 |
| PT3 | the collocation solver on Poeschl-Teller (N = 481, S = 24, theta = -1.2) | relative error of W^2 <= 1e-6 |
| W1-D5, W1-D4 | shooting reproduces #195's W^2 | relative 1e-8 |
| W2-D5, W2-D4 | collocation (theta = -0.7, N = 481) reproduces it (the second method) | relative 1e-4 |
| W3-D5, W3-D4 | the time-domain operator: error <= 3e-4 at h = 0.01 and second order | ratio of errors at h = 0.02, 0.01 in [3, 5] |

The linear system and the zero modes:

| check | claim | bar |
|---|---|---|
| Z1-n2, Z1-n3 | E2 reduces to `Y_tt = DY - 2(n-1) g/r0`; E1tt, E1ll at g = 0 | sympy difference exactly 0 |
| Z2-n2, Z2-n3 (eight candidates each) | `Y1`, `t Y1`, `Y2`, `t Y2`, `t^2/2 Y1 + Y^(1)`, the translation mode solve all five equations; `t` times the translation mode does not | residual exactly 0; for the last, some residual nonzero |
| Z3-n2, Z3-n3 | the generalized zero mode is unbounded: `Z/l^3` -> 1/2 (D = 4), slope 1/2 per e-fold over the last decade (D = 5) | 2 % (D = 4), 1 % (D = 5) |
| Z4-n2, Z4-n3 | `d ln|Delta| / d ln W` at W = 0.01 ... 0.08: simple pole at D = 4, double pole with a logarithm at D = 5 | bands [0.90, 1.20] and [1.55, 2.10] |

The spectrum:

| check | claim | bar |
|---|---|---|
| S1-D5, S1-D4 | the Re W > 0 boxes around the unstable root have winding 1, the neighbours 0 | 0.05 |
| S2-D{5,4}-{even,odd} | **no zero of M with Re W in [-1.4, -0.2] and Im W in [0, 1]**, the region of kappa = 0.495 and 0.244 | none found |
| S3-D{5,4}-{even,odd} | each zero found elsewhere in Re W in [-8.2, -0.2], Im W in [0, 8] is a zero: it moves by at most 1e-3 over four ray angles and two far points | 1e-3 |
| S4-D{5,4}-{even,odd} | collocation: the only eigenvalue of `|W^2| < 80` present at theta = -0.7, -0.85, -1.0 is the unstable one (even), none (odd) | counts |

The time domain and the comparison with #255, #267:

| check | claim | bar |
|---|---|---|
| T1-D5, T1-D4 | h = 0.02, 0.01, 0.005: observed order of `Y(t, 0)` at t = 10, 20 in [1.8, 2.3]; Richardson correction <= 1 % | |
| T2-D5 | k of #255's estimator `v = v_inf + c e^{-k(t - 6.5)}` on t in [6.5, 12] of the linear response against kappa = 0.495 | +-0.01 |
| T2-D4 | the same against kappa = 0.244 | +-0.024 |
| T2m-D4 | the late decay rate of the throat speed at t = 20 (mean over four data) against #267's 0.205 to 0.222 | +-10 % of the range |
| T3-D5, T3-D4 | the late decay rate at t = 20 does not depend on the data | spread <= 0.02 |
| T4-D5, T4-D4 | `Y(t, 0)/P` for two data far from the throat, `P = int w Y1 sigma_0 dl`, `w = 1/(r'^2 r^n)`, at t = 20 | 1 % |
| T5-D5 | the secular speed at D = 5 is constant: `d ln v / dt` at t = 15, 25 | <= 0.005 |
| T5-D4 | the D = 4 shift saturates: `Y(40)/Y(30) - 1` | <= 1 % |
| T7-D5, T7-D4 | the late throat speed is a power law: `-d ln v / d ln t` (= rate x t) at t = 15, 20, 25 constant, and positive | spread <= 12 % of the mean |
| T6 | `rdot_inf / E_net` of #255's table at B = 0.02 ... 0.1 is B independent (what a speed linear in the injected energy needs) | max/min <= 1.2 |

Predictions written before the runs of record, from the development runs `dev/dev_01` to `dev_04` (where the numbers were seen; raw logs there):
PT1 to PT3, W1 to W3, Z1 to Z4 (Z3-n3 after its window was set to the last decade), S1, S2, S4, S3 for the even sectors, T1, T3-D5, T4, T5-D4 and T7 **pass**;
**T2-D5, T2-D4, T2m-D4, T3-D4, T5-D5 and T6 fail**, and **S3 fails for the odd sectors** (a candidate zero near the cut that moves with the ray: D = 5, W = -6.78 + 0.47i, spread 0.18;
D = 4, W = -7.22 + 0.27i, spread 1.8e-2). A failing check is a result: it is reported and its bar is not moved. Two bars need a word: the issue gives no
tolerance for "against kappa" beyond #255's +-0.01, so T2-D4 takes 10 %; and S4's count is a statement about what complex scaling can expose
(modes with Omega/gamma above about 0.1 only, see the note), not about what exists. T7 was added after dev_03, when the D = 4 rates were seen to fall as 1/t.

## Mutations (`--mutate=NAME`; the effect was computed in a development run before it was declared)

| mutation | what it breaks | checks that fire in the development run (and only these) | dev log |
|---|---|---|---|
| `wrong_p` | n -> n + 1 in the Y' coefficient of E2, in the shooting solver, the collocation operator and the time-domain operator | W1-D5, W1-D4, W2-D5, W2-D4, W3-D5, W3-D4 (`--only=planted`; PT1 to PT3 pass) | `dev_05` |
| `pt_V` | V0 = 2.6 in the shooting solver's Poeschl-Teller | PT1 | `dev_06` |
| `ray_flip` | the sign of the ray's rotation (shooting and boxes) | PT1, PT2 | `dev_07` |
| `ecs_noscale` | theta = 0 in the collocation (no complex scaling) | PT3 | `dev_08` |
| `wrong_secular` | L = 0 in the candidate `t Y1` (not the solution of E1tl) | Z2-n2 `t Y1`, Z2-n3 `t Y1` (`--only=zero`) | `dev_09` |
| `pole_off` | Z4 taken with the odd throat solution | Z4-n2, Z4-n3 | `dev_010` |
| `no_projection` | the time domain without removing the unstable mode | T4-D4, T4-D5, T5-D4, T7-D4, T7-D5 (`--only=time`; T2-D4, T2-D5, T2m-D4, T5-D5 and T6 fail without it too, so the mutation cannot show them) | `dev_12` |

(`dev_011` is the first run of `no_projection`, before T7 got its sign test; `dev_12` is on the code of record. File names `dev_09`, `dev_010`, `dev_011` carry the
script's counter. The planted stage, the zero stage and the time stage were rerun on the final code: `dev_13` (20 of 20), `dev_06` to `dev_08` (planted under mutation: PT3 passes unmutated).)

## Things the issue did not specify and the choices made

- "The transient's rates" are read as the poles and the branch structure of the resolvent of E2: a pole at W = -gamma + i Omega is a quasinormal mode of rate gamma; the
  response to compact data also contains the cut along negative real W (the tail) and the pole at W = 0.
- "Bounded" in the issue's `Y` is read in the gauge's variable Y; the table of asymptotics in the note also gives the canonical variable `u = Y / (r' r^{n/2})`.
- E_net is second order in the amplitude, so no linear map from E_net to the data of the linear problem exists: T6 tests the consequence (a speed linear in E_net),
  and the secular coefficient per unit conjugate momentum `P` is reported (`v/P`), not compared with `rdot_inf/E_net`.
- Rates are computed for proper time t = tau (g_tt = -1 on the background).
