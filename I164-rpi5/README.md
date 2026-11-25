# I164-rpi5: reading of the slow-rotation and charged-wormhole merger papers behind §1.1's rotating row

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64). Worktree `~/Source/negative-mass-i164` (wip/i164-slow-rotation at main
dffa582, read-only). Issue: https://github.com/nmoinvaz/negative-mass/issues/164

Task: read arXiv:2301.05243, 2403.08387, 2510.11406 and 2607.18399 in full, and say what each contains about (a) the merger
of the unstable radial modes and its continuation and (b) the numbers [SN26b] attributes to them, then propose wording for
`notes/critical_ghost.md` §1.1 (the rotating row), §1.2 (the [SN26b] block) and §6 ("Not read"). Reading only. The note is
the coordinator's; this folder holds the proposal. Written before any paper body was read, except the abs pages (read to
verify the ids). Sections "Files" and "Id verification" are filled from the fetch.

## Questions

| id | question |
|---|---|
| Q0 | Is each of the four ids the paper that [BGKKKN26] (arXiv:2610.38659) and [SN26b] (arXiv:2610.29941) cite? Title, authors, versions, journal reference |
| Q1 | S04 (I152 `quotes.md`): is "the static unstable mode weakens, with a positive O(J²) correction for every asymmetry, while for nearly symmetric wormholes a second unstable mode grows out of a static zero mode" in the slow-rotation papers, and in what words? |
| Q2 | S05: is "the authors conjecture that the modes merge beyond the reliable range of the quadratic approximation and the instability disappears" in the source? Does it say "disappears"? Merge of what two modes? |
| Q3 | S06 and A10: is "in the charged analogue the merged modes continue as a complex pair (oscillating growth), and the growth rate reaches zero only in the extremal limit" in the charged-wormhole papers? In which paper, which sector (radial or nonradial)? |
| Q4 | Where do [SN26b]'s "33 % from second-order perturbation theory" and its C ≤ 0.2 crossings come from in the slow-rotation papers, and in what normalization of the angular momentum? |

## How each answer is checked

- Every answer is a quote from a fetched source with its section, equation, figure or table number, in `quotes.md`
  (quote id, source file, location, question). What I recall about a paper is not a source. A claim with no quote is listed
  as unsupported, never softened into the proposed text.
- Locations come from the TeX (`\section`, `\label`, equation order) and are cross-checked against `pdftotext` of the PDF,
  because the PDF is what the reader sees. Where a paper has no section numbers the location says so.
- A contradiction with [BGKKKN26] or [SN26b], or between two papers, is reported as found. Versions that differ are both read.
- Numbers (critical J, percentages) are copied, not recomputed, unless the paper gives the inputs. A recompute is labelled.
- I152's quote format and `check_quotes.py` are the model; this folder's `check_quotes.py` is an adaptation.

## Checks (each can fail; the control is a mutation that must exit 1)

| id | check | pass criterion | control |
|---|---|---|---|
| C0 | the four ids are the cited papers (`verify_ids.py`) | abs-page title, authors, journal reference and version list agree with the entries in [BGKKKN26]'s and [SN26b]'s bibliographies and with what was fetched | `--mutate=title`, `author`, `jref`, `version` |
| C1 | every quote of `quotes.txt` occurs verbatim in its source TeX (`check_quotes.py`) | after removing comments and collapsing whitespace the quote is a substring of the equally normalized TeX; TeX markup kept | `--mutate=quote` alters one word of one quote |
| C2 | every quote also occurs in the PDF text | a fragment squashed to lower-case alphanumerics occurs on one page of `pdftotext`; numbers in `@pdfnum` occur on that page | `--mutate=pdf` checks one quote against another paper's PDF |
| C3 | every sentence of the proposed text in `proposal.md` cites at least one existing quote id; each table cell and diff bullet equals its joined sentences | exit 0 | `--mutate=cite`, `dangling`, `cell`, `bullet` |
| C4 | sha256 of every file in `sha256sums.txt` equals the file on disk | exit 0 | `--mutate=sha` |
| C5 | every number in a proposed sentence occurs in a cited quote | exit 0 | `--mutate=number` |
| C6 | every double-quoted string in a proposed sentence occurs in a cited quote | exit 0 | `--mutate=quoted` |
| C7 | a claim that a phrase is absent from a paper (for example "disappears") is checked by a search of the TeX, not by reading | `@absent` quotes and `@lacks` strings: the TeX must not contain them | `--mutate=absent` points the check at a source that contains the string |

`run_controls.sh` runs C0 to C7 and every control and exits non-zero if any control behaves wrongly. A control that is
silent on its named target is reported as silent.

## Predictions, written before the papers' bodies were read (a miss is reported, not adjusted)

The abs pages' abstracts were read to verify the ids, so these concern the bodies.
1. S04's two halves (positive O(J²) correction for every asymmetry; second unstable mode from a static zero mode for nearly
   symmetric wormholes) are both in 2403.08387's body. 2301.05243 (6 pages in v1) is a short letter that gives the first
   indication and may treat one asymmetry only.
2. S05's "conjecture" is hedged in the body of 2403.08387. Its abstract says the unstable mode "reaches zero and then
   disappears", which is about the single static mode of the generic case; the merger of two modes is the nearly symmetric case.
   The word "merge" may not occur in 2301.05243 or 2403.08387, and then S05 is a paraphrase by [SN26b], not a quote.
3. The abstract of 2510.11406 says "By analogy, we conjecture an analogous behavior for rotating chargeless wormholes" (the
   merged pair continues with opposite real parts). If the body of 2403.08387 predicts disappearance and 2510.11406 predicts
   a complex pair, the two papers by overlapping authors contradict each other, and [SN26b]'s S05 and S06 describe
   different conjectures. Which is later in time is a fact to report.
4. "the growth rate reaches zero only in the extremal limit" is in 2510.11406, about the supercritical radial modes as the
   charge approaches its extremal value. 2607.18399 is a nonradial paper and adds no radial merger statement beyond what
   it cites.
5. The 33 % is the zero of the second-order rate, in 2403.08387, for the family C = 1 of [SN26b], in units where J is scaled
   by the throat quantities of that paper, not [SN26b]'s A/8π. Its conversion is [SN26b]'s ("on this axis").

## Files

Fetched from arXiv on 2026-11-25 (UTC) with `fetch.sh` (log `fetch.log`; every request HTTP 200). Each id was fetched at
every version its abs page lists, with an explicit version suffix. TeX was extracted from the e-prints with `tar` into
`src/` (only `*.tex`; the REVTeX class sample `reftest4-1.tex` in the 2301.05243v1 e-print is not the paper and is not kept).
`dl/` holds the downloads as fetched (e-print, PDF, abs page, INSPIRE record). Full hashes: `sha256sums.txt`. The two
I152 source files that hold the citing bibliographies are listed there with relative paths into `../I152-rpi5/`.

| paper, version | e-print | TeX (committed) | PDF | PDF pages |
|---|---|---|---|---|
| arXiv:2301.05243v1 | `dl/2301.05243v1/eprint` 70989514…26d2 | `src/2301.05243v1/sr_ellis.tex` 7fe120b0…4584 | `dl/2301.05243v1/pdf` f04bf21e…c908 | 6 |
| arXiv:2301.05243v2 | `dl/2301.05243v2/eprint` 95fde33d…b5e5 | `src/2301.05243v2/paper8.tex` 1a9e39ab…4e94 | `dl/2301.05243v2/pdf` 7eaf1ccc…db17 | 10 |
| arXiv:2403.08387v1 | `dl/2403.08387v1/eprint` 1b050a57…9c98 | `src/2403.08387v1/main.tex` 76d0082e…6f12 | `dl/2403.08387v1/pdf` 39fdc77e…8fb1 | 27 |
| arXiv:2510.11406v1 | `dl/2510.11406v1/eprint` 8d2c1dd3…459c | `src/2510.11406v1/main.tex` 5d35cbaf…fa53 | `dl/2510.11406v1/pdf` f17bcfc2…be9e | 5 |
| arXiv:2510.11406v2 | `dl/2510.11406v2/eprint` cb0cf5c5…540d | `src/2510.11406v2/main.tex` f9584b53…7938 | `dl/2510.11406v2/pdf` 3ea82328…b609 | 5 |
| arXiv:2607.18399v1 | `dl/2607.18399v1/eprint` 24a20b0c…d498 | `src/2607.18399v1/main.tex` 2ac76504…1f2b | `dl/2607.18399v1/pdf` 7889d02c…2ecc | 35 |
| arXiv:2607.18399v2 | `dl/2607.18399v2/eprint` 361344ba…d9c3 | `src/2607.18399v2/main.tex` ab125007…b26d | `dl/2607.18399v2/pdf` 4096743d…a41f | 35 |

## Id verification (Q0, C0)

`python3 -I verify_ids.py` exits 0 (`verify_ids.log`); its four mutations each exit 1 (`verify_ids_<name>.log`; `jref` fires on
3 of 4 ids, since the abs page of 2301.05243 shows no journal reference). All four ids are right: each abs page's title,
authors and, where shown, journal reference equal what [BGKKKN26] (arXiv:2610.38659, its TeX comments) and [SN26b]
(arXiv:2610.29941 v2, its `\bibitem` entries) print.

| id | title (abs page) | authors | versions | journal reference | cited by |
|---|---|---|---|---|---|
| 2301.05243 | Are slowly rotating Ellis-Bronnikov wormholes stable? | B. Azad, J. L. Blázquez-Salcedo, F. S. Khoo, J. Kunz | v1 12 Jan 2023, v2 23 Nov 2023 ("equations added, minor typos corrected, results unchanged, matches published version") | none on the abs page; Phys. Lett. B 848, 138349 (2024) in both citing papers and in INSPIRE (recid 2623092) | [BGKKKN26] `Azad:2023iju`, [SN26b] `azad2023` |
| 2403.08387 | Radial perturbations of Ellis-Bronnikov wormholes in slow rotation up to second order | same four | v1 13 Mar 2024 | Phys. Rev. D 109, 124051 (2024) (abs page, INSPIRE recid 2768383) | [BGKKKN26] `Azad:2024axu`, [SN26b] `azad2024` |
| 2510.11406 | Radial perturbations of charged wormholes (v1 title: "Charged wormholes can be long-lived") | J. L. Blázquez-Salcedo, L. M. González-Romero, F. S. Khoo, J. Kunz, P. Navarro Moreno | v1 13 Oct 2025, v2 13 Mar 2026 ("added references, results unchanged, matches published version") | Phys. Lett. B 875, 140335 (2026) (abs page, INSPIRE recid 3068528) | [BGKKKN26] `Blazquez-Salcedo:2025dit`, [SN26b] `blazquez2025` |
| 2607.18399 | Nonradial perturbations of static charged wormholes | same five | v1 20 Jul 2026, v2 8 Oct 2026 ("added references, matches published version") | Phys. Rev. D 114, 084019 (2026) (abs page, INSPIRE recid 3182213) | [BGKKKN26] `Blazquez-Salcedo:2026cps` only |

Two facts for the notes. [BGKKKN26] names 2607.18399 alongside 2510.11406 for "this merger" (its Introduction, paragraph 6), but
[SN26b]'s bibliography has only 2510.11406. The abs pages of 2301.05243 (v2) and 2510.11406 (v2) say the later version
matches the published one; the journal references the notes would print for them are verified by INSPIRE
(`dl/inspire/<id>.json`), not by the publisher.

## Status

| step | state |
|---|---|
| 1 ids verified, sources fetched | done |
| 2 slow-rotation papers read, `quotes.md` | |
| 3 charged-wormhole papers read | |
| 4 `proposal.md`, checks, controls | |
