#!/bin/bash
# Step 3: the general diagonal identity (and the diagonal-K case before it), 12 h cap (stop condition).
cd /home/nathan/Source/negative-mass-i99
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
RAW=/home/nathan/Source/negative-mass-raw/I99-rpi5
echo "start $(date -Is) commit $(git rev-parse --short HEAD) sha256 $(sha256sum notes/warp/weitzenbock_conf.py | cut -c1-16)" > $RAW/step3.time
/usr/bin/time -v -o $RAW/step3.time.v nice -n 10 timeout 43200 /home/nathan/Source/negative-mass-venv314/bin/python -u notes/warp/weitzenbock_conf.py --no-controls --only=identity_diag_Kdiag,identity_diag_general > $RAW/step3_general.log 2>&1
rc=$?
echo "end $(date -Is) exit $rc" >> $RAW/step3.time
echo $rc > $RAW/done/step3.rc
