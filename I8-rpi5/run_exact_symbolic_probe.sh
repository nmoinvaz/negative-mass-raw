#!/bin/bash
# Probe of the symbolic method: 300 s deadline, log only.
cd /home/nathan/Source/negative-mass-i8/phase2/nonradial
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
echo "# python verify_polar_exact.py --method=symbolic --deadline=300" > /home/nathan/Source/negative-mass-raw/I8-rpi5/probe/symbolic_probe.log
/usr/bin/time -v -o /home/nathan/Source/negative-mass-raw/I8-rpi5/probe/symbolic_probe.time.v nice -n 10 timeout 900 $HOME/Source/negative-mass-venv314/bin/python -I -u verify_polar_exact.py --method=symbolic --deadline=300 >> /home/nathan/Source/negative-mass-raw/I8-rpi5/probe/symbolic_probe.log 2>&1
echo $? > /home/nathan/Source/negative-mass-raw/I8-rpi5/probe/symbolic_probe.rc
