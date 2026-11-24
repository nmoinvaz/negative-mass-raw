#!/bin/bash
# queue 2: the final run, then the 17 mutations (5 new-section controls with --section=new, 12 full), one process at a time
RAW=$(cd "$(dirname "$0")" && pwd)
"$RAW/run_step.sh" final
for m in largex centre scale lelimit lefv; do "$RAW/run_step.sh" mut_$m --mutate=$m --section=new; done
for m in printedW matrix planted xmap units tfactor count domain potential background deltaphi cpath; do "$RAW/run_step.sh" mut_$m --mutate=$m; done
echo done > "$RAW/queue_mut2.done"
