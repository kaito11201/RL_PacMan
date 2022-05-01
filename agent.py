import copy
from msvcrt import kbhit
import numpy as np

class Agent:
    def __init__(
            self,
            alpha=.2,
            gamma=.99,
            k = .999,
            actions=None,
            pos=None,
            observation=None,
            dot_size=None):
        
        self.alpha = alpha
        self.gamma = gamma
        self.k = k
        self.epsilon = None
        self.compute_epsilon(0)
        self.reward_history = []
        self.actions = actions
        self.vector = None
        
        self.pos = pos
        self.ini_pos = self.pos
        self.dot_pos = pos[0] * dot_size, pos[1] * dot_size
        self.ini_dot_pos = self.dot_pos
        
        self.state = observation
        self.ini_state = observation
        self.previous_state = None
        self.previous_action = None
        self.q_table = self._create_q_table()
    
    def _create_q_table(self):
        # Qテーブルを作る関数
        q_table = {}
        
        q_table[self.state] = np.repeat(0.0, len(self.actions))
        return q_table
    
    def _init_state(self):
        # エージェントの状態を初期化する関数
        self.previous_state = copy.deepcopy(self.ini_state)
        self.state = copy.deepcopy(self.ini_state)
        return self.state
    
    def act(self):
        # ε-greedy選択で行動をする関数
        
        # random行動
        if np.random.uniform() < self.epsilon:
            action = np.random.randint(0, len(self.q_table[self.state]))
            
        # greedy 行動
        else:
            action = np.argmax(self.q_table[self.state])
        
        self.vector = action
        self.previous_action = action
        return action
    
    def observe(self, next_state, reward=None):
        # 次の状態への移行と報酬の観測を行う関数
        
        next_state = next_state
        if next_state not in self.q_table:  # 始めて訪れる状態であれば
            self.q_table[next_state] = np.repeat(0.0, len(self.actions))

        self.previous_state = copy.deepcopy(self.state)
        self.state = next_state

        if reward is not None:
            self.reward_history.append(reward)
            self.learn(reward)

    def learn(self, reward):
        # Q値の更新を行う関数
        
        # Q(s, a)
        q = self.q_table[self.previous_state][self.previous_action]
        # max Q(s')
        max_q = max(self.q_table[self.state])
        # Q(s, a) = Q(s, a) + alpha*(r+gamma*maxQ(s')-Q(s, a))
        self.q_table[self.previous_state][self.previous_action] = q + \
            (self.alpha * (reward + (self.gamma * max_q) - q))
    
    def set_pos(self, pos):
        self.pos = pos
            
    def set_dot_pos(self, pos):
        self.dot_pos = pos
    
    def get_dot_pos(self):
        return self.dot_pos
    
    def get_vector(self):
        return self.vector
    
    def set_vector(self, vector):
        self.vector = vector
    
    def get_state(self):
        return self.state
    
    def reset(self):
        self.pos = self.ini_pos
        self.dot_pos = self.ini_dot_pos
        self._init_state()
    
    def compute_epsilon(self, episode):
        self.epsilon = 1 / (self.k * episode + 1)