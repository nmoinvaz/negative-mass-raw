#!/bin/bash
# launch_I267.sh : the runs of record, detached: the three bisections (three lanes' worth on two lanes), then the 30 jobs.
RAW=$HOME/Source/negative-mass-raw/I267-mac
cd $RAW
( for L in 0 1; do $RAW/scripts/run_jobs.sh $RAW/runs $RAW/jobs_pstar.txt $L 2 > $RAW/logs/pstar_lane$L.log 2>&1 & done; wait
  for L in 0 1; do $RAW/scripts/run_jobs.sh $RAW/runs $RAW/jobs_rec.txt $L 2 > $RAW/logs/rec_lane$L.log 2>&1 & done; wait
  echo finished > $RAW/logs/rec_done ) 
