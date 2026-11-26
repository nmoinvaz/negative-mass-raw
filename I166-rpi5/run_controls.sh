#!/bin/bash
# usage: run_controls.sh TAG   (one process at a time: every control of the script, log ctl_<TAG>_<name>.log/.rc/.time)
RAW=/home/nathan/Source/negative-mass-raw/I166-rpi5
REPO=/home/nathan/Source/negative-mass-i166
PY=/home/nathan/Source/negative-mass-venv314/bin/python
TAG=$1
cd $REPO
for n in $($PY -c "import sys; sys.argv=['x']; sys.path.insert(0,'notes/warp'); import one_sign_time as m; print(' '.join(m.MUTATIONS))"); do
  $RAW/run_step.sh ctl_${TAG}_$n $PY notes/warp/one_sign_time.py --mutate=$n
  echo "$n exit $(cat $RAW/logs/ctl_${TAG}_$n.rc)" >> $RAW/logs/ctl_${TAG}_batch.log
done
echo done >> $RAW/logs/ctl_${TAG}_batch.log
