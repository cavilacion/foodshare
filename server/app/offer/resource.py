from flask_restful import Resource, abort
from flask import request, json
from app import ecv
import datetime
from models.offer import Offer
from models.user import User
from app.general_responses import *
from app.publish import Publisher

class OfferListResource(Resource):

    def get(self):
        return [offer.to_dict() for offer in ecv.session.query(Offer).all()]

    def post(self):
        data = check_request_json(request)

        # Check and get host
        host_id = data.get('host_id')
        if host_id is None:
            missing_required_field('host_id')

        portions = data.get('portions')
        if portions is None:
            missing_required_field('portions')

        price = data.get('price')
        if price is None:
            missing_required_field('price')

        info = data.get('info')
        if info is None:
            missing_required_field('info')

        time_ready = data.get('time_ready')
        if time_ready is None:
            missing_required_field('time_ready')
            
        p = Publisher()
        result = p.offer(host_id=host_id,portions=portions,price=price,info=info,time_ready=time_ready)

        return result, 201

class OfferResource(Resource):
    def get(self, offer_id):
        offer = ecv.session.query(Offer).filter_by(id=offer_id).first()
        if not offer:
            abort(404, message='Offer with id {} does not exist.'.format(offer_id))
        return offer.to_dict()

    # TODO PUT request to update an offer
    def put(self, offer_id):
        # data = check_request_json(request)

        offer = ecv.session.query(Offer).filter_by(id=offer_id).first()
        if not offer:
            abort(404, message='Offer with id {} does not exist.'.format(offer_id))

        return offer.to_dict()

    def delete(self, offer_id):
        offer = ecv.session.query(Offer).filter_by(id=offer_id).first()
        if not offer:
            abort(404, message='Offer with id {} does not exist.'.format(offer_id))

        ecv.session.delete(offer)
        ecv.session.commit()

        return dict()
        
