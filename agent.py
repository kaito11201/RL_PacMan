import copy
import numpy as np

class Agent:
    def __init__(self, alpha, gamma, k, actions, pos, dot_size, observation):
        
        # 学習系の変数
        self.alpha = alpha
        self.gamma = gamma
        self.k = k
        self.compute_epsilon(0)
        
        # 行動系の変数
        self.actions = actions
        self.vector = None
        
        # 座標系の変数
        self.pos = pos
        self.ini_pos = pos
        self.dot_pos = (pos[0] * dot_size, pos[1] * dot_size)
        self.ini_dot_pos = self.dot_pos
        
        # 状態系の変数
        self.state = observation
        self.ini_state = observation
        self.previous_state = None
        self.previous_action = None
        
        # Q値を表すQテーブル
        self.q_table = self._create_q_table()
    
    def _create_q_table(self):
        # Qテーブルを作る関数
        
        q_table = {}
        q_table[self.state] = np.repeat(0.0, len(self.actions))
        return q_table
    
    def act(self):
        # 行動を選択する関数(ε-greedy法)
        
        # ランダムで行動を選択
        if np.random.uniform() < self.epsilon:
            action = np.random.randint(0, len(self.q_table[self.state]))
            
        # Q値が最も高い行動を選択
        else:
            action = np.argmax(self.q_table[self.state])
            
        self.previous_action = action
        return action
    
    def observe(self, next_state, reward):
        # 次の状態への移行と報酬の観測を行う関数
        
        # 新しい状態の場合、Qテーブルに追加
        if next_state not in self.q_table:
            self.q_table[next_state] = np.repeat(0.0, len(self.actions))
        
        # 前の状態を今の状態に更新
        self.previous_state = copy.deepcopy(self.state)
        
        # 次の状態を今の状態に更新
        self.state = next_state
        
        # 状態と報酬から学習
        self._learn(reward)

    def _learn(self, reward):
        # Q値の更新を行う関数(学習する関数)
        
        # Q(s, a)
        q = self.q_table[self.previous_state][self.previous_action]
        
        # max Q(s')
        max_q = max(self.q_table[self.state])
        
        # Q(s, a) = Q(s, a) + alpha*(r+gamma*maxQ(s')-Q(s, a))
        self.q_table[self.previous_state][self.previous_action] = q + (self.alpha * (reward + (self.gamma * max_q) - q))
    
    def compute_epsilon(self, episode):
        # 探索率を計算する関数
        self.epsilon = 1 / (self.k * episode + 1)
    
    def set_pos(self, pos):
        # リスト上での座標を渡す関数
        self.pos = pos
            
    def set_dot_pos(self, pos):
        # ドット上での座標を渡す関数
        self.dot_pos = pos
    
    def get_dot_pos(self):
        # ドット上での座標を取得する関数
        return self.dot_pos
    
    def set_vector(self, vector):
        # 向いている方向を渡す関数
        self.vector = vector
    
    def get_vector(self):
        # 向いている方向を取得する関数
        return self.vector
    
    def get_state(self):
        # 状態を取得する関数
        return self.state
    
    def reset(self):
        # 座標と状態をリセットする関数
        
        self.pos = self.ini_pos
        self.dot_pos = self.ini_dot_pos
        self.previous_state = copy.deepcopy(self.ini_state)
        self.state = copy.deepcopy(self.ini_state)