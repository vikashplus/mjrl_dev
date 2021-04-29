# Getting started with [Hydra](https://hydra.cc/)

## Installation
1. install hydra `pip install hydra-core --upgrade`
2. install [submitit](https://github.com/facebookincubator/submitit) launcher hydra plugin to launch jobs on cluster/ local `pip install hydra-submitit-launcher --upgrade`

## Launch jobs
1. Try demos script using `python hydra_demo_script.py`
2. To launch job using submitit launcher locally try `python hydra_demo_script.py --multirun hydra/launcher=submitit_local`
3. To launch job using submitit launcher on the slurm cluster `python hydra_demo_script.py --multirun hydra/launcher=submitit_slurm`

## Hyperparameter sweeps
1. To sweep over any (e.g-exp.seed) parameter `python hydra_demo_script.py --multirun hydra/launcher=submitit_local exp.seed=10,20`

## Examples
1. Train using [mjrl](https://github.com/aravindr93/mjrl) agents
    - `python hydra_policy_opt_job_script.py`
    - `python hydra_policy_opt_job_script.py --multirun hydra/launcher=submitit_local`
    - `python hydra_policy_opt_job_script.py --multirun hydra/launcher=submitit_slurm`
    - `python hydra_policy_opt_job_script.py --multirun hydra/launcher=submitit_local seed=10,12`

