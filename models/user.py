from peewee import Model, CharField, IntegerField
from .db import db

class User(Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    age = IntegerField()
    gender_id = IntegerField()
    height = IntegerField()

    class Meta:
        database = db