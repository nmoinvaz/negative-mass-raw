#!/bin/sh
# usage: runmuts.sh TAGPREFIX NAME...  -> for each mutation NAME: derive and check, logs TAGPREFIX_NAME_{derive,check}_run<N>.log
cd "$(dirname "$0")" || exit 1
pre=$1; shift
for m in "$@"; do
  ./runx.sh "${pre}_${m}_derive" derive --mutate=$m
  ./runx.sh "${pre}_${m}_check" check --mutate=$m
done
