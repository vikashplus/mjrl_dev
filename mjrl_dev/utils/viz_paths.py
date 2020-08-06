
import numpy as np

# Useful to check the horizon for teleOp / Hardware experiments
def plot_horizon_distribution(paths, e, fileName_prefix=None):
    import matplotlib as mpl
    mpl.use('TkAgg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 5})

    if "time" in paths[0]['env_infos']:
        horizon = np.zeros(len(paths))

        # plot timesteps
        plt.clf()

        rl_dt_ideal = e.env.env.frame_skip * e.env.env.model.opt.timestep
        for i, path in enumerate(paths):
            dt = path['env_infos']['time'][1:] - path['env_infos']['time'][:-1]
            horizon[i] = path['env_infos']['time'][-1] - path['env_infos'][
                'time'][0]
            h1 = plt.plot(
                path['env_infos']['time'][1:],
                dt,
                '-',
                label=('time=%1.2f' % horizon[i]))
        h1 = plt.plot(
            np.array([0, max(horizon)]),
            rl_dt_ideal * np.ones(2),
            'g', alpha=.5,
            linewidth=2.0)

        plt.legend([h1[0]], ['ideal'], loc='upper right')
        plt.ylabel('time step (sec)')
        plt.xlabel('time (sec)')
        plt.ylim(rl_dt_ideal - 0.005, rl_dt_ideal + .005)
        plt.suptitle('Timestep profile for %d rollouts' % len(paths))

        file_name = fileName_prefix + '_timesteps.pdf'
        plt.savefig(file_name)
        print("Saved:", file_name)

        # plot horizon
        plt.clf()
        h1 = plt.plot(
            np.array([0, len(paths)]),
            e.horizon * rl_dt_ideal * np.ones(2),
            'g',
            linewidth=5.0,
            label='ideal')
        plt.bar(np.arange(0, len(paths)), horizon, label='observed')
        plt.ylabel('rollout duration (sec)')
        plt.xlabel('rollout id')
        plt.legend()
        plt.suptitle('Horizon distribution for %d rollouts' % len(paths))

        file_name = fileName_prefix + '_horizon.pdf'
        plt.savefig(file_name)
        print("Saved:", file_name)


def plot_paths(paths, e=None, fileName_prefix=''):
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 5})

    for i, path in enumerate(paths):
        plt.clf()

        # observations
        nplt1 = len(path['env_infos']['obs_dict'])
        for iplt1, key in enumerate(
                sorted(path['env_infos']['obs_dict'].keys())):
            ax = plt.subplot(nplt1, 2, iplt1 * 2 + 1)
            if iplt1 != (nplt1 - 1):
                ax.axes.xaxis.set_ticklabels([])
            if iplt1 == 0:
                plt.title('Observations')
            ax.yaxis.tick_right()
            plt.plot(
                path['env_infos']['time'],
                path['env_infos']['obs_dict'][key],
                label=key)
            # plt.ylabel(key)
            plt.text(0.01, .01, key, transform=ax.transAxes)
        plt.xlabel('time (sec)')

        # actions
        nplt2 = 3
        ax = plt.subplot(nplt2, 2, 2)
        ax.set_prop_cycle(None)
        # h4 = plt.plot(path['env_infos']['time'], e.env.env.act_mid + path['actions']*e.env.env.act_rng, '-', label='act') # plot scaled actions
        h4 = plt.plot(
            path['env_infos']['time'], path['actions'], '-',
            label='act')  # plot normalized actions
        plt.ylabel('actions')
        ax.axes.xaxis.set_ticklabels([])
        ax.yaxis.tick_right()

        # rewards/ scores
        if "score" in path['env_infos']:
            ax = plt.subplot(nplt2, 2, 6)
            plt.plot(
                path['env_infos']['time'],
                path['env_infos']['score'],
                label='score')
            plt.xlabel('time')
            plt.ylabel('score')
            ax.yaxis.tick_right()

        if "rwd_dict" in path['env_infos']:
            ax = plt.subplot(nplt2, 2, 4)
            ax.set_prop_cycle(None)
            for key in sorted(path['env_infos']['rwd_dict'].keys()):
                plt.plot(
                    path['env_infos']['time'],
                    path['env_infos']['rwd_dict'][key],
                    label=key)
            plt.legend(
                loc='upper left',
                fontsize='x-small',
                bbox_to_anchor=(.75, 0.25),
                borderaxespad=0.)
            ax.axes.xaxis.set_ticklabels([])
            plt.ylabel('rewards')
            ax.yaxis.tick_right()

        file_name = fileName_prefix + '_sample' + str(i) + '.pdf'
        plt.savefig(file_name)
        print("saved ", file_name)