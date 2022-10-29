from flask import *
from flask_restful import Resource, Api

from urllib.parse import urlparse, parse_qsl, urlencode
from helpers.signature_checker import is_valid

from routers.init import Init
from routers.search import Search, getByType
from routers.tasks import tasksOn, tasksOff
from routers.edit import Edit
from routers.callback import Callback

from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

secret = 'bcac3d2805f74372b89dd36379ad3ed6'
@app.before_request
def before():
    try:
        r = request.data
        data = json.loads(r)

        # print(request.url)

        if ('params' not in data) and ('secret' not in data):
            return json.dumps(
                {'error': 1, 'code': 1403, 'message': 'Отсутствуют параметры запуска'}
            ), 403

        if 'secret' not in data:
            params = data['params']
            url = 'https://example.com/{}'.format(params)
            query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
            status = is_valid(query=query_params)
            if not status:
                return json.dumps({'error': 1, 'code': 1403, 'message': 'Подделка параметров запуска'}), 403

            g.user = int(query_params['vk_user_id'])
        else:
            if data['secret'] != secret:
                return json.dumps({'error': 1, 'code': 1403, 'message': 'Подделка параметров запуска'}), 403

            g.user = 0
    except Exception as err:
        return json.dumps(
            {'error': 1, 'code': 1403, 'message': 'Подделка параметров запуска! ({})'.format(err)}
        ), 403

api.add_resource(Init, '/init')
api.add_resource(Search, '/search')
api.add_resource(getByType, '/getByType')
api.add_resource(tasksOn, '/tasksOn')
api.add_resource(tasksOff, '/tasksOff')
api.add_resource(Edit, '/edit')
api.add_resource(Callback, '/callback')


if __name__ == '__main__':
    app.run(debug=True)