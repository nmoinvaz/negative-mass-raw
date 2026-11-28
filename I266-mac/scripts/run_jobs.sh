#!/bin/bash
# run_jobs.sh ROOT JOBFILE LANE NLANES : run lines LANE, LANE+NLANES, ... of JOBFILE ("FAM B H" per line) through run_one.sh; one line of progress per job.
ROOT=$1; JOBS=$2; LANE=$3; NL=$4
k=0
while read fam B h; do
  if [ $((k % NL)) -eq $LANE ]; then
    t0=$(date +%s); $HOME/Source/negative-mass-raw/I266-mac/scripts/run_one.sh $ROOT $fam $B $h; rc=$?
    echo "$(date '+%F %T') lane $LANE: $fam $B $h rc=$rc $(( $(date +%s) - t0 )) s"
  fi
  k=$((k+1))
done < $JOBS
