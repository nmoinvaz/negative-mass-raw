#!/bin/bash
# Starts a second worker of launch_I126.sh on LISTFILE once the 15-minute load average is below 4 (checked once a minute).
# Usage: [LIMIT=SECONDS] ./start_second.sh LISTFILE
HERE=$(cd "$(dirname "$0")" && pwd)
while true; do
  l15=$(cut -d' ' -f3 /proc/loadavg)
  if awk -v l="$l15" 'BEGIN{exit !(l < 4)}'; then
    echo "$(date -Is) 15-min load $l15 < 4: starting a second worker on $1" >> "$HERE/queue.log"
    setsid nohup "$HERE/launch_I126.sh" "$1" > "$HERE/launcher2.out" 2>&1 < /dev/null &
    exit 0
  fi
  sleep 60
done
