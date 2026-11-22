#!/bin/bash
# Gated queue worker of I117-rpi5.   Usage: [LIMIT=SECONDS] ./launch_I117.sh LISTFILE
# LISTFILE has one job name per line. jobs.txt has one "job|script|arguments" per line. A job runs, from
# phase2/nonradial of the worktree, as
#   nice -n 10 [timeout LIMIT] $PY -u <script> <arguments> --cachedir=$RAW/cache > $RAW/<job>.log 2>&1
# and its exit status goes to done/<job>.rc (a job with a .rc file is skipped). Before taking a job, under one lock shared
# by all workers of this folder, the worker counts this task's running winding2.py / zerilli_zeros.py processes:
#   none         take the next job at once (the first process);
#   one          take it only while the 15-minute load average is below 4 (the second process);
#   two or more  wait.
# The gate is tested before the job is taken, so a waiting worker holds no job. A wait is logged in queue.log when it
# begins and the start line gives the load. Checked once a minute. Env overrides for tests: PY, NR.
HERE=$(cd "$(dirname "$0")" && pwd)
export RAW=$HERE NR=${NR:-$HOME/Source/negative-mass-i117/phase2/nonradial} PY=${PY:-$HOME/Source/negative-mass-venv314/bin/python}
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
LIST=$(basename "$1")
cd "$NR" || exit 2
mkdir -p "$RAW/done" "$RAW/cache"
peek() {  # "n name" of the next job without a done file, from line qpos+1 of the list
  local n name
  n=$(cat "$RAW/qpos.$LIST" 2>/dev/null || echo 0)
  while name=$(sed -n "$((n+1))p" "$RAW/$LIST"); [ -n "$name" ]; do
    n=$((n+1))
    [ -f "$RAW/done/$name.rc" ] && continue
    echo "$n $name"; return 0
  done
  return 1
}
exec 9> "$RAW/gate.lock"
waited=0
while true; do
  flock 9
  nm=$(peek) || { flock -u 9; break; }
  n=${nm%% *}; name=${nm#* }
  others=$(pgrep -fc "^$PY -u (winding2|zerilli_zeros)"); l15=$(cut -d' ' -f3 /proc/loadavg)
  why=""
  if [ "$others" -eq 0 ]; then :
  elif [ "$others" -eq 1 ] && awk -v l="$l15" 'BEGIN{exit !(l < 4)}'; then why="15-min load $l15 < 4: "
  else
    flock -u 9
    [ $waited -eq 0 ] && echo "$(date -Is) waiting to start $name: $others of this task's processes running, 15-min load $l15 (needs one process and load < 4)" >> "$RAW/queue.log"
    waited=1; sleep 60; continue
  fi
  waited=0
  line=$(grep "^$name|" "$RAW/jobs.txt") || { echo "$(date -Is) no job $name in jobs.txt" >> "$RAW/queue.log"; echo $n > "$RAW/qpos.$LIST"; flock -u 9; continue; }
  echo $n > "$RAW/qpos.$LIST"
  script=$(echo "$line" | cut -d'|' -f2); args=$(echo "$line" | cut -d'|' -f3)
  echo "$(date -Is) ${why}start $name: $script $args --cachedir=$RAW/cache${LIMIT:+ (timeout $LIMIT s)}" >> "$RAW/queue.log"
  nice -n 10 ${LIMIT:+timeout "$LIMIT"} "$PY" -u "$script" $args --cachedir="$RAW/cache" > "$RAW/$name.log" 2>&1 9>&- &
  pid=$!; sleep 3; flock -u 9
  wait $pid; rc=$?
  echo $rc > "$RAW/done/$name.rc"
  echo "$(date -Is) end $name rc=$rc" >> "$RAW/queue.log"
done
