#!/bin/bash
# run_controls.sh PREFIX : every control of exchange_review.py in turn (serial), log PREFIX_<name>.log in this folder
# usage: systemd-run --user --unit=nm-i209-<name> --working-directory=<worktree>/notes/wormhole_largeD nice -n 10 ./run_controls.sh dev_ctl [NAME...]
# with NAMEs, only those controls run
prefix="$1"; shift
only=" $* "
here="$(cd "$(dirname "$0")" && pwd)"
py=/home/nathan/Source/negative-mass-venv314/bin/python
while read -r name parts; do
  [ -z "$name" ] && continue
  if [ -n "$*" ] && [[ "$only" != *" $name "* ]]; then continue; fi
  "$here/run_logged.sh" "$here/${prefix}_${name}.log" "$py" -u exchange_review.py $parts --mutate="$name"
done <<'LIST'
sym_S1 sym
sym_S2 sym
sym_c1 sym
sym_P sym
sym_S6 sym
sym_S7 sym
sym_S8 sym
sym_S9 sym
sym_S10 sym
sym_S11 sym
exact_K exact
exact_L1 exact
exact_h2 exact
e1_sign exact exch
e1_factor exact exch
e2_weight exact exch
bnd_G exch
bnd_Y0 exch
e3_Om0 exch
e3_factor exch
cl_moment clausen
cl_arg clausen
cl_arg2 clausen
grid_coarse grid
grid_short grid
grid_wrongh grid
grid_wrongOm1 grid
LIST
