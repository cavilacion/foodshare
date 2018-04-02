import pytest
from functools import partial
from sqlalchemy import inspect
from app import ecv
from models.base import Base
from models.user import User
from models.offer import Offer
from models.reservation import Reservation

import datetime

@pytest.fixture()
def db():
    Base.metadata.drop_all(bind=ecv.engine)
    Base.metadata.create_all(bind=ecv.engine)
    return ecv

@pytest.fixture
def context(db):
    ctx = ecv.test_request_context()
    ctx.push()
    yield ctx
    ctx.pop()

@pytest.fixture
def json_header():
    return [('Content-Type', 'application/json')]

@pytest.fixture
def client(context):
    yield ecv.test_client()

@pytest.fixture
def get(client):
    return partial(client.get)

@pytest.fixture
def delete(client):
    return partial(client.delete)

@pytest.fixture
def post(client):
    return partial(client.post)

@pytest.fixture
def user(db):
    u = User(
        username='user'
    )

    db.session.add(u)
    db.session.commit()
    yield u
    if inspect(u).persistent:
        db.session.delete(u)
        db.session.commit()

@pytest.fixture
def user_host(db):
    u = User(
        username='user_host'
    )

    db.session.add(u)
    db.session.commit()
    yield u
    if inspect(u).persistent:
        db.session.delete(u)
        db.session.commit()

@pytest.fixture
def user_client(db):
    u = User(
        username='user_client'
    )

    db.session.add(u)
    db.session.commit()
    yield u
    if inspect(u).persistent:
        db.session.delete(u)
        db.session.commit()

@pytest.fixture
def offer(db, user_host):
    o = Offer(
        host_id = user_host.id,
        portions = 5,
        price = 10.50, # price is per portion
        info = 'this is a test description',
        time_ready = datetime.datetime.utcnow() + datetime.timedelta(hours=10),
        time_created = datetime.datetime.utcnow()
    )

    db.session.add(o)
    db.session.commit()

    yield o

    if inspect(o).persistent:
        db.session.delete(o)
        db.session.commit()

@pytest.fixture
def reservation(db, offer, user_client):
    r = Reservation(
        user_id = user_client.id,
        offer_id = offer.id,
        portions = 3,
        timestamp = datetime.datetime.utcnow()
    )

    db.session.add(r)
    db.session.commit()

    yield r

    if inspect(r).persistent:
        db.session.delete(r)
        db.session.commit()