#!/bin/bash

SUB="franka_comp_expert"

for d in $(ls /checkpoint/aravraj/outputs/);
do
    if [[ "$d" == "$SUB"* ]]; then
        echo $d
        mkdir $d
        rsync -avz /checkpoint/aravraj/outputs/$d/*/*/job/* $d/ --exclude *policy_* --exclude *baseline_* 
    fi
done
