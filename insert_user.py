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

def create_users_data(num_users=100):
    """ユーザーデータを生成する関数"""
    users_data = []
    for i in range(num_users):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        age = random.randint(10, 60)
        gender_id = random.randint(0, 1)
        height = random.randint(150, 200)
        
        user = {
            "id": i + 1,
            "name": f"{first_name}{last_name}",
            "age": age,
            "gender_id": gender_id,
            "height": height,
            "new_time": random.choice([
                datetime.now() - timedelta(days=random.randint(0, 365)),
                datetime.now() - timedelta(days=random.randint(0, 365))
            ])
        }
        users_data.append(user)
    return users_data

def insert_user(num_users=100):
    """ユーザーデータを挿入する関数"""
    users_data = create_users_data(num_users)
    for user in users_data:
        User.create(**user)
    print(f"=== {num_users} 件の User 登録完了 ===")
        
if __name__ == "__main__":
    db.connect(reuse_if_open=True)
    insert_user()
    db.close()
    print("=== User 登録完了 ===")
