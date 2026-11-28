#!/bin/bash
# usage: run_queue.sh JOBS   one job at a time; each line "name|command" (variables expanded by the shell that reads the line).
# stdout in NAME.log, stderr in NAME.err, exit code in NAME.rc, /usr/bin/time -l in NAME.time; 2 h wall limit per job (rc 124).
# A job whose NAME.log exists is skipped, never overwritten.
. "$(dirname "$0")/env.sh"
while IFS='|' read -r name cmd; do
  [ -z "$name" ] && continue
  [ -e "$RAW/$name.log" ] && { echo "skip $name: log exists" >&2; continue; }
  {
    echo "# $name: $(date -u +%FT%TZ) machine $(hostname -s) load $(sysctl -n vm.loadavg | tr -d '{}') threads 2 nice 10 (RAYON_NUM_THREADS=2)"
    echo "# command: $cmd"
  } > "$RAW/$name.log"
  gtimeout 7200 /usr/bin/time -l -o "$RAW/$name.time" nice -n 10 bash -c "$cmd" >> "$RAW/$name.log" 2> "$RAW/$name.err"
  rc=$?
  echo "# $name finished $(date -u +%FT%TZ) exit $rc load $(sysctl -n vm.loadavg | tr -d '{}')" >> "$RAW/$name.log"
  echo $rc > "$RAW/$name.rc"
done < "$1"
