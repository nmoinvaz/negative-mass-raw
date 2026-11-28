#!/bin/bash
cd /home/nathan/Source/negative-mass-i227/notes/wormhole_evolution; export OMP_NUM_THREADS=1
PS=4.7527725276423075e-05
for spec in "bumpP10 1e-10 1e-8 1e-18" "bumpP16 1e-16 1e-14 1e-24"; do
  set -- $spec; name=$1; eta=$2; w=$3; tol=$4
  mkdir -p /home/nathan/Source/negative-mass-raw/I227-rpi5/dev/pert/$name
  lo=$(/home/nathan/Source/negative-mass-venv314/bin/python -c "print(repr($PS - $w))"); hi=$(/home/nathan/Source/negative-mass-venv314/bin/python -c "print(repr($PS + $w))")
  nice -n 10 /home/nathan/Source/negative-mass-venv314/bin/python extended_bisect.py bisect --D=4 --h=0.02 --variant=E --bump=$eta --lo=$lo --hi=$hi --tol=$tol --out=/home/nathan/Source/negative-mass-raw/I227-rpi5/dev/pert/$name > /home/nathan/Source/negative-mass-raw/I227-rpi5/dev/pert/$name/log.txt 2> /home/nathan/Source/negative-mass-raw/I227-rpi5/dev/pert/$name/err.txt; echo $? > /home/nathan/Source/negative-mass-raw/I227-rpi5/dev/pert/$name/rc
done
