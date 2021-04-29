import hydra
from omegaconf import DictConfig, OmegaConf, open_dict
import os

@hydra.main(config_name="hydra_demo_config", config_path="config")
def my_app(cfg : DictConfig) -> None:

    # add new configs
    with open_dict(cfg):
        cfg['new'] = 'new'
    print(OmegaConf.to_yaml(cfg))
    print("Resolved out_dir: "+cfg.exp.out_dir)

    # save log in custom folder
    EXP_FILE = cfg.exp.out_dir+'/user.log'
    if not os.path.exists(cfg.exp.out_dir):
        os.mkdir(cfg.exp.out_dir)
    with open(EXP_FILE, 'w') as fp:
        fp.write("Dummy User log\n")

if __name__ == "__main__":
    my_app()
