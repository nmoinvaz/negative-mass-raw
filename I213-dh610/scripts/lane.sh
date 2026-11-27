#!/bin/bash
# one lane of the runs of record: lane.sh N reads scripts/queue_N.txt; each job runs `expansion.py job` niced, under a 2 h limit, log and exit code in runs/
RAW=$HOME/Source/negative-mass-raw/I213-dh610
cd $HOME/Source/negative-mass-i213/notes/wormhole_evolution
while IFS= read -r line; do
  [ -z "$line" ] && continue
  tag=$(echo "$line" | tr -c 'A-Za-z0-9.=\n' '_')
  echo "$(date +%F_%T) start $line" >> $RAW/runs/lane_$1.log
  /usr/bin/time -v -o $RAW/runs/job_$tag.time timeout 7200 nice -n 10 $HOME/Source/negative-mass-venv314/bin/python expansion.py job $line --out=$RAW/runs > $RAW/runs/job_$tag.log 2>&1
  rc=$?
  echo "$(date +%F_%T) end   $line rc=$rc" >> $RAW/runs/lane_$1.log
done < $RAW/scripts/queue_$1.txt
echo "$(date +%F_%T) lane $1 done" >> $RAW/runs/lane_$1.log
