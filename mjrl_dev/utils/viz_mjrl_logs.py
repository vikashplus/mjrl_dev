''' Use this script to comapare multiple results \n
    Usage: python viz_resulyts.py -j expdir1_group0 expdir2_group0 -j expdir3_group1 expdir4_group1 ...
'''

import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 8})
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_pdf import PdfPages

import sys
from termcolor import cprint
import argparse
from scipy import signal
import warnings
warnings.filterwarnings(
    action="ignore", module="scipy", message="^internal gelsd")


def get_results(filename):
    results = []
    try:
        data = np.loadtxt(filename, skiprows=1)
        results = {
            'iter': data[:, 0],
            'reward': data[:, 1],
            'episode': data[:, -1]
        }
    except Exception as e:
        print("WARNING: %s not found." % filename)
    return results


def get_log(filename):
    try:
        data = np.genfromtxt(filename, dtype=float, delimiter=',', names=True)
    except Exception as e:
        print("WARNING: %s not found." % filename)
    return data


def get_job_data(filename):
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
    try:
        return signal.savgol_filter(y, window_length, polyorder)
    except:
        return y


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
    parser.add_argument(
        '-x', '--xlim', type=str, default=None, help='max xlimit')
    args = parser.parse_args()

    # Prepare plots
    fig = plt.figure()
    ax1 = fig.add_subplot(4, 2, 1)
    ax2 = fig.add_subplot(4, 2, 2)
    ax3 = fig.add_subplot(4, 2, 3)
    ax4 = fig.add_subplot(4, 2, 4)
    ax5 = fig.add_subplot(4, 2, 5)
    ax6 = fig.add_subplot(4, 2, 6)
    ax7 = fig.add_subplot(4, 2, 8)
    ax8 = fig.add_subplot(4, 2, 7)
    results_info = ''

    # scan labels
    if args.label is not None:
        assert (len(args.job) == len(args.label)
                ), "The number of labels has to be same as the number of jobs"
    else:
        args.label = [''] * len(args.job)

    # Scan jobs and plot
    for iexp, exp_dir in enumerate(args.job):
        sum_reward = None
        sum_score = None
        sum_succ_p = None
        exp_info = '%30s  seed     std   #traj    gamma     reward    score    success%%' % (
            'job group ' + str(iexp))
        results_info = results_info + exp_info + '\n'
        cprint(exp_info, 'white', 'on_blue', attrs=['bold', 'underline'])
        for i, exp_path in enumerate(exp_dir):
            job = get_job_data(exp_path + '/job_data.txt')
            log = get_log(exp_path + '/logs/log.csv')
            epochs = np.arange(len(log['stoc_pol_mean']))
            samples = np.cumsum(log['num_samples']) #epochs * job['num_traj'] * job['horizon']
            # rewards
            reward = smooth_data(log['stoc_pol_mean'], window_length=args.smooth)/job['horizon'] # termination penalties provides rewards for path beyong termination
            ax1.plot(epochs, reward, label=job['job_name'], linewidth=2)
            ax7.plot(samples, reward, label=job['job_name'], linewidth=2)
            
            # score
            # score = smooth_data(log['score'], window_length=args.smooth)/log['num_samples'] # no termination penalties, hence normalized by samples
            if 'score' in log.dtype.names:
                score = smooth_data(log['score'], window_length=args.smooth) # score/step is returned
            else:
                score = np.zeros_like(reward)
            ax3.plot(epochs, score, label=job['job_name'], linewidth=2)

            # Success percentage
            try:
                succ_p = smooth_data(log['success_rate'], window_length=args.smooth)
            except ValueError as e:
                succ_p = np.zeros(len(reward))
            ax5.plot(epochs, succ_p, label=job['job_name'], linewidth=2)
            
            # user
            if args.user is not None:
                try:
                    user = smooth_data(log[args.user], window_length=args.smooth)
                except:
                    print("%s not found"%args.user)
                    user = np.nan*epochs
                # user = log['time_sampling']+log['time_vpg']+log['time_npg']
                ax8.plot(epochs, user, label=job['job_name'], linewidth=2)


            # gather stats 
            if sum_reward is not None:
                sum_reward_min_length = min(len(sum_reward), len(score))
                sum_reward = sum_reward[:sum_reward_min_length] + reward[:sum_reward_min_length]
                sum_score = sum_score[:sum_reward_min_length] + score[:sum_reward_min_length]
                sum_succ_p = sum_succ_p[:sum_reward_min_length] + succ_p[:sum_reward_min_length]
            else:
                sum_reward = reward
                sum_score = score
                sum_succ_p = succ_p
                sum_reward_min_length = len(sum_reward)
            
            # gather records 
            exp_info = '%30s   %3d   %+1.2f     %3d    %0.3f    %+.2f    %+.2f    %.1f%%' % (job['job_name'], job['seed'], \
                job['init_std'], job['num_traj'], job['gamma'], reward[-1], score[-1], succ_p[-1])
            print(exp_info)
            results_info = results_info + exp_info + '\n'

        # stats
        mean_reward = sum_reward[:sum_reward_min_length] / len(exp_dir)
        mean_score = sum_score[:sum_reward_min_length] / len(exp_dir)
        mean_succ_p = sum_succ_p[:sum_reward_min_length] / len(exp_dir)
        ax2.plot(mean_reward, label='g' + str(iexp) + ':' + args.label[iexp])
        ax4.plot(mean_score, label='g' + str(iexp) + ':score')
        ax6.plot(mean_succ_p, label='g' + str(iexp) + ':' + 'success%')
        group_stats = "Group stats: <mean reward %+.2f>, <mean score %+.2f>, <mean success %+.1f>" % \
         (mean_reward[-1], mean_score[-1], mean_succ_p[-1],)
        print(group_stats, end='\n\n')
        results_info = results_info + group_stats + '\n\n'

    # Format visuals
    ax1.set_ylabel('rewards/H')
    ax1.legend(fontsize='x-small')
    ax1.yaxis.tick_right()
    # ax1.axes.xaxis.set_ticklabels([])
    if args.xlim:
        ax1.set_xlim(eval(args.xlim))


    ax2.set_ylabel('mean rewards/H')
    ax2.yaxis.tick_right()
    ax2.legend()
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_ylim(ax1.get_ylim())
    ax2.legend(fontsize='x-small')
    ax2.axes.xaxis.set_ticklabels([])

    ax3.set_ylabel('score/H')
    ax3.yaxis.tick_right()
    ax3.set_xlim(ax1.get_xlim())

    ax4.set_ylabel('mean score/H')
    ax4.yaxis.tick_right()
    ax4.set_xlim(ax1.get_xlim())
    ax4.set_ylim(ax3.get_ylim())
    ax4.legend(fontsize='x-small')

    ax5.set_ylabel('success')
    ax5.yaxis.tick_right()
    ax5.set_xlim(ax1.get_xlim())
    ax5.set_ylim([-5, 105])
    ax5.set_xlabel('#epochs')

    ax6.set_ylabel('mean success')
    ax6.legend(fontsize='x-small')
    ax6.set_xlim(ax1.get_xlim())
    ax6.set_ylim(ax5.get_ylim())
    ax6.yaxis.tick_right()
    ax6.set_xlabel('#epochs')

    ax7.set_xlabel('#samples')
    ax7.set_ylabel('rewards')
    ax7.yaxis.tick_right()

    ax8.set_xlabel('#epochs')
    ax8.set_ylabel(args.user)
    ax8.set_xlim(ax1.get_xlim())
    ax8.yaxis.tick_right()

    plt.tight_layout()
    plt.show()

    # add result info and save
    fig_text = plt.figure()
    font = FontProperties()
    font.set_family('monospace')
    fig_text.text(
        .5,
        .9,
        results_info,
        verticalalignment='top',
        horizontalalignment='center',
        fontproperties=font)
    with PdfPages(job['env_name'] + '.pdf') as pdf:
        pdf.savefig(fig)
        pdf.savefig(fig_text)
    plt.close()


if __name__ == '__main__':
    main()
