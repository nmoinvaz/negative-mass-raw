# I175-rpi5: modular cofactors, CRT and rational reconstruction of a unit certificate for #157's numerator ideals

Machine rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared), at most 3 processes, each `nice -n 10`, one thread.
Issue: https://github.com/nmoinvaz/negative-mass/issues/175. Branch `wip/i175-unit-cert`, worktree
`~/Source/negative-mass-i175`, from main 3384b61. Python `~/Source/negative-mass-venv314/bin/python` (3.14.10, sympy 1.14.0,
no gmpy2). Singular 4.4.1 at `/usr/bin/Singular`. Written 2026-11-28, before the runs of record (the `dev/` folder holds the
development runs that fixed the numbers below; each is named in the amendments).

## Question

#157 left open (H): is `1 - s u1` plus a subset of #157's coefficient ideals the unit ideal over Q? Modulo 32003 R2 and
J_all (R3) are (#157 `dev_R2_p32003`, `dev_R3_p32003`); `liftstd` over Q stopped at 1 h. A unit certificate
sum c_i f_i = kappa != 0 over Q[s, u0..u4] for R2 or J_all decides lambda = 0 without H; for the numerators of I22 it gives
H's two memberships (`a`, `b^2`) up to a power of u1.

## Candidates (in order, none added or reordered after a run)

| case | generators (regenerated from `three_scalars_ideal.py`) | count | terms |
|---|---|---|---|
| R2 | N'_ab at theta_0 = pi/2 and at (c, S) = (3/5, 4/5), then `1 - s u1` | 11 | 188 160 87 108 466 412 430 360 350 283 2 |
| R3 | J_all: every coefficient of c^k and S c^k of every N'_ab, then `1 - s u1` | 34 | up to 369 |
| K22 | the five N'_22 coefficients, then `1 - s u1` (H) | 6 | 108 205 199 152 82 2 |

sha256 of each generator list (`t157.gens_text`): R2 642a19cc6c837168, R3 f831ffd08245fe8a, K22 07df55ac2035d820 (first 16 hex).
R3 is tried only if R2 does not stabilize, K22 only if neither does (the issue's order).

## Method

1. `three_scalars_cert.py emit` regenerates the generators with `three_scalars_ideal.py` (imported, read only) and writes
   `lifts/<case>_p<P>.sing`: `ring R = P,(s,u0..u4),dp; option(redSB); ideal I = ...; liftstd(I, T)`, printing G[1],
   kappa_p = sum I[i] T[i,1] (a constant) and every cofactor T[i,1].
2. Primes: the 31-bit primes below 2^31 - 1 from the top: 2147483629, 2147483587, 2147483579, ... (`prime_list`).
3. Each input runs once under `run_one.sh` / `run_list.sh` (nice 10, `timeout 3600`, never overwritten; `.out .err .time .rc`).
4. `check` reads the finished runs, divides each run's cofactors by kappa_p (so that sum c_i f_i = 1 mod p), keeps the runs
   whose cofactors have identical supports (a run on another Groebner path cannot be combined), applies CRT to every
   coefficient, rational reconstruction (Wang, bound sqrt(M/2) on numerator and denominator), and writes `certs/<case>.json`
   (primes used, cofactors as text).
5. Verification parses the certificate's text exactly (`t157.parse_poly`), regenerates the generators again, and checks that
   sum c_i f_i is a nonzero constant in sympy's `ring(..., QQ)`. Trusted: sympy 1.14.0 exact arithmetic; Singular only proposes.

## Stabilization rule (before the runs)

With K finished runs in the largest support group, the reconstruction from the first K - 1 and from all K primes must (a)
exist for every coefficient and (b) be identical. A certificate is accepted only if it also verifies exactly (step 5). A
failure of (a) or (b) means "not stabilized with K primes": the answer is then reported with K, the modulus size, the
number of coefficients without a reconstruction, the support group sizes and the cofactor term counts per prime. Status words:
verified exact certificate = *certified* (sympy trusted); modular results alone = *numerical evidence*.

## Planted cases (same code path, before the wall)

| id | ideal | known truth | expected |
|---|---|---|---|
| PLANT | 4 generators in Q[s, u0..u4]: 1 - s u1, Q u1 - P, u0 - B, u0 u1 - A (P, Q, B, A random 60-bit), mixed by a random unitriangular polynomial matrix | the hand-written certificate g4 - u1 g3 - (B/Q) g2 = BP/Q - A, transformed by the exact inverse | the reconstruction (kappa = 1) equals known_i / kappa; verifies |
| PLANT2 | 5 random quadrics in (s, u0, u1, u2), 4 monomials + constant, seed 1 | Singular's `liftstd` over Q (kappa has 186 digits) | the reconstruction equals the Q cofactors divided by kappa, coefficient for coefficient; needs about 40 of 64 primes |

Criteria for the planted cases (each can fail):
- P1 `gens_hash`: the regenerated generators have the sha256 that Singular was given.
- P2 `support_agree`: every prime in one support group.
- P3 `stabilize`: R(K-1) = R(K), no coefficient without reconstruction.
- P4 `cert_verify`: sum c_i f_i = nonzero constant, exactly.
- P5 `plant_known` (PLANT) / `plant_ref` (PLANT2): equal to the known certificate / Singular's Q answer, divided by kappa.
- P6 `too_few`: reconstructions R(k) from fewer primes than k0 (the first k with R(k) = R(K)) all differ from R(K) and none verifies.

## Controls (`check --mutate=NAME`, `controls`)

Declared target, then the result of the development run `dev/pl2` (computed on PLANT and PLANT2 before this README's
declaration; the controls of the wall cases are added with their dev results in the amendments):

| control | change | targets | dev result (PLANT, PLANT2) |
|---|---|---|---|
| `cert-corrupt` | 1 added to the last coefficient of the first nonzero cofactor | `cert_verify` | fires, fires |
| `cert-satoff` | the verification drops the last generator | `cert_verify` | fires, fires |
| `gen-corrupt` | the constant term of the first regenerated generator shifted by 1 | `gens_hash`, `cert_verify` | fires, fires |
| `run-scaled` | one run's cofactors off by a factor 2 | `stabilize`, `cert_verify` | fires, fires |
| `wrong-prime` | the last run read modulo another prime | `stabilize`, `cert_verify` | fires, fires |
| `few-primes` | a third of the primes | `stabilize`, `cert_verify` | fires, fires |
| `support-mix` | one run's cofactor gets an extra term | `support_agree` | fires, fires |
| `ref-corrupt` | the Q reference has 1 added | `plant_ref` | (PLANT2) fires |
| `known-corrupt` | the known certificate has 1 added | `plant_known` | (PLANT) fires |

An earlier `wrong-modulus` (CRT of the last run with the previous prime's modulus) crashed with a non-invertible
modulus and was silent; it was replaced by `wrong-prime` (amendment A1).

## Stop conditions

1 h per Singular run (`timeout 3600`); 2 h for any other single run; the session's budget is 3 to 6 h. Memory is reported,
never a stop condition. A run that reaches the stop is a result ("not finished in 1 h"), never retried with a changed
generator list.

## Amendments

(A1) 2026-11-28, before any run of record: `wrong-modulus` replaced by `wrong-prime` (see above).
