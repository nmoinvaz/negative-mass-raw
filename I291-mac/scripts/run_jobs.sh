#!/bin/bash
# run_jobs.sh ROOT JOBFILE LANE NLANES : run lines LANE, LANE+NLANES, ... of JOBFILE ("H E K" per line, E = pstar for the bisection) through run_one.sh; one line of progress per job.
ROOT=$1; JOBS=$2; LANE=$3; NL=$4
k=0
while read h e kk; do
  if [ $((k % NL)) -eq $LANE ]; then
    t0=$(date +%s); $HOME/Source/negative-mass-raw/I291-mac/scripts/run_one.sh $ROOT $h $e $kk; rc=$?
    echo "$(date '+%F %T') lane $LANE: h $h $e k$kk rc=$rc $(( $(date +%s) - t0 )) s"
  fi
  k=$((k+1))
done < $JOBS
