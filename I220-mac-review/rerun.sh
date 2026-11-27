#!/bin/bash
# The coordinator's rerun of #220's run_01 (sym exch6) and run_05 (values pslq remainder over the stored evaluations), one process, nice 10.
cd $HOME/Source/negative-mass-r220/notes/wormhole_largeD || exit 2
PY=$HOME/Source/negative-mass/.venv/bin/python
export OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
[ -e /Users/nathan/Source/negative-mass-raw/I220-mac-review/rerun_01.log ] || { nice -n 10 $PY order6.py sym exch6 > /Users/nathan/Source/negative-mass-raw/I220-mac-review/rerun_01.log 2>&1; echo "rc=$?" >> /Users/nathan/Source/negative-mass-raw/I220-mac-review/rerun_01.log; }
[ -e /Users/nathan/Source/negative-mass-raw/I220-mac-review/rerun_05.log ] || { nice -n 10 $PY order6.py values pslq remainder --load=/Users/nathan/Source/negative-mass-raw/I220-rpi5/G1.json,/Users/nathan/Source/negative-mass-raw/I220-rpi5/G2.json,/Users/nathan/Source/negative-mass-raw/I220-rpi5/B.json --w2raw=/Users/nathan/Source/negative-mass-raw/I220-rpi5/inputs_w2_growthD.txt > /Users/nathan/Source/negative-mass-raw/I220-mac-review/rerun_05.log 2>&1; echo "rc=$?" >> /Users/nathan/Source/negative-mass-raw/I220-mac-review/rerun_05.log; }
echo done > /Users/nathan/Source/negative-mass-raw/I220-mac-review/rerun_done
