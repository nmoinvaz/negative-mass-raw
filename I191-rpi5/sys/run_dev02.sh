#!/bin/bash
# dev_02: the randomized exploration of dev_00 with fit degrees up to 9 (cells with more unknowns), same cases
cd "$(dirname "$0")/explore" || exit 1
PY=$HOME/Source/negative-mass-venv314/bin/python
RAW=$HOME/Source/negative-mass-raw/I191-rpi5
export DMAX=9
$PY explore3.py 30 1 > $RAW/dev_02_explore3_d9_s1.log 2>&1; echo $? > $RAW/dev_02_explore3_d9_s1.rc
mv rows_d9_1.json $RAW/dev_02_rows_d9_1.json
$PY explore3.py 60 2 > $RAW/dev_02_explore3_d9_s2.log 2>&1; echo $? > $RAW/dev_02_explore3_d9_s2.rc
mv rows_d9_2.json $RAW/dev_02_rows_d9_2.json
$PY analyze2.py $RAW/dev_02_rows_d9_1.json $RAW/dev_02_rows_d9_2.json > $RAW/dev_02_analyze2.log 2>&1; echo $? > $RAW/dev_02_analyze2.rc
