#!/bin/sh

for f in *.prof
do
    echo "$f"
    for e in ,bootstrap_0_ok,    \
             ,bootstrap_0_start, \
             ,bootstrap_0_stop,  \
             ,cancel_pilot,      \
             ,cmd,               \
             ,cu_exec_start,     \
             ,exec_start,        \
             ,req_start,         \
             ,req_stop,          \
             ,schedule_ok,       \
             ,advance,           \
             ,sub_agent_start,   \
             ,sub_agent_stop,    \
             ,unschedule_stop,
    do
      echo "\t $e"
      grep "$e" $f >> /tmp/filtered.prof
    done
done

