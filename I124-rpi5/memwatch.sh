#!/bin/bash
# Reports only: once a minute, the load, free memory and the cpu and rss of this task's zerilli_zeros.py processes.
# It stops nothing. Usage: memwatch.sh >> memwatch.log
while true; do
  echo "$(date -Is) load $(cut -d' ' -f1-3 /proc/loadavg) mem_avail_MB $(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)"
  ps -eo pid,ni,pcpu,rss,etime,args | grep -E 'negative-mass-venv314.*zerilli_zeros' | grep -v grep \
    | awk '{printf "   pid %s ni %s cpu %s%% rss_MB %d etime %s %s %s %s %s %s %s\n",$1,$2,$3,$4/1024,$5,$8,$9,$10,$11,$12,$13}'
  sleep 60
done
