from moving_object import MovingObject
import numpy as np
import copy

class Enemy(MovingObject):
    def __init__(self, number, pos, dot_size, actions, observation, objects, scope):
        super().__init__(number, pos, dot_size, actions)
        self.objects = objects
        self.scope = scope
        self.view = observation[0]
        self.ini_view = observation[0]
        # self.origin = np.array([scope, scope])
        
    def act(self, agents_pos):
        # 行動を選択する関数
        
        # エージェントまでのベクトルを求める
        vectors = self._compute_vectors(agents_pos)
        action = self._decision_action(vectors)
        # print(agents_pos, self.pos, vectors, action)
        return action
    
    def _decision_action(self, vectors):
        # 進む方向を決める関数
        
        # 敵から近いエージェントまでのベクトルを求める
        vector = self._compute_near_agent_vector(vectors)
        
        actions = []
        
        if vector[1] < 0:
            actions.append(self.actions['up'])
        if vector[1] > 0:
            actions.append(self.actions['down'])
        if vector[0] < 0:
            actions.append(self.actions['left'])
        if vector[0] > 0:
            actions.append(self.actions['right'])
        
        if actions:
            return np.random.choice(actions)
        else:
            return self.actions['up']
    
    def _compute_vectors(self, agents_pos):
        # エージェントがいる方向を求める関数
        
        vectors = []
        
        # numpy配列に変換
        agents_pos = self._to_array(agents_pos)
        
        for pos in agents_pos:
            vector = pos - self.pos
            vectors.append(vector)
            
        return vectors
    
    def _compute_near_agent_vector(self, vectors):
        # 敵から近いエージェントまでのベクトルを返す関数
        
        distance_list = np.array([])
        
        for vector in vectors:
            distance_list = np.append(distance_list, np.sum(np.power(vector, 2)))
        
        return vectors[np.argmin(distance_list)]
        
    def _compute_agent_pos(self):
        # 視界の中でのエージェントの座標を求める関数
        index = self.view.index(self.objects['agent'])
        agent_x = index % (self.scope * 2 + 1)
        agent_y = index // (self.scope * 2 + 1)
        
        return np.array([agent_x, agent_y])
        
    def set_view(self, view):
        self.view = view
    
    def _to_array(self, tuples_list):
        return list(map(np.array, tuples_list))
    
    def reset(self):
        super().reset()
        self.view = copy.deepcopy(self.ini_view)