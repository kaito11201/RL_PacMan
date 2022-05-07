from world import World
from agent import Agent
from enemy import Enemy
from app import App
import numpy as np
import csv

#---------------------------------実験の設定---------------------------------#
# エピソード数
EPISODE = 300
# ステップ数
STEP = 300

# マップサイズ
MAP_W = 16
MAP_H = 16
# オブジェクトの種類
OBJECTS = {'none': 0, 'dot': 1, 'wall': 2, 'agent': 3, 'enemy': 4}
OBJECTS.update({v: k for k, v in OBJECTS.items()})

# エージェント数
AGENT_N = 1
# エージェントの初期位置
AGENTS_POS = [(1,1)]

# 敵の数
ENEMY_N = 1
# 敵の初期位置
ENEMIES_POS = [(14,14)]

# 視界の範囲
SCOPE = 2
# 行動の種類
ACTIONS = {'up': 0, 'down': 1, 'left': 2, 'right': 3}

#-----------------------------Q学習の設定------------------------------#
# 探索率の係数(1に近い方が良い)
K = .99999999
# 学習率
ALPHA = .1
# 割引率
GAMMA = .90
# 報酬
REWARDS = {'none': -1, 'dot': 10, 'wall': -10, 'agent': -1, 'enemy': -100, 'all': 50}

#--------------------------------pyxelの設定---------------------------------#
# ドットのサイズ
DOT_SIZE = 8
# 秒間フレーム数
FPS = 100
# 描画するオブジェクトのドット絵がある場所
OBJ_POS = {'none': (8,8), 'dot': (8,16), 'wall': (0,16), 'agent': (0,0), 'enemy': (0, 8)}

def main():
    # 環境の生成
    world = World(MAP_W, MAP_H, OBJECTS, ACTIONS, REWARDS, SCOPE, AGENTS_POS, ENEMIES_POS)
    
    # エージェントの生成
    agents = []
    for n in range(AGENT_N):
        agents.append(Agent(ALPHA, GAMMA, K, n, AGENTS_POS[n], DOT_SIZE, ACTIONS,
                            world.get_state(AGENTS_POS[n][0], AGENTS_POS[n][1]), False))
    
    # 敵の生成
    enemies = []
    for n in range(ENEMY_N):
        enemies.append(Enemy(n, ENEMIES_POS[n], DOT_SIZE, ACTIONS,
                             world.get_state(ENEMIES_POS[n][0],ENEMIES_POS[n][1]),
                             OBJECTS, SCOPE))
    
    # 実験
    for episode in range(EPISODE - 1):
        
        # 探索率の算出
        for agent in agents:
            agent.compute_epsilon(episode)
        
        for step in range(STEP):
            if episode == 200:
                print(agents[0].pos, enemies[0].pos)
                
            # エージェントの行動
            for agent in agents:
                # エージェントが生存している場合、行動
                if not agent.get_is_dead():
                    agent_move(agent, world)
            
            # 敵の行動
            if step % 2 == 0:
                for enemy in enemies:
                    enemy_move(enemy, agents, world)
                
            # ドットを全て回収、またはエージェントが死滅した場合終了
            if world.is_completed() or is_all_dead(agents):
                break
        
        # 初期化
        for agent in agents:
            agent.reset()
        for enemy in enemies:
            enemy.reset()
        world.reset()
    
    result(agents)
    
    # pyxelで最後のエピソードを描画
    app = App(world, agents, enemies, MAP_W, MAP_H, DOT_SIZE,
              FPS, OBJECTS, OBJ_POS, ACTIONS)
    app.loop()
    
    return 0

def agent_move(agent, world):
    # エージェントの行動を行う関数
    
    x, y = agent.pos[0], agent.pos[1]
    
    # エージェントの足元を何も無い状態にする
    world.to_object(x, y, OBJECTS['none'])
    
    # 行動を選択
    action = agent.act()
    
    # 移動
    to_x, to_y, is_wall = world.step(x, y, action)
    
    # 観測
    if is_wall:
        agent.observe(world.get_state(to_x, to_y), REWARDS['wall'])
    else:
        agent.observe(world.get_state(to_x, to_y), world.get_reward(to_x, to_y))
    
    # 移動先にあるオブジェクトが敵
    if (to_x, to_y) in world.enemies_pos:
        agent.set_is_dead(True)
    
    # 位置を渡す
    agent.set_pos(to_x, to_y)
    world.set_agent_pos(to_x, to_y, agent.number)

def enemy_move(enemy, agents, world):
    # 敵の行動を行う関数
    
    # エージェントの座標を求める
    agents_pos = []
    for agent in agents:
        agents_pos.append(agent.pos)
    
    x, y = enemy.pos[0], enemy.pos[1]
    
    # 行動を選択
    action = enemy.act(agents_pos)
    
    # 移動
    to_x, to_y, is_wall = world.step(x, y, action)
    
    if is_wall:
        return 0
    
    # 移動先にあるオブジェクトがエージェント
    for agent in agents:
        if agent.pos == (to_x, to_y):
            agent.set_is_dead(True)
            agent.observe(agent.get_state(), REWARDS['enemy'])
            # print(agent.get_state(), agent.q_table[agent.get_state()])
    
    # 位置を渡す
    enemy.set_pos(to_x, to_y)
    world.set_enemy_pos(to_x, to_y, enemy.number)

def is_all_dead(agents):
    count = 0
    
    for agent in agents:
        if agent.is_dead:
            count += 1
    
    if count >= len(agents):
        return True
    else:
        return False

def result(agents):
    # 学習結果の出力をする関数
    
    
    # 各エージェントのQテーブルを出力
    for i, agent in enumerate(agents):
        with open(f'result/q_tables/q_table({i}).csv', 'w') as f:
            writer = csv.writer(f)
            for k, v in agent.q_table.items():
                writer.writerow([k, v])

if __name__ == "__main__":
    main()