#!/bin/bash
# Step 3 at the final commit: every run of verify_polar_exact.py, one after the other, one process at a time.
# Each log has the command on its first line; its exit code goes to done/exact_<name>.rc. Order = order of the output file.
cd /home/nathan/Source/negative-mass-i8/phase2/nonradial
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=$HOME/Source/negative-mass-venv314/bin/python
echo "start $(date -Is) commit $(git rev-parse --short HEAD)" > /home/nathan/Source/negative-mass-raw/I8-rpi5/exact_all.time
run() { name=$1; shift
  echo "# python verify_polar_exact.py $*" > /home/nathan/Source/negative-mass-raw/I8-rpi5/verify_polar_exact_$name.log
  s=$(date +%s)
  nice -n 10 $PY -I -u verify_polar_exact.py "$@" >> /home/nathan/Source/negative-mass-raw/I8-rpi5/verify_polar_exact_$name.log 2>&1
  rc=$?
  echo $rc > /home/nathan/Source/negative-mass-raw/I8-rpi5/done/exact_$name.rc
  echo "$name exit $rc wall $(($(date +%s)-s)) s" >> /home/nathan/Source/negative-mass-raw/I8-rpi5/exact_all.time; }
run points --method=points --npoints=20
run mutate_coef --method=points --npoints=20 --mutate=coef
run mutate_bg_alpha --method=points --npoints=20 --mutate=bg
run mutate_bg_a --method=points --npoints=20 --mutate=bg:a
run mutate_bg_phi0 --method=points --npoints=20 --mutate=bg:phi0
run mutate_bg_u --method=points --npoints=20 --mutate=bg:u
run mutate_eq --method=points --npoints=20 --mutate=eq
run points_af --method=points --engine=af --npoints=20
run sensitivity --sensitivity
run selftest --selftest
run symbolic --method=symbolic --deadline=28800
run symbolic_mutate_coef --method=symbolic --mutate=coef --deadline=28800
run symbolic_mutate_bg_alpha --method=symbolic --mutate=bg --deadline=28800
run symbolic_mutate_bg_a --method=symbolic --mutate=bg:a --deadline=28800
run symbolic_mutate_bg_phi0 --method=symbolic --mutate=bg:phi0 --deadline=28800
run symbolic_mutate_bg_u --method=symbolic --mutate=bg:u --deadline=28800
run symbolic_mutate_eq --method=symbolic --mutate=eq --deadline=28800
run crosscheck --crosscheck --npoints=5
run frac_free_r --method=symbolic --engine=frac --free=r --npoints=1
run frac_free_r_s --method=symbolic --engine=frac --free=r,s --npoints=1
run frac_free_r_alpha_a --method=symbolic --engine=frac --free=r,alpha,a --npoints=1
echo "end $(date -Is)" >> /home/nathan/Source/negative-mass-raw/I8-rpi5/exact_all.time
echo all > /home/nathan/Source/negative-mass-raw/I8-rpi5/done/exact_all.rc
