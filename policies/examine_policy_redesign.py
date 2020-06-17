from os import environ
environ["MKL_THREADING_LAYER"] = "GNU"
import pickle
import os

# Utilities
import evaluate_args
from mjrl.utils.gym_env import GymEnv
from utils.viz_paths import *

# Policies
from mjrl.policies.gaussian_mlp import MLP

# Samplers
# import mjrl.samplers.trajectory_sampler as trajectory_sampler
# import mjrl.samplers.base_sampler as base_sampler
from mjrl.samplers.core import do_rollout


def main():
    # See evaluate_args.py for the list of args.
    args = evaluate_args.get_args()

    if args.include is not "":
        exec("import "+args.include)

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
    # e.env.env._seed(args.seed)

    # load policy
    policy = args.policy
    mode = args.mode
    if args.policy == "":
        pol = MLP(e.spec, init_log_std=-.50)
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
        # if (mode == "evaluation"):
            # pol.log_std = pol.log_std - 10  # since there is no other way of expecifying that we want mean policy samplling

        # parallel sampling
        # paths = trajectory_sampler.sample_paths_parallel(num_samples, pol, e.horizon, env_name, 0, 1)

        # Serial sampling
        paths = do_rollout(
            num_traj=args.num_samples,
            env=e,
            policy=pol,
            eval_mode = True,
            horizon=e.horizon,
            base_seed=args.seed)

        # Policy stats
        succ_p = e.env.env.evaluate_success(paths)
        mean_reward = 0
        mean_score = 0
        stats = ''
        for ipath, path in enumerate(paths):
            mean_reward += path['env_infos']['rewards']['total'][-1]
            mean_score += path['env_infos']['score'][-1]
            stats = stats + "path%d:: <reward: %+.3f>, <score: %+.3f>\n" % (
                ipath, path['env_infos']['rewards']['total'][-1], path['env_infos']['score'][-1])
        mean_reward = mean_reward / len(paths)
        mean_score = mean_score / len(paths)
        stats += "Policy stats:: <mean reward: %+.3f>, <mean score: %+.3f>, <mean success: %2.1f%%>\n" % (
            mean_reward, mean_score, succ_p)
        print(stats)

        # save to a file
        file_name = policy[:-7] + '_stats.txt'
        print(stats, file=open(file_name, 'w'))
        print("saved ", file_name)

        plot_horizon_distribution(paths, e, fileName_prefix=policy[:-7])
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
