#!/bin/bash
# run_muts.sh RAWDIR OUTDIR LANE NLANES BASELOG : analyze --mutate=NAME for every mutation of settled_mass_route3.py; lanes take every NLANES-th;
# logs, errs, rc go to OUTDIR (absolute; reruns get .2, .3, ...). RAWDIR holds runs/.
RAWDIR=$1; OUT=$2; LANE=$3; NL=$4; BASE=$5     # BASE: the unmutated analysis's log (its [FAIL] lines are the baseline)
WT=$HOME/Source/negative-mass-i295/notes/wormhole_evolution
PY=$HOME/Source/negative-mass/.venv/bin/python
export NUMBA_NUM_THREADS=1
mkdir -p $OUT
cd $WT
names=$($PY - <<PYEOF
import sys, importlib
sys.argv = ["x"]
m = importlib.import_module("settled_mass_route3")
print(" ".join(m.MUTATIONS))
PYEOF
)
k=0
for mu in $names; do
  if [ $((k % NL)) -eq $LANE ]; then
    n=1; lg=$OUT/$mu.log
    while [ -e $lg ]; do n=$((n+1)); lg=$OUT/$mu.$n.log; done
    t0=$(date +%s)
    nice -n 10 $PY settled_mass_route3.py analyze --raw=$RAWDIR --baseline=$BASE --mutate=$mu > $lg 2> ${lg%.log}.err
    echo $? > ${lg%.log}.rc
    echo "$(date '+%F %T') lane $LANE: $mu rc=$(cat ${lg%.log}.rc) $(( $(date +%s) - t0 )) s: $(grep '^mutation ' $lg | tail -1 | cut -c1-300)"
  fi
  k=$((k+1))
done
