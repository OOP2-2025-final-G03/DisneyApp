from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from peewee import fn
from models import History, User, Attraction
from datetime import datetime

# Blueprintの作成
history_bp = Blueprint('history', __name__, url_prefix='/historys')


@history_bp.route('/')
def list():
    historys = History.select()
    return render_template('history_list.html', title='履歴一覧', items=historys)


@history_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']
        attraction_id = request.form['attraction_id']
        history_date = datetime.now()
        History.create(user=user_id, attraction=attraction_id, history_date=history_date)
        return redirect(url_for('history.list'))
    
    users = User.select()
    attractions = Attraction.select()
    return render_template('history_add.html', users=users, attractions=attractions)


@history_bp.route('/edit/<int:history_id>', methods=['GET', 'POST'])
def edit(history_id):
    history = History.get_or_none(History.id == history_id)
    if not history:
        return redirect(url_for('history.list'))

    if request.method == 'POST':
        history.user = request.form['user_id']
        history.attraction = request.form['attraction_id']
        history.save()
        return redirect(url_for('history.list'))

    users = User.select()
    attractions = Attraction.select()
    return render_template('history_edit.html', history=history, users=users, attractions=attractions)

@history_bp.route('/api/attraction_monthly_totals')
def attraction_monthly_totals():
    # month: "YYYY-MM" で月を作る
    month_expr = fn.strftime('%Y-%m', History.history_date).alias('month')

    rows = (
        History
        .select(
            month_expr,
            Attraction.id.alias('attraction_id'),
            Attraction.name.alias('attraction_name'),
            fn.COUNT(History.id).alias('total')
        )
        .join(Attraction)  # History.attraction -> Attraction
        .group_by(month_expr, Attraction.id, Attraction.name)
        .order_by(month_expr, Attraction.id)
        .dicts()
    )

    return jsonify([r for r in rows])