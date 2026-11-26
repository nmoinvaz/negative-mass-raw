#!/bin/zsh
# run_03: every control (--mutate=NAME runs the checks it targets with one deliberate error; each must exit 1)
cd /Users/nathan/Source/negative-mass-i186/phase2/nonradial
D=/Users/nathan/Source/negative-mass-raw/I186-mac
{ echo "# $(date '+%Y-%m-%d %H:%M:%S') commit $(git rev-parse --short HEAD) load $(uptime | sed 's/.*load averages*: //')"; } > $D/run_03_controls.log
for m in jsign lowsum lin_drop recip_dd noqr star_eps zc1 start_term shift_off wide_table moncrief swapcols mext0 qstart; do
  echo "##### control $m" >> $D/run_03_controls.log
  RAYON_NUM_THREADS=2 nice -n 10 /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --mutate=$m >> $D/run_03_controls.log 2>> $D/run_03_controls.err
  echo "exit $?" >> $D/run_03_controls.log
done
echo done > $D/run_03_controls.rc
