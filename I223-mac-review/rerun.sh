#!/bin/bash
# The coordinator's partial rerun of #223, one process, nice 10.
R=$HOME/Source/negative-mass-raw/I223-mac-review
cd $HOME/Source/negative-mass-r223/notes/black_universe || exit 2
PY=$HOME/Source/negative-mass/.venv/bin/python
export OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
mkdir -p $R/rerun
for c in check planted planted_complex "complex S_m0.2 S_m0.3 B1_q0.77 --out=$R/rerun/complex.json" "count S_m1 --res=R2 --out=$R/rerun/S_m1_R2.json" "count B1_q0.5 --res=R2 --out=$R/rerun/B1_q0.5_R2.json"; do
  tag=$(echo $c | awk '{print $1"_"$2}' | tr -d '-' | cut -c1-30)
  [ -e $R/rerun/$tag.log ] && continue
  /usr/bin/time -l nice -n 10 $PY bounce.py $c > $R/rerun/$tag.log 2> $R/rerun/$tag.err
  echo "rc=$?" >> $R/rerun/$tag.log
done
echo "rerun done $(date -u +%FT%TZ)" > $R/rerun/done
