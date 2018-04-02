from flask_restful import Resource, abort
from flask import request, json
from app import ecv
from models.user import User
from models.rating import Rating
from app.general_responses import *
from app.publish import Publisher

class RatingListResource(Resource):

    def get(self):
        return [rating.to_dict() for rating in ecv.session.query(Rating).all()]
    
    def post(self):
        data = check_request_json(request)
        
        user_id = data.get('user_id')
        if user_id is None:
            missing_required_field('user_id')
            
        host_id = data.get('host_id')
        if host_id is None:
            missing_required_field('host_id')

        stars = data.get('stars')
        if stars is None:
            missing_required_field('stars')

        comment = data.get('comment')
        if comment is None:
            missing_required_field('comment')
            
        p = Publisher()
        result = p.rate(user_id=user_id,host_id=host_id,stars=stars,comment=comment)

        return result, 201

class RatingResource(Resource):
    def get(self, rating_id):
        rating = ecv.session.query(Rating).filter_by(id=rating_id).first()
        if not rating:
            abort(404, message='Rating with id {} does not exist.'.format(rating_id))
        return rating.to_dict()
