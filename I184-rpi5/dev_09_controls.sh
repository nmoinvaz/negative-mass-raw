#!/bin/bash
# development run of every control (README step 4): each control runs only the checks it names; logs and exit codes here
RAW=/home/nathan/Source/negative-mass-raw/I184-rpi5
OUT=$RAW/dev_09_controls
mkdir -p $OUT
cd /home/nathan/Source/negative-mass-i184 || exit 2
PY=/home/nathan/Source/negative-mass-venv314/bin/python
$PY notes/warp/conical_loglog.py --list --nobuild | while read name targets; do
  t0=$(date +%s)
  RAYON_NUM_THREADS=2 nice -n 10 $PY notes/warp/conical_loglog.py --mutate=$name --nobuild --only=$targets > $OUT/ctl_$name.log 2>&1
  echo $? > $OUT/ctl_$name.rc
  echo "$name rc=$(cat $OUT/ctl_$name.rc) $(( $(date +%s) - t0 )) s targets=$targets" >> $OUT/summary.txt
done
echo "all done" >> $OUT/summary.txt
echo 0 > $OUT/script.rc
