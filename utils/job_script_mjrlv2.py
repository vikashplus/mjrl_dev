from os import environ

import pickle
import time as timer
import sys
import os
import copy
import itertools
import click
import pprint
from glob import glob
cwd = os.getcwd()

# Utilities
from mjrl.utils.train_agent import train_agent
from mjrl.utils.gym_env import GymEnv
# Policies
from mjrl.policies.gaussian_mlp import MLP
# Baselines
from mjrl.baselines.mlp_baseline import MLPBaseline
# Algos
from mjrl.algos.npg_cg import NPG
# Environments
import robel
# parallel job execution
import multiprocessing as mp


def product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))


def single_process(job):
    job_start_time = timer.time()

    # Allow process to parallelize things internally
    curr_proc = mp.current_process()
    curr_proc.daemon = False

    os.chdir(cwd)
    dirpath = os.path.join(job['save_dir'], job['job_name'])
    os.makedirs(dirpath, exist_ok=True)

    # start job
    os.chdir(cwd)
    job_start_time = timer.time()
    print('Started New Job : ', job['job_name'], '=======================')
    print('Job specifications : \n', job)

    # Make Env
    e = GymEnv(job['env_name'])

    # Make baseline
    baseline = MLPBaseline(e.spec)

    # save job details
    job['horizon'] = e.horizon
    job['ctrl_timestep'] = e.env.env.dt
    job['sim_timestep'] = e.env.env.model.opt.timestep
    # job['sim_skip'] = e.env.env.skip
    job_data_file = open(dirpath + '/job_data.txt', 'w')
    pprint.pprint(job, stream=job_data_file)

    job_data_file.close()

    # Make policy (???vik: sizes are hard coded)
    if 'init_policy' in job:
        policy = MLP(
            e.spec,
            init_log_std=job['init_std'],
            hidden_sizes=(32, 32),
            seed=job['seed'])
        loaded_policy = pickle.load(open(job['init_policy'], 'rb'))
        loaded_params = loaded_policy.get_param_values()
        print('log std values in loaded policy = ')
        print(params[-policy.m:])
        # NOTE: if the log std is too small
        # (say <-2.0, it is problem dependent and intuition should be used)
        # then we need to bump it up so that it explores
        # params[-policy.m:] += 1.0
        policy.set_param_values(loaded_params)
        del job['init_policy']

    else:
        policy = MLP(
            e.spec,
            init_log_std=job['init_std'],
            hidden_sizes=(32, 32),
            seed=job['seed'])
    # Agent
    agent = NPG(e, policy, baseline, seed=job['seed'], \
        normalized_step_size=job['normalized_step_size'], \
        save_logs=job['save_logs'], FIM_invert_args=job['FIM_invert_args'])

    # Train Agent
    train_agent(
        job_name=dirpath,
        agent=agent,
        seed=job['seed'],
        niter=job['niter'],
        gamma=job['gamma'],
        gae_lambda=job['gae_lambda'],
        num_cpu=job['num_cpu'],
        sample_mode=job['sample_mode'],
        num_traj=job['num_traj'],
        evaluation_rollouts=job['evaluation_rollouts'],
        save_freq=job['save_freq'],
        plot_keys={'stoc_pol_mean', 'stoc_pol_std'},
    )

    total_job_time = timer.time() - job_start_time
    print('Job', job['job_name'],
          'took %f seconds ==============' % total_job_time)
    return total_job_time

def notify_user(summary='test subject', details='test body'):
    print(summary + ": ", details)
    if "SMS_GATEWAY" in os.environ:
        send_message(os.environ['SMS_GATEWAY'], summary, details)

@click.command(help='Run Jobs')
@click.option(
    '--configs',
    help='List of comma-separated config patterns.',
    required=True)
@click.option(
    '--save_dir', help='Directory to save trained policies.', default='mjrl')
@click.option('--prefix', help='Prefix to experiment folder name.', default='')
@click.option(
    '--parallel/--sequential',
    help='whether to run jobs in parallel',
    default=False)
def main(configs, save_dir, prefix, parallel):
    patterns = configs.split(',')

    # Scan job sets
    job_set = []
    file_names = []
    for pattern in patterns:
        file_names += glob(pattern)
    for file_name in file_names:
        with open(file_name, 'rb') as f:
            s = f.read()
            job_set.append(eval(s))

    # create jobs
    jobs = []
    ctr = 0
    for j in job_set:
        for j2 in product_dict(**j):
            if prefix:
                j2['job_name'] = '_'.join((prefix, j2['job_name']))
            j2['job_name'] += '_' + str(ctr)
            j2['save_dir'] = save_dir
            jobs.append(j2)
            ctr += 1

    # execute jobs
    t1 = timer.time()
    if parallel:
        # processes: Number of processes to create
        # maxtasksperchild: the number of tasks a worker process can complete before it will exit and be replaced with a fresh worker process
        pool = mp.Pool(processes=len(jobs), maxtasksperchild=1)
        parallel_runs = [
            pool.apply_async(single_process, args=(job, )) for job in jobs
        ]
        try:
            max_process_time = 36000  # process time out in seconds
            results = [p.get(timeout=max_process_time) for p in parallel_runs]
        except Exception as e:
           notify_user("exception thrown in "+jobs[0]['job_name'], str(e))
        
        pool.close()
        pool.terminate()
        pool.join()
    else:
        for job in jobs:
            try:
                time_taken = single_process(job)
            except Exception as e:
               notify_user("exception thrown in "+jobs['job_name'], str(e))
            
    t2 = timer.time()
    notify_user(jobs[0]['job_name'] + "finished", "Total time taken = %f sec" %(t2-t1))



if __name__ == '__main__':
    main()
