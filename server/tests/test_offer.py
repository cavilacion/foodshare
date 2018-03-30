import pytest
from flask import json
import datetime
from models.offer import Offer

class TestOfferAPI:
    @pytest.fixture
    def url(self):
        return '/api/offer'

    def test_get_all_offers_empty(self, get, url):
        r = get(url)
        data = json.loads(r.data)

        assert r.status_code == 200
        assert data == []

    def test_get_all_offers(self, get, url, offer):
        r = get(url)
        data = json.loads(r.data)

        assert r.status_code == 200
        assert data[0]['id'] == offer.id
        assert data[0]['portions'] == offer.portions
        assert data[0]['price'] == offer.price

    def test_create_offer_broken_json(self, post, url, json_header):
        data = 'This is a string'
        r = post(url, headers=json_header, data=data)
        data = json.loads(r.data)

        assert r.status_code == 400

    def test_create_offer(self, post, url, json_header, user):
        data = json.dumps(dict(
            host_id = user.id,
            portions = 10,
            price = 10.50,
            info = 'This is really good food.',
            time_ready = datetime.datetime.utcnow().timestamp()
        ))
        r = post(url, headers=json_header, data=data)

        assert r.status_code == 201

    def test_create_offer_missing_field(self, post, url, json_header, user):
        data = json.dumps(dict(
            host_id = user.id,
            price = 10.50,
            info = 'This is really good food.',
            time_ready = datetime.datetime.utcnow().timestamp()
        ))
        r = post(url, headers=json_header, data=data)

        assert r.status_code == 422

        data = json.dumps(dict(
            host_id = user.id,
            portions = 10,
            info = 'This is really good food.',
            time_ready = datetime.datetime.utcnow().timestamp()
        ))
        r = post(url, headers=json_header, data=data)

        assert r.status_code == 422

    def test_get_offer(self, get, url, offer):
        s_url = url + '/' + str(offer.id)
        r = get(s_url)
        data = json.loads(r.data)

        assert r.status_code == 200
        assert data['id'] == offer.id
        assert data['portions'] == offer.portions
        assert data['price'] == offer.price

    def test_get_offer_nonexistant(self, get, url, offer):
        s_url = url + '/' + str(offer.id+1)
        r = get(s_url)

        assert r.status_code == 404

    def test_delete_offer(self, delete, url, offer):
        s_url = url + '/' + str(offer.id)
        r = delete(s_url)

        assert r.status_code == 200

    def test_delete_offer_nonexistant(self, delete, url, offer):
        s_url = url + '/' + str(offer.id+1)
        r = delete(s_url)

        assert r.status_code == 404