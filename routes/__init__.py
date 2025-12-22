from .home import home_bp
from .user import user_bp
from .history import history_bp
from .attraction import attraction_bp
from .area import area_bp
from .status import stats_bp

# Blueprintをリストとしてまとめる
blueprints = [
  home_bp,
  user_bp,
  history_bp,
  attraction_bp,
  area_bp, #area_Blueprintの追加
  stats_bp
]
