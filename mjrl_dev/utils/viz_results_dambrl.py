''' Use this script to comapare multiple results \n
    Usage: python viz_resulyts.py -j expdir1_group0 expdir2_group0 -j expdir3_group1 expdir4_group1 ...
'''
from vtils.plotting.simple_plot import *
import json
import numpy as np
import argparse
from scipy import signal


def get_log(filename):
    try:
        data = np.genfromtxt(filename, dtype=float, delimiter=',', names=True)
    except Exception as e:
        print("WARNING: %s not found." % filename)
    return data


def get_job_data(filename):

    with open(filename) as f:
        job = json.load(f)
    return job


def smooth_data(y, window_length=101, polyorder=3):
    window_length = min(int(len(y) / 2),
                        window_length)  # set maximum valid window length
    # if window not off
    if window_length % 2 == 0:
        window_length = window_length + 1
    return signal.savgol_filter(y, window_length, polyorder)


# MAIN =========================================================
def main():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-j', '--job', action='append', nargs='+', help='job group')
    parser.add_argument(
        '-l', '--label', action='append', nargs='?', help='job group label')
    parser.add_argument(
        '-s', '--smooth', type=int, default=101, help='window for smoothing')
    parser.add_argument(
        '-u', '--user', type=str, default=None, help='User defined field from log')
    args = parser.parse_args()

    results_info = ''

    # scan labels
    if args.label is not None:
        assert (len(args.job) == len(args.label)
                ), "The number of labels has to be same as the number of jobs"
    else:
        args.label = [''] * len(args.job)

    # Scan jobs and plot
    for iexp, exp_dir in enumerate(args.job):
        for i, exp_path in enumerate(exp_dir):
            job = get_job_data(exp_path + '/job_data.json')
            log = get_log(exp_path + '/log.csv')

            if args.label[iexp] is '':
                job_name = exp_path.split('/')[-1]
            else:
                job_name = args.label[iexp]#+str(i)

            epochs = np.arange(len(log['rollout_score']))
            # rewards
            reward_metric = smooth_data(log['rollout_metric'], window_length=args.smooth)
            reward_score = smooth_data(log['rollout_score'], window_length=args.smooth)/job['horizon']
            eval_metric = smooth_data(log['eval_metric'], window_length=args.smooth)
            eval_score = smooth_data(log['eval_score'], window_length=args.smooth)/job['horizon']
            plot(xdata=epochs, ydata=reward_metric, legend=job_name, yaxislabel='reward_metric', subplot_id=(2, 2, 1), fig_name='DA-MBRL')
            plot(xdata=epochs, ydata=reward_score, legend=job_name, yaxislabel='reward_score/horizon', subplot_id=(2, 2, 2), fig_name='DA-MBRL')
            plot(xdata=epochs, ydata=eval_metric, legend=job_name, yaxislabel='eval_metric', subplot_id=(2, 2, 3), fig_name='DA-MBRL')
            plot(xdata=epochs, ydata=eval_score, legend=job_name, yaxislabel='eval_score/horizon', subplot_id=(2, 2, 4), fig_name='DA-MBRL')

    show_plot()

if __name__ == '__main__':
    main()
