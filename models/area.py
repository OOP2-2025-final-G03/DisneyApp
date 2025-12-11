from peewee import Model, CharField, ForeignKeyField
from db import db
from .attraction import Attraction

class Area(Model):
    name = CharField
    attraction = ForeignKeyField(Attraction, backref='areas')

    class Meta:
        database = db