#!/bin/bash
# usage: run_muts.sh PART OUTDIR BASELOG   (PART = dev or record); one mutation at a time, nice 10, one thread, logs never overwritten (a numbered rerun)
PART="$1"; OUT="$2"; BASE="$3"
SCRIPT="$HOME/Source/negative-mass-i296/notes/wormhole_evolution/settled_mass_eps.py"
PY="$HOME/Source/negative-mass/.venv/bin/python"
export NUMBA_NUM_THREADS=1
mkdir -p "$OUT"
for M in asym_sign coef_a coef_c dep_eps drop_point eps_swap loo_off m0_shift no_rscale no_run no_speed rdot_nolapse; do
  N=0; LOG="$OUT/$M.log"
  while [ -e "$LOG" ]; do N=$((N+1)); LOG="$OUT/$M.$N.log"; done
  nice -n 10 "$PY" "$SCRIPT" analyze --part="$PART" --mutate="$M" --baseline="$BASE" > "$LOG" 2> "${LOG%.log}.err"
  echo "$M rc=$? $(grep '^mutation ' "$LOG" | cut -c1-400)"
done
