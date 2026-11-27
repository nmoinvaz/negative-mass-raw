#!/bin/bash
# usage: run_members.sh RES outdir c1 c2 ...
RES=$1; OUT=$2; shift; shift
PY=/home/nathan/Source/negative-mass-venv314/bin/python
for c in "$@"; do
  /usr/bin/time -v $PY /home/nathan/Source/negative-mass-i212/notes/black_universe/stability.py count $c --res=$RES --out=$OUT/member_${c}_${RES}.json > $OUT/member_${c}_${RES}.log 2>&1
  echo "c=$c exit $?" >> $OUT/${RES}_status.txt
done
