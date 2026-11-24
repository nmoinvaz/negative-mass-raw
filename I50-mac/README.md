# I50-mac: the coordinator's review of #50's reading of critical_ghost.md's gaps and the Frolov map

Machine: macOS (the coordinator's Mac, arm64), Python 3.14, sympy 1.14.0, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/50. Reviewed raw `I50-rpi5` at d0ea4ce (no repository branch).

## Independent check `ind50.py` (criteria written before its first run)

ind50 shares no code with `frolov_map.py`, `make_quotes.py`, `citers.py` or `ctx.py`. It fetches its sources itself (GET
only, a generic client name) into its own folder and types each formula from the TeX it fetched. Shared with #50: the
list of sources, the sha256 values in `I50-rpi5/fetch.log`, and the four quotes tested in H5.

Sources: Brady gr-qc/9402023 (eqs. (2)–(9), (11), (mass1)), Frolov gr-qc/9704040v1 (eqs. (es), (ss_soln), the mass),
Maeda et al. 0811.2962v2 (eqs. (roberts1)–(roberts-mass)), Shirokov–Nachevsky 2610.13206v2, Shirokov 2604.00071,
Clough–Dietrich–Khan 2406.02466v2, and INSPIRE's record of arXiv:2610.38659.

| id | criterion | kind |
|---|---|---|
| H1 | the e-prints of gr-qc/9402023, gr-qc/9704040v1, 0811.2962v2, 2610.13206v2 and 2406.02466v2 fetched here have `fetch.log`'s sha256 | hashes |
| H2 | planted: each paper's printed solution satisfies its own printed field equations, with σ = Σ = 0. Brady: r² = αv² + βu² − uv and φ of (11), α ≠ 0, in (3)–(7). Frolov: R² = u² − uv − pv² and Φ of (ss_soln) in (es). Symbolic in α, β (Brady) and p (Frolov) | symbolic |
| H3 | the map U = √β u, V = v/√β, p = −αβ: (a) Brady's r² equals Frolov's R²; (b) ∂_UΦ_F = σ∂_Uφ_B and ∂_VΦ_F = σ∂_Vφ_B for exactly one σ ∈ {+1, −1}; (c) Brady's m = −uv(1 − 4αβ)/(4r) equals Frolov's M from 1 − 2M/R = 2g^{uv}R_{,u}R_{,v}; (d) α = 0 ↔ p = 0 and 4αβ = 1 ↔ p = −1/4 | symbolic |
| H4 | Maeda's (roberts1) is Brady's (8) with (C₁, C₂) = (α, β), and 2√π ∂φ_M = ±∂φ_B for exactly one sign, so p = −C₁C₂ and Φ_F = ±2√π φ_M + const | symbolic |
| H5 | quotes, whitespace-normalized, in the sources fetched here: 2610.13206v2 has "do not establish the scaling" and "consistent with a type-I critical solution"; 2604.00071 states a factor 1/2 (or 0.5) on the phantom stress-energy of its collapse run; 2406.02466v2 has "not a black hole"; INSPIRE's abstract of 2610.38659 has "0.100628" and "not stabilization" | text |

Mutations, each must exit 1 with its target failing: `hash` (one expected sha256 altered; H1), `brady` (β → −β in
Brady's r²; H2), `pmap` (p = +αβ; H3), `maeda` (1/(2√π) → 1/√π in Maeda's φ; H4), `quote` (a quote with one word
changed; H5).

## Results

| file | what |
|---|---|
| `rerun/` | `frolov_map.py` with its 10 mutations and `make_quotes.py` with `textual`, run on a copy of `I50-rpi5` on the Mac |
| `ind50_run1.py`, `.txt` | the independent check, run 1 (`ind50.py` is the same version); the sources it fetched are not committed again |
| `ind50_mut_*.txt` | its 5 mutations |

**Rerun.** `frolov_map.py`'s PASS/FAIL lines equal rpi5's (23 PASS), each of its 10 mutations exits 1, and the regenerated
`quotes.md` is byte-identical; `--mutate=textual` exits 1.

**ind50 run 1** (exit 0):

| criterion | run 1 |
|---|---|
| H1 | the five e-prints have `fetch.log`'s sha256 |
| H2 | Brady's (8), (11) satisfy his (3)–(7), and Frolov's (ss_soln) his (es), symbolic in the parameter |
| H3 | with U = √β u, V = v/√β, p = −αβ: R² = r²; Φ_F = −φ_B + const (one sign); Brady's (mass1) equals the mass from (mass); α = 0 ↔ p = 0 and 4αβ = 1 ↔ p = −1/4 |
| H4 | Maeda's (roberts1) is Brady's (8) with (C₁, C₂) = (α, β), and φ_B = +2√π φ_M + const |
| H5 | 2610.13206v2: "do not establish the scaling" and "consistent with a type-I critical solution"; 2604.00071: "to force a clean collapse … we reduce the phantom stress-energy" by a factor 1/2; 2406.02466v2: "not a black hole"; INSPIRE's abstract of 2610.38659: "0.100628" and "not stabilization" |

So p = −C₁C₂, and Φ_F = −φ_B = 2√π φ_M + const when φ_M takes the lower sign of Maeda's ±, as #50 states. Re-solve: H3, the map from the two papers'
own printed formulas.

| mutation | exit | failed | target met |
|---|---|---|---|
| `hash` | 1 | H1 | yes |
| `brady` | 1 | H2 (and H3) | yes |
| `pmap` | 1 | H3 | yes |
| `maeda` | 1 | H4 | yes |
| `quote` | 1 | H5 | yes |
