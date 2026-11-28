#!/bin/sh
# Run every mutation of settled_mass_eps_scan.py, two at a time, one log per mutation.
# usage (from notes/wormhole_evolution of the worktree): sh run_muts.sh <outdir> <part> <baseline log> [python]
out=$1
part=$2
base=$3
py=${4:-$HOME/Source/negative-mass/.venv/bin/python}
mkdir -p "$out"
run() {
  for m in "$@"; do
    NUMBA_NUM_THREADS=1 nice -n 10 "$py" settled_mass_eps_scan.py analyze --part="$part" --mutate="$m" --baseline="$base" > "$out/$m.log" 2>&1
    echo "$m exit $?" >> "$out/exits.txt"
  done
}
run eps_swap dep_eps rdot_nolapse speed_t1 wj_swap coef_c m0_shift &
run drop_pt no_rscale v3_sign b0_stale exit_last moves_never grid_drop &
wait
echo done >> "$out/exits.txt"
