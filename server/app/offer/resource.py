from flask_restful import Resource, abort
from app import ecv
from models.offer import Offer

class OfferListResource(Resource):

    def get(self):
        return [offer.to_dict() for offer in ecv.session.query(Offer).all()]

class OfferResource(Resource):
    def get(self, offer_id):
        offer = ecv.session.query(Offer).filter_by(id=offer_id).first()
        if not offer:
            abort(404, message='Offer with id {} does not exist.'.format(offer_id))
        return offer.to_dict()
