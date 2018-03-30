from flask_restful import abort
from flask import json

def missing_required_field(field):
    abort(422, message='Request data is missing required field: {}'.format(field))


def does_not_exist(name, identifier, field='id'):
    abort(404, message='{} with {} {} does not exist.'
                       ''.format(name, field, identifier))

def check_request_json(request):
    if request.mimetype != 'application/json':
        abort(415, message='Request data MIME type must be '
                        '\'application/json\'. '
                        'Received {}'.format(request.mimetype))
    try:
        data = json.loads(
            request.data,
            encoding=request.mimetype_params.get('charset')
        )
    except ValueError:
        abort(400, message='Decoding JSON has failed')

    return data
