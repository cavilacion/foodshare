from flask_restful import Resource, abort
from flask import request, json
from app import ecv
import datetime
from models.reservation import Reservation
from models.offer import Offer
from models.user import User
from app.general_responses import *
from app.publish import Publisher

class UserListResource(Resource):
    def get(self):
        return [user.to_dict() for user in ecv.session.query(User).all()]

    def post(self):
        data = check_request_json(request)

        # Check and get host
        username = data.get('username')
        if username is None:
            missing_required_field('username')

        username_check = ecv.session.query(User).filter_by(username=username).first()
        if username_check != None:
            abort(400, message='Username {} already exists.'.format(username))
		
        p = Publisher()
        result = p.register(username=username)

        return result, 201

class UserResource(Resource):
    def get(self, user_id):
        user = ecv.session.query(User).filter_by(id=user_id).first()
        if not user:
            abort(404, message='User with id {} does not exist.'.format(user_id))

        return user.to_dict()

    def delete(self, user_id):
        user = ecv.session.query(User).filter_by(id=user_id).first()
        if not user:
            abort(404, message='User with id {} does not exist.'.format(user_id))

        ecv.session.delete(user)
        ecv.session.commit()

        return dict()
        
