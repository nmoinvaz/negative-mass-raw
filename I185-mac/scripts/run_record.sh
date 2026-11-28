#!/bin/zsh
# the run of record of #185: all checks, then the controls. Usage: run_record.sh WT RAW
WT=$1; RAW=$2
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
cd $WT || exit 2
nice -n 10 $PY notes/warp/conical_eta0.py --logdir=$RAW/record > $RAW/record/run_01.log 2> $RAW/record/run_01.err
echo $? > $RAW/record/run_01.rc
