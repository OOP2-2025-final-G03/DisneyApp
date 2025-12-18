from flask import Flask, render_template
from models import initialize_database, User  # Userモデルをインポート
from routes import blueprints
from collections import defaultdict  # 集計用にインポート
from datetime import datetime        # 日付処理用にインポート

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
    # --- 追加: 月別集計処理 ---
    users = User.select()
    monthly_counts = defaultdict(int)

    for user in users:
        # user.new_time が文字列の場合とdatetime型の場合の両方を考慮
        if isinstance(user.new_time, str):
            # 文字列の場合は日付型に変換 (形式に合わせて調整が必要かもしれません)
            try:
                dt = datetime.strptime(user.new_time, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                # ミリ秒がない場合などの予備対応
                dt = datetime.strptime(user.new_time, '%Y-%m-%d %H:%M:%S')
        else:
            dt = user.new_time
        
        # 'YYYY-MM' の形式の文字列を取得
        month_str = dt.strftime('%Y-%m')
        monthly_counts[month_str] += 1
    
    # グラフ用に月（ラベル）と人数（データ）のリストを作成（月順にソート）
    sorted_months = sorted(monthly_counts.keys())
    counts = [monthly_counts[m] for m in sorted_months]
    # -----------------------

    # 集計データをテンプレートに渡す
    return render_template('index.html', months=sorted_months, counts=counts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)