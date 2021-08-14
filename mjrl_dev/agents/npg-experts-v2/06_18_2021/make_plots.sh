#!/bin/bash

function plot-logs() {
  python /Users/aravraj/work/Projects/gcdt/mjrl/mjrl/utils/plot_from_logs.py --data "$1" --output "${2:-.}" --xkey "${3:-None}" --xscale "${4:-1}"
}

for d in $(ls -d */);
do
    echo $d
    plot-logs $d/logs/log.pickle $d/
done
