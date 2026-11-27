#!/bin/bash
# run_04a: stage a of the run of record again with the final script (the diff to run_03a is printed summaries only), under timeout 3600
RAW=/home/nathan/Source/negative-mass-raw/I183-rpi5
cd /home/nathan/Source/negative-mass-i183
export RAYON_NUM_THREADS=2 PATH=/home/nathan/.cargo/bin:$PATH
s=$(date +%s)
timeout 3600 /home/nathan/Source/negative-mass-venv314/bin/python notes/warp/conical_offgrid.py --nobuild --no-controls --dump=$RAW/dump_run_04a --only=n_table,series_hp,plant_167,plant_far,regress167,scan,spread,modes,symmetry,n4_factor,closed_form,bisect,independent,recip_check,step_halving > $RAW/run_04a.log 2>&1
echo $? > $RAW/run_04a.rc
echo "run_04a $(( $(date +%s) - s )) s rc $(cat $RAW/run_04a.rc)" >> $RAW/run_03_times.log
