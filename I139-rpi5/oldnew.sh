#!/bin/bash
# A2 without --csv: the script before and after the option, --lmax 60, three runs one after the other (from phase2/dg_proof).
RAW=$HOME/Source/negative-mass-raw/I139-rpi5
PY=$HOME/Source/negative-mass-venv314/bin/python
mkdir -p "$RAW/oldnew"
$PY -u "$RAW/run_old.py" --lmax 60 > "$RAW/oldnew/old_lmax60.txt" 2> "$RAW/oldnew/old_lmax60.err"; echo $? > "$RAW/oldnew/old_lmax60.rc"
$PY -u threshold_isolation.py --lmax 60 > "$RAW/oldnew/new_lmax60.txt" 2> "$RAW/oldnew/new_lmax60.err"; echo $? > "$RAW/oldnew/new_lmax60.rc"
$PY -u threshold_isolation.py --lmax 60 --csv="$RAW/oldnew/new_lmax60.csv" > "$RAW/oldnew/new_lmax60_csv.txt" 2> "$RAW/oldnew/new_lmax60_csv.err"; echo $? > "$RAW/oldnew/new_lmax60_csv.rc"
