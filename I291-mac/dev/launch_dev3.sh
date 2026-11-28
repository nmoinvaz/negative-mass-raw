#!/bin/bash
RAW=$HOME/Source/negative-mass-raw/I291-mac
cd $RAW
# lane 0: all h = 0.01 jobs; lane 1: all h = 0.005 jobs (a pstar must precede its member: the file order does that within a lane)
grep '^0.01 ' dev/jobs_dev3.txt > dev/jobs_dev3_a.txt; grep '^0.005 ' dev/jobs_dev3.txt > dev/jobs_dev3_b.txt
$RAW/scripts/run_jobs.sh $RAW/dev dev/jobs_dev3_a.txt 0 1 > logs/dev03a.log 2>&1 &
$RAW/scripts/run_jobs.sh $RAW/dev dev/jobs_dev3_b.txt 0 1 > logs/dev03b.log 2>&1 &
wait
echo finished > logs/dev03_done
