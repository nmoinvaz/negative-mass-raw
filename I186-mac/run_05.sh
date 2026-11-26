#!/bin/zsh
# run_05: check V4 alone (amendment A1); run_06: the control moncrief again, now targeting A2 and V4
cd /Users/nathan/Source/negative-mass-i186/phase2/nonradial
D=/Users/nathan/Source/negative-mass-raw/I186-mac
export VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1
{ echo "# $(date '+%Y-%m-%d %H:%M:%S') commit $(git rev-parse --short HEAD) load $(uptime | sed 's/.*load averages*: //')"; } > $D/run_05_V4.log
RAYON_NUM_THREADS=2 /usr/bin/time -l nice -n 10 /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --only=V4 >> $D/run_05_V4.log 2> $D/run_05_V4.err
echo $? > $D/run_05_V4.rc
{ echo "# $(date '+%Y-%m-%d %H:%M:%S') commit $(git rev-parse --short HEAD) load $(uptime | sed 's/.*load averages*: //')"; } > $D/run_06_control_moncrief.log
RAYON_NUM_THREADS=2 /usr/bin/time -l nice -n 10 /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --mutate=moncrief >> $D/run_06_control_moncrief.log 2> $D/run_06_control_moncrief.err
echo $? > $D/run_06_control_moncrief.rc
