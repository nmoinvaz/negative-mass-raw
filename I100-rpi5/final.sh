#!/bin/bash
# Step 5: the whole script, stdout to notes/warp/weitzenbock_boundary_output.txt in the worktree and a copy to final.log, with
# /usr/bin/time -v in final.time, the exit code in done/final.rc. One process, nice 10, one thread.
RAW=$HOME/Source/negative-mass-raw/I100-rpi5
cd $HOME/Source/negative-mass-i100 || exit 99
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
echo "commit $(git rev-parse --short HEAD), python notes/warp/weitzenbock_boundary.py > notes/warp/weitzenbock_boundary_output.txt" > $RAW/final.cmd
nice -n 10 /usr/bin/time -v -o $RAW/final.time $HOME/Source/negative-mass-venv314/bin/python notes/warp/weitzenbock_boundary.py > notes/warp/weitzenbock_boundary_output.txt 2> $RAW/final.err
echo $? > $RAW/done/final.rc
cp notes/warp/weitzenbock_boundary_output.txt $RAW/final.log
