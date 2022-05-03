from itertools import count
import numpy as np
import copy

class World:
    def __init__(self, width, height, objects, actions, rewards, scope):
        self.objects = objects
        self.actions = actions
        self.rewards = rewards
        self.scope = scope
        
        # 二次元リストのマップ
        self.ini_map = self._create_map(width, height)
        self.map = copy.deepcopy(self.ini_map)
        
        # マップ上にあるドットの数
        self.dot_n = self._count_dot()
        
    def step(self, x, y, action, state):
        # 行動を実行する関数
        
        to_x, to_y = x, y
        
        # 行動に従って座標を更新
        if action == self.actions['up']:
            to_y -= 1
        elif action == self.actions['down']:
            to_y += 1
        elif action == self.actions['left']:
            to_x -= 1
        elif action == self.actions['right']:
            to_x += 1
        
        # 移動先が壁か判定
        if self._is_wall(to_x, to_y):
            return (x, y), state, self.rewards['wall'], True, False
        
        # 移動先の状態と報酬を取得
        agent_state = self.get_state(to_x, to_y)
        reward = self._get_reward(to_x, to_y)
        
        # マップにあるドットをすべて回収したか判定
        is_completed = self._is_completed()
        
        return (to_x, to_y), agent_state, reward, False, is_completed
    
    def _is_wall(self, x, y):
        # 受け取った座標に壁があるか判定する関数
        
        if self.map[y, x] == self.objects['wall']:
            return True
        else:
            return False
    
    def get_state(self, x, y):
        # agentの状態を渡す関数
        
        state = []
        
        # エージェントの視界
        view = []
        for h in range(-self.scope, self.scope + 1):
            for w in range(-self.scope, self.scope + 1):
                view.append(self.map[y+h, x+w])
        view = tuple(view)
        
        # 各情報を追加
        state.append(view)
        
        return tuple(state)
    
    def _get_reward(self, x, y):
        # 報酬を渡す関数
        return self.rewards[self.objects[self.map[y, x]]]
    
    def _is_completed(self):
        # ドットを全て回収できたか確認する関数
        
        dot_n = self._count_dot()
        
        if dot_n == 0:
            return True
        else:
            return False
    
    def _count_dot(self):
        # マップにあるドットの数を数える関数
        return np.count_nonzero(self.map == self.objects['dot'])
    
    def _create_map(self, width, height):
        # 初期状態のマップを作成する関数
        
        map = np.ones(width * height).reshape((height, width))
        
        # 周囲に壁を配置
        map[0, :] = self.objects['wall']
        map[height-1, :] = self.objects['wall']
        map[:, 0] = self.objects['wall']
        map[:, width-1] = self.objects['wall']
        
        return map
    
    def get_map(self):
        # マップを渡す関数
        return self.map
    
    def to_none(self, x, y):
        # 受け取った座標上にあるオブジェクトを何もない状態にする関数
        self.map[y, x] = self.objects['none']
    
    def to_agent(self, x, y):
        # 受け取った座標上にあるオブジェクトをエージェントに更新する関数
        self.map[y, x] = self.objects['agent']
    
    def reset(self):
        # マップを初期状態にする関数
        self.map = copy.deepcopy(self.ini_map)