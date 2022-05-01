from world import World
from agent import Agent
from app import App
import numpy as np

#-------実験の設定------#
# エピソード数
EPISODE = 300
# ステップ数
STEP = 200
# マップサイズ
MAP_W = 10
MAP_H = 10
# オブジェクトの種類
OBJECTS = {'none': 0, 'dot': 1, 'wall': 2, 'agent': 3, 'enemy': 4}
OBJECTS.update({v: k for k, v in OBJECTS.items()})
# 報酬
REWARDS = {'none': -1, 'dot': 10, 'wall': -10, 'agent': -1, 'enemy': -100}
# エージェント数
AGENT_N = 1
# エージェントの初期位置(エージェント数に合わせる)
AGENTS_POS = [(1,1), (8,8)]
# エネミー数
ENEMY_N = 0


#----エージェントの設定----#
# 探索率を算出する係数
K = .9999
# 学習率
ALPHA = .1
# 割引率
GAMMA = .90
# 行動の種類数
ACTIONS = {'up': 0, 'down': 1, 'left': 2, 'right': 3}

#----pyxelの設定----#
# ドットのサイズ
DOT_SIZE = 8

# 秒間フレーム数
FPS = 100

# 描画するオブジェクトのドット絵がある場所
OBJ_POS = {'none': (8,8), 'dot': (8,16), 'wall': (0,16), 'agent': (0,0)}


def main():
    # 環境の生成
    world = World(MAP_W, MAP_H, DOT_SIZE, OBJECTS,
                  AGENTS_POS, ACTIONS, REWARDS)
    
    # エージェントの生成
    agents = []
    for n in range(AGENT_N):
        agents.append(Agent(alpha=ALPHA,
                            gamma=GAMMA,
                            k=K,
                            actions=ACTIONS,
                            pos=AGENTS_POS[n],
                            dot_size=DOT_SIZE,
                            observation=world.get_state(AGENTS_POS[n][0], AGENTS_POS[n][0])))
    
    # 実験
    for episode in range(EPISODE):
        
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
                
                pos, state, reward, is_wall, is_end_episode = world.step(x, y, action, agent.state)
                
                # 状態と報酬の観測
                agent.observe(state, reward)
                
                # agentの位置を渡す
                agent.set_pos(pos)
                world.to_agent(pos[0], pos[1])
                
                # 描画
                # app.set_map(world.map)
                
            if is_end_episode:
                break
        
        world.reset()
        for agent in agents:
            agent.reset()
    
    app = App(world, agents, MAP_W, MAP_H, DOT_SIZE,
              FPS, OBJECTS, OBJ_POS, ACTIONS, EPISODE, STEP)
    app.loop()
    
    return 0
    
if __name__ == "__main__":
    main()