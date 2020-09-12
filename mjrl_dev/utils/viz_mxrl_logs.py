''' Use this script to comapare multiple results \n
    Usage: python viz_resulyts.py -j expdir1_group0 expdir2_group0 -j expdir3_group1 expdir4_group1 ...
'''
from vtils.plotting.simple_plot import *
import json
import numpy as np
import argparse
from scipy import signal
import pandas
import glob

def get_file(search_path, file_name):
    filename = glob.glob(search_path+"/*/**"+file_name)
    assert (len(filename) > 0), "No file found at: {}".format(search_path+"/*/**"+file_name)
    assert (len(filename) == 1), "Multiple files found: \n{}".format(filename)
    try:
        data = pandas.read_csv(filename[0])
    except Exception as e:
        print("WARNING: %s not found." % filename[0])
        quit()
    return data

def get_log(filename):
    try:
        data = pandas.read_csv(filename)
    except Exception as e:
        print("WARNING: %s not found." % filename)
    return data


def get_job_data(filename):

    with open(filename) as f:
        job = json.load(f)
    return job


def get_job_data_txt(filename):
    try:
        info = open(filename)
        job = eval(info.read())
    except:
        print("WARNING: %s not found" % filename)
    return job


def smooth_data(y, window_length=101, polyorder=3):
    window_length = min(int(len(y) / 2),
                        window_length)  # set maximum valid window length
    # if window not off
    if window_length % 2 == 0:
        window_length = window_length + 1
    return signal.savgol_filter(y, window_length, polyorder)


def plot_mbrl_logs(log, job, job_name, smooth, user):
        # x axis
        epochs = log['iteration']
        samples = np.cumsum(log['num_samples'])
        horizon = job['horizon']

        # # dynamics pred error
        # ind = 0; keys=[]
        # while "dyn_loss_gen_"+str(ind) in log.keys():
        #     keys.append("dyn_loss_gen_"+str(ind)); ind += 1
        # dyn_loss_gen = log[keys]
        # plot(xdata=epochs, ydata=dyn_loss_gen.mean(axis=1), errmin=dyn_loss_gen.min(axis=1), 
        #     errmax=dyn_loss_gen.max(axis=1), legend=job_name, subplot_id=(3, 2, 1), 
        #     fig_name='MXRL', plot_name="Dynamics pred error")

        # # dynamics training loss
        # ind = 0; keys=[]
        # while "dyn_loss_"+str(ind) in log.keys():
        #     keys.append("dyn_loss_"+str(ind)); ind += 1
        # dyn_loss = log[keys]
        # plot(xdata=epochs, ydata=dyn_loss.mean(axis=1), errmin=dyn_loss.min(axis=1), 
        #     errmax=dyn_loss.max(axis=1), legend=job_name, subplot_id=(3, 2, 3), 
        #     fig_name='MXRL', plot_name="Dynamics training loss")

        # # Policy rewards achieved
        # ind = 0; keys=[]
        # while "rew_loss_"+str(ind) in log.keys():
        #     keys.append("rew_loss_"+str(ind)); ind += 1
        # rew_loss = log[keys]
        # plot(xdata=epochs, ydata=rew_loss.mean(axis=1), errmin=rew_loss.min(axis=1), 
        #     errmax=rew_loss.max(axis=1), legend=job_name, subplot_id=(3, 2, 5), 
        #     fig_name='MXRL', plot_name="Rewards training loss")

        # Policy's evalulation rewards (score)
        plot(xdata=epochs, ydata=smooth_data(log['eval_score'], smooth)/horizon, legend=job_name, subplot_id=(2, 4, 1), fig_name='MXRL', plot_name="Policy's Reward/ Horizon (eval)", fig_size=(16, 8))
        plot(xdata=samples, ydata=smooth_data(log['eval_score'], smooth)/horizon, legend=job_name, subplot_id=(2, 4, 5), fig_name='MXRL', plot_name="Policy's Reward/ Horizon (eval)")

        # Policy's training rewards (score)
        key = 'running_score' if 'running_score' in log.keys() else 'rollout_score'
        plot(xdata=epochs, ydata=smooth_data(log[key], smooth)/horizon, legend=job_name, subplot_id=(2, 4, 2), fig_name='MXRL', plot_name="Policy's Reward/ Horizon (train)")
        plot(xdata=samples, ydata=smooth_data(log[key], smooth)/horizon, legend=job_name, subplot_id=(2, 4, 6), fig_name='MXRL', plot_name="Policy's Reward/ Horizon (train)")

        # Policy's training metric (success rate)
        key = 'success_rate' if 'success_rate' in log.keys() else 'eval_metric'
        plot(xdata=epochs, ydata=smooth_data(log[key], smooth), legend=job_name, subplot_id=(2, 4, 3), fig_name='MXRL', plot_name="Policy's Success (train)")
        plot(xdata=samples, ydata=smooth_data(log[key], smooth), legend=job_name, subplot_id=(2, 4, 7), fig_name='MXRL', plot_name="Policy's Success (train)")

        # Policy's training metric (success rate)
        if 'score' in log.keys():
            key = 'score'
            plot(xdata=epochs, ydata=smooth_data(log[key], smooth), legend=job_name, subplot_id=(2, 4, 4), fig_name='MXRL', plot_name="Policy's score (eval)")
            plot(xdata=samples, ydata=smooth_data(log[key], smooth), legend=job_name, subplot_id=(2, 4, 8), fig_name='MXRL', plot_name="Policy's score (eval)")


        # plot(xdata=epochs, ydata=smooth_data(log['rollout_score'], smooth)/horizon, legend=job_name+' train', subplot_id=(2, 2, 2), fig_name='MXRL', plot_name="Policy's Reward", color=h_plot[0].get_color(), linestyle='--')

        # plot(xdata=samples, ydata=smooth_data(log['rollout_score'], smooth)/horizon, legend=job_name+' train', subplot_id=(2, 2, 1), fig_name='MXRL', plot_name="Policy's Reward", color=h_plot[0].get_color(), linestyle='--')


        # # Success rate
        # h_fig, h_axis, h_plot = plot(xdata=epochs, ydata=smooth_data(log['eval_metric'], smooth), legend=job_name+' eval', subplot_id=(2, 2, 4), fig_name='MXRL', plot_name="Policy's success")
        # plot(xdata=epochs, ydata=smooth_data(log['rollout_metric'], smooth), legend=job_name+' train', subplot_id=(2, 2, 4), fig_name='MXRL', plot_name="Policy's success", color=h_plot[0].get_color(), linestyle='--')




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

    # scan labels
    if args.label is not None:
        assert (len(args.job) == len(args.label)
                ), "The number of labels has to be same as the number of jobs"
    else:
        args.label = [''] * len(args.job)

    # Scan jobs and plot
    for iexp, exp_dir in enumerate(args.job):
        for i, exp_path in enumerate(exp_dir):
            try:
                job = get_job_data(exp_path + '/job_data.json')
            except Exception as e:
                job = get_job_data_txt(exp_path + '/job_data.txt')
                
            log = get_file(exp_path, 'log.csv')

            if args.label[iexp] is '':
                job_name = exp_path.split('/')[-1]
            else:
                job_name = args.label[iexp]#+str(i)

            plot_mbrl_logs(log, job, job_name, args.smooth, args.user)
    show_plot()

if __name__ == '__main__':
    main()
