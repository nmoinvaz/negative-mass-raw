#!/bin/zsh
# development runs of l = 4, 5, 6, one process at a time (launched detached; each devrun keeps its own log, err, rc)
cd /Users/nathan/Source/negative-mass-i187/phase2/nonradial
/Users/nathan/Source/negative-mass-raw/I187-mac/devrun.sh rows_RA4 /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --rows --only=RA4 --jsonl-dir=/Users/nathan/Source/negative-mass-raw/I187-mac/dev_jsonl
/Users/nathan/Source/negative-mass-raw/I187-mac/devrun.sh rows_RA5_CAP5 /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --rows --only=RA5,CAP5 --jsonl-dir=/Users/nathan/Source/negative-mass-raw/I187-mac/dev_jsonl
/Users/nathan/Source/negative-mass-raw/I187-mac/devrun.sh rows_RA6_CAP6 /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --rows --only=RA6,CAP6 --jsonl-dir=/Users/nathan/Source/negative-mass-raw/I187-mac/dev_jsonl
