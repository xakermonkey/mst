import cityflow
import random
import gym
import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard
import tensorflow.keras as K
import tensorflow.keras.layers as L
from rl.agents import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import BoltzmannQPolicy
from gym.spaces import Box, Discrete
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import Adam



class IntersectionGym(gym.Env):
    def __init__(self, config_path):

        self.action_space = Discrete(8)
        self.observation_space = Box(low=0, high=50, shape=(1, 24))
        self.state = np.array([0]*24)
        # self.game_length = 500
        self.eng = cityflow.Engine(config_path, thread_num=1)
        self.eng.set_save_replay(True)
        self.act = 0

    def step(self, action):
        self.eng.set_tl_phase('intersection_1_1', action)
        self.eng.next_step()
        arr = np.array(list(self.eng.get_lane_waiting_vehicle_count().values()))
        reward = 0
        if action != self.act:
            reward -= 1
        reward += self.eng.get_vehicle_count() - sum(arr)
            # print(arr)

        self.act = action
        self.state = arr

        if self.eng.get_current_time() < 1000:
            done = False
        else:
            done = True

        info = {}

        return self.state, reward, done, info


    def render(self, mode="human"):
        pass
    def reset(self):
        self.eng.reset(0)
        self.eng.set_save_replay(True)
        self.state = np.array([0]*24)
        return self.state


config_path = 'config.json'
env = IntersectionGym(config_path)

# episodes = 10
# for i in range(1, episodes+1):
#     state = env.reset()
#     done = False
#     score = 0
#
#     while not done:
#         action = env.action_space.sample()
#         n_state, reward, done, info = env.step(action)
#         score += reward
#     print(f"Episodes {i}: Score: {score}")


eng = cityflow.Engine(config_path, thread_num=1)





states = env.observation_space.shape
action = env.action_space.n



def build_model(states, actions):
    model = K.models.Sequential([
        L.Flatten(input_shape=states),
        L.Dense(24, activation='relu'),
        L.Dense(24, activation='relu'),
        L.Dense(actions, activation='softmax')
    ])
    return model


model = build_model(states, action)

model.summary()
# cb = TensorBoard(log_dir='log')

def build_agent(model,action):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=5000, window_length=1)
    dqn = DQNAgent(model=model, policy=policy, memory=memory, nb_actions=action, target_model_update=1e-2, nb_steps_warmup=10)
    return dqn


agent = build_agent(model, action)
agent.compile(Adam(1e-3), metrics=['mse'])



# while eng.get_current_time() < 500:
#     eng.next_step()
#     a = agent.predict((1,np.array(list(eng.get_lane_waiting_vehicle_count().values()))))
#     print(a)
#     eng.set_tl_phase('intersection_1_1')


agent.load_weights('model/agent_1_3.h5f')
# history = agent.fit(env, nb_steps=100000, visualize=False, verbose=1).history

# env.reset()
#
#
#
#
#
score = agent.test(env, nb_episodes=1, visualize=False)
#
# agent.save_weights('model/agent_1_3.h5f', overwrite=True)

