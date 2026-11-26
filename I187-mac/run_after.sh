#!/bin/zsh
# after the default-mode rerun (run_18): the two diagnostics on the rows of record, one process at a time
until [ -f /Users/nathan/Source/negative-mass-raw/I187-mac/run_18_default_mode_rerun.rc ]; do sleep 15; done
cd /Users/nathan/Source/negative-mass-i187/phase2/nonradial
/Users/nathan/Source/negative-mass-raw/I187-mac/runrec.sh diag_gap_vs_gamma /Users/nathan/Source/negative-mass/.venv/bin/python /Users/nathan/Source/negative-mass-raw/I187-mac/diag_gap_vs_gamma.py jsonl
/Users/nathan/Source/negative-mass-raw/I187-mac/runrec.sh diag_f64_vs_dd /Users/nathan/Source/negative-mass/.venv/bin/python /Users/nathan/Source/negative-mass-raw/I187-mac/diag_f64_vs_dd.py jsonl
