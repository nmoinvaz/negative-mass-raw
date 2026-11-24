#!/bin/bash
# usage: run_final.sh RUN_TAG [script args...]   (stdout of the script goes to run_final.<tag>.log, rc to .rc, /usr/bin/time -v to .time)
RAW=/home/nathan/Source/negative-mass-raw/I162-rpi5
tag=$1; shift
cd /home/nathan/Source/negative-mass-i162 || exit 2
git rev-parse --short HEAD > $RAW/run_final.$tag.commit
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 /usr/bin/time -v -o $RAW/run_final.$tag.time nice -n 10 \
  /home/nathan/Source/negative-mass-venv314/bin/python notes/warp/bessel_closure.py "$@" > $RAW/run_final.$tag.log 2>&1
echo $? > $RAW/run_final.$tag.rc
