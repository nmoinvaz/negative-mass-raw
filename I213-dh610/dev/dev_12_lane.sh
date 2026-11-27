#!/bin/bash
# dev_12: trial of the runs of record at full size (development, not of record): one lane = lines "kind args"
cd /home/nathan/Source/negative-mass-i213/notes/wormhole_evolution
OUT=~/Source/negative-mass-raw/I213-dh610/dev/rec_trial/runs
while IFS= read -r line; do
  [ -z "$line" ] && continue
  nice -n 10 ~/Source/negative-mass-venv314/bin/python expansion.py job $line --out=$OUT >> $OUT/lane_$LANE.log 2>&1
  echo "$line rc=$?" >> $OUT/lane_$LANE.done
done
