"""Script for launching training jobs."""

import copy
import glob
import itertools
import os
import pickle
import time as timer
import traceback
import pprint
import psutil

os.environ['MKL_THREADING_LAYER'] = 'GNU'

# Utilities
import train_args
from train_loop import train_loop
from mjrl.utils.gym_env import GymEnv
# Policies
from mjrl.policies.gaussian_mlp import MLP
# Baselines
from mjrl.baselines.mlp_baseline import MLPBaseline
# Algos
from mjrl.algos.npg_cg import NPG
# Environments
import robel
import deepmimic.envs
import aparo.envs

# from adept_envs.utils.tensorboard import tensorboard
# parallel job execution
import multiprocessing as mp

from robel_dev.utils.notification import send_message


# Import shared framework utils.
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../utils'))
# import config_reader


def single_process(job):
    job_start_time = timer.time()

    # Allow process to parallelize things internally
    curr_proc = mp.current_process()
    curr_proc.daemon = False

    # Create a directory for the job results.
    job_dir = os.path.join(job['output_dir'])
    if not os.path.isdir(job_dir):
        os.mkdir(job_dir)

    # start job
    job_start_time = timer.time()
    print('Started New Job : ', job['job_name'], '=======================')
    print('Job specifications : \n', job)

    # Make Env
    env_name = job['env_name']
    # adept_envs.global_config.set_config(env_name, {
    #     'robot_params': job['robot'],
    #     **job.get('env_params', {}),
    # })
    e = GymEnv(env_name)

    # Make baseline
    baseline = MLPBaseline(e.spec)

    # save job details
    job['horizon'] = e.horizon
    job['ctrl_timestep'] = e.env.env.dt
    job['sim_timestep'] = e.env.env.model.opt.timestep
    # job['sim_skip'] = e.env.env.skip

    with open(os.path.join(job_dir, 'job_data.txt'), 'w') as job_data_file:
        pprint.pprint(job, stream=job_data_file)

    if 'init_policy' in job:
        policy = MLP(e.spec, init_log_std=job['init_std'], hidden_sizes=(32,32), seed=job['seed'])
        loaded_policy = pickle.load(open(job['init_policy'], 'rb'))
        loaded_params = loaded_policy.get_param_values()
        print("log std values in loaded policy = ")
        print(loaded_params[-policy.m:])
        # NOTE: if the log std is too small 
        # (say <-2.0, it is problem dependent and intuition should be used)
        # then we need to bump it up so that it explores
        loaded_params[-policy.m:] += 1.0
        policy.set_param_values(loaded_params)
        del job['init_policy']

    else:
        policy = MLP(
            e.spec,
            init_log_std=job['init_std'],
            hidden_sizes=job['hidden_sizes'],
            # hidden_sizes=(32, 32),
            seed=job['seed'])

    # Agent
    agent = NPG(
        e,
        policy,
        baseline,
        seed=job['seed'],
        normalized_step_size=job['normalized_step_size'],
        save_logs=job['save_logs'],
        FIM_invert_args=job['FIM_invert_args'])

    # Train Agent
    train_loop(
        job_name=job['job_name'],
        agent=agent,
        save_dir=job_dir,
        seed=job['seed'],
        niter=job['niter'],
        gamma=job['gamma'],
        gae_lambda=job['gae_lambda'],
        num_cpu=job['num_cpu'],
        sample_mode=job['sample_mode'],
        num_samples=job.get('num_traj') or job.get('num_samples'),
        evaluation_rollouts=job['evaluation_rollouts'],
        save_freq=job['save_freq'],
        plot_keys={'stoc_pol_mean', 'stoc_pol_std'},
    )

    total_job_time = timer.time() - job_start_time
    print('Job', job['job_name'],
          'took %f seconds ==============' % total_job_time)
    return total_job_time


def product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))

def notify_user(summary='test subject', details='test body'):
    details += ":: CPU-" + str(psutil.cpu_percent()) + str(psutil.virtual_memory())
    print(summary + ": ", details)
    if "SMS_GATEWAY" in os.environ:
        send_message(os.environ['SMS_GATEWAY'], summary, details)

def main():

    # See train_args.py for the list of args.
    args = train_args.get_args()

    # Get the config files, expanding globs and directories (*) if necessary.
    # jobs = config_reader.process_config_files(args.config)
    # assert jobs, 'No jobs found from config.'

    # Scan job sets
    job_set = []
    for i in range(0, 1):
        file_name = 'job_data_mjrl_%d.txt' % i
        with open(file_name, 'rb') as f:
            s = f.read()
            job_set.append(eval(s))

    # create jobs 
    jobs = []
    ctr = 0
    for j in job_set:
        for j2 in product_dict(**j):
            j2['job_name'] = j2['job_name'] + "_" + str(ctr)
            jobs.append(j2)
            ctr += 1


    # Create the output directory if not present.
    output_dir = args.output_dir or os.getcwd()
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    output_dir = os.path.abspath(output_dir)

    # If the log directory is given, enable Tensorboard logging.
    # Create the Tensorboard log directory if not present.
    if args.tensorboard:
        tb_output_path = os.path.join(output_dir, 'tensorboard')
        if not os.path.isdir(tb_output_path):
            os.mkdir(tb_output_path)
        tensorboard.enable(tb_output_path)

    robot_args = {
        'is_hardware': args.hardware,
        'legacy': args.legacy,
        'device_name': args.device,
        'overlay': args.overlay,
        'calibration_mode': args.calibration_mode,
    }

    for index, job in enumerate(jobs):
        # Modify the job name to include the job number.
        assert 'job_name' in job
        if len(jobs) > 1:
            job['job_name'] = '{}_{}'.format(job['job_name'], index)

        # Add additional parameters to the job.
        job['output_dir'] = os.path.join(output_dir, job['job_name'])

        # Set the robot configuration.
        if 'robot' not in job:
            job['robot'] = {}
        # Only keep the entries where the arg is given.
        job['robot'].update({k: v for k, v in robot_args.items() if v})

        # Override num_cpus if the args.num_cpu is given or if we're running on hardware.
        job['num_cpu'] = 1 if args.hardware else (args.num_cpu
                                                  or job['num_cpu'])

    print('Running {} jobs {}'.format(
        len(jobs), 'in parallel' if args.parallel else 'sequentially'))

    # execute jobs
    t1 = timer.time()
    if args.parallel:
        # processes: Number of processes to create
        # maxtasksperchild: the number of tasks a worker process can complete before it will exit and be replaced with a fresh worker process
        pool = mp.Pool(processes=len(jobs), maxtasksperchild=1)
        parallel_runs = [
            pool.apply_async(single_process, args=(job, )) for job in jobs
        ]
        try:
            max_process_time = 360000  # process time out in seconds
            results = [p.get(timeout=max_process_time) for p in parallel_runs]
        except Exception as e:
            notify_user("exception thrown in "+jobs[0]['job_name'], str(e))
            print('exception thrown')
            print(str(e))
            traceback.print_exc()

        pool.close()
        pool.terminate()
        pool.join()
    else:
        for job in jobs:
            try:
                time_taken = single_process(job)
            except Exception as e:
                notify_user("exception thrown in "+jobs['job_name'], str(e))
                print('exception thrown')
                print(str(e))
                traceback.print_exc()

    t2 = timer.time()
    notify_user(jobs[0]['job_name'] + "finished", "Total time taken = %f sec" %(t2-t1))
    print('Total time taken = ', t2 - t1)

    # Send notifcation to the user
    msg_subject = job['job_name'] + ' completed'
    msg_body = 'Total time taken = %f' % (t2 - t1)
    msg_body += ":: CPU-" + str(psutil.cpu_percent()) + str(psutil.virtual_memory())

    if args.email:
        send_message(args.email, msg_subject, msg_body)
    if args.sms:
        send_message(args.sms, msg_subject, msg_body)
    return


if __name__ == '__main__':
    main()
