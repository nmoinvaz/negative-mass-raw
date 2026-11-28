# I264-rpi5: independent review of E4 (k = 6), E2W and E5 (k = 7), their boundary terms, and the masters ∫ℓ²D₃, ⟨lt²C²⟩, ⟨lt³D₃⟩ (#264)

Machine: rpi5-ubuntu (Ubuntu, 4 cores, 8 GB, aarch64; Python 3.14.10 venv `negative-mass-venv314`, mpmath 1.3.0 with the pure-Python
backend, sympy 1.14.0), shared with other projects (at most 3 processes of mine, `nice -n 10`; runs longer than a few minutes are systemd
user units `nm-i264-*`). Runner `negative-mass-rpi5-i264` (Claude Code, Sonnet 5.5, account claude-me2), started by the coordinator over hc.
Issue: https://github.com/nmoinvaz/negative-mass/issues/264 (milestone G5, widened by the coordinator to E2W and E5 of #263).
Code: worktree `~/Source/negative-mass-i264`, branch `wip/i264-identity-review` from c618f36; script `notes/wormhole_largeD/identity_review.py`,
output `identity_review_output.txt`, note `identity_review.md`. Push: `git push origin HEAD:refs/heads/wip/i264-identity-review`.
Logs: `dev_NN_*` development runs, `run_NN_*` runs of record, `ctl_*` controls; each keeps stdout (`.log`), stderr (`.err`) and exit code
(`.rc`); nothing is overwritten, reruns are numbered. Status words as in AGENTS.md. No sentence here claims novelty.

## Order of work (the disclosure the task asks for)

1. `derivations.md` was committed first (raw commit 38869df, 2026-11-28T03:09Z by this machine's clock), before any script of this review ran
   and before I opened `omega4.md` or `omega5.md` beyond the statement lines listed in its §0. The by-hand derivations include the
   boundary terms, the growth bounds, the weights w₄, g₄, w₄′, the primitives W₄, P, W and the reduced forms of G₆ and G₇.
2. This README (criteria, routes, mutations) is written after that and before any run.
3. After the declared runs I compare with `omega4.md` and `omega5.md` (derivation sections, and `order6.py`, `order7.py`, `PanelK` only
   to identify differences); differences are reported, not fixed.

## Routes

- **Hierarchy (own code; shares nothing with `PanelK`, `order4.py`–`order7.py`, or the coordinator's `ind26`/`ind208`).** The order equations of
  derivations §1, with c_m expanded by sympy from K(ε) = (1+εΩ)e^{εl} − ½e^{−εl} − εSe^{−εl} at run time (no table). Taylor jets in l: the
  Frobenius recursion at the throat, then power series about l = 1.5, 2.5, … propagated by one step of length 1, all in Python integers
  (fixed point, 400 to 512 bits). Orders Y₀ … Y₇, L₀ … L₆. The θ-integrals by Gauss–Legendre panels in v = √l (dθ = v dv/u(v²), analytic
  in v), l_max = v_max² ≈ 340. C and D₃ from mpmath (`clsin(2, π − 2θ)`, `(3/4)ζ(3) + clcos(3, π − 2θ)`), checked against
  nested quadrature of C′ = 2 lt, D₃′ = 2C.
- **Identities.** Each side is a θ-integral of the hierarchy's own functions times the weights of derivations §2–§5, written from the
  derivation and verified by `sym` (not copied from the notes).
- **Reduced forms.** G₆ and G₇ from the definitions (G_k = 2∫(h_k − Ω_{k−1})/S) against the reduced forms of §4.9 and §5.11, which use only
  Y₀ … Y₃ and L₀ … L₃.
- **Masters.** Direct quadrature of the definitions at 70 digits (no Fourier series, no Parseval), then a PSLQ identification of the value in
  a weight-6 basis of my own; after the derivations were committed, comparison with the notes' closed forms.

## Criteria (each can fail; fixed before the first run; "digits" = −log₁₀(|Δ| / the largest term involved))

| id | criterion | bar |
|---|---|---|
| SY | sympy residual 0 for: c₁ … c₃ in the S-form, c₆ and c₇ against the printed definitions, w₄, g₄, w₄′ from c_m, P′ = u g₄, W₄′ = w₄, W′ = w₄′ (with C′ = 2(ℓ + ln 2), D₃′ = 2C), (L cot θ)′ = 2h/S from the L equation, E3's relation, the throat and π/2 expansions of the boundary terms | residual 0 |
| H0 | planted truth: the hierarchy's Y₁, L₁, Y₂, L₂ against README's closed forms (K(u) by quadrature) at 20 nodes with l ≤ 100 | 1e-35 absolute |
| H1 | the hierarchy converged: a second setting (other N, panel layout, bits) changes every reported integral | by < 1e-40 |
| H2 | G₂ … G₆ from the definition at the closed forms of Ω₀ … Ω₄ (README, #220) vanish; G₇ at #263's Ω₅ is reported with its value | 1e-30 absolute each (G₇ reported) |
| E1_6, E1_7 | E1 at k = 6, 7 | 30 digits |
| E2_4, E2_5, E2_6 | E2 at m = 4, 5, 6 | 30 digits |
| E3_5, E3_6, E3_7 | E3 at m = 5, 6, 7 minus one: ∫Y_m(4ℓ + 2c₁)/S = −4∫(ℓ − Ω₀)F_{m−1} | 30 digits |
| **E4_6** | ∫Y₄w₄ = −2∫(22ℓ² − 8Ω₀ℓ − 2Ω₁ + 16uC)F₃ at Ω₀ … Ω₃ roots and at Ω₂ shifted by +1/2 | **30 digits** |
| E4_7 | ∫Y₅w₄ = −2∫(…)F₄ | 30 digits |
| **E2Wa, E2Wb** | ∫12ℓ²L₄ = −2∫(−4ℓ³)h₄/S; ∫g₄L₄ = −2∫P h₄/S | **30 digits** |
| **E5_7** | ∫Y₄w₄′ = −2∫W u F₃, with W(π/2) = 0 checked (K = 0) | **30 digits** |
| G6R, G7R | G₆, G₇ from the definition = reduced form, at the root and with the free constant shifted (slope −4π) | 30 digits (shifted), 1e-30 absolute (root) |
| SLOPE | dG_k/dΩ_{k−2} = −4π, k = 6, 7 | 1e-30 relative |
| HYP | with Ω₂ shifted by 1e-3, E2Wb fails by the predicted amount (G₄ ≠ 0) while E4_6 still holds | E2Wb fails (≥ 1e-8), E4_6 30 digits |
| BND | the boundary terms of derivations §3 scale as predicted at both ends (throat: b/θ → the stated leading coefficient; outer: b/(x l^q) bounded) | the table of the note |
| GROW | Y_k/l^k at l = 256 (reported, no bar) | |
| M0 | C and D₃ by mpmath against nested quadrature at 5 values of θ | 40 digits |
| **M1** | ∫₀^{π/2} ℓ²D₃ = ¾ζ(3)J₂ + (π/4)(2 ln 2 ζ(4) + 5ζ(5) − 2ζ(2)ζ(3)), J₂ = ∫ℓ² | **40 digits** |
| M2, M3 | ⟨lt²C²⟩ and ⟨lt³D₃⟩ by quadrature: value to 60 digits and, after the commit, against the notes' closed forms | 40 digits |
| M4 | PSLQ of M1, M2, M3 (my own basis, weight 6, no Li) at 70 digits finds a relation, or reports that it does not | reported |
| FP | planted finite-part split (a convergent integral written as two divergent finite parts) by the rule of derivations §9 against direct quadrature | 40 digits |

## Mutations (`--mutate=NAME`; the targets are computed in a development run and declared in an amendment *before* the runs of record)

| name | change |
|---|---|
| `e4_20` | the 22ℓ² of E4's right side as 20ℓ² (the task's example) |
| `e4_Om1` | E4's −2Ω₁ as +2Ω₁ |
| `e4_C` | E4's 16uC as 8uC |
| `e2w_P` | P without the D₃ term |
| `e2w_g` | g₄'s −32ℓ² as −30ℓ², P left as derived |
| `e5_noD3` | W without its 16D₃ cot θ term |
| `e5_a1` | a₁ = 8Ω₁ + 8Ω₀² + 64 ln 2 as 8Ω₁ + 8Ω₀² + 32 ln 2 in W only |
| `e5_K` | W with the constant K = 0 replaced by +1/100 |
| `hyp_G4` | Ω₂ shifted in the hierarchy by 1e-3 (E2Wb and E5_7 should fail, E4_6 not) |
| `c_wrong` | c₃'s −2ℓ³ taken as −3ℓ³ in the hierarchy (H0, H2, G6R, G7R) |
| `g6r_slope`, `g7r_slope` | the reduced forms with the Ω₄- or Ω₅-dependence dropped |
| `m1_basis`, `m1_J2` | M1's closed form with 5ζ(5) as 4ζ(5), with J₂ as J₂ + 0.01 |
| `fp_const` | the FP rule's constant term replaced by the next term |

## Amendments

(none yet)
