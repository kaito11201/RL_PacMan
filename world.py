from itertools import count
import numpy as np
import copy

class World:
    def __init__(self, width, height, objects, actions, rewards):
        self.objects = objects
        self.actions = actions
        self.ini_map = self.create_map(width, height)
        self.map = copy.deepcopy(self.ini_map)
        self.dot_n = self._count_dot()
        self.rewards = rewards
        
        self._count_dot()
        
    def create_map(self, width, height):
        # 初期状態のマップを作成する関数
        
        map = np.ones(width * height).reshape((height, width))
        
        # 周囲に壁を配置
        map[0, :] = self.objects['wall']
        map[height-1, :] = self.objects['wall']
        map[:, 0] = self.objects['wall']
        map[:, width-1] = self.objects['wall']
        
        return map
        
    def step(self, x, y, action, state):
        
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
        
        if self._is_wall(to_x, to_y):
            return (x, y), state, self.rewards['wall'], True, False
        
        agent_state = self.get_state(to_x, to_y)
        reward = self._get_reward(to_x, to_y)
        is_completed = self._is_completed()
        
        return (to_x, to_y), agent_state, reward, False, is_completed
        
    def _count_dot(self):
        # マップにあるドットの数を数える関数
        # 戻り値: <class 'int'>
        return np.count_nonzero(self.map == self.objects['dot'])
    
    def get_map(self):
        # マップを渡す関数
        return self.map
    
    def set_map(self, map):
        # マップを取得する関数
        self.map = map
    
    def get_state(self, x, y, scope=1):
        # agentの視界を渡す関数
        view = []
        
        for h in range(-scope, scope + 1):
            for w in range(-scope, scope + 1):
                try:
                    view.append(self.map[y+h, x+w])
                except:
                    print(x, y, y+h, x+w)
                
        return tuple(view)
        
    def _is_wall(self, x, y):
        
        if self.map[y, x] == self.objects['wall']:
            return True
        else:
            return False
    
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

    def reset(self):
        self.map = copy.deepcopy(self.ini_map)
    
    def to_none(self, x, y):
        self.map[y, x] = self.objects['none']
    
    def to_agent(self, x, y):
        self.map[y, x] = self.objects['agent']