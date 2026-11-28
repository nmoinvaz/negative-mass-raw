#!/bin/bash
# launch_I291_extra.sh : after the runs of record, the delta dependence (report only): member 0's pairs at e = 11, 10 for the three h, two lanes.
RAW=$HOME/Source/negative-mass-raw/I291-mac
cd $RAW
$RAW/scripts/run_jobs.sh $RAW jobs_rec_C.txt 0 1 > $RAW/logs/extra_laneC.log 2>&1 &
$RAW/scripts/run_jobs.sh $RAW jobs_rec_D.txt 0 1 > $RAW/logs/extra_laneD.log 2>&1 &
wait
echo finished > $RAW/logs/extra_done
