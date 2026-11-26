#!/bin/zsh
# rerun.sh A|B: the coordinator's rerun of #187's runs of record from a worktree at 2a84083, two lanes, nice 10
W=/Users/nathan/Source/negative-mass-r187/phase2/nonradial
R=/Users/nathan/Source/negative-mass-raw/I187-mac-review
P=/Users/nathan/Source/negative-mass/.venv/bin/python
cd $W
run() { local n=$1; shift; { echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC load $(uptime | sed 's/.*load averages*: //')"; echo "# cmd: $*"; } > $R/rerun_$n.log
  RAYON_NUM_THREADS=2 /usr/bin/time -l nice -n 10 "$@" >> $R/rerun_$n.log 2> $R/rerun_$n.err; echo $? > $R/rerun_$n.rc; }
if [[ $1 == A ]]; then
  run rows_l2 $P taylor_polar.py --rows --only=RA2,RX --jsonl-dir=$R/jsonl
  run rows_l4 $P taylor_polar.py --rows --only=RA4 --jsonl-dir=$R/jsonl
  run rows_l5_cap5 $P taylor_polar.py --rows --only=RA5,CAP5,CAP5s --jsonl-dir=$R/jsonl
  run rows_l3 $P taylor_polar.py --rows --only= --print-rows=3 --jsonl-dir=$R/jsonl
else
  run rows_l6_cap6 $P taylor_polar.py --rows --only=RA6,CAP6 --jsonl-dir=$R/jsonl
  run default_mode $P taylor_polar.py
fi
echo done > $R/rerun_$1.done
