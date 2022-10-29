from flask import *
from flask_restful import Resource
import json

from db.models import User

def badParams(data):
    if 'period' not in data or 'learn_count' not in data:
        return True

    if not isinstance(data['period'], int) or not isinstance(data['learn_count'], int):
        return True

    if not (20*60 <= data['period'] <= 24*60*60) or not (3 <= data['learn_count'] <= 100):
        return True

    return False

class Edit(Resource):
    def post(self):
        r = request.data
        data = json.loads(r)

        userid = g.get('user')

        user = User.select().where(User.userid == userid)
        if len(user) == 0:
            return dict(
                error=True,
                code=400,
                message='Пользователя не существует'
            )

        if badParams(data):
            return dict(
                error=True,
                code=400,
                message='Некорректные параметры'
            )
        user = user[0]
        user.period = data['period']
        user.learn_count = data['learn_count']

        user.save()

        return dict(
            error=False,
            code=200,
            message = 'Настройки сохранены'
        )