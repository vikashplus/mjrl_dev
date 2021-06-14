# mjrl_dev
some development and utility scripts for mjrl

## Hydra

* Hydra is a configuration management framework. For details see hydra [documentation](https://www.internalfb.com/intern/staticdocs/hydra/docs/fb/fair-cluster)

* Configurations are yaml files stored hierarchically in a folder. 
    * See `mjrl_dev/hydra/config` folder and it's subfolders

* Configuration files are composable. 
    * For example `hydra_demo_config.yaml` references other configs as defaults.
    * Defaults can be overridden on command line while invoking. 
    * For example: 
```
# defaults to local run
python hydra_demo_script.py --multirun 

#overrides to slurm run
python hydra_demo_script.py --multirun hydra/launcher=slurm hydra/output=slurm
```
* Some configurations like `launcher` / `output` have special meaning and one needs to be careful overloading these. For more on these refer to hydra documentation linked above.

* Quick overview of our config demo:
    * `hydra_demo_config.yaml` is a top level config.
    * It refers to configs under `launcher` and `output` as defaults.
    * `launcher` configs are about Hydra launchers. Hydra lets you save on boilerplate by providing launchers that can launch your job on a distributed cluster like FAIR Cluster (where it uses `submitit` library to do the actual launching)
    * `output` configs are about specifyinh `hyrdra.run.dir` and `hydra.sweep.dir` These are the locations where your job output logs (stdout / stderr) go.





