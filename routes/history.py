from flask import Blueprint, render_template, request, redirect, url_for
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
