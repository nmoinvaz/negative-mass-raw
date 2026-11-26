#!/bin/bash
# second run of record (13 checks): python3 notes/warp/sum_products.py, the 12 checks then every control, per-control logs in run2/
cd /home/nathan/Source/negative-mass-i169
R=/home/nathan/Source/negative-mass-raw/I169-rpi5
nice -n 10 /usr/bin/time -v -o $R/logs/run_02.time /home/nathan/Source/negative-mass-venv314/bin/python notes/warp/sum_products.py --logdir=$R/run2 > $R/logs/run_02.log 2>&1
echo "exit $?" > $R/logs/run_02.rc
