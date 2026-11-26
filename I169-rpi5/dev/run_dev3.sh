#!/bin/bash
# dev run 3: checks and all controls of sum_products.py (computes what each control does; not of record)
cd /home/nathan/Source/negative-mass-i169
nice -n 10 /home/nathan/Source/negative-mass-venv314/bin/python notes/warp/sum_products.py --logdir=/home/nathan/Source/negative-mass-raw/I169-rpi5/dev/ctl3
echo "exit $?" > /home/nathan/Source/negative-mass-raw/I169-rpi5/dev/dev3.rc
