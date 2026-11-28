#!/bin/sh
# baseline then every mutation, on the development pairs; usage: dev_all.sh N   (N = the run number of the logs)
RAW="$HOME/Source/negative-mass-raw/I318-mac"
PY="$HOME/Source/negative-mass/.venv/bin/python"
SCRIPT="$HOME/Source/negative-mass-i318/notes/wormhole_evolution/settled_mass_second.py"
N="$1"
NUMBA_NUM_THREADS=1 nice -n 10 "$PY" "$SCRIPT" analyze --raw="$RAW" --runs="$RAW/dev/runs_dev/runs" > "$RAW/dev/analyze_dev.$N.log" 2> "$RAW/dev/analyze_dev.$N.err"
echo "baseline rc=$?"
sh "$RAW/scripts/run_muts.sh" "$RAW/dev/runs_dev/runs" "$RAW/dev/mut" "$RAW/dev/analyze_dev.$N.log" "$N"
echo done
