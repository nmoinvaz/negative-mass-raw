#!/bin/bash
# extended_bisect_output.txt of the negative-mass note: the controls, the analysis of the runs of record, the mutation tables. Run from this folder:  scripts/make_output.sh > OUT
RAW=$(cd "$(dirname "$0")/.." && pwd)
NR=$HOME/Source/negative-mass-i227/notes/wormhole_evolution; PY=$HOME/Source/negative-mass-venv314/bin/python
cd "$NR" || exit 2
echo "== python3 extended_bisect.py controls =="
$PY extended_bisect.py controls; echo "exit $?"
echo
echo "== python3 extended_bisect.py analyze --raw=<negative-mass-raw>/I227-rpi5 =="
$PY extended_bisect.py analyze --raw=$RAW; echo "exit $?"
echo
echo "== mutations: analysis level (scripts/mut_table.py analyze), controls level (mut_table.py controls), run level (mut_runs_table.py) =="
cat $RAW/mut/analysis_table.txt
cat $RAW/mut/controls_table.txt
cat $RAW/mut/runlevel_table.txt
