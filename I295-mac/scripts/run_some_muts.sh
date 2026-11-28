#!/bin/bash
# run_some_muts.sh RAWDIR OUTDIR BASELOG NAME...: the named mutations, one after the other (the full set is run_muts.sh).
RAWDIR=$1; OUT=$2; BASE=$3; shift 3
WT=$HOME/Source/negative-mass-i295/notes/wormhole_evolution
PY=$HOME/Source/negative-mass/.venv/bin/python
export NUMBA_NUM_THREADS=1
mkdir -p $OUT; cd $WT
for mu in "$@"; do
  n=1; lg=$OUT/$mu.log
  while [ -e $lg ]; do n=$((n+1)); lg=$OUT/$mu.$n.log; done
  nice -n 10 $PY settled_mass_route3.py analyze --raw=$RAWDIR --baseline=$BASE --mutate=$mu > $lg 2> ${lg%.log}.err
  echo $? > ${lg%.log}.rc
  echo "$(date '+%F %T') $mu rc=$(cat ${lg%.log}.rc): $(grep '^mutation ' $lg | tail -1 | cut -c1-300)"
done
