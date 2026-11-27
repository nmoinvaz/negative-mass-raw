#!/bin/bash
# usage: run_ts13_mutations.sh OUTDIR   (run from anywhere; one process at a time, nice 10)
# Runs ts13_digits.py unmutated and with each --mutate=NAME of the script's MUTATIONS table; one log each; prints
# "mutation  failed checks (exit N)" in the form compare_targets.py reads.
OUT=${1:?outdir}
PY=~/Source/negative-mass-venv314/bin/python
SCRIPT=~/Source/negative-mass-i221/notes/wormhole_largeD/ts13_digits.py
mkdir -p "$OUT"
names=$(cd "$(dirname "$SCRIPT")" && $PY -c "import ts13_digits as t; print(' '.join(t.MUTATIONS))")
for m in none $names; do
  f="$OUT/$m.log"
  if [ "$m" = none ]; then (cd "$(dirname "$SCRIPT")" && nice -n 10 $PY "$SCRIPT") > "$f" 2>&1; else (cd "$(dirname "$SCRIPT")" && nice -n 10 $PY "$SCRIPT" --mutate="$m") > "$f" 2>&1; fi
  echo "exit $?" >> "$f"
  fired=$(grep -E '^FAIL    ' "$f" | sed -E 's/^FAIL    ([A-Z0-9]+):.*/\1/' | sort | tr '\n' ' ' | sed 's/ $//')
  printf '%-12s %s (%s)\n' "$m" "${fired:-none}" "$(tail -1 "$f")"
done
