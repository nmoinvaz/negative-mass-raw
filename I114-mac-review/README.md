# I114-mac-review: the coordinator's review of #114 (the two capped rtol 1e-12 rows of #4, and the cap in `convergence.py`)

Machine: mac (the coordinator's Mac, macOS, Apple silicon), Python from `~/Source/negative-mass/.venv`.

Issue: https://github.com/nmoinvaz/negative-mass/issues/114

Under review: branch `wip/i114-convergence-cap` at f7b8e10 (2447e1c, 6e73456, f7b8e10), raw `I114-win` at af5d045d.
Merged into main locally as the coordinator's merge of that branch; RESULTS.md §3a conflicted with #187's update bullet
and was resolved by keeping both, with that bullet's "l = 6 still running" sentence replaced by a pointer to #198.

## What was checked

| check | how | result |
|---|---|---|
| the two values and their relative differences | `rel_diff.py` reads `../I114-win/*.partial.csv` with `json` only, no code of `convergence.py` | l = 5: 2.331e-9, l = 6: 3.251e-8, both D < 0, 66 results each, a `done` record and no `capped` or `died` record (`rel_diff.out`) |
| `rel_diff.py` can fail | `--mutate=sign` flips each rtol 1e-12 value | both rows FAIL, exit 1 (`rel_diff_mutate_sign.out`) |
| criterion 3: the outputs are the script's | `review.sh` regenerates both outputs on the Mac from copies of the stored partial files, nothing evaluated | both byte-identical to the committed files; the partial files are unchanged (`review.log`, `regen5.txt`, `regen6.txt`) |
| criterion 2: the cap and its control | `review.sh` reruns `ctl_cap` (`CAP_S=4`, l = 2, γ ∈ {1e-3, 40}) and `ctl_nocap` (`--mutate=nocap`) | `ctl_cap`: the γ = 40 row carries six "not completed" marks, γ = 1e-3 none, exit 0. `ctl_nocap`: no mark, exit 0, D at γ = 40 equal to win's to the printed digits (`ctl_cap.txt`, `ctl_nocap.txt`) |
| `review.sh` can fail | `--mutate=diff` changes one time in the exported l = 5 output before the comparison | "l=5 output DIFFERS", FAIL, exit 1 (`review_mutate_diff.log`) |
| the code change | read the diff of `convergence.py` | sound; notes below |

What the checks share with the work under review: `review.sh` runs `convergence.py` itself, so criteria 2 and 3 are a
rerun on another machine, not an independent implementation. `rel_diff.py` shares only the partial files.

## Notes on the code (not blocking)

- A worker that dies before it reports `start` is never seen by the loop in `evaluate`, which would then wait forever.
  Not met in any run.
- After a cap, `evaluate` respawns when the tasks left outnumber the workers that reported `start`, so a worker that is
  still building its problems can be doubled, briefly above `NPROC`. Harmless at `NPROC=1`.

## For #198

#198 is unblocked. `phase2/nonradial/taylor_drift.md` recommended task 2 sets #198's bar from the floor "before the
l = 6 value of #114 is compared". That value is now public in #114's closing comment and in RESULTS.md, so a bar set
from here on is not blind to it. This review did not write the crate comparison anywhere.

## Rerun

From this folder (`negative-mass-raw/I114-mac-review`), with the negative-mass checkout at `../../negative-mass`:

```
./review.sh
python3 rel_diff.py
```

`./review.sh --mutate=diff` and `python3 rel_diff.py --mutate=sign` are the planted failures; both exit 1.
