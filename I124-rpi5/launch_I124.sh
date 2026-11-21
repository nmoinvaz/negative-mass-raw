#!/bin/bash
# Launcher for I124-rpi5 (negative-mass issue 124) on rpi5.   Usage: ./launch_I124.sh LISTFILE
# LISTFILE has one job name per line (controls.txt, pilot.txt, boxes.txt). jobs.txt maps a name to "name|arguments of
# zerilli_zeros.py" (the output of collect_i121.py --jobs --only=3a). A job runs, from phase2/nonradial of the worktree, as
#   nice -n 10 $PY -u zerilli_zeros.py <arguments> --cachedir=$RAW/cache
# with stdout and stderr in <name>.log and its exit status in done/<name>.rc. A job with done/<name>.rc is skipped.
# A second copy on the same LISTFILE shares the queue (flock on queue.lock, position in qpos.<LISTFILE>).
# A job that died without a .rc is run again by starting the launcher again; the cache keeps finished points.
HERE=$(cd "$(dirname "$0")" && pwd)
export RAW=$HERE NR=$HOME/Source/negative-mass-i124/phase2/nonradial PY=$HOME/Source/negative-mass-venv314/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export LIST=$(basename "$1")
cd "$NR" || exit 2
next() {
  flock "$RAW/queue.lock" bash -c '
    cd "$RAW"; n=$(cat "qpos.$LIST" 2>/dev/null || echo 0)
    while name=$(sed -n "$((n+1))p" "$LIST"); [ -n "$name" ]; do
      n=$((n+1))
      [ -f "done/$name.rc" ] && continue
      echo $n > "qpos.$LIST"; echo "$name"; exit 0
    done; echo $n > "qpos.$LIST"'
}
while name=$(next); [ -n "$name" ]; do
  line=$(grep "^$name|" "$RAW/jobs.txt") || { echo "$(date -Is) no job $name in jobs.txt" >> "$RAW/queue.log"; continue; }
  args=${line#*|}
  echo "$(date -Is) start $name: zerilli_zeros.py $args --cachedir=$RAW/cache" >> "$RAW/queue.log"
  nice -n 10 "$PY" -u zerilli_zeros.py $args --cachedir="$RAW/cache" > "$RAW/$name.log" 2>&1; rc=$?
  echo $rc > "$RAW/done/$name.rc"
  echo "$(date -Is) end $name rc=$rc" >> "$RAW/queue.log"
done
