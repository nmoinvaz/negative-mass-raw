#!/bin/zsh
# run_04: the one-time costs the per-evaluation times leave out: the star's Newton shooting and the J table of one l
cd /Users/nathan/Source/negative-mass-i186/phase2/nonradial/taylor_polar
D=/Users/nathan/Source/negative-mass-raw/I186-mac
B=./target/release/taylor_polar
M="omega=0.7603 eps=-1.0 lam=10240.0 mu=21845333.333333336"
{ echo "# $(date '+%Y-%m-%d %H:%M:%S') commit $(git rev-parse --short HEAD) load $(uptime | sed 's/.*load averages*: //')"; } > $D/run_04_setup.log
/usr/bin/time -l nice -n 10 $B star ${=M} >> $D/run_04_setup.log 2>> $D/run_04_setup.err
PCZC=$(grep '"cmd":"star"' $D/run_04_setup.log | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print('pc='+d['pc'], 'zc='+d['zc'])")
for l in 2 6; do for lane in f64 dd; do
  echo "# l=$l lane=$lane" >> $D/run_04_setup.log
  /usr/bin/time -l nice -n 10 $B d lane=$lane l=$l ${=PCZC} ${=M} gammas=1,300 >> $D/run_04_setup.log 2>> $D/run_04_setup.err
done; done
echo done > $D/run_04_setup.rc
