from enemy import Enemy
from world import World

#---------------------------------実験の設定---------------------------------#
# エピソード数
EPISODE = 300
# ステップ数
STEP = 150
# マップサイズ
MAP_W = 10
MAP_H = 10
# オブジェクトの種類
OBJECTS = {'none': 0, 'dot': 1, 'wall': 2, 'agent': 3, 'enemy': 4}
OBJECTS.update({v: k for k, v in OBJECTS.items()})
# 報酬
REWARDS = {'none': -1, 'dot': 10, 'wall': -10, 'agent': -1, 'enemy': -50, 'all': 50}
# エージェント数
AGENT_N = 1
# エージェントの初期位置
AGENTS_POS = [(1,1)]
# エージェントの視界
AGENT_SCOPE = 2
# 敵の数
ENEMY_N = 1
# 敵の初期位置
ENEMY_POS = [(8,8)]
# 敵の視界
AGENT_SCOPE = 2

#-----------------------------エージェントの設定------------------------------#
# 探索率の係数(1に近い方が良い)
K = .999
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

# 環境の生成
world = World(MAP_W, MAP_H, OBJECTS, ACTIONS, REWARDS, AGENT_SCOPE)

world.map[AGENTS_POS[0][1], AGENTS_POS[0][0]] = OBJECTS['agent']

print(world.map)

enemy = Enemy(ENEMY_POS[0], DOT_SIZE, ACTIONS, OBJECTS)

enemy.act(world.map)