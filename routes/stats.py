from flask import Blueprint, jsonify
from models import User, Attraction, Area

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/api/stats', methods=['GET'])
def stats():
    """ユーザー、アトラクション、エリアの総数を返す API"""
    return jsonify({
        'users': User.select().count(),
        'attractions': Attraction.select().count(),
        'areas': Area.select().count(),
    })