#!/bin/zsh
# does the crate's D (rows) react to the star's start radius rs? l = 2, gamma = 1, base variant only; prints mext, star steps, D, q
cd /Users/nathan/Source/negative-mass-i187/phase2/nonradial
for rs in 1e-8 1e-6 1e-3; do
  echo "# rs = $rs"
  line=$(taylor_polar/target/release/taylor_polar star omega=0.7603 eps=-1.0 lam=10240.0 mu=21845333.333333336 rs=$rs | head -1)
  echo "$line" | cut -c1-200
  pc=$(echo "$line" | python3 -c "import json,sys;print(json.load(sys.stdin)['pc'])")
  zc=$(echo "$line" | python3 -c "import json,sys;print(json.load(sys.stdin)['zc'])")
  taylor_polar/target/release/taylor_polar rows l=2 lane=dd variants=base gammas=1 pc=$pc zc=$zc rs=$rs omega=0.7603 eps=-1.0 lam=10240.0 mu=21845333.333333336 | python3 -c "
import json,sys
for x in sys.stdin:
    o=json.loads(x)
    if o['cmd']=='rowsetup': print('setup star_steps', o['star_steps'])
    else: print('D', o['d'][:28], 'q_int', o['q_int'][:22], 'mext', o['mext'][:30], 'rm', o['rm'])
"
done
