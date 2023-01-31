"""
Take first x timesteps of each trajectory from a demos dataset
"""
import click
import pickle
import numpy as np

@click.command()
@click.option('--data', type=str, help='path to the dataset', required=True)
@click.option('--timesteps', type=int, help='number of first timesteps to take from each trajectory', default=75)

def main(data, timesteps):
    demos = pickle.load(open(data, 'rb'))

    new_demos = []
    for demo in demos:
        path = {
                'observations': demo['observations'][0:timesteps],
                'actions': demo['actions'][0:timesteps],
                'rewards': demo['rewards'][0:timesteps],
                'goals': demo['goals'][0:timesteps],
                'obs_dicts': demo['obs_dicts'][0:timesteps],
                'init_qpos': demo['init_qpos'][0:timesteps],
                'init_qvel': demo['init_qvel'][0:timesteps],
                'env_infos': demo['env_infos'][0:timesteps]
                }
        new_demos.append(path)
    pickle.dump(new_demos, open(data[:-4]+str(timesteps)+'_timesteps'+'.pkl', 'wb'))

if __name__ == '__main__':
    main()