from peewee import Model, CharField, IntegerField, DateTimeField
from datetime import datetime
from .db import db

class User(Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    age = IntegerField()
    gender_id = IntegerField()
    height = IntegerField()
    new_time = DateTimeField(default=datetime.now)

    class Meta:
        database = db