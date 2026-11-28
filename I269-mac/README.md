# I269-mac: the exact nonlinear family behind the black universes' Y = R e^{K(t+x)}, its checks, mutations and development logs

Machine: the coordinator's Mac (Apple M5, macOS, shared with other agents), `~/Source/negative-mass/.venv/bin/python` (sympy 1.14.0, mpmath 1.3.0), `nice -n 10`, one thread per
process, at most two processes. Code: `notes/black_universe/exact_mode.py` in worktree `~/Source/negative-mass-i269`, branch `wip/i269-exact-solution` on main 3ba8819.
Issue: https://github.com/nmoinvaz/negative-mass/issues/269 (depends on #262). Written 2026-11-27 before the runs of record. Every development log is in `dev/` (scripts
`nl*.py`, `chk212.py`, logs `*_run<N>.txt|log`; the script's development runs are `dev_base_*` and `devmut_*`).

## Question

#262: Y = R e^{K(t+x)}, K = −2c/π, solves #212's linear radial problem exactly for every member c (b = 1, A = 1 + cR² + K(ρ + R² arctan ρ), R² = 1 + ρ²,
φ = √2 arctan ρ, the BF06 potential), and is checked in the static gauge (`I262-mac-review/ind262c.py`). Why does a closed form exist for every member? Is it the
linearization of an exact nonlinear family (candidate: a time-dependent throat radius b(v))? If so, what is its fate?

## What development found, in the order it happened (this is not a search over the declared classes)

Candidate classes of the brief: (a) a symmetry of the field equations acting on the family; (b) an exact nonlinear time-dependent family, linearized about each member;
(c) an intertwiner of the radial operator. Class (b) was tried first, with one ansatz, and held. (a) and (c) were not pursued after that.

1. `nl1` (log `nl1_run1.txt`): a brute-force Ricci tensor for ds² = −F dv² + 2G dv dρ + r² dΩ² (ingoing null chart, φ = √2 arctan ρ as the radial coordinate), with the
   convention of `ind262c.py` (R_ab = ε φ_a φ_b + V g_ab, ε = −1, ε□φ = V′). The static member (F = A, G = 1, r = R) solves the five equations to 1e-165 at c = −3/10, −1, 30 digits.
2. `nl2`: the ansatz r = λ(v) R(ρ), G = 1, F = A + f(v, ρ). The ρρ equation vanishes for every λ (r_ρρ = ½φ′²r is homogeneous of degree 1 in r). The scalar equation gives f_ρ = −2λ′/λ,
   the vρ equation holds with it, the θθ equation then gives f = −2ρλ′/λ + 1/λ² − 1. (Printed in `nl2_run1.txt`; the derivation by hand is in the note.)
3. `nl3`: with that F, four of the five equations vanish for an arbitrary λ(v). The fifth is E_vv = 2(−2cλλ′ − πλλ″ − πλ′²)/(π(1 + ρ²)λ²), that is
   proportional to (λλ′)′ − Kλλ′ with K = −2c/π. Its ρ dependence is the overall factor 1/(1 + ρ²).
4. `nl4`: with c and the coefficient Ks of ρ + R² arctan ρ independent (no asymptotic flatness; potential linear in (c, Ks)) the same: E_vv ∝ Ks λλ′ − λλ″ − λ′². The rate is Ks, not −2c/π.
5. `nl5`: λ² = L + β e^{Kv}: all five residuals are 0 for symbolic c, L, β.
6. `chk212`: Y = R at W = 0 is not a solution of #212's operator (residual 1.414 at c = −1, ρ = 1; 0.303 at c = −3/10). The static family L ≠ 1 of step 5 (β = 0) is a solution of the field equations;
   #212's equation at W = 0 does not describe it because the tρ equation it was derived from is empty there.
7. `nl6`: R2 = −F_ρρ of the 2D metric is independent of v and β; Kretschmann at β < 0 grows like 1/λ⁴ (K λ⁴ = 8.54 at c = −1, ρ = 1/2); at β > 0 it tends to a limit (2.587 at ρ = 1/2).
8. `exact_mode.py` was written after items 1–7 (the same equations, the checks below, the mutations). Its development runs: `dev_base_derive_run1` / `dev_base_check_run1` (7 of 7, 7 of 7),
   `devmut_<name>_{derive,check}_run1` for the 11 mutations, then S6 and the info line of N4 were added, and `dev_base_*_run2` (8 of 8, 7 of 7), `devmut_*_run2` (all 11 mutations) give the fired
   sets declared below. Nothing in the checks of record has been run before this README.

## Declared before the runs of record

### Acceptance (issue #269), and the checks that decide each

| acceptance | checks |
|---|---|
| a candidate whose linearization equals Y_K in the static gauge, symbolically (or in #232's double-null solver to 1e-6) | S5 (symbolic: #212's operator annihilates the first-order δr = (β/2) R e^{K(t+x)}), S3 (all orders in β, hence the first), N2 (the gauge image of the first order, brute-force linearized equations in the static gauge, 50 digits). The double-null solver is not used (the issue's alternative). |
| a perturbed candidate (one coefficient changed) fails | the mutations `kf`, `kh`, `rate`, `shape` (one coefficient or ingredient each) fire S3, N1, N2 and others (table below); `kappa`, `naive`, `pot`, `eps` are further perturbations |
| an exact nonlinear solution: residuals vanish symbolically; its fate stated with its status word | S1–S3, S6 (symbolic), N1 (50 digits); fate: N4 (β < 0), N5 (β > 0) |

### The candidate

In the ingoing null chart (v, ρ) with φ = √2 arctan ρ unchanged, G = g_{vρ} = 1, g_{ρρ} = 0:
r = λ(v) R(ρ), F = A − k_f ρ λ′/λ + k_h (1/λ² − 1), k_f = 2, k_h = 1, λ² = L + β e^{rate·v}, rate = K = −2c/π; ds² = −F dv² + 2 dv dρ + r² dΩ². The mutations change one entry.

### Checks (S: sympy, symbolic for symbolic c; N: mpmath at 50 digits; a check fails when its residual is nonzero symbolically or above its bar)

| id | what | bar |
|---|---|---|
| S0 | the static member solves the five equations in the null chart (convention and potential: planted truth) | symbolic zero |
| S1 | arbitrary λ(v): E_ρρ, E_vρ, E_θθ and the scalar equation vanish identically | symbolic zero |
| S2 | arbitrary λ(v): E_vv = 2(K λλ′ − λλ″ − λ′²)/((1 + ρ²)λ²) | symbolic equality |
| S3 | λ² = L + β e^{Kv}: all five residuals vanish for symbolic c, L, β | symbolic zero |
| S4a | K = (R²A′ − 2ρA)/2 + ρ, equal to −2c/π | symbolic equality |
| S4b | with c and Ks independent: S1's four vanish and E_vv has Ks in place of K | symbolic |
| S5 | #212's operator Y″ − PY′ − QY annihilates R e^{Wx} at W = the rate | symbolic zero |
| S6 | the hand-reduced equations (the by-hand derivation) at arbitrary λ(v) give S1's four zeros and S2's E_vv | symbolic |
| N0 | hand-reduced equations against the brute-force Ricci residuals on a generic non-solution metric | 1e-30 (residual scale > 1e-3) |
| N1 | the exact family, hand-reduced equations, c = −1, −3/10, −3/2, −10, 1/2, L = 1, 3/2, β of both signs, λ² from 0.3 to 3.0, 4 values of ρ | 1e-30 relative |
| N2 | static gauge, brute-force linearized equations at Y = R Q T, H2 = 2D Q T/A, H0 = T(−2DQ/A + 4WΞ), D = k_f Wρ/2 + k_h, Ξ free; c = −1, −3/10, −3/2, −10, 8 points, Ξ = 0, 3/7 | 1e-25 relative to the sum of the terms |
| N3 | the Kretschmann routine on Schwarzschild: 48M²/r⁶ (planted truth) | 1e-40 |
| N4 | β = −7/10: K_Kretschmann λ⁴ converges (1e-3, from λ² = 1e-6 to 1e-8) to a positive limit, and K > 1e12 at λ² = 1e-8, at c = −1, −3/2, −10; ρ = −2, 1/2, 3 | as stated |
| N5 | β = 7/10: Kretschmann changes by < 1e-5 from λ² = 1e6 to 1e12, F < 0 there (c < 0), d ln r/dv = K/2 to 1e-10; c = −1, −3/2, −10, −3/10; ρ = −2, 1/2, 3 | as stated |
| N6 | the static family β = 0, L = 3/2, 1/3, 5 (r = √L R, F = A + 1/L − 1): five residuals at 5 members | 1e-30 relative |

Information lines, not checks: #212's operator on Y = R at W = 0 (N6); F and the Kretschmann invariant on the line ρ = −1/K at β < 0 (N4).

### Mutations: each with the checks it must fire (development runs of record in `dev/`, `devmut_*_run2`)

| name | what it changes | fires |
|---|---|---|
| `kf` | k_f = 2 → 2.02 | S1 S2 S3 S4b S6 N1 N2 |
| `kh` | k_h = 1 → 1.01 | S1 S2 S3 S4b S6 N1 N2 N6 |
| `rate` | rate = K → 1.001 K | S3 S5 N1 N2 |
| `kappa` | rate = surface gravity κ(c) = A′(ρ_h)/2 (numeric checks; same as K at c = −1) | N1 N2 |
| `shape` | r = λρ in place of λR | S1 S2 S3 S4b S5 S6 N1 N2 N4 N6 |
| `naive` | k_f = k_h = 0: b → b(v) with F = A unchanged | S1 S2 S3 S4b S6 N1 N2 N4 N5 N6 |
| `pot` | V → −V | S0 S1 S2 S3 S4b S6 N1 N2 N6 |
| `eps` | ε = +1 (canonical scalar) | S0 S1 S3 S4b S6 N1 N6 |
| `charge` | the charge without its + ρ | S4a |
| `hand_drop` | drops (F′/2) r_ρ from H_vρ in the hand-reduced equations | S6 N0 N1 N6 |
| `kret_drop` | the same term in the Kretschmann routine | N3 |

Two facts about the table, from the development runs: `eps` does not fire N2 (the static-gauge first-order equations do not contain ε, since δφ = 0), and `kret_drop` fires only the planted N3 (N4, N5 do not
depend on that term at their bars). The runs of record must reproduce each fired set exactly.

### Status words

S0–S6 *checked symbolically*; N0–N6 at 50 digits *numerical evidence* (N1, N2, N6 repeat symbolic identities S3, S5 numerically with an independent evaluator, and N0 ties the hand-reduced equations to the brute-force tensor);
the by-hand derivation in the note is *proved* given the reduced equations (S6, N0). The fate statements: a divergence of the Ricci scalar at β < 0 is *proved* from the closed form; the Kretschmann
limits are *numerical evidence*. No sentence says a result is new.

### Not claimed

- That the family describes the nonlinear fate of asymptotically flat data: for β ≠ 0 it is not asymptotically flat (F − A grows like ρ at fixed v), and its linearization is #262's Y_ref, not the decaying Y_∞ = Y_ref − Y_b/I₀.
- Anything about Y_b, or about the double-null solver of #232 (not run).
- The causal structure beyond what N4 and N5 compute.

## Runs of record

2026-11-27, script `notes/black_universe/exact_mode.py` at branch commit e0c1c44 (unchanged since the declaration), `runs/runrec.sh` (logs are numbered, none overwritten).

| run | log | result | exit |
|---|---|---|---|
| `derive` | `runs/derive_run1.log` | S0 S1 S2 S3 S4a S4b S5 S6: 8 of 8 pass, 7 s | 0 |
| `check` | `runs/check_run1.log` | N0 – N6: 7 of 7 pass, 6 s | 0 |
| 11 mutations, each `derive` + `check` | `runs/m_<name>_{derive,check}_run1.log`, concatenated in `runs/m_<name>.log` | the fired sets equal the declared ones, 11 of 11 (`exact_mode.py mutations runs m_`) | 1 (a failed check exits 1, as intended) |

Worst residuals in the run of record: N0 2.41e-51, N1 2.81e-49, N2 1.23e-50, N6 3.34e-49; N3 exact. No amendment to the criteria.
`exact_mode_output.txt` in the repository is `derive_run1.log`, `check_run1.log` and the `mutations` report, in that order.
