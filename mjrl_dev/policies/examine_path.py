DESC = '''
Helper script to examine(openloop playback) paths. \n
USAGE:\n
	$ python examine_paths.py --env "swimmer-v0" --path path_to_file.pickle --repeat 10\n
'''
import pickle
import click
import numpy as np
from mjrl.utils.gym_env import GymEnv
from mjrl.utils import tensor_utils

@click.command(help=DESC)
@click.option('-i', '--include', type=str, help='task suite to import', default="")
@click.option('-e', '--env_name', type=str, help='Env name', required=True)
@click.option('-p', '--path_file', type=str, help='pickle file with paths', required=True)
@click.option('-l', '--loop', type=int, help='number of times to loop paths', default=10)
@click.option('-r', '--render', type=bool, help='rendering', default=True)
@click.option('-s', '--save', type=bool, help='save resulting playback paths', default=False)
def main(include, env_name, path_file, loop, render, save):
    # get env
    if include is not "":
        exec("import "+include)
    env = GymEnv(env_name)

    # load paths
    paths = pickle.load(open(path_file, 'rb'))

    # playback paths
    pbk_paths = []
    for i_loop in range(loop):
        for path in paths:
            obs = []
            act = []
            rewards = []
            env_infos = []
            states = []

            # initialize paths
            if "state" in path.keys():
                env.reset(init_state=path["state"][0])
            else:
                env.reset()

            # playback input path
            if render:
                env.env.env.mujoco_render_frames = True
            o = env.get_obs()
            for i_step in range(path['actions'].shape[0]):
                a = path['actions'][i_step]
                s = env.get_env_state()
                onext, r, d, info = env.step(a) # t = t+1
                if render:
                    env.render()
                obs.append(o); o = onext
                act.append(a)
                rewards.append(r)
                env_infos.append(info)
                states.append(env.get_env_state())
            if render:
                env.env.env.mujoco_render_frames = True

            # create output paths
            pbk_path = dict(observations=np.array(obs),
                actions=np.array(act),
                rewards=np.array(rewards),
                env_infos=tensor_utils.stack_tensor_dict_list(env_infos),
                states=states)
            pbk_paths.append(pbk_path)
        print("Finished playback loop:{}".format(i_loop))

    # save output paths
    if save:
        pbk_file_name = path_file[:path_file.rfind('.')]+"_playback.pickle"
        pickle.dump(pbk_paths, open(pbk_file_name, 'wb'))
        print("Saved: "+pbk_file_name)

    return pbk_paths


if __name__ == '__main__':
    main()
