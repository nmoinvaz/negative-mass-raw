#!/bin/bash
# usage: run_ctl_batch.sh PREFIX NAME...   one control per name on the ctl grid, every check; log PREFIX_ctl_NAME.log, rc PREFIX_ctl_NAME.rc
PREFIX=$1; shift
RAW=/home/nathan/Source/negative-mass-raw/I183-rpi5
cd /home/nathan/Source/negative-mass-i183
export RAYON_NUM_THREADS=2 PATH=/home/nathan/.cargo/bin:$PATH
for NAME in "$@"; do
  s=$(date +%s)
  /home/nathan/Source/negative-mass-venv314/bin/python notes/warp/conical_offgrid.py --nobuild --grid=ctl --mutate=$NAME > $RAW/${PREFIX}_ctl_$NAME.log 2>&1
  echo $? > $RAW/${PREFIX}_ctl_$NAME.rc
  echo "$NAME $(( $(date +%s) - s )) s" >> $RAW/${PREFIX}_ctl_times.log
done
