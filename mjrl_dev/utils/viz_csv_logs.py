''' Use this script to comapare multiple results \n
    Usage: python viz_resulyts.py -j expdir1_group0 expdir2_group0 -j expdir3_group1 expdir4_group1 -k "key1" "key2"...
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
        return job
    except:
        print("WARNING: %s not found" % filename)
        return None


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

def plot_log_keys(log, job_name, smooth, keys):
        # x axis
        if 'iteration' in log.keys():
            epochs = log['iteration']
        else:
            epochs = range(len(log))
        samples = np.cumsum(log['num_samples'])/1e6

        # keys
        nkeys = len(keys)
        for ikey, key in enumerate(keys):
            plot(xdata=epochs, ydata=smooth_data(log[key], smooth), legend=job_name, subplot_id=(2, nkeys, ikey+1), xaxislabel='epochs', fig_name='viz_csv', plot_name=key, fig_size=(4*nkeys, 8))
            plot(xdata=samples, ydata=smooth_data(log[key], smooth), legend=job_name, subplot_id=(2, nkeys, nkeys+ikey+1), xaxislabel='samples(M)', fig_name='viz_csv', plot_name=key, xaxisscale="log")


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
        '-k', '--keys', nargs='+', default=["running_score"], help='Keys to plot')
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
            # try:
            #     job = get_job_data(exp_path + '/job_config.json')
            # except Exception as e:
            #     job = get_job_data_txt(exp_path + '/job_data.txt')

            log = get_file(exp_path, 'log.csv')

            print(exp_path)
            # if i==4:
            #     args.keys = ["success_rate"]
            # validate keys
            if len(args.keys)>0:
                for key in args.keys:
                    assert key in log.keys(), "{} not present in available keys {}".format(key, log.keys())
            else:
                print("Available keys: ", log.keys())

            # validate lables
            if args.label[iexp] is '':
                job_name = exp_path.split('/')[-1]
            else:
                job_name = args.label[iexp]#+str(i)

            # plot keys
            plot_log_keys(log, job_name, args.smooth, args.keys)
    show_plot()

if __name__ == '__main__':
    main()
