#!/bin/bash
# usage: run_queue.sh JOBS   one process at a time; each line "name|command"; log, rc and memory in the raw folder; 1 h limit per job
RAW=$HOME/Source/negative-mass-raw/I190-rpi5
while IFS='|' read -r name cmd; do
  [ -z "$name" ] && continue
  [ -f $RAW/$name.rc ] && continue
  {
    echo "# $name: $(date -u +%FT%TZ) machine $(hostname) load $(cut -d' ' -f1-3 /proc/loadavg) threads 2 nice 10 (RAYON_NUM_THREADS=2)"
    echo "# command: $cmd"
  } > $RAW/$name.log
  timeout 3600 /usr/bin/time -v bash -c "$cmd" >> $RAW/$name.log 2>&1
  rc=$?
  echo "# $name finished $(date -u +%FT%TZ) exit $rc load $(cut -d' ' -f1-3 /proc/loadavg)" >> $RAW/$name.log
  echo $rc > $RAW/$name.rc
done < "$1"
