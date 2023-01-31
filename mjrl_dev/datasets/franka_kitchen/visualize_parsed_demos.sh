#!/bin/bash

#for d in $(ls ./kitchen_demos_multitask/); 
#do
#    echo $d
#    python utils/visualize_demos.py --env kitchen-v3 \
#    --data kitchen_demos_multitask/$d/kitchen-v3_full_demos.pkl \
#    --ntraj 2
#done

python utils/visualize_demos.py --env kitchen-v3 --data kitchen_demos_multitask/kitchen-v3_all_parsed_paths.pkl
