#!/bin/bash
# waits for the control runs, then runs the full rerun (nice 10)
cd "$(dirname "$0")"
until [ -f ctl_done ]; do sleep 5; done
nice -n 10 $HOME/Source/negative-mass-venv314/bin/python -I rerun_queries.py --out=rerun > full.log 2>&1; echo $? > full.rc
echo done > full_done
