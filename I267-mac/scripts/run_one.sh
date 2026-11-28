#!/bin/bash
# run_one.sh ROOT H E|pstar : for one h, either bisect p*_h (E = "pstar") or run the chain (job) and the pair (member) at delta = 10^-E.
# ROOT holds G_B0.1/h<H>/{pstar,e<E>/{chain,member,logs}}. Never overwrites a log: a rerun gets the next number (.2, .3, ...).
ROOT=$1; H=$2; E=$3
WT=$HOME/Source/negative-mass-i267/notes/wormhole_evolution
PY=$HOME/Source/negative-mass/.venv/bin/python
export NUMBA_NUM_THREADS=1
D=$ROOT/G_B0.1/h$H
if [ "$E" = "pstar" ]; then stages="pstar"; LD=$D/logs; else stages="job member"; D=$D/e$E; LD=$D/logs; fi
mkdir -p $LD
cd $WT
for stage in $stages; do
  case $stage in pstar) out=pstar ;; job) out=chain ;; member) out=member ;; esac
  lg=$LD/$out.log; n=1
  while [ -e $lg ]; do n=$((n+1)); lg=$LD/$out.$n.log; done
  if [ "$E" = "pstar" ]; then
    nice -n 10 $PY settled_mass_member.py pstar --h=$H --out=$D/pstar > $lg 2> ${lg%.log}.err
  else
    nice -n 10 $PY settled_mass_member.py $stage --h=$H --e=$E --out=$D/$out --pstar=$ROOT > $lg 2> ${lg%.log}.err
  fi
  rc=$?
  echo $rc > ${lg%.log}.rc
  if [ $rc -ne 0 ]; then echo "stage $stage failed rc=$rc ($lg)"; exit $rc; fi
done
echo "done h$H $E"
