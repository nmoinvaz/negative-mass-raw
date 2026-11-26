#!/bin/bash
# the run of record of #183: five stages, each under `timeout 3600`, in order; logs run_03<x>.log, exit codes run_03<x>.rc
RAW=/home/nathan/Source/negative-mass-raw/I183-rpi5
cd /home/nathan/Source/negative-mass-i183
export RAYON_NUM_THREADS=2 PATH=/home/nathan/.cargo/bin:$PATH
PY=/home/nathan/Source/negative-mass-venv314/bin/python
S="notes/warp/conical_offgrid.py --nobuild"
stage() { name=$1; shift; s=$(date +%s)
  timeout 3600 $PY $S "$@" > $RAW/run_03$name.log 2>&1; echo $? > $RAW/run_03$name.rc
  echo "run_03$name $(( $(date +%s) - s )) s rc $(cat $RAW/run_03$name.rc)" >> $RAW/run_03_times.log; }
stage a --no-controls --dump=$RAW/dump_run_03a --only=n_table,series_hp,plant_167,plant_far,regress167,scan,spread,modes,symmetry,n4_factor,closed_form,bisect,independent,recip_check,step_halving
stage b --no-controls --dump=$RAW/dump_run_03b --only=dd_qd
mkdir -p $RAW/ctl_run_03
stage c --controls-only --logdir=$RAW/ctl_run_03 --controls=eq-coeff,series-coeff,plant-locator,locator-side,recip-dd,start-bar,halving,halving-coarse
stage d --controls-only --logdir=$RAW/ctl_run_03 --controls=n-drift,sym-break,n4-coeff,cf-coeff,bisect-end
stage e --controls-only --logdir=$RAW/ctl_run_03 --controls=indep-eq,regress-kind,match-sign
echo done >> $RAW/run_03_times.log
