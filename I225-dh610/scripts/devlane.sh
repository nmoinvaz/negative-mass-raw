#!/bin/bash
# development reruns with logs: dev_NN_*.log (never overwritten: a rerun gets the next number). Run from notes/wormhole_evolution of the worktree.
PY=$HOME/Source/negative-mass-venv314/bin/python
RAW=$HOME/Source/negative-mass-raw/I225-dh610
cd $HOME/Source/negative-mass-i225/notes/wormhole_evolution
run() { name=$1; shift; i=1; while [ -e $RAW/dev/${name}_r$i.log ]; do i=$((i+1)); done; /usr/bin/time -v -o $RAW/dev/${name}_r$i.time "$@" > $RAW/dev/${name}_r$i.log 2>&1; echo $? > $RAW/dev/${name}_r$i.rc; }
D=$RAW/dev
run dev_01_sweep_vs_dn nice -n 10 $PY $D/dev_01_sweep_vs_dn.py
run dev_02_triangle nice -n 10 $PY $D/dev_02_triangle.py
run dev_03_locus_D4_h0.01 nice -n 10 $PY $D/dev_03_locus_D4_h0.01.py
run dev_07_static_member nice -n 10 $PY $D/dev_07_static_member.py
run dev_08_planted_static nice -n 10 $PY $D/dev_08_planted_static.py
run dev_05_pair_rate_D4 nice -n 10 $PY $D/dev_05_pair_rate.py 4 1 32 9
run dev_05_pair_rate_D5 nice -n 10 $PY $D/dev_05_pair_rate.py 5 0 34 9
run dev_06_expand_probe nice -n 10 $PY $D/dev_06_expand_probe.py 4 0.04 100 0.04 /tmp/dev06.npz
run dev_09_stall_D4 nice -n 10 $PY $D/dev_09_stall_job.py 4 0 /tmp/dev09_4
run dev_09_member_D4 nice -n 10 $PY $D/dev_09_member_table.py 4 0.02 /tmp/dev09_4
run dev_09_stall_D5 nice -n 10 $PY $D/dev_09_stall_job.py 5 0 /tmp/dev09_5
run dev_09_member_D5 nice -n 10 $PY $D/dev_09_member_table.py 5 0.00707107 /tmp/dev09_5
run dev_10_expand_S nice -n 10 $PY $D/dev_10_expand_S_G.py 4 0 0.05 100 S /tmp/dev10
run dev_10_expand_G nice -n 10 $PY $D/dev_10_expand_S_G.py 4 0 0.05 100 G /tmp/dev10
for v in 0.0 0.1 0.5; do run dev_11_planted_series_D4_v$v nice -n 10 $PY $D/dev_11_planted_series.py 4 0 $v; done
run dev_11_planted_series_D5_v0.13 nice -n 10 $PY $D/dev_11_planted_series.py 5 0 0.13
