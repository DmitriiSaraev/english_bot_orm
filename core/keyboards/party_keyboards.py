from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.database.create_table import User, Party
from core.utils.callback_data import MainCallbackData


def keyboard_get_students_without_group(action, students: list[User], lesson_id=None):
    # Вывести студентов для записи в группу
    builder = InlineKeyboardBuilder()

    for student in students:
        student: User
        builder.button(text=f'{student.first_name} '
                            f'{student.middle_name} '
                            f'{student.last_name}',
                       callback_data=
                       MainCallbackData(action=action,
                                        student_id=student.id,
                                        lesson_id=lesson_id))

    # builder.button(text='Показать всех учеников',
    #                callback_data=MainCallbackData
    #                (action='show_all_students',
    #                 lesson_id=lesson_id))

    builder.adjust(1, *[1 for item in students])

    return builder.as_markup()


# Для выбора группы в котороую добавить ученика
def keyboard_add_student_to_party(student_id, partys):
    builder = InlineKeyboardBuilder()

    for party in partys:
        party: Party
        builder.button(text=f'{party.name}',
                       callback_data=
                       MainCallbackData(action='add_student_to_party',
                                        student_id=student_id,
                                        party_id=party.id))

    builder.adjust(*[1 for item in partys])
    return builder.as_markup()




