from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.database.create_table import User


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

