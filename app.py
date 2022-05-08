import pyxel
import numpy as np

class App:
    def __init__(self, world, agents, enemies, map_w, map_h, dot_size, fps, objects, obj_pos, actions, vector_list):
        self.world = world
        self.agents = agents
        self.enemies = enemies
        self.map_w = map_w
        self.map_h = map_h
        self.dot_size = dot_size
        self.objects = objects
        self.obj_pos = obj_pos
        self.actions = actions
        
        self.vector_list = vector_list
        
        self.frame = 0
        
        # マップ上のドットがすべて回収されたかどうか表す
        self.is_completed = False
        
        # 描画を開始するか判定
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
            
            turn = self._compute_turn()
            
            action_index = self._compute_action()
            
            if action_index < len(self.vector_list):
            
                # エージェントの移動
                for agent in self.agents:
                    if not agent.get_is_dead():
                        if turn == agent.number or turn - 1 == agent.number:
                            self._move(agent, self.vector_list[action_index])
                
                # 敵の移動
                if not self._is_all_dead():
                    for enemy in self.enemies:
                        if turn == len(self.agents) * 2 + enemy.number:
                            self._move(enemy, self.vector_list[action_index])
            
            # # エージェントの移動
            # for agent in self.agents:
            #     if not agent.get_is_dead():
            #         if turn == agent.number or turn - 1 == agent.number:
            #             self._agent_move(agent)
            # # 敵の移動
            # if not self._is_all_dead():
            #     for enemy in self.enemies:
            #         if turn == len(self.agents) * 2 + enemy.number:
            #             self._enemy_move(enemy)
            
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
        
        dot_x, dot_y = moving.get_dot_pos()
        
        if self._is_match_dot(dot_x, dot_y):
            
            # リスト上での座標を取得
            x, y = self._to_world_pos(dot_x, dot_y)
            
            if moving in self.agents:
                # エージェントの足元を何も無い状態にする
                self.world.to_object(x, y, self.objects['none'])
            # エージェントの移動
            _, _,  is_wall = self.world.step(x, y, vector)
            
            if is_wall:
                return 0
            
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
        
    
    def _agent_move(self, agent):
        # エージェントが移動する関数
        
        # ドット上でのエージェントの座標を取得
        dot_x, dot_y = agent.get_dot_pos()
        
        # ドット上での座標と、リスト上での座標が一致しているか判定
        if self._is_match_dot(dot_x, dot_y):
            
            # リスト上での座標を取得
            x, y = self._to_world_pos(dot_x, dot_y)
            
            # エージェントがいる座標を何もない状態にする
            self.world.to_object(x, y, self.objects['none'])
            
            # Qテーブルから方向を選択
            vector = agent.act()
            agent.set_vector(vector)
            
            # エージェントの移動
            to_x, to_y, is_wall = self.world.step(x, y, vector)
            
            # 状態と報酬の観測
            if is_wall:
                agent.observe(self.world.get_state(x, y), self.world.rewards['wall'])
            else:
                agent.observe(self.world.get_state(to_x, to_y), self.world.get_reward(to_x, to_y))
            
            agent.set_pos(to_x, to_y)
            self.world.set_agent_pos(to_x, to_y, agent.number)
            
            # 「移動先が壁」or「マップ上のドットを全て回収した」場合移動しない
            if is_wall or self.world.is_completed():
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
        
        # 移動先にあるオブジェクトが敵
        for enemy in self.enemies:
            if enemy.dot_pos == (dot_x, dot_y):
                agent.set_is_dead(True)
        
        # 移動先をエージェントに渡す
        agent.set_dot_pos((dot_x, dot_y))
        
    def _enemy_move(self, enemy):
        # 敵が移動する関数
        
        # ドット上での敵の座標を取得
        dot_x, dot_y = enemy.get_dot_pos()
        
        # ドット上での座標と、リスト上での座標が一致しているか判定
        if self._is_match_dot(dot_x, dot_y):
            
            # リスト上での座標を取得
            x, y = self._to_world_pos(dot_x, dot_y)
            
            # 行動を決定
            vector = enemy.act(self.world.agents_pos)
            enemy.set_vector(vector)
            
            # 移動
            to_x, to_y, is_wall = self.world.step(x, y, vector)
            
            if is_wall:
                return 0
            
            #「マップ上のドットを全て回収した」場合移動しない
            if self.world.is_completed():
                return 0
            
            enemy.set_pos(to_x, to_y)
            self.world.set_enemy_pos(to_x, to_y, enemy.number)
        
        # エージェントが向いている方向を取得
        vector = enemy.get_vector()
        
        # 方向に従って移動
        if vector == self.actions['up']:
            dot_y -= 1
        elif vector == self.actions['down']:
            dot_y += 1
        elif vector == self.actions['left']:
            dot_x -= 1
        elif vector == self.actions['right']:
            dot_x += 1
        
        # 移動先にあるオブジェクトがエージェント
        for agent in self.agents:
            if agent.dot_pos == (dot_x, dot_y):
                agent.set_is_dead(True)
                agent.observe(agent.get_previous_state(), self.world.rewards['enemy'])
        
        # 移動先を敵に渡す
        enemy.set_dot_pos((dot_x, dot_y))

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
    
    def _is_all_dead(self):
        count = 0
        for agent in self.agents:
            if agent.get_is_dead():
                count += 1
        
        return count == len(self.agents)
    
    def _compute_turn(self):
        # ターンを計算する関数
        return (self.frame // self.dot_size) % (len(self.agents) * 2 + len(self.enemies))
    
    def _compute_action(self):
        # ベクトルリストの添え字を求める関数
        return self.frame // self.dot_size
    
    def loop(self):
        # pyxelを実行する関数
        pyxel.run(self._update, self._draw)