#!/bin/bash
# the analyses of record, from the stored runs; numbered logs, nothing overwritten
RAW=$HOME/Source/negative-mass-raw/I228-dh610
cd $HOME/Source/negative-mass-i228/notes/wormhole_evolution
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1
mkdir -p $RAW/runs/analysis
k=1; while [ -e $RAW/runs/analysis/g_d6_analyze_record$k.log ]; do k=$((k+1)); done
nice -n 10 $HOME/Source/negative-mass-venv314/bin/python g_d6.py analyze --base=$RAW/runs --hks=1,2 > $RAW/runs/analysis/g_d6_analyze_record$k.log 2> $RAW/runs/analysis/g_d6_analyze_record$k.err
echo "rc=$?" > $RAW/runs/analysis/g_d6_analyze_record$k.rc
