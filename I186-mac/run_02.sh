#!/bin/zsh
# run_02: every check of taylor_polar.py, TS against run_01's scipy timings
cd /Users/nathan/Source/negative-mass-i186/phase2/nonradial
D=/Users/nathan/Source/negative-mass-raw/I186-mac
{ echo "# $(date '+%Y-%m-%d %H:%M:%S') commit $(git rev-parse --short HEAD) load $(uptime | sed 's/.*load averages*: //')"; } > $D/run_02_checks.log
RAYON_NUM_THREADS=2 /usr/bin/time -l nice -n 10 /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --scipy-file=$D/scipy_timing.jsonl >> $D/run_02_checks.log 2> $D/run_02_checks.err
echo $? > $D/run_02_checks.rc
