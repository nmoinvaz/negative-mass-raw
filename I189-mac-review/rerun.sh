#!/bin/zsh
# rerun.sh: the coordinator's rerun of #189's crate switch, feature lib_plane on, from a worktree at 6c40e02; one lane, nice 10
W=/Users/nathan/Source/negative-mass-r189/nm/phase2/nonradial
R=/Users/nathan/Source/negative-mass-raw/I189-mac-review
P=/Users/nathan/Source/negative-mass/.venv/bin/python
cd $W
run() { local n=$1; shift; { echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC load $(uptime | sed 's/.*load averages*: //')"; echo "# cmd: $*"; } > $R/rerun_$n.log
  RAYON_NUM_THREADS=2 /usr/bin/time -l nice -n 10 "$@" >> $R/rerun_$n.log 2> $R/rerun_$n.err; echo $? > $R/rerun_$n.rc; }
run rows_l2 $P taylor_polar.py --rows --only=RA2,RX --jsonl-dir=$R/jsonl
run rows_l4 $P taylor_polar.py --rows --only=RA4 --jsonl-dir=$R/jsonl
run rows_l6_cap6 $P taylor_polar.py --rows --only=RA6,CAP6 --jsonl-dir=$R/jsonl
run default_mode $P taylor_polar.py
echo done > $R/rerun.done
