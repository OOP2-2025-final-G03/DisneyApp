from .user import user_bp
from .product import product_bp
from .history import history_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  product_bp,
  history_bp
]
