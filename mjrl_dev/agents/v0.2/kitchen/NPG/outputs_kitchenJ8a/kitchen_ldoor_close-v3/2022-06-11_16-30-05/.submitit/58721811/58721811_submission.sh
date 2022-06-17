#!/bin/bash

# Parameters
#SBATCH --array=0-6%7
#SBATCH --cpus-per-task=24
#SBATCH --error=/checkpoint/vikashplus/outputs_kitchenJ8b/kitchen_ldoor_close-v3/2022-06-11_16-30-05/.submitit/%A_%a/%A_%a_0_log.err
#SBATCH --job-name=kitchen_ldoor_close_v3
#SBATCH --mem=64GB
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --open-mode=append
#SBATCH --output=/checkpoint/vikashplus/outputs_kitchenJ8b/kitchen_ldoor_close-v3/2022-06-11_16-30-05/.submitit/%A_%a/%A_%a_0_log.out
#SBATCH --signal=USR1@90
#SBATCH --time=4320
#SBATCH --wckey=submitit

# command
export SUBMITIT_EXECUTOR=slurm
srun --output /checkpoint/vikashplus/outputs_kitchenJ8b/kitchen_ldoor_close-v3/2022-06-11_16-30-05/.submitit/%A_%a/%A_%a_%t_log.out --error /checkpoint/vikashplus/outputs_kitchenJ8b/kitchen_ldoor_close-v3/2022-06-11_16-30-05/.submitit/%A_%a/%A_%a_%t_log.err --unbuffered /private/home/vikashplus/.conda/envs/mjrl-gpu-env/bin/python -u -m submitit.core._submit /checkpoint/vikashplus/outputs_kitchenJ8b/kitchen_ldoor_close-v3/2022-06-11_16-30-05/.submitit/%j
