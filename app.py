from threading import setprofile
import pyxel
import numpy as np

class App:
    def __init__(self, world, agents, map_w, map_h, dot_size, fps, objects, obj_pos, actions):
        self.world = world
        self.agents = agents
        self.map_w = map_w
        self.map_h = map_h
        self.dot_size = dot_size
        self.objects = objects
        self.obj_pos = obj_pos
        self.actions = actions
        
        # マップ上のドットがすべて回収されたかどうか表す
        self.is_completed = False
        
        # 描画を一時停止するか表す
        self.is_stop = False
        
        # pyxelの設定
        pyxel.init(map_w*dot_size, map_h*dot_size, fps=fps)
        
        # ドット絵をロード
        pyxel.load('dot_pictures/pacman.pyxres')
        
    def _update(self):
        # エージェントの座標などを更新する関数
        
        # エージェントの移動
        for agent in self.agents:
            self._agent_move(agent)
        
        self._stop()
            
    def _draw(self):
        # マップやエージェントを毎フレーム描画する関数
        
        # 背景を真っ黒にする
        pyxel.cls(0)
        
        # マップの描画
        self._draw_map()
        
        # エージェントの描画
        for agent in self.agents:
            x, y = agent.get_dot_pos()
            self._draw_agent(x, y)
        
    def _draw_map(self):
        # マップを描画する関数
        
        for y in range(self.map_h):
            for x in range(self.map_w):
                # 各オブジェクトの描画
                pyxel.blt(x * self.dot_size, y * self.dot_size, 0,
                          self.obj_pos[self.objects[self.world.map[y,x]]][0],
                          self.obj_pos[self.objects[self.world.map[y,x]]][1],
                          self.dot_size, self.dot_size)
    
    def _draw_agent(self, x, y):
        # エージェントを描画する関数
        
        pyxel.blt(x, y, 0,
                  self.obj_pos['agent'][0],
                  self.obj_pos['agent'][1],
                  self.dot_size, self.dot_size)
        
    def _agent_move(self, agent):
        # エージェントが移動する関数
        
        # ドット上でのエージェントの座標を取得
        dot_x, dot_y = agent.get_dot_pos()
        
        # ドット上での座標と、リスト上での座標が一致しているか判定
        if self._is_match_dot(dot_x, dot_y):
            
            # リスト上での座標を取得
            x, y = self._to_world_pos(dot_x, dot_y)
            
            # エージェントがいる座標を何もない状態にする
            self.world.to_none(x, y)
            
            # Qテーブルから方向を選択
            vector = agent.act()
            agent.set_vector(vector)
            
            # エージェントの移動
            pos, state, reward, is_wall, is_completed = self.world.step(x, y, vector, agent.get_state())
            
            # 状態と報酬の観測
            agent.observe(state, reward)
            
            # 「移動先が壁」or「マップ上のドットを全て回収した」場合移動しない
            if is_wall or is_completed:
                return 0
        
        # エージェントが向いている方向を取得
        vector = agent.get_vector()
        
        # 方向に従って移動
        if vector == self.actions['up']:
            dot_y -= 1
        elif vector == self.actions['down']:
            dot_y += 1
        elif vector == self.actions['left']:
            dot_x -= 1
        elif vector == self.actions['right']:
            dot_x += 1
            
        # 移動先をエージェントに渡す
        agent.set_dot_pos((dot_x, dot_y))
        
    def _is_match_dot(self, x, y):
        # ドット上での座標とリスト上での座標が一致しているか返す関数
        if x % self.dot_size == 0 and y % self.dot_size == 0:
            return True
        else:
            return False
    
    def _to_world_pos(self, x, y):
        # ドットでの座標を二次元リストの座標に変換する関数
        x = x // self.dot_size
        y = y // self.dot_size
        return x, y
    
    def _stop(self):
        # pyxelを一時停止する関数
        print(self.is_stop)
        if pyxel.btnp(pyxel.KEY_Q):
            self.is_stop = True
        
        while(self.is_stop):
            if pyxel.btnp(pyxel.KEY_Q):
                self.is_stop = False
            
    def loop(self):
        # pyxelを実行する関数
        pyxel.run(self._update, self._draw)