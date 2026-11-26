# I165-rpi5: prolongation of the static one-sign system with u_xρ ≠ 0 (logs, Singular files, certificates)

Machine rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process, one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/165. Branch `wip/i165-one-sign-static`, worktree
`~/Source/negative-mass-i165` (main 07ac2b1). Python `~/Source/negative-mass-venv314/bin/python` (3.14.10, sympy 1.14.0),
Singular 4.4.1 (`/usr/bin/Singular`, aarch64). Written 2026-11-25, after the development probes listed below and before
the first run of `notes/warp/one_sign_static.py`. Stop condition: a single run not finished after 1 h of wall time is
stopped and reported. Memory is logged (`/usr/bin/time -v`), never a stop condition.

## Question

#158 reduced the static one-sign class u(x, ρ) with u_xρ ≠ 0 to a rank-2 distribution X₁ = D_x, X₂ = D_ρ on the jets
(ρ, u, a, β, s) (a = u_x, β = u_ρ, s = tan(θ/2), v₀ = β cos θ, v₁ = β sin θ, v₂ = a/(u cos θ − sin θ)) with
[X₁, X₂] = C ∂_s. A solution is an integral surface, so it lies on C = 0, then on X₁C = X₂C = 0, and so on. Decide: empty
(certificate), a surviving set, or not finished.

## Reduction (stated before the runs of record)

1. **Scaling.** (x, ρ) → k(x, ρ), u → u maps solutions to solutions and acts on the jets by (ρ, a, β) → (kρ, a/k, β/k).
   The ideals of the chain are weighted homogeneous (weights ρ: 1, a, β: −1), so ρ = 1 loses nothing. The Euler term of
   X₂ f (a weight times f) lies in the ideal, so the chain needs no weight term. Coordinates: u, b = ρβ, v = ρ v₂, s.
2. **Fields at ρ = 1** (c = (1−s²)/(1+s²), σ = 2s/(1+s²), w = u c − σ, D = u(1−s²) − 2s = (1+s²) w; ρa = v w):
   Φ₁ = (b²c² + v² − v²w²)/u, Ψ = −2 b c v, Φ₃ + b = 2 b² c σ (ρ²u_xx, ρ²u_xρ, ρ²u_ρρ + b). σ̄ₓ, σ̄_ρ solve E₁ (a_xρ = a_ρx), E₂
   (β_xρ = β_ρx), as in #158's `static_system` but in 5D (ρ, u, a, β, s) first, then ρ = 1 and a = v w.
   X̄₁ = a ∂_u + Ψ ∂_b + (…) ∂_v + σ̄ₓ ∂_s, X̄₂ = b ∂_u + (Φ₃ + b) ∂_b + (…) ∂_v + σ̄_ρ ∂_s. The ∂_v components follow from a = v w.
   [X̄₁, X̄₂] = −X̄₁ + C̄ ∂_s, and C̄ = C at ρ = 1.
3. **Chain.** f₀ = C̄ with the nonvanishing factors removed; f₁ = X̄₁f₀, f₂ = X̄₂f₀, f₁₁ = X̄₁f₁, f₁₂ = X̄₂f₁ (numerators in
   lowest terms, nonvanishing factors removed, primitive, leading coefficient > 0). I_{k+1} = I_k + (X̄ᵢ f).
4. **Nonvanishing quantities** (the open set of the reduction, each justified in the note): u (u ≡ 0 on an open set is
   flat); b = ρβ (h > 0); v = ρ v₂ (Z ≠ 0, so v₀ v₂ ≠ 0); s²−1 (v₀ ≠ 0, that is u_xρ ≠ 0, given b v ≠ 0); s (Y, Q ≠ 0;
   s ≡ 0 is decided by hand in the note); s²+1; D (a ≠ 0, since ρa = v D/(1+s²)); Δ′ (the common factor of the denominators
   of σ̄ₓ and σ̄_ρ, 26 terms, degree 8 in s; list: σ̄ₓ: 8 s u Δ′, σ̄_ρ: 8 s u (1+s²) Δ′; Φ₁: u (1+s²)²; Ψ: 1+s²; the ∂_v components of X̄ᵢ: u, 1+s², D, Δ′).
   The branch where the surface lies inside Δ′ = 0 is NOT covered by this task (E₁, E₂ are then not solvable for σ).

## Development probes (before this README; logs in `dev/`)

| probe | what | result |
|---|---|---|
| 1 | 5D fraction field, C numerator | 734 terms = a · b · (s−1)(s+1)(s²+1) · N_C, N_C 656 terms, degree 39; Δ of degree 12 in s; 330 s |
| 2 | same at ρ = 1, coordinates (u, a, b, s) | same factors, N_C 656 terms, degree 37, 144 s |
| 3 | coordinates (u, b, v, s) | f₀ 319 terms, degrees (u,b,v,s) = (6,4,4,18), v even; 48 s |
| 4 | level 1, level 2 numerators | f₁ 1388, f₂ 1818, f₁₁ 3837, f₁₂ 4892, f₂₁ 4898, f₂₂ 5792 terms; 100 s |
| 5 | `std(f₀, f₁, f₂)` mod 32003, 4 variables, dp | not finished at 25:00 (exit 124, 1.9 GB) (`dev/p6.*`) |
| 6 | the same at fixed s = 7 (3 variables) | dim 1, mult 22 (plain); saturated by u v b D Δ′: dim 0, mult 194; with f₁₁ saturated: unit ideal |
| 7 | s as a parameter (F_p(s) coefficients), f₀ f₁ f₂ f₁₁, saturated | not finished at 20:00 (exit 124, 490 MB) (`dev/p11_A.*`) |
| 8 | block order (dp(4), dp(1)), full ring | started and stopped by me after < 1 min, no result |
| 9 | slice u = 3 (not s), liftstd | not finished at 10:00 (exit 124, 940 MB) |
| 10 | which subsets at s = 7 and s = 5, mod 32003 | f₀ f₁ f₂ + one of f₁₁, f₁₂ (alone) saturated by u, Δ′ already unit; subsets without f₁ or f₂ not |
| 11 | liftstd over ℚ at s = 7 | not finished at 15:00 (exit 124, 1.0 GB) |
| 12 | 60 lifts at s = 2..61 mod 32003 | supports of the cofactors are the same (≤ 3 terms differ), cofactor degrees 22, 17, 15, 11, 23; 3.5 s per lift; coefficient degree in s above 20 |
| 13 | liftstd at s = 2 mod 50 primes near 2³¹ (with the same generators, saturation u v b D Δ′), CRT, rational reconstruction | running at the time of this commit; 12 primes (112 digits) did not suffice for the reconstruction; result in the first amendment |

No criterion below was changed after seeing a failing check; the criteria were written after these probes, and the choice of
generators (f₀, f₁, f₂, f₁₁) and of the saturation factors was made from probes 6 and 10.

## Criteria (each is coded exactly as worded; each can fail)

All criteria are exact (sympy rational arithmetic) unless marked *modular*. Names are the script's check names.

| id | check | criterion |
|---|---|---|
| S1 | `blocks` | `one_sign_classify.static_blocks(u, a, β, Φ₁, Ψ, Φ₃, ρ)` equals `v_block(v₀, v₁, v₂)` identically in (ρ, u, a, β, s) (#158's block, Lemma R) |
| S2 | `AB` | A = Q(Z²+Y²) + 2hZY and B = PQY − Z(Q²+Y²) lie in the radical of Lemma R's ideal saturated by ZYQ (`one_sign_classify.rad_member`, Rabinowitsch) |
| S3 | `fields` | the u, b, v components of [X̄₁, X̄₂] + X̄₁ are 0 as rational functions of (u, b, v, s); its s component is C̄ |
| S4 | `Cpoints` | at 3 exact points (u, b, v, s) with s ∉ {0, ±1}, D Δ′ ≠ 0: C̄ equals #158's 5D formula C = D_ρσₓ − D_xσ_ρ evaluated through partial derivatives at the corresponding 5D point (a = v w), and C̄ ≠ 0 |
| S5 | `denoms` | σ̄ₓ and σ̄_ρ in lowest terms have the denominators of reduction item 4, with Δ′ the polynomial stored in `chain/delta.txt`; numer(C̄) = c · v · b · (s²−1) · D · f₀ with c ∈ ℚ, c ≠ 0 |
| P1 | `planted_s1` | for the family u = c x + C ln ρ + d (s = 1; also s = −1): (a) σ̄ₓ, σ̄_ρ are 0 at s = ±1 and u, 1+s², D, Δ′ are not 0 polynomials there, so every unsaturated chain numerator F_k lies in (s²−1); (b) F₀, F₁, F₂ (numerators before removing factors) vanish at s = ±1; (c) the same F₀, F₁, F₂ vanish at 5 exact jets of the explicit family; (d) the saturated f₀, f₁, f₂ do not vanish at s = 1 (saturation is what removes the family) |
| P2 | `toy` | toy system X₁ = ∂_p, X₂ = ∂_q + p(q²+1) ∂_r (C = q²+1, known inconsistent) through the same chain, Singular and verification code: stored certificate with Σ cᵢ fᵢ = κ ≠ 0 over ℚ; toy X₂ = ∂_q + q ∂_r (C = 0, flat) has an empty chain (survives) |
| C1 | `chain` | the generators f₀, f₁, f₂, f₁₁, f₁₂ recomputed in sympy have term counts 319, 1388, 1818, 3837, 4892, degrees (u,b,v,s) as in probe 4, v even, and SHA-256 equal to the stored `chain/chain.json` |
| D1 | `slice_cert` | for each stored slice certificate at s = s₀ ∈ ℚ: Σ cᵢ gᵢ = κ ≠ 0 exactly in ℚ[t, u, b, v], with g = (f₀, f₁, f₂, f₁₁)(s = s₀) from the recomputed chain and g₅ = 1 − t u v b D(s₀) Δ′(s₀). Meaning: at s = s₀ no complex point of f₀ = f₁ = f₂ = f₁₁ = 0 has u v b D Δ′ ≠ 0 |
| D2 | `full_cert` | only if it exists: Σ cᵢ gᵢ = κ ≠ 0 exactly in ℚ[t, u, b, v, s], g = (f₀, f₁, f₂, f₁₁, 1 − t · u v b s (s²−1)(s²+1) D Δ′). This is outcome 1. |

Outcome rule. Outcome 1 (empty, *certified*) iff D2 passes. Otherwise outcome 3, and the note states what each of D1, the modular
evidence, and the failed full-ring runs establishes, with the status words *certified* (D1, at the listed s₀ only),
*numerical evidence* (modular), *conjecture*. The surviving-set outcome 2 would need an exact point of a nonempty variety.
*Modular* statements carry the prime and are never called certified.

## Certificate format

`certs/slice_s<s0>.json`: `s0` (string fraction), `gens` (names), `primes` (the primes used), `cofactors`: for each of the 5
generators a list of [exponents (t, u, b, v), numerator, denominator], `kappa`. Verification expands Σ cᵢ gᵢ in a sympy
`ring` over ℚ and compares with κ (no Singular, no modular arithmetic). Cofactors come from `liftstd` mod several primes
near 2³¹ and CRT with rational reconstruction; only the exact identity counts. `chain/chain.json`: the generators as lists
of [exponents (u, b, v, s), numerator, denominator] and their SHA-256. `singular/`: every Singular input and output.
`logs/`: stdout of every run, numbered; a rerun gets a new number.

## Controls (`--mutate=NAME`; each must exit non-zero with exactly these checks failing)

| control | change | target checks |
|---|---|---|
| `Phi1-sign` | Φ₁ with the opposite sign of a² (#158's compat-Phi1) | `blocks`, `fields`, `chain` |
| `Psi-sign` | Ψ with the opposite sign | `blocks`, `fields`, `chain` |
| `AB-sign` | B built as PQY + Z(Q²+Y²) | `AB` |
| `denoms-claim` | claims the denominator 4 s u Δ′ in place of 8 s u Δ′ | `denoms` |
| `Cpoints-s1` | the three points drawn on s = 1, where C̄ = 0 | `Cpoints` |
| `plant-s2` | the planted test at s = 2 in place of s = 1 | `planted_s1` |
| `toy-flat` | the flat toy is passed to the rejection test | `toy` |
| `cert-corrupt` | one cofactor coefficient of the first stored slice certificate changed by 1 | `slice_cert` |
| `cert-satdrop` | the saturation generator verified with u dropped from P | `slice_cert` |

A control that exits 0, or whose failing checks differ from its target list, is reported as silent (or off target), and the
target list is never edited without a README amendment.

## Runs of record (filled in as they are done)

See the amendments and `logs/` below.

## Amendments (dated; the criteria above stay as first written, these say what the code tests)

**A1 (2026-11-25, after dev run 1 and the dev control batch, before any run of record).**
- S3 as coded: [X̄₁, X̄₂] + X̄₁ = C̄ (∂_s − (v w_s/w) ∂_v) as rational functions of (u, b, v, s). The criterion as first worded
  (u, b, v components vanish) was wrong: ∂_s at fixed (u, ρa, ρβ) is ∂_s − (v w_s/w) ∂_v in the coordinates (u, b, v, s), since
  v = ρa/w. Dev run 1 failed on it (`logs/dev_verify_1.log`). A bug in the check as worded, found before a run of record.
  The identity "[X̄₁, X̄₂] = −X̄₁ + C̄ ∂_s" of the Reduction (item 2) holds in the coordinates (u, ρa, ρβ, s).
- S4 as coded: C̄ = −ρ² C, where C = D_ρσ_x − D_xσ_ρ is #158's formula. #158 writes [X₁, X₂] = C ∂_s, but the s component of
  [X₁, X₂] is D_xσ_ρ − D_ρσ_x = −C. A sign discrepancy with #158's wording only; the zero sets agree. Dev run 1 failed on it.
- D1 as coded is **modular**: Σ cᵢ gᵢ = κ ≠ 0 in GF(p)[t, u, b, v] for p ∈ {2147483629, 2147483587} and s₀ ∈ {2, 3, 5, 7, 11}
  (10 certificates). The criterion "exactly in ℚ[t, u, b, v]" cannot be met by this route: probe 13 (12 to 50 primes, up to
  467 digits of modulus) did not reconstruct the rational cofactors at s = 2, because their coefficients exceed about 230
  digits; liftstd over ℚ at s = 7 did not finish in 15 min (probe 11). So the status of D1 is *certified over GF(p)* (the
  chain polynomials are exact over ℚ and reduced mod p by this script; Singular is untrusted), and nothing is certified over
  ℚ for the saturated level-2 ideal. By the spreading-out argument, a proper ideal over ℚ is proper modulo all but finitely
  many primes, so unit modulo 2 primes at 5 slices is evidence, not proof. No criterion was loosened: the first wording was
  not satisfiable and nothing was passed in its place.
- D2 (`full_cert`) is not attempted by interpolation (the s-degree of the cofactors exceeds 20; the cost estimate is in the
  note). The run of record for the generic-s question is one `std` of f₀ f₁ f₂ f₁₁ and the saturation generator mod
  2147483629 in the full ring with the block order (dp(4), dp(1)) (s last), 60 min cap (`certs/fullring.json`, `logs/`).
- `slice_cert` is skipped (and reported as skipped) when `chain` fails, so a mutated chain does not also fire it.
- Toy: after normalization the generators are q²+1, 0, q (Singular's cofactors 1, 0, −q), not q²+1, 0, 2q.
- `dims` (`--compute=dims`) is added: the dimension, multiplicity and unit-ness mod p of the saturated chain ideals at s₀ ∈
  {2, 3, 5, 7, 11}, written to `certs/dims_p<p>.json` and printed as info. The numbers quoted in the note for V₀, V₁, V₂ come
  from it, not from the probes.
- Controls, computed in a dev batch before declaring (`logs/ctl_dev_*`): `Phi1-sign` fires `blocks`, `chain`, `denoms`,
  `planted_s1` (not `fields`: σ is solved from the same mutated E₁, E₂, so the identity holds by construction; `Psi-sign`
  likewise fires only `blocks`, `chain`). The README table's target lists for these two were wrong; the lists above are the
  corrected targets. The other seven controls fired on their README targets in the dev batch. The runs of record repeat all nine.
- The script was edited (the `dims` step, additive) while the dev control batch was running; no check changed.
