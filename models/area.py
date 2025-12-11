from peewee import Model, CharField, ForeignKeyField
from db import db
from .attraction import Attraction #仮置き

class Area(Model):
    name = CharField
    attraction = ForeignKeyField(Attraction, backref='areas')

    class Meta:
        database = db