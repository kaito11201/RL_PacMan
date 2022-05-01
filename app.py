from threading import setprofile
import pyxel
import numpy as np

class App:
    def __init__(self, world, agents, map_w, map_h, dot_size, fps, objects, obj_pos, actions, episode, step):
        
        self.map_w = map_w
        self.map_h = map_h
        self.dot_size = dot_size
        self.objects = objects
        self.obj_pos = obj_pos
        self.actions = actions
        self.world = world
        self.agents = agents
        
        self.limit_episode = episode
        self.limit_step = step * 2
        self.episode = 0
        self.step = 0
        self.is_episode_end = False
        
        # pyxelの設定
        pyxel.init(map_w*dot_size, map_h*dot_size, fps=fps)
        
        # ドット絵をロード
        pyxel.load('pacman.pyxres')
        
    def _update(self):
        if self.step == self.limit_step:
            self._reset()
            self.step = 0
            self.episode += 1
        
        if self.episode == self.limit_episode:
            pyxel.quit()
        
        # agentの描画
        for agent in self.agents:
            self._agent_move(agent)
        
        
        
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        
    
    def _draw(self):
        
        # 背景を真っ黒にする
        pyxel.cls(0)
        self._draw_map()
        for agent in self.agents:
            self._draw_agent(agent.dot_pos)
        
        pyxel.text(self.dot_size, 0, self._get_text(), 0)
        
    def _draw_map(self):
        
        # マップの取得
        
        for y in range(self.map_h):
            for x in range(self.map_w):
                
                # 各オブジェクトの描画
                pyxel.blt(x * self.dot_size, y * self.dot_size, 0,
                          self.obj_pos[self.objects[self.world.map[y,x]]][0],
                          self.obj_pos[self.objects[self.world.map[y,x]]][1],
                          self.dot_size, self.dot_size)
    
    def _draw_agent(self, pos):
        pyxel.blt(pos[0], pos[1], 0,
                  self.obj_pos['agent'][0],
                  self.obj_pos['agent'][1],
                  self.dot_size, self.dot_size)
        
    def _agent_move(self, agent):
        
        dot_x, dot_y = agent.get_dot_pos()
        vector = agent.get_vector()
        
        # 行動選択
        if self._is_match_dot(dot_x, dot_y):
            
            x, y = self._cordinate_transform(dot_x, dot_y)
            self.world.to_none(x, y)
            vector = agent.act()
            agent.set_vector(vector)
            pos, state, reward, is_wall, self.is_episode_end = self.world.step(x, y, vector, agent.get_state())
            agent.observe(state, reward)
            self.step += 1
            
            if is_wall:
                return 0
        
        if vector == self.actions['up']:
            dot_y -= 1
        elif vector == self.actions['down']:
            dot_y += 1
        elif vector == self.actions['left']:
            dot_x -= 1
        elif vector == self.actions['right']:
            dot_x += 1

        agent.set_dot_pos((dot_x, dot_y))
    
    def set_world(self, world):
        self.world = world
    
    def set_agents(self, agent):
        self.agent = agent
        
    def loop(self):
        # pyxelの実行
        pyxel.run(self._update, self._draw)
        
    def _is_match_dot(self, x, y):
        # pyxelの座標と二次元リストの座標が一致しているか返す関数
        
        if x % self.dot_size == 0 and y % self.dot_size == 0:
            return True
        else:
            return False
    
    def _cordinate_transform(self, x, y):
        x = int(x / 8)
        y = int(y / 8)
        return x, y
    
    def _reset(self):
        self.world.reset()
        for agent in self.agents:
            agent.reset()
    
    def _get_text(self):
        return f"episode:{self.episode} step:{self.step}"