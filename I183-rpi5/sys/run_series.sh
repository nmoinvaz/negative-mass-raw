#!/bin/bash
cd /home/nathan/Source/negative-mass-raw/I183-rpi5/sys
nice -n 10 /home/nathan/Source/negative-mass-venv314/bin/python gen_series.py > gen_series.log 2>&1
echo $? > gen_series.rc
