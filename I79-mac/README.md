# I79-mac: the coordinator's review of #79's independent review of #65

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2
processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/79. Reviewed branch `wip/i79-review-two-scalars` at 7c6d2a7 and
raw `I79-rpi5` at 5c63452.

## Rerun of the runner's scripts

The five scripts `notes/warp/review_two_scalars_{cartan,lemma,ideals,omega,compare}.py`, each full with its controls,
and `review_two_scalars_ideals.py --certs --no-controls` for the certificates file, from a detached worktree of 7c6d2a7
(`rerun/`).

## Independent check `ind79.py` (criteria written before its first run)

ind79 imports nothing from the repository: none of the five review scripts, `review_cartan.py`, `two_scalars.py` or
`phantom_source.py`. Its coordinate Ricci routine, its polar wall route (generic w(r)) and its Cartesian truncated-Taylor
route are the coordinator's, from `I77-mac/ind77.py` and `I78-mac/ind78.py`. #79's certificates enter only as data: the
cofactors are parsed from `review_two_scalars_ideals_certs_output.txt` and multiplied into the coordinator's own
coefficients.

Shared with #79 and #65: the metrics and frame, the definitions of P, Q, Z, Y, h, A = 2w − rw′, B = w′ + rw″ and
ω = (w′ − rw″)/(rw′²), the printed formulas (typed here from the notes), the cofactors, and the claims tested.

| id | criterion | kind |
|---|---|---|
| H0 | planted: the own Ricci routine finds Painlevé–Gullstrand Schwarzschild Ricci-flat | symbolic |
| H1 | b(t, x, ρ) a generic function, own coordinate Ricci in (t, x, ρ, ϕ), frame (n, ∂_x, ∂_ρ, ∂_ϕ/ρ), n = ∂_t − b∂_x: R(e_ϕ, ·) = 0; the block on (n, ∂_x, ∂_ρ) equals [[P − h, Q, Z], [Q, −P − h, Y], [Z, Y, h]] with P = n(b_x) − b_x², Q = −½(b_ρρ + b_ρ/ρ), Z = ½b_xρ, Y = −½n(b_ρ) + b_x b_ρ, h = ½b_ρ²; its determinant equals D = h(h² − P² − Q² + Y² + Z²) − P(Y² − Z²) + 2QYZ. All exact | symbolic |
| H2 | constant speed, own polar route: 16r³ det R₃ = Σ_{k=0..3} c_k c^{2k} with no odd powers of c; c₀ = 2r w′²(r²w′⁴ − 4w²w′² − (w′ + rw″)²) and c₃ = −2(rww″ + rw′² − ww′)²(2rww″ + rw′² − 2ww′) as printed in two_scalars.md. With w = (A + rw′)/2, w″ = (B − w′)/r, no c_k has a term free of A and of degree < 2 in B. #79's printed cofactors give Σ cof · c_k = A and = B² exactly with these c_k | symbolic |
| H3 | the no-open-set step by `sympy.dsolve`: 2w = rw′ has w = C r², and w′ + rw″ = 0 then forces C = 0, so w′ ≡ 0 | symbolic |
| H4 | accelerating bubble: (i) own Cartesian route, b = −v_s(1 − Q/4)³, v_s = 1 + t/2 + t²/3, x_s = t + t²/4 + t³/5, at (t, x, y) = (0, 3/5, 4/5), (1/4, −17/32, 3/5), (−1/2, 119/1040, 18/13): the frame block equals the constant-speed block with w = w̃ = x_s′ − v_s f, P shifted by +A w̃′c and Y by −A w̃′s/2, A = v_s′/v_s. (ii) With that block in general jets, 16r³D has degree 6 in c, its odd coefficients are divisible by 4Arw′, and #79's printed accelerating cofactors give Σ cof · e_k = 1 exactly, with e_k = c_k (k even), c_k/(4Arw′) (k odd), w″ = w′/r − ω w′² | exact + symbolic |
| H5 | the ω formula, 6 random rational instances with k ∧ m ≠ 0, dual K, M and a random ω₀: with dk = −ω₀ ∧ k and dm = ω₀ ∧ m, dm(K, M)k + ι_K dk = ω₀, and the map ω ↦ (ω ∧ k, ω ∧ m) has rank 4. With a random dk not of that form the candidate violates ω ∧ k = −dk | exact |
| H6 | b(ρ): own coordinate Ricci with b(ρ) generic; where b″ = εb′² − b′/ρ, R_ab = h((dρ)² − ((1 + εb)dt + ε dx)²) with h = ½b′², ε = ±1; and for ν = dρ + (1 + εb)dt + ε dx, the (t, x, ρ) component of ν ∧ dν is b′ | symbolic |

Mutations, each must exit 1 with its target failing:

| mutation | change | target |
|---|---|---|
| `pg` | √(2M)/r for √(2M/r) | H0 |
| `qsign` | +½(b_ρρ + b_ρ/ρ) for Q in the expected block | H1 |
| `c3` | 2rww″ + rw′² + 2ww′ for the last factor of the typed c₃ | H2 |
| `cof` | the first parsed cofactor of target A doubled | H2 |
| `ode` | second relation w′ − rw″ = 0 | H3 |
| `accY` | Y shifted by +A w̃′s/2 | H4 |
| `acccof` | the first parsed accelerating cofactor doubled | H4 |
| `omega` | dm(K, M)k − ι_K dk | H5 |
| `h2` | 2h for h in the expected b(ρ) tensor | H6 |

## Results

| file | what |
|---|---|
| `rerun/*.txt`, `.err`, `.rc` | the five scripts at 7c6d2a7 with their controls, and `ideals --certs --no-controls` |
| `rpi5_ideals_certs_output.txt` | `review_two_scalars_ideals_certs_output.txt` at 7c6d2a7, the cofactors ind79 reads |
| `ind79_run1.*` | run 1: H0 and H1 pass, then the coordinator's own assertion stops H2 |
| `ind79_run2.py`, `.txt` | run 2: every criterion passes (`ind79.py` is the same version) |
| `ind79_mut_*.txt` | its 9 mutations, on run 2's version |

**Rerun.** All six runs exit 0:

| script | time |
|---|---|
| `cartan` | 30 s |
| `lemma` | 27 s |
| `ideals` | 47 s |
| `omega` | 2 min 34 s |
| `compare` | 3 s |
| `ideals --certs --no-controls` | 5 s |

All 32 controls fire. Each output equals the committed one line for line, apart from the timings and the Python
version, including every residual printed in e-notation. The certificates file equals the committed one, so its
command is `python3 notes/warp/review_two_scalars_ideals.py --certs --no-controls`, which the note does not state.

**ind79 run 1** stopped at an assertion in the coordinator's code: the reduced 16r³D had the denominator sin²θ, which
the reduction did not replace by 1 − c². Run 2 divides by 1 − c² there. The criteria did not change.

**ind79 run 2** (exit 0, 2 s):

| criterion | run 2 |
|---|---|
| H0 | Painlevé–Gullstrand Ricci-flat |
| H1 | generic b(t, x, ρ): R(e_ϕ, ·) = 0, the block [[P − h, Q, Z], [Q, −P − h, Y], [Z, Y, h]] and det = D exactly |
| H2 | 16r³D of degree 6 in c with no odd powers; c₀ and c₃ as printed; each c_k in (A, B²); #79's 39 + 39 cofactors give A and B² exactly |
| H3 | w = C₁r², and w′ + rw″ = 4C₁r forces C₁ = 0 |
| H4 | the accelerating entries at 3 exact points (Cartesian route); degree 6 in c; odd coefficients divisible by 4Arw′; #79's 25 cofactors give 1 exactly |
| H5 | 6 instances: the candidate equals ω₀, rank 4, a random dk is violated |
| H6 | R = h((dρ)² − ν′²) and (ν ∧ dν)_{txρ} = b′ for ε = ±1 |

Re-solve: H1, #65's D for a generic b(t, x, ρ), fully symbolic. #79 did it in the Cartan jets of b = G(t, x, y² + z²)
and at 9 exact points.

| mutation | exit | failed | target met |
|---|---|---|---|
| `pg` | 1 | H0 | yes |
| `qsign` | 1 | H1 | yes |
| `c3` | 1 | H2 | yes |
| `cof` | 1 | H2 | yes |
| `ode` | 1 | H3 | yes |
| `accY` | 1 | H4 | yes |
| `acccof` | 1 | H4 | yes |
| `omega` | 1 | H5 | yes |
| `h2` | 1 | H6 | yes |
