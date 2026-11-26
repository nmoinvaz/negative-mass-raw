#!/bin/zsh
# rerun.sh A|B|C: the coordinator's rerun of #195's runs of record (I195-dh610's .env commands, paths mapped to this Mac)
R=/Users/nathan/Source/negative-mass-raw/I195-mac-review
W=/Users/nathan/Source/negative-mass-r195/notes/wormhole_largeD
cd $W
run() { local n=$1; local c=$(grep "^$n|" $R/cmds.txt | cut -d'|' -f2-); { echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC load $(uptime | sed 's/.*load averages*: //')"; echo "# cmd: $c"; } > $R/rerun_$n.env
  /usr/bin/time -l ${=c} > $R/rerun_$n.log 2> $R/rerun_$n.err; echo $? > $R/rerun_$n.rc; }
case $1 in
A) for n in run_01_planted_f64 run_01_planted_dd run_01_planted_qd run_02_w2_qd_growth run_03_w2_qd_Dlist run_01_planted_od_D5_50 run_01_planted_od_D1000_10000 run_04_w2_od_Dlist_p2; do run $n; done ;;
B) for n in run_04_w2_od_Dlist_p0 run_04_w2_od_Dlist_p1; do run $n; done ;;
C) run run_08_driver_final ;;
esac
echo done > $R/rerun_$1.done
