# I147-mac: the coordinator's review of #147's 16 new mutations of zerilli_derivation.py

Machine: macOS (the coordinator's Mac, arm64), Python 3.14, sympy 1.14.0, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/147. Reviewed branch `wip/i147-zerilli-mutations` at 990ae7c,
raw `I147-rpi5` at c75b6ea (pre-registration at 5e9657b).

## Independent check `ind147.py` (criteria written before its first run)

ind147 checks the bookkeeping of the controls, from files only. It shares no code with `zerilli_derivation*.py` or the
library. It reads: the Mac rerun's unmutated output and controls output; the committed `zerilli_derivation_output.txt`;
the controls driver's `PAIRS` list (parsed with `ast`, not imported); the table of `I147-rpi5/README.md` at 5e9657b
(`git show`); and the source of `zerilli_derivation.py` at 990ae7c. Raw commit times come from `git log`.

| id | criterion | kind |
|---|---|---|
| N1 | Mac controls: the baseline line is OK with 32 PASS, there are 34 pair lines, 33 OK, and exactly one MISS, `fsign_bg` with first FAIL PL.O.3 | parse |
| N2 | the driver's 16 new pairs (after #143's 18) equal the pre-registered table at 5e9657b in name, target and exit code, and #143's 18 pairs are unchanged from 3400e74 | parse |
| N3 | every one of the 32 check ids that the unmutated run prints as PASS is the target of at least one of the 34 pairs, and each new pair's first FAIL on the Mac equals its target | parse |
| N4 | 5e9657b's commit time is earlier than the code commit 7a44d73 and than every later `I147-rpi5` commit | git |
| N5 | in `zerilli_derivation.py` at 990ae7c, each of the 16 names occurs only inside `mut('NAME')`, in the `XFLIP` table, in the docstring or in comments; `mut` is `name in _MUT`, and `_MUT` is filled only from `--mutate=` | source scan |
| N6 | the Mac unmutated output equals the committed `zerilli_derivation_output.txt` apart from the `# [ … s]` timing lines | diff |

Mutations of ind147, each must exit 1 with its target failing: `miss2` (one OK pair read as MISS; N1), `retarget` (one
pre-registered target changed in memory; N2), `drop_pair` (one new pair removed from the parsed list; N3), `leak` (a
bare occurrence of `ds_sign` added to the scanned source in memory; N5).

## Results
