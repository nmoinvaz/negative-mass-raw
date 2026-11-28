#!/bin/bash
# dev_set.sh LANE: the development set at h = 0.01 and 0.005 (bracket scan inside devpoint.py, or the given bracket) for the selected route (5.0, 0.7) and #305's X2 reproduction point (from its stored bracket). Logs never overwritten.
RAW=$HOME/Source/negative-mass-raw/I313-mac
cd $RAW/dev
export NUMBA_NUM_THREADS=1
PY=$HOME/Source/negative-mass/.venv/bin/python
SET=$RAW/dev/set_a
mkdir -p $RAW/dev/logs
if [ "$1" = "0" ]; then
  jobs="runs 0.09431 5.0 0.7 0.005|runs 0.0394 5.0 0.7 0.005|runs 0.0768 5.0 0.7 0.01"
else
  jobs="runs 0.0768 5.0 0.7 0.005|runs_rep 0.1695 4.0 1.5 0.005 0.0064 0.0128|runs 0.0394 5.0 0.7 0.01|runs 0.09431 5.0 0.7 0.01"
fi
IFS='|' read -ra JL <<< "$jobs"
for j in "${JL[@]}"; do
  set -- $j
  sub=$1; shift
  tag=a_${sub}_B$1_xc$2_w$3_h$4
  lg=$RAW/dev/logs/$tag.log; n=1
  while [ -e $lg ]; do n=$((n+1)); lg=$RAW/dev/logs/$tag.$n.log; done
  t0=$(date +%s)
  nice -n 10 $PY $RAW/scripts/devpoint.py $SET/$sub "$@" > $lg 2> ${lg%.log}.err
  echo $? > ${lg%.log}.rc
  echo "$(date '+%F %T') lane $LANE: $j rc=$(cat ${lg%.log}.rc) $(( $(date +%s) - t0 )) s"
done
