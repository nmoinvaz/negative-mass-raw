#!/bin/bash
# Gated queue worker of I123-rpi5 (copied from I126-rpi5's launch_I126_gated.sh).   Usage: [LIMIT=SECONDS] ./launch_I123.sh LISTFILE
# jobs.txt has one `job|arguments of zerilli_zeros.py` per line (the output of `collect_i121.py --jobs`); a job's log is
# <job>.log and its exit code done/<job>.rc. Before every job it checks, under one lock shared by all gated workers, how
# many of this task's zerilli_zeros.py processes run:
#   none         start at once (the first process);
#   one          start only while the 15-minute load average is below 4 (the second process);
#   two or more  wait.
# A wait is logged in queue.log when it begins, and the start line gives the load. Checked once a minute.
HERE=$(cd "$(dirname "$0")" && pwd)
export RAW=$HERE NR=$HOME/Source/negative-mass-i123/phase2/nonradial PY=$HOME/Source/negative-mass-venv314/bin/python
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
  script=zerilli_zeros.py; args=$(echo "$line" | cut -d'|' -f2)
  exec 9> "$RAW/gate.lock"; waited=0
  while true; do
    flock 9
    others=$(pgrep -fc "^$PY -u (winding2|zerilli_zeros)"); l15=$(cut -d' ' -f3 /proc/loadavg)
    if [ "$others" -eq 0 ]; then why=""; break
    elif [ "$others" -eq 1 ] && awk -v l="$l15" 'BEGIN{exit !(l < 4)}'; then why="15-min load $l15 < 4: "; break; fi
    flock -u 9
    [ $waited -eq 0 ] && echo "$(date -Is) waiting to start $name: $others of this task's processes running, 15-min load $l15 (needs one process and load < 4)" >> "$RAW/queue.log"
    waited=1; sleep 60
  done
  echo "$(date -Is) ${why}start $name: $script $args --cachedir=$RAW/cache${LIMIT:+ (timeout $LIMIT s)}" >> "$RAW/queue.log"
  nice -n 10 ${LIMIT:+timeout "$LIMIT"} "$PY" -u "$script" $args --cachedir="$RAW/cache" > "$RAW/$name.log" 2>&1 9>&- &
  pid=$!; sleep 3; flock -u 9; exec 9>&-
  wait $pid; rc=$?
  echo $rc > "$RAW/done/$name.rc"
  echo "$(date -Is) end $name rc=$rc" >> "$RAW/queue.log"
done
