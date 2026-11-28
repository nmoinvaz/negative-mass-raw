#!/bin/bash
# usage: run_muts.sh PART BASELINE_LOG OUTDIR SERIAL   (e.g. dev .../analyze_dev.1.log .../dev/mut 1)
# one mutated analysis per name, one log per run: OUTDIR/<name>.<SERIAL>.log (never overwritten)
part="$1"; base="$2"; out="$3"; serial="$4"
script="$HOME/Source/negative-mass-i317/notes/wormhole_evolution/settled_mass_blind.py"
py="$HOME/Source/negative-mass/.venv/bin/python"
export NUMBA_NUM_THREADS=1
names="${5:-coef_a coef_c m0_shift no_rscale no_speed eps_swap dep_eps rdot_nolapse asym_sign no_run bar_shift no_subtract sub_sign sub_r_only sub_v_only keep_e12 stale_frozen test_swap x_loader_h git_untracked b0_eps parse_wrong no_member_dep}"
mkdir -p "$out"
for n in $names; do
  f="$out/$n.$serial.log"
  if [ -e "$f" ]; then echo "exists: $f" >&2; exit 2; fi
  nice -n 10 "$py" "$script" analyze --part="$part" --mutate="$n" --baseline="$base" > "$f" 2> "$out/$n.$serial.err"
  echo "$n exit $? : $(tail -1 "$f" | cut -c1-300)"
done
