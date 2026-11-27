#!/bin/bash
# run 2 of the spectral check, with the results directory the runner's command passed (the Mac's own member results)
here=$(cd "$(dirname "$0")" && pwd)
until [ -e "$here/results/member_-0.01_R2.log" ] && grep -q "^exit" "$here/results/member_-0.01_R2.log"; do sleep 20; done
cd /Users/nathan/Source/negative-mass-r212/notes/black_universe || exit 2
{ echo "# $(date -u +%FT%TZ) $(uptime) (run 2: with the results directory)"; OMP_NUM_THREADS=1 /usr/bin/time -l nice -n 10 \
  /Users/nathan/Source/negative-mass/.venv/bin/python stability.py spectral "$here/results" 2>&1; echo "exit $?"; } > "$here/rerun_spectral_2.log" 2>&1
