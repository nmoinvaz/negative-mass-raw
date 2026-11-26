#!/bin/zsh
# development runs of the controls of --rows mode, one process at a time
cd /Users/nathan/Source/negative-mass-i187/phase2/nonradial
for c in qint_cofsign qint_f rm_off1 rm_cut r0_grid qstart moncrief tol_loose; do
  /Users/nathan/Source/negative-mass-raw/I187-mac/devrun.sh ctl_$c /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --rows --mutate=$c
done
