from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, Date, Integer, Boolean, create_engine, \
    select, func, DateTime
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


engine = create_engine('sqlite:///bot.db', echo=True)


class BaseModel(DeclarativeBase):
    pass


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    middle_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    birthday: Mapped[Optional[Date]] = mapped_column(Date, default=func.now())
    registration_date: Mapped[Optional[Date]] = mapped_column(
        Date, default=func.now()
    )
    studies: Mapped[Optional[bool]] = mapped_column(Boolean)
    full_name_telegram: Mapped[Optional[str]] = mapped_column(String)
    chat_id: Mapped[Optional[int]] = mapped_column(Integer)

    parties_attending = relationship("Party", secondary="student_in_party")

    def __repr__(self):
        return (f"User(id={self.id!r}, name={self.first_name!r},"
                f" last_name={self.last_name!r})")


class Party(BaseModel):
    __tablename__ = "party"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    create_date: Mapped[Optional[Date]] = mapped_column(
        Date, default=func.now()
    )
    update_date: Mapped[Optional[Date]] = mapped_column(
        Date, default=func.now()
    )
    active: Mapped[bool] = mapped_column(Boolean)

    students_in_party = relationship("User", secondary="student_in_party",
                                     back_populates="parties_attending")

    def __repr__(self):
        return f"Party(id={self.id!r}, name={self.name!r})"


class Schedule(BaseModel):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[Date] = mapped_column(Date)
    start_lesson: Mapped[DateTime] = mapped_column(DateTime)
    end_lesson: Mapped[DateTime] = mapped_column(DateTime)


class StudentInParty(BaseModel):
    __tablename__ = "student_in_party"

    id: Mapped[int] = mapped_column(primary_key=True)
    create_date: Mapped[Date] = mapped_column(Date, default=func.now())
    update_date: Mapped[Date] = mapped_column(Date)
    party_id: Mapped[int] = mapped_column(ForeignKey("party.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    party = relationship("Party", back_populates="students_in_party")
    student = relationship("User", back_populates="parties_attending")

    def __repr__(self):
        return (f"StudentInParty(id={self.id}, party_id={self.party_id},"
                f" student_id={self.student_id})")


# class LessonsHistory(BaseModel):
#     __tablename__ = "lessons_history"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     lesson_id: Mapped[int]
#     student: Mapped[]
#     party: Mapped[]
#     visit: Mapped[bool]
#     payment: Mapped[bool]




# Провести миграции (создать таблицы)
BaseModel.metadata.create_all(engine)








