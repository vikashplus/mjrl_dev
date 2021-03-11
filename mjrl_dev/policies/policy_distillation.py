from mjrl.utils.gym_env import GymEnv
from mjrl.policies.gaussian_mlp import MLP
from mjrl.algos.behavior_cloning import BC
from mjrl.samplers.core import sample_paths
import mjrl.envs
import time as timer
import pickle
import numpy as np

# ------------------------------
# User Inputs
SEED = 500
bc_epochs = 50
n_demos = 50

import aparo
env_name0 = 'AparoBalanceRandom-v0'
policy_path0 = '/home/vik/Projects/aparo/AparoBalanceRandom-v0-j2k_0/iterations/best_policy.pickle'

import darwin
env_name = 'DarwinBalanceRandom-v0'
policy_path = '/home/vik/Projects/darwin/DarwinBalanceRandom-v0-j5a_0/iterations/best_policy.pickle'


def concatenate_paths(path1, path2):
    assert len(path1)==len(path2), "Different number of paths: len(path1)!=len(path2)"
    path0 = []
    for i_path in range(len(path1)):
        path = {}
        horizon = min(path1[i_path]['actions'].shape[0], path2[i_path]['actions'].shape[0])
        path['actions'] = np.hstack([path1[i_path]['actions'][:horizon,:], path2[i_path]['actions'][:horizon,:]])
        path['observations'] = np.hstack([path1[i_path]['observations'][:horizon,:], path2[i_path]['observations'][:horizon,:]])
        path['rewards'] = path1[i_path]['rewards'][:horizon] + path2[i_path]['rewards'][:horizon]
        path['terminated'] = path1[i_path]['terminated'] * path2[i_path]['terminated']
        path0.append(path)
    return path0

def get_paths(env_name, policy_path, num_traj):
    pol = pickle.load(open(policy_path, 'rb'))
    paths = sample_paths(num_traj=n_demos, policy=pol, env=env_name)
    return paths

# ------------------------------
# Get demonstrations
print("========================================")
print("Collecting expert demonstrations")
print("========================================")
demo_paths0 = get_paths(env_name0, policy_path0, n_demos)
demo_paths1 = get_paths(env_name0, policy_path0, n_demos)
fused_paths = concatenate_paths(demo_paths0, demo_paths1)

# ------------------------------
# Train BC
n_inp = demo_paths0[0]['observations'].shape[1] + demo_paths1[0]['observations'].shape[1] 
n_out = demo_paths0[0]['actions'].shape[1] + demo_paths1[0]['actions'].shape[1] 
policy = MLP(input_size=n_inp, output_size=n_out, hidden_sizes=(64,64), seed=SEED)
bc_agent = BC(fused_paths, policy=policy, epochs=bc_epochs, batch_size=64, lr=1e-3) # will use Adam by default
ts = timer.time()
print("========================================")
print("Running BC with expert demonstrations")
print("========================================")
bc_agent.train()
print("========================================")
print("BC training complete !!!")
print("time taken = %f" % (timer.time()-ts))
print("========================================")

"""

# ------------------------------
# Evaluate Policies
bc_pol_score = e.evaluate_policy(policy, num_episodes=20, mean_action=True)
expert_score = e.evaluate_policy(expert_pol, num_episodes=20, mean_action=True)

print("Expert policy performance (eval mode) = %f" % expert_score[0][0])
print("BC policy performance (eval mode) = %f" % bc_pol_score[0][0])


# visualize resulting policy
e.env.env.visualize_policy(
    policy,
    horizon=e.horizon,
    num_episodes=10,
    mode="evaluation")
bc_agent.logger.save_log('/home/vik/Libraries/mjrl/examples/policy_distillation/') 

"""
