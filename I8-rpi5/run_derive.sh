#!/bin/bash
# Step 2: derive_nonradial.py with wall time, peak rss and exit code. 3 h cap (stop condition).
cd /home/nathan/Source/negative-mass-i8/phase2/nonradial
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
echo "start $(date -Is) commit $(git rev-parse --short HEAD)" > /home/nathan/Source/negative-mass-raw/I8-rpi5/derive_nonradial.time
/usr/bin/time -v -o /home/nathan/Source/negative-mass-raw/I8-rpi5/derive_nonradial.time.v nice -n 10 timeout 10800 /home/nathan/Source/negative-mass-venv314/bin/python -u derive_nonradial.py > /home/nathan/Source/negative-mass-raw/I8-rpi5/derive_nonradial.log 2>&1
rc=$?
echo "end $(date -Is) exit $rc" >> /home/nathan/Source/negative-mass-raw/I8-rpi5/derive_nonradial.time
echo $rc > /home/nathan/Source/negative-mass-raw/I8-rpi5/done/derive.rc
