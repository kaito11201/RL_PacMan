from moving_object import MovingObject
import numpy as np

class Enemy(MovingObject):
    def __init__(self, pos, dot_size, actions, observation, objects, scope):
        super().__init__(pos, dot_size, actions, observation)
        self.objects = objects
        self.scope = scope
        
    def act(self):
        # 行動を選択する関数
        view = self.state[0]
        if self.objects['agent'] in view:
            index = view.index(self.objects['agent'])
            view_len = len(view)
            
            x = view_len % (self.scope * 2 + 1)
            y = view_len // (self.scope * 2 + 1)
            
            vector = self._compute_vector(x, y)
            
            
        else:
            key = [k for k, v in self.objects.items() if v == np.randint(len(self.actions))][0]
            return self.actions[key]
    
    def _compute_vector(self, x, y):
        # エージェントがいる方向を求める関数
        return np.array([x - self.scope, y - self.scope])
        
        
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