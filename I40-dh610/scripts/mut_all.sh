#!/bin/bash
# the mutation runs of record, one after the other (flags as in the development runs dev_14 and dev_17)
S=$(dirname "$(readlink -f "$0")")
$S/mut.sh bisect_loose --ed
$S/mut.sh ed_unit --ed
$S/mut.sh no_corrector --ed
for m in theta_coef ghost_sign finder_sign; do $S/mut.sh $m --ed; done
for m in ellis_charge scalar_coef data_constraint_sign; do $S/mut.sh $m; done
$S/mut.sh g6 time_unit
