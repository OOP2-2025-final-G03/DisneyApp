from flask import Blueprint, render_template, request, redirect, url_for
from models import Attraction

# Blueprintの作成
attraction_bp = Blueprint('attraction', __name__, url_prefix='/attractions')


@attraction_bp.route('/')
def list():
    
    # データ取得
    attractions = Attraction.select()

    return render_template('attraction_list.html', title='アトラクション一覧', items=attractions)


@attraction_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':
        name = request.form['name']
        hight_limit = request.form['hight_limit']
        age_limit = request.form['age_limit']
        Attraction.create(name=name, hight_limit=hight_limit, age_limit=age_limit)
        return redirect(url_for('attraction.list'))
    
    return render_template('attraction_add.html')


@attraction_bp.route('/edit/<int:attraction_id>', methods=['GET', 'POST'])
def edit(attraction_id):
    attraction = Attraction.get_or_none(Attraction.id == attraction_id)
    if not attraction:
        return redirect(url_for('attraction.list'))

    if request.method == 'POST':
        attraction.name = request.form['name']
        attraction.hight_limit = request.form['hight_limit']
        attraction.age_limit = request.form['age_limit']
        attraction.save()
        return redirect(url_for('attraction.list'))

    return render_template('attraction_edit.html', attraction=attraction)