# I149-mac: the coordinator's review of #149's reading of DG06 and DG08

Machine: macOS (the coordinator's Mac, arm64), Python 3.14, sympy 1.14.0, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/149. Reviewed raw `I149-rpi5` at ee03b34 (no repository branch).

## Independent check `ind149.py` (criteria written before its first run)

ind149 shares no code with `lemma1_conversion.py`, `dg06_check.py` or `make_quotes.py`. It fetches the five arXiv
e-prints itself (GET only, a generic client name), unpacks them into its own folder, and reads the TeX with its own
patterns. Shared with #149: the version list (gr-qc/0604021 v1, v2; arXiv:0809.3615 v1, v2, v3) and the sha256 values in
`I149-rpi5/fetch.log`.

| id | criterion | kind |
|---|---|---|
| P1 | the five e-prints fetched here have the sha256 of `I149-rpi5/fetch.log`, and their main .tex files the sha256 listed there | hashes |
| P2 | DG06 v1 has none of `\label{cz}`, `\label{nv1}`, `\label{im}` or "Lemma 1"; DG06 v2 has all of them | text |
| P3 | DG06 v2's (cz): its right-hand side is `\frac{2 \lambda^2}{3 \mu (2 \lambda+3)}` with no minus sign before it; (nv1)'s H₁ line has the denominator `r (r+\mu) (2 \lambda r - 3 \mu)`; (nv1)'s ζ term of H₂ is preceded by `+` | text, whitespace-normalized |
| P4 | DG08 v1 contains "sign error" within 200 characters of "(16)" or of a reference to DG06's eq. 16; DG08 v2 and v3 each state Lemma 1 with c₀ = λ²c₋₁/(3M(3+2λ)) | text |
| P5 | with Ψ = c₋₁/(r − r_s) + c₀ + O(r − r_s), ζ = (2λr − 3μ)Ψ, μ = −2M, r_s = 3μ/(2λ): ζ′(r_s)/ζ(r_s) = c₀/c₋₁, and DG08's c₀/c₋₁ = λ²/(3M(3+2λ)) equals c* = −2λ²/(3μ(2λ+3)) of `I146-mac` Q4 | symbolic |

Observation, not a criterion: the HTTP status of the two DOIs from here.

Mutations, each must exit 1 with its target failing: `hash` (one expected sha256 altered; P1), `v1lab` (`\label{RW1}`,
present in v1, added to the labels v1 must lack; P2), `minus` (P3 run with `-\frac{2 \lambda^2}` as the expected form;
P3), `sign` (DG08's c₀ taken with a minus; P5).

## Results
