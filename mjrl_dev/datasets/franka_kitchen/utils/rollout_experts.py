from mjrl.utils.gym_env import GymEnv
from mjrl.algos.npg_cg import NPG
from mjrl.samplers.core import sample_paths

import pickle
import numpy as np
import gym
import mj_envs
import click

DESC = '''
Script to rollouts expert demos from an expert policy
    $ python rollouts_experts.py --policy <path/to/npg-policy? --env kitchen_knob1_on-v3 \n
'''

@click.command(help=DESC)
@click.option('--policy', type=str, help='path to the expert policy', required=True)
@click.option('--env', type=str, help='env to rollout policy in', required=True)
@click.option('--output_dir', type=str, help='dir to save demos to', default='../../datasets/hydra_datasets/expert')
@click.option('--num_demos', type=int, help='number of demos to rollout', default=50)
@click.option('--noise', type=float, help='how noisy should expert rollouts be', default=0.0)

def main(policy, env, output_dir, num_demos, noise):
    e = GymEnv(env)
    policy = pickle.load(open(policy, 'rb'))
    policy.log_std_val = np.ones_like(policy.log_std_val) * noise
    demo_paths = sample_paths(env=e.env_id, policy=policy, num_traj=num_demos, eval_mode=True)

    # evaluate expert rollout
    expert_score = np.mean([np.sum(p['rewards']) for p in demo_paths])
    expert_success_rate = e.env.env.evaluate_success(demo_paths)
    print("Expert policy performance = " , expert_score)
    print("Expert policy success rate (demos) = %f" % expert_success_rate)

    pickle.dump(demo_paths, open(output_dir + '/' + e.env_id + '.pkl', 'wb'))

if __name__ == '__main__':
    main()