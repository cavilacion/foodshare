from flask import Flask
from flask_restful import Api

from app import config

ecv = Flask(__name__)
ecv.config.from_object(config)

api = Api(ecv)
from app.offer.resource import OfferListResource, OfferResource
from app.rating.resource import RatingListResource, RatingResource
from app.reservation.resource import ReservationListResource, ReservationResource
from app.user.resource import UserListResource, UserResource

api.add_resource(OfferListResource, '/api/offer')
api.add_resource(OfferResource, '/api/offer/<offer_id>')
api.add_resource(RatingListResource, '/api/rating')
api.add_resource(RatingResource, '/api/rating/<rating_id>')
api.add_resource(ReservationListResource, '/api/reservation')
api.add_resource(ReservationResource, '/api/reservation/<reservation_id>')
api.add_resource(UserListResource, '/api/user')
api.add_resource(UserResource, '/api/user/<user_id>')


# publisher = Publisher()

# @ecv.route("/")
# def hello():
#     return "Hello World!"