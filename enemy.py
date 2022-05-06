from moving_object import MovingObject
import numpy as np

class Enemy(MovingObject):
    def __init__(self, pos, dot_size, actions, observation, objects, scope):
        super().__init__(pos, dot_size, actions, observation)
        self.objects = objects
        self.scope = scope
        self.view = self.state[0]
        self.origin = self._compute_origin()
        
    def act(self):
        # 行動を選択する関数
        
        if self.objects['agent'] in self.view:
            vector = self._compute_vector(self._compute_agent_pos())
            return self._decision_action(vector)
            
        else:
            key = [k for k, v in self.objects.items() if v == np.randint(len(self.actions))][0]
            return self.actions[key]
    
    def _decision_action(self, vector):
        # 進む方向を決める関数
        if vector[1] < 0:
            return self.actions['up']
        elif vector[1] > 0:
            return self.actions['down']
        elif vector[0] < 0:
            return self.actions['left']
        elif vector[0] > 0:
            return self.actions['right']
        else:
            # 敵とエージェントの位置が重なっている場合
            return self.actions['right']
    
    def _compute_vector(self, pos):
        # エージェントがいる方向を求める関数
        return pos - self.origin
    
    def _compute_agent_pos(self):
        # 視界の中でのエージェントの座標を求める関数
        index = self.view.index(self.objects['agent'])
        agent_x = index % (self.scope * 2 + 1)
        agent_y = index // (self.scope * 2 + 1)
        
        return np.array([agent_x, agent_y])
    
    def _compute_origin(self):
        # 視界の中での敵の座標を求める関数
        view_len = len(self.view)
        origin_x = view_len % (self.scope * 2 + 1)
        origin_y = view_len // (self.scope * 2 + 1)
        
        return np.array([origin_x, origin_y])
    
    # def _depth_search(self, x, y, route):
    #     # 深さ優先でルートを探索する関数
        
    #     if self.map[y, x] == self.objects['agent']:
    #         print(1)
    #         return route
        
    #     # 探索済み
    #     self.map[y, x] = self.objects['searched']
        
    #     # 上下左右を探索
    #     if self._can_search(x, y - 1):
    #         route.append(self.actions['up'])
    #         self._depth_search(x, y - 1, route)
            
    #     elif self._can_search(x, y + 1):
    #         route.append(self.actions['down'])
    #         self._depth_search(x, y + 1, route)
            
    #     elif self._can_search(x - 1, y):
    #         route.append(self.actions['left'])
    #         self._depth_search(x - 1, y, route)
            
    #     elif self._can_search(x + 1, y):
    #         route.append(self.actions['right'])
    #         self._depth_search(x + 1, y, route)
        
    #     print(route)
    #     # 探索可能に戻す
    #     self.map[y, x] = self.objects['none']
    #     route.pop(-1)
    
    # def _can_search(self, x, y):
    #     # 受け取った座標が探索できるか判定する関数
        
    #     # 壁か探索済みの場合探索できない
    #     if self.map[y, x] == self.objects['wall']:
    #         return False
    #     elif self.map[y, x] == self.objects['searched']:
    #         return False
    #     return True