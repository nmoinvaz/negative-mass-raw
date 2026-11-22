#!/bin/bash
# Builds phase2/nonradial/matter_sv_output.txt from the logs of run_matter_sv.sh.
RAW=/home/nathan/Source/negative-mass-raw/I8-rpi5; OUT=/home/nathan/Source/negative-mass-i8/phase2/nonradial/matter_sv_output.txt
{
echo "matter_sv.py, unmodified, run from phase2/nonradial at commit $(sed -n 's/.*commit //p' $RAW/matter_sv.time) (branch wip/i8-polar-exact) on rpi5-ubuntu,"
echo "Python 3.14.10 (sympy 1.14.0, numpy 2.5.4, scipy 1.18.1). Raw logs, timings and exit codes: negative-mass-raw, folder I8-rpi5."
echo "Each run below is  nice -n 10 python matter_sv.py <eps> <w> <l>  (OMP_NUM_THREADS=1); every exit code is 0."
echo "sv2/sv1 and sv3/sv1 are the second and third singular values of A over the first (matter_sv.py's docstring);"
echo "the table lists every 4th of the 25 values of gamma, the first line gives the minimum over all 25."
for cfg in "-1 0.7603 2" "-1 0.7603 3" "1 0.75 2" "1 0.75 3"; do
  name=$(echo $cfg | tr ' ' '_')
  echo
  echo "$ python matter_sv.py $cfg"
  tail -n +2 $RAW/matter_sv_$name.log
  echo "exit $(cat $RAW/done/matter_sv_$name.rc)"
done
} > $OUT
