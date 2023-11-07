from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.database.create_table import User, Schedule, LessonsHistory, Party

engine = create_engine('sqlite:///bot.db', echo=True)


def get_active_party():

    session = Session(engine)
    party = session.query(Party).filter(Party.active is True).all()
    session.close()

    return party
