import glob, os
import argparse
import pandas
from vtils.plotting.simple_plot import *
import numpy as np
from scipy import signal

def get_csv(search_path, file_name):
    filenames = glob.glob(search_path+"/*/**"+file_name)
    assert (len(filenames) > 0), "No file found at: {}".format(search_path+"/*/**"+file_name)
    # assert (len(filenames) == 1), "Multiple files found: \n{}".format(filenames)
    data = []
    for filename in filenames:
        try:
            print("Reading logs from", filename)
            dat = pandas.read_csv(filename)
            data.append(dat)
        except Exception as e:
            print("WARNING: %s not found." % filename)
            quit()
    return data

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
        '-u', '--user', type=str, default='reward-mean', help='User defined field from log')
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

            if args.label[iexp] is '':
                job_name = exp_path.split('-')[-1]
            else:
                job_name = args.label[iexp]#+str(i)

            # job = get_job_data(exp_path + '/job_data.json')
            logs = get_csv(exp_path, "progress.csv")
            for il, log in enumerate(logs):
                # x axis: find all matching keys
                plot_keys = [key for key in log.keys() if args.user in key]

                max_keys = len(plot_keys)
                for ikey, key in enumerate(plot_keys):
                    plot(xdata=log['epoch'], ydata=smooth_data(log[key], window_length=args.smooth), legend=job_name+str(il), plot_name=key, subplot_id=(1, max_keys, ikey+1), fig_name="SAC")

    show_plot()

if __name__ == '__main__':
    main()