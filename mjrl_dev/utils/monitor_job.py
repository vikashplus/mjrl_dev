import time
import os
from vtils.plotting.srv import SRV
import numpy as np
from utils.viz_results import get_results, smooth_data

def sync_remote():
    print("syncing")
    os.system("sshpass -p handrobot rsync -av --include='best_policy.pickle' --include='agent_final.pickle' --exclude='*.pickle' --exclude='*.out' vikash@voltron.cs.washington.edu:~/Projects/darwin ~/Projects/")

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

# sync once
sync_remote()
res0 = get_results("/home/vik/Projects/darwin/walk/DNekoWalkRandom-v0-VJ8c_0/results.txt")
res1 = get_results("/home/vik/Projects/darwin/walk/DNekoWalkRandom-v0-VJ9a_0/results.txt")
plot = SRV(buff_sz=10000, legends=('height', 'no-height'), fig_name="DNekoWalkRandom-v0-VJ9a_0", markers=(None, None))
plot.update(key='height' ,x_data=res0['iter'], y_data=smooth_data(res0['reward']))
plot.update(key='no-height' ,x_data=res1['iter'], y_data=smooth_data(res1['reward']))

# start ploting

while True:
    # sync
    sync_remote()

    # update plot 
    res1 = get_results("/home/vik/Projects/darwin/walk/DNekoWalkRandom-v0-VJ9a_0/results.txt")
    plot.update(key='no-height' ,x_data=res1['iter'], y_data=smooth_data(res1['reward']))

    # wait
    time.sleep(60)