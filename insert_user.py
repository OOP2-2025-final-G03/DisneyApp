#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
100個のランダムなユーザーデータを生成して登録するスクリプト
"""

import random
from datetime import datetime, timedelta
from models import initialize_database, User
from models.db import db

# 日本人名リスト（サンプル）
first_names = ['太郎', '花子', '次郎', '美咲', '健一', '由美', '翔太', '小春', 
               '大輔', '優衣', '拓也', 'さくら', '勇気', '麗奈', '隆一', '彩花',
               '康平', 'みお', '龍一', 'あかり', '雄太', '菜月', '勲', 'ひかり',
               '徹', '桜', '誠', 'ゆりか', '哲也', '彩', '昭平', 'なな', '靖也',
               '瑠美', '哲平', 'あやか', '京平', '玲奈', '利平', 'ひな', '貞一']

last_names = ['山田', '鈴木', '佐藤', '田中', '伊藤', '中村', '小林', '加藤',
              '吉田', '池田', '江藤', '藤田', '林', '前田', '長田', '水野',
              '岡本', '松本', '岡田', '橋本', '新田', '山本', '桜井', '香取']

# データベース初期化
initialize_database()

# 既存のユーザーを削除（重複登録を避けるため）
User.delete().execute()

# ランダムデータ生成と登録
users_data = []
base_date = datetime.now() - timedelta(days=365)  # 1年前から今日までのランダムな日付

for i in range(1, 101):  # ID 1 から 100
    name = random.choice(last_names) + random.choice(first_names)
    age = random.randint(18, 80)
    gender_id = random.randint(0, 1)  # 0 or 1
    height = random.randint(150, 200)  # 150-200cm
    
    # ランダムな登録日時
    random_days = random.randint(0, 365)
    new_time = base_date + timedelta(days=random_days)
    
    User.create(
        id=i,
        name=name,
        age=age,
        gender_id=gender_id,
        height=height,
        new_time=new_time
    )
    users_data.append({
        'id': i,
        'name': name,
        'age': age,
        'gender_id': gender_id,
        'height': height,
        'new_time': new_time.strftime('%Y-%m-%d %H:%M:%S')
    })

print(f"✓ {len(users_data)}個のユーザーデータを登録しました")
print(f"\n登録されたユーザーの例:")
for user in users_data[:5]:
    print(f"  ID:{user['id']:3d} | {user['name']:10s} | 年齢:{user['age']:2d} | 性別ID:{user['gender_id']} | 身長:{user['height']}cm | 登録日時:{user['new_time']}")
print(f"  ...")
print(f"\n合計: {User.select().count()}件のユーザーが登録されています")