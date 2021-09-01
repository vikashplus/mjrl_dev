import mj_envs
import click 
import os
import gym
import numpy as np
import pickle
from mjrl.utils.gym_env import GymEnv

DESC = '''
Helper script to visualize demonstrations.\n
USAGE:\n
    Visualizes demonstrations on the env\n
    $ python visualize_demos --env kitchen-v3 --data <path/to/file.pkl>  --horizon 75 --demo 100 \n
'''

# MAIN =========================================================
@click.command(help=DESC)
@click.option('--env', type=str, help='name of environment to load', default='kitchen-v3')
@click.option('--data', type=str, help='path to parsed demo file', required=True)
@click.option('--max_horizon', type=int, help='number of timesteps to visualize', default=None)
@click.option('--demo', type=int, help='demo to begin visualizing from', default=0)
@click.option('--ntraj', type=int, help='number of trajectories to visualize', default=1e6)
def main(env, data, max_horizon, demo, ntraj):
    demos = pickle.load(open(data, 'rb'))
    max_horizon = np.inf if max_horizon is None else max_horizon
    # render demonstrations
    demo_playback(env, demos[demo:], max_horizon, ntraj)

def demo_playback(env, demos, max_horizon, ntraj):
    e = GymEnv(env)
    e.reset()
    for idx, demo in enumerate(demos):
        e.env.env.set_state(demo['init_qpos'], demo['init_qvel'])
        actions = demo['actions']
        horizon = min(actions.shape[0], max_horizon)
        print("\n \n Trajectory : %i | Horizon : %i" % (idx, actions.shape[0]))
        for t in range(horizon):
            e.step(actions[t])
            e.env.unwrapped.mj_render()
            print(t, end=', ', flush=True)
        print("\n ===========================================")
        if idx >= ntraj:
            break

if __name__ == '__main__':
    main()
