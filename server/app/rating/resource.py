from flask_restful import Resource, abort
from app import ecv
from models.classes import Rating

class RatingListResource(Resource):

    def get(self):
        return [rating.to_dict() for rating in ecv.session.query(Rating).all()]

class RatingResource(Resource):
    def get(self, rating_id):
        rating = ecv.session.query(Rating).filter_by(id=rating_id).first()
        if not rating:
            abort(404, message='Rating with id {} does not exist.'.format(rating_id))
        return rating.to_dict()