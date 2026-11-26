#!/bin/bash
# usage: run_final.sh N   (default mode: checks then every control; stdout to logs/final_N.log, stderr to .err, rc and time beside)
RAW=/home/nathan/Source/negative-mass-raw/I166-rpi5
REPO=/home/nathan/Source/negative-mass-i166
N=$1
LOG=$RAW/logs/final_$N.log
if [ -e "$LOG" ]; then echo "refusing to overwrite $LOG"; exit 2; fi
cd $REPO
git rev-parse HEAD > $RAW/logs/final_$N.commit
/usr/bin/time -v -o $RAW/logs/final_$N.time nice -n 10 /home/nathan/Source/negative-mass-venv314/bin/python notes/warp/one_sign_time.py > $LOG 2> $RAW/logs/final_$N.err
echo $? > $RAW/logs/final_$N.rc
