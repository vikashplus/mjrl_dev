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

def get_csv(search_path, file_name):
    filename = glob.glob(search_path+"/*/**"+file_name)
    assert (len(filename) > 0), "No file found at: {}".format(search_path+"/*/**"+file_name)
    assert (len(filename) == 1), "Multiple files found: \n{}".format(filename)
    try:
        data = pandas.read_csv(filename[0])
    except Exception as e:
        print("WARNING: %s not found." % filename[0])
        quit()
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
    try:
        return signal.savgol_filter(y, window_length, polyorder)
    except Exception as e:
        return y # nans


def plot_mbrl_logs(log, job, job_name, smooth, user):
        # x axis
        n_epochs = len(log['rollout_score'])
        epochs = np.arange(n_epochs)
        horizon = job['horizon']

        # dynamics pred error
        ind = 0; keys=[]
        while "dyn_loss_gen_"+str(ind) in log.keys():
            keys.append("dyn_loss_gen_"+str(ind)); ind += 1
        n_dyn_models = ind-1
        dyn_loss_gen = np.log10(log[keys])
        h_fig, h_axis, h_plot = plot(xdata=epochs, ydata=dyn_loss_gen.mean(axis=1), errmin=dyn_loss_gen.min(axis=1), 
            errmax=dyn_loss_gen.max(axis=1), legend=job_name, subplot_id=(3, 2, 1), 
            fig_name='MBRL', plot_name="Dynamics pred error (log10)", fig_size=(12,8))
        job_color = h_plot[0].get_color()

        # dynamics training loss
        ind = 0; keys=[]
        while "dyn_loss_"+str(ind) in log.keys():
            keys.append("dyn_loss_"+str(ind)); ind += 1
        n_dyn_models = ind-1
        dyn_loss = np.log10(log[keys])
        plot(xdata=epochs, ydata=dyn_loss.mean(axis=1), errmin=dyn_loss.min(axis=1), 
            errmax=dyn_loss.max(axis=1), legend=job_name, subplot_id=(3, 2, 3), 
            fig_name='MBRL', plot_name="Dynamics training loss (log10)")

        # Rewards learning loss
        ind = 0; keys=[]
        while "rew_loss_"+str(ind) in log.keys():
            keys.append("rew_loss_"+str(ind)); ind += 1
        n_rew_models = ind-1
        rew_loss = log[keys]
        plot(xdata=epochs, ydata=rew_loss.mean(axis=1), errmin=rew_loss.min(axis=1), 
            errmax=rew_loss.max(axis=1), legend=job_name, subplot_id=(3, 2, 5), 
            fig_name='MBRL', plot_name="Rewards training loss")

        # Policy's rewards
        plot(xdata=epochs, ydata=smooth_data(log['eval_score'], smooth)/horizon, legend=job_name+' eval', subplot_id=(3, 2, 2), fig_name='MBRL', plot_name="Policy's Reward/ Horizon", linewidth=4)
        plot(xdata=epochs, ydata=smooth_data(log['rollout_score'], smooth)/horizon, legend=job_name+' train', subplot_id=(3, 2, 2), fig_name='MBRL', plot_name="Policy's Reward/ step", color=job_color, linestyle='--', linewidth=1.5)

        # Policy's success rate
        try:
            plot(xdata=epochs, ydata=smooth_data(log['eval_metric'], smooth), legend=job_name+' eval', subplot_id=(3, 2, 4), fig_name='MBRL', plot_name="Policy's success", linewidth=4)
        except:
            pass
        plot(xdata=epochs, ydata=smooth_data(log['rollout_metric'], smooth), legend=job_name+' train', subplot_id=(3, 2, 4), fig_name='MBRL', plot_name="Policy's success", color=job_color, linestyle='--', linewidth=1.5)


        # time ['data_collect_time, 'model_update_time', 'policy_update_time', 'eval_log_time', 'iter_time']
        plot(xdata=epochs, ydata=log['iter_time'], legend=job_name+' iter', subplot_id=(3, 2, 6), fig_name='MBRL', plot_name="Computation time", linestyle='-', linewidth=5)
        plot(xdata=epochs, ydata=log['data_collect_time'], legend=job_name+' sample', subplot_id=(3, 2, 6), fig_name='MBRL', plot_name="Computation time", color=job_color, linestyle='-', linewidth=1, alpha=0.5)
        plot(xdata=epochs, ydata=log['model_update_time'], legend=job_name+' model', subplot_id=(3, 2, 6), fig_name='MBRL', plot_name="Computation time", color=job_color, linestyle='--', linewidth=1, alpha=0.5)
        plot(xdata=epochs, ydata=log['policy_update_time'], legend=job_name+' policy', subplot_id=(3, 2, 6), fig_name='MBRL', plot_name="Computation time", color=job_color, linestyle=':', linewidth=2, alpha=0.5)
        plot(xdata=epochs, ydata=log['eval_log_time'], legend=job_name+' eval', subplot_id=(3, 2, 6), fig_name='MBRL', plot_name="Computation time", color=job_color, linestyle='-.', linewidth=3, alpha=0.5)

        # return
        # SUBSTEPS =================================================================================================
        # policy leanring curves
        n_pol_substeps = 0
        while "rollout_score_mean_0."+str(n_pol_substeps) in log.keys():
            n_pol_substeps += 1
        keys = []
        for i_substep in range(n_pol_substeps):
            keys.append("rollout_score_mean_{}.{}".format(0, i_substep))
        keys.append(keys[-1]) # add a fake dim that we will convert to nan
        rew_learning = log[keys].values/horizon; rew_learning[:,-1] = np.nan

        plot(xdata=np.arange(0, n_epochs, 1/(n_pol_substeps+1)), ydata=rew_learning.ravel(), subplot_id=(3, 2, 1), fig_name="MBRL (epochs.substeps)", plot_name="pol train loss", xaxislabel="epochs", marker='.', legend=job_name, color=job_color, fig_size=(12,8))
        plot(log[keys[-1]]-log[keys[0]], subplot_id=(3, 2, 2), fig_name="MBRL (epochs.substeps)", plot_name="pol improvement", xaxislabel="epochs", marker='.', legend=job_name, color=job_color)


        # dynamics leanring curves
        n_dyn_substeps = 0
        while "dyn_loss_0."+str(n_dyn_substeps) in log.keys():
            n_dyn_substeps += 1
        for i_model in range(n_dyn_models):
            keys = []
            for i_substep in range(n_dyn_substeps):
                keys.append("dyn_loss_{}.{}".format(i_model, i_substep))

            dyn_learning = log[keys].values; dyn_learning[:,-1] = np.nan
            plot(xdata=np.arange(0, n_epochs, 1/n_dyn_substeps), ydata=np.log10(dyn_learning.ravel()), subplot_id=(3, 1, 2), fig_name="MBRL (epochs.substeps)", plot_name="dyn train loss(log10)", xaxislabel="epochs.substeps", color=job_color)

        # rewards leanring curves
        if n_rew_models>0:
            n_rew_substeps = 0
            while "rew_loss_0."+str(n_rew_substeps) in log.keys():
                n_rew_substeps += 1
            for i_model in range(n_rew_models):
                keys = []
                for i_substep in range(n_rew_substeps):
                    keys.append("rew_loss_{}.{}".format(i_model, i_substep))
                
                rew_learning = log[keys].values; rew_learning[:,-1] = np.nan
                plot(xdata=np.arange(0, n_epochs, 1/n_rew_substeps), ydata=np.log10(rew_learning.ravel()), subplot_id=(3, 1, 3), fig_name="MBRL (epochs.substeps)", plot_name="rew_{} train loss(log10)".format(i_model), xaxislabel="epochs.substeps", legend=job_name+"rew"+str(i_model), color=job_color)




# MAIN =========================================================
def main():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-j', '--job', action='append', nargs='+', help='job group')
    parser.add_argument(
        '-l', '--label', action='append', nargs='?', help='job group label')
    parser.add_argument(
        '-s', '--smooth', type=int, default=21, help='window for smoothing')
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
            job = get_job_data(exp_path + '/job_data.json')
            log = get_csv(exp_path, 'log.csv')

            if args.label[iexp] is '':
                job_name = exp_path.split('/')[-1]
            else:
                job_name = args.label[iexp]#+str(i)

            plot_mbrl_logs(log, job, job_name, args.smooth, args.user)
    show_plot()

if __name__ == '__main__':
    main()
