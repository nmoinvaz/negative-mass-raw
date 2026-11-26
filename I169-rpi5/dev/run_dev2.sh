#!/bin/bash
# dev run 2: the checks of sum_products.py without controls (not of record)
cd /home/nathan/Source/negative-mass-i169
nice -n 10 /home/nathan/Source/negative-mass-venv314/bin/python notes/warp/sum_products.py --no-controls
echo "exit $?" > /home/nathan/Source/negative-mass-raw/I169-rpi5/dev/dev2.rc
