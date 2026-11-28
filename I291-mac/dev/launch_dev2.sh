#!/bin/bash
RAW=$HOME/Source/negative-mass-raw/I291-mac
cd $RAW
for L in 0 1; do $RAW/scripts/run_jobs.sh $RAW/dev/runs dev/jobs_dev2a.txt $L 2 > logs/dev02a_lane$L.log 2>&1 & done; wait
for L in 0 1; do $RAW/scripts/run_jobs.sh $RAW/dev/runs dev/jobs_dev2b.txt $L 2 > logs/dev02b_lane$L.log 2>&1 & done; wait
echo finished > logs/dev02_done
