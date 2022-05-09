import pyxel
import numpy as np

class App:
    # 描画を行うクラス
    
    def __init__(self, world, agents, enemies, map_w, map_h, dot_size, fps, objects, obj_pos, actions, action_list):
        self.world = world
        self.agents = agents
        self.enemies = enemies
        self.map_w = map_w
        self.map_h = map_h
        self.dot_size = dot_size
        self.objects = objects
        self.obj_pos = obj_pos
        self.actions = actions
        
        # エージェントと敵の行動を格納したリスト
        self.action_list = action_list
        
        # 現在のフレームを表す変数
        self.frame = 0
        
        # 描画を開始するか判定する変数
        self.is_start = True
        
        # pyxelの設定
        pyxel.init(map_w*dot_size, map_h*dot_size, fps=fps)
        
        # ドット絵をロード
        pyxel.load('dot_pictures/pacman.pyxres')
        
    def _update(self):
        # エージェントの座標などを更新する関数
        
        # [q]が押されたとき、描画開始
        if pyxel.btnp(pyxel.KEY_Q):
            self.is_start = False
        
        if not self.is_start:
            
            # 行動を保存したリストのインデックスを求める
            action_index = self._compute_action_index()
            
            # アクションリストに従って、各オブジェクトが行動
            if action_index < len(self.action_list):
                for agent in self.agents:
                    if agent.number == self.action_list[action_index][0]:
                        self._move(agent, self.action_list[action_index][1])
                        
                for enemy in self.enemies:
                    if enemy.number == self.action_list[action_index][0] - len(self.agents):
                        self._move(enemy, self.action_list[action_index][1])
            
            self.frame += 1

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
        
        # 敵の描画
        for enemy in self.enemies:
            x, y = enemy.get_dot_pos()
            self._draw_enemy(x, y)
            
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
    
    def _draw_enemy(self, x, y):
        # 敵を描画する関数
        
        pyxel.blt(x, y, 0,
                  self.obj_pos['enemy'][0],
                  self.obj_pos['enemy'][1],
                  self.dot_size, self.dot_size)
    
    def _move(self, moving, vector):
        # エージェントと敵が行動する関数
        
        dot_x, dot_y = moving.get_dot_pos()
        
        # pyxel上での座標と二次元マップの座標が一致
        if self._is_match_dot(dot_x, dot_y):
            
            # リスト上での座標を取得
            x, y = self._to_world_pos(dot_x, dot_y)
            
            if moving in self.agents:
                self.world.to_object(x, y, self.objects['none'])
                
            # エージェントの移動
            _, _, is_wall = self.world.step(x, y, vector)
            
            if is_wall:
                return 0
            
        # ベクトルに従って移動する関数
        
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
        moving.set_dot_pos((dot_x, dot_y))
        
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
    
    def _compute_action_index(self):
        # 行動を格納したリストのインデックスを求める関数
        return self.frame // self.dot_size
    
    def loop(self):
        # pyxelを実行する関数
        pyxel.run(self._update, self._draw)