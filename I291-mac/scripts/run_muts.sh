#!/bin/bash
# run_muts.sh DATA OUTDIR LANE NLANES : every mutation of MUTS (one per line of mut_list.txt next to this script), analysis of DATA with --mutate=NAME, log to OUTDIR/NAME.log (a rerun gets the next number).
DATA=$1; OUT=$2; LANE=$3; NL=$4; SD=$(cd $(dirname $0) && pwd)
WT=$HOME/Source/negative-mass-i291/notes/wormhole_evolution
PY=$HOME/Source/negative-mass/.venv/bin/python
export NUMBA_NUM_THREADS=1
mkdir -p $OUT
cd $WT
k=0
while read name; do
  if [ $((k % NL)) -eq $LANE ]; then
    lg=$OUT/$name.log; n=1
    while [ -e $lg ]; do n=$((n+1)); lg=$OUT/$name.$n.log; done
    nice -n 10 $PY throat_tail.py analyze --raw=$DATA --mutate=$name > $lg 2> ${lg%.log}.err
    echo $? > ${lg%.log}.rc
    echo "$(date '+%F %T') lane $LANE: $name rc=$(cat ${lg%.log}.rc): $(grep '^mutation' $lg | cut -c1-300)"
  fi
  k=$((k+1))
done < $SD/mut_list.txt
