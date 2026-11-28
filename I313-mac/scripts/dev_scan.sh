#!/bin/bash
# dev_scan.sh LANE: development tuning at h = 0.02 of the new candidates (x_c w), B tuned to gamma_1 = 0.012, 0.048, 0.075 (devtune.py, #295's). Logs never overwritten.
RAW=$HOME/Source/negative-mass-raw/I313-mac
cd $RAW/dev
export NUMBA_NUM_THREADS=1
PY=$HOME/Source/negative-mass/.venv/bin/python
if [ "$1" = "0" ]; then cands="4.0,1.0 4.5,1.0 5.0,0.7 5.0,1.0 4.0,1.5"; else cands="2.0,0.35 2.5,0.25 3.0,0.25 2.0,0.25"; fi
for c in $cands; do
  IFS=, read xc w <<< "$c"
  lg=logs/tune_xc${xc}_w${w}_h0.02.log; n=1
  while [ -e $lg ]; do n=$((n+1)); lg=logs/tune_xc${xc}_w${w}_h0.02.$n.log; done
  nice -n 10 $PY $RAW/scripts/devtune.py $RAW/dev/runs_dev $xc $w 0.02 0.012 0.048 0.075 > $lg 2> ${lg%.log}.err
  echo $? > ${lg%.log}.rc
  echo "$(date '+%F %T') lane $1: xc $xc w $w rc=$(cat ${lg%.log}.rc)"
done
