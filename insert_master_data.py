from models.db import db
from models.user import User
from models.attraction import Attraction
from models.history import History

def create_tables():
    db.create_tables([User, Attraction, History])

def insert_attractions():
    attractions = [
        {"name": "スペースマウンテン", "hight_limit": 130, "age_limit": 7},
        {"name": "ビッグサンダー・マウンテン", "hight_limit": 102, "age_limit": 5},
        {"name": "ホーンテッドマンション", "hight_limit": 0, "age_limit": 0},
        {"name": "スプラッシュマウンテン", "hight_limit": 90, "age_limit": 6},
        {"name": "カリブの海賊", "hight_limit": 0, "age_limit": 0},
        {"name": "タワー・オブ・テラー", "hight_limit": 140, "age_limit": 10},
        {"name": "イッツ・ア・スモールワールド", "hight_limit": 0, "age_limit": 0},
        {"name": "ベイマックスのハッピーライド", "hight_limit": 90, "age_limit": 4},
    ]

    for a in attractions:
        Attraction.create(**a)

def insert_users():
    users = [
        {"id": 1, "name": "田中太郎", "age": 20, "gender_id": 0, "height": 170},
        {"id": 2, "name": "佐藤花子", "age": 19, "gender_id": 1, "height": 158},
        {"id": 3, "name": "鈴木一郎", "age": 22, "gender_id": 0, "height": 175},
        {"id": 4, "name": "高橋美咲", "age": 21, "gender_id": 1, "height": 162},
        {"id": 5, "name": "伊藤健", "age": 18, "gender_id": 0, "height": 168},
    ]
    for u in users:
        User.create(**u)

if __name__ == "__main__":
    db.connect(reuse_if_open=True)
    create_tables()
    insert_users()
    insert_attractions()
    db.close()
    print("=== User / Attraction 登録完了 ===")
