#!/bin/bash
# rerun.sh A|B: #212's runs of record on this Mac, from the review worktree; refuses to overwrite a log.
here=$(cd "$(dirname "$0")" && pwd)
py=/Users/nathan/Source/negative-mass/.venv/bin/python
cd /Users/nathan/Source/negative-mass-r212/notes/black_universe || exit 2
export OMP_NUM_THREADS=1
run() { n=$1; shift; [ -e "$here/$n.log" ] && { echo "refusing to overwrite $n.log" >&2; return; }
        { echo "# $(date -u +%FT%TZ) $(uptime)"; /usr/bin/time -l nice -n 10 "$py" "$@" 2>&1; echo "exit $?"; } > "$here/$n.log" 2>&1; }
case "$1" in
A) run rerun_check stability.py check; run rerun_planted stability.py planted; run rerun_spectral stability.py spectral
   run rerun_controls stability.py controls ;;
B) mkdir -p "$here/results"
   for c in -10 -3 -2 -1.5 -1.1 -1.01 -1.001 -1.0001 -1.0 -0.9999 -0.999 -0.99 -0.95 -0.9 -0.7 -0.5 -0.3 -0.2 -0.1 -0.01; do
     for r in R1 R2; do run results/member_${c}_$r stability.py count $c --res=$r --out="$here/results/member_${c}_$r.json"; done
   done ;;
esac
