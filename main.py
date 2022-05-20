from world import World
from agent import Agent
from enemy import Enemy
from app import App
import numpy as np
import copy
import csv
import datetime

#---------------------------------実験の設定---------------------------------#
# エピソード数
EPISODE = 100000
# ステップ数
STEP = 400

# マップサイズ
MAP_W = 10
MAP_H = 10
# オブジェクトの種類
OBJECTS = {'none': 0, 'dot': 1, 'wall': 2, 'agent': 3, 'enemy': 4}
OBJECTS.update({v: k for k, v in OBJECTS.items()})

# エージェント数
AGENT_N = 2
# エージェントの初期位置
AGENTS_POS = [(1,1), (MAP_W - 2, 1), (((MAP_W - 2) // 2), 1)]

# 敵の数
ENEMY_N = 1
# 敵の初期位置
ENEMIES_POS = [(MAP_W - 2,MAP_H - 2), (1, MAP_H - 2)]

# 行動の種類
ACTIONS = {'up': 0, 'down': 1, 'left': 2, 'right': 3}

#-----------------------------Q学習の設定------------------------------#
# 探索率の係数(1に近い方が良い)
K = .9999
# 学習率
ALPHA = .1
# 割引率
GAMMA = .90

# 視界の範囲
SCOPE = 2
# 認識機能の一覧
RECOGNITION_DICT = {0: 'view', 1: 'remain_dots', 2: 'pos', 3: 'agents_pos', 4: 'enemies_pos'}
RECOGNITION_DICT.update({v: k for k, v in RECOGNITION_DICT.items()})
# エージェントに与える認識機能の番号
RECOGNITION = [0, 1, 2, 3, 4]

# 報酬
REWARDS = {'none': -1, 'dot': 5, 'wall': -10, 'agent': -1, 'enemy': -50, 'all': 50}

#--------------------------------pyxelの設定---------------------------------#
# ドットのサイズ
DOT_SIZE = 8
# 秒間フレーム数
FPS = 100
# 描画するオブジェクトのドット絵がある場所
OBJ_POS = {'none': (8,8), 'dot': (8,16), 'wall': (0,16), 'agent': (0,0), 'enemy': (0, 8)}

def main(now):
    # 環境の生成
    world = World(MAP_W, MAP_H, OBJECTS, ACTIONS, REWARDS,
                  RECOGNITION_DICT, RECOGNITION, SCOPE,
                  AGENTS_POS[:AGENT_N], ENEMIES_POS[:ENEMY_N])
    
    # エージェントの生成
    agents = []
    for n in range(AGENT_N):
        agents.append(Agent(ALPHA, GAMMA, K, n, AGENTS_POS[n], DOT_SIZE, ACTIONS,
                            world.get_state(AGENTS_POS[n][0], AGENTS_POS[n][1]), False))
    
    # 敵の生成
    enemies = []
    for n in range(ENEMY_N):
        enemies.append(Enemy(n, ENEMIES_POS[n], DOT_SIZE, ACTIONS))
    
    # 設定の出力
    output_option(now, world.get_ini_map())
    
    # ドットを全て回収した回数を保存する変数
    completed_count = 0
    # ドットを全て回収した時のstep数を保存するリスト
    completed_step_list = []
    # ドットを全て回収したときの行動を保存するリスト
    completed_action_list = []
    
    # 実験
    for episode in range(EPISODE):
        action_list = []
        
        # 実験の経過を出力
        if episode % (EPISODE // 10) == 0:
            print(f"{episode}episode経過しました。")
        
        # 探索率の算出
        for agent in agents:
            agent.compute_epsilon(episode)
        
        for step in range(STEP):
            
            # エージェントの行動
            for agent in agents:
                # エージェントが生存している場合、行動
                if not agent.get_is_dead():
                    action_list.append((agent.number, agent_move(agent, world)))
            
            # 敵の行動
            for enemy in enemies:
                # エージェントが死滅していない場合、行動
                if not is_all_dead(agents):
                    action_list.append((AGENT_N + enemy.number, enemy_move(enemy, agents, world)))
            
            # ドットを全て回収した場合episode終了
            if world.is_completed():
                
                # 全てのエージェントに報酬を与える
                for agent in agents:
                    agent.observe(agent.get_previous_state(), REWARDS['all'])
                
                # 行動の保存
                completed_action_list = copy.deepcopy(action_list)
                
                completed_count += 1
                completed_step_list.append(step)
                break
            
            # エージェントが全て死んだ場合終了
            if is_all_dead(agents):
                break
            
        # ドットを全て回収できなかったとき、最後の行動を保存
        if not completed_action_list:
            if episode == EPISODE - 1:
                last_action_list = copy.deepcopy(action_list)
            
        # 初期化
        for agent in agents:
            agent.reset()
        for enemy in enemies:
            enemy.reset()
        world.reset()
    
    # 学習結果を表示
    output_result(dt_now, completed_action_list,
                completed_count, completed_step_list,
                agents, world.get_ini_map())
    
    # pyxelで実験の様子を描画
    if completed_action_list:
        app = App(world, agents, enemies, MAP_W, MAP_H, DOT_SIZE,
                FPS, OBJECTS, OBJ_POS, ACTIONS, completed_action_list)
        
    else:
        print("ドットを全て回収できたepisodeはありませんでした。")
        app = App(world, agents, enemies, MAP_W, MAP_H, DOT_SIZE,
                FPS, OBJECTS, OBJ_POS, ACTIONS, last_action_list)
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
        world.set_agent_pos(None, None, agent.number)
        
    # 位置を渡す
    agent.set_pos(to_x, to_y)
    world.set_agent_pos(to_x, to_y, agent.number)
    
    return action

def enemy_move(enemy, agents, world):
    # 敵の行動を行う関数
    
    x, y = enemy.pos[0], enemy.pos[1]
    
    # 行動を選択
    action = enemy.act(world.get_agents_pos())
    
    # 移動
    to_x, to_y, is_wall = world.step(x, y, action)
    
    if is_wall:
        return 0
    
    # 移動先にあるオブジェクトがエージェント
    for agent in agents:
        if agent.pos == (to_x, to_y):
            agent.set_is_dead(True)
            agent.observe(agent.get_previous_state(), REWARDS['enemy'])
            world.set_agent_pos(None, None, agent.number)
    
    # 位置を渡す
    enemy.set_pos(to_x, to_y)
    world.set_enemy_pos(to_x, to_y, enemy.number)
    
    return action

def is_all_dead(agents):
    # エージェントが死滅したか判定する関数
    
    count = 0
    
    for agent in agents:
        if agent.is_dead:
            count += 1
    
    if count >= len(agents):
        return True
    else:
        return False

def output_option(now, map):
    # 実験の設定を出力する関数
    
    f = open(f'result/learn_results/learn_result_{now}.txt', 'w')
    
    # 設定の記述
    f.write("[option(experiment)]\n")
    f.write(f"EPISODE:{EPISODE} STEP:{STEP}\n")
    f.write(f"MAP_WIDTH:{MAP_W} MAP_HEIGHT:{MAP_H}\n")
    f.write(f"AGENTS_POSITION:{AGENTS_POS[:AGENT_N]} ENEMIES_POSITION:{ENEMIES_POS[:ENEMY_N]}\n")
    f.write(f"SCOPE:{SCOPE}\n")
    write_map(f, map)
    
    f.write("\n[option(learning)]\n")
    f.write(f"K:{K} ALPHA:{ALPHA} GAMMA:{GAMMA}\n")
    f.write(f"RECOGNITION: {write_recognition()}\n")
    f.write(f"REWARDS:{REWARDS}\n")
    
    f.close()
    
def output_result(now, completed_action_list, completed_count, completed_step_list, agents, map):
    # 学習結果を出力する関数
    
    mean = None
    median = None
    
    if completed_step_list:
        mean = np.mean(completed_step_list)
        median = np.median(completed_step_list)
    
    f = open(f'result/learn_results/learn_result_{now}.txt', 'a')
    
    f.write(f"\n[result]\n")
    f.write(f"completed:{completed_count}/{EPISODE} completed_ratio:{completed_count/ EPISODE * 100}%\n")
    f.write(f"completed_step_mean:{mean}\n")
    f.write(f"completed_step_median:{median}\n")
    f.write(f"action_list:{completed_action_list}")
    f.close()
    
    # 各エージェントのQテーブルを出力
    for i, agent in enumerate(agents):
        with open(f'result/q_tables/q_table({i})_{dt_now}.csv', 'w') as f:
            writer = csv.writer(f)
            for k, v in agent.q_table.items():
                writer.writerow([k, v])

def compute_mean(list_):
    # 与えられたリストの平均値を求める関数
    return np.mean(list_)

def write_map(f, map):
    # マップをテキストで出力する関数
    for y in map:
        f.write(f"{y}\n")

def write_recognition():
    # 認識機能の設定をテキストで出力する関数
    list_ = []
    for key in RECOGNITION:
        list_.append(RECOGNITION_DICT[key])
    return list_
    
if __name__ == "__main__":
    
    # 現在の日付と時刻を取得
    dt_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    
    main(dt_now)