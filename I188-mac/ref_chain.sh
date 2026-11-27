#!/bin/zsh
# the scipy references after run_01: b1 at rtol 1e-8 (the stored rtol) on the 8 timing points, then l = 6 (b6) at rtol 1e-13 and 1e-8 on its 8 points; one process at a time
D=$(cd "$(dirname "$0")" && pwd)
PY=$HOME/Source/negative-mass/.venv/bin/python
cd $HOME/Source/negative-mass-i188/phase2/nonradial
$D/runrec.sh scipy_ref_b1_rtol1e-08_tc $PY -u taylor_polar.py --complex --scipy-ref-make=b1 --rtol=1e-8 --points=tc --out=$D/ref/scipy_b1_rtol1e-08.jsonl
$D/runrec.sh scipy_ref_b6_rtol1e-13_tc $PY -u taylor_polar.py --complex --scipy-ref-make=b6 --rtol=1e-13 --points=tc --out=$D/ref/scipy_b6_rtol1e-13.jsonl
$D/runrec.sh scipy_ref_b6_rtol1e-08_tc $PY -u taylor_polar.py --complex --scipy-ref-make=b6 --rtol=1e-8 --points=tc --out=$D/ref/scipy_b6_rtol1e-08.jsonl
