# I78-mac: the coordinator's review of #78's test of two same-sign scalars on the Alcubierre wall

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2
processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/78. Reviewed branch `wip/i78-same-sign` at 1d59d2f
(`same_sign_scalars.py` sha256 5161ecd1…) and raw `I78-rpi5` at 871a4e7.

## Rerun of the runner's script

`python3 notes/warp/same_sign_scalars.py`, full, with its 22 controls, from a detached worktree of 1d59d2f (`rerun/`).

## Independent check `ind78.py` (criteria written before its first run)

ind78 imports nothing from the repository: no `same_sign_scalars.py`, `three_scalars.py`, `two_scalars.py` or
`phantom_source.py`. Its Ricci routine, polar wall route (generic w(r), the coframe of comoving polar coordinates) and
Cartesian truncated-Taylor route are the coordinator's, copied from `I77-mac/ind77.py`, which shares nothing with #78
either. The rank tests use the gcd and the real roots of the 2 × 2 minors of R₃ − λη₃ as polynomials in λ, and
`sympy.solve` for the b(ρ) system. #78 uses the 3 × 3 minors of the 4 × 4 pencil, Gröbner bases and Rabinowitsch.

Shared with #78: the metrics, the frame (n = ∂_t − b∂_x, ∂_x, ∂_ρ), the profiles and #77's point lists, the printed
formulas of `same_sign_scalars.md` (typed here from the note), and the claims tested.

Notation as in the note: w = v(1 − f), u = r w″ − w′, V = w u + 2r w′² (the note's v), z = 2w′ + u s², c = cos θ,
s = sin θ, F = R₀₁(R₀ρ² + R₁ρ²) + 2R_ρρ R₀ρ R₁ρ, B = −z(u² + V²) + 2r u V w′² s².

| id | criterion | kind |
|---|---|---|
| F0 | planted, own Ricci routine: Painlevé–Gullstrand Schwarzschild is Ricci-flat. P1 = AdS₂ × ℝ², (−dτ² + dz²)/z² + dR² + R²dΘ², has R = −g + (dX² + dY²) with X + iY = R e^{iΘ} (λ = −1, s = +1). P2 = dS₂ × ℝ² with 1/τ² has R = g − (dX² + dY²) (λ = 1, s = −1). D2 = −dτ² + dz² + E²(dX² + dY²), E = 1 + (z² − τ²)/10, has R + (4/10)g/E = (4/100)(τ² − z²)(dX² + dY²). All exact | symbolic |
| F1 | the wall, own polar route, generic w: the frame block equals the printed entries (R₀₀ = −[2ww′ + 2wuc² + rw′²(1 + c²)]/(2r), 2rR₀₁ = −z, 2rR₀ρ = usc, 2rR₁ρ = Vsc, R_ρρ = w′²s²/2, R₁₁ = −R₀₀ − 2R_ρρ) mod s² + c² − 1. F = s²c²B/(8r³) from the own entries. B is affine in s² with constant term −2w′(u² + V²). For a generic symmetric R₃ with R₁₁ = −R₀₀ − 2R_ρρ and N = R₃ − λη₃: R₀ρ(N₀₀N₁ρ − N₀₁N₀ρ) + R₁ρ(N₁₁N₀ρ − N₀₁N₁ρ) + F = 0 identically | symbolic |
| F2 | re-solve at exact points of the wall (the 3 off-axis bump points of #77 at v = 7/4, the 18 explicit bump points and 4 random jet sets of `I77-mac`): R₃ is indefinite, and no real λ makes all 2 × 2 minors of R₃ − λη₃ vanish (gcd of the minors in λ without a real root), exactly. At the 18 tanh points (60 digits): R₃ indefinite, and at each real root of the minor N₀₀N₂₂ − N₀₂² some other minor has relative size > 1e-20 | exact + 60 digits |
| F3 | accelerating bubble, own Cartesian route: b = −v_s(t)(1 − Q/4)³, v_s = 1 + t/2 + t²/3, x_s = t + t²/4 + t³/5, at 3 exact points (t, x, y, 0), y > 0, Q < 4. The frame block equals the printed entries with w = w̃ = x_s′ − v_s f and its r-derivatives, A = v_s′/v_s: the constant-speed R₀₀, R₀₁, R₀ρ, R_ρρ with R₀₀ + A w′ c, R₁₁ − A w′ c, R₁ρ = s(Vc − A r w′)/(2r). No real λ makes all 2 × 2 minors vanish. At v_s = t, x_s = t²/2, t = 0 the block is [[−kc, 0, 0], [0, kc, ks/2], [0, ks/2, 0]] with k = v_s′ f′, at 2 exact points | exact |
| F4 | shift b(ρ), own Ricci with a generic b: the frame block is [[−h, Q, 0], [Q, −h, 0], [0, 0, h]], h = b′²/2, Q = −(b″ + b′/ρ)/2. `sympy.solve` of the 2 × 2 minors of R₃ − λη₃ for (λ, Q), with h a nonzero symbol, gives exactly {λ = h, Q = 0}. For b = 2 ln ρ at 3 exact points: λ = h is a root, R − λg has inertia (0, 2), and the kernel span(n, ∂_ρ) is not integrable ([n, ∂_ρ] = b′∂_x ∉ span) | symbolic + exact |

Mutations, each must exit 1 with its target failing:

| mutation | change | target |
|---|---|---|
| `pg` | √(2M)/r for √(2M/r) in the planted metric | F0 |
| `d2lam` | λ = −3γ/E for −4γ/E in D2 | F0 |
| `r00` | the sign of the 2wuc² term flipped in the typed R₀₀ | F1 |
| `bconst` | 2r u V w′² s² replaced by 2r u V w′² in the typed B | F1 |
| `psd` | at one bump point R₃ replaced by λη₃ + ε n nᵀ with the weighted trace −2λ (rank-1 N), λ = −1 | F2 |
| `accA` | the A w′ c term dropped from the typed R₀₀ | F3 |
| `qh` | the expected b(ρ) solution with Q = h | F4 |
| `psdmp` | added after run 1: the planted rank-1 N of `psd` at the first tanh point, through the 60-digit branch | F2 |

## Results

| file | what |
|---|---|
| `rerun/same_sign_full.*` | the rerun at 1d59d2f: stdout, `/usr/bin/time -l`, exit code |
| `rpi5_output.txt` | `same_sign_scalars_output.txt` at 1d59d2f, for the comparison |
| `ind78_run1.*` | run 1: every criterion passes |
| `ind78_mut_psdmp_run1crash.txt` | `psdmp` on run 1's code: a crash in mpmath's `polyroots` |
| `ind78_run2.py`, `.txt` | run 2: every criterion passes (`ind78.py` is the same version) |
| `ind78_mut_*.txt` | the 8 mutations, on run 2's version |

**Rerun** (exit 0, 85 s, 86 MB peak): 31 of 31 checks pass and 22 of 22 controls fire. The output equals rpi5's line
for line apart from the timings and the Python version.

**ind78 run 1** passed every criterion, and the 7 mutations of the table fired on target. None of them reached F2's
60-digit branch (the tanh points), so `psdmp` was added after run 1. On run 1's code it crashed: the planted N makes the
quadratic minor's root double, and mpmath's `polyroots` does not converge there. A real double root at a tanh point
would have crashed F2 in the same way. Run 2 takes the roots of that quadratic from the quadratic formula. Nothing else
changed, and the criteria did not change.

**ind78 run 2** (exit 0, 1 s):

| criterion | run 2 |
|---|---|
| F0 | Painlevé–Gullstrand Ricci-flat; P1, P2 and D2 exactly as printed |
| F1 | the six entries as printed (mod the circle); F = s²c²B/(8r³); B affine in s² with constant term −2w′(u² + V²); the certificate is an identity |
| F2 | R₃ indefinite and no real λ with rank(R₃ − λη₃) ≤ 1: bump 3 of 3, explicit 18 of 18, random 4 of 4 (exact), tanh 18 of 18 (60 digits) |
| F3 | the accelerating entries with A = v_s′/v_s as printed at 3 of 3 exact points, no common real root there; the v_s = 0 block as printed at 2 of 2 |
| F4 | R₃ of b(ρ) as printed; `sympy.solve` gives exactly {λ = h, Q = 0}; D3 at 3 points: inertia (0, 2), kernel span(n, ∂_ρ), the bracket outside it. R(e_ϕ, ·) = 0 is printed, not a criterion |

Re-solve: F2, the absence of a rank-1 λ at the 43 wall points, by the gcd of the minors in place of #78's 3 × 3 minors
of the 4 × 4 pencil.

| mutation | exit | failed | target met |
|---|---|---|---|
| `pg` | 1 | F0 | yes |
| `d2lam` | 1 | F0 | yes |
| `r00` | 1 | F1, F3 (both use the typed entries) | yes |
| `bconst` | 1 | F1 | yes |
| `psd` | 1 | F2 | yes |
| `psdmp` | 1 | F2 | yes |
| `accA` | 1 | F3 | yes |
| `qh` | 1 | F4 | yes |
