from peewee import AutoField, CharField, DateTimeField
import datetime
from flask_login import UserMixin

from app.database import BaseModel

class Susers(BaseModel, UserMixin):
    id = AutoField()
    username = CharField()
    password = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
