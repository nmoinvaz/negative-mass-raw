#!/bin/sh
# usage: run_muts.sh RUNS_DIR OUTDIR BASELINE_LOG [N]   (every mutation of settled_mass_second.py on one set of pairs; absolute paths)
RAW="$HOME/Source/negative-mass-raw/I318-mac"
PY="$HOME/Source/negative-mass/.venv/bin/python"
SCRIPT="$HOME/Source/negative-mass-i318/notes/wormhole_evolution/settled_mass_second.py"
RUNS="$1"; OUT="$2"; BASE="$3"; N="${4:-1}"
mkdir -p "$OUT"
for mu in eps_swap d_sign b0_scale same_moment_off plant_ratio m1_sign dv_scale rep_off m0_shift bis_off zone_one_path run_miss cfg_e v3_coef dep_eps lam_off; do
  NUMBA_NUM_THREADS=1 nice -n 10 "$PY" "$SCRIPT" analyze --raw="$RAW" --runs="$RUNS" --mutate=$mu --baseline="$BASE" > "$OUT/$mu.$N.log" 2> "$OUT/$mu.$N.err"
  echo "$mu rc=$? $(grep '^mutation ' "$OUT/$mu.$N.log" | cut -c1-400)"
done
