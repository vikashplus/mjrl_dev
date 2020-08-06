import copy
import logging
import os
import pickle
import time as timer

import numpy as np
from tabulate import tabulate

from mjrl.utils.make_train_plots import make_train_plots
from mjrl.samplers.trajectory_sampler import sample_paths_parallel

# from adept_envs.utils.tensorboard import tensorboard


def train_loop(job_name,
               agent,
               save_dir,
               seed = 0,
               niter = 101,
               gamma = 0.995,
               gae_lambda = None,
               num_cpu = 1,
               sample_mode = 'trajectories',
               num_samples = None,
               save_freq = 10,
               evaluation_rollouts = None,
               plot_keys = ['stoc_pol_mean']):
    """Trains the given agent and saves the resultant policies.

    Args:
        job_name: The title of the job.
        agent: The MJRL agent to train.
        save_dir: The directory to save the trained policies and logs to.
        seed: The seed for np.random.
        niter: The number of iterations.
        gamma: Discount factor.
        gae_lambda: Multiplier to the discount factor when calculating advantages.
        num_cpu: Number of CPUs used to perform the train step and sampling
        sample_mode: One of 'trajectories' or 'samples'.
        num_samples: The number of samples. This is the number of trajectories
            in trajectory sampling mode, or the number of samples in the batch
            otherwise.
        save_freq: The frequency of iterations when the policy is saved.
        evaluation_rollouts: The number of evaluation rollouts to perform per iteration.
        plot_keys: The keys plotted on the training plot.
    """
    # Validate parameters.
    if not os.path.isdir(save_dir):
        raise ValueError('Save directory {} does not exist'.format(save_dir))
    if sample_mode not in ['trajectories', 'samples']:
        raise ValueError('Invalid sample mode: {}'.format(sample_mode))

    # Choose a default for num_samples if not specified.
    if num_samples is None:
        num_samples = 50 if sample_mode == 'trajectories' else 50000

    # Initialize the folders in the save directory.
    iterations_dir = os.path.join(save_dir, 'iterations')
    if not os.path.isdir(iterations_dir):
        os.mkdir(iterations_dir)
    logs_dir = os.path.join(save_dir, 'logs')
    if agent.save_logs and not os.path.isdir(logs_dir):
        os.mkdir(logs_dir)

    # Initialize results log file.
    results_path = os.path.join(save_dir, 'results.txt')
    open(results_path, 'w').close()

    # Initialize training variables.
    np.random.seed(seed)
    best_policy = copy.deepcopy(agent.policy)
    best_perf = -1e8
    train_curve = best_perf * np.ones(niter)
    mean_pol_perf = 0.0

    # Prefix tensorboard logs with the job name.
    # tb_logger = tensorboard.get_prefixed(job_name)
    tb_logger = []
    # print('Starting training for job: {}'.format(job_name))

    for i in range(niter):
        print('.' * 80 + '\nITERATION : {}'.format(i))

        if train_curve[i-1] > best_perf:
            best_policy = copy.deepcopy(agent.policy)
            best_perf = train_curve[i-1]

        stats = agent.train_step(
            N=num_samples,
            sample_mode=sample_mode,
            gamma=gamma,
            gae_lambda=gae_lambda,
            num_cpu=num_cpu,
        )
        train_curve[i] = stats[0]

        if evaluation_rollouts is not None and evaluation_rollouts > 0:
            print('Performing evaluation rollouts ........')
            mean_pol_perf = _evaluation_rollout(agent, evaluation_rollouts, num_cpu)
            if agent.save_logs:
                agent.logger.log_kv('eval_score', mean_pol_perf)

        if i % save_freq == 0 and i > 0:
            _save_policy(agent.policy, 'policy_{}'.format(i), iterations_dir)
            _save_policy(agent.baseline, 'baseline_{}'.format(i), iterations_dir)
            _save_policy(best_policy, 'best_policy', iterations_dir)
            if agent.save_logs:
                agent.logger.save_log(logs_dir)
                make_train_plots(log=agent.logger.log, keys=plot_keys, save_loc=logs_dir)

        _log_performance(i, train_curve[i], mean_pol_perf, best_perf,
                         results_path, tb_logger)
        if agent.save_logs:
            print_data = sorted(filter(lambda v: np.asarray(v[1]).size == 1,
                                       agent.logger.get_current_log().items()))
            print(tabulate(print_data))

    # Save the final best policy.
    _save_policy(best_policy, 'best_policy', iterations_dir)
    if agent.save_logs:
        agent.logger.save_log(logs_dir)
        make_train_plots(log=agent.logger.log, keys=plot_keys, save_loc=logs_dir)

def _evaluation_rollout(agent, num_rollouts, num_cpu):
    """Performs an evaluation rollout.

    Args:
        agent: The MJRL agent to perform the rollout with.
        num_rollouts: The number of rollouts.
        num_cpu: The number of CPUs to perform the rollout on.

    Returns:
        The mean return over the rollout.
    """
    eval_paths = sample_paths_parallel(
        N=num_rollouts,
        policy=agent.policy,
        num_cpu=num_cpu,
        env_name=agent.env.env_id,
        mode='evaluation',
    )
    return np.mean([np.sum(path['rewards']) for path in eval_paths])

def _save_policy(policy, file_name, output_dir):
    """Saves the given policy.

    Args:
        policy: The policy object to pickle and save.
        file_name: The name to save the policy as. '.pickle' is appended to
            this file name.
        output_dir: The directory to save the policy to.
    """
    assert os.path.isdir(output_dir)
    with open(os.path.join(output_dir, file_name + '.pickle'), 'wb') as file:
        pickle.dump(policy, file)

def _log_performance(i, train_perf, mean_pol_perf, best_perf, results_path,
                     tb_logger):
    """Logs the performance for the given iteration.

    Args:
        i: The current iteration number.
        train_perf: The mean return over the paths for the current iteration.
        mean_pol_perf: The last mean return from an evaluation rollout.
        best_perf: The best mean return over all previous iterations.
        tb_logger: Tensorboard logger to use.
    """
    # tb_logger.add_scalars('performance', {
    #     'train_perf': train_perf,
    #     'eval_perf': mean_pol_perf,
    #     'best_train_perf': best_perf,
    # }, global_step=i)

    with open(results_path, 'a') as results_file:
        if i == 0:
            headings = ['Iter', 'Sampled Pol', 'Mean Pol', 'Best (Sampled)']
            headings = ' | '.join(headings)
            results_file.write(headings + '\n')
            print('Timestamp' + (' ' * 17)  + ' | ' + headings)

        log = ['{:<4d}', '{:>11.2f}', '{:>8.2f}', '{:>14.2f}']
        log = '   '.join(log).format(i, train_perf, mean_pol_perf, best_perf)
        results_file.write(log + '\n')
        print('{:<26s}   {}'.format(
            timer.asctime(timer.localtime(timer.time())), log))
