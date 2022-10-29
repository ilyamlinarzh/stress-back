from flask import *
from flask_restful import Resource
import json
from db.models import User
from background.helpers import messageTrue, messageFalse
from threading import Thread

class Callback(Resource):
    def post(self):
        r = request.data
        data = json.loads(r)

        if data['type'] == 'confirmation':
            return '7129928c'
        elif data['type'] == 'message_new':
            if 'payload' not in data['object'].keys():
                return 'ok'

            payload = data['object']['payload']
            if len(payload) <= 1:
                return 'ok'
            if 'action' not in payload:
                return 'ok'
            try:
                payload = json.loads(payload)
            except:
                return 'ok'

            if payload['action'] == 'answer' and 'normal' in payload:
                print(data)
                answer = payload['normal']
                user = User.select().where(User.userid == data['object']['from_id'])
                b_attach = user[0].bot_attach
                if len(b_attach) > 0:
                    goodAnswer = b_attach[0].word.word
                    if goodAnswer == answer:
                        Thread(target=messageTrue, args=(data['object']['from_id'], goodAnswer, b_attach[0].word.interpretation)).start()
                    else:
                        Thread(target=messageFalse, args=(data['object']['from_id'], goodAnswer, b_attach[0].word.interpretation)).start()


        return 'ok'