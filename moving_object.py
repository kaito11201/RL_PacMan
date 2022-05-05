import copy

class MovingObject:
    def __init__(self, pos, dot_size, actions, observation):
        
        # 座標系の変数
        self.pos = pos
        self.ini_pos = pos
        self.dot_pos = (pos[0] * dot_size, pos[1] * dot_size)
        self.ini_dot_pos = self.dot_pos
        
        # 行動系の変数
        self.actions = actions
        self.vector = None
        
        # 状態系の変数
        self.state = observation
        self.ini_state = observation
        
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
    
    def reset(self):
        # 座標と状態をリセットする関数
        self.pos = self.ini_pos
        self.dot_pos = self.ini_dot_pos
        self.state = copy.deepcopy(self.ini_state)