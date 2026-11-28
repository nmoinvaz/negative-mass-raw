#!/bin/bash
# The coordinator's stage 3 rerun (#192): builds, step lists, default mode with lib_table. Logs beside this script.
R=$HOME/Source/negative-mass-raw/I192-mac-review/s3
C=$HOME/Source/negative-mass-r192/phase2/nonradial/taylor_polar
PY=$HOME/Source/negative-mass/.venv/bin/python
mkdir -p $C/target/bins
cd $C
nice -n 10 cargo build --release -j 2 > $R/b1_default.log 2>&1; echo $? > $R/b1_default.rc
cp target/release/taylor_polar target/bins/default
cargo tree -e normal > $R/tree_default.txt 2>&1
nice -n 10 cargo build --release -j 2 --features lib_table > $R/b2_libtable.log 2>&1; echo $? > $R/b2_libtable.rc
cp target/release/taylor_polar target/bins/libtable
cd $HOME/Source/negative-mass-raw/I192-mac
nice -n 10 $PY s3_steps.py --out=$R/steps_out $C/target/bins/default $C/target/bins/libtable > $R/steps.log 2> $R/steps.err; echo $? > $R/steps.rc
for f in $(ls s3_steps_out); do cmp s3_steps_out/$f $R/steps_out/$f && echo "$f equal" || echo "$f DIFFERS"; done > $R/steps_cmp.txt
cd $HOME/Source/negative-mass-r192/phase2/nonradial
nice -n 10 $PY taylor_polar.py --raw=$HOME/Source/negative-mass-raw > $R/default_mode_libtable.log 2> $R/default_mode_libtable.err; echo $? > $R/default_mode_libtable.rc
