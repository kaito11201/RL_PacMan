import copy

class MovingObject:
    # 動くオブジェクトの親クラス
    
    def __init__(self, number, pos, dot_size, actions):
        
        # 番号
        self.number = number
        
        # 座標系の変数
        self.pos = pos
        self.ini_pos = pos
        self.dot_pos = (pos[0] * dot_size, pos[1] * dot_size)
        self.ini_dot_pos = self.dot_pos
        
        # 行動系の変数
        self.actions = actions
        self.vector = None
        
    def set_pos(self, x, y):
        # リスト上での座標を渡す関数
        self.pos = (x, y)
    
    def get_pos(self):
        # リスト上での座標を取得する関数
        return self.pos
    
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
        # 座標をリセットする関数
        self.pos = self.ini_pos
        self.dot_pos = self.ini_dot_pos