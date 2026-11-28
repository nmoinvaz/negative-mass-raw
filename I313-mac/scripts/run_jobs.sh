#!/bin/bash
# run_jobs.sh ROOT JOBFILE LANE NLANES : run lines LANE, LANE+NLANES, ... of JOBFILE ("B XC W H LO HI" per line) through run_one.sh; one line of progress per job.
ROOT=$1; JOBS=$2; LANE=$3; NL=$4
k=0
while read B XC W H LO HI; do
  if [ $((k % NL)) -eq $LANE ]; then
    t0=$(date +%s); $HOME/Source/negative-mass-raw/I313-mac/scripts/run_one.sh $ROOT $B $XC $W $H $LO $HI; rc=$?
    echo "$(date '+%F %T') lane $LANE: B $B xc $XC w $W h $H rc=$rc $(( $(date +%s) - t0 )) s"
  fi
  k=$((k+1))
done < $JOBS
