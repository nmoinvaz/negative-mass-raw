#!/bin/bash
# mutlane.sh QUEUE LANE NLANES RAWROOT OUTDIR: runs `settled_mass_d56.py analyze --mutate=NAME --cases=CASES --skip=pl41,pfx` for the lines "NAME CASES [SKIP]" (SKIP defaults to pl41,pfx) of QUEUE with line number mod NLANES = LANE.
# Each log goes to OUTDIR/NAME.log (never overwritten: an existing log is moved aside), its exit code to OUTDIR/NAME.rc.
QUEUE=$1; LANE=$2; NL=$3; ROOT=$4; OUT=$5
SRC=$HOME/Source/negative-mass-i246/notes/wormhole_evolution
PY=$HOME/Source/negative-mass-venv314/bin/python
export OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p $OUT; cd $SRC || exit 1
awk -v l=$LANE -v nl=$NL '(NR-1)%nl==l' $QUEUE | while read name cases skip; do
  [ -z "$skip" ] && skip=pl41,pfx
  [ -z "$name" ] && continue
  [ -f $OUT/$name.log ] && mv $OUT/$name.log $OUT/$name.log.aborted.$(date +%s)
  /usr/bin/time -v -o $OUT/$name.time timeout 10800 $PY settled_mass_d56.py analyze --raw=$ROOT --cases=$cases --skip=$skip --mutate=$name > $OUT/$name.log 2> $OUT/$name.err
  echo $? > $OUT/$name.rc
  echo "done $name rc=$(cat $OUT/$name.rc) $(tail -1 $OUT/$name.log | cut -c1-200)"
done
