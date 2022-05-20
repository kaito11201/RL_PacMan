# RL_PacMan
## 環境
- python 3.8.5
## 各ファイル
- app.py: pyxelの設定
- agent.py: Q学習を行うエージェントの設定
- enemy.py: 敵の設定
- moving_object.py: エージェントと敵の親クラスの設定
- world.py: マップの設定
- main.py: 実行用スクリプト

## 各フォルダ
- dot_pictures: pyxelで描画するドット絵ファイルを格納するフォルダ
- result: 実験の設定と結果、各エージェントのQテーブルを格納するフォルダ

## 実行方法
1. リポジトリをクローン
2. main.pyを実行
~~~
python main.py
~~~
3. Pyxelが起動した後、「space」キーを押すとキャラクターが動く