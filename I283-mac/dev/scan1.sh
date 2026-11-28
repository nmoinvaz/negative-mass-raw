#!/bin/bash
# scan1.sh LANE: development scan at h = 0.02 over the first guesses of the two routes
cd $HOME/Source/negative-mass-raw/I283-mac/dev
export NUMBA_NUM_THREADS=1
PY=$HOME/Source/negative-mass/.venv/bin/python
if [ "$1" = "0" ]; then specs="0.1,3.0,0.35 0.1,3.0,0.7 0.1,3.0,1.0"; else specs="0.1,2.0,0.5 0.1,2.5,0.5 0.1,3.5,0.5 0.1,4.0,0.5"; fi
for s in $specs; do
  IFS=, read B xc w <<< "$s"
  nice -n 10 $PY devpoint.py $PWD/runs_dev $B $xc $w 0.02 > logs/dp_B${B}_xc${xc}_w${w}_h0.02.log 2> logs/dp_B${B}_xc${xc}_w${w}_h0.02.err
  echo "$s rc=$? $(grep -h '^RESULT' logs/dp_B${B}_xc${xc}_w${w}_h0.02.log | cut -c1-400)"
done
