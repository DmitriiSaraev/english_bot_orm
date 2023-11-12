from datetime import datetime

from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session, aliased, joinedload

from core.database.create_table import User, StudentInParty, Party

engine = create_engine('sqlite:///bot.db', echo=True)


# Создать пользователя, если он еще не создан
def create_user(first_name,
                middle_name,
                last_name,
                chat_id,
                birthday=None,
                studies=False,
                full_name_telegram=None,
                ):

    today = datetime.now().date()

    with Session(engine) as session:
        user = session.query(User).filter(User.chat_id == chat_id).first()

        if user:
            return False
        else:
            new_user = User(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                chat_id=chat_id,
                birthday=birthday,
                registration_date=today,
                studies=studies,
                full_name_telegram=full_name_telegram,
            )

            # Добавьте экземпляр Schedule в сессию
            session.add(new_user)

            # Зафиксируйте изменения в базе данных
            session.commit()

            user = session.query(User).filter(User.chat_id == chat_id).first()

            return user


def get_student_without_party():
    def get_users_with_studies_and_empty_partys():
        with Session(engine) as session:
            users = (
                session.query(User)
                .options(joinedload(User.partys))
                .filter(~User.partys.any())
                .all()
            )

        return users

    # Использование функции
    users = get_users_with_studies_and_empty_partys()

    return users


