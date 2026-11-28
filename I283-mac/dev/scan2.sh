#!/bin/bash
# scan2.sh LANE: development tuning of B for the targets gamma_1 = 0.012, 0.048, 0.075 at h = 0.02 for candidate widths (lane 0) and centres (lane 1)
cd $HOME/Source/negative-mass-raw/I283-mac/dev
export NUMBA_NUM_THREADS=1
PY=$HOME/Source/negative-mass/.venv/bin/python
if [ "$1" = "0" ]; then cands="3.0,0.7 3.0,1.0 3.0,0.35"; else cands="3.5,0.5 2.5,0.5 4.0,0.5"; fi
for c in $cands; do
  IFS=, read xc w <<< "$c"
  nice -n 10 $PY devtune.py $PWD/runs_dev $xc $w 0.02 0.012 0.048 0.075 > logs/tune_xc${xc}_w${w}_h0.02.log 2> logs/tune_xc${xc}_w${w}_h0.02.err
  echo "$c rc=$?"; grep -h '^TUNED' logs/tune_xc${xc}_w${w}_h0.02.log
done
