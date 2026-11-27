#!/bin/bash
# usage: dev_s2_run_mutants.sh TAG NAME...   (development runs of checks.py --mutate=NAME, one thread each, nice 10)
cd /home/nathan/Source/negative-mass-i39/notes/wormhole_evolution
TAG=$1; shift
for mu in "$@"; do
  /usr/bin/time -v nice -n 10 /home/nathan/Source/negative-mass-venv314/bin/python checks.py --mutate=$mu > /home/nathan/Source/negative-mass-raw/I39-dh610/dev/${TAG}_mut_$mu.log 2> /home/nathan/Source/negative-mass-raw/I39-dh610/dev/${TAG}_mut_$mu.time
  echo "rc=$?" > /home/nathan/Source/negative-mass-raw/I39-dh610/dev/${TAG}_mut_$mu.rc
done
