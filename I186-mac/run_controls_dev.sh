#!/bin/zsh
# development run of every control: each --mutate=NAME runs only its targeted checks and must exit 1
cd /Users/nathan/Source/negative-mass-i186/phase2/nonradial
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
for m in jsign dropterm lin_drop recip_dd noqr star_eps zc1 start_term shift_off wide_table moncrief swapcols mext0 qstart; do
  /Users/nathan/Source/negative-mass-raw/I186-mac/devrun.sh control_$m $PY taylor_polar.py --mutate=$m
done
echo done > /Users/nathan/Source/negative-mass-raw/I186-mac/run_controls_dev.finished
