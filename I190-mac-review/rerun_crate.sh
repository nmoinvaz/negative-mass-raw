#!/bin/bash
# rerun_crate.sh: the crate at 550800c with implicit_lib on this Mac; offgrid ctl and loglog, as the Pi's run_42, run_30
here=$(cd "$(dirname "$0")" && pwd)
py=/Users/nathan/Source/negative-mass/.venv/bin/python
wt=/Users/nathan/Source/negative-mass-r190/nm
export RAYON_NUM_THREADS=2
for n in rerun_build_on rerun_on_offgrid_ctl rerun_on_loglog; do [ -e "$here/$n.log" ] && { echo "refusing to overwrite $n.log" >&2; exit 2; }; done
{ echo "# $(date -u +%FT%TZ) $(uptime)"; cd $wt/notes/warp/conical_global && nice -n 10 cargo build --release -j 2 --features implicit_lib 2>&1; echo "exit $?"; } > "$here/rerun_build_on.log" 2>&1
cd $wt || exit 2
mkdir -p "$here/dump_on_ctl_mac" "$here/ctl_on_loglog_mac"
{ echo "# $(date -u +%FT%TZ) $(uptime)"; /usr/bin/time -l nice -n 10 $py notes/warp/conical_offgrid.py --grid=ctl --no-controls --nobuild --dump="$here/dump_on_ctl_mac" 2>&1; echo "exit $?"; } > "$here/rerun_on_offgrid_ctl.log" 2>&1
{ echo "# $(date -u +%FT%TZ) $(uptime)"; /usr/bin/time -l nice -n 10 $py notes/warp/conical_loglog.py --nobuild --logdir="$here/ctl_on_loglog_mac" 2>&1; echo "exit $?"; } > "$here/rerun_on_loglog.log" 2>&1
