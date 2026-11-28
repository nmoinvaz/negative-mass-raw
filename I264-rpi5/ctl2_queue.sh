#!/bin/bash
# three workers, serial per worker; each control is one process at nice 10
cd "$(dirname "$0")" || exit 2
xargs -P 3 -L 1 ./ctl2_one.sh < ctl2_jobs.txt
