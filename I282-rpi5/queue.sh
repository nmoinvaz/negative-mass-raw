#!/bin/bash
# queue.sh JOBS: a worker of a queue. Pops the next line "name|command" of the file JOBS under flock, runs it from $WT with devrun.sh
# (RAW/name.{log,err,rc}, never overwritten), and repeats until the queue is empty. env: PY, WT. State: JOBS.pos, JOBS.lock, JOBS.log.
set -u
d=$(dirname "$(readlink -f "$0")")
jobs=$(readlink -f "$1")
while true; do
  line=$(flock "$jobs.lock" bash -c '
    n=$(cat "'"$jobs"'.pos" 2>/dev/null || echo 0); n=$((n+1)); echo $n > "'"$jobs"'.pos"; sed -n "${n}p" "'"$jobs"'"')
  [ -z "$line" ] && break
  name=${line%%|*}; cmd=${line#*|}
  echo "$(date -Is) start $name" >> "$jobs.log"
  (cd "$WT" && PY="$PY" RAW="$d" "$d/devrun.sh" "$name" nice -n 10 bash -c "$cmd")
  echo "$(date -Is) end $name rc $(cat "$d/$name.rc")" >> "$jobs.log"
done
