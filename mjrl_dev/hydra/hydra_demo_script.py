import logging
import hydra
from omegaconf import DictConfig, OmegaConf, open_dict
import os

# A logger for this file
log = logging.getLogger(__name__)

@hydra.main(config_name="hydra_demo_config", config_path="config")
def my_app(cfg : DictConfig) -> None:

    # add new configs
    with open_dict(cfg):
        cfg['new'] = 'new'

    print("Passed configs ========")
    print(OmegaConf.to_yaml(cfg, resolve=False))
    print("Resolved configs ========")
    print(OmegaConf.to_yaml(cfg, resolve=True))
    log.info(OmegaConf.to_yaml(cfg, resolve=True))

    # save log in custom folder
    EXP_FILE = cfg.exp.out_dir+'/user.log'
    if not os.path.exists(cfg.exp.out_dir):
        os.mkdir(cfg.exp.out_dir)
    with open(EXP_FILE, 'w') as fp:
        fp.write("Dummy User log\n")

if __name__ == "__main__":
    my_app()
