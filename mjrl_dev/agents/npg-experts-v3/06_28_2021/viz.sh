#!/bin/bash

function viz-pol() {
  python /Users/aravraj/work/Projects/gcdt/mjrl/mjrl/utils/visualize_policy.py --env_name "$1" --policy "${2:-None}" --mode "${3:-evaluation}"
}

for e in kitchen_micro_open-v3 kitchen_rdoor_open-v3 kitchen_ldoor_open-v3 kitchen_sdoor_open-v3 kitchen_light_on-v3 kitchen_knob1_on-v3 kitchen_knob2_on-v3 kitchen_knob3_on-v3 kitchen_knob4_on-v3;
do
    echo $e
    viz-pol $e franka_comp_expert_$e/iterations/best_policy.pickle evaluation
done
