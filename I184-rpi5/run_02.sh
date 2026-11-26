#!/bin/bash
# the run of record (step 5): default mode with the controls; stdout to run_02.log (run_01 failed to start: no cargo on the unit's PATH)
export PATH=/home/nathan/.cargo/bin:$PATH
RAW=/home/nathan/Source/negative-mass-raw/I184-rpi5
mkdir -p $RAW/run_02_controls
cd /home/nathan/Source/negative-mass-i184 || exit 2
RAYON_NUM_THREADS=2 /usr/bin/time -v nice -n 10 /home/nathan/Source/negative-mass-venv314/bin/python notes/warp/conical_loglog.py --logdir=$RAW/run_02_controls > $RAW/run_02.log 2> $RAW/run_02.err
echo $? > $RAW/run_02.rc
