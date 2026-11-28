#!/bin/bash
# run_one.sh ROOT B XC W H LO HI : for one route point (B, xc, w) at one h: bisect p*_h inside the bracket (LO, HI), run the chain (job) and the pair (member).
# ROOT holds <tag>/h<H>/{pstar,chain,member,logs}, tag = R_B<B>_xc<XC>_w<W>. Never overwrites a log: a rerun gets the next number (.2, .3, ...).
ROOT=$1; B=$2; XC=$3; W=$4; H=$5; LO=$6; HI=$7
WT=$HOME/Source/negative-mass-i283/notes/wormhole_evolution
PY=$HOME/Source/negative-mass/.venv/bin/python
export NUMBA_NUM_THREADS=1
cd $WT
TAG=$($PY settled_mass_route.py tag --route=$B,$XC,$W | tail -1)
D=$ROOT/$TAG/h$H
LD=$D/logs
mkdir -p $LD
for stage in pstar job member; do
  case $stage in pstar) out=pstar ;; job) out=chain ;; member) out=member ;; esac
  lg=$LD/$out.log; n=1
  while [ -e $lg ]; do n=$((n+1)); lg=$LD/$out.$n.log; done
  if [ "$stage" = "pstar" ]; then
    nice -n 10 $PY settled_mass_route.py pstar --route=$B,$XC,$W --h=$H --out=$D/pstar --bracket=$LO,$HI > $lg 2> ${lg%.log}.err
  else
    nice -n 10 $PY settled_mass_route.py $stage --route=$B,$XC,$W --h=$H --out=$D/$out --pstar=$ROOT > $lg 2> ${lg%.log}.err
  fi
  rc=$?
  echo $rc > ${lg%.log}.rc
  if [ $rc -ne 0 ]; then echo "stage $stage failed rc=$rc ($lg)"; exit $rc; fi
done
echo "done $TAG h$H"
