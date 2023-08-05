import gym
from gym import error, spaces, utils
from gym.utils import seeding

import os
import pybullet as p
import pybullet_data
import math
import numpy as np
import random

MAX_EPISODE_LEN = 5000
JOINTS=[0,1,4,5]
MAX_TORQUE=100
FORCE_ACTION={
#    0: 0,
#    1: 0,
#    2: 0,
#    3: 0,
}

def quaternion_multiply(quaternion1, quaternion0):
    w0, x0, y0, z0 = quaternion0
    w1, x1, y1, z1 = quaternion1
    return np.array([
      -x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0, x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0,
      -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0, x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0
    ], dtype=np.float64)

class NFEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    _max_episode_steps=MAX_EPISODE_LEN

    def __init__(self,show_gui=False,fall_rew=-1000.0,motion_rew=0,time_rew=0,height_rew=1.0,rand_force=None,mp4_path=None):
        self.step_counter = 0
        if show_gui:
            mode=p.GUI
        else:
            mode=p.DIRECT
        options=""
        if mp4_path:
            options+="--width=1024 --height=768 --mp4=\""+mp4_path+"\" --mp4fps=240"
        p.connect(mode, options=options)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.observation_space = spaces.Box(np.array([-1]*21), np.array([1]*21))
        self.action_space = spaces.Box(np.array([-1]*4), np.array([1]*4))
        self.prev_pos=None
        self.fall_rew=fall_rew
        self.motion_rew=motion_rew
        self.time_rew=time_rew
        self.height_rew=height_rew
        self.rand_force=rand_force

    def reset(self):
        self.step_counter = 0
        p.resetSimulation()
        p.setGravity(0,0,-10)
        self.plane_id = p.loadURDF("plane.urdf")
        #self.wall1_id = p.loadURDF("plane.urdf",[-0.7,0,0],p.getQuaternionFromEuler([0,math.pi/2,0]))
        #self.wall2_id = p.loadURDF("plane.urdf",[0.7,0,0],p.getQuaternionFromEuler([0,-math.pi/2,0]))
        cubeStartPos = [0,0,2]
        cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
        try:
            self.bot_id = p.loadURDF("/Users/dj/stuff/bot/urdf/bot11.urdf", cubeStartPos, cubeStartOrientation)
        except:
            self.bot_id = p.loadURDF("/content/drive/My Drive/bot/bot10.urdf", cubeStartPos, cubeStartOrientation)

        maxForce = 0
        mode = p.VELOCITY_CONTROL
        for i in range(8):
            p.setJointMotorControl2(self.bot_id, i, controlMode=mode, force=maxForce)

        c = p.createConstraint(self.bot_id, 1, self.bot_id, 2, jointType=p.JOINT_GEAR,jointAxis =[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=1, maxForce=10000)

        c = p.createConstraint(self.bot_id, 5, self.bot_id, 6, jointType=p.JOINT_GEAR,jointAxis =[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=1, maxForce=10000)

        res=p.getBasePositionAndOrientation(self.bot_id)
        pos=res[0]
        rot=p.getEulerFromQuaternion(res[1])

        obs=[]
        joint_states=[p.getJointState(self.bot_id, JOINTS[i]) for i in range(4)]
        for s in joint_states:
            obs.append(s[0]/math.pi) # pos
        for s in joint_states:
            obs.append(s[1]/math.pi) # vel
        for s in joint_states:
            obs.append(s[3]/MAX_TORQUE) # torque
        res=p.getBaseVelocity(self.bot_id)
        obs+=[rot[0]/math.pi,rot[1]/math.pi,rot[2]/math.pi] # orient (3)
        obs+=res[0] # lin vel (3)
        obs+=[res[1][0]/math.pi,res[1][1]/math.pi,res[1][2]/math.pi] # ang vel (3)
        self.observation = obs 

        if self.rand_force:
            r=random.uniform(-1,1)
            f=np.array(self.rand_force)*r
            p.applyExternalForce(self.bot_id,-1,f,[0,0,0],p.WORLD_FRAME)

        return np.array(self.observation).astype(np.float32)

    def step(self, action):
        mode = p.POSITION_CONTROL
        for i in range(4):
            a=action[i]
            if i in FORCE_ACTION:
                a=FORCE_ACTION[i]
            pos=a*math.pi
            joint_no=JOINTS[i]
            p.setJointMotorControl2(self.bot_id, joint_no, controlMode=mode, targetPosition=pos, force=MAX_TORQUE)

        p.stepSimulation()

        res=p.getBasePositionAndOrientation(self.bot_id)
        pos=res[0]
        #print("pos",pos)
        rot=p.getEulerFromQuaternion(res[1])
        #print("rot",rot)

        obs=[]
        joint_states=[p.getJointState(self.bot_id, JOINTS[i]) for i in range(4)]
        for s in joint_states:
            obs.append(s[0]/math.pi) # pos
        for s in joint_states:
            obs.append(s[1]/math.pi) # vel
        for s in joint_states:
            obs.append(s[3]/MAX_TORQUE) # torque
        res=p.getBaseVelocity(self.bot_id)
        obs+=[rot[0]/math.pi,rot[1]/math.pi,rot[2]/math.pi] # orient (3)
        obs+=res[0] # lin vel (3)
        obs+=[res[1][0]/math.pi,res[1][1]/math.pi,res[1][2]/math.pi] # ang vel (3)
        self.observation = obs 


        reward=0
        if self.prev_pos:
            reward+=(pos[1]-self.prev_pos[1])*self.motion_rew
        reward+=pos[2]*self.height_rew
        reward+=self.time_rew
        done = False

        if pos[2]<1.1:
            reward=self.fall_rew
            done=True
        
        if abs(rot[0])>=math.pi/4:
            reward=self.fall_rew
            done=True

        if abs(rot[1])>=math.pi/4:
            reward=self.fall_rew
            done=True

        self.step_counter += 1
        if not done and self.step_counter > MAX_EPISODE_LEN:
            reward = 0
            done = True

        info = {}

        self.prev_pos=pos
        return np.array(self.observation).astype(np.float32), reward, done, info

    def render(self):
        pass

    def _get_state(self):
        return self.observation

    def close(self):
        p.disconnect()
