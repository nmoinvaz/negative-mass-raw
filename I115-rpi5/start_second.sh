#!/bin/bash
# Starts the second worker of launch_I115.sh once the 15-minute load average is below 4 (checked once a minute).
HERE=$(cd "$(dirname "$0")" && pwd)
while true; do
  l15=$(cut -d' ' -f3 /proc/loadavg)
  if awk -v l="$l15" 'BEGIN{exit !(l < 4)}'; then
    echo "$(date -Is) 15-min load $l15 < 4: starting the second worker" >> "$HERE/queue.log"
    setsid nohup "$HERE/launch_I115.sh" > "$HERE/launcher2.out" 2>&1 < /dev/null &
    exit 0
  fi
  sleep 60
done
