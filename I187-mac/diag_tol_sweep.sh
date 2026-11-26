#!/bin/zsh
# development: D at (l = 5, gamma = 6000), dd, order 30, base r_m, for a sweep of the Taylor tolerance; the dd default is 1.2e-30
cd /Users/nathan/Source/negative-mass-i187/phase2/nonradial
BIN=taylor_polar/target/release/taylor_polar
M="omega=0.7603 eps=-1.0 lam=10240.0 mu=21845333.333333336"
line=$($BIN star ${=M} | head -1)
pc=$(echo "$line" | python3 -c "import json,sys;print(json.load(sys.stdin)['pc'])")
zc=$(echo "$line" | python3 -c "import json,sys;print(json.load(sys.stdin)['zc'])")
for tol in 1.2e-30 1e-12 1e-3 1e-2 1e-1 1 10; do
  echo "# tol = $tol"
  $BIN d lane=dd l=5 gammas=6000 rm=24.10980364018201 tol=$tol pc=$pc zc=$zc ${=M} | python3 -c "
import json,sys
for x in sys.stdin:
    o=json.loads(x)
    if o['cmd']=='d': print('D', o['d'][:22], 'steps_y', o['steps_y'], 'wall', o['wall'])
"
done
