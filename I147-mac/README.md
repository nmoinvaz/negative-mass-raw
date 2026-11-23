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

| file | what |
|---|---|
| `rerun/` | `zerilli_derivation.py` (exit 0, 32 PASS) and `zerilli_derivation_controls.py` (34 OK, 1 MISS, exit 1) at 990ae7c on the Mac at nice 10, with the per-run control logs |
| `ind147_run1.py`, `.txt` | the independent check, run 1 (`ind147.py` is the same version) |
| `ind147_mut_*.txt` | its 4 mutations |

**Rerun.** The unmutated output equals the committed one apart from timing lines. The controls rows equal rpi5's apart
from timings: 33 of 34 pairs on target, `fsign_bg` the one MISS (first FAIL PL.O.3).

**Code review of the diff 3400e74..990ae7c.** Every new behavior is behind `mut('NAME')`. The unmutated path changes by
an identity wrapper (`route2_h` returns h unless `x_odd` or `x_gauge` is on) and one renamed variable in E.4. `e5a_det0`
and `d5_ah0` override the value their checks read, as #147 says; the other 14 break the quantity their check tests.
Example: `grr_trace` fails E.2 on the "no second derivative in δG_rr" conjunct alone.

**ind147 run 1** (exit 0):

| criterion | run 1 |
|---|---|
| N1 | baseline OK with 32 PASS; 34 pairs, 33 OK; the one MISS is `fsign_bg` at PL.O.3 |
| N2 | #143's 18 pairs unchanged; the 16 new pairs equal the table at 5e9657b |
| N3 | all 32 PASS ids are targets; the 16 new pairs' first FAIL on the Mac is their target |
| N4 | 5e9657b (14:20:33 −08:00) precedes 7a44d73 (14:24:55) and the raw commits bea1290 and c75b6ea |
| N5 | no bare use of the 16 names; `mut` is `name in _MUT`, filled only from `--mutate=` |
| N6 | 105 non-timing lines equal |

Re-solve, one pair by hand: `grr_trace` on the Mac fails E.2 with "no second derivatives in tr, tx, rx True and in
delta G_rr False", the conjunct it targets.

| mutation | exit | failed | target met |
|---|---|---|---|
| `miss2` | 1 | N1 | yes |
| `retarget` | 1 | N2 | yes |
| `drop_pair` | 1 | N3 | yes |
| `leak` | 1 | N5 | yes |
