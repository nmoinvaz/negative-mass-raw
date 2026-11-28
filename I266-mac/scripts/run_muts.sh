#!/bin/bash
# run_muts.sh RAWDIR OUTDIR LANE NLANES [SCRIPT] : analyze --mutate=NAME for every mutation of SCRIPT (default settled_mass_b.py); lanes take every NLANES-th;
# logs, errs, rc go to OUTDIR (reruns get .2, .3, ...)
RAWDIR=$1; OUT=$2; LANE=$3; NL=$4; SMB=${5:-settled_mass_b.py}
WT=$HOME/Source/negative-mass-i266/notes/wormhole_evolution
PY=$HOME/Source/negative-mass/.venv/bin/python
export NUMBA_NUM_THREADS=1
mkdir -p $OUT
cd $WT
MOD=${SMB%.py}
names=$($PY - <<PYEOF
import sys, importlib
sys.argv = ["x"]
b = importlib.import_module("$MOD")
print(" ".join(b.MUTATIONS))
PYEOF
)
k=0
for m in $names; do
  if [ $((k % NL)) -eq $LANE ]; then
    n=1; lg=$OUT/$m.log
    while [ -e $lg ]; do n=$((n+1)); lg=$OUT/$m.$n.log; done
    t0=$(date +%s)
    nice -n 10 $PY $SMB analyze --raw=$RAWDIR --mutate=$m > $lg 2> ${lg%.log}.err
    echo $? > ${lg%.log}.rc
    echo "$(date '+%F %T') lane $LANE: $m rc=$(cat ${lg%.log}.rc) $(( $(date +%s) - t0 )) s: $(grep '^mutation ' $lg | tail -1)"
  fi
  k=$((k+1))
done
