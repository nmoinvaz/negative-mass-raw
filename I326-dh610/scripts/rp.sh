#!/bin/bash
# usage: rp.sh TAG B HK A T   control RP: one `fate` run of a stored point (amplitude A, stored event time T) at X = T + 2, in runs/rp_TAG (run1.sh: nothing overwritten).
RAW=${RAW:-$HOME/Source/negative-mass-raw/I326-dh610}
TAG=$1; B=$2; HK=$3; A=$4; T=$5
X=$(python3 -c "print(round($T + 2.0, 3))")
$RAW/scripts/run1.sh runs/rp_$TAG 7200 @PY@ drift_b6_long.py fate --B=$B --hk=$HK --A=$A --tcap=$X --out=@RAW@/runs/rp_$TAG/fate.json
