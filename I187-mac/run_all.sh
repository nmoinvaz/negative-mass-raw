#!/bin/zsh
# the runs of record of #187, one process at a time (launched detached)
cd /Users/nathan/Source/negative-mass-i187/phase2/nonradial
J=/Users/nathan/Source/negative-mass-raw/I187-mac/jsonl
{ echo "# code: $(git rev-parse HEAD) branch $(git rev-parse --abbrev-ref HEAD)"; echo "# rustc: $(rustc --version); cargo: $(cargo --version)"; echo "# python: $(/Users/nathan/Source/negative-mass/.venv/bin/python --version)"; echo "# crate: taylor_polar 0.1.0, multishoot =4.2.0, multidouble main ba0ad101ce76 (Cargo.lock)"; echo "# machine: $(sysctl -n machdep.cpu.brand_string), $(sysctl -n hw.ncpu) cores, load $(uptime | sed 's/.*load averages*: //')"; } > /Users/nathan/Source/negative-mass-raw/I187-mac/run_00_env.log
/Users/nathan/Source/negative-mass-raw/I187-mac/runrec.sh planted_rm /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --rows --only=QP,RP,RM
/Users/nathan/Source/negative-mass-raw/I187-mac/runrec.sh rows_l2 /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --rows --only=RA2,RX --jsonl-dir=$J
/Users/nathan/Source/negative-mass-raw/I187-mac/runrec.sh rows_l3 /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --rows --only= --print-rows=3 --jsonl-dir=$J
/Users/nathan/Source/negative-mass-raw/I187-mac/runrec.sh rows_l4 /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --rows --only=RA4 --jsonl-dir=$J
/Users/nathan/Source/negative-mass-raw/I187-mac/runrec.sh rows_l5_cap5 /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --rows --only=RA5,CAP5,CAP5s --jsonl-dir=$J
/Users/nathan/Source/negative-mass-raw/I187-mac/runrec.sh rows_l6_cap6 /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --rows --only=RA6,CAP6 --jsonl-dir=$J
/Users/nathan/Source/negative-mass-raw/I187-mac/runrec.sh default_mode /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py
for c in qint_cofsign qint_f rm_off1 rm_cut r0_grid qstart moncrief tol_loose jsign; do
  /Users/nathan/Source/negative-mass-raw/I187-mac/runrec.sh ctl_$c /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --rows --mutate=$c
done
/Users/nathan/Source/negative-mass-raw/I187-mac/runrec.sh ctl_tol_loose_CAP5s /Users/nathan/Source/negative-mass/.venv/bin/python taylor_polar.py --rows --mutate=tol_loose --only=CAP5s
