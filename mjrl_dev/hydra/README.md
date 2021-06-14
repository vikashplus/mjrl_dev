# Getting started with [Hydra](https://hydra.cc/)

## Installation
1. install hydra `pip install hydra-core --upgrade`
2. install [submitit](https://github.com/facebookincubator/submitit) launcher hydra plugin to launch jobs on cluster/ local `pip install hydra-submitit-launcher --upgrade`

NOTE: FAIR cluster users should follow [hydra's internal guide](https://www.internalfb.com/intern/staticdocs/hydra/docs/fb/intro/) for installation

## Launch jobs
1. Default to local run `python hydra_demo_script.py --multirun `
2. To launch job using submitit launcher locally try `python hydra_demo_script.py --multirun hydra/launcher=local hydra/output=local`
3. To launch job using submitit launcher on the slurm cluster `python hydra_demo_script.py --multirun hydra/launcher=slurm hydra/output=slurm`

## Hyperparameter sweeps
1. To sweep over any (e.g-exp.seed) parameter `python hydra_demo_script.py --multirun hydra/launcher=slurm hydra/output=slurm exp.seed=10,20`

## Examples
1. Over ride a parameter `python hydra_demo_script.py exp.seed=1`
2. Add a new group to your configs `python hydra_demo_script.py +group=group1`
3. To sweep over parameters `python hydra_demo_script.py -m exp.seed=1,2`
4. Train using [mjrl](https://github.com/aravindr93/mjrl) agents
    - `python hydra_policy_opt_job_script.py`
    - `python hydra_policy_opt_job_script.py --multirun hydra/launcher=local hydra/output=local`
    - `python hydra_policy_opt_job_script.py --multirun hydra/launcher=slurm hydra/output=slurm`
    - `python hydra_policy_opt_job_script.py --multirun hydra/launcher=slurm hydra/output=slurm seed=10,12`

