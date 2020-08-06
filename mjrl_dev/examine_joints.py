from utils.viz_paths import *
from vtils.plotting import simple_plot as sp
import pickle
import numpy as np

path_id = 0
paths_file_path = '/home/vik/Projects/darwin/walk/DNekoWalkRandom-v0-GJ5i_0/iterations/best_policy_paths.pickle'

paths = pickle.load(open(paths_file_path, 'rb'))

jnts = paths[path_id]['env_infos']['obs_dict']['dk_kitty_qpos']*180/np.pi
acts = paths[path_id]['env_infos']['last_ctrl']*180/np.pi
time = paths[path_id]['env_infos']['time']
# acts = paths[path_id]['actions']

hor, ndof = jnts.shape
for i in range(ndof):
    title = 'err: {:02.4f}'.format(np.linalg.norm(jnts[:,i]-acts[:,i]))
    sp.plot(xdata=time, ydata=jnts[:,i], legend='Hjnt'+str(i), subplot_id=(4, 3, i+1), fig_name='DOFs', marker='.')
    sp.plot(xdata=time, ydata=acts[:,i], legend='Hact'+str(i), subplot_id=(4, 3, i+1), fig_name='DOFs', marker='.', plot_name=title)


# paths_file_path = '/home/vik/Projects/darwin/walk/DNekoWalkRandom-v0-VJ3f_0/iterations/best_policy_paths.pickle'

# paths = pickle.load(open(paths_file_path, 'rb'))


# jnts = paths[path_id]['env_infos']['obs_dict']['dk_kitty_qpos']
# acts = paths[path_id]['env_infos']['a_applied']
# time = paths[path_id]['env_infos']['time']
# # acts = paths[path_id]['actions']
# hor, ndof = jnts.shape
# for i in range(ndof):
#     title = 'err: {:02.4f}'.format(np.linalg.norm(jnts[:,i]-acts[:,i]))
#     sp.plot(xdata=time, ydata=jnts[:,i], legend='Sjnt'+str(i), subplot_id=(4, 3, i+1), fig_name='DOFs', marker='.')
#     sp.plot(xdata=time, ydata=acts[:,i], legend='Sact'+str(i), subplot_id=(4, 3, i+1), fig_name='DOFs', marker='.', plot_name=title)


# sp.save_plot(name=paths_file_path[:-7]+'_jnts(sim+hwr).pdf')
sp.show_plot()


# plot_paths(paths, fileName_prefix='test_joints_')