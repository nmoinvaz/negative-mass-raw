# I162-mac: the coordinator's review of #162's closure failure for the Bessel shift family

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2
processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/162. Reviewed branch `wip/i162-bessel-closure` at 115fc31 and
raw `I162-rpi5` at 4d09fb9.

## Rerun of the runner's script

`python3 bessel_closure.py` from `notes/warp/` of a detached worktree of 115fc31, full, with its 13 controls (`rerun/`).

## Independent check `ind162.py` (criteria written before its first run)

ind162 imports nothing from the repository: no `bessel_closure.py` and no `two_scalars.py`. Its Ricci routine is the
coordinator's, from `I77-mac` on. Its exterior calculus is its own: the coefficient of k ∧ dk on dt ∧ dx ∧ dρ, in
coordinates, from the components of k. So is its elimination for Theorem 2.

Shared with #162: the metric and the ODE g″ + g′/ρ = ε(g′² + 2c²); the printed a, b (θ¹ = dx + u dt, ν = θ⁰ + εθ¹,
W = √(g′² + 2c²)), k̃ = √2(a + b), m̃ = √2(a − b); the printed O_k, O_m, H_k and P; and the exact jets quoted below.

| id | criterion | kind |
|---|---|---|
| R0 | planted: the own Ricci routine finds Painlevé–Gullstrand Schwarzschild Ricci-flat | symbolic |
| R1 | for u = c x + g(ρ) with undefined g, ε = ±1: the own Ricci tensor, with g″ replaced by the ODE, equals a ⊗ a − b ⊗ b in coordinates | symbolic |
| R2 | the own coefficient of k̃ ∧ dk̃ and of m̃ ∧ dm̃ on dt ∧ dx ∧ dρ, on the ODE, equals the printed O_k = g′(g′² + 4c² + 5cεW − 2cg′/(ρW)) and O_m = g′(g′² + 4c² − 5cεW + 2cg′/(ρW)), for ε = ±1. Without the ODE, their sum is 2g′(g′² + 4c²). At g′ = 0 the ODE gives g″ = 2εc². Planted, through the same Frobenius code: dρ, dt and d(t + x) give 0, and dt + x dρ gives ±1 | symbolic |
| R3 | Theorem 2, own elimination for (k, ε) and (m, ε), ε = ±1. Take H = (W/G)O with G = g′, r = 1/ρ. H is linear in r; solve it for r. Substitute into the derivative along G′ = εW² − Gr, r′ = −r², W′ = GG′/W. Write the numerator as p₀ + p₁W with W² = G² + 2c². Then N = p₀² − p₁²(G² + 2c²) is a nonzero rational multiple of c^i G^j (G² + 2c²) P, with the printed P = G¹² − 21c²G¹⁰ − 78c⁴G⁸ + 720c⁶G⁶ + 5936c⁸G⁴ + 13056c¹⁰G² + 8704c¹², in all four cases | symbolic |
| R4 | re-solve at exact jets, from R2's own coefficients: (c, g′, ρ, ε) = (−2, 1, 4/39, +1) gives (O_k, O_m) = (0, 34); (2, 1, 4/39, +1) gives (34, 0). At #80's six jets, (c, g′) ∈ {(2, 1), (6, 17), (0, 1/2)}, ε = ±1, ρ = 5/7: (O_k, O_m) ≠ (0, 0), and at c = 0, O_k = O_m = g′³ | exact |

Mutations, each must exit 1 with its target failing:

| mutation | change | target |
|---|---|---|
| `pg` | √(2M)/r for √(2M/r) | R0 |
| `bsign` | ν = θ⁰ − εθ¹ in b | R1 |
| `frob` | the own Frobenius coefficient with the sign of its k_ρ term flipped | R2 |
| `poly` | 20c²G¹⁰ for 21c²G¹⁰ in P | R3 |
| `jet` | expected (O_k, O_m) = (0, 33) | R4 |

## Results

| file | what |
|---|---|
| `rerun/bessel_closure_full.*` | the rerun at 115fc31: stdout, `/usr/bin/time -l`, exit code |
| `ind162_run1.py`, `.txt`, `.time` | run 1 (`ind162.py` is the same version) |
| `ind162_mut_*.txt` | its 5 mutations |

**Rerun** (exit 0, 14 min, 80 MB peak): 10 of 10 checks pass and 13 of 13 controls fire on target only. The output
equals rpi5's apart from the timings.

**ind162 run 1** (exit 1, 3.5 s, 71 MB peak). R3 fails as worded; everything else passes.

| criterion | run 1 |
|---|---|
| R0 | Painlevé–Gullstrand Ricci-flat |
| R1 | the own Ricci tensor on the ODE equals a ⊗ a − b ⊗ b for ε = ±1 |
| R2 | the own Frobenius coefficients equal the printed O_k, O_m for ε = ±1; their sum is 2g′(g′² + 4c²) without the ODE; g″ = 2εc² at g′ = 0; planted dρ, dt, d(t + x) give 0 and dt + x dρ gives 1 |
| R3 | **fails as worded**: in all four cases N / ((G² + 2c²)P) = 1/(G² + 2c²), that is, **N = P exactly** |
| R4 | (−2, 1, 4/39, +1) → (0, 34), (2, 1, 4/39, +1) → (34, 0); #80's six jets all have (O_k, O_m) ≠ (0, 0), and (1/8, 1/8) = g′³ at c = 0 |

Re-solve: R4, the exact jets, and R3's elimination, by the coordinator's own code.

**R3's failure.** The criterion asked for N to be a monomial multiple of (G² + 2c²)P, as #162 prints N = −(G² + 2c²)P.
The coordinator's elimination gives N = P itself, the same monic degree-12 polynomial, without the factor G² + 2c².
That factor depends on how the denominators are cleared: sympy's `together` cancels it here. It is positive, so it
does not change Theorem 2. Theorem 2 needs only N ≢ 0 as a polynomial in G, and that holds. R3 stays failed: the
criterion fixed a factor that the computation does not reproduce.

| mutation | exit | failed | target met |
|---|---|---|---|
| `pg` | 1 | R0 (R3 at baseline) | yes |
| `bsign` | 1 | R1, R2, R4 (R3 at baseline) | yes |
| `frob` | 1 | R2, R4 (R3 at baseline) | yes |
| `poly` | 1 | R3, which fails at baseline; informative, because the quotient is no longer 1/(G² + 2c²) | yes |
| `jet` | 1 | R4 (R3 at baseline) | yes |
