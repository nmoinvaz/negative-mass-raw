#!/bin/bash
# ctl_queue.sh: a worker of the queue of the controls of record. Pops the next line "name|command" of ctl_jobs.txt under flock, runs it from $WT with
# devrun.sh (RAW/name.{log,err,rc}, never overwritten), and repeats until the queue is empty. env: PY, WT. State: ctl_qpos.
set -u
d=$(dirname "$(readlink -f "$0")")
while true; do
  line=$(flock "$d/ctl_queue.lock" bash -c '
    n=$(cat "'"$d"'/ctl_qpos" 2>/dev/null || echo 0); n=$((n+1)); echo $n > "'"$d"'/ctl_qpos"; sed -n "${n}p" "'"$d"'/ctl_jobs.txt"')
  [ -z "$line" ] && break
  name=${line%%|*}; cmd=${line#*|}
  echo "$(date -Is) start $name" >> "$d/ctl_queue.log"
  (cd "$WT" && PY="$PY" RAW="$d" "$d/devrun.sh" "$name" nice -n 10 bash -c "$cmd")
  echo "$(date -Is) end $name rc $(cat "$d/$name.rc")" >> "$d/ctl_queue.log"
done
