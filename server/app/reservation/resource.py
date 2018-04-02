from flask_restful import Resource, abort
from flask import request, json
from app import ecv
import datetime
from models.reservation import Reservation
from models.offer import Offer
from models.user import User
from app.general_responses import *
from app.publish import Publisher

class ReservationListResource(Resource):

    def get(self):
        return [reservation.to_dict() for reservation in ecv.session.query(Reservation).all()]

    def post(self):
        data = check_request_json(request)

        offer_id = data.get('offer_id')
        if offer_id is None:
            missing_required_field('offer_id')
        
        #offer = ecv.session.query(Offer).filter_by(id=offer_id).first()
        #if offer is None:
        #    abort(404, message='The offer does not exist.')

        user_id = data.get('user_id')
        if user_id is None:
            missing_required_field('user_id')
       
        #user = ecv.session.query(User).filter_by(id=user_id).first()
        #if user is None:
        #    abort(404, message='The user does not exist')

        portions = data.get('portions')
        if portions is None:
            missing_required_field('portions')
        
        p = Publisher()
        result = p.reserve(user_id = user_id, offer_id = offer_id, portions=portions)

        return result, 201


class ReservationResource(Resource):
    def get(self, reservation_id):
        reservation = ecv.session.query(Reservation).filter_by(id=reservation_id).first()
        if not reservation:
            abort(404, message='Reservation with id {} does not exist.'.format(reservation_id))
        return reservation.to_dict()

    def delete(self, reservation_id):
        reservation = ecv.session.query(Reservation).filter_by(id=reservation_id).first()
        if not reservation:
            abort(404, message='Offer with id {} does not exist.'.format(reservation_id))

        ecv.session.delete(reservation)
        ecv.session.commit()

        return dict()
