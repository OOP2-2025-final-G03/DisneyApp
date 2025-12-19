from flask import Blueprint, render_template, request, redirect, url_for
from models import User

# Blueprintの作成
user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/')
def list():
    
    # データ取得
    users = User.select()

    return render_template('user_list.html', title='ユーザー一覧', items=users)


@user_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':
        # ID を自動採番
        new_id = User.get_next_id()
        name = request.form['name']
        age = request.form['age']
        gender_id = request.form['gender_id']
        height = request.form['height']

        User.create(id=new_id, name=name, age=age, gender_id=gender_id, height=height)
        return redirect(url_for('user.list'))
    
    return render_template('user_add.html')


@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return redirect(url_for('user.list'))

    if request.method == 'POST':
        user.name = request.form['name']
        user.age = request.form['age']
        user.gender_id = request.form['gender_id']
        user.height = request.form['height']
        user.save()
    
        return redirect(url_for('user.list'))

    return render_template('user_edit.html', user=user)