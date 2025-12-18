from .home import home_bp
from .user import user_bp
from .product import product_bp
from .history import history_bp
from .order import order_bp
from .attraction import attraction_bp
from .area import area_bp
from .stats import stats_bp

# Blueprintをリストとしてまとめる
blueprints = [
  home_bp,
  user_bp,
  product_bp,
  history_bp,
  order_bp,
  attraction_bp,
  area_bp, #area_Blueprintの追加
  stats_bp
]
