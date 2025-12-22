import insert_master_data, insert_fake_history, insert_user
from models import db, initialize_database, MODELS

if __name__ == "__main__":
    # 既存のテーブルを削除してリセットする
    db.connect()
    db.drop_tables(MODELS)
    db.close()

    # データベースを初期化して、テーブルを再作成する
    initialize_database()
    db.connect(reuse_if_open=True)
    insert_user.insert_user(100)
    insert_master_data.insert_master_data()
    insert_fake_history.insert_history()
    db.close()
    print("=== マスターデータ / 履歴 / ユーザー 登録完了 ===")