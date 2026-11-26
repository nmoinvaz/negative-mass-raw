#!/bin/zsh
# run_01: the scipy path (convergence.py's base variant) at the timing points, one process, one thread, nice 10
cd /Users/nathan/Source/negative-mass-i186/phase2/nonradial
export VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
D=/Users/nathan/Source/negative-mass-raw/I186-mac
{ echo "# $(date '+%Y-%m-%d %H:%M:%S') commit $(git rev-parse --short HEAD) load $(uptime | sed 's/.*load averages*: //')"; } > $D/run_01_scipy_timing.log
/usr/bin/time -l nice -n 10 /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --scipy-timing $D/scipy_timing.jsonl >> $D/run_01_scipy_timing.log 2> $D/run_01_scipy_timing.err
echo $? > $D/run_01_scipy_timing.rc
