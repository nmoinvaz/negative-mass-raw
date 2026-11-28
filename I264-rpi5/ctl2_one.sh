#!/bin/bash
# usage: ctl2_one.sh NAME PARTS...  -> ctl_NAME.{log,err,rc}
cd "$(dirname "$0")" || exit 2
N=$1; shift
PY=/home/nathan/Source/negative-mass-venv314/bin/python
SCRIPT=/home/nathan/Source/negative-mass-i264/notes/wormhole_largeD/identity_review.py
CACHE=/tmp/claude-1000/-home-nathan-Source-negative-mass-i264/68a7bf57-1915-46d5-843f-9e1cd30b9313/scratchpad/cache_rec
[ -e ctl2_$N.log ] && { echo "ctl2_$N.log exists" >&2; exit 3; }
nice -n 10 $PY $SCRIPT "$@" --mutate=$N --cache=$CACHE > ctl2_$N.log 2> ctl2_$N.err
echo $? > ctl2_$N.rc
