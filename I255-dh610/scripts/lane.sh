#!/bin/bash
# lane.sh LANE: takes lines of runs/queue.txt one at a time (flock), runs each as `throat_drift.py <args>` with a 2 h limit (timeout 7200), one thread, nice 10;
# logs runs/logs/job_<name>.{log,time,rc,lane}; a log is never overwritten (a rerun gets a numbered name).
LANE=$1
PY=$HOME/Source/negative-mass-venv314/bin/python
RAW=$HOME/Source/negative-mass-raw/I255-dh610
Q=$RAW/runs/queue.txt
cd $HOME/Source/negative-mass-i255/notes/wormhole_evolution
while true; do
  line=$(flock $Q.lock bash -c 'l=$(head -n1 "$0"); if [ -n "$l" ]; then sed -i 1d "$0"; fi; echo "$l"' $Q)
  [ -z "$line" ] && break
  name=${line%%|*}; args=${line#*|}
  f=$RAW/runs/logs/job_$name; i=1
  while [ -e $f.log ]; do f=$RAW/runs/logs/job_${name}_r$i; i=$((i+1)); done
  echo "$LANE $(date +%F_%T)" > $f.lane
  /usr/bin/time -v -o $f.time timeout 7200 nice -n 10 $PY throat_drift.py $args > $f.log 2>&1
  echo $? > $f.rc
  echo "$LANE $(date +%F_%T) $name rc=$(cat $f.rc)" >> $RAW/runs/logs/lanes.log
done
