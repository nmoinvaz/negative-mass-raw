#!/bin/bash
# usage: waitrun.sh PATH CMD...   waits until PATH exists, then runs CMD (a dependency inside one run, so that no other lane can take the run before it)
p=$1; shift
while [ ! -e "$p" ]; do sleep 30; done
exec "$@"
