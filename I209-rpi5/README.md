# I209-rpi5: logs of the independent re-derivation of the exchange identities E1, E2, E3 and the Clausen integrals

Machine: rpi5-ubuntu (4 cores, 8 GB, aarch64, Python 3.14 venv `negative-mass-venv314`, mpmath 1.3.0 with the pure-Python
backend, sympy 1.14.0). Issue: https://github.com/nmoinvaz/negative-mass/issues/209. Code: branch `wip/i209-exchange-review` of
negative-mass, script `notes/wormhole_largeD/exchange_review.py`. Runner: `negative-mass-rpi5-i209`, started by the
coordinator over hc.

## What is being checked

The statements are given by the task. They are re-derived from the order equations (order4.py's docstring, README.md
"Method") and the definitions, then each step is checked. R = r^s = sec² θ, l = ln R = −2ℓ, ℓ = ln cos θ, u = tan θ.

- **E1:** G_k = 4∫₀^{π/2}L_{k−1}dθ + 2∫Σ_{j=1}^{k−1}L_{k−1−j}l^j/j! dθ + 2∫(Σ_{j<k}Y_j c_{k−j} − Ω_{k−1})/sin²θ dθ.
- **E2:** ∫₀^{π/2}L_{k−1}dθ = 2∫h_{k−1} ln cos θ/sin²θ dθ, with every boundary term stated.
- **E3** (#208), at k = 5: Y₄ enters G₅ only through a term that integrates by parts against P = cot θ (ℓ − Ω₀) and leaves no
  Y₄; the boundary argument at j = 4.
- **Clausen:** with C = Cl₂(π − 2θ), ∫₀^{π/2} tan θ C dθ = π³/12 and ∫₀^{π/2} C² dθ = π⁵/360.
- **Third grid:** Ω₂ and Ω₃ on a method-B grid with N, w, V used by neither #26 (B1, B2) nor #208 (B3, B4).

## What the runner may and may not read

Independence is the point. Allowed: the issue, README.md "Method", `matched.py`, the top of `order4.py` (docstring, `cc`, `hk`,
`Fsum`, `PanelB`, `run_B`) and `order5.py` (docstring, `parse`, `cc`, `hk`, `Fsum`, `PanelK`, `omega_chain`, `run_B`, `GRIDS`,
`check_grid`, `main`), and the numbers in `order4_output.txt` and `order5_output.txt`. Not read until the comparison step:
`omega2.md`, `omega3.md`, the `reduce`, `reduce5`, `closed`, `n4b`, `n4bg` parts of `order4.py` and `order5.py`, and the raw folders
I26-dh610 and I208-dh610.

Disclosed: (1) a `grep` of the two output files for the grid names printed lines of the `reduce` parts (`H8`, `RD8`, `A5`: the
numbers G₃(0) = 130.98…, G₄(0) = 934.55…, G₅(0) = −8203.83…, and Ω₃'s closed form, which the task and README.md state anyway).
No derivation step was in those lines. (2) The docstring of `order4.py` (allowed) states, in its lines 13 to 17, the shape of
the reduction by hand (moments of ln cos, the Clausen integral ∫tan C = π³/12, the D3 function); it was read before the
derivations were written.

## Layout

- `run_logged.sh LOG CMD…`: runs CMD under `/usr/bin/time -v`, appends stdout and stderr to LOG, ends with `exit=<code>`.
- `dev_*`: development runs (never gate anything; kept, numbered, never overwritten).
- `run_*`: the declared runs, after the declarations below were committed.
- `ctl_*`: the control runs (`--mutate=NAME`).
- Systemd units are named `nm-i209-<name>`; the unit of each log is in the log's name or in `units.txt`.

## Declarations (before the declared runs)

### Grids

| name | N | w | V | dps | panels | used by | cost on rpi5 |
|---|---|---|---|---|---|---|---|
| E-grid | 36 | 1/2 | 16 | 80 | 32 | the E1, E2, E3 and boundary checks | 50 s (dev_exch_02.log) |
| third grid | 64 | 1/3 | 24 | 130 | 72 | Ω₂, Ω₃ against A70 and B4 | 96 s (dev_grid1_N64_w1-3_V24_dps130.log) |

The third grid's (N, w, V) = (64, 1/3, 24) is not one of B1 (40, 1/2, 18), B2 (50, 2/5, 20), B3 (80, 3/10, 28), B4 (90, 1/4, 30).
The development run on the third grid gave Ω₀, Ω₁, Ω₂ against the closed forms to 87.8, 87.3, 87.2 digits and the slopes of
G_k against −4π to 88.8 digits. Neither grid is moved after its development run.

### Checks and bars

A digit count is −log₁₀ of a relative difference between two evaluations. It is not an error bar.

| id | check | bar |
|---|---|---|
| S1 … S11 | sympy residual 0: the substitution, c₁/sin², P′, the Y_{k−1} coefficient, boundary limits, Beta moments, C′, sine-series integrals | residual 0 |
| P0b, P0c | K(u) against its definition; the table's h₁, h₂ against README's closed forms | 40 digits |
| P1 | E1 at k = 2 (Ω₀ = 3/10) against −4πΩ₀ − 16π ln 2, closed forms, no panel code | 40 digits |
| P2_1, P2_2 | E2 at m = 1, 2 from closed forms, no panel code | 40 digits |
| CM, CL1, CL1a, CL2 | the moments of ln cos, ∫tan C = π³/12, its by-parts step, ∫C² = π⁵/360, by mpmath quadrature at 60 digits | 40 digits |
| P0 | the E-grid's Y₁, L₁, Y₂, L₂ against README's closed forms at the nodes with l ≤ V²/4 | 1e-30 |
| E1_3, E1_4, E1_5 | G_k against E1's right side, Ω_{k−2} at its root (right side must be 0 to 1e-30 of its terms) and shifted by 1/2 | 30 digits |
| E2_2, E2_3, E2_4 | ∫L_m dθ against 2∫h_m ln cos/sin², Ω_{m−1} at the solved value, 0 and 1/2 | 30 digits |
| E3_3, E3_4, E3_5 | ∫Y_m[(ℓ − Ω₀)/sin² + 1]dθ = 2∫(ℓ − Ω₀)F_{m−1}dθ, m = k − 1 | 30 digits |
| E3G_3, E3G_4, E3G_5 | G_k from the hierarchy against the reduced form with no Y_{k−1} and no Y_k | 30 digits |
| BND | boundary terms at the first two and the last node: Y_k cot θ, ℓC_m, cot θ ℓ, Y₄P | throat end: b/θᵖ constant to 1 % and equal to the predicted leading coefficient where there is one; outer end: \|b\| < 1e-30 and b/(x lᵠ) bounded |
| GROW | growth of Y_k, L_k against powers of l at the last node | reported, no bar |
| GR1 | Ω₂ on the third grid against #26's A70 (`order4_output.txt`, 48 printed digits) | 40 digits |
| GR2 | Ω₃ on the third grid against #208's B4 (`order5_output.txt`, 113 printed digits) | 40 digits |
| GR3 | Ω₀, Ω₁ on the third grid against −4 ln 2 and 2π²/3 + 8 ln² 2 | 40 digits |
| GR4 | slope of G_k in Ω_{k−2}, k = 2 … 5, against −4π | 40 digits |

### Controls

Each control is a `--mutate=NAME` run of the part it names. The targets below were computed in development runs of every
control (`dev_ctl_*`, `dev2_ctl_*` for the ones added or changed afterwards, `dev3_ctl_cl_moment.log` after `digits()` was
fixed: it divided by a first moment that the control makes exactly 0), and are declared here and in `TARGETS` of the script,
before the declared runs. "Silent" lists the checks that the development run showed do not fire; a control that fires on one
of them, or misses a target, is reported off target. A control that is silent on a check is a result, not a defect.

| name | what it breaks | part | fires (target) | silent (declared) |
|---|---|---|---|---|
| sym_S1 | S1's constant 2 taken as 1 | sym | S1 | |
| sym_S2 | dl/dθ = 2 tan θ taken as tan θ | sym | S2 | |
| sym_c1 | c₁'s 3l/2 taken as l | sym | S3, S5 | |
| sym_P | the sign of P′ | sym | S4 | |
| sym_S6 | the antiderivative −cot θ ℓ + θ | sym | S6 | |
| sym_S7 | the limit of cot θ ℓ replaced by that of ℓ | sym | S7 | |
| sym_S8 | the sign of ∫ℓ | sym | S8 | S9 |
| sym_S9 | C′ = 2 ln(2 sin θ) | sym | S9 | |
| sym_S10 | I₂ = +π/2 | sym | S10 | |
| sym_S11 | Σ(π/2)/n² = π³/6 | sym | S11 | |
| exact_K | K = θ ln 2 − Cl₂(π − 2θ) | exact | P0b, P2_2 | P0c, P1, P2_1 |
| exact_L1 | the closed L₁ = −2Ω₀ − l | exact | P0c, P1, P2_1, P2_2 | P0b |
| exact_h2 | README's h₂ with a stray l/10 | exact | P0c | P1, P2_1, P2_2 |
| e1_sign | the sign of E1's Σ_{j≥1} term | exact, exch | P1, E1_3, E1_4, E1_5 | E2_*, E3G_* |
| e1_factor | E1's 4∫L_{k−1} taken as 2∫L_{k−1} | exact, exch | P1, E1_3, E1_4, E1_5 | E2_*, E3G_* |
| e2_weight | E2's weight ln cos replaced by ln cos + ln 2 | exact, exch | P2_1, P2_2, E2_2, E2_3, E2_4 | E1_*, E3G_* |
| bnd_G | Ω₀ + 1/100 on the E-grid, so G₂ ≠ 0 | exch | P0, BND | E1_*, E2_*, E3_*, E3G_* |
| bnd_Y0 | Y_k + 1e-3, so Y_k(0) ≠ 0 | exch | P0, BND, E1_*, E2_*, E3_*, E3G_* | |
| e3_Om0 | P without Ω₀ | exch | E3G_3, E3G_4, E3G_5 | E3_*, E1_*, E2_* |
| e3_factor | the by-parts coefficient 4 taken as 2 | exch | E3G_3, E3G_4, E3G_5 | E3_*, E1_*, E2_* |
| cl_moment | ln cos + ln 2 in the moments | clausen | CM | CL1, CL1a, CL2 |
| cl_arg | Cl₂(π − θ) in place of Cl₂(π − 2θ), as the task suggests | clausen | CL1, CL1a, CL2 | CM |
| cl_arg2 | Cl₂(2θ) in place of Cl₂(π − 2θ) | clausen | CL1, CL1a | CM, CL2 |
| grid_coarse | N = 10 on the third grid (`coarse_B` of order5.py) | grid | GR1 … GR4 | |
| grid_short | V = 6 on the third grid (`short_tail`) | grid | GR1 … GR4 | |
| grid_wrongh | the sign of −l/R in c₂ (`wrong_h`) | grid | GR1, GR2, GR3 | GR4 |
| grid_wrongOm1 | Ω₁ + 1/100 in the G₄ step (`wrong_Om1`) | grid | GR1, GR2 | GR3, GR4 |

Two of the silences are results. (1) `bnd_G` leaves E1 and E2 silent because `PanelK`'s L_m = −2Ω − u·(tail from the node to V)
has no growing term for any Ω₀: the hierarchy it builds is the decaying solution, which equals the throat-analytic one only if
G_m = 0. The shift shows where it should, at the throat, where the decaying solution's C_m(0) is −G_m, not 0. (2) `cl_arg2`
leaves ∫C² silent because the orthogonality of sin 2nθ does not see the sign (−1)^{n+1}.

## Logs

- `dev_grid1_*`: the development run of the third grid (96 s). `dev_sym_*`, `dev_exact_*`, `dev_clausen_*`, `dev_exch_*`: the
  development runs of the parts (the first `dev_sym` attempt ran in the foreground and was stopped by hand; its note is
  `dev_sym_00_note.txt`). `dev_grid_02.log`: the third grid through the script.
- `units.txt`: the systemd units.

## Runs of record

Code: `notes/wormhole_largeD/exchange_review.py` at negative-mass `886f764` (unchanged by the runs below; the note was edited
after them). All runs on rpi5-ubuntu, one process each, `nice -n 10`, as systemd units (`units.txt`).

| log | what | exit | wall | peak RSS |
|---|---|---|---|---|
| `run_01_sym_exact_clausen_exch_grid.log` | `sym exact clausen exch grid`: 39 of 39 pass | 0 | 203 s | 100.6 MB |
| `ctl_<name>.log` (27) | each control, `--mutate=NAME` | 1 each (a control fails its targets by design) | 2 s to 2.4 min | |
| `run_02_all_ctlsum.log` | the same parts and `ctlsum` over `ctl_*`: 66 of 66 pass, 27 of 27 controls on target; writes `exchange_review_output.txt` | 0 | 199 s | 100.8 MB |

No stop condition fired. Memory was reported only. The third grid took 98 s (inside `run_01`), well under the 1 h limit.

The comparison with `omega2.md` and `omega3.md` was made after `exchange_review.md` (with the derivations) and its output were
committed and pushed (negative-mass `a2e647e`, raw `1589421`). Its result is §8 of the note: no difference in a sign, constant or
result; differences in route and in what is stated.

