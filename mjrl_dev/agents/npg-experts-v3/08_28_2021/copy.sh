#!/bin/bash

SUB="franka_comp_expert"

for d in $(ls /checkpoint/giriman/outputs/coss/mjrl_master_plus_mp_fix_mj_envs_dfdd9d7807d2e00838932f6fb23bd9ff56e3e9f5);
do
    if [[ "$d" == "$SUB"* ]]; then
        echo $d
        mkdir $d
        rsync -avz /checkpoint/giriman/outputs/coss/mjrl_master_plus_mp_fix_mj_envs_dfdd9d7807d2e00838932f6fb23bd9ff56e3e9f5/$d/*/*/job/* $d/ --exclude *policy_* --exclude *baseline_* 
    fi
done
