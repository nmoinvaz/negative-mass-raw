#!/bin/bash
# lane2.sh QUEUE LANE NLANES OUTROOT: as lane.sh, with per-job extra arguments: QUEUE lines are "n fam k delta suffix [extra args...]" (suffix "-" for none).
QUEUE=$1; LANE=$2; NL=$3; OUT=$4
SRC=$HOME/Source/negative-mass-i246/notes/wormhole_evolution
RAW=$HOME/Source/negative-mass-raw/I246-dh610
PY=$HOME/Source/negative-mass-venv314/bin/python
export OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd $SRC || exit 1
awk -v l=$LANE -v nl=$NL '(NR-1)%nl==l' $QUEUE | while read n fam k delta suffix extra; do
  [ -z "$n" ] && continue
  [ "$suffix" = "-" ] && suffix=""
  D=$((n+2))
  tag="D${D}_${fam}_k${k}_d${delta}${suffix}"
  dir=$OUT/$tag
  if [ -d "$dir" ]; then
    if [ -f "$dir/summary.json" ] && [ -f "$dir/job.rc" ] && [ "$(cat $dir/job.rc)" = "0" ]; then echo "skip $tag (done)"; continue; fi
    mv "$dir" "${dir}_aborted_$(date +%s)"
  fi
  mkdir -p "$dir"
  date +%s > $dir/job.start
  /usr/bin/time -v -o $dir/job.time timeout 10800 $PY settled_mass_d56.py job --n=$n --fam=$fam --k=$k --delta=$delta --out=$dir --pstar=$RAW/runs $extra > $dir/job.log 2> $dir/job.err
  echo $? > $dir/job.rc
  echo "done $tag rc=$(cat $dir/job.rc)"
done
