import pytest
from flask import json
import datetime
from models.reservation import Reservation

class TestReservationAPI:
    @pytest.fixture
    def url(self):
        return '/api/reservation'

    def test_get_all_reservations_empty(self, get, url):
        r = get(url)
        data = json.loads(r.data)

        assert r.status_code == 200
        assert data == []

    def test_get_all_reservations(self, get, url, reservation):
        r = get(url)
        data = json.loads(r.data)

        assert r.status_code == 200
        assert data[0]['id'] == reservation.id
        assert data[0]['offer_id'] == reservation.offer_id
        assert data[0]['portions'] == reservation.portions

    def test_create_reservation_broken_json(self, post, url, json_header):
        data = 'This is a string'
        r = post(url, headers=json_header, data=data)
        data = json.loads(r.data)

        assert r.status_code == 400

    def test_create_reservation(self, post, url, json_header, user_client, offer):
        data = json.dumps(dict(
            user_id = user_client.id,
            offer_id = offer.id,
            portions = 2
        ))
        r = post(url, headers=json_header, data=data)

        assert r.status_code == 201

    def test_create_reservation_missing_field(self, post, url, json_header, user_client, offer):
        data = json.dumps(dict(
            offer_id = offer.id,
            portions = 2
        ))
        r = post(url, headers=json_header, data=data)

        assert r.status_code == 422

        data = json.dumps(dict(
            user_id = user_client.id,
            offer_id = offer.id
        ))
        r = post(url, headers=json_header, data=data)

        assert r.status_code == 422

    def test_get_reservation(self, get, url, reservation):
        s_url = url + '/' + str(reservation.id)
        r = get(s_url)
        data = json.loads(r.data)

        assert r.status_code == 200
        assert data['id'] == reservation.id
        assert data['portions'] == reservation.portions

    def test_get_reservation_nonexistant(self, get, url, reservation):
        s_url = url + '/' + str(reservation.id+1)
        r = get(s_url)

        assert r.status_code == 404

    def test_delete_reservation(self, delete, url, reservation):
        s_url = url + '/' + str(reservation.id)
        r = delete(s_url)

        assert r.status_code == 200

    def test_delete_reservation_nonexistant(self, delete, url, reservation):
        s_url = url + '/' + str(reservation.id+1)
        r = delete(s_url)

        assert r.status_code == 404