# I184-rpi5: the conical regime F ~ ln ln η, its expansion about q = −p², and whether any member reaches a limit

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with a choptuik-large-d runner). Worktree
`~/Source/negative-mass-i184`, branch `wip/i184-conical-loglog` (from main 011199e). Issue:
https://github.com/nmoinvaz/negative-mass/issues/184. One process at a time, nice 10, `RAYON_NUM_THREADS=2`,
`cargo build -j 2`. Rust 1.100.0; crates `multishoot =4.2.0`, `multisolver =0.2.2`, `multidouble =5.1.0` (as #167).
Python 3.14.10 (`~/Source/negative-mass-venv314`), sympy 1.14.0, mpmath 1.3.0.

This README is written before the first run of anything in this folder. It states the route, the quantities, the
criteria with their bars, the planted cases with the outcome I predict for each, and the names of the controls. The
targets of the controls are declared by an amendment after their development runs (step 4 of the brief). Amendments are
appended at the end, dated and numbered. No amendment changes a criterion, a grid, a precision, a bar or a step setting
after a run has shown data without asking the coordinator first.

## Question

#167 found that every solution of N = 0 that crosses η = 0 regularly and reaches η = 200 is in the regime

    p = ηF′ ≈ 1/(ln η + t₀),  q = η²F″ + ηF′ ≈ −p²,  F ≈ ln(ln η + t₀) + g₀,

the exact solution of the ν⁰ part A₀ = p²(p² − q)(p² + q) = 0 (ν = 1/η). It has no limit. #159/#168 cover only solutions
with a limit. Three things are asked:

1. the expansion about this solution with the ν² corrections of A₁ and A₂, as a formal series, and what it is;
2. its basin: which of #167's forward-grid solutions approach it, and how closely at stated η;
3. whether any member reaches a limit F_∞ at very large η, by a Taylor walk to η = 10¹² (a crossover to #159's family
   needs |p| ≈ 4F_∞/η²), and what precision the walk needs to see one.

## Quantities

t = ln η, σ = ν² = η⁻², G = F, p = θG, q = θ²G (θ = η d/dη = d/dt), F′ = pν, F″ = (q − p)ν². N = A₀ + σA₁ + σ²A₂ with
A₀, A₁, A₂ as printed in `conical_limit.md` §1. N(−G, −p, −q) = N, so a member with p < 0 is mirrored to p > 0. The
flow is G′ = p, p′ = q, σ′ = −2σ (′ = d/dt). With w = q + p²: A₀ = p²w(2p² − w), ∂A₀/∂q at q = −p² is 2p⁴.

- **Root series** Q_K(G, p, σ) = −p² + Σ_{k=1..K} σ^k e_k(G, p): the branch of the cubic N = 0 in q through q = −p² at
  σ = 0, solved order by order. By hand A₁(G, p, −p²) = p⁶(G − 1)², so e₁ = −p²(G − 1)²/2 (this is checked, not
  assumed). The e_k are Laurent polynomials in p with polynomial coefficients in G, and the series converges for small
  |σ| at fixed (G, p) (a simple root of a polynomial). It is **checked symbolically** and is the answer to item 1.
- **Invariants** T = 1/p − t and g = G + ln p. At σ = 0 they are the two constants (t₀, g₀) of the exact solution,
  p = 1/(t + T), G = ln(t + T) + g. Along the flow T′ = −w/p² and g′ = w/p exactly, with w = q + p² = Σσ^k e_k, so the
  corrections to the exact solution are exponentially small in t and T, g tend to limits T_∞, g_∞.
- **Residual of the series** ρ_K(η) = |q − Q_K(G, p, η⁻²)| / p², with (G, p, q) taken from the walk. ρ₀ = |q + p²|/p².
- **n_rel** = |N| / Σ|terms of N| at a state (as #167).
- **Verdict at η_end = 10¹²** for a member walked from η = 0 (mirrored to p > 0): `LIMIT` if |G(10¹²) − G(10⁶)| ≤ 1e-3
  and |p(10¹²)| ≤ 1e-6; `LOGLOG` if ρ₀(10¹²) ≤ 1e-10 and p > 0 and it is not `LIMIT`; otherwise `OTHER`.

## Route

1. **Formal series** (sympy, `conical_loglog.py`): θ-form, root series to K = 6, the identities for T and g, the same
   generator applied to a planted equation with a known σ-shift.
2. **Walker** (crate additions in `notes/warp/conical_global/src/hp.rs`, new subcommands, #167's modes unchanged): the
   implicit Taylor recursion of #167 written once over multidouble's `Precision` (double-, quad-, octo-double), with
   - every constant a lane-precision constant: 1/(k + 1), the shifted coefficients of N about the step's x₀ (formed in
     the lane's scalar from the exact integers and the f64 x₀), the division by ∂N/∂F″; no double-double constant enters
     a quad-double lane;
   - exact h = x_new − x₀ and Horner's rule in the lane;
   - a step planner with the last-two-terms rule of multishoot but relative to each field's own magnitude (the absolute
     rule of #167 lets the step exceed the radius of convergence once |F′| falls below the tolerance; see the planted
     case P5);
   - two modes: `conserve` (as #167: order 0 of N is not imposed, so N is constant along the flow and the rounding
     of each step stays in it) and `project` (one Newton correction of F″ at each step's start so that N = 0 holds to
     the lane's rounding of the current scale);
   - checkpoints at chosen η (steps are cut to land on them) and a per-step trace.
   multidouble's `Relaxed` is not used: its squares start at step e > 2 `BLOCK_MIN` (QV 64, OV 16, `qv.rs:1002`,
   `ov.rs:682`), so at the quad-double order used here it is bitwise `cs_range`. This is to be confirmed by one probe and
   stated in the note.
3. **Basin and approach**: #167's forward grid (below) from η = 0 to 10¹² in double-double (production) and quad-double
   (reference); the 15 `LOGLOG` members get ρ_K, T and g at the checkpoints.
4. **Controls**: each check gets a `--mutate=NAME`.
5. **Run of record**: `conical_loglog.py` stdout to `notes/warp/conical_loglog_output.txt`.

### The precision a walk needs to see a crossover

A crossover to #159's family means p falls from about 1/ln η to about 4F_∞/η² (the family has p = 4F_∞σ + …).
In `conserve` mode N is a constant of the flow. The data and the first steps leave N = ε ≈ u S₀ (u the unit roundoff of the
lane, S₀ = Σ|terms of N| at the start, the scale of the log-log state); N has no term below degree 6 in (p, q), so on the
family's side the scale is S ≈ (p_c/p₀)⁶ S₀ and the walk follows N = 0 there only if u ≪ (p_c/p₀)⁶, p_c ≈ 4F_∞σ_c. With
p₀ ≈ 0.05 and F_∞ = 1:

| crossover at η_c | needed u ≪ | double-double (1e-32) | quad-double (1e-64) | octo-double (1e-127) |
|---|---|---|---|---|
| 10³ | 3e-25 | yes | yes | yes |
| 10⁵ | 3e-49 | no | yes | yes |
| 10⁶ | 3e-61 | no | yes, 3 digits to spare | yes |
| 10⁹ | 3e-97 | no | no | yes |
| 10¹² | 3e-133 | no | no | no |

(The entries are (4σ_c/0.05)⁶ at F_∞ = 1, to be recomputed in the output.) So a `conserve` walk cannot see a crossover at 10¹²
at any lane precision; the `project` mode, which restores N = 0 to the lane's rounding of the current scale at each step,
needs only the relative accuracy of (G, p), a few digits more than the 24 that separate p ≈ 0.04 from 4σ at 10¹². The
table is a prediction. P5 tests the mechanism on a planted equation, where the scale collapses by a known factor.
The production walks are `project`; DD and QD runs of the real members in both modes are compared and reported.

## Grid, checkpoints, precisions (fixed before the first run)

- Forward grid (#167's): F(0) ∈ {0.1, 0.25, 0.5, 0.75, 1.5, 2, 3, 5, −0.5, −2}, F′(0) ∈ ±{0.01, 0.1, 1, 10, 100},
  F″(0) = −F′(0)²/F(0). 100 solutions. The minus side of (f, f₁) is the plus side of (f, −f₁) (N(F₀, −F₁, F₂; −η) = N),
  so walking the plus side of all 100 covers all 200 walks of #167; P-parity checks it on three pairs.
- Checkpoints η ∈ {200, 10³, 10⁴, 10⁶, 10⁹, 10¹²}.
- double-double (DD): order 30, tolerance 1e-32. quad-double (QD): order 60, tolerance 1e-64. Both relative to each
  field's magnitude; largest step unbounded (the step is set by the radius).
- Basin map beyond the grid (reported, not gating): F(0) in 40 values in [0.1, 5] and F′(0) in ±40 values in
  [0.01, 100] (log-spaced), walked to 200 in DD.

## Criteria (each can fail; each is coded as worded)

| id | criterion | tool |
|---|---|---|
| S1 `theta_form` | with F = G, F′ = pν, F″ = (q − p)ν², η = 1/ν, `det_classify.conical_N()` equals A₀ + ν²A₁ + ν⁴A₂ exactly (sympy `expand`), with A₀, A₁, A₂ typed here from `conical_limit.md` §1; and the crate's N at 40 rational points equals `conical_N()` to 1e-26 relative (#167's `n_table`, rerun) | sympy, crate |
| S2 `root_series` | e₁ … e₆ solved from N(G, p, −p² + w, σ) order by order in σ; the exact residual N(G, p, Q₆, σ) has no term of order σ⁰ … σ⁶ (each `expand`ed coefficient is 0); e₁ = −p²(G − 1)²/2; the table of the lowest and highest power of p and the degree in G of each e_k is printed | sympy |
| S3 `shift_series` | the same generator on the planted equation of P3 (a known σ-shift) returns e₁ = −2c(1 − p), e₂ = −c², e₃ = e₄ = 0, exactly | sympy |
| S4 `invariants` | with G′ = p, p′ = q: T′ = −(q + p²)/p², g′ = (q + p²)/p, exactly; at q = −p² both vanish; p = 1/(t + T), G = ln(t + T) + g solves G′ = p, p′ = −p² | sympy |
| W0 `regress` | on the 100 forward-grid points walked to +200, the new DD `conserve` walker (order 30, tolerance 1e-32, relative planner) and #167's walker give the same class (LOGLOG, SINGULAR kind, as #167's `forward` prints) and, for the LOGLOG ones, F, F′, F″ at 200 agree to 1e-24 relative | crate, #167's crate |
| W1 `basin` | the DD `project` walk of every grid point to 10¹² (or to its singular η*, located as in #167 to 1e-8): the LOGLOG set equals #167's 15 plus-side members; every other point ends as #167 recorded (class and kind; η* to 1e-8 where it has one) | crate |
| W2 `approach` | for each of the 15: ρ₄(η) ≤ 1e-10 at η = 10³, 10⁶ and 10¹² (DD walk, state read as the sum of parts and evaluated in mpmath at 60 digits). The table of ρ₀ … ρ₆ at 200, 10³, 10⁶, 10¹² is printed (200 and the lower K are not gating) | crate, mpmath |
| W3 `no_limit` | the verdict of each of the 15 at 10¹² is LOGLOG (none LIMIT); G(10¹²) − G(10⁶) = ln((t₂ + T₁)/(t₁ + T₁)) to 1e-8 with T₁ = 1/p − t at 10⁶ (t₁ = ln 10⁶, t₂ = ln 10¹²) | crate, mpmath |
| W4 `invariants_conv` | for each of the 15: \|T(η) − T(10¹²)\| ≤ 1e-8 and \|g(η) − g(10¹²)\| ≤ 1e-8 at η = 10⁶ and 10⁹ (the exponentially small corrections); T_∞, g_∞ printed | crate, mpmath |
| W5 `n_floor` | max n_rel at the step ends of each walk after the first step: DD `project` ≤ 1e-26, QD `project` ≤ 1e-54; the `conserve` values are printed | crate |
| W6 `dd_qd` | for each of the 15 at each checkpoint: DD and QD agree in G, p and q to 1e-26 relative | crate |
| W7 `independent` | own mpmath integration (30 digits, `odefun`) of G′ = p, p′ = Q₆(G, p, σ) in t, started at η = 10³ from the QD state, against the QD walk at 10⁶, 10⁹, 10¹² for (F(0), F′(0)) ∈ {(2, 1), (5, 100), (−2, −10)}: G and p to 1e-12 relative. Shared with the crate: N (typed from `conical_limit.md`), the start state. Not shared: the Taylor recursion, F″ by implicit recursion, the walker | mpmath |
| W8 `recip_check` | QD, member (2, 1) from η = 0 to 10⁶: the change of the final (G, p) when every step is halved is ≤ 1e-55 with lane-precision constants; with the double-double constants (control `recip-dd`) it exceeds 1e-45 (the model is choptuik-large-d's `hp/recip_check.py`, bar and control as there) | crate |
| W9 `parity` | for (f, f₁) ∈ {(2, 1), (3, 10), (5, 100)}: the walk of (f, f₁) to −200 equals the walk of (f, −f₁) to +200 in F and ηF′ (sign) to 1e-24 | crate |
| P1 `plant_167` | #167's planted cases through the rebuilt crate: `plant linear`, `plant cubic` (C⁻, C⁺, e to 1e-20, nodes to 1e-22) and `plant blowup` (η* to 1e-8) | crate |
| P2 `plant_loglog` | N_pl2 = η²F″ + ηF′ + η²F′² (q + p² = 0), start η = 2 with T = 13/10, g = 7/10: exact p = 1/(t + T), G = ln(t + T) + g. DD `project` and `conserve` walks to 10¹²: relative error of F, F′, F″ at every checkpoint ≤ 1e-26; QD ≤ 1e-55. The same verdict code returns LOGLOG | crate |
| P3 `plant_shift` | N_pl3 = p²w′(2p² − w′) with w′ = q + p² + 2cσ(1 − p) + c²σ², c = 1/3, written as a polynomial in (F′, F″, η) (multiplied by η⁸). Exact p = 1/(t + T) + cσ, G = g + ln(t + T) − cσ/2 + …; the exact F′ and F″ are the derivatives. DD `project` walk from η = 2 to 10¹²: p and q to 1e-25 relative at the checkpoints, and (p − 1/(t + T))/(cσ) = 1 to 1e-3 at 10⁶ | crate |
| P4 `plant_limit` | the planted linear equation of P1 to 10¹²: F → α + (a + bη)/(1 + η²) to 1e-24 relative at the checkpoints and the verdict code returns LIMIT | crate |
| P5 `plant_scale` | N_pl5 = η⁶F′⁴F″ + 4η⁵F′⁵ (= p⁴(q + 3p); solutions F′ = cη⁻⁴, so p falls as η⁻³), exact solution c = 1, start η₀ = 10 (F′ = 1e-4, F = 7/10 + the integral), walk to η = 3000: p falls by 2.7e7, the scale of N (about p⁵) by 7e-38. In `conserve` mode N = ε ≈ u S₀ stays, so q + 3p = ε/p⁴ and the relative error of p grows like u (p₀/p)⁵: 1e5 for DD, 1e-27 for QD. **Predicted**: DD `conserve` fails (relative error of p at the end ≥ 1e-3), QD `conserve` passes (≤ 1e-20), DD `project` passes (≤ 1e-24), QD `project` passes (≤ 1e-50). The check passes when the four outcomes are as predicted | crate |

Not gating, printed: the 40 × 80 basin map; the table above recomputed; the DD/QD cost per walk; the peak memory.

## Controls (`conical_loglog.py --mutate=NAME` must exit non-zero with its named checks failing)

Targets are declared by amendment after their development runs.

| name | change | intended check |
|---|---|---|
| `theta-coeff` | one coefficient of A₁ typed wrong | S1, S2 |
| `root-coef` | one coefficient of e₂ perturbed in the residual check | S2 |
| `shift-series` | the planted generator returns e₂ = −c²/2 | S3 |
| `inv-sign` | T′ = +w/p² | S4 |
| `class-sign` | the LOGLOG test uses q = +p² for p > 0 | W1 |
| `series-k` | the approach uses K = 1 | W2 |
| `walk-eq` | one coefficient of N in the hp walker changed | W2, W7 |
| `no-project` | `project` runs as `conserve` | P5 (DD project) |
| `recip-dd` | the QD lanes use double-double constants | W8 |
| `indep-q` | the independent integration uses Q₀ = −p² only | W7 |
| `plant-exact` | the exact solution of P2 has g + 0.001 | P2 |
| `plant-c` | the planted equation of P3 has c·(1 + 1e-6) | P3 |
| `limit-class` | the LIMIT test reads |p| ≥ 1e-6 | P4, P2 |

## Rules for the runs

Every stdout goes to a numbered log here (`dev_NN_*.log`, `run_NN.log`, `ctl_<name>.log` with `.rc`). No log is
overwritten; reruns are numbered. A run longer than 1 h of wall time is stopped by its PID and reported. Memory is only
reported. Nothing here is certified: every number is **numerical evidence** except where a line says **checked
symbolically**.

## Amendment A1 (2026-11-26, after the development runs `dev_01` to `dev_08`, before any run of record)

Each item says what the development runs showed. No bar was loosened; items that cannot run as worded are printed as
`NOT MET (as first worded)` and do not gate the exit code, as in #167.

1. **W0 as worded fails and stays NOT MET** (ruling of the coordinator, hc 2026-11-26). The new DD `conserve` walker and #167's
   walker differ at η = 200 by up to 5.2e-18 relative (bar 1e-24), at the members with F′(0) = 100. Cause (`dev_08`):
   both are N-conserving double-double walks; N's rounding from the first steps stays in N while the scale of N falls, so both
   are only good to about their own n_rel at 200 (3e-17 for (5, 100)). A QD walk with F′(0) perturbed by 1e-30 relative moves the
   state at 200 by 1e-31 (the forward map is well conditioned), and the DD `project` walk equals the QD one to 7e-32. This is the
   P5 mechanism, already at work in #167's forward walks, and it does not change #167's classes. W0 is printed
   `NOT MET (as first worded)` with this explanation and does not gate the exit code; no tolerance taken from the data's floor
   replaces it.
   **Added after the dev run `dev_08`, which showed W6's measured value 2e-29: W6 is the gating replacement.** Its bar 1e-26
   (DD `project` against QD `project` at 200, 10³, 10⁴, 10⁶, 10⁹, 10¹² for the 15 members, relative difference of G, p, q) was
   already in this README before the run; it is stated here as the gate of the DD walker's accuracy, fixed at 1e-26 now, set after
   seeing 2e-29. Its control is `no-project`: the member walks run as `conserve`, and DD `conserve` against QD `project` differs
   by 1e-18 at the members with F′(0) = 100 (`dev_08`), so W6 must fail.
2. **W1 is not changed.** The reference is #167's raw records: `negative-mass-raw/I167-mac/dev_09_forward.log` (the 100
   rows of `forward ... --rstop=1e-8` with η* and the bar of each side). A rerun of #167's crate on this machine must give the
   same class and kind and η* to 1e-8 (the sum of that bound and the two bars is printed beside it, as #167's parity check did).
   Points for which this cannot be met (the κ locus, where η* is known to 1e-6 only) are reported as not met, not compared at
   fewer digits. W1 also requires each of the 15 members to reach 10¹² with verdict LOGLOG (added: the verdict of a walk is part of
   "approach").
3. **W9 stays as worded and is printed NOT MET (as first worded)**, since the two walks of a pair cannot both reach ±200 unless the
   solution is global. **Replacement W9′ (added in this amendment, before any run of record):** (a) on every singular side, as #167
   did: for each of the 100 solutions the minus side of (f, f₁) and the plus side of (f, −f₁) have the same class and kind and η* equal
   to 1e-8 (the bars added are printed) in the rerun of #167's crate; (b) on the regular sides: for each of the 15 members (f, f₁)
   the walk of (f, −f₁) to −200 equals the walk of (f, f₁) to +200 in F, F′ (sign) and F″ to 1e-24 relative (DD `conserve`, both
   arithmetics mirrored, so the expected difference is 0).
4. **P4** gates F only, as worded. The dev run shows that `project` loses F′ and F″ there (1.1e-20 at 10¹²) because it slaves
   F″ to the cancellation in F − α, while `conserve` keeps 1e-31; both are printed.
5. **Basin map** (not gating) is 20 values of F(0) in [0.1, 5] times ±20 values of F′(0) in [0.01, 100] (800 walks to 200 in
   DD `conserve`), not 40 × 80: the map costs about 0.3 s per walk on this machine and the run of record must stay under
   1 h. Added: the boundary F′(0)*(F(0)) between the stopped walks and the walks that reach 200, by bisection at 8 values of F(0).
6. **Added controls** so that every gating check has one: `inv-conv` (T computed as 1/p + t) for W4; `parity-sign` (F′ summed
   with the wrong sign) for W9′(b). `no-project` also targets W5 and W6 (the member walks run as `conserve`), `walk-eq` also W2 and W7.
7. **The first unlogged runs** are in `dev_00_unlogged_first_runs.md` (the underflow of the Taylor coefficients at η ≥ 3e5, fixed by
   the power-of-two step variable before any logged run).
8. **Added after the dev runs `dev_06` to `dev_08` (the hand argument of Theorem 1 in the note), bars derived by hand, not from data.**
   `trap_bounds`: the four polynomial bounds |A₁| ≤ 26u²p⁶, |∂A₁/∂q| ≤ 30u²p⁴, |A₂| ≤ 15u³p⁴, |∂A₂/∂q| ≤ 35u³p³ for 0 < p ≤ 1/4,
   |w| ≤ p²/2, u = 1 + |G| hold at 4000 random states (ratio ≤ 1); at 300 random states of D = {p ≤ 1/4, σu³ ≤ p²/5} N changes sign
   across |w| ≤ p²/2 and is increasing there, the root obeys |w| ≤ 20σu²p², p′ = q lies in p²[−5/4, −3/4] and (ln r)′ < −3/5 with
   r = σu³/p². `trap_entry`: each of the 15 DD `project` walks, at every step, enters D (with |q/p² + sgn p| ≤ 1/2) at η_in ≤ 1e6 and
   stays in it with r non-increasing; 1e6 was fixed from an estimate before the run (r ≈ 6e-5 at 10⁶ for (5, 100)); measured η_in ≤ 1.27e4.
   Controls `trap-bound` (2.6 in place of 26) and `trap-eps` (ε = 1e-12).
9. **Two checks that crashed under a control now fail instead.** In `dev_09` the control `walk-eq` raised a `KeyError` in `independent`
   (the walk of the changed equation ends before η = 10³). `independent` and `approach` count a walk that does not reach 10¹² as a
   failure; `dev_10` is the rerun.
10. **A control silent on its named target (`dev_09`, `plant-exact`).** The mutation shifted g in the exact solution, which also builds
    the start state, and F does not enter q + p² = 0, so the walk reproduced the shifted solution and `plant_loglog` passed (exit 0).
    The mutation now shifts only the solution the walk is compared with (the start state keeps g = 7/10): `dev_10`, error 3.9e-4, fired.
    `limit-class` predicted P4 and P2; in `dev_09` it fired P4 only, because P2's G changes by 0.6 between 10⁶ and 10¹², so inverting the
    |p| test does not make it LIMIT: P2 is dropped from its targets.

## Amendment A2 (2026-11-26, control targets, after the development runs `dev_09` and `dev_10`)

Each control is `conical_loglog.py --mutate=NAME`; a control runs only the checks it names, so "no other check fails" holds by
construction, and the expected outcome is exit 1 with exactly the named checks `[FAIL]`.

| name | change | target checks | development result |
|---|---|---|---|
| `theta-coeff` | 4Gp⁴q → 5Gp⁴q in A₁ | `theta_form`, `root_series` | conical_N − (A₀ + ν²A₁ + ν⁴A₂) = −Gν²p⁴q; e₁ = −p²(G² − 3G + 1)/2 |
| `root-coef` | e₂ × (1 + 1/7) at one monomial of the residual | `root_series` | lowest order 2 |
| `shift-series` | expected e₂ = −c²/2 | `shift_series` | fired |
| `inv-sign` | T′ expected +w/p² | `invariants` | T′ identity False |
| `class-sign` | the LOGLOG test reads q = +p² at p > 0 | `basin`, `no_limit` | all 15 members OTHER |
| `inv-conv` | T = 1/p + t | `invariants_conv` | worst \|T(η) − T(10¹²)\| 28 |
| `parity-sign` | F′ summed with the wrong sign | `parity` | fired |
| `series-k` | K = 1 in place of 4 | `approach` | ρ₁ 2.1e-6 at 10³ (bar 1e-10) |
| `walk-eq` | −6 → −5 on FF′²F″η² in the walker | `approach`, `independent` | ρ₄ 4.0e-3 at 10³ (11 of 15 reach 10¹²); independent 2e-5 (a walk ends at η = 40.9) |
| `indep-q` | independent integration with Q₀ = −p² | `independent` | 5.5e-5 |
| `plant-exact` | comparison solution with g + 1e-3, start state unchanged | `plant_loglog` | 3.9e-4 (silent in `dev_09`: see A1 item 10) |
| `plant-c` | c = 1003/3000 in the planted equation | `plant_shift` | error 1.7e-4, ratio −1.3e7 |
| `limit-class` | LIMIT test reads \|p\| ≥ 1e-6 | `plant_limit` | verdict OTHER (does not fire `plant_loglog`: A1 item 10) |
| `no-project` | `project` runs as `conserve` | `plant_scale`, `n_floor`, `dd_qd` | n_rel 3.1e-17; DD against QD 4.1e-14; the DD project plant fails |
| `recip-dd` | constants rounded to double-double in QD | `recip_check` | 2.0e-33 (bar 1e-55; must exceed 1e-45: it does) |
| `trap-bound` | 2.6 u²p⁶ in place of 26 u²p⁶ | `trap_bounds` | worst ratio 1.25 |
| `trap-eps` | D with ε = 1e-12 | `trap_entry` | η_in from 4.5e8 to 6.2e9 |

W0 (`regress`) has no control: it does not gate (A1 item 1). The run of record is `python3 notes/warp/conical_loglog.py` from the repository
root, in the environment of the setup (venv314), stdout to `run_01.log` here and to `notes/warp/conical_loglog_output.txt`.
