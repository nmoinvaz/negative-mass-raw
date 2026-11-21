#!/bin/bash
# ./run_scan.sh L : column_scan_i123.py L into column_scan_l<L>.log, nice 10, one thread
HERE=$(cd "$(dirname "$0")" && pwd)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
nice -n 10 "$HOME/Source/negative-mass-venv314/bin/python" -u "$HERE/column_scan_i123.py" "$1" > "$HERE/column_scan_l$1.log" 2>&1
echo "exit $?" >> "$HERE/column_scan_l$1.log"
