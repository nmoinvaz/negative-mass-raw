#!/bin/zsh
# the run of record of #185: all checks, then the controls. Usage: run_record.sh WT RAW N   (logs record/run_0N.*, controls in record/run_0N_controls/)
WT=$1; RAW=$2; N=$3
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
cd $WT || exit 2
mkdir -p $RAW/record/run_0${N}_controls
nice -n 10 $PY notes/warp/conical_eta0.py --logdir=$RAW/record/run_0${N}_controls > $RAW/record/run_0${N}.log 2> $RAW/record/run_0${N}.err
echo $? > $RAW/record/run_0${N}.rc
