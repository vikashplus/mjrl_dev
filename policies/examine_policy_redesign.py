from os import environ
environ["MKL_THREADING_LAYER"] = "GNU"

# Utilities
import evaluate_args
from mjrl.utils.gym_env import GymEnv
# Policies
from mjrl.policies.gaussian_mlp import MLP
# Samplers
# import mjrl.samplers.trajectory_sampler as trajectory_sampler
# import mjrl.samplers.base_sampler as base_sampler
from mjrl.samplers.core import do_rollout


# envs
import deepmimic
import robel
import aparo
import MPL

import pickle
import os
import numpy as np
from sys import platform as _platform


# Useful to check the horizon for teleOp / Hardware experiments
# TODO-Vik: Move to utils
def plot_horizon_distribution(paths, e):
    import matplotlib as mpl
    mpl.use('TkAgg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 5})

    if "time" in paths[0]['env_infos']:
        horizon = np.zeros(len(paths))

        # plot timesteps
        plt.clf()
        rl_dt_ideal = e.env.env.skip * e.env.env.model.opt.timestep
        for i, path in enumerate(paths):
            dt = path['env_infos']['time'][1:] - path['env_infos']['time'][:-1]
            horizon[i] = path['env_infos']['time'][-1] - path['env_infos'][
                'time'][0]
            h1 = plt.plot(
                path['env_infos']['time'][1:],
                dt,
                '-',
                label=('time=%1.2f' % horizon[i]))
        h1 = plt.plot(
            np.array([0, horizon[0]]),
            rl_dt_ideal * np.ones(2),
            'g',
            linewidth=5.0)

        plt.legend([h1[0]], ['ideal'], loc='upper right')
        plt.ylabel('time step (sec)')
        plt.xlabel('time (sec)')
        plt.ylim(rl_dt_ideal - 0.005, rl_dt_ideal + .045)
        plt.suptitle('Timestep profile for %d rollouts' % len(paths))

        file_name = e.env_id + '_timesteps.pdf'
        plt.savefig(file_name)
        print("Saved:", file_name)

        # plot horizon
        plt.clf()
        rl_steps = len(paths[0]['env_infos']['time'])
        h1 = plt.plot(
            np.array([0, len(paths)]),
            rl_steps * e.env.env.skip * e.env.env.model.opt.timestep *
            np.ones(2),
            'g',
            linewidth=5.0,
            label='ideal')
        plt.bar(np.arange(0, len(paths)), horizon, label='observed')
        plt.ylabel('rollout duration (sec)')
        plt.xlabel('rollout id')
        plt.legend()
        plt.suptitle('Horizon distribution for %d rollouts' % len(paths))

        file_name = e.env_id + '_horizon.pdf'
        plt.savefig(file_name)
        print("Saved:", file_name)


def plot_paths(paths, e, fileName_prefix=''):
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 5})

    for i, path in enumerate(paths):
        plt.clf()

        # observations
        nplt1 = len(path['env_infos']['obs_dict'])
        for iplt1, key in enumerate(
                sorted(path['env_infos']['obs_dict'].keys())):
            ax = plt.subplot(nplt1, 2, iplt1 * 2 + 1)
            if iplt1 != (nplt1 - 1):
                ax.axes.xaxis.set_ticklabels([])
            if iplt1 == 0:
                plt.title('Observations')
            ax.yaxis.tick_right()
            plt.plot(
                path['env_infos']['time'],
                path['env_infos']['obs_dict'][key],
                label=key)
            plt.ylabel(key)
        plt.xlabel('time (sec)')

        # actions
        nplt2 = 3
        ax = plt.subplot(nplt2, 2, 2)
        ax.set_prop_cycle(None)
        # h4 = plt.plot(path['env_infos']['time'], e.env.env.act_mid + path['actions']*e.env.env.act_rng, '-', label='act') # plot scaled actions
        h4 = plt.plot(
            path['env_infos']['time'], path['actions'], '-',
            label='act')  # plot normalized actions
        plt.ylabel('actions')
        ax.axes.xaxis.set_ticklabels([])
        ax.yaxis.tick_right()

        # rewards/ scores
        if "score" in path['env_infos']:
            ax = plt.subplot(nplt2, 2, 6)
            plt.plot(
                path['env_infos']['time'],
                path['env_infos']['score'],
                label='score')
            plt.xlabel('time')
            plt.ylabel('score')
            ax.yaxis.tick_right()

        if "rewards" in path['env_infos']:
            ax = plt.subplot(nplt2, 2, 4)
            ax.set_prop_cycle(None)
            for key in sorted(path['env_infos']['rewards'].keys()):
                plt.plot(
                    path['env_infos']['time'],
                    path['env_infos']['rewards'][key],
                    label=key)
            plt.legend(
                loc='upper left',
                fontsize='x-small',
                bbox_to_anchor=(.75, 0.25),
                borderaxespad=0.)
            ax.axes.xaxis.set_ticklabels([])
            plt.ylabel('rewards')
            ax.yaxis.tick_right()

        file_name = fileName_prefix + '_sample' + str(i) + '.pdf'
        plt.savefig(file_name)
        print("saved ", file_name)


# MAIN =========================================================
def main():
    # See evaluate_args.py for the list of args.
    args = evaluate_args.get_args()

    if args.env_name is "":
        print(
            "Unknown env. Use 'python examine_policy --help' for instructions")
        return

    # load envs
    # adept_envs.global_config.set_config(
    #     args.env_name, {
    #         'robot_params': {
    #             'is_hardware': args.hardware,
    #             'legacy': args.legacy,
    #             'device_name': args.device,
    #             'overlay': args.overlay,
    #             'calibration_mode': args.calibration_mode,
    #         },
    #     })
    e = GymEnv(args.env_name)
    # e.env.env._seed(0)

    # load policy
    policy = args.policy
    mode = args.mode
    if args.policy == "":
        pol = MLP(e.spec, init_log_std=-2)
        mode = "exploration"
        policy = "random_policy.pickle"

    elif args.policy == "saved":
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        policy = curr_dir + "/" + args.env_name + "/best_policy.pickle"
        pol = pickle.load(open(policy, 'rb'))
    else:
        pol = pickle.load(open(policy, 'rb'))

    # dump rollouts
    if (args.num_samples > 0):
        if (mode == "evaluation"):
            pol.log_std = pol.log_std - 10  # since there is no other way of expecifying that we want mean policy samplling

        # parallel sampling
        # paths = trajectory_sampler.sample_paths_parallel(num_samples, pol, e.horizon, env_name, 0, 1)
        # Serial sampling
        paths = do_rollout(
            num_traj=args.num_samples,
            env=args.env_name,
            policy=pol,
            eval_mode = True,
            horizon=e.horizon,
            base_seed=0)

        # Policy stats
        stats = e.env.env.evaluate_success(paths)
        succ_p = np.abs(np.around(stats / 1000000, decimals=2))
        mean_score = (stats / abs(stats+1e-6)) * (abs(stats) - succ_p * 1000000)
        mean_reward = 0
        stats = ''
        for ipath, path in enumerate(paths):
            mean_reward = path['env_infos']['rewards']['total'][-1]
            stats = stats + "path%d:: <score = %+.3f>\n" % (
                ipath, path['env_infos']['score'][-1])
        mean_reward = mean_reward / len(paths)

        # save to a file
        stats = "Policy stats:: <mean reward: %+.3f>, <mean score: %+.3f>, <mean success: %2.1f%%>\n" % (
            mean_reward, mean_score, succ_p)
        file_name = policy[:-7] + '_stats.txt'
        print(stats, file=open(file_name, 'w'))
        print("saved ", file_name)
        print(stats)

        # plot_horizon_distribution(paths, e)
        plot_paths(paths, e, fileName_prefix=policy[:-7])
        file_name = policy[:-7] + '_paths.pickle'
        pickle.dump(paths, open(file_name, 'wb'))
        print("saved ", file_name)

    else:
        # Visualized policy
        if args.render == "onscreen":
            # On screen
            e.env.env.visualize_policy(
                pol,
                horizon=e.horizon,
                num_episodes=args.num_episodes,
                mode=mode)
        else:
            # Offscreen buffer
            e.env.env.visualize_policy_offscreen(
                pol,
                horizon=100,
                num_episodes=args.num_episodes,
                mode=mode,
                filename=args.filename)

    # Close envs
    e.env.env.close_env()


if __name__ == '__main__':
    main()
