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
    
    @classmethod
    def get_next_id(cls):
        """次の利用可能なID を取得（連番）"""
        max_id = cls.select().count()
        if max_id == 0:
            return 1
        # 既存ID の最大値 + 1
        max_existing = cls.select().order_by(cls.id.desc()).first()
        if max_existing:
            return max_existing.id + 1
        return 1