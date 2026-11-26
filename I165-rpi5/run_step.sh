#!/bin/bash
# usage: run_step.sh NAME command...   (log, exit code and /usr/bin/time -v in logs/; refuses to overwrite a log)
RAW=/home/nathan/Source/negative-mass-raw/I165-rpi5
REPO=/home/nathan/Source/negative-mass-i165
NAME=$1; shift
LOG=$RAW/logs/$NAME.log
if [ -e "$LOG" ]; then echo "refusing to overwrite $LOG"; exit 2; fi
cd $REPO
/usr/bin/time -v -o $RAW/logs/$NAME.time nice -n 10 "$@" > $LOG 2>&1
echo $? > $RAW/logs/$NAME.rc
