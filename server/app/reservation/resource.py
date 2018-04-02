from flask_restful import Resource, abort
from flask import request, json
from app import ecv
import datetime
from models.reservation import Reservation
from models.offer import Offer
from models.user import User
from app.general_responses import *
from message_queue.publish import Publisher

class ReservationListResource(Resource):

    def get(self):
        return [reservation.to_dict() for reservation in ecv.session.query(Reservation).all()]

    def post(self):
        data = check_request_json(request)

        offer_id = data.get('offer_id')
        if offer_id is None:
            missing_required_field('offer_id')
        


        user_id = data.get('user_id')
        if user_id is None:
            missing_required_field('user_id')
       


        portions = data.get('portions')
        if portions is None:
            missing_required_field('portions')
        
        if ecv.testing:
            offer = ecv.session.query(Offer).filter_by(id=offer_id).first()
            if offer is None:
                abort(404, message='The offer does not exist.')
            user = ecv.session.query(User).filter_by(id=user_id).first()
            if user is None:
                abort(404, message='The user does not exist')
            reservation = Reservation(
                offer_id = offer_id, 
                user_id = user_id, 
                portions = portions, 
                timestamp = datetime.datetime.utcnow()
            )
            ecv.session.add(reservation)
            ecv.session.commit()
            return reservation.to_dict(), 201
        else:
            p = Publisher()
            result = p.reserve(user_id = user_id, offer_id = offer_id, portions=portions)
            return result, 201


class ReservationResource(Resource):
    def get(self, reservation_id):
        reservation = ecv.session.query(Reservation).filter_by(id=reservation_id).first()
        if not reservation:
            abort(404, message='Reservation with id {} does not exist.'.format(reservation_id))
        return reservation.to_dict()

    def put(self, reservation_id):
        data = check_request_json(request)
        portions = data.get('portions')
        p = Publisher()
        result = p.updatereserve(reservation_id=reservation_id, portions=portions)
        return result, 201


    def delete(self, reservation_id):
        p = Publisher()
        result = p.deletereserve(reservation_id=reservation_id)

        return dict()
