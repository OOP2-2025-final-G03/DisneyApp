# アプリ名: ディズニーアプリ

## 概要
このアプリはディズニーランドの顧客のデータとアトラクションなどのデータの管理及びデータ分析を行うアプリです。

## アピールポイント
![アプリケーションの動作サンプル](./sample.gif)

## 動作条件: require
```bash
python 3.13.7

# python lib
Flask==3.1.2
peewee==3.18.3
```

## 使い方: usage
1. 必要なライブラリをインストール。
```bash
$ pip install Flask==3.1.2 peewee==3.18.3
```

2. アプリケーションを起動。
```bash
$ python app.py
```

3. リポジトリをクローン。
```bash
$ git clone https://github.com/OOP2-2025-final-G03/DisneyApp.git
```

4. プロジェクトディレクトリに移動。
```bash
$ cd DisneyApp/
```
> ランダムでユーザーデータなどを挿入。(テスト用)
```bash
$ python insert_data.py
```

5. 実行
```bash
$ python app.py
```

3. ブラウザでアプリケーションを開く。
> 例:app.pyを以下の配置で起動した場合:
> <br>app.run(host='0.0.0.0', port=8000, debug=True)
```
http://localhost:8000
```
