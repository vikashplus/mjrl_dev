import mj_envs
import click
import os
import h5py
import gym
import numpy as np
import pickle

DESC = '''
Helper script to visualize demonstrations.\n
USAGE:\n
    Visualizes demonstrations on the env\n
    $ python parse_demos.py --env_name relocate-v0 --data_path relocate-v0_demos.pickle\n
'''

# MAIN =========================================================
@click.command(help=DESC)
@click.option('-e', '--env_name', type=str, help='environment to load', required= True)
@click.option('-d', '--data_path', type=str, help='dataset path', required= True)
@click.option('-r', '--render', type=bool, help='Onscreen Visualization', default=True)
def main(env_name, data_path, render):
    if env_name is "":
        print("Unknown env.")
        return
    data_name, data_type = os.path.splitext(data_path)
    if data_type == ".pickle":
        demos = pickle.load(open(data_path, 'rb'))
    elif data_type == ".h5":
        demos = h5py.File(data_path, 'r')
        print(f"Number of demos loaded: {len(demos)}")
        raise NotImplementedError("Playback using .h5 format isn't supported yet")
    else:
        raise TypeError("unknown file format")


    demo_playback(env_name, demos, render)

def demo_playback(env_name, demo_paths, render):
    e = gym.make(env_name)
    e.reset()

    for i_path, path in enumerate(demo_paths):
        # initialize
        e.reset()
        e.set_env_state(path['init_state_dict'])

        # Playback
        actions = path['actions']
        rewards = 0
        for t in range(actions.shape[0]):
            obs, rwd, done, info = e.step(actions[t])
            rewards+=rwd
            # render demonstrations
            if render:
                e.env.mj_render()
        print(f"Trajectory{i_path}: Total rewards = {rewards}")
        print(f"Env dt: {e.env.sim.model.opt.timestep}, Final Env.time {e.env.sim.data.time}")
    e.close()

if __name__ == '__main__':
    main()
