''' Use this script to comapare multiple results \n
    Usage: python viz_results.py -j expdir1_group0 expdir2_group0 -j expdir3_group1 expdir4_group1 -k "key1" "key2"...
'''
# from turtle import width
from vtils.plotting import simple_plot
import argparse
from scipy import signal
import pandas
import glob
import numpy as np

def get_files(search_path, file_name):
    search_path = search_path[:-1] if search_path.endswith('/') else search_path
    search_path = search_path+"*/**/"+file_name
    filenames = glob.glob(search_path, recursive=True)
    assert (len(filenames) > 0), "No file found at: {}".format(search_path)
    return filenames


def get_log(filename, format="csv"):
    try:
        if format=="csv":
            data = pandas.read_csv(filename)
        elif format=="json":
            data = pandas.read_json(filename)
    except Exception as e:
        print("WARNING: Can't read %s." % filename)
        quit()
    return data

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

def plot_single_env(job_dir, env_id, title, legend, subplot_id, args):

    env_dir = job_dir+env_id+"/"
    print("  env> "+env_dir)
    # all the seeds/ variations runs within the env
    yruns = []
    for irun, run_log in enumerate(sorted(get_files(env_dir, args.run_log))):
        print("    run> "+run_log)
        log = get_log(filename=run_log, format="csv")
        # validate keys
        for key in [args.xkey]+args.ykeys:
            assert key in log.keys(), "{} not present in available keys {}".format(key, log.keys())
        if 'sample' in args.xkey: #special keys
            xdata = np.cumsum(log[args.xkey])/1e6
            plot_xkey = args.xkey+"(M)"
        else:
            xdata = log[args.xkey]
            plot_xkey = args.xkey
        yruns.append(log[args.ykeys])
        del log

    # stats over keys
    yruns = pandas.concat(yruns)
    yruns_stacked = yruns.groupby(yruns.index)
    yruns_mean = yruns_stacked.mean()
    yruns_min = yruns_stacked.min()
    yruns_max = yruns_stacked.max()
    yruns_std = yruns_stacked.std()

    for iykey, ykey in enumerate(sorted(args.ykeys)):
        h_figp,h_axis,_= simple_plot.plot(xdata=xdata,
                ydata=smooth_data(yruns_mean[ykey], args.smooth),
                errmin=smooth_data(yruns_min[ykey], args.smooth),
                errmax=smooth_data(yruns_max[ykey], args.smooth),
                legend=legend,
                subplot_id=(3, 3, subplot_id),
                xaxislabel=plot_xkey,
                xaxislimit=(-.1,5.1),
                yaxislimit=(-5,105),
                plot_name=title,
                yaxislabel="success %",
                fig_size=(6, 4),
                fig_name='NPG performance',
                )
    return h_figp, h_axis

def plot_env_pairs(job_dir, env_ids, subplot_id, args):
    h_figp, h_axis = plot_single_env(job_dir, env_id=env_ids[0], title=env_ids[0][:-8], legend="fixed", subplot_id=subplot_id, args=args)
    h_figp, h_axis = plot_single_env(job_dir, env_id=env_ids[1], title=env_ids[0][:-8], legend="random", subplot_id=subplot_id, args=args)

    h_axis.set_xlabel(None)
    h_axis.xaxis.set_ticks((0, 2.5, 5))
    h_axis.xaxis.set_ticklabels([])

    h_axis.yaxis.set_ticks((0, 50, 100))
    h_axis.yaxis.set_ticklabels([])
    h_axis.set_ylabel(None)

    h_axis.get_legend().remove()
    return h_figp, h_axis

# MAIN =========================================================
def main():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-j', '--job', required=True, action='append', nargs='?', help='job group')
    parser.add_argument(
        '-lf', '--run_log', type=str, default="log.csv", help='name of log file (with extension)')
    parser.add_argument(
        '-cf', '--config_file', type=str, default="job_config.json", help='name of config file (with extension)')
    parser.add_argument(
        '-t', '--title', type=str, default=None, help='Title of the plot')
    parser.add_argument(
        '-l', '--label', action='append', nargs='?', help='job group label')
    parser.add_argument(
        '-s', '--smooth', type=int, default=11, help='window for smoothing')
    parser.add_argument(
        '-y', '--ykeys', nargs='+', default=['rwd_dense', 'rwd_sparse', 'success_percentage'], help='yKeys to plot')
    parser.add_argument(
        '-x', '--xkey', default="num_samples", help='xKey to plot')
    args = parser.parse_args()


    job_dir = args.job[0]
    env_ids=["myoFingerReachFixed-v0", "myoFingerReachRandom-v0"]
    h_figp, h_axis = plot_env_pairs(job_dir, env_ids, subplot_id=1, args=args)
    h_axis.set_ylabel("Success %")
    h_axis.yaxis.set_ticklabels(("0", "", "100"))

    env_ids=["myoFingerPoseFixed-v0", "myoFingerPoseRandom-v0"]
    h_figp, h_axis = plot_env_pairs(job_dir, env_ids, subplot_id=2, args=args)

    env_ids=["myoElbowPose1D6MFixed-v0", "myoElbowPose1D6MRandom-v0"]
    h_figp, h_axis = plot_env_pairs(job_dir, env_ids, subplot_id=3, args=args)

    env_ids=["myoHandPoseFixed-v0", "myoHandPoseRandom-v0"]
    h_figp, h_axis = plot_env_pairs(job_dir, env_ids, subplot_id=4, args=args)
    h_axis.set_ylabel("Success %")
    h_axis.yaxis.set_ticklabels(("0", "", "100"))

    env_ids=["myoHandReachFixed-v0", "myoHandReachRandom-v0"]
    h_figp, h_axis = plot_env_pairs(job_dir, env_ids, subplot_id=5, args=args)

    env_ids=["myoHandObjHoldFixed-v0", "myoHandObjHoldRandom-v0"]
    h_figp, h_axis = plot_env_pairs(job_dir, env_ids, subplot_id=6, args=args)

    env_ids=["myoHandKeyTurnFixed-v0", "myoHandKeyTurnRandom-v0"]
    h_figp, h_axis = plot_env_pairs(job_dir, env_ids, subplot_id=7, args=args)
    h_axis.set_ylabel("Success %")
    h_axis.set_xlabel("samples(M)")
    h_axis.xaxis.set_ticklabels(("0", "", "5"))
    h_axis.yaxis.set_ticklabels(("0", "", "100"))

    env_ids=["myoHandPenTwirlFixed-v0", "myoHandPenTwirlRandom-v0"]
    h_figp, h_axis = plot_env_pairs(job_dir, env_ids, subplot_id=8, args=args)
    h_axis.set_xlabel("samples(M)")
    h_axis.xaxis.set_ticklabels(("0", "", "5"))

    env_ids=["myoHandBaodingFixed-v1", "myoHandBaodingRandom-v1"]
    h_figp, h_axis = plot_env_pairs(job_dir, env_ids, subplot_id=9, args=args)
    h_axis.legend()
    h_axis.set_xlabel("samples(M)")
    h_axis.xaxis.set_ticklabels(("0", "", "5"))

    sl = '' if args.job[0].endswith('/') else '/'
    simple_plot.save_plot(args.job[0]+sl+'TrainPerf-NPG.pdf', h_figp)


if __name__ == '__main__':
    main()
