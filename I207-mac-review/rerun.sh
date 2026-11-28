#!/bin/zsh
# The coordinator's rerun of #207 at 2701c5d: the ctl grid with the default build (off) and with --features locate_lib (on).
R=$HOME/Source/negative-mass-raw/I207-mac-review
W=$HOME/Source/negative-mass-r207
PY=$HOME/Source/negative-mass/.venv/bin/python
export RAYON_NUM_THREADS=2
cd $W/notes/warp/conical_global
nice -n 10 cargo build --release -j 2 > $R/b_off.log 2>&1; echo $? > $R/b_off.rc
cd $W
mkdir -p $R/dump_off
nice -n 10 $PY notes/warp/conical_offgrid.py --nobuild --grid=ctl --no-controls --dump=$R/dump_off > $R/off_ctl.log 2> $R/off_ctl.err; echo $? > $R/off_ctl.rc
cd $W/notes/warp/conical_global
nice -n 10 cargo build --release -j 2 --features locate_lib > $R/b_on.log 2>&1; echo $? > $R/b_on.rc
cd $W
mkdir -p $R/dump_on
nice -n 10 $PY notes/warp/conical_offgrid.py --nobuild --grid=ctl --no-controls --dump=$R/dump_on > $R/on_ctl.log 2> $R/on_ctl.err; echo $? > $R/on_ctl.rc
