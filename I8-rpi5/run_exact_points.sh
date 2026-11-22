#!/bin/bash
# Step 3, points method: the 20-point run, the controls and the self-test, one after the other, one process at a time.
# Each log has the command on its first line; its exit code goes to done/<name>.rc.
cd /home/nathan/Source/negative-mass-i8/phase2/nonradial
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=$HOME/Source/negative-mass-venv314/bin/python
run() { name=$1; shift
  echo "# $PY -I verify_polar_exact.py $*" > /home/nathan/Source/negative-mass-raw/I8-rpi5/verify_polar_exact_$name.log
  nice -n 10 $PY -I verify_polar_exact.py "$@" >> /home/nathan/Source/negative-mass-raw/I8-rpi5/verify_polar_exact_$name.log 2>&1
  echo $? > /home/nathan/Source/negative-mass-raw/I8-rpi5/done/exact_$name.rc; }
run points --method=points --npoints=20
run mutate_coef --method=points --npoints=20 --mutate=coef
run mutate_bg_alpha --method=points --npoints=20 --mutate=bg
run mutate_bg_a --method=points --npoints=20 --mutate=bg:a
run mutate_bg_phi0 --method=points --npoints=20 --mutate=bg:phi0
run mutate_bg_u --method=points --npoints=20 --mutate=bg:u
run sensitivity --sensitivity
run selftest --selftest
echo all > /home/nathan/Source/negative-mass-raw/I8-rpi5/done/exact_points_all.rc
