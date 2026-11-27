#!/bin/bash
# I206-mac: the Python exploration (I191's cases, degrees up to 9) under a grid of first orders, seeds 1 and 2 in parallel
# (two processes), then the analysis. usage: run_explore.sh <tag> <phis, comma separated>
# the logs <tag>_s1.log, <tag>_s2.log, <tag>_analyze.log, the rows and the dumped series go to the raw folder
TAG=$1
PHIS=$2
RAW=$HOME/Source/negative-mass-raw/I206-mac
PY=/private/tmp/claude-501/-Users-nathan-Source-negative-mass-i206-libs-multisolver/84294958-42d6-4032-9618-1096d90926ff/scratchpad/venv/bin/python
cd "$RAW/sys/explore" || exit 1
export DMAX=9 PHIS
(OUT=$RAW/${TAG}_s1 nice -n 10 $PY explore3.py 30 1 > $RAW/${TAG}_s1.log 2>&1; echo $? > $RAW/${TAG}_s1.rc) &
(OUT=$RAW/${TAG}_s2 nice -n 10 $PY explore3.py 60 2 > $RAW/${TAG}_s2.log 2>&1; echo $? > $RAW/${TAG}_s2.rc) &
wait
nice -n 10 $PY analyze_i206.py $RAW/${TAG}_s1_rows.json $RAW/${TAG}_s2_rows.json > $RAW/${TAG}_analyze.log 2>&1; echo $? > $RAW/${TAG}_analyze.rc
