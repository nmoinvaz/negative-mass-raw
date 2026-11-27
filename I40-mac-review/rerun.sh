#!/bin/bash
# The coordinator's rerun of #40: 13 of its 26 jobs with the runner's flags, two lanes, nice 10, one thread each.
# usage: rerun.sh LANE (1 or 2). Writes rerun/<job>/ (job.log, job.err, job.rc, job.time). Nothing is overwritten.
LANE=$1
R=$HOME/Source/negative-mass-raw/I40-mac-review
WT=$HOME/Source/negative-mass-r40/notes/wormhole_evolution
PY=$HOME/Source/negative-mass/.venv/bin/python
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
if [ "$LANE" = 1 ]; then
  JOBS="4:S:0.005: 4:G:0.01:--ed 4:O:0.01:--ed 5:S:0.00353553:--ed 4:S:0.02: 4:G:0.02:"
else
  JOBS="4:G:0.005: 4:O:0.005: 6:S:0.0025:--ed 4:S:0.01:--ed 5:S:0.00707107: 6:S:0.005: 4:O:0.02:"
fi
cd "$WT" || exit 2
for jb in $JOBS; do
  IFS=: read D fam h ed <<< "$jb"
  dir=$R/rerun/D${D}_${fam}_h$(printf '%.6g' $h)
  [ -e "$dir/job.rc" ] && { echo "$dir has a result; not overwriting"; continue; }
  mkdir -p "$dir"
  echo "start $(date -u +%FT%TZ) lane $LANE" > "$dir/job.start"
  /usr/bin/time -l nice -n 10 $PY threshold.py job --D=$D --family=$fam --h=$h --out="$dir" --cons --stall $ed > "$dir/job.log" 2> "$dir/job.err"
  echo "rc=$?" > "$dir/job.rc"
done
echo "lane $LANE done $(date -u +%FT%TZ)"
