from models import Base
from app import ecv
import datetime
from models import User, Offer, Reservation, Rating
from app.database import create_engine_and_session


create_engine_and_session(ecv)


def setup_db():
    Base.metadata.drop_all(bind=ecv.engine)
    Base.metadata.create_all(bind=ecv.engine)

def app_fixtures():
    u1 = User(username='Sem')
    u2 = User(username='Cham')
    u3 = User(username='Jafeth')
    ecv.session.add(u1)
    ecv.session.add(u2)
    ecv.session.add(u3)

    hours = 6
    time_ready = datetime.datetime.utcnow() + datetime.timedelta(hours=hours)
    o1 = Offer(host=u1, portions=2, price=3.50, info="spaghetti gambanero, non-vegetarian", time_ready=time_ready)
    ecv.session.add(o1)

    res1 = Reservation(user=u2, offer=o1, portions=1)
    res2 = Reservation(user=u3, offer=o1, portions=1)
    ecv.session.add(res1)
    ecv.session.add(res2)

    rat1 = Rating(user=u2, host=u1, stars=2, comment="I liked the sauce, but the company was terrible! I think his father was drunk...")
    rat2 = Rating(user=u3, host=u1, stars=5, comment="had a good time =) his dad is a fun guy")
    ecv.session.add(rat1)
    ecv.session.add(rat2)
    
    # commit changes
    ecv.session.commit()

setup_db()
app_fixtures()