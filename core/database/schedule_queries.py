from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime

from core.database.create_table import User, Schedule, LessonsHistory, Party

engine = create_engine('sqlite:///bot.db', echo=True)


def create_lesson(date, start_lesson, end_lesson):
    with Session(engine) as session:
        # Создайте экземпляр Schedule с необходимыми значениями
        new_schedule = Schedule(
            date=date,
            start_lesson=start_lesson,
            end_lesson=end_lesson
        )

        # Добавьте экземпляр Schedule в сессию
        session.add(new_schedule)

        # Зафиксируйте изменения в базе данных
        session.commit()


# Получить все уроки которые будут или уже были сегодня, и будующие уроки
def get_all_future_lessons():
    today = datetime.now().date()

    session = Session(engine)
    lessons = session.query(Schedule).filter(Schedule.date >= today).all()
    session.close()

    return lessons


def get_lesson_by_id(lesson_id) -> Schedule:
    with Session(engine) as session:
        lesson = session.query(Schedule).get(lesson_id)

        if lesson is not None:
            return lesson
        else:
            return "Урок не найден"


def get_students_from_lessons_history(lesson_id) -> LessonsHistory:
    with Session(engine) as session:
        results = session.query(LessonsHistory).filter(
            LessonsHistory.lesson_id == lesson_id).all()
        session.close()

        return results




