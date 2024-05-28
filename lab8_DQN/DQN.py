# requirements
# - Python >= 3.7
# - torch >= 1.7
# - gym == 0.23
# - (Optional) tensorboard, wandb

import gym
import argparse
import numpy as np
import torch
import torch.nn.functional as F
from torch import nn, optim


class QNet(nn.Module):
    '''
        this is a simple Q network with one hidden layer
        input: state
        output: Q value for each action
    '''
    def __init__(self, input_size, hidden_size, output_size):
        super(QNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        # TODO write another linear layer here with 
        self.fc2 = nn.Linear(hidden_size, hidden_size) # another layer
        self.fc3 = nn.Linear(hidden_size, output_size)


    def forward(self, x):
        x = torch.Tensor(x)
        x = F.relu(self.fc1(x))
        # TODO calculate output with another layer
        x = F.relu(self.fc2(x)) 
        x = self.fc3(x)#no activation function for the output layer
        return x

import random
from collections import deque
class ReplayBuffer:
    """
    A simple FIFO experience replay buffer for DQN agents.
    """
    def __init__(self, capacity):
        # TODO Define buffer with given capacity
        self.buffer = deque(maxlen = capacity) # capacity of the buffer

    def len(self):
        # TODO Return the size of buffer
        return self.buffer.__len__()

    def push(self, *transition):
        # TODO Add transition to buffer, input is a tuple
        self.buffer.append(transition)
        ...

    def sample(self, batch_size):
        # TODO Sample transitions from buffer
        # return a tuple of lists
        # (state, actions, rewards, next_state)
        transitions = random.sample(self.buffer, batch_size)
        return zip(*transitions)
    
    def clean(self):
        # TODO Clean buffer
        self.buffer.clear()
        ...


class DQN:
    def __init__(self, env, input_size, hidden_size, output_size):
        self.env = env
        # network for evaluate
        self.eval_net = QNet(input_size, hidden_size, output_size)
        # target network
        self.target_net = QNet(input_size, hidden_size, output_size)
        self.optim = optim.Adam(self.eval_net.parameters(), lr=args.lr)
        self.eps = args.eps
        self.buffer = ReplayBuffer(args.capacity)
        self.loss_fn = nn.MSELoss()
        self.learn_step = 0
    
    def choose_action(self, obs):
        # TODO Return an action 
        #according to the given observation "obs"
        #with ε-greedy policy, epision probability to choose random action
        #otherwise choose the action with the highest Q value
        if np.random.rand() < self.eps:
            return self.env.action_space.sample()
        else:
            obs = torch.Tensor(obs)
            Q = self.eval_net(obs)
            return torch.argmax(Q).item() 
        ...

    def store_transition(self, *transition):
        self.buffer.push(*transition)
        
    def learn(self):
        # [Epsilon Decay]
        # if self.eps > args.eps_min:
        #     self.eps *= args.eps_decay

        # [Update Target Network Periodically]
        if self.learn_step % args.update_target == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_step += 1
        
        # [Sample Data From Experience Replay Buffer]
        obs, actions, rewards, next_obs, dones = self.buffer.sample(args.batch_size)
        actions = torch.LongTensor(actions)  # to use 'gather' latter
        dones = torch.FloatTensor(dones)
        rewards = torch.FloatTensor(rewards)

        # TODO [Calculate and Perform Gradient Descend]
        # For example:
        # 1. calculate q_eval with eval_net and q_target with target_net
        # 2. td_target = r + gamma * (1-dones) * q_target
        # 3. calculate loss between "q_eval" and "td_target" with loss_fn
        # 4. optimize the network with self.optim
        obs = torch.FloatTensor(obs)
        next_obs = torch.FloatTensor(next_obs)
        q_eval = self.eval_net(obs).gather(1, actions.unsqueeze(1)).squeeze(1)
        q_next = self.target_net(next_obs).detach()
        q_target = rewards + args.gamma * (1-dones) * q_next.max(1)[0]
        loss = self.loss_fn(q_eval, q_target)
        self.optim.zero_grad()
        loss.backward()
        self.optim.step()
        ...

import matplotlib.pyplot as plt
def main():
    env = gym.make(args.env) #start the environment
    o_dim = env.observation_space.shape[0]
    a_dim = env.action_space.n
    agent = DQN(env, o_dim, args.hidden, a_dim)                         # 初始化DQN智能体
    max_reward = 0
    reward_list = []
    epoch_list = []
    for i_episode in range(args.n_episodes):                            # 开始玩游戏
        obs = env.reset()                                               # 重置环境
        episode_reward = 0                                              # 用于记录整局游戏能获得的reward总和
        done = False
        step_cnt=0
        while not done and step_cnt<500:
            step_cnt+=1
            env.render()                                                # 渲染当前环境(仅用于可视化)
            action = agent.choose_action(obs)                           # 根据当前观测选择动作
            next_obs, reward, done, info = env.step(action)             # 与环境交互
            agent.store_transition(obs, action, reward, next_obs, done) # 存储转移
            episode_reward += reward                                    # 记录当前动作获得的reward
            obs = next_obs
            if agent.buffer.len() >= args.capacity:                     #if buffer is full, start learning
                agent.learn()                                           # 学习以及优化网络
        reward_list.append(episode_reward)
        if episode_reward > max_reward:
                max_reward = episode_reward
                # print(f"Episode: {i_episode}, Reward: {episode_reward}")
        print(f"Episode: {i_episode}, Reward: {episode_reward}")
    epoch_list = list(range(args.n_episodes))
    plt.plot(epoch_list, reward_list)
    plt.xlabel('Epoch')
    plt.ylabel('Reward')
    plt.title('Reward Curve')
    print(f"Max Reward: {max_reward}")
    plt.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--env",        default="CartPole-v1",  type=str,   help="environment name")
    parser.add_argument("--lr",             default=1e-3,       type=float, help="learning rate")
    parser.add_argument("--hidden",         default=64,         type=int,   help="dimension of hidden layer")
    parser.add_argument("--n_episodes",     default=500,        type=int,   help="number of episodes")
    parser.add_argument("--gamma",          default=0.99,       type=float, help="discount factor")
    # parser.add_argument("--log_freq",       default=100,        type=int)
    parser.add_argument("--capacity",       default=10000,      type=int,   help="capacity of replay buffer")
    parser.add_argument("--eps",            default=0.1,        type=float, help="epsilon of ε-greedy")
    # parser.add_argument("--eps_min",        default=0.05,       type=float)
    parser.add_argument("--batch_size",     default=128,        type=int)
    # parser.add_argument("--eps_decay",      default=0.999,      type=float)
    parser.add_argument("--update_target",  default=100,        type=int,   help="frequency to update target network")
    args = parser.parse_args()
    main()