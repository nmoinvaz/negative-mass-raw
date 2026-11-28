#!/bin/bash
# runs the command quoted in identity_review.md, as written, from notes/wormhole_largeD (the worktree)
RAW="$(cd "$(dirname "$0")" && pwd)"
N=$1
for e in log err rc; do [ -e "$RAW/$N.$e" ] && { echo "$N.$e exists" >&2; exit 3; }; done
cd /home/nathan/Source/negative-mass-i264/notes/wormhole_largeD || exit 2
/home/nathan/Source/negative-mass-venv314/bin/python identity_review.py sym exch shifts bnd masters masters2 fp ctlsum --ctldir=../../../negative-mass-raw/I264-rpi5 --ctlprefix=ctl2 > "$RAW/$N.log" 2> "$RAW/$N.err"
echo $? > "$RAW/$N.rc"
