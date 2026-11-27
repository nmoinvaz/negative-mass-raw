#!/bin/bash
# rerun.sh: the four runs of record of I208-dh610 on this Mac, from the review worktree; refuses to overwrite a log.
set -u
here=$(cd "$(dirname "$0")" && pwd)
py=/Users/nathan/Source/negative-mass/.venv/bin/python
raw=/Users/nathan/Source/negative-mass-raw/I208-dh610
cd /Users/nathan/Source/negative-mass-r208/notes/wormhole_largeD || exit 2
run() {
    n=$1; shift
    for e in log err rc; do [ -e "$here/$n.$e" ] && { echo "refusing to overwrite $here/$n.$e" >&2; exit 2; }; done
    { date -u +%FT%TZ; uptime; echo "cmd $*"; } >"$here/$n.env"
    /usr/bin/time -l nice -n 10 "$py" -u "$@" >"$here/$n.log" 2>"$here/$n.err"
    echo $? >"$here/$n.rc"
}
run rerun_run_01_sym order5.py sym
run rerun_run_02_evals_pslq_remainder order5.py evals pslq remainder --save="$here/rerun_run_02_evals.json" \
    --w2raw="$raw/inputs_w2_growthD.txt"
run rerun_run_03_closedform order5.py closedform --load="$here/rerun_run_02_evals.json"
run rerun_run_04_reduce5_a5 order5.py reduce5 a5 --load="$here/rerun_run_02_evals.json"
