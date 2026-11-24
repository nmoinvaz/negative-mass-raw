#!/bin/bash
# usage: launch.sh <name> [args...]: starts run_step.sh as the systemd user unit nm-i148-<name> (nice 10)
name=$1
systemd-run --user --unit=nm-i148-$name --collect -p Nice=10 /bin/bash /home/nathan/Source/negative-mass-raw/I148-rpi5/run_step.sh "$@"
