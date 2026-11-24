# I148-mac: the coordinator's review of #148's certificate for the forward direction at every l

Machine: macOS (the coordinator's Mac, arm64), Python 3.14, sympy 1.14.0, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/148. Reviewed branch `wip/i148-zerilli-certificate` at ad3bc5e,
raw `I148-rpi5` at 9aa1b41.

## Independent check `ind148.py` (criteria written before its first run)

ind148 shares no code with `zerilli_certificate*.py` or `zerilli_derivation_lib.py`. #148's closing report says its
runner did not open the coordinator's `ind*.py`. ind148 reuses the coordinator's `I143-mac/ind143.py` operator
(Lichnerowicz form) with **P abstract**: P = P(x), P″ removed by Legendre's equation (1 − x²)P″ = 2xP′ − LP, L symbolic.
It takes #148's seven printed equations and seven printed certificate coefficients from `zerilli_certificate_output.txt`
as data, parsed with sympy. ψ (DG06 (9)) and V (DG06 (6)) are typed by the coordinator, with λ = (L − 2)/2.

My radial forms: δR_tt = F_tt P E, δR_tr = F_tr P E, δR_rr = F_rr P E, δR_tx = F_tx P′E, δR_rx = F_rx P′E,
(1 − x²)δR_xx = (a P + b xP′)E, δR_φφ/(1 − x²) = (c P + d xP′)E, with t → 0 for E.

| id | criterion | kind |
|---|---|---|
| R0 | planted: (a) for a general even h, the abstract-P components with L = 6, 12 and P → P_2, P_3 equal the explicit-P components of the same operator, all 10, symbolic in r, x, M, s; the forms F_*, a, b, c, d are x-free. (b) Odd Regge–Wheeler with abstract P: h1 = rΨ/F, s h0 = F(F h1)′, Ψ,ₓₓ = (V_RW + s²)Ψ: all 10 components vanish, L symbolic | symbolic |
| R1 | each printed equation of #148 lies in the Q(r, M, s, L)-span of mine: tt in {F_tt}, tr in {F_tr}, rr in {F_rr}, tx in {F_tx}, rx in {F_rx}, trace and traceless in {a, b, c, d}; the multipliers are printed | exact certificates |
| R2 | with #148's printed equations and coefficients, ψ,ₓₓ − (V + s²)ψ = Σ c_ik D^k E_i holds exactly, jet by jet, in Q(r, M, s, L); the denominators of the 7 coefficients factor into L, r and (L − 2)r + 6M only | symbolic |

R1 and R2 together give #148's statement with my operator: each E_i vanishes on every solution of δR = 0, so Z does.

Mutations, each must exit 1 with its target failing: `legendre` (2xP′ → −2xP′ in the reduction; R0), `lich` (the
∇_a∇_b h term dropped; R1), `ccoef` (the traceless coefficient −2(r − 2M)/r² halved; R2), `vz` (9M² → 8M² in V; R2),
`psi9` (λ + 1 → λ + 2 in (9)'s first denominator; R2).

A run that has not finished after 2 hours is stopped and reported as not completed.

## Results
