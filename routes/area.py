from flask import Blueprint, render_template, request, redirect, url_for
from models import Area, Attraction

# Blueprintの作成
area_bp = Blueprint('area', __name__, url_prefix='/areas')

#エリア一覧
@area_bp.route('/')
def list():
    # データ取得
    areas = Area.select()
    return render_template('area_list.html', title='エリア一覧', items=areas)

#エリア追加
@area_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        attraction_id = request.form['attraction_id']
        Area.create(name=name, attraction=attraction_id)
        return redirect(url_for('area.list'))
    
    attractions = Attraction.select()
    return render_template('area_add.html', attractions=attractions)

#エリア編集
@area_bp.route('/edit/<int:area_id>', methods=['GET', 'POST'])
def edit(area_id):
    area = Area.get_or_none(Area.id == area_id)
    if not area:
        return redirect(url_for('area.list'))
    
    if request.method == 'POST':
        area.name = request.form['name']
        area.product = request.form['attraction_id']
        area.save()
        return redirect(url_for('area.list'))
    
    attractions = Attraction.select()
    return render_template('area_edit.html', attractions=attractions)
