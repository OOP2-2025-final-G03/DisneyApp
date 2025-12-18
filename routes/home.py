from flask import Blueprint, render_template
from peewee import fn
from models.history import History

# Blueprint（history_bp と区別するため home_bp）
home_bp = Blueprint('home', __name__, url_prefix='')

# 月別集計を行う関数
def get_monthly_history_counts():
    query = (
        History
        .select(
            fn.strftime('%Y-%m', History.history_date).alias('month'),
            fn.COUNT(History.id).alias('count')
        )
        .group_by(fn.strftime('%Y-%m', History.history_date))
        .order_by(fn.strftime('%Y-%m', History.history_date))
    )

    labels = [item.month for item in query]
    counts = [item.count for item in query]

    return labels, counts

@home_bp.route('/api/history_monthly_count')
def history_monthly_count():
    from peewee import fn
    from models.history import History

    query = (
        History
        .select(
            fn.strftime('%Y-%m', History.history_date).alias('month'),
            fn.COUNT(History.id).alias('count')
        )
        .group_by(fn.strftime('%Y-%m', History.history_date))
        .order_by(fn.strftime('%Y-%m', History.history_date))
    )

    labels = [item.month for item in query]
    data = [item.count for item in query]

    return {
        "labels": labels,
        "data": data
    }



@home_bp.route('/')
def index():
    labels, counts = get_monthly_history_counts()

    # TOPページ用テンプレート(index.html)に渡す
    return render_template(
        'index.html',
        title='トップページ',
        labels=labels,
        counts=counts
    )
