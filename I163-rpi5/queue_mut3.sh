#!/bin/bash
# queue 3: the unmutated rerun and the two controls rerun after the code changes of README amendment 8
RAW=$(cd "$(dirname "$0")" && pwd)
"$RAW/run_step.sh" final_run2
"$RAW/run_step.sh" mut_centre_run2 --mutate=centre --section=new
"$RAW/run_step.sh" mut_xmap_run2 --mutate=xmap
echo done > "$RAW/queue_mut3.done"
