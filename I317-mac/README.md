# I317-mac: corrected eps = 1e-2 reading (V3), frozen, then predicting #305's X1 to X3 (analysis of stored runs only)

Machine: the coordinator's Mac (Apple M5, macOS, shared). Issue: https://github.com/nmoinvaz/negative-mass/issues/317
Code: `notes/wormhole_evolution/settled_mass_blind.py` in nmoinvaz/negative-mass, branch `wip/i317-corrected-blind`
(`freeze` and `analyze`; `--part=dev|record`, `--mutate=`, `--baseline=`). No evolution runs: the stored runs of #266, #267, #283, #295 and #305 are read.

Stage 0 (this stub, before any analysis log): the folder layout.

- `dev/`: development runs. They read only the fifteen training members of #296 and B = 0, never #305's X1 to X3 and never #295's N1 to N3 (a guard in the script raises).
- `record/`: the runs of record, after the frozen file is committed and pushed.
- `frozen_v3.json`: the frozen coefficients (written by `freeze --part=record`, never overwritten).
- `scripts/`: drivers.

Stage 1 (method, bar, mutations and their development effects) follows below once the development runs are done.
