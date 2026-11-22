#!/bin/bash
# Step 4: matter_sv.py for four stars, one after the other, from phase2/nonradial, unmodified.
cd /home/nathan/Source/negative-mass-i8/phase2/nonradial
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=$HOME/Source/negative-mass-venv314/bin/python
echo "start $(date -Is) commit $(git rev-parse --short HEAD)" > /home/nathan/Source/negative-mass-raw/I8-rpi5/matter_sv.time
for cfg in "-1 0.7603 2" "-1 0.7603 3" "1 0.75 2" "1 0.75 3"; do
  name=$(echo $cfg | tr ' ' '_')
  echo "# python matter_sv.py $cfg" > /home/nathan/Source/negative-mass-raw/I8-rpi5/matter_sv_$name.log
  /usr/bin/time -v -o /home/nathan/Source/negative-mass-raw/I8-rpi5/matter_sv_$name.time.v nice -n 10 $PY -I matter_sv.py $cfg >> /home/nathan/Source/negative-mass-raw/I8-rpi5/matter_sv_$name.log 2>&1
  echo $? > /home/nathan/Source/negative-mass-raw/I8-rpi5/done/matter_sv_$name.rc
  echo "$cfg done $(date -Is) exit $(cat /home/nathan/Source/negative-mass-raw/I8-rpi5/done/matter_sv_$name.rc)" >> /home/nathan/Source/negative-mass-raw/I8-rpi5/matter_sv.time
done
echo all > /home/nathan/Source/negative-mass-raw/I8-rpi5/done/matter_sv_all.rc
