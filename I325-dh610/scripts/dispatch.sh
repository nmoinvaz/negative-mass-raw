#!/bin/bash
# usage: dispatch.sh   issues the tickets of the pairs, in the order below, once $RAW/README_2B_DONE exists and fewer than 4 compute processes of mine run, and the pair's bisection is finished.
RAW=${RAW:-$HOME/Source/negative-mass-raw/I325-dh610}
I228=$HOME/Source/negative-mass-raw/I228-dh610/runs
mkdir -p "$RAW/tickets"
# name B HK DELTA (priority order: the long h = 0.00125 pairs first)
list=("0.01 2 1e-11" "0.014 2 1e-11" "0.03 2 1e-11" "0.04 2 1e-11" "0.02 2 1e-10" "0.02 2 1e-11")
while [ ! -e "$RAW/README_2B_DONE" ]; do sleep 20; done
left=${#list[@]}
declare -A done_
while [ "$left" -gt 0 ]; do
  n=$(pgrep -u "$USER" -fc '^/home/nathan/Source/negative-mass-venv314/bin/python (-u )?(g_d6.py drift|drift_b6.py)')
  if [ "$n" -lt 4 ]; then
    for e in "${list[@]}"; do
      set -- $e; B=$1; HK=$2; D=$3; key="$B-$HK-$D"
      [ -n "${done_[$key]}" ] && continue
      case $HK in 1) H=0.0025;; 2) H=0.00125;; esac
      if [ -e "$RAW/runs/bisect/D6_B${B}_h${H}/summary.json" ] || [ -e "$I228/bisect/D6_B${B}_h${H}/summary.json" ]; then
        touch "$RAW/tickets/pair_B${B}_d${D}_hk${HK}"; done_[$key]=1; left=$((left-1)); echo "$(date -Is) ticket $key (running $n)"; sleep 25; break
      fi
    done
  fi
  sleep 15
done
echo "all tickets issued"
