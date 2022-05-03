from world import World
from agent import Agent
from app import App
import numpy as np
import matplotlib.pyplot as plt

#---------------------------------実験の設定---------------------------------#
# エピソード数
EPISODE = 1000
# ステップ数
STEP = 100
# マップサイズ
MAP_W = 10
MAP_H = 10
# オブジェクトの種類
OBJECTS = {'none': 0, 'dot': 1, 'wall': 2, 'agent': 3}
OBJECTS.update({v: k for k, v in OBJECTS.items()})
# 報酬
REWARDS = {'none': -1, 'dot': 10, 'wall': -10, 'agent': -1}
# エージェント数
AGENT_N = 1
# エージェントの初期位置(エージェント数に合わせる)
AGENTS_POS = [(1,1), (8,8)]
# エージェントの視界
AGENT_SCOPE = 1

#-----------------------------エージェントの設定------------------------------#
# 探索率の係数(1に近い方が良い)
K = .9999
# 学習率
ALPHA = .1
# 割引率
GAMMA = .90
# 行動の種類
ACTIONS = {'up': 0, 'down': 1, 'left': 2, 'right': 3}

#--------------------------------pyxelの設定---------------------------------#
# ドットのサイズ
DOT_SIZE = 8
# 秒間フレーム数
FPS = 100
# 描画するオブジェクトのドット絵がある場所
OBJ_POS = {'none': (8,8), 'dot': (8,16), 'wall': (0,16), 'agent': (0,0)}

def main():
    # 環境の生成
    world = World(MAP_W, MAP_H, OBJECTS, ACTIONS, REWARDS, AGENT_SCOPE)
    
    # エージェントの生成
    agents = []
    for n in range(AGENT_N):
        agents.append(Agent(ALPHA, GAMMA, K, ACTIONS, AGENTS_POS[n], DOT_SIZE,
                            world.get_state(AGENTS_POS[n][0], AGENTS_POS[n][1])))
    
    # 実験
    for episode in range(EPISODE - 1):
        
        # 探索率の算出
        for agent in agents:
            agent.compute_epsilon(episode)
        
        for step in range(STEP):
            for agent in agents:
                
                x, y = agent.pos[0], agent.pos[1]
                
                # agentの足元を何も無い状態にする
                world.to_none(x, y)
                
                # 行動を選択
                action = agent.act()
                
                # エージェントが移動
                pos, state, reward, is_wall, is_completed = world.step(x, y, action, agent.get_state())
                
                # 状態と報酬の観測
                agent.observe(state, reward)
                
                # agentの位置を渡す
                agent.set_pos(pos)
                world.to_agent(pos[0], pos[1])
            
            # マップ上のドットをすべて回収していればエピソード終了
            if is_completed:
                break
        
        # 初期化
        for agent in agents:
            agent.reset()

        world.reset()
        
    # pyxelで最後のエピソードを描画
    app = App(world, agents, MAP_W, MAP_H, DOT_SIZE,
              FPS, OBJECTS, OBJ_POS, ACTIONS)
    app.loop()
    
    return 0
    
if __name__ == "__main__":
    main()