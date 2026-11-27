#!/bin/bash
# Queue worker of I253-rpi5 (negative-mass issue 253) on rpi5.   Usage: ./launch_I253.sh LISTFILE     (a second and third copy share the queue)
# LISTFILE has one job per line:  name|command.  Each job runs at nice 10 with one thread, log in <name>.log, exit status in done/<name>.rc, and is
# skipped if done/<name>.rc exists. The command carries its own `timeout 7200` (the 2 h stop). The next line is taken under flock.
HERE=$(cd "$(dirname "$0")" && pwd)
export RAW=$HERE NR=$HOME/Source/negative-mass-i253/notes/wormhole_evolution PY=$HOME/Source/negative-mass-venv314/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMBA_NUM_THREADS=1
LIST=$(basename "$1")
cd "$NR" || exit 2
mkdir -p "$RAW/done" "$RAW/runs" "$RAW/logs"
next() {
  flock "$RAW/queue.lock" bash -c '
    cd "$RAW"; n=$(cat "qpos.'"$LIST"'" 2>/dev/null || echo 0)
    while line=$(sed -n "$((n+1))p" "'"$LIST"'"); [ -n "$line" ]; do
      n=$((n+1)); name=${line%%|*}
      [ -f "done/$name.rc" ] && continue
      echo $n > "qpos.'"$LIST"'"; echo "$line"; exit 0
    done; echo $n > "qpos.'"$LIST"'"'
}
while job=$(next); [ -n "$job" ]; do
  name=${job%%|*}; cmd=${job#*|}
  echo "$(date -Is) start $name (15-min load $(cut -d' ' -f3 /proc/loadavg))" >> "$RAW/queue.log"
  eval "nice -n 10 $cmd" > "$RAW/logs/$name.log" 2>&1; rc=$?
  echo $rc > "$RAW/done/$name.rc"
  echo "$(date -Is) end $name rc=$rc" >> "$RAW/queue.log"
done
