#!/bin/bash
while [ ! -f /home/nathan/Source/negative-mass-raw/I96-dh610/sectors-s16-p340.log.exit ]; do
  echo "$(date -Is) rss_kib $(ps -eo rss,args | grep 'tanh_spectrum.py' | grep -v grep | awk '{s+=$1} END {print s+0}') $(grep MemAvailable /proc/meminfo | tr -s ' ')" >> /home/nathan/Source/negative-mass-raw/I96-dh610/memwatch.log
  sleep 60
done
