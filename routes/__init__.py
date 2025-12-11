from .user import user_bp
from .product import product_bp
from .order import order_bp
from .attraction import attraction_bp
from .history import history_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  product_bp,
  order_bp,
  attraction_bp,
  history_bp
]
