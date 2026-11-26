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
