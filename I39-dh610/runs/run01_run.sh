#!/bin/bash
# usage: run01_run.sh NAME KERNELFLAGS... -- ARGS...   runs checks.py once under /usr/bin/time -v, nice 10, one thread; log, time and rc go to runs/
# NAME is the log stem; the numba-free run sets DN_NO_NUMBA=1 in its own unit.
cd /home/nathan/Source/negative-mass-i39/notes/wormhole_evolution
R=/home/nathan/Source/negative-mass-raw/I39-dh610/runs
NAME=$1; shift
/usr/bin/time -v nice -n 10 /home/nathan/Source/negative-mass-venv314/bin/python checks.py "$@" --json=$R/$NAME.json > $R/$NAME.log 2> $R/$NAME.time
echo "rc=$?" > $R/$NAME.rc
