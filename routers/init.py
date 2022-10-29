from flask import *
from flask_restful import Resource
import json

from db.models import User

class Init(Resource):
    def post(self):
        userid = g.get('user')

        user = User.select().where(User.userid == userid)
        if len(user) == 0:
            user = User.create(userid=userid)

        return dict(
            error=False,
            code=200,
            user=dict(
                userid = userid,
                notify = user[0].notify,
                period = user[0].period,
                learn_count = user[0].learn_count
            )
        )