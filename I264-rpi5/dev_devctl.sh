#!/bin/bash
# usage: devctl.sh NAME PARTS  -> runs one mutation in dev mode
SC=/tmp/claude-1000/-home-nathan-Source-negative-mass-i264/68a7bf57-1915-46d5-843f-9e1cd30b9313/scratchpad
NAME=$1; shift
cd /tmp
nice -n 10 ~/Source/negative-mass-venv314/bin/python /home/nathan/Source/negative-mass-i264/notes/wormhole_largeD/identity_review.py "$@" --mutate=$NAME --cache=$SC/cache > $SC/dev/dev_ctl_$NAME.log 2>&1
echo "exit $?" >> $SC/dev/dev_ctl_$NAME.log
