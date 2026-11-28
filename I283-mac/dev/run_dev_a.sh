#!/bin/bash
# run_dev_a.sh LANE: development set at the six selected points and the reproduction point, h = 0.01 and 0.005 (bracket scan, bisection, chain, pair), into runs_a/runs
cd $HOME/Source/negative-mass-raw/I283-mac/dev
export NUMBA_NUM_THREADS=1
PY=$HOME/Source/negative-mass/.venv/bin/python
if [ "$1" = "0" ]; then specs="0.07905,3.0,1.0 0.1543,3.0,1.0 0.1909,3.0,1.0 0.1,3.0,0.5"; else specs="0.0393,4.0,0.5 0.07726,4.0,0.5 0.09576,4.0,0.5"; fi
for h in 0.01 0.005; do
  for s in $specs; do
    IFS=, read B xc w <<< "$s"
    t0=$(date +%s)
    nice -n 10 $PY devpoint.py $PWD/runs_a/runs $B $xc $w $h > logs/a_B${B}_xc${xc}_w${w}_h${h}.log 2> logs/a_B${B}_xc${xc}_w${w}_h${h}.err
    echo "$(date '+%F %T') lane $1: $s h $h rc=$? $(( $(date +%s) - t0 )) s"
  done
done
