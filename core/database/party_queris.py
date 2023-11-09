from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.database.create_table import User, Schedule, LessonsHistory, Party

engine = create_engine('sqlite:///bot.db', echo=True)


def create_party(name) -> Party:
    with Session(engine) as session:
        party = session.query(Party).filter(Party.name == name).first()

        if party:
            return False
        else:
            new_party = Party(
                name=name
            )
            session.add(new_party)
            session.commit()

            party = session.query(Party).filter(Party.name == name).first()

            return party


def get_active_party():

    session = Session(engine)
    party = session.query(Party).filter(Party.active == True).all()
    session.close()

    return party
