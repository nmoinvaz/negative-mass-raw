#!/bin/bash
# usage: run01_mutants.sh NAME...   one run of record of checks.py --mutate=NAME each
D=/home/nathan/Source/negative-mass-raw/I39-dh610/runs
for mu in "$@"; do $D/run01_run.sh run01_mut_$mu --mutate=$mu; done
