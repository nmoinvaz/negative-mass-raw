#!/bin/bash
# Two chains of run_cross.sh, each one process: ./run_cross_chain.sh A | B
HERE=$(cd "$(dirname "$0")" && pwd)
if [ "$1" = A ]; then
  "$HERE/run_cross.sh" n3_l2 cross_n3_l2
  "$HERE/run_cross.sh" n3_l2 cross_n3_l2_shift --mutate=shift
else
  "$HERE/run_cross.sh" n3_l3 cross_n3_l3
  "$HERE/run_cross.sh" n3_l2_flat cross_n3_l2_flat --flat
fi
