from peewee import *
import datetime
from uuid import uuid4
import os
from pathlib import Path, PurePath

dirpath = Path(__file__).parent
basepath = PurePath(dirpath, 'tables.db')

conn = SqliteDatabase(basepath)

class BaseModel(Model):
    class Meta:
        database = conn

class User(BaseModel):
    userid = IntegerField(unique=True)
    notify = BooleanField(default=False)
    period = IntegerField(null=True, default=3600)
    learn_count = IntegerField(default=10)
    last_bot_answer = IntegerField(default=0)

class Word(BaseModel):
    word = TextField()
    description = TextField(null=True, default=None)
    interpretation = TextField(null=True, default=None)
    type = CharField()

class BotAttach(BaseModel):
    user = ForeignKeyField(User, backref='bot_attach')
    word = ForeignKeyField(Word)

class ClientActive(BaseModel):
    user = ForeignKeyField(User, backref='actives')
    word = ForeignKeyField(Word)

class Answer(BaseModel):
    user = ForeignKeyField(User, backref='answers')
    word = ForeignKeyField(Word, backref='answers')
    good = BooleanField()
    answer = TextField()

class Learned(BaseModel):
    user = ForeignKeyField(User, backref='learned')
    word = ForeignKeyField(Word, backref='learned')

conn.create_tables([User, Word,  BotAttach, Answer, Learned, ClientActive])