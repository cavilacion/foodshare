from flask_restful import Resource, abort
from app import ecv
from models.classes import Reservation

class ReservationListResource(Resource):

    def get(self):
        return [reservation.to_dict() for reservation in ecv.session.query(Reservation).all()]

class ReservationResource(Resource):
    def get(self, reservation_id):
        reservation = ecv.session.query(Reservation).filter_by(id=reservation_id).first()
        if not reservation:
            abort(404, message='Reservation with id {} does not exist.'.format(reservation_id))
        return reservation.to_dict()