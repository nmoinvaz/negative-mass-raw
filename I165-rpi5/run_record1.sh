#!/bin/bash
RAW=/home/nathan/Source/negative-mass-raw/I165-rpi5
PY=/home/nathan/Source/negative-mass-venv314/bin/python
$RAW/run_step.sh compute_dims_1 $PY notes/warp/one_sign_static.py --compute=dims --s0=2,3,5,7,11 --primes=2147483629
$RAW/run_step.sh compute_fullring_1 $PY notes/warp/one_sign_static.py --compute=fullring --primes=2147483629 --minutes=60
echo done > $RAW/logs/record1.done
