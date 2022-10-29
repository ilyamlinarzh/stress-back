from flask import *
from flask_restful import Resource
import json
from peewee import fn, Case, JOIN

from db.models import User, Word, ClientActive, Learned

class getRandoms(Resource):
    def post(self):
        r = request.data
        data = json.loads(r)

        userid = g.get('user')

        user = User.select().where(User.userid == userid)
        if len(user) == 0:
            return dict(
                error=True,
                code=400,
                message='Пользователь не существует'
            )

        user = user[0]

        words = Word.select(Word).join(Learned, on=(Learned.user == user), join_type=JOIN.LEFT_OUTER).order_by(fn.Rand()).limit(10)
        words = [dict(
            word=word.word,
            description=word.description,
            interpretation=word.interpretation,
            type=word.type
        ) for word in words]
        