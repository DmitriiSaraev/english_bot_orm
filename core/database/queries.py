from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.database.create_table import User

engine = create_engine('sqlite:///bot.db', echo=True)

engine.connect()

with Session(engine) as session:
    admin = User(
        first_name = 'Дмитрий',
        middle_name = 'Андреевич',
        last_name = 'Сараев',
    )


# with Session(engine) as session:
#     party = Party(
#         name='first class',
#         active=True
#     )
#
#     session.add_all([party])
#     session.commit()

#
# with Session(engine) as session:
#     admin = User(
#         first_name='Дмитрий',
#         middle_name='Андреевич',
#         last_name='Сараев',
#     )
#
#     session.add_all([admin])
#     session.commit()

# session = Session(engine)
#
# stmt = select(Party)
#
# party = session.scalars(stmt).one()
#
# users = party.users
# print(users)

# with Session(engine) as session:
#     admin = User(
#         first_name='Дмитрий',
#         middle_name='Андреевич',
#         last_name='Сараев',
#         party_id=party.id
#     )
#
#     session.add_all([admin])
#     session.commit()

# for party in session.scalars(stmt):
#     print(party.name)