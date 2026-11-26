#!/bin/bash
# usage: run_dev.sh NAME args...   (runs conical_offgrid.py in the worktree, log and rc in the raw folder)
NAME=$1; shift
RAW=/home/nathan/Source/negative-mass-raw/I183-rpi5
cd /home/nathan/Source/negative-mass-i183
export RAYON_NUM_THREADS=2 PATH=/home/nathan/.cargo/bin:$PATH
/home/nathan/Source/negative-mass-venv314/bin/python notes/warp/conical_offgrid.py --nobuild --dump=$RAW/dump_$NAME "$@" > $RAW/$NAME.log 2>&1
echo $? > $RAW/$NAME.rc
