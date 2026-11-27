#!/bin/bash
# the development record: D = 4 only, to compute the targets of the checks that need stored runs. usage: devrec_all.sh LANE (1, 2 or 3)
R=$HOME/Source/negative-mass-raw/I225-dh610
L=$R/scripts/devrec_lane.sh
O=$R/dev/rec
case $1 in
1) $L series_D4_hk1 series --D=4 --hk=1 --out=$O/series/D4_G_h0.01
   $L planted_D4_v0.1 planted --D=4 --hk=0 --v=0.1 --out=$O/planted ;;
2) $L series_D4_hk0 series --D=4 --hk=0 --out=$O/series/D4_G_h0.02
   $L stall_D4_hk0 stall --D=4 --hk=0 --out=$O/stall
   $L stall_D4_hk1 stall --D=4 --hk=1 --out=$O/stall
   $L expand_S_D4_0.05_hk0 expand --D=4 --hk=0 --member=0.05 --X=200 --family=S --out=$O/expand ;;
3) for hk in 0 1; do for m in tuned 0.05; do $L expand_G_D4_${m}_hk$hk expand --D=4 --hk=$hk --member=$m --X=100 --family=G --out=$O/expand; done; done ;;
esac
