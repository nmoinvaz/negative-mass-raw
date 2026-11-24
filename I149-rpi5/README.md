# I149-rpi5: DG06's (cz), (nv1) and DG08's Lemma 1 in every version, quoted from the sources (#149)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/149
Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0), run with `-I`. No repository file is written.

Written 2026-11-23, before the first fetch. Nothing from the sources below is run: TeX, PDF and HTML are read as text only,
and any text in them addressed to an AI agent is quoted, not acted on. No message, comment or erratum goes to the authors or
any site.

## Sources to try, in order

Each download goes into its own new directory (`dg06_listing/`, `dg06_v1/`, `dg06_v2/`, ..., `dg08_listing/`, `dg08_v1/`, ...)
with the HTTP status and sha256 recorded in `fetch.log`.

| # | source | what it gives |
|---|---|---|
| 1 | https://arxiv.org/abs/gr-qc/0604021 | DG06 listing: versions (v1, v2, ...), submission dates, journal-ref, DOI |
| 2 | `curl -sL https://arxiv.org/e-print/gr-qc/0604021vN` for each N the listing shows | TeX source of each version (gzip of one .tex, or a tar) |
| 3 | `https://arxiv.org/pdf/gr-qc/0604021vN` for a version whose source is missing or cannot be read | PDF, read with `pdftotext` if installed |
| 4 | https://doi.org/<DOI of the listing's journal-ref> | the journal text (expect 403 or a paywall: record the status, mark *(unverified)*) |
| 5 | https://inspirehep.net/api/literature?q=arxiv:gr-qc/0604021 (fields: titles, publication_info, dois) | cross-check of journal-ref and DOI against a second index |
| 6 | https://arxiv.org/abs/0809.3615 | DG08 listing: versions, dates, journal-ref, DOI |
| 7 | `curl -sL https://arxiv.org/e-print/0809.3615vN` for each N, PDF as in 3 if needed | DG08 TeX of each version |
| 8 | https://doi.org/<DOI of DG08's journal-ref> | DG08's journal text, as in 4 |

Not tried: mirrors or copies of the journal text outside the publisher, arXiv or INSPIRE.

## What is quoted, per DG06 version and for the journal text

Exactly, with the version, the equation label and the TeX line number (`grep -n` on the extracted file):

1. **(cz)**, the condition at r = 3μ/(2λ): in particular the sign of 2λ²/(3μ(2λ+3)).
2. **(nv1), H₁ line**, in particular its denominator.
3. **(nv1), H₂**, the ζ term, in particular its sign.
4. For the version read in #146 (`I146-rpi5/dg06_src`, sha256 4da32b56…): which listing version it is, by byte comparison.

A version that cannot be read gets "could not be read" and the reason (HTTP status or the file's type).

## What is quoted from DG08

Lemma 1 exactly (variable, expansion, constants), with the arXiv version and the TeX line. Then, in `lemma1_conversion.py`
(sympy, symbolic in λ, μ or M, with the substitution written first), the conversion of its condition to ζ′(r_s)/ζ(r_s):

- if DG08's variable is ψ = c₋₁/(r − r_s) + c₀ + …, the substitution is ζ = (2λr − 3μ)ψ = 2λ(r − r_s)ψ, so ζ(r_s) = 2λc₋₁ and
  ζ′(r_s) = 2λc₀ (DG06's (im)); the ratio is c₀/c₋₁;
- DG08's M is compared with DG06's μ through μ = −2M, which DG08's own definitions must confirm (to be read, not assumed).

Criteria, fixed now:

| id | criterion | can fail how |
|---|---|---|
| C1 | the conversion's output equals c* = −2λ²/(3μ(2λ+3)) = λ²/(3M(2λ+3)) (#146 §1) as a rational-function identity | prints the difference; non-zero exits 1 |
| C2 | planted: the same code with the sign of the DG08 constant reversed (`--mutate=sign`) does not equal c* and exits 1 | the check must fire on the mutation |
| C3 | the conversion uses only DG08's text and DG06's (im); it does not read #146's c* until the final comparison | by construction, printed order |

If DG08's Lemma 1 has a form that does not equal c*, that is reported as a discrepancy, not adjusted.

## Deliverables

- `quotes.md`: every quote with its source file, line and sha256.
- The proposed text for `notes/literature.md` goes in the closing comment on #149 (the coordinator edits the note).
- The closing comment lists acceptance criteria with verdicts, what ran and its exit codes, this folder and its commit.

## Added after fetching and reading the sources, before running any script (2026-11-23)

What the fetch showed (details in `fetch.log` and `quotes.md`): DG06 has two arXiv versions, v1 (5 Apr 2006) and v2
(29 May 2006, byte-equal to #146's file); v1 has no (cz), (nv1), (im) or Lemma 1. DG08 has three, v1 (21 Sep 2008),
v2 (19 Jun 2009), v3 (17 Sep 2009); only v2 and v3 have a "Lemma 1" with the smoothness condition (v1's Lemma 1 is the
intertwiner lemma, and it prints the condition as (crc) in its section 2, with a remark on DG06's eq. (16)). The journal
DOIs answered 403 (Cloudflare challenge page); not bypassed. The second journal URL tried for DG06
(`iopscience.iop.org/.../pdf`) was not in the list above and also answered 403.

Two scripts, `~/Source/negative-mass-venv314/bin/python -I`, formulas typed from the quoted TeX lines (not read from the
files), each check with a `--mutate=` that must make it fail. Predictions written now:

`lemma1_conversion.py` (DG08)

| id | check | prediction |
|---|---|---|
| A1 | substitution ζ = (2λr − 3μ)Ψ_z, μ = −2M, r_s = −3M/λ, DG08's (crc) c₀ = λ²c₋₁/(3M(3+2λ)) gives ζ′(r_s)/ζ(r_s) = −2λ²/(3μ(2λ+3)); only then compared with c* (#146) and with DG06's printed (cz) | equals c*, and is −1 times the printed (cz) |
| A2 | DG08's (zm6) coefficient (ℓ+2)²(ℓ−1)²/(12M(ℓ²+ℓ+1)) equals λ²/(3M(3+2λ)) at λ = (ℓ−1)(ℓ+2)/2 | equal |
| A3 | first principles from DG08's own (RW2), (RW2a): a Laurent Ψ_z = c₋₁/ρ + c₀ + c₁ρ + … makes K and H₁ pole-free iff c₀/c₋₁ = DG08's (crc) (both K and H₁ give the same ratio) | PASS, ratio equals (crc) |
| A4 | DG06's (RW2)/(RW2a)/(RW3a) and DG08's (RW2)/(RW2a)/(zeri) are the same expressions for q (= f), h, so Ψ_z of DG08 is ψ_Z of DG06 | textual and symbolic equality |

Mutations: `sign` (the (crc) constant negated; A1 and A3's comparison fire), `h_typo` (a sign in h's numerator; A3 fires),
`zm6` (ℓ² + ℓ + 1 → ℓ² + ℓ + 2; A2 fires).

`dg06_check.py` (DG06 v1/v2)

| id | check | prediction |
|---|---|---|
| E1 | (AppB2), typed, has at r_s the residues A = 2/ρ and B = 4λ²/(3μ(2λ+3))/ρ, equal to the 1/ρ coefficients of the printed (exp) (v1 line 825–830, v2 line 364–369); an analytic χ then has χ′/χ = −2λ²/(3μ(2λ+3)) | PASS; the printed (cz) of v2 is −1 times this |
| X1 | ζ = C r e^{−kr}(r+μ)^{kμ}e^{kt} of (AppC5), kμ = 2λ(λ+1)/3, put through the printed (nv1) and through the derived map (from (RW2), (RW2a), ψ = ζ/(2λr − 3μ), M = −μ/2): compared with (RW24a) | K printed = K derived = (RW24a) K for one C; H₁ and H₂ derived equal (RW24a), H₁ printed is 2/r times it, H₂ printed differs; a miss of this prediction is a discrepancy to report |

Mutations: `exp_sign` (E1 fires), `rw24a_k` (the sign of (RW24a)'s K; X1 fires).
(nv1) against (3)–(4) at the level of coefficients was done by #146 (R.7) and the coordinator (`I146-mac`, Q3) on the same file;
it is not repeated here.

## Run log (2026-11-23), what ran and in what order

All scripts: `~/Source/negative-mass-venv314/bin/python -I`, nice 10, one process. Final runs (`*.time` hold /usr/bin/time -v):

| script | exit | PASS | wall | peak rss | log |
|---|---|---|---|---|---|
| `lemma1_conversion.py` | 0 | 10 | 2.0 s | 60 MB | `lemma1_conversion.log` |
| `lemma1_conversion.py --mutate=sign` | 1 | | | | `lemma1_conversion_mut_sign.log`: A3.K, A3.H1, C1, C1', C1'' FAIL |
| `lemma1_conversion.py --mutate=h_typo` | 1 | | | | A4, A3.0, A3.H1 FAIL (A4 was not predicted; A3.H1 was) |
| `lemma1_conversion.py --mutate=zm6` | 1 | | | | A2 FAIL |
| `dg06_check.py` | 0 | 12 | 5.1 s | 62 MB | `dg06_check.log` |
| `dg06_check.py --mutate=exp_sign` | 1 | | | | E1a FAIL |
| `dg06_check.py --mutate=rw24a_k` | 1 | | | | X1.H1d, X1.H2d FAIL |
| `make_quotes.py` | 0 | T1 x4 | 0.04 s | 19 MB | `make_quotes.log`, writes `quotes.md` |
| `make_quotes.py --mutate=textual` | 1 | | | | T1.q FAIL |

Mistakes, kept in the folder and not hidden:

- `dg06_check_run1.log` (exit 1, 2 min 44 s): 8 FAIL and one vacuous PASS, all from my script. sympy did not cancel the symbolic
  powers `(r+μ)^n` in X1, so equalities that hold were not recognized; and E1a read the residues with `.coeff(rho, -1)` on an
  unexpanded expression, got 0, and compared 0 with 0 (a PASS that could not fail). Fixed by writing ζ = r u e^{kt} with
  u′ = u(n/(r+μ) − k) (rational expressions only) and by taking the residues with `limit`, and by adding E1a0, which requires
  the residues to equal 2 and 4λ²/(3μ(2λ+3)). No criterion or prediction was changed. Run 1 also printed `nan` for χ′/χ.
- `make_quotes.py` first run: T1.inv FAIL because I sliced fixed line numbers that missed the equation. Replaced by extraction
  from the `\label` line to `\end{equation}`. T1.q and T1.h passed in that run.
- A4 of `lemma1_conversion.py` compares two expressions typed by me, so it can only fire under `--mutate=h_typo`; the real
  check that DG06's and DG08's definitions are the same text is T1 of `make_quotes.py`.
- The mutation `--mutate=textual` of `make_quotes.py` writes `quotes.md` before it exits 1; the file in the folder is from the
  clean run that followed.
- `make_index.py` ran once from the wrong directory (no effect).
