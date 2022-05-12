from itertools import count
import numpy as np
import copy

class World:
    # マップ（二次元リスト）を管理するクラス
    
    def __init__(self, width, height, objects, actions,
                 rewards, recognition_dict, recognition,
                 scope, agents_pos, enemies_pos):
        self.width = width
        self.height = height
        self.objects = objects
        self.actions = actions
        self.rewards = rewards
        self.recognition_dict = recognition_dict
        self.recognition = recognition
        self.scope = scope
        self.agents_pos = agents_pos
        self.ini_agents_pos = agents_pos
        self.enemies_pos = enemies_pos
        self.ini_enemies_pos = enemies_pos
        
        # 二次元リストのマップ
        self.ini_map = self._create_map(width, height)
        self.map = copy.deepcopy(self.ini_map)
        
        # マップ上にあるドットの数
        self.dot_n = self._count_dot()
    
    def _create_map(self, width, height):
        # 初期状態のマップを作成する関数
        
        map = np.ones(width * height).reshape((height, width))
        
        # 周囲に壁を配置
        map[0, :] = self.objects['wall']
        map[height-1, :] = self.objects['wall']
        map[:, 0] = self.objects['wall']
        map[:, width-1] = self.objects['wall']
        return map
    
    def step(self, x, y, action):
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
            return x, y, True
        else:
            return to_x, to_y, False
    
    def _is_wall(self, x, y):
        # 受け取った座標に壁があるか判定する関数
        
        if self.map[y, x] == self.objects['wall']:
            return True
        else:
            return False
    
    def get_state(self, x, y):
        # エージェントの状態を渡す関数
        
        state = []
        
        # エージェントの視界
        if self.recognition_dict['view'] in self.recognition:
            view = []
            for h in range(-self.scope, self.scope + 1):
                for w in range(-self.scope, self.scope + 1):
                    
                    if self._is_within_range(x+w, y+h):
                        
                        moving_object = self._exist_moving_object(x+w, y+h)
                        
                        if moving_object:
                            view.append(moving_object)
                        else:
                            view.append(self.map[y+h, x+w])
                            
                    else:
                        view.append(None)
                        
            view = tuple(view)
            state.append(view)
        
        # マップに残っているドットの数
        if self.recognition_dict['remain_dots'] in self.recognition:
            dot_n = self._count_dot()
            state.append(dot_n)
            
        # 他エージェントの位置
        if self.recognition_dict['agents_pos'] in self.recognition:
            state.append(tuple(self.agents_pos))
        
        # 敵の位置
        if self.recognition_dict['enemies_pos'] in self.recognition:
            state.append(tuple(self.enemies_pos))
        
        return tuple(state)
    
    def get_reward(self, x, y):
        # 報酬を渡す関数
        
        reward = 0
        
        # ドットをすべて回収した場合追加
        if self.is_completed():
            reward += self.rewards['all']
            
        moving_object = self._exist_moving_object(x, y)
        
        if moving_object:
            reward += self.rewards[self.objects[moving_object]]
        else:
            reward += self.rewards[self.objects[self.map[y, x]]]
        return reward
    
    def is_completed(self):
        # ドットを全て回収できたか確認する関数
        
        dot_n = self._count_dot()
        
        if dot_n == 0:
            return True
        else:
            return False
        
    def _count_dot(self):
        # マップにあるドットの数を数える関数
        return np.count_nonzero(self.map == self.objects['dot'])
    
    def _exist_moving_object(self, x, y):
        # 受け取った座標に動くオブジェクト（敵）がいた場合、そのオブジェクトを返す
        
        if (x, y) in self.enemies_pos:
            return self.objects['enemy']
        
        else:
            return False
    
    def _is_within_range(self, x, y):
        # 受け取った座標がマップの範囲内か返す関数
        
        if x < 0 or x >= self.width:
            return False
        elif y < 0 or y >= self.height:
            return False
        return True
    
    def to_object(self, x, y, object):
        # オブジェクトを置き換える関数
        self.map[y, x] = object
    
    def set_agent_pos(self, x, y, number):
        # エージェントの位置を受け取る関数
        self.agents_pos[number] = (x, y)
    
    def set_enemy_pos(self, x, y, number):
        # 敵の位置を受け取る関数
        self.enemies_pos[number] = (x, y)
    
    def get_agents_pos(self):
        # 各エージェントの座標を返す関数
        return self.agents_pos
    
    def get_ini_map(self):
        return self.ini_map
    
    def reset(self):
        # マップを初期状態にする関数
        self.map = copy.deepcopy(self.ini_map)
        self.agents_pos = copy.deepcopy(self.ini_agents_pos)
        self.enemies_pos = copy.deepcopy(self.ini_enemies_pos)