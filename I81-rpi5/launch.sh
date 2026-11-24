#!/bin/bash
# usage: launch.sh <name> [args to sheared.py...]; detached unit nm-i81-<name>-<n>, logs <name>.run<n>.log/.err/.rc, never overwritten
NAME=$1; shift
RAW=/home/nathan/Source/negative-mass-raw/I81-rpi5
N=1; while [ -e "$RAW/$NAME.run$N.log" ]; do N=$((N+1)); done
LOG="$RAW/$NAME.run$N.log"; RC="$RAW/$NAME.run$N.rc"
systemd-run --user --unit="nm-i81-$NAME-$N" --nice=10 --collect /bin/bash "$RAW/step.sh" "$LOG" "$RC" "$@"
echo "log $LOG rc $RC"
