#!/bin/bash
# Rerun 2 of the two D = 5 jobs with the runner's h (the strings its job.log records).
R=$HOME/Source/negative-mass-raw/I40-mac-review
WT=$HOME/Source/negative-mass-r40/notes/wormhole_evolution
PY=$HOME/Source/negative-mass/.venv/bin/python
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
cd "$WT" || exit 2
for jb in 0.0070710678118654745: 0.0035355339059327372:--ed; do
  IFS=: read h ed <<< "$jb"
  dir=$R/rerun_2/D5_S_h$(printf '%.6g' $h)
  [ -e "$dir/job.rc" ] && { echo "$dir has a result; not overwriting"; continue; }
  mkdir -p "$dir"
  /usr/bin/time -l nice -n 10 $PY threshold.py job --D=5 --family=S --h=$h --out="$dir" --cons --stall $ed > "$dir/job.log" 2> "$dir/job.err"
  echo "rc=$?" > "$dir/job.rc"
done
echo "rerun 2 done $(date -u +%FT%TZ)"
