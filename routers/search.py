from flask import *
from flask_restful import Resource
import json

from db.models import Word

types = ['noun','verb','details','adj','partnverbadj','adverb'] # существительное, глагол, деепричастие, прилагательное, причастие и отглагольное прилагательное, наречие

def getByQ(q):
    words = Word.select().where(Word.word.contains(q))
    return [dict(
        word = word.word,
        description = word.description,
        interpretation = word.interpretation,
        type = word.type
    ) for word in words]

def getTypesWords(type):
    words = Word.select().where(Word.type == type)
    return [dict(
        word=word.word,
        description=word.description,
        interpretation=word.interpretation,
        type=word.type
    ) for word in words]

class Search(Resource):
    def post(self):
        r = request.data
        data = json.loads(r)

        if 'q' not in data or not isinstance(data['q'], str):
            return dict(
                error=True,
                code=400,
                message='Некорректный запрос'
            )

        result = getByQ(data['q'])
        return dict(
            error = False,
            code = 200,
            words = result
        )

class getByType(Resource):
    def post(self):
        r = request.data
        data = json.loads(r)

        if 'type' not in data or data['type'] not in types:
            return dict(
                error=True,
                code=400,
                message='Некорректный запрос'
            )

        result = getTypesWords(data['type'])
        return dict(
            error=False,
            code=200,
            words=result
        )