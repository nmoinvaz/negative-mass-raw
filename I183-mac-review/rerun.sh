#!/bin/zsh
# rerun.sh: the coordinator's rerun of #183, from a detached worktree at 9debda2: stage a of the run of record, then the
# default modes of conical_global.py (#167) and conical_loglog.py (#184), nice 10, RAYON_NUM_THREADS=2
R=/Users/nathan/Source/negative-mass-raw/I183-mac-review
P=/Users/nathan/Source/negative-mass/.venv/bin/python
cd /Users/nathan/Source/negative-mass-r183
export RAYON_NUM_THREADS=2
run() { local n=$1; shift; { echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC load $(uptime | sed 's/.*load averages*: //')"; echo "# cmd: $*"; } > $R/rerun_$n.env
  /usr/bin/time -l nice -n 10 "$@" > $R/rerun_$n.log 2> $R/rerun_$n.err; echo $? > $R/rerun_$n.rc; }
run 03a $P notes/warp/conical_offgrid.py --no-controls --dump=$R/dump_rerun_03a --only=n_table,series_hp,plant_167,plant_far,regress167,scan,spread,modes,symmetry,n4_factor,closed_form,bisect,independent,recip_check,step_halving
run global_default $P notes/warp/conical_global.py
run loglog_default $P notes/warp/conical_loglog.py
echo done > $R/rerun.done
