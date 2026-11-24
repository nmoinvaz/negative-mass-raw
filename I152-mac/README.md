# I152-mac: the coordinator's review of #152's reading of the rotating-wormhole stability papers

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/152. Reviewed raw `I152-rpi5` at 7ef70af (a reading task; no
branch, no file in the repository).

## Rerun of the runner's scripts

`bash run_controls.sh` in a copy of `I152-rpi5` (`rerun/`), so that its `controls/` logs do not overwrite rpi5's. The
copy is the whole folder at 7ef70af. Output: `rerun_run_controls.txt` and `rerun/controls/`.

## Sources, fetched by the coordinator

On 2026-11-24, from arxiv.org with a generic client, into a new empty scratch folder outside this repository:
- the e-prints and PDFs of 1309.2448v1, 2610.38659v1, 2610.29941v1 and 2610.29941v2;
- the arXiv API record for the three ids;
- the three abs pages.

The e-prints were unpacked each into its own new folder. They are not committed again: their sha256 is listed in
`fetch.txt`, and ind152 compares them with rpi5's `sha256sums.txt`.

## Independent check `ind152.py` (criteria written before its first run)

ind152 imports nothing from `I152-rpi5`. Its TeX normalization is its own: comments dropped, `\cite{…}` removed, TeX
commands dropped with their braces kept as content, `$`, braces, `~` and line breaks removed, whitespace collapsed. It
reads the data folder passed as its argument and runs with `python3 -I` from this folder.

Shared with #152: the proposed text (closing comment 7135193323 and `proposal.md`), from which the strings and numbers
below are copied, and the four source files, which are the same bytes (P0).

| id | criterion |
|---|---|
| P0 | the 4 TeX files from the coordinator's own fetch have the sha256 that `I152-rpi5/sha256sums.txt` lists; so do the 4 PDFs |
| P1 | arXiv metadata (API and abs pages), compared case-insensitively. [BGKKKN26] = 2610.38659: title "Exact rotating wormholes in five dimensions and their exceptional-point instability"; authors Blázquez-Salcedo, González-Romero, Khoo, Kleihaus, Kunz, Navarro Moreno, in that order; v1 28 Oct 2026. [SN26b] = 2610.29941: title "Rotation slows the instability of Ellis-Bronnikov wormholes"; authors Shirokov, Nachevsky; v2 6 Nov 2026. [DFKKR13] = 1309.2448: title "Rotating wormholes in five dimensions"; authors Dzhunushaliev, Folomeev, Kleihaus, Kunz, Radu; journal ref Phys. Rev. D 88, 124028 (2013) |
| P2 | each double-quoted string of the proposed text occurs in its source, normalized. From [DFKKR13]: "within the type of modes investigated", "may stabilize wormholes", "no new unstable modes of a different type appear", "vanishes when the angular momentum exceeds some critical value". From [BGKKKN26]: "not stabilization", "correctly located the merger". From [SN26b] v2: "evidence of prolonged radial stability", "bound growth only over that span", "without identifying a second eigenmode" |
| P3 | each number of the proposed text occurs as a token in its source. [DFKKR13]: 0.10063, 0.1381. [BGKKKN26]: 0.100628, 2.190024, 0.48717, the strings `10^{-6}` and `(|J|/A-0.5)^6`. [SN26b] v2: 150, 28, 81, 5.4, 13.3, 24, 32, 33, 28.8, 0.2, 80.8, `128/192/256`, D90, D75, D80, and `G=c=1` (spaces ignored) |
| P4 | v1 against v2 of [SN26b]: "no evidence of instability" and "addresses the four-dimensional stability question" occur in v1 and not in v2 |
| P5 | re-solve of the runner's recompute, with the coordinator's own code from [BGKKKN26] Eqs. (8) and (19)–(22), typed from the TeX: \|J\|/A = \|κ\|(e^{2a}e^{q})^{1/2}/(32πG p^{3/2}) at the throat, with p = 1/2, s = πλ/4, e^{2a} = sin²s/(1 − cos s), e^{q} = λ sin s/(2(1 − cos s)), κ² = −λ³cos s/(16 sin³s). With 4πG = 1 the values at λ = 2.190024, 2.059523, 3.948341 round to the printed 0.100628, 0.05475, 0.48717, and λ → 4 gives 1/2 within 1e-6. With G = 1 none of the three rounds to its printed value. Neither 2610.38659 nor 1309.2448 contains `G=1`, `4\pi G=1`, `8\pi G=1` or `16\pi G=1` (spaces ignored) |

Mutations, each must exit 1 with its target failing:

| mutation | change | target |
|---|---|---|
| `sha` | one hex digit of the expected main.tex sha256 flipped | P0 |
| `author` | Khoo → Kho | P1 |
| `date` | v2 date 7 Nov 2026 | P1 |
| `quote` | "not stabilization" → "no stabilization" | P2 |
| `number` | 0.100628 → 0.100629 | P3 |
| `v1v2` | v1 and v2 swapped in P4 | P4 |
| `G1` | G = 1 used as the passing normalization | P5 |

## Results

(after the runs)
