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
