from flask import *
from flask_restful import Resource
import json

from db.models import User

class tasksOn(Resource):
    def post(self):
        userid = g.get('user')

        user = User.select().where(User.userid == userid)
        if len(user) == 0:
            return dict(
                error=True,
                code=400,
                message='Пользователя не существует'
            )
        user = user[0]

        user.notify = True
        user.save()

        return dict(
            error=False,
            code=200,
            message='Уведомления включены'
        )


class tasksOff(Resource):
    def post(self):
        userid = g.get('user')

        user = User.select().where(User.userid == userid)
        if len(user) == 0:
            return dict(
                error=True,
                code=400,
                message='Пользователя не существует'
            )
        user = user[0]

        user.notify = False
        user.save()

        return dict(
            error=False,
            code=200,
            message='Уведомления включены'
        )