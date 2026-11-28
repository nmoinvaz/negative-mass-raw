#!/bin/sh
# usage: run_pairs.sh OUTROOT   (the seven new pairs at e = 9, two at a time, nice 10, one thread each; logs and rc beside the output)
RAW="$HOME/Source/negative-mass-raw/I318-mac"
PY="$HOME/Source/negative-mass/.venv/bin/python"
SCRIPT="$HOME/Source/negative-mass-i318/notes/wormhole_evolution/settled_mass_second.py"
OUT="$1"
mkdir -p "$OUT/logs"
run_one() {
  n="$1"
  d="$OUT/runs/$n/h0.005/e9"
  mkdir -p "$d"
  NUMBA_NUM_THREADS=1 nice -n 10 "$PY" "$SCRIPT" pair --member="$n" --e=9 --out="$d/member" --pstore="$RAW/pstar_store" > "$OUT/logs/$n.log" 2> "$OUT/logs/$n.err"
  echo $? > "$OUT/logs/$n.rc"
}
export RAW PY SCRIPT OUT
for n in W3 C3 N3 B0.125 X1 X2 X3; do
  run_one "$n" &
  # at most two at a time
  while [ "$(jobs -r | wc -l)" -ge 2 ]; do sleep 2; done
done
wait
echo done > "$OUT/logs/ALL.done"
