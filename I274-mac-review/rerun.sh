#!/bin/zsh
# The coordinator's rerun of #274 at 6f91397: build, stars, the boxes s1_l6 and s2_l2 into rerun/, then the collector on I274-mac.
R=$HOME/Source/negative-mass-raw/I274-mac-review
PY=$HOME/Source/negative-mass/.venv/bin/python
cd $HOME/Source/negative-mass-r274/phase2/nonradial
export RAYON_NUM_THREADS=2
nice -n 10 $PY taylor_polar.py --complex --build > $R/rr_build.log 2>&1; echo $? > $R/rr_build.rc
nice -n 10 $PY -u recount_i274.py --raw=$HOME/Source/negative-mass-raw --out-dir=$R/rerun --stars > $R/rr_stars.log 2> $R/rr_stars.err; echo $? > $R/rr_stars.rc
nice -n 10 $PY -u recount_i274.py --raw=$HOME/Source/negative-mass-raw --out-dir=$R/rerun --boxes=s1_l6,s2_l2 > $R/rr_boxes.log 2> $R/rr_boxes.err; echo $? > $R/rr_boxes.rc
nice -n 10 $PY recount_i274.py --raw=$HOME/Source/negative-mass-raw --collect --extra > $R/rr_collect.txt 2> $R/rr_collect.err; echo $? > $R/rr_collect.rc
