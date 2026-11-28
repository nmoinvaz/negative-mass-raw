#!/bin/bash
# runs of record: the full driver, then (second script) the controls. Logs are never overwritten: numbered.
cd ~/Source/negative-mass-i272/notes/wormhole_evolution
PY=~/Source/negative-mass/.venv/bin/python
RAW=~/Source/negative-mass-raw/I272-mac/runs
nice -n 10 $PY ellis_spectrum.py run > $RAW/run_01_full.log 2> $RAW/run_01_full.err
echo $? > $RAW/run_01_full.rc
