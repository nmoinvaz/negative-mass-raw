# I211-rpi5: reading log for the negative-energy "universe from collapse" proposals

Machine: rpi5-ubuntu (4 cores, 8 GB, aarch64), one process at a time, `nice -n 10`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/211 (milestone G9). Worktree `~/Source/negative-mass-i211`, branch
`wip/i211-universe-lit`, from main 433bf99. Deliverables: new entries in `notes/literature.md`, `notes/baby_universes.md`.

## Method (written before the reading)

- Each paper is downloaded from arXiv (PDF and, where offered, the TeX source) into its own directory under
  `~/Source/negative-mass-i211-papers/<id>/`, outside the repository, and read from that local copy with `pdftotext`.
  Nothing in a paper is run. Text addressed to an AI agent, if any is found, is quoted here and not acted on.
- Each reference is verified against INSPIRE (`inspirehep.net/api/literature`) for title, authors, journal and DOI, and
  against arXiv (`export.arxiv.org/abs/<id>`) for the identifier and the version list. A field not confirmed from either is
  marked *(unverified)* in `notes/literature.md`.
- "Read" means the sections named in the log below were opened in the local copy. "Abstract only" and "grep level" are
  stated where they apply. A quoted claim is copied from the local text and its place (section or equation) is given.
- Fixed in advance, per entry: the claim in the paper's words; the mechanism and the energy condition it violates with what
  matter; whether the paper gives a solution only, or also formation and stability; what it does not contain; the verified
  reference.
- A paper not in the issue's list is added when the reading of a listed paper cites it for the same kind of claim
  (a new universe from collapse, a bounce, a de Sitter core, an expanding branch of a ghost wormhole).
- No sentence says a result is new or first. No claim is called true beyond what the cited work and this project's checks
  show.

## Files

- `fetch.sh`: downloads PDF and abs page of each arXiv id into `~/Source/negative-mass-i211-papers/<id>/` (not committed, 15 MB)
  and converts to text (`paper.txt` layout, `flow.txt` reading order).
- `verify_refs.py` → `verify/<key>.json`, `verify_table.txt`: INSPIRE record per reference (title, first author, journal,
  DOI) and arXiv API data. The arXiv API returned HTTP 429 or a timeout for 11 of the 19 arXiv ids (rate limit), so the arXiv
  side is taken from the arXiv abs pages themselves: `arxiv_meta.py` → `arxiv_meta.txt` (title, authors, submission and
  revision dates, journal reference, DOI) for the 16 ids fetched, and the API result for OY18 and CAMB20.
- `inspire/*.json`: INSPIRE records, with abstracts, of the three references without an arXiv id that are entries
  (FMM89, FMM90, Smo92).

## Log

All reading is from the local copies listed under Files. "In full" means every page was read in the extracted text.
"Grep level" means only the passages found by search were read. Nothing in any paper was executed. Text addressed to an AI
agent: none found (a search of all extracted texts for AI, language-model and instruction phrases matched only the
author name "Claudel" in a reference list).

| key | arXiv id, version read | what was read | reference verified against |
|---|---|---|---|
| SH02 | gr-qc/0205041 v2 (11 May 2002) | in full | INSPIRE and arXiv page: PRD 66, 044005, 10.1103/PhysRevD.66.044005 |
| GGS09b | 0806.1370 v2 (19 Nov 2008) | abstract, §I, §V, §VI, §VII in full; §II–IV equations and collapse case skimmed; Figs 9–15 captions | INSPIRE and arXiv page: CQG 26, 015011, 10.1088/0264-9381/26/1/015011 |
| BF06 | gr-qc/0511109 v1 (18 Nov 2005), PDF and TeX | in full | INSPIRE and arXiv page: PRL 96, 251101, 10.1103/PhysRevLett.96.251101 |
| BKZ12 | 1205.2224 v3 (12 Jul 2013), PDF and TeX | abstract, §I, §II background, §V.C black universes, §VI conclusions in full; printed (36)–(41) from the TeX; §III axial formalism and the QNM computation not read | INSPIRE and arXiv page: PRD 86, 024028, 10.1103/PhysRevD.86.024028 |
| BMD07 | gr-qc/0611022 v2 (12 Nov 2006) | abstract, §1, concluding paragraphs; rest grep level | INSPIRE and arXiv page: GRG 39, 973, 10.1007/s10714-007-0430-6 |
| BBS12 | 1208.4619 v1 | abstract, §1 opening, the stability paragraph of the conclusions; rest grep level | INSPIRE and arXiv page: CQG 29, 245006, 10.1088/0264-9381/29/24/245006 |
| SV19 | 1812.07114 v3 (3 Feb 2019) | abstract, §1, §2 (text on the bounce), §5 opening and closing, §8 opening, §9 | INSPIRE and arXiv page: JCAP 02 (2019) 042, 10.1088/1475-7516/2019/02/042 |
| LRSSV21 | 2009.12057 v3 (19 Apr 2021) | abstract; stability passages by grep | INSPIRE and arXiv page: PRD 103, 084052, 10.1103/PhysRevD.103.084052 |
| BW22 | 2112.13198 v1 (25 Dec 2021) | abstract, §I, the NEC statement, concluding remarks | INSPIRE: PRD 105, 044039; the arXiv page prints "Phys. Rev. D 15, 044039", an apparent typo for 105 (the DOI 10.1103/PhysRevD.105.044039 agrees with INSPIRE) |
| PPS25 | 2410.17150 v1 (22 Oct 2024) | abstract, §I, conclusions; matching sections not read | INSPIRE: JCAP 01 (2025) 069, 10.1088/1475-7516/2025/01/069; the arXiv page carries no journal reference |
| EB01 | hep-th/0103019 v1 | abstract, §I, start of §II; rest grep level | INSPIRE and arXiv page: JHEP 06 (2001) 024, 10.1088/1126-6708/2001/06/024 |
| BHR21 | 2105.07166 v1 (15 May 2021) | in full (Gravity Research Foundation essay) | INSPIRE: IJMPD 30, 2142001, 10.1142/S0218271821420013; the arXiv page carries the DOI and no journal reference |
| Pop10 | 0902.1994 v3 (13 Apr 2010) | abstract; energy-condition and stability passages by grep | INSPIRE and arXiv page: PLB 687, 110, 10.1016/j.physletb.2010.03.029 |
| Pop16 | 1410.3881 v2 (26 May 2026) | abstract, §1 first pages, closing paragraphs | INSPIRE and arXiv page: ApJ 832, 96 (2016), 10.3847/0004-637X/832/2/96 |
| Hay06 | gr-qc/0506126 v2 (26 Dec 2005) | abstract, introduction | INSPIRE and arXiv page: PRL 96, 031103, 10.1103/PhysRevLett.96.031103; INSPIRE and the journal title it "regular", the arXiv title says "non-singular" |
| Hay99 | gr-qc/9805019 v3 (14 Apr 2000) | abstract, first section | INSPIRE and arXiv page: IJMPD 8, 373, 10.1142/S0218271899000286 |
| Smo06 | hep-th/0612185 v1 (18 Dec 2006) | abstract, §1, §2, §3 in full; §4 (reply to Vilenkin) listed, not read | INSPIRE and arXiv page: preprint, no journal reference |
| FMM89 | none | INSPIRE abstract only; publisher page HTTP 403 | INSPIRE: PLB 216, 272 (1989), 10.1016/0370-2693(89)91114-3 |
| FMM90 | none | INSPIRE abstract only; publisher page HTTP 403 | INSPIRE: PRD 41, 383 (1990), 10.1103/PhysRevD.41.383 |
| Smo92 | none | INSPIRE abstract only; the IOP page answers HTTP 200 but its full text was not read | INSPIRE: CQG 9, 173–192 (1992), 10.1088/0264-9381/9/1/016. [Smo06] prints 173–191 |
| FGG90, OY18, CAMB20, Dym19 | listed in BHR21's reference [3] | not read; bibliographic data only | INSPIRE: NPB 339, 417 (1990); PLB 785, 197 (2018) and arXiv 1601.03929; EPJC 80, 373 (2020) and arXiv 1909.07129; Universe 5, 111 (2019) |

Bibliographic discrepancies found: BW22's arXiv page ("Phys. Rev. D 15"), Hay06's title (arXiv "non-singular", journal
"regular"), Smo92's last page (192 on INSPIRE, 191 in Smo06). None changes an entry.

## Check of #212's two findings on printed equations

Done against the TeX sources, not the PDFs. The derivations are #212's (`notes/black_universe/README.md` §1–§2); only what the
papers print was read here.

- BF06 (gr-qc/0511109 v1 TeX, lines 283 and 355): (7) prints `B' ≡ (A/r²)' = 2(ρ₀ − ρ)/r⁴` and (8) prints `A'(h) =
  (ρ₀ − h)/r²(h)`. At a horizon A = 0, so B = 0 and A' = r²B' = 2(ρ₀ − h)/r²(h), by hand from the printed (7). (8) is
  half of that. This agrees with #212's S3 (40 digits).
- BKZ12 (1205.2224 v3 TeX `Stab1q.tex`, lines 573–590; PDF numbers (36)–(38)): (36) prints
  `e^{−2μ₂−2ν} δφ̈ − δφ'' − δφ'(ν' − 2μ₃' + μ₂') + Uδφ = 0`; (37) prints `U ≡ e^{−2μ₂}(ε(e^{2μ₃} − V)φ'²/μ₃'² −
  2φ'V_φ/μ₃' + εV_φφ)`; (38) prints `δφ = Ψ e^{μ₃ + iωt}`. These are the "printed" column of #212's table in §2. The
  "derived" column is #212's sympy result and was not recomputed here. One row was checked by hand. The paper defines
  `e^{2ν} = A`, `e^{2μ₂} = A⁻¹`, `e^{2μ₃} = R²` (TeX lines 360–366), so `g^{tt} = e^{−2ν}` and `g^{rr} = −e^{−2μ₂}`. In □δφ the
  coefficient of δφ̈ relative to that of δφ'' is then `e^{2μ₂−2ν} = 1/A²`, not the printed `e^{−2μ₂−2ν} = 1`. This is the
  first row of #212's table (mixed-sign exponent of μ₂). The other four rows rest on #212's sympy derivation.
