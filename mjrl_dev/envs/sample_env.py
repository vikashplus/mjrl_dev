import numpy as np
from gym import utils
from mjrl.envs import mujoco_env
from mujoco_py import MjViewer
import os
from darwin.darwin_utils.obs_vec_dict import ObsVecDict
import collections

OBS_KEYS = [ ]
RWD_KEYS = [ ]
REW_MODE = 'rwd_dense' # rwd_dense/ rwd_sparse

class SampleEnvV0(mujoco_env.MujocoEnv, utils.EzPickle, ObsVecDict):
    def __init__(self):

        # get sim
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        sim = mujoco_env.get_sim(model_path=curr_dir+'/assets/DAPG_door.xml')
        # ids
        self.obj_sid = sim.model.site_name2id('obj')
        self.jnt_did = sim.model.jnt_dofadr[sim.model.joint_name2id('door_hinge')]
        self.prt_bid = sim.model.body_name2id('part')
        # scales
        self.act_mid = np.mean(sim.model.actuator_ctrlrange, axis=1)
        self.act_rng = 0.5*(sim.model.actuator_ctrlrange[:,1]-sim.model.actuator_ctrlrange[:,0])

        # get env
        utils.EzPickle.__init__(self)
        ObsVecDict.__init__(self)
        self.obs_dict = {}
        self.rwd_dict = {}
        mujoco_env.MujocoEnv.__init__(self, sim=sim, frame_skip=5)

    # step the simulation forward
    def step(self, a):
        a = np.clip(a, -1.0, 1.0)
        try:
            a = self.act_mid + a*self.act_rng # mean center and scale
        except:
            a = a                             # only for the initialization phase
        self.do_simulation(a, self.frame_skip)
        
        # observation and rewards
        obs = self.get_obs()
        self.expand_dims(self.obs_dict) # required for vectorized rewards calculations
        self.rwd_dict = self.get_reward_dict(self.obs_dict)
        self.squeeze_dims(self.rwd_dict)
        self.squeeze_dims(self.obs_dict)

        # finalize step
        env_info = self.get_env_infos()
        return obs, env_info[REW_MODE], bool(env_info['done']), env_info

    def get_obs(self):
        self.obs_dict['t'] = np.array([self.sim.data.time])
        self.obs_dict['err'] = self.data.qpos[:-2].copy()

        obs = self.obsdict2obsvec(self.obs_dict, OBS_KEYS)
        return obs

    def get_reward_dict(self, obs_dict):
        reach_dist = np.linalg.norm(obs_dict['palm_pos']-obs_dict['handle_pos'], axis=-1)
        door_pos = obs_dict['door_pos'][:,:,0]
        
        rwd_dict = collections.OrderedDict((
            # Optional Keys
            ('reach', -0.1* reach_dist),
            ('open', -0.1*(door_pos - 1.57)*(door_pos - 1.57)),
            ('bonus', 2*(door_pos > 0.2) + 8*(door_pos > 1.0) + 10*(door_pos > 1.35)),
            # Must keys
            ('sparse',  door_pos),
            ('solved',  door_pos > 1.35),
            ('done',    reach_dist > 5.0),
        ))
        rwd_dict['dense'] = np.sum([rwd_dict[key] for key in RWD_KEYS], axis=0)
        return rwd_dict
    
    # use latest obs, rwds to get all info (be careful, information belongs to different timestamps)
    # Its getting called twice. Once in step and sampler calls it as well
    def get_env_infos(self):
        env_info = {
            'time': self.obs_dict['t'][()],
            'rwd_dense': self.rwd_dict['dense'][()],
            'rwd_sparse': self.rwd_dict['sparse'][()],
            'solved': self.rwd_dict['solved'][()],
            'done': self.rwd_dict['done'][()],
            'obs_dict': self.obs_dict,
            'rwd_dict': self.rwd_dict,
        }
        return env_info

    # compute vectorized rewards for paths
    def compute_path_rewards(self, paths):
        # path has two keys: observations and actions
        # path["observations"] : (num_traj, horizon, obs_dim)
        # path["rewards"] should have shape (num_traj, horizon)
        obs_dict = self.obsvec2obsdict(paths["observations"])
        rwd_dict = self.get_reward_dict(obs_dict)

        rewards = reward_dict['dense']
        done = reward_dict['done']
        # time align rewards. last step is redundant
        done[...,:-1] = done[...,1:]
        rewards[...,:-1] = rewards[...,1:] 
        paths["done"] = done if done.shape[0] > 1 else done.ravel()
        paths["rewards"] = rewards if rewards.shape[0] > 1 else rewards.ravel()
        return paths

    # truncate paths as per done condition
    def truncate_paths(self, paths):
        hor = paths[0]['rewards'].shape[0]
        for path in paths:
            if path['done'][-1] == False:
                path['terminated'] = False
                terminated_idx = hor
            elif path['done'][0] == False:
                terminated_idx = sum(~path['done'])+1
                for key in path.keys():
                    path[key] = path[key][:terminated_idx+1, ...]
                path['terminated'] = True
        return paths

    def reset_model(self):
        qp = self.init_qpos.copy()
        qv = self.init_qvel.copy()
        self.set_state(qp, qv)

        self.model.body_pos[self.door_bid,0] = self.np_random.uniform(low=-0.3, high=-0.2)
        self.model.body_pos[self.door_bid, 1] = self.np_random.uniform(low=0.25, high=0.35)
        self.model.body_pos[self.door_bid,2] = self.np_random.uniform(low=0.252, high=0.35)
        self.sim.forward()
        return self.get_obs()

    def get_env_state(self):
        """
        Get state of hand as well as objects and targets in the scene
        """
        qp = self.data.qpos.ravel().copy()
        qv = self.data.qvel.ravel().copy()
        door_body_pos = self.model.body_pos[self.door_bid].ravel().copy()
        return dict(qpos=qp, qvel=qv, door_body_pos=door_body_pos)

    def set_env_state(self, state_dict):
        """
        Set the state which includes hand as well as objects and targets in the scene
        """
        qp = state_dict['qpos']
        qv = state_dict['qvel']
        self.set_state(qp, qv)
        self.model.body_pos[self.door_bid] = state_dict['door_body_pos']
        self.sim.forward()

    # def get_env_infos(self):
    #     state = self.get_env_state()
    #     door_pos = self.data.qpos[self.door_hinge_did]
    #     goal_achieved = True if door_pos >= 1.35 else False
    #     return dict(state=state, goal_achieved=goal_achieved)

    def mj_viewer_setup(self):
        self.viewer = MjViewer(self.sim)
        self.viewer.cam.azimuth = 90
        self.sim.forward()
        self.viewer.cam.distance = 1.5

    # evaluate paths and log metrics to logger
    def evaluate_success(self, paths, logger=None):
        num_success = 0
        num_paths = len(paths)
        horizon = self.spec.max_episode_steps # paths could have early termination
        # success if door open for 25 steps
        for path in paths:
            if np.sum(path['env_infos']['solved']) > 5:
                num_success += 1
        success_percentage = num_success*100.0/num_paths

        # log stats
        if logger:
            rwd_sparse = np.mean([np.mean(p['env_infos']['rwd_sparse']) for p in paths]) # return rwd/step
            rwd_dense = np.mean([np.sum(p['env_infos']['rwd_sparse'])/horizon for p in paths]) # return rwd/step
            logger.log_kv('rwd_sparse', rwd_sparse)
            logger.log_kv('rwd_dense', rwd_dense)
            logger.log_kv('score', score)
            logger.log_kv('success_rate', success_percentage)

        return success_percentage
