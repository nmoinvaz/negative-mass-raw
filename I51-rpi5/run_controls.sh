#!/bin/bash
# runs the control subset plain and with each mutation; each must give the expected exit code (plain 0, mutated 1)
cd "$(dirname "$0")"
PY=$HOME/Source/negative-mass-venv314/bin/python
nice -n 10 $PY -I rerun_queries.py --subset=control --out=rerun_ctl_plain > ctl_plain.log 2>&1; echo $? > ctl_plain.rc
nice -n 10 $PY -I rerun_queries.py --subset=control --mutate=window --out=rerun_ctl_window > ctl_window.log 2>&1; echo $? > ctl_window.rc
nice -n 10 $PY -I rerun_queries.py --subset=control --mutate=terms --out=rerun_ctl_terms > ctl_terms.log 2>&1; echo $? > ctl_terms.rc
echo done > ctl_done
