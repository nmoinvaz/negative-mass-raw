#!/bin/bash
RAW=/home/nathan/Source/negative-mass-raw/I184-rpi5
cd /home/nathan/Source/negative-mass-i184 || exit 2
RAYON_NUM_THREADS=2 nice -n 10 /home/nathan/Source/negative-mass-venv314/bin/python notes/warp/conical_loglog.py --nobuild --only=regress,basin,parity,trap_bounds,trap_entry,basin_map > $RAW/dev_11_walk_checks.log 2>&1
echo $? > $RAW/dev_11_walk_checks.rc
