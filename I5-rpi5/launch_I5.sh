#!/bin/bash
# Launcher for I5-rpi5 (negative-mass issue 5) on rpi5.  Reads jobs.txt, one job per line:  name|command
# Each job runs at nice 10, OMP_NUM_THREADS=1, log in <name>.log, exit status in done/<name>.rc, and is skipped if
# done/<name>.rc exists.  Start one worker per allowed process:  ./launch_I5.sh  (a second copy shares the queue).
# ./launch_I5.sh --reset starts the queue from line 1 (finished jobs are still skipped; the programs resume from caches).
HERE=$(cd "$(dirname "$0")" && pwd)
export RAW=$HERE NR=$HOME/Source/negative-mass-i5/phase2/nonradial PY=$HOME/Source/negative-mass-venv314/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$NR" || exit 2
[ "$1" = "--reset" ] && rm -f "$RAW/qpos" && shift
next() {
  flock "$RAW/queue.lock" bash -c '
    cd "$RAW"; n=$(cat qpos 2>/dev/null || echo 0)
    while line=$(sed -n "$((n+1))p" jobs.txt); [ -n "$line" ]; do
      n=$((n+1)); name=${line%%|*}
      [ -f "done/$name.rc" ] && continue
      echo $n > qpos; echo "$line"; exit 0
    done; echo $n > qpos'
}
while job=$(next); [ -n "$job" ]; do
  name=${job%%|*}; cmd=${job#*|}
  echo "$(date -Is) start $name" >> "$RAW/queue.log"
  eval "nice -n 10 $cmd" > "$RAW/$name.log" 2>&1; rc=$?
  echo $rc > "$RAW/done/$name.rc"
  echo "$(date -Is) end $name rc=$rc" >> "$RAW/queue.log"
done
