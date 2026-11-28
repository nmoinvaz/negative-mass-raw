#!/bin/bash
# run_one.sh ROOT H E|pstar K : for one h and one bracket k of the ensemble (k = 0 is the run of record), either bisect p*_h (E = "pstar") or run the pair p*_h -/+ 10^-E (member).
# ROOT/runs (k = 0) or ROOT/runs_k<K> holds G_B0.02/h<H>/{pstar,e<E>/{member,logs}}. Never overwrites a log: a rerun gets the next number (.2, .3, ...).
ROOT=$1; H=$2; E=$3; K=${4:-0}
WT=$HOME/Source/negative-mass-i291/notes/wormhole_evolution
PY=$HOME/Source/negative-mass/.venv/bin/python
export NUMBA_NUM_THREADS=1
RD=$ROOT/runs; [ "$K" != "0" ] && RD=$ROOT/runs_k$K
D=$RD/G_B0.02/h$H
if [ "$E" = "pstar" ]; then LD=$D/logs; base=$LD/pstar.log; else D=$D/e$E; LD=$D/logs; base=$LD/member.log; fi
mkdir -p $LD
cd $WT
lg=$base; n=1
while [ -e $lg ]; do n=$((n+1)); lg=${base%.log}.$n.log; done
if [ "$E" = "pstar" ]; then
  nice -n 10 $PY throat_tail.py pstar --h=$H --k=$K --out=$D/pstar > $lg 2> ${lg%.log}.err
else
  nice -n 10 $PY throat_tail.py member --h=$H --e=$E --k=$K --out=$D/member --pstar=$RD > $lg 2> ${lg%.log}.err
fi
rc=$?
echo $rc > ${lg%.log}.rc
if [ $rc -ne 0 ]; then echo "stage failed rc=$rc ($lg)"; exit $rc; fi
echo "done h$H $E k$K"
