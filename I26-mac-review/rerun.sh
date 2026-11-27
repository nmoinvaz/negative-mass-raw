#!/bin/bash
# rerun.sh A|B: the runs of record of I26-dh610 on this Mac, from the review worktree; refuses to overwrite a log.
set -u
here=$(cd "$(dirname "$0")" && pwd)
py=/Users/nathan/Source/negative-mass/.venv/bin/python
cd /Users/nathan/Source/negative-mass-r26/notes/wormhole_largeD || exit 2
run() {
    n=$1; shift
    for e in log err rc; do [ -e "$here/$n.$e" ] && { echo "refusing to overwrite $here/$n.$e" >&2; exit 2; }; done
    { date -u +%FT%TZ; uptime; echo "cmd $*"; } >"$here/$n.env"
    /usr/bin/time -l nice -n 10 "$py" -u "$@" >"$here/$n.log" 2>"$here/$n.err"
    echo $? >"$here/$n.rc"
}
case "$1" in
A) run rerun_run_02_n4b order4.py n4b ;;
B) run rerun_run_01_sym_closed_reduce order4.py sym closed reduce
   run rerun_run_03_n4bg order4.py n4bg
   run rerun_run_04_evals_remainder order4.py evals remainder \
       --w2raw=/Users/nathan/Source/negative-mass-raw/I26-dh610/inputs_w2_growthD.txt
   run rerun_run_05_lc2 order4.py lc2 ;;
*) echo "usage: rerun.sh A|B" >&2; exit 2 ;;
esac
