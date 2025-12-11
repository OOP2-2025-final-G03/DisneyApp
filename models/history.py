from peewee import Model, ForeignKeyField, DateTimeField
from .db import db
from .user import User
from .attraction import Attraction

class History(Model):
    user = ForeignKeyField(User, backref='historys')
    attraction = ForeignKeyField(Attraction, backref='historys')
    history_date = DateTimeField()

    class Meta:
        database = db
