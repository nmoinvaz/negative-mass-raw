#!/bin/bash
# three workers, serial per worker; each control is one process at nice 10
cd "$(dirname "$0")" || exit 2
xargs -P 3 -L 1 ./ctl_one.sh < ctl_jobs.txt
