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
| C1 | every quote of `quotes.txt` occurs verbatim in its source TeX (`check_quotes.py`); every `@also` version contains the same text; every `@absent` version lacks it | after removing comments and collapsing whitespace the quote is a substring of the equally normalized TeX; TeX markup kept | `--mutate=quote` alters the first word of the first quote; `also` checks the first `@also` quote against another paper; `absent` points the first `@absent` at its own source |
| C2 | every quote also occurs in the PDF text | a fragment squashed to lower-case alphanumerics occurs on one page of `pdftotext` (or of the cache `pdftext/`); numbers in `@pdfnum` occur on that page | `--mutate=pdf` checks the first quote against another paper's PDF |
| C3 | every sentence of the proposed text in `proposal.md` cites at least one existing quote id; each table cell, diff bullet and entry equals its joined sentences | exit 0 | `--mutate=cite`, `dangling`, `cell`, `bullet`, `entry` |
| C4 | sha256 of every file in `sha256sums.txt` equals the file on disk (downloads, TeX, the two I152 citing sources and PDFs, the `pdftext/` cache) | exit 0 | `--mutate=sha` |
| C5 | every number in a proposed sentence occurs in a cited quote or, for `CALC1`, in a `VALUE` line of `recompute_run1.log` | exit 0 | `--mutate=number` |
| C6 | every double-quoted string in a proposed sentence occurs in a cited quote | exit 0 | `--mutate=quoted` |
| C7 | a claim that a phrase is absent from a paper (for example "oscillating growth") is checked by a search of the TeX and the PDF text, not by reading | `@lacks` terms (plain, or `re:` regex) occur in none of the record's sources; its `@has` term occurs in all (the search can find things) | `--mutate=lacks` adds the record's `@has` term to its `@lacks` list |
| C8 | the section label of every quote is computed from the TeX headings (`\section`, `\subsection`, run-in `\prlsec`, `\noindent{\textbf{}}`, `\paragraph`) | the quote's `@loc` starts with the computed label | `--mutate=loc` |
| C9 | the diff block of `proposal.md` is the diff that `make_diff.py` derives from the sentences and the stored base note (`src/critical_ghost_dffa582.md`, the note at main dffa582); `patch --dry-run` applies it; a sentence tagged {KEEP} occurs in the base note | exit 0 | `--mutate=diff` (an extra word in the first derived line), `anchor` (shifts an anchor line, so its prefix check fails), `keep` |
| C10 | every double-quoted string in the narrative sections of `proposal.md` (answers, what is not settled, what is not carried) occurs in some record | exit 0 | `--mutate=answer` |
| CALC1 | `recompute_jc.py` recomputes J_c/A, the mode crossing and the normalization of J from the printed tables (a recompute, labelled as such) | P1 to P6 in its docstring, fixed before the first run (the Fig. 6 readings were taken before the script ran; the area formula was chosen after seeing that the plot matched it) | `--mutate=delta`, `cross`, `area`, `w`, `table`, `min` |

`run_controls.sh` runs C0 to CALC1 and every control and exits non-zero if any control behaves wrongly (`SILENT` for a
mutation that exits 0, `NOT RUN` for a check that could not run). `check_quotes.py` exits 3, not 1, when neither
`pdftotext` nor the `pdftext/` cache is available, so a missing tool is never mistaken for a control firing. Without
`proposal.md` the proposal controls (`cite` to `answer`) exit 1 because the file is absent, which is not a result; with it, each
fires on its named target (`controls/check_<name>.log`).

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

Scripts and data written in steps 2 and 3 (all run with `python3 -I`, stdlib only except `recompute_jc.py` P5, which needs sympy):

| file | what |
|---|---|
| `quotes.txt` | 105 records (quotes and absence records), the data; `quotes.md` is generated from it by `check_quotes.py --write` |
| `check_quotes.py` | C1 to C10; 18 `--mutate=` controls |
| `recompute_jc.py`, `recompute_run1.log` | CALC1: J_c/A and the mode crossing from the printed tables, normalization of J, minimal surface; 6 controls |
| `make_diff.py` | derives the unified diff of `proposal.md` against the base note; `--check` is C9 |
| `proposal.md` | the proposed text (40 sentences with quote ids), the diff, the answers, what is not settled |
| `run_controls.sh`, `run_controls.out` | runs every check and every control (26 runs, all `ok`); logs in `controls/` |
| `src/critical_ghost_dffa582.md` | `notes/critical_ghost.md` at main dffa582, the base of the diff (pinned in `sha256sums.txt`) |
| `pdftext/` | `pdftotext` output of each PDF, pinned in `sha256sums.txt`, used only when `pdftotext` is missing (the Mac) |

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

Two facts for the notes. [BGKKKN26] names 2607.18399 alongside 2510.11406 for "this merger" (its Introduction, paragraph 5, second sentence), but
[SN26b]'s bibliography has only 2510.11406. The abs pages of 2301.05243 (v2) and 2510.11406 (v2) say the later version
matches the published one; the journal references the notes would print for them are verified by INSPIRE
(`dl/inspire/<id>.json`), not by the publisher.

## Step 2 and 3 findings (what the sources say; answers and the proposed text follow in step 4)

The four papers are read in full (both versions of 2301.05243, 2510.11406 and 2607.18399 where they exist; the TeX
diffs between versions were read). 105 records in `quotes.txt` (`quotes.md` has locations, PDF pages and TeX lines). The
predictions above against the bodies:

| prediction | result |
|---|---|
| 1 both halves of S04 are in 2403.08387; 2301.05243 may treat one asymmetry only | both halves are in both papers. 2301.05243 also covers several C (Table 1: C = 0 to 1.0; "for every value of C we have studied", L06). Wrong about 2301.05243. "Nearly symmetric" is not in either text: the second mode is "independent of C" (M12) and is shown only for C = 0, 0.05, 0.1, 0.2 (L14, L15, M13, M14) |
| 2 S05's conjecture is hedged; "merge" may not occur in 2301.05243 or 2403.08387 | wrong. "merge and disappear" is in 2301.05243 Sec. 5 and 6 (L17, L18) and in 2403.08387 Sec. I, V, VI (M02, M16, M19), in both versions of 2301.05243. "beyond the reliable range of the quadratic approximation" is [SN26b]'s paraphrase: the sources say the crossing "is indicating a deficiency of the applied quadratic approximation" (L16, M17) and, in the same paper, that second order "should be excellent" for "most of the range J/A < J_c/A" (M10) |
| 3 2510.11406 conjectures the complex pair by analogy; the two papers disagree | confirmed. 2510.11406: "whereas one might be tempted to conjecture that the radial instability disappears at the critical value, this is not the case" (H12) and "can only be confirmed by a non-perturbative study" (H22). 2403.08387 (Mar 2024): the instability disappears (M16, M19). 2510.11406 is later (v1 13 Oct 2025); as read, it neither mentions nor withdraws the earlier "disappear" conjecture (read, not searched). 2607.18399 (Jul 2026) conjectures that the 4D radial instability "will therefore be relaxed" (N09), not that it disappears |
| 4 "reaches zero only in the extremal limit" is in 2510.11406; 2607.18399 adds no radial statement | half wrong. Neither paper says "only". Closest: "while not yet fully radially stable" (H17), "the instability does not seem to completely vanish as long as M/r_T<1" (N05, subcritical), omega_I "tends to zero very quickly in the limit" (N04, H16). 2607.18399 has a radial subsection per class (Sec. 5.2.3, 5.3.3, 5.4.3) with the same merger statement (N06) |
| 5 the 33 % is the zero of the C = 1 second-order rate in 2403.08387 | wrong. "33" as a percentage occurs in none of the seven TeX sources (N13, N14, N16). Printed: crossing "around J/A = 0.013, slightly above 30 %" for C = 0, 0.05, 0.1, 0.2 (L13, M15); "around 1/3" for the merger (H18). Recompute (`recompute_run1.log`): the crossing is 32.6 to 33.0 % of 1/(8 pi); the zero of the main-mode rate at C = 1 is 41.9 % (J_c/A = 0.0167, which reproduces Fig. 6 of 2403.08387 within 0.0001 at C = 0, 1.0, 1.4), not 33 % |

Other facts found, for the notes:

- 2510.11406 Eq. (6) as printed (omega_I proportional to (1 - M/r_T)^-3.1) diverges at M/r_T = 1, against its own text
  and Fig. 2 inset (tau_0). 2607.18399 prints omega_I ~ (1 - M/r_T)^3.1 in Sec. 5.2.3 (N04) and tau ~ (1 - M/r_T)^-3.1 in
  Sec. 5.3.3 (N05). A printing slip in 2510.11406, not a disagreement of the physics (H09 note).
- 2510.11406 v1 and v2 differ in wording: v1 says the wormholes "become effectively stabilized" (H24) and its abstract says
  "long-lived" (H23); v2 says "characteristic time of the instability", adds that the bifurcation "is a novel result that
  has not been observed in" [GGS09c]'s paper (H15; v1 had "see also") and that other instabilities may creep up (H25).
- 2607.18399 v1 and v2 agree on every quote used (`@also N1`).
- 2607.18399 Sec. 5.1.2 and its abstract report a nonradial polar instability of the static (massive) Ellis wormholes,
  fundamental l = 2 branch, for M/r_T > about 0.3 (N01, N11). The note's §1.1 says "one unstable mode" for the static
  family; that statement is about radial perturbations and stands, but the nonradial one is not in the note.
- 2510.11406's supercritical charged wormholes have two purely imaginary unstable radial modes at small mass (H11); the
  note's §1.1 charged row says "one growing mode ... numerical evidence for super-critical" [GGS09c]. What [GGS09c] found
  is not read here.
- 2301.05243 normalizes with the area of the throat A "(obtained in second order)" (L04) and prints the static
  A = 4 pi r0^2 exp(pi C / 2 r0) for "the throat ... located at r = 0" (L19). 2403.08387 says that for C != 0 the throat
  is "shifted to one of the sides as seen by determining the minimal surface" (M04). The metric it prints has the minimum
  at r = C/2, with a different area. Fig. 6 of 2403.08387 reproduces with the r = 0 area (`recompute_run1.log`).
- J is read off at infinity (M05) and w -> 2 J / r^3 for r -> infinity (recompute, P5), which is G = 1; neither paper
  states G (M21, N13). The limit J/A -> 1/(8 pi) is that of the extremal Kerr black hole (L05, M07).

## Step 4: proposal and checks

`proposal.md` holds 40 sentences (17 for a new §1.1 row on slowly rotating 4D wormholes, 6 for the charged row, 14 in two
bullet groups of the §1.2 [SN26b] block, 3 for the "Not read" entry), the derived diff, the answers to Q1 to Q4 with quote
ids, what the papers do not settle and what is not carried. `check_quotes.py` exits 0: 105 records, 40 sentences, 28
numbers and 40 quoted strings checked against their cited records, 37 quoted strings of the narrative sections checked
against all records, 1 {KEEP} sentence found in the base note, the diff applied by `patch --dry-run`. It also exits 0 on
a machine without `pdftotext`, from the `pdftext/` cache (tested here with `PATH` stripped). `run_controls.sh`: 26 runs,
26 `ok` (`run_controls.out`): 18 mutations of `check_quotes.py` and 6 of `recompute_jc.py` each exit 1 on their named
target. No control was silent.

Slips of this session, none in a posted number: the first `run_controls.sh` run used the system python, which has no sympy,
so the `recompute_plain` run reported `NOT RUN` (exit 3) and was rerun with the venv python (`PY=`); a first draft of
`quotes.txt` had a placeholder record (X05) that was replaced before the first commit; six PDF fragments crossed a page
break or a footnote and were shortened or split with `||`; a `@has` control used a case-sensitive match until the
`Kerr` record failed; the recompute's first table parser tried to read the header row as numbers. The README of step 1
said "paragraph 6" for the sentence of [BGKKKN26] that names both charged papers; it is paragraph 5, second sentence
(quote G01, C8 computes the section label only). An untracked folder `src/2403.08387v1/figs/` from the extraction is not
committed; nothing in it is quoted (the figure readings were taken from the PDF).

## Status

| step | state |
|---|---|
| 1 ids verified, sources fetched | done (8aac3b8) |
| 2 slow-rotation papers read, `quotes.md` | done (1380379) |
| 3 charged-wormhole papers read | done (same `quotes.txt`) |
| 4 `proposal.md`, final checks and controls | done |
