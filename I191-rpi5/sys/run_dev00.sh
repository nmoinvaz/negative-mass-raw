#!/bin/bash
# dev_00: the design exploration of the estimators (python, mpmath), rerun with its logs kept. Cases here are NOT the planted suite.
cd "$(dirname "$0")/explore" || exit 1
PY=$HOME/Source/negative-mass-venv314/bin/python
RAW=$HOME/Source/negative-mass-raw/I191-rpi5
for n in explore1 explore2 probe; do
  $PY $n.py > $RAW/dev_00_$n.log 2>&1; echo $? > $RAW/dev_00_$n.rc
done
$PY explore3.py 30 1 > $RAW/dev_00_explore3_s1.log 2>&1; echo $? > $RAW/dev_00_explore3_s1.rc
mv rows_1.json $RAW/dev_00_rows_1.json
$PY explore3.py 60 2 > $RAW/dev_00_explore3_s2.log 2>&1; echo $? > $RAW/dev_00_explore3_s2.rc
mv rows_2.json $RAW/dev_00_rows_2.json
$PY analyze2.py $RAW/dev_00_rows_1.json $RAW/dev_00_rows_2.json > $RAW/dev_00_analyze2.log 2>&1; echo $? > $RAW/dev_00_analyze2.rc
