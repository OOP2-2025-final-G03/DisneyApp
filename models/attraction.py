from peewee import Model, CharField, IntegerField
from .db import db

class Attraction(Model):
    name = CharField()
    hight_limit = IntegerField()
    age_limit = IntegerField()

    class Meta:
        database = db