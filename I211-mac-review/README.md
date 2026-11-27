# I211-mac-review: the coordinator's review of #211 (independent check ind211)

Machine: macOS (the coordinator's Mac), Python 3.14.7, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/211.
Under review: branch `wip/i211-universe-lit` at eac1f17 (`notes/literature.md`'s new section, `notes/baby_universes.md`),
raw `I211-rpi5` at 77cb32e. Written 2026-11-27 before the first run of `ind211.py`.

#211 is a reading task, with no computation of record to rerun; its fetch and verification scripts touched the network
only. The review reads two things independently.

## ind211

- **K1, the references.** A fixed sample of six of the 25 arXiv ids in the new section: every fourth in sorted order,
  starting with the first. Each is fetched once from arXiv's API in a single query and stored here as data
  (`arxiv_sample.xml`). The entry in `literature.md` that cites the id must carry arXiv's title (compared ignoring
  case, punctuation and TeX markup) and the first author's surname.
- **K2, [SH02]'s H.** #211 says [SH02]'s H ≈ 1.1/a is the exponent of a fit r/a = 1 + b₄ exp(H(τ − b₅)) to the departure,
  not a de Sitter rate. The review reads arXiv:gr-qc/0205041's TeX source, stored as data in `sh02_src/`, and looks for
  that fit form and the value of H there.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | For each of the six sampled ids, the citing entry carries arXiv's title and the first author's surname |
| K2 | [SH02]'s source contains a fit of the throat's radius of the form 1 + b exp(H(τ − b′)), and the value of H that `literature.md` quotes |

## Mutations

| mutation | change | targets |
|---|---|---|
| `title` | K1 compares with the first sampled title with one word changed | K1 |
| `fitform` | K2 looks for exp(−H…) in place of exp(H…) | K2 |

## Runs

| file | what |
|---|---|
