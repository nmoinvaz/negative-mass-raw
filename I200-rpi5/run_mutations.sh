#!/bin/bash
# usage: run_mutations.sh OUTDIR   (run from anywhere; one process at a time, nice 10)
# Runs check_growth.py unmutated and with every mutation; prints "mutation -> failed checks" and writes one log each.
OUT=${1:?outdir}
PY=~/Source/negative-mass-venv314/bin/python
CG=~/Source/negative-mass-i200/notes/wormhole_largeD/check_growth.py
mkdir -p "$OUT"
muts=(none ts13_swap crate_scale round_trunc list50 wrong_om2 wrong_om3 s_off)
for D in 4 5 6 7 8 9 10 11 20 30 50 100 200 500 1000 2000; do muts+=("last_digit:$D" "drop_row:$D" "source:$D"); done
for m in "${muts[@]}"; do
  f="$OUT/$(echo "$m" | tr ':' '_').log"
  if [ "$m" = none ]; then nice -n 10 $PY $CG > "$f" 2>&1; else nice -n 10 $PY $CG --mutate="$m" > "$f" 2>&1; fi
  echo "exit $?" >> "$f"
  printf '%-16s %s\n' "$m" "$(grep '^failed:' "$f" | sed 's/^failed: //') ($(tail -1 "$f"))"
done
