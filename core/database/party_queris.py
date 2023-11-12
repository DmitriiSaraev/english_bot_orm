from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.database.create_table import User, Schedule, LessonsHistory, Party, \
    StudentInParty

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


def add_party_to_lesson(party_id, lesson_id):
    with Session(engine) as session:
        lesson = session.query(LessonsHistory).filter(
            LessonsHistory.party_id == party_id
        ).first()

        created = False

        if lesson is None:
            new_lesson = LessonsHistory(
                visit=False,
                payment=False,
                lesson_id=lesson_id,
                student_id=None,
                party_id=party_id
            )
            session.add(new_lesson)
            session.commit()

            created = True

        return lesson, created


def add_student_to_party_by_id(student_id, party_id):
    with Session(engine) as session:
        party = (session.query(StudentInParty)
                 .filter(StudentInParty.party_id == party_id)
                 .filter(StudentInParty.student_id == student_id)
                 .first()
                 )

        created = False

        if party is None:
            new_student_in_party = StudentInParty(
                party_id=party_id,
                student_id=student_id
            )
            session.add(new_student_in_party)
            session.commit()

            created = True

        return new_student_in_party, created


