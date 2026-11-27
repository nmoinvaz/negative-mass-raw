#!/bin/bash
# rerun.sh A|B: #39's runs of record on this Mac (chain A: checks numba then numpy; chain B: derive then ind39 run 1)
here=$(cd "$(dirname "$0")" && pwd)
py=/Users/nathan/Source/negative-mass/.venv/bin/python
cd /Users/nathan/Source/negative-mass-r39/notes/wormhole_evolution || exit 2
export OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1
run() { n=$1; shift; [ -e "$here/$n.log" ] && { echo "refusing to overwrite $n.log" >&2; return; }
        { echo "# $(date -u +%FT%TZ) $(uptime)"; /usr/bin/time -l nice -n 10 "$@" 2>&1; echo "exit $?"; } > "$here/$n.log" 2>&1; }
case "$1" in
A) run rerun_checks_numba "$py" checks.py
   run rerun_checks_numpy env DN_NO_NUMBA=1 "$py" checks.py --kernel=numpy ;;
B) run rerun_derive "$py" derive.py
   run ind39_run1 "$py" -u "$here/ind39.py" ;;
esac
