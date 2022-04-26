# Getting started with [Hydra](https://hydra.cc/)

## Installation
1. Install the dependnecies using `pip install -r requirements.txt`. We use Hydra as the config manager and the [submitit](https://github.com/facebookincubator/submitit) launcher plugin to launch jobs on cluster or locally.

NOTE: FAIR cluster users should follow [hydra's internal guide](https://www.internalfb.com/intern/staticdocs/hydra/docs/fb/intro/) for installation


## Configs Overview
1. Configurations are yaml files stored hierarchically in a folder. See `mjrl_dev/hydra/config` folder and it's subfolders.
2. Configuration files are composable. For example `hydra_demo_config.yaml` references other configs as defaults. Defaults can be overridden on command line while invoking. See `Examples` below
3. Some configurations like `launcher` / `output` have special meaning and one needs to be careful overloading these. For more on these refer to hydra documentation linked above.
4. A quick overview of demo configs. `hydra_demo_config.yaml` is a top level config. It refers to configs under `launcher` and `output` as defaults. `launcher` configs are about Hydra launchers. Hydra lets you save on boilerplate by providing launchers that can launch your job on a distributed cluster like FAIR Cluster (where it uses `submitit` library to do the actual launching) `output` configs are about specifyinh `hyrdra.run.dir` and `hydra.sweep.dir` These are the locations where your job output logs (stdout / stderr) go.

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
    - `python hydra_mjrl_launcher.py`
    - `python hydra_mjrl_launcher.py --multirun hydra/launcher=local hydra/output=local`
    - `python hydra_mjrl_launcher.py --multirun hydra/launcher=slurm hydra/output=slurm`
    - `python hydra_mjrl_launcher.py --multirun hydra/launcher=slurm hydra/output=slurm seed=10,12`

