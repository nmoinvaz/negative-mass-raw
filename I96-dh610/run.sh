#!/bin/bash
cd $HOME/Source/negative-mass-i96
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
nice -n 10 /home/nathan/Source/negative-mass-venv314/bin/python -u notes/warp/tanh_spectrum.py --part=vc,planted,shift,tanh --sigmas=16 --p=16:340 --npan=320 --procs=1 --raw=/home/nathan/Source/negative-mass-raw/I96-dh610/eig > /home/nathan/Source/negative-mass-raw/I96-dh610/sectors-s16-p340.log 2>&1
echo $? > /home/nathan/Source/negative-mass-raw/I96-dh610/sectors-s16-p340.log.exit
