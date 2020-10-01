import time
import os
from vtils.plotting.srv import SRV
# import numpy as np
import glob
import argparse
import pandas
from scipy import signal

def sync_remote(remote, path):
    ind = path.rfind('/')
    path_root = path[:ind+1] if ind>-1 else ''
    os.system("sshpass -p handrobot rsync -av --include=\"*/\" --include='*.csv' --include='job_data.*' --exclude='*' vikash@{}.cs.washington.edu:~/Projects/{} ~/Projects/{}".format(remote, path, path_root))

def search_files(search_path, file_name, filter):
    return glob.glob("{}/*{}*/**/{}".format(search_path, filter, file_name))


def get_data(filename, key):
    try:
        data = pandas.read_csv(filename)
    except Exception as e:
        print("WARNING: %s not found." % filename)
        quit()

    it = data['iteration'] if 'iteration' in data.keys() else range(len(data))
    return it, data[key]

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
        '-s', '--source', type=str, required=True, help='Remote log location')
    parser.add_argument(
        '-p', '--path', type=str, default="mjrl", help='Path to sync')
    parser.add_argument(
        '-f', '--filter', type=str, required=True, help='filter logs')
    parser.add_argument(
        '-k', '--key', type=str, default='eval_score', help='log key to plot')
    parser.add_argument(
        '-w', '--wait', type=int, default=60, help='seconds to wait before refresh')
    args = parser.parse_args()

    init = True
    while True:
        print("syncing remote", end=">> ")
        sync_remote(remote=args.source, path=args.path)
        log_names = search_files(search_path="/home/vik/Projects/"+args.path, file_name="log.csv", filter=args.filter)

        print(log_names)
        if init:
            plot = SRV(buff_sz=10000, legends=tuple(log_names), fig_name="Monitor Remote", markers=None)
            init = False

        print("Reading logs", end=">> ")
        for log_name in log_names:
            log_xdata, log_ydata  = get_data(filename=log_name, key=args.key)
            plot.update(key=log_name, x_data=log_xdata, y_data=smooth_data(log_ydata))
        print("Plots updated")

        time.sleep(args.wait)

if __name__ == '__main__':
    main()



# def get_results(filename):
#     results = []

#     try:
#         data = np.loadtxt(filename, skiprows=1)
#         results = {
#             'iter': data[:, 0],
#             'reward': data[:, 1],
#             'episode': data[:, -1]
#         }
#     except Exception as e:
#         print("WARNING: %s not found." % filename)
#     return results


# # sync once

# sync_remote("bundle", "mbrl")
# search_files(search_path="~/Projects")
# plot = SRV(buff_sz=10000, legends=('height', 'no-height'), fig_name="Monitor Remote", markers=(None, None))
# plot.update(key='height' ,x_data=res0['iter'], y_data=smooth_data(res0['reward']))
# plot.update(key='no-height' ,x_data=res1['iter'], y_data=smooth_data(res1['reward']))

# # start ploting
# while True:
#     # sync
#     sync_remote()

#     # update plot 
#     res1 = get_results("/home/vik/Projects/darwin/walk/DNekoWalkRandom-v0-VJ9a_0/results.txt")
#     plot.update(key='no-height' ,x_data=res1['iter'], y_data=smooth_data(res1['reward']))

#     # wait
#     time.sleep(60)