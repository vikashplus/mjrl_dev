''' Use this script to comapare multiple results \n
    Usage: python viz_resulyts.py -j expdir1_group0 expdir2_group0 -j expdir3_group1 expdir4_group1 -k "key1" "key2"...
'''
from vtils.plotting import simple_plot
import json
import yaml
import numpy as np
import argparse
from scipy import signal
import pandas
import glob

def get_files(search_path, file_name):
    search_path = search_path+"/*/**/"+file_name
    filenames = glob.glob(search_path, recursive=True)
    assert (len(filenames) > 0), "No file found at: {}".format(search_path)
    return filenames

# Another example, Python 3.5+
def get_files_p35(search_path, file_name):
    from pathlib import Path
    filenames = []
    for path in Path(search_path).rglob(file_name):
        filenames.append(path)
    return filenames


def get_log(filename, format="csv"):
    try:
        if format=="csv":
            data = pandas.read_csv(filename)
        elif format=="listofdicts":
            data = read_listofDicts(filename)
        elif format=="json":
            data = pandas.read_json(filename)
        elif format=="yaml" or format=="yml":
            with open(filename) as f:
                data = yaml.safe_load(f)
    except Exception as e:
        print("WARNING: Can't read %s." % filename)
        quit()
    return data

def read_listofDicts(filename):
    with open(filename, 'rt') as log_file:
        lines = log_file.read().split('\n')
        dict_list = []
        for l in lines:
            if l != '':
                dictionary = eval(l)
                dict_list.append(dictionary)
    return pandas.DataFrame(dict_list)

def get_job_data(filename):
    Warning("Depricated: Use 'get_log(filename, format='json') instead")
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

def plot_log_keys(log, job_name, smooth, xkeys=None, ykeys=None, title=None, args=None):
        # Default x data
        if xkeys is None:
            xkeys = ['epochs']
            log['epochs'] = range(len(log))

        # keys
        nxkeys = len(xkeys)
        nykeys = len(ykeys)
        for ixkey, xkey in enumerate(xkeys):
            if xkey in ['num_samples']: #special keys
                plot_xdata = np.cumsum(log[xkey])/1e6
                plot_xkey = xkey+"(M)"
            else:
                plot_xdata = log[xkey]
                plot_xkey = xkey

            for iykey, ykey in enumerate(ykeys):
                simple_plot.plot(xdata=plot_xdata, ydata=smooth_data(log[ykey], smooth), legend=job_name, subplot_id=(nxkeys, nykeys, nykeys*ixkey+iykey+1), xaxislabel=plot_xkey, fig_name='viz_csv', plot_name=title, yaxislabel=ykey, fig_size=(4*nykeys, 4*nxkeys), xaxislimit=eval(args.xlim))


# MAIN =========================================================
def main():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-j', '--job', action='append', nargs='+', help='job group')
    parser.add_argument(
        '-f', '--file', type=str, default="log.csv", help='name of log file (with extension)')
    parser.add_argument(
        '-e', '--type', choices=['csv','listofdicts'], default="csv", help='log format')
    parser.add_argument(
        '-t', '--title', type=str, default=None, help='Title of the plot')
    parser.add_argument(
        '-l', '--label', action='append', nargs='?', help='job group label')
    parser.add_argument(
        '-s', '--smooth', type=int, default=21, help='window for smoothing')
    parser.add_argument(
        '-y', '--ykeys', nargs='+', default=["eval_score", "success_percentage"], help='yKeys to plot')
    parser.add_argument(
        '-x', '--xkeys', nargs='+', default=["iteration"], help='xKeys to plot')
    parser.add_argument(
        '-i', '--index', type=int, default=-4, help='index in log filename to use as labels')
    parser.add_argument(
        '-xl', '--xlim', type=str, default=None, help='max xlimit')
    args = parser.parse_args()

    # scan labels
    if args.label is not None:
        assert (len(args.job) == len(args.label)), "The number of labels has to be same as the number of jobs"
    else:
        args.label = [''] * len(args.job)

    # Scan jobs and plot
    for iexp, exp_dir in enumerate(args.job):
        for i, exp_path in enumerate(exp_dir):
            # try:
            #     job = get_job_data(exp_path + '/job_config.json')
            # except Exception as e:
            #     job = get_job_data_txt(exp_path + '/job_data.txt')

            for log_file in get_files(exp_path, args.file):
                print("Reading log: ", log_file)
                log = get_log(filename=log_file, format=args.type)

                # validate keys
                for key in args.xkeys+args.ykeys:
                    assert key in log.keys(), "{} not present in available keys {}".format(key, log.keys())

                # validate lables
                if args.label[iexp] is '':
                    job_name = log_file.split('/')[args.index]
                else:
                    job_name = args.label[iexp]#+str(i)

                # plot keys
                plot_log_keys(log, job_name, args.smooth, xkeys=args.xkeys, ykeys=args.ykeys, title=args.title, args=args)
    simple_plot.show_plot()

if __name__ == '__main__':
    main()
