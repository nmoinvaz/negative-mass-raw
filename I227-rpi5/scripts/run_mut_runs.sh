#!/bin/bash
# The run-level mutations of extended_bisect.py (each mutated bisection/series is a run, its effect read by `analyze --only=`). Usage: run_mut_runs.sh OUTDIR PSTARDIR LANE
# OUTDIR holds one folder per mutation; PSTARDIR has the unmutated bisect.json of variant E (its p*). LANE A or B (two lanes, one process each, nice 10).
OUT=$1; PSD=$2; LANE=$3
NR=$HOME/Source/negative-mass-i227/notes/wormhole_evolution; PY=$HOME/Source/negative-mass-venv314/bin/python
export OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1
cd "$NR" || exit 2
PS=$($PY - "$PSD" <<'PYEOF'
import json, sys
b = json.load(open(sys.argv[1] + "/bisect.json"))
print(repr(0.5 * (float(b["lo"]) + float(b["hi"]))))
PYEOF
)
brk() { $PY -c "p=$PS; w=$1; print(f'--lo={p-w!r} --hi={p+w!r}')"; }
run() { name=$1; shift; mkdir -p "$OUT/$name"; echo "$(date -Is) start $name"; nice -n 10 "$@" > "$OUT/$name/log.txt" 2> "$OUT/$name/err.txt"; echo $? > "$OUT/$name/rc"; echo "$(date -Is) end $name rc=$(cat $OUT/$name/rc)"; }
if [ "$LANE" = A ]; then
  run float_cast_E   $PY extended_bisect.py bisect --D=4 --h=0.02 --variant=E --mutate=float_cast $(brk 1e-14) --tol=1e-24 --out=$OUT/float_cast_E
  run float_cast_P16 $PY extended_bisect.py bisect --D=4 --h=0.02 --variant=E --mutate=float_cast --eta-scale=1e-16 $(brk 1e-14) --tol=1e-24 --out=$OUT/float_cast_P16
  run h_wrong        $PY extended_bisect.py bisect --D=4 --h=0.02 --variant=E --mutate=h_wrong --lo=4.0e-05 --hi=6.0e-05 --tol=1e-12 --out=$OUT/h_wrong
else
  run noise_f64      $PY extended_bisect.py bisect --D=4 --h=0.02 --variant=E --mutate=noise_f64 $(brk 1e-11) --tol=1e-24 --out=$OUT/noise_f64
  run noise_f64_series $PY extended_bisect.py series --D=4 --h=0.02 --elist=3,6,9,11,12,13,14,15,16,18,20 --mutate=noise_f64 --out=$OUT/noise_f64
  run eta_dropped    $PY extended_bisect.py bisect --D=4 --h=0.02 --variant=E --mutate=eta_dropped --eta-scale=1e-16 $(brk 1e-14) --tol=1e-24 --out=$OUT/eta_dropped
fi
