#!/bin/bash
# mutation queue 1: one run at a time (the 5 new-section controls, then 10 old+new); logs mut_<name>.log/.rc/.time here
RAW=$(cd "$(dirname "$0")" && pwd)
for m in largex centre scale lelimit lefv; do "$RAW/run_step.sh" mut_$m --mutate=$m --section=new; done
for m in printedW matrix planted xmap units tfactor count domain potential background; do "$RAW/run_step.sh" mut_$m --mutate=$m; done
echo done > "$RAW/queue_mut1.done"
