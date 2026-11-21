#!/bin/bash
# Launcher for I126-rpi5 (negative-mass issue 126) on rpi5.   Usage: [LIMIT=SECONDS] ./launch_I126.sh LISTFILE
# LISTFILE has one job name per line (controls.txt, z_boxes.txt, pilot.txt, w_boxes.txt). jobs.txt holds the unmodified
# output of `python collect_i126.py --jobs`, one "job|script|arguments|source folder" per line. A job runs, from
# phase2/nonradial of the worktree, as
#   nice -n 10 $PY -u <script> <arguments> --cachedir=$RAW/cache
# with stdout and stderr in <job>.log and its exit status in done/<job>.rc. A job with done/<job>.rc is skipped.
# LIMIT (seconds) puts `timeout LIMIT` in front of the python command (exit status 124); it is the pilot's stop condition.
# A second copy on the same LISTFILE shares the queue (flock on queue.lock, position in qpos.<LISTFILE>).
# A job that died without a .rc is run again by starting the launcher again; the cache keeps finished points.
HERE=$(cd "$(dirname "$0")" && pwd)
export RAW=$HERE NR=$HOME/Source/negative-mass-i126/phase2/nonradial PY=$HOME/Source/negative-mass-venv314/bin/python
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
  script=$(echo "$line" | cut -d'|' -f2); args=$(echo "$line" | cut -d'|' -f3)
  echo "$(date -Is) start $name: $script $args --cachedir=$RAW/cache${LIMIT:+ (timeout $LIMIT s)}" >> "$RAW/queue.log"
  nice -n 10 ${LIMIT:+timeout "$LIMIT"} "$PY" -u "$script" $args --cachedir="$RAW/cache" > "$RAW/$name.log" 2>&1; rc=$?
  echo $rc > "$RAW/done/$name.rc"
  echo "$(date -Is) end $name rc=$rc" >> "$RAW/queue.log"
done
