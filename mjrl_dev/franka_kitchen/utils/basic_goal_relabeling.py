"""
Extract goals from human play data for use with imitation learning
"""
import numpy as np
import pickle, os, click
import mj_envs
from mjrl.utils.gym_env import GymEnv

DESC = '''
Script to extract and relabel goals for trajectories in the Franka kitchen environment
This performs the basic relabeling with a fixed shift forward in time
    $ python basic_goal_relabeling.py --shift_window 30 --data <path/to/file.pkl> \n
'''

@click.command(help=DESC)
@click.option('--data', type=str, help='path to the Franka kitchen dataset', required=True)
@click.option('--shift_window_lower', type=int, help='lower range for forward time shift for goal extraction and relabeling', default=30)
@click.option('--shift_window_upper', type=int, help='upper range for relabeling', default=30)
@click.option('--granularity', type=int, help='how granular to relabel at', default=5)
def main(data, shift_window_lower, shift_window_upper, granularity):
    paths = pickle.load(open(data, 'rb'))

    while shift_window_lower <= shift_window_upper:
        paths = relabel_paths(paths, shift_window_lower)
        out_file = data[:-21] + str(shift_window_lower) + '_shift_window.pkl'
        pickle.dump(paths, open(out_file, 'wb'))
        print("The relabeled dataset was written to: " + out_file)
        shift_window_lower += granularity

def relabel_paths(paths, shift_window):
    e = GymEnv('kitchen-v3')
    for path in paths:
        obs = path['observations']      # (horizon, obs_dim)
        r_obs = obs.copy()              # placeholder for relabelled observations
        horizon = obs.shape[0]
        for t in range(horizon):
            shift_t = min(t + shift_window, horizon-1)
            r_obs[t, e.env.env.key_idx['goal']] = obs[shift_t, e.env.env.key_idx['objs_jnt']]
        path['observations'] = r_obs
    return paths

if __name__ == '__main__':
    main()