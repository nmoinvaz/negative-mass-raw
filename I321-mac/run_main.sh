#!/bin/sh
# usage: run_main.sh CMD...   runs of record, one process each, nice 10; logs RAW/runs/CMD.log, resources RAW/runs/CMD.time, exit RAW/runs/CMD.exit
RAW="$HOME/Source/negative-mass-raw/I321-mac"
cd "$HOME/Source/negative-mass-i321/notes/black_universe" || exit 2
for CMD in "$@"; do
  /usr/bin/time -l nice -n 10 "$HOME/Source/negative-mass/.venv/bin/python" log_at_S.py "$CMD" > "$RAW/runs/$CMD.log" 2> "$RAW/runs/$CMD.time"
  echo $? > "$RAW/runs/$CMD.exit"
done
