#!/bin/bash
# after the full run: the two mutations again with the final script (INSPIRE base queries parenthesized)
cd "$(dirname "$0")"
PY=$HOME/Source/negative-mass-venv314/bin/python
until [ -f full_done ]; do sleep 5; done
nice -n 10 $PY -I rerun_queries.py --subset=control --mutate=window --out=rerun_ctl_window > ctl_window.log 2>&1; echo $? > ctl_window.rc
nice -n 10 $PY -I rerun_queries.py --subset=control --mutate=terms --out=rerun_ctl_terms > ctl_terms.log 2>&1; echo $? > ctl_terms.rc
nice -n 10 $PY -I rerun_queries.py --subset=control --out=rerun_ctl_plain > ctl_plain.log 2>&1; echo $? > ctl_plain.rc
echo done > ctl2_done
