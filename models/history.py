from peewee import Model, ForeignKeyField, DateTimeField
from .db import db
from .user import User
from .product import Product

class History(Model):
    user = ForeignKeyField(User, backref='historys')
    product = ForeignKeyField(Product, backref='historys')
    history_date = DateTimeField()

    class Meta:
        database = db
