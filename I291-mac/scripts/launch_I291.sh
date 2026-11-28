#!/bin/bash
# launch_I291.sh : the runs of record, detached, two lanes (jobs_rec_A.txt, jobs_rec_B.txt), then a marker file.
RAW=$HOME/Source/negative-mass-raw/I291-mac
cd $RAW
mkdir -p logs
$RAW/scripts/run_jobs.sh $RAW jobs_rec_A.txt 0 1 > $RAW/logs/rec_laneA.log 2>&1 &
$RAW/scripts/run_jobs.sh $RAW jobs_rec_B.txt 0 1 > $RAW/logs/rec_laneB.log 2>&1 &
wait
echo finished > $RAW/logs/rec_done
