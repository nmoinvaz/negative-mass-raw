#!/bin/bash
# Step 5: the full run, checks and every control, stdout to the committed output file, one process.
cd /home/nathan/Source/negative-mass-i99
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
RAW=/home/nathan/Source/negative-mass-raw/I99-rpi5
echo "start $(date -Is) commit $(git rev-parse --short HEAD) sha256 $(sha256sum notes/warp/weitzenbock_conf.py | cut -c1-16)" > $RAW/final.time
/usr/bin/time -v -o $RAW/final.time.v nice -n 10 /home/nathan/Source/negative-mass-venv314/bin/python -u notes/warp/weitzenbock_conf.py > notes/warp/weitzenbock_conf_output.txt 2> $RAW/final.err
rc=$?
echo "end $(date -Is) exit $rc" >> $RAW/final.time
echo $rc > $RAW/done/final.rc
cp notes/warp/weitzenbock_conf_output.txt $RAW/final.log
