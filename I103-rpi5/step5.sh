#!/bin/bash
# he_surface.py (with its controls), stdout to RAW, exit code to done/s5_surface.rc
RAW=$HOME/Source/negative-mass-raw/I103-rpi5
cd $HOME/Source/negative-mass-i103
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
/usr/bin/time -v -o $RAW/s5_surface.time nice -n 10 $HOME/Source/negative-mass-venv314/bin/python notes/warp/he_surface.py > $RAW/s5_surface.log 2> $RAW/s5_surface.err
echo $? > $RAW/done/s5_surface.rc
