#!/bin/bash

for d in $(ls ./kitchen_demos_multitask/); 
do
    echo $d
    python utils/parse_demos.py \
       --env kitchen-v3 \
       --demo_dir ./kitchen_demos_multitask/$d/ \
       --view playback \
       --skip 40 \
       --render None \
       --save_demos True \
       --kettle_joint 6dof
done

echo "Combining all the parsed demonstrations into a single file"
python utils/combine_demos.py --demo_dir ./kitchen_demos_multitask
