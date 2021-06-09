"""
This is a job script for running policy gradient algorithms on gym tasks using hydra
Separate job scripts are provided to run few other algorithms
- For DAPG see here: https://github.com/aravindr93/hand_dapg/tree/master/dapg/examples
- For model-based NPG see here: https://github.com/aravindr93/mjrl/tree/master/mjrl/algos/model_accel
"""

import os
import json
import time as timer
import hydra
from omegaconf import DictConfig, OmegaConf
from hydra_mjrl_job import train_loop

# ===============================================================================
# Process Inputs and configure job
# ===============================================================================
@hydra.main(config_name="hydra_npg_config", config_path="config")
def configure_jobs(job_data):
    print("========================================")
    print("Job Configuration")
    print("========================================")

    if not os.path.exists(job_data.job_name):
        os.mkdir(job_data.job_name)
    assert 'algorithm' in job_data.keys()
    assert any([job_data.algorithm == a for a in ['NPG', 'NVPG', 'VPG', 'PPO']])
    assert 'sample_mode' in job_data.keys()
    job_data.alg_hyper_params = dict() if 'alg_hyper_params' not in job_data.keys() else job_data.alg_hyper_params

    EXP_FILE = job_data.job_name + '/job_config.json'
    with open(EXP_FILE, 'w') as fp:
        # json.dump(job_data, f, indent=4)
        OmegaConf.save(config=job_data, f=fp.name)

    if job_data.sample_mode == 'trajectories':
        assert 'rl_num_traj' in job_data.keys()
        job_data.rl_num_samples = 0 # will be ignored
    elif job_data.sample_mode == 'samples':
        assert 'rl_num_samples' in job_data.keys()
        job_data.rl_num_traj = 0    # will be ignored
    else:
        print("Unknown sampling mode. Choose either trajectories or samples")
        exit()

    print(OmegaConf.to_yaml(job_data))
    train_loop(job_data)

if __name__ == "__main__":
    configure_jobs()