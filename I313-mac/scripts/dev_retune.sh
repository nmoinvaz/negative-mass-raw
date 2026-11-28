#!/bin/bash
# dev_retune.sh: the selected route (5.0, 0.7) retuned at h = 0.02 to gamma_1 = 0.012, 0.048, 0.075 (devtune.py, #295's secant iteration): a reproduction check of the stored B of the selection. Logs never overwritten.
RAW=$HOME/Source/negative-mass-raw/I313-mac
cd $RAW/dev
export NUMBA_NUM_THREADS=1
PY=$HOME/Source/negative-mass/.venv/bin/python
xc=5.0; w=0.7
lg=logs/tune_xc${xc}_w${w}_h0.02.log; n=1
while [ -e $lg ]; do n=$((n+1)); lg=logs/tune_xc${xc}_w${w}_h0.02.$n.log; done
nice -n 10 $PY $RAW/scripts/devtune.py $RAW/dev/runs_dev $xc $w 0.02 0.012 0.048 0.075 > $lg 2> ${lg%.log}.err
echo $? > ${lg%.log}.rc
echo "$(date '+%F %T') retune xc $xc w $w rc=$(cat ${lg%.log}.rc)"
