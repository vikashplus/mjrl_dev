"""
This is a launcher script for launching mjrl training using hydra
"""

from omegaconf import OmegaConf

import hydra
from mjrl_job_script import train_loop


# ===============================================================================
# Process Inputs and configure job
# ===============================================================================
@hydra.main(config_name="hydra_npg_config", config_path="config")
def configure_jobs(job_data):
    print("========================================")
    print("Job Configuration")
    print("========================================")

    assert "algorithm" in job_data
    assert job_data.algorithm in ["NPG", "NVPG", "VPG", "PPO"]
    assert "sample_mode" in job_data
    assert job_data.sample_mode in ["samples", "trajectories"]
    job_data.alg_hyper_params = (
        dict() if "alg_hyper_params" not in job_data else job_data.alg_hyper_params
    )

    with open("job_config.yaml", "w") as fp:
        OmegaConf.save(config=job_data, f=fp.name)

    if job_data.sample_mode == "trajectories":
        assert "rl_num_traj" in job_data
        job_data.rl_num_samples = 0  # will be ignored
    elif job_data.sample_mode == "samples":
        assert "rl_num_samples" in job_data
        job_data.rl_num_traj = 0  # will be ignored
    else:
        print("Unknown sampling mode. Choose either trajectories or samples")
        exit()

    print(OmegaConf.to_yaml(job_data, resolve=True))
    train_loop(job_data)


if __name__ == "__main__":
    configure_jobs()
