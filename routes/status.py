from flask import Blueprint, jsonify
from models import User, Attraction, Area

# Blueprintの作成 (url_prefixを /api/stats に設定)
stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')

@stats_bp.route('/')
def get_stats():
    """ユーザー、アトラクション、エリアの総数を返す API"""
    stats = {
        'users': User.select().count(),
        'attractions': Attraction.select().count(),
        'areas': Area.select().count()
    }
    return jsonify(stats)