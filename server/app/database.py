import datetime
import pika
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.pool import QueuePool

from models.base import Base

def create_engine_and_session(app):
    app.engine = create_engine('sqlite:///foodshare0.db', connect_args={'check_same_thread': False}) 
    Base.metadata.create_all(app.engine)

    app.session = scoped_session(sessionmaker(  autocommit=False,
                                                autoflush=True,
                                                bind=app.engine))

