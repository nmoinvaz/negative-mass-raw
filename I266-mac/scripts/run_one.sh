#!/bin/bash
# run_one.sh ROOT FAM B H : bisect p*_h, run the chain at delta = 1e-8, run the member pair, for one family member and h.
# ROOT is the folder that holds <tag>/h<H>/{pstar,chain,member}; logs, errs and rc go to ROOT/<tag>/h<H>/logs. B is "-" for family O.
# Never overwrites a log: a rerun gets the next number (.2, .3, ...).
ROOT=$1; FAM=$2; B=$3; H=$4
WT=$HOME/Source/negative-mass-i266/notes/wormhole_evolution
PY=$HOME/Source/negative-mass/.venv/bin/python
export NUMBA_NUM_THREADS=1
if [ "$FAM" = "O" ]; then TAG=O; BARG=""; else TAG=G_B$B; BARG="--B=$B"; fi
D=$ROOT/$TAG/h$H
mkdir -p $D/logs
cd $WT
for stage in pstar job member; do
  case $stage in pstar) out=pstar ;; job) out=chain ;; member) out=member ;; esac
  n=1; base=$D/logs/$out
  while [ -e $base.log ] || [ -e $base.$n.log ]; do n=$((n+1)); done
  [ -e $base.log ] && lg=$base.$n.log || lg=$base.log
  [ $n -gt 1 ] && [ ! -e $base.log ] && lg=$base.log
  nice -n 10 $PY settled_mass_b.py $stage --fam=$FAM $BARG --h=$H --out=$D/$out --pstar=$ROOT > $lg 2> ${lg%.log}.err
  rc=$?
  echo $rc > ${lg%.log}.rc
  if [ $rc -ne 0 ]; then echo "stage $stage failed rc=$rc ($lg)"; exit $rc; fi
done
echo "done $TAG h$H"
